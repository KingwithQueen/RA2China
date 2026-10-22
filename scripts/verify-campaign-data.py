"""独立读取保留的原始 INI，与 C 运行报告核对任务记录和未支持对象。"""
import collections
import hashlib
import json
import sys
from pathlib import Path

source, runtime, output = map(Path, sys.argv[1:4])
raw = source.read_bytes()
sections = collections.defaultdict(dict)
section = ""
for row in raw.decode("utf-8-sig").splitlines():
    row = row.split(";", 1)[0].strip()
    if row.startswith("[") and row.endswith("]"):
        section = row[1:-1]
    elif "=" in row:
        key, value = row.split("=", 1)
        sections[section][key.strip()] = value.strip()
report = json.loads(runtime.read_text(encoding="utf-8-sig"))
checks = 0

def check(condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f"independent campaign check {checks} failed")

check(hashlib.sha1(raw).hexdigest() == report["map_sha1"])
for name, field in [("Triggers", "triggers"), ("TeamTypes", "teams"), ("CellTags", "cell_tags")]:
    check(len(sections[name]) == report[field])
for identifier in sections["Triggers"]:
    check(len(sections["Triggers"][identifier].split(",")) == 8)
    events = sections["Events"][identifier].split(",")
    actions = sections["Actions"][identifier].split(",")
    check(len(events) == 1 + int(events[0]) * 3)
    check(len(actions) == 1 + int(actions[0]) * 8)
    check(all(int(events[1 + n * 3]) < 128 for n in range(int(events[0]))))
    for n in range(int(actions[0])):
        if int(actions[1 + n * 8]) in (12, 22, 53, 54):
            check(actions[3 + n * 8] in sections["Triggers"])
for identifier, value in sections["Tags"].items():
    check(value.split(",")[2] in sections["Triggers"])
for cell, tag in sections["CellTags"].items():
    check(tag in sections["Tags"])
    check(0 <= int(cell) % 1000 < 512 and 0 <= int(cell) // 1000 < 512)
for identifier in sections["TeamTypes"].values():
    check(sections[identifier]["TaskForce"] in sections)
    check(sections[identifier]["Script"] in sections)
unsupported = {"DRED", "V3", "ADOG"} if report["simulation"] < 11 else set()
expected = collections.Counter()
for section in ("Units", "Infantry", "Aircraft"):
    for record in sections[section].values():
        name = record.split(",")[1]
        if name in unsupported:
            expected[name] += 1
actual = collections.Counter(record["type"] for record in report["missing_objects"])
check(actual == expected)
check(report["complete_original_mission"] is False)
if report["simulation"] >= 11:
    check(report["initial_objects"] == sum(len(sections[name]) for name in ("Units", "Infantry", "Aircraft", "Structures")))
    if len(sys.argv) > 4:
        rules = collections.defaultdict(dict)
        section = ""
        for row in Path(sys.argv[4]).read_text(encoding="utf-8-sig").splitlines():
            row = row.split(";", 1)[0].strip()
            if row.startswith("[") and row.endswith("]"):
                section = row[1:-1]
            elif "=" in row:
                key, value = row.split("=", 1)
                rules[section][key.strip()] = value.strip()
        catalogs = {name: list(dict.fromkeys(values.values())) for name, values in rules.items() if name.endswith("Types")}
        for trigger in report["trigger_status"]:
            raw_events = sections["Events"][trigger["id"]].split(",")
            for i, event in enumerate(trigger["events"]):
                kind, arg = int(raw_events[1 + i * 3]), int(raw_events[3 + i * 3])
                check(event["kind"] == kind)
                if kind in (19, 20, 21, 22, 32, 57):
                    catalog = {20: "VehicleTypes", 21: "InfantryTypes", 22: "AircraftTypes"}.get(kind, "BuildingTypes")
                    name = catalogs[catalog][arg]
                    expected_id = report["type_ids"].index(name) if name in report["type_ids"] else -1
                    check(event["argument"] == expected_id)
output.write_text(json.dumps({"passed": True, "checks": checks, "source_sha1": hashlib.sha1(raw).hexdigest(), "missing_original_objects": dict(expected)}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"checks": checks, "passed": True}))
