"""独立验收用参考解码器；产品库和查看器不依赖 Python。"""
import json
import struct
import sys
from pathlib import Path


def shp_hash(data):
    zero, width, height, frames = struct.unpack_from("<4H", data)
    assert zero == 0
    digest = 14695981039346656037
    modes = set()
    for number in range(frames):
        x, y, w, h, flags, _, _, offset = struct.unpack_from("<4H4I", data, 8 + number * 24)
        pixels = bytearray(width * height)
        if offset and w and h:
            modes.add(flags & 3)
            cursor = offset
            for row in range(h):
                if flags & 2:
                    length, = struct.unpack_from("<H", data, cursor)
                    encoded = data[cursor + 2:cursor + length]
                    decoded = []
                    at = 0
                    while at < len(encoded):
                        value = encoded[at]
                        at += 1
                        if value:
                            decoded.append(value)
                        else:
                            decoded.extend([0] * encoded[at])
                            at += 1
                    decoded = (decoded + [0] * w)[:w]
                    cursor += length
                else:
                    decoded = data[cursor:cursor + w]
                    cursor += w
                start = (y + row) * width + x
                pixels[start:start + w] = bytes(decoded)
        for value in pixels:
            digest = ((digest ^ value) * 1099511628211) & 0xffffffffffffffff
    return f"{digest:016x}", modes


def csf_entries(data):
    signature, version, count, strings, reserved, language = struct.unpack_from("<4s5I", data)
    assert signature == b" FSC" and version in (2, 3)
    cursor = 24
    result = []
    seen_strings = 0
    for _ in range(count):
        tag, values, length = struct.unpack_from("<4s2I", data, cursor)
        assert tag == b" LBL"
        cursor += 12
        label = data[cursor:cursor + length].decode("ascii")
        cursor += length
        texts = []
        for _ in range(values):
            tag, units = struct.unpack_from("<4sI", data, cursor)
            assert tag in (b" RTS", b"WRTS")
            cursor += 8
            text = bytes(value ^ 255 for value in data[cursor:cursor + units * 2]).decode("utf-16-le")
            texts.append(text)
            cursor += units * 2
            if tag == b"WRTS":
                extra, = struct.unpack_from("<I", data, cursor)
                cursor += 4 + extra
            seen_strings += 1
        result.append({"label": label, "values": texts})
    assert cursor == len(data) and seen_strings == strings
    return result


def check(path):
    report = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    images = []
    palettes = 0
    modes = set()
    for item in report["resources"]:
        if "raw_hex" not in item:
            continue
        data = bytes.fromhex(item["raw_hex"])
        if item["name"].endswith(".pal"):
            rgb = bytes((value << 2) | (value >> 4) for value in data)
            assert rgb.hex() == item["rgb_hex"], item["name"]
            palettes += 1
        else:
            digest, used_modes = shp_hash(data)
            assert digest == item["pixel_fnv1a64"], item["name"]
            images.append(item["name"])
            modes.update(used_modes)
    texts = csf_entries(bytes.fromhex(report["csf"]["raw_hex"]))
    assert texts == report["csf"]["entries"]
    assert images and palettes and texts
    return {"report": str(path), "shp_samples": images, "palette_samples": palettes, "csf_labels": len(texts), "frame_modes": sorted(modes)}


print(json.dumps({"passed": True, "profiles": [check(path) for path in sys.argv[1:]]}, ensure_ascii=False))
