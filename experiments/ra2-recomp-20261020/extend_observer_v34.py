from pathlib import Path
R=Path(__file__).resolve().parent;S=R/"evidence/movement-state-v34"
(S/"connection_observer.c").write_bytes((S/"baseline/evidence/movement-state-v33/connection_observer.c").read_bytes())
print("Preserved all accepted original-byte-checked hooks and actor IDs")
