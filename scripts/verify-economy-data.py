"""独立读取原始 INI 与压缩矿藏；不依赖产品的 C 规则和地图解码器。"""
import hashlib
import importlib.util
import json
import math
import sys
from decimal import Decimal
from pathlib import Path


def ini(data):
    result = {}
    section = ""
    for line in data.decode("cp1252").splitlines():
        line = line.split(";", 1)[0].strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].lower()
            result.setdefault(section, {})
        elif section and "=" in line:
            key, value = line.split("=", 1)
            result[section][key.strip().lower()] = value.strip()
    return result


def main():
    report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8-sig"))
    sources = Path(sys.argv[2])
    raw_rules = (sources / "rules.ini").read_bytes()
    assert hashlib.sha1(raw_rules).hexdigest() == report["rules_sha1"]
    rules = ini(raw_rules)
    art = ini((sources / "art.ini").read_bytes())
    checks = 1
    for row in report["types"]:
        definition = rules[row["id"].lower()]
        cost = int(definition.get("cost", 0))
        ticks = max(1, math.ceil(cost * Decimal(rules["general"]["buildspeed"]) * 900 * Decimal(definition.get("buildtimemultiplier", "1")) / 1000))
        expected = dict(cost=cost, ticks=ticks, tech=int(definition.get("techlevel", -1)), storage=int(definition.get("storage", 0)),
                        adjacent=int(definition.get("adjacent", 2)), factory={"buildingtype": 1, "unittype": 2}.get(definition.get("factory", "").lower(), 0),
                        power=int(definition.get("power", 0)), harvester=definition.get("harvester", "no").lower() == "yes",
                        chrono=definition.get("harvester", "no").lower() == "yes" and definition.get("teleporter", "no").lower() == "yes")
        if row["foundation"] != [0, 0]:
            expected["foundation"] = [int(v) for v in art[definition.get("image", row["id"]).lower()]["foundation"].split("x")]
        for key, value in expected.items():
            assert row[key] == value, (row["id"], key, row[key], value)
            checks += 1
    spec = importlib.util.spec_from_file_location("reference_maps", Path(__file__).with_name("reference-maps.py"))
    maps = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(maps)
    raw_map = next(p.read_bytes() for p in sources.glob("*.map.ini") if hashlib.sha1(p.read_bytes()).hexdigest() == report["map_sha1"])
    parsed = maps.read_ini(raw_map)
    overlay = maps.pack(parsed, "OverlayPack", maps.lcw)
    density = maps.pack(parsed, "OverlayDataPack", maps.lcw)
    names = list(rules["overlaytypes"].values())
    cells, amounts = [0, 0], [0, 0]
    maximum = 0
    for cell, value in enumerate(overlay):
        name = names[value] if value < len(names) else ""
        kind = 1 if name.startswith("GEM") else 0 if name.startswith(("TIB", "GOLD")) else -1
        if kind < 0:
            continue
        cells[kind] += 1
        amounts[kind] += density[cell] + 1
        maximum = max(maximum, density[cell])
        checks += 1
    assert [report["ore_cells"], report["gem_cells"]] == cells
    assert [report["ore_amount"], report["gem_amount"]] == amounts
    assert report["max_density_index"] == maximum
    assert report["ore_frames"] >= 12 and report["gem_frames"] >= 12
    print(json.dumps(dict(passed=True, checks=checks + 4, types=len(report["types"]), cells=sum(cells), amounts=amounts)))


if __name__ == "__main__":
    main()
