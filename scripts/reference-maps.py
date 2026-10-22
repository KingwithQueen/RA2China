"""独立验收程序；产品与构建不依赖 Python，也不调用 C 地图解码器。"""
import base64
import configparser
import hashlib
import json
import struct
import subprocess
import sys
import zlib
from pathlib import Path


def sha(data):
    return hashlib.sha1(data).hexdigest()


def resource_id(name):
    data = name.upper().encode('ascii')
    remainder = len(data) % 4
    if remainder:
        data += bytes([remainder]) + bytes([data[-remainder]]) * (3 - remainder)
    return zlib.crc32(data)


def read_ini(data):
    parser = configparser.ConfigParser(interpolation=None, strict=False, inline_comment_prefixes=(';',))
    parser.read_string('[__RA2_Map_Preamble]\n' + data.decode('cp1252').lstrip('\ufeff'))
    return parser


def lzo(data):
    """使用文档中的字典距离和立即数状态解释指令。"""
    source = iter(data)
    output = bytearray()
    state = 0

    def length(value, maximum):
        if value:
            return value
        value = maximum
        while True:
            extension = next(source)
            value += extension or 255
            if extension:
                return value

    def literals(n):
        output.extend(next(source) for _ in range(n))

    def back(distance, n):
        assert 0 < distance <= len(output)
        pattern = output[-distance:]
        output.extend((pattern * ((n + len(pattern) - 1) // len(pattern)))[:n])

    first = next(source)
    token = first
    if first > 17:
        literals(first - 17)
        state = min(first - 17, 4)
        token = next(source)
    while True:
        if token < 16 and state == 0:
            literals(length(token, 15) + 3)
            state = 4
            token = next(source)
            continue
        if token < 16:
            distance = next(source) * 4 + (token >> 2) + (2049 if state == 4 else 1)
            count, trailing = (3 if state == 4 else 2), token & 3
        elif token >= 64:
            distance = next(source) * 8 + ((token >> 2) & 7) + 1
            count, trailing = (token >> 5) + 1, token & 3
        else:
            count = length(token & (31 if token >= 32 else 7), 31 if token >= 32 else 7) + 2
            word = next(source) + (next(source) << 8)
            trailing = word & 3
            distance = (word >> 2) + (1 if token >= 32 else 16384 + ((token & 8) << 11))
            if token < 32 and distance == 16384:
                assert count == 3 and trailing == 0 and next(source, None) is None
                return bytes(output)
        back(distance, count)
        literals(trailing)
        state = trailing
        token = next(source)


def lcw(data):
    source = iter(data)
    output = bytearray()
    token = next(source)
    relative = token == 0
    if relative:
        token = next(source)
    while token != 128:
        if token < 128:
            count, distance = (token >> 4) + 3, ((token & 15) << 8) + next(source)
        elif token < 192:
            output.extend(next(source) for _ in range(token & 63))
            token = next(source)
            continue
        elif token == 254:
            count = next(source) + (next(source) << 8)
            output.extend(bytes([next(source)]) * count)
            token = next(source)
            continue
        else:
            count = next(source) + (next(source) << 8) if token == 255 else (token & 63) + 3
            position = next(source) + (next(source) << 8)
            distance = position if relative else len(output) - position
        assert 0 < distance <= len(output)
        pattern = output[-distance:]
        output.extend((pattern * ((count + len(pattern) - 1) // len(pattern)))[:count])
        token = next(source)
    assert next(source, None) is None
    return bytes(output)


def pack(ini, section, decoder):
    if section not in ini:
        return b''
    lines = ini[section]
    data = base64.b64decode(''.join(lines[str(n)] for n in range(1, len(lines) + 1)), validate=True)
    output = bytearray()
    position = 0
    while position < len(data):
        compressed, size = struct.unpack_from('<HH', data, position)
        plain = decoder(data[position + 4:position + 4 + compressed])
        assert len(plain) == size
        output.extend(plain)
        position += compressed + 4
    assert position == len(data)
    return bytes(output)


def tmp_stats(data):
    columns, rows, width, height = struct.unpack_from('<4I', data)
    assert width == 60 and height == 30
    result = dict(tiles=columns * rows, present=0, extras=0, base_bytes=0, extra_bytes=0, depth_bytes=0, sha1=sha(data))
    present = []
    for offset, in struct.iter_unpack('<I', data[16:16 + columns * rows * 4]):
        present.append(bool(offset))
        if not offset:
            continue
        x, y, extra, depth, extra_depth, ex, ey, ew, eh, flags = struct.unpack_from('<iiIIIiiiiI', data, offset)
        assert len(data[offset + 52:offset + 52 + 900]) == 900
        result['present'] += 1
        result['base_bytes'] += 900
        if flags & 2:
            assert len(data[offset + depth:offset + depth + 900]) == 900
            result['depth_bytes'] += 900
        if flags & 1:
            assert ew > 0 and eh > 0 and len(data[offset + extra:offset + extra + ew * eh]) == ew * eh
            result['extras'] += 1
            result['extra_bytes'] += ew * eh
            if flags & 2:
                assert len(data[offset + extra_depth:offset + extra_depth + ew * eh]) == ew * eh
                result['depth_bytes'] += ew * eh
    return result, present


def validate(report_path, game, tool):
    report = json.loads(Path(report_path).read_text(encoding='utf-8-sig'))

    def index(spec):
        result = json.loads(subprocess.check_output([str(tool), 'mix', spec], encoding='utf8'))
        result['entries'] = {int(e['id'], 16) if isinstance(e['id'], str) else e['id']: e for e in result['entries']}
        return result

    root = index(str(game / 'ra2.mix'))
    root_bytes = (game / 'ra2.mix').read_bytes()

    def member(archive, raw, entry_id):
        entry = archive['entries'][entry_id]
        start = archive['data_offset'] + entry['offset']
        return raw[start:start + entry['size']]

    archives = {}
    all_tmp = {}
    classified = {}
    for name in ['isogen.mix', 'isotemp.mix', 'isosnow.mix', 'isourb.mix', 'temperat.mix', 'snow.mix', 'urban.mix', 'local.mix']:
        archive = index(str(game / 'ra2.mix') + '|' + name)
        data = member(root, root_bytes, resource_id(name))
        archives[name] = (archive, data)
        if name == 'local.mix':
            continue
        for entry_id in archive['entries']:
            value = member(archive, data, entry_id)
            if len(value) >= 16 and struct.unpack_from('<II', value, 8) == (60, 30):
                all_tmp[(name, f'{entry_id:08x}')] = tmp_stats(value)
            else:
                category = 'SHP' if len(value) >= 8 and value[:2] == b'\0\0' else 'PAL' if len(value) == 768 else 'other'
                classified[category] = classified.get(category, 0) + 1
    assert len(all_tmp) == len(report['tmp_resources'])
    for expected in report['tmp_resources']:
        actual = all_tmp[(expected['archive'], expected['id'])][0]
        assert expected['ok'] and all(expected[key] == value for key, value in actual.items())

    theater_tables = {}
    for theater, filename, extension in [('TEMPERATE', 'temperat.ini', 'tem'), ('SNOW', 'snow.ini', 'sno'), ('URBAN', 'urban.ini', 'urb')]:
        ini = read_ini(member(*archives['local.mix'], resource_id(filename)))
        table = []
        n = 0
        while f'TileSet{n:04d}' in ini:
            section = ini[f'TileSet{n:04d}']
            table.extend(f"{section['filename']}{i:02d}.{extension}" for i in range(1, int(section['tilesinset']) + 1))
            n += 1
        theater_tables[theater] = table

    map_bytes = {}
    for name in ['MULTI.MIX', 'MAPS01.MIX', 'MAPS02.MIX']:
        archive = index(str(game / name))
        data = (game / name).read_bytes()
        for entry_id in archive['entries']:
            value = member(archive, data, entry_id)
            map_bytes[sha(value)] = value
    cache = {}
    probes = 0
    for expected in report['maps']:
        if expected['sha1'] not in cache:
            ini = read_ini(map_bytes[expected['sha1']])
            packed = pack(ini, 'IsoMapPack5', lzo)
            if len(packed) % 11 == 4:
                assert packed[-4:] == bytes(4)
                packed = packed[:-4]
            cells = [list(record) for record in struct.iter_unpack('<HHIBBB', packed)]
            stored = len(cells)
            width, height = map(int, ini['Map']['size'].split(',')[2:])
            coordinates = {(c[0], c[1]) for c in cells}
            left, right, y = width, width + 1, 1
            while left < right:
                for x in range(left, right):
                    if (x, y) not in coordinates:
                        cells.append([x, y, 0, 0, 0, 0])
                        coordinates.add((x, y))
                left += -1 if y < width else 1
                right += 1 if y < height else -1 if y > height else 0
                y += 1
            overlays = pack(ini, 'OverlayPack', lcw)
            overlay_data = pack(ini, 'OverlayDataPack', lcw)
            preview = pack(ini, 'PreviewPack', lzo)
            missing = 0
            missing_names = {}
            table = theater_tables[ini['Map']['theater'].upper()]
            for x, y, tile, sub, level, ice in cells:
                if tile in (65535, 0xffffffff):
                    tile, sub = 0, 0
                found = None
                if tile < len(table):
                    key = f'{resource_id(table[tile]):08x}'
                    for archive in ['isourb.mix', 'isosnow.mix', 'isotemp.mix', 'isogen.mix', 'urban.mix', 'snow.mix', 'temperat.mix']:
                        if (archive, key) in all_tmp:
                            found = all_tmp[(archive, key)][1]
                            break
                failed = found is None or sub >= len(found) or not found[sub]
                if failed:
                    name = table[tile] if tile < len(table) else str(tile)
                    missing_names[name] = missing_names.get(name, 0) + 1
                missing += failed
            object_count = sum(len(ini[s]) for s in ['Waypoints', 'Structures', 'Units', 'Infantry', 'Aircraft', 'Terrain', 'Smudge'] if s in ini)
            cache[expected['sha1']] = dict(cells=cells, stored=stored, overlay_sha1=sha(overlays), data_sha1=sha(overlay_data), preview_sha1=sha(preview),
                overlays=sum(overlays[c[0] + c[1] * 512] != 255 for c in cells) if overlays else 0, missing=missing, objects=object_count)
        actual = cache[expected['sha1']]
        assert expected['ok'] and len(actual['cells']) == expected['cells'] and actual['stored'] == expected['stored_cells']
        for key in ['overlay_sha1', 'data_sha1', 'preview_sha1', 'overlays', 'missing', 'objects']:
            assert expected[key] == actual[key], (expected['name'], key, expected[key], actual[key], missing_names if key == 'missing' else '')
        selected = [actual['cells'][n * (len(actual['cells']) - 1) // 16] for n in range(17)]
        assert selected == expected['probes']
        probes += len(selected)
    return dict(maps=len(report['maps']), unique_maps=len(cache), tmp=len(all_tmp), cell_probes=probes, full_packs_compared=len(cache) * 4,
        reference_issues_confirmed=report['summary']['missing_references'], unclassified_members=classified)


if __name__ == '__main__':
    project = Path(__file__).resolve().parent.parent
    results = []
    for report, game in zip(sys.argv[1:3], sys.argv[3:5]):
        results.append(validate(report, Path(game), project / 'build/ra2tool.exe'))
    print(json.dumps(dict(passed=True, profiles=results), ensure_ascii=False))
