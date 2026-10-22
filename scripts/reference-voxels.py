"""独立资源验收，不被纯 C 产品或构建过程调用。"""
import json
import math
import struct
import sys
from pathlib import Path


def fnv(data):
    result = 14695981039346656037
    for value in data:
        result = ((result ^ value) * 1099511628211) & 0xffffffffffffffff
    return f"{result:016x}"


def read_vxl(data):
    count, trailers, size = struct.unpack_from("<3I", data, 20)
    assert count == trailers
    base = 802 + count * 28
    result = []
    voxels = bytearray()
    for section in range(count):
        name = data[802 + section * 28:818 + section * 28].split(b"\0")[0].decode("ascii")
        tail = base + size + section * 92
        starts, ends, source, scale = struct.unpack_from("<3If", data, tail)
        bounds = struct.unpack_from("<6f", data, tail + 64)
        x, y, z, normal_type = data[tail + 88:tail + 92]
        for column in range(x * y):
            begin, = struct.unpack_from("<I", data, base + starts + column * 4)
            if begin == 0xffffffff:
                continue
            cursor = base + source + begin
            height = 0
            while height < z:
                skip, run = data[cursor:cursor + 2]
                cursor += 2
                height += skip
                for _ in range(run):
                    color, normal = data[cursor:cursor + 2]
                    cursor += 2
                    voxels.extend((column % x, column // x, height, color, normal))
                    height += 1
                assert data[cursor] == run
                cursor += 1
        result.append({"name": name, "scale": scale or 1.0, "bounds": bounds, "size": (x, y, z)})
    return result, fnv(voxels)


def read_hva(data):
    frames, sections = struct.unpack_from("<2I", data, 16)
    names = [data[24 + i * 16:40 + i * 16].split(b"\0")[0].decode("ascii") for i in range(sections)]
    start = 24 + sections * 16
    matrices = [struct.unpack_from("<12f", data, start + i * 48) for i in range(frames * sections)]
    return frames, names, matrices, fnv(data[start:])


def verify(path):
    report = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    samples = {entry["name"]: entry for entry in report["resources"] if "raw_hex" in entry}
    vxl_count = hva_count = vpl_count = probes = 0
    for name, entry in samples.items():
        data = bytes.fromhex(entry["raw_hex"])
        if name.endswith(".vxl"):
            sections, digest = read_vxl(data)
            assert digest == entry["voxel_fnv1a64"], name
            animation = samples[name[:-4] + ".hva"]
            _, names, matrices, _ = read_hva(bytes.fromhex(animation["raw_hex"]))
            for probe in entry.get("transform_probes", []):
                section = sections[probe["section"]]
                matrix = matrices[probe["frame"] * len(names) + names.index(section["name"])]
                steps = [(section["bounds"][i + 3] - section["bounds"][i]) / section["size"][i] for i in range(3)]
                local = [section["bounds"][i] + probe["input"][i] * steps[i] for i in range(3)]
                expected = [(sum(matrix[i * 4 + j] * local[j] for j in range(3)) + matrix[i * 4 + 3] * section["scale"] * steps[i]) * section["scale"] for i in range(3)]
                assert all(math.isclose(a, b, rel_tol=2e-5, abs_tol=2e-5) for a, b in zip(expected, probe["output"])), (name, probe)
                probes += 1
            vxl_count += 1
        elif name.endswith(".hva"):
            frames, names, _, digest = read_hva(data)
            assert digest == entry["matrix_fnv1a64"] and frames == entry["frames"] and len(names) == entry["sections"]
            hva_count += 1
        else:
            start, end, count, _ = struct.unpack_from("<4I", data)
            assert start == entry["remap_start"] and end == entry["remap_end"] and count == entry["shades"]
            assert fnv(data[784:]) == entry["table_fnv1a64"]
            vpl_count += 1
    assert vxl_count and hva_count and vpl_count and probes
    return {"report": str(path), "vxl_samples": vxl_count, "hva_samples": hva_count, "vpl_samples": vpl_count, "transform_probes": probes}


print(json.dumps({"passed": True, "profiles": [verify(path) for path in sys.argv[1:]]}, ensure_ascii=False))
