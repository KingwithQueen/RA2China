"""独立核对原始地图 CSV 与 C 场景对象，不参与产品运行。"""
import csv
import hashlib
import json
import pathlib
import sys

checks = 0


def require(value, message):
    global checks
    checks += 1
    if not value:
        raise AssertionError(message)


def ini(path):
    section = ""
    result = {}
    by_line = {}
    data = pathlib.Path(path).read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    text = data.decode("cp1252")
    for line, raw in enumerate(text.split("\n"), 1):
        raw = raw.split(";", 1)[0].strip()
        if raw.startswith("[") and raw.endswith("]"):
            section = raw[1:-1].strip().lower()
        elif "=" in raw:
            key, value = raw.split("=", 1)
            entry = (line, section, key.strip().lower(), value.strip())
            result[(section, key.strip().lower())] = entry
            by_line[line] = entry
    return result, by_line


def value(data, section, key, default=""):
    entry = data.get((section.lower(), key.lower()))
    return entry[3] if entry else default


def run(corpus_path):
    corpus = json.loads(pathlib.Path(corpus_path).read_text(encoding="utf-8-sig"))
    root = pathlib.Path(corpus["maps"][0]["source_file"]).parent
    rules_path = root / "rules.ini"
    art_path = root / "art.ini"
    require(hashlib.sha1(rules_path.read_bytes()).hexdigest() == corpus["rules_sha1"], "rules bytes differ")
    require(hashlib.sha1(art_path.read_bytes()).hexdigest() == corpus["art_sha1"], "art bytes differ")
    rules, _ = ini(rules_path)
    buildings = units = pending = 0
    missing = []
    for sample in corpus["maps"]:
        local, lines = ini(sample["source_file"])
        owner_teams = {h["id"].lower(): h["team"] for h in sample["houses"]}
        produced = {h["team"]: 0 for h in sample["houses"]}
        consumed = produced.copy()
        original = [e for e in local.values() if e[1] in ("structures", "units", "infantry", "aircraft")]
        require(len(original) == len(sample["objects"]) + len(sample["pending_objects"]), f"{sample['map']}: objects silently lost")
        seen = set()
        for obj in sample["objects"]:
            require(obj["line"] in lines, "source line missing")
            line, section, key, text = lines[obj["line"]]
            fields = next(csv.reader([text]))
            label = f"{sample['map']}:{line}:{obj['type']}"
            require(line not in seen, label + ": duplicate object")
            seen.add(line)
            require(section == ("structures" if obj["structure"] else "units"), label + ": kind differs")
            require(fields[0].strip() == obj["owner"] and fields[1].strip() == obj["type"], label + ": owner/type differs")
            require(int(fields[3]) == obj["x"] and int(fields[4]) == obj["y"], label + ": coordinates differ")
            require(int(fields[5]) == obj["facing"], label + ": facing differs")
            raw_health = int(fields[2])
            global_strength = value(rules, obj["type"], "Strength", "0")
            strength = int(value(local, obj["type"], "Strength", global_strength) if obj["structure"] else global_strength)
            require(strength == obj["strength"] and strength > 0, label + ": local Strength differs")
            health = strength * raw_health // 256
            if raw_health and not health:
                health = 1
            require(health == obj["health"], label + ": initial health differs")
            if obj["structure"]:
                buildings += 1
                team = owner_teams[obj["owner"].lower()]
                power = int(value(local, obj["type"], "Power", value(rules, obj["type"], "Power", "0")))
                if health:
                    if power > 0:
                        produced[team] += power * health // strength
                    else:
                        consumed[team] -= power
            else:
                units += 1
        for entry in sample["pending_objects"]:
            require(entry["line"] in lines and entry["line"] not in seen, "pending object source differs")
            seen.add(entry["line"])
            pending += 1
        for house in sample["houses"]:
            require(produced[house["team"]] == house["power"] and consumed[house["team"]] == house["drain"], "house power differs")
            expected = 1 << (house["team"] - 1)
            for ally in value(local, house["id"], "Allies").split(","):
                ally = ally.strip()
                name = value(local, "Houses", ally, ally).lower()
                if name in owner_teams:
                    expected |= 1 << (owner_teams[name] - 1)
            require(expected == house["allies"], "house alliance differs")
        for visual in sample["visuals"]:
            if visual.get("missing"):
                missing.append({"map": sample["map"], "type": visual["id"], "reason": visual["reason"]})
            else:
                require(visual["normal_pixels"] > 0 and visual["damaged_pixels"] > 0, "empty building composite")
                require(len(visual["normal_sha1"]) == 40 and len(visual["damaged_sha1"]) == 40, "image hash missing")
        require(not sample["script_runtime"] and not sample["complete_campaign"] and not sample["complete_skirmish"], "coverage claims exceed implementation")
    return {"passed": True, "checks": checks, "maps": len(corpus["maps"]), "structures": buildings, "tanks": units,
            "pending_objects": pending, "missing_visuals": missing, "reference": "original map CSV and rule bytes"}


if __name__ == "__main__":
    try:
        record = run(sys.argv[1])
    except Exception as error:
        record = {"passed": False, "checks": checks, "error": str(error)}
    pathlib.Path(sys.argv[2]).write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: item for key, item in record.items() if key != "missing_visuals"}, ensure_ascii=False))
    sys.exit(0 if record["passed"] else 1)
