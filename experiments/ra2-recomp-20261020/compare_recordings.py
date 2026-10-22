"""按无损解码后的 RGB 帧寻找精确匹配，独立于菜单流程是否通过。"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FFMPEG = Path(r'E:\Program Files\ffmpeg-6.0-full_build\bin\ffmpeg.exe')
FFPROBE = FFMPEG.with_name('ffprobe.exe')


def hashes(path, target):
    with target.open('wb') as out:
        subprocess.run([str(FFMPEG), '-v', 'error', '-i', str(path), '-map', '0:v:0', '-pix_fmt', 'rgb24', '-f', 'framehash', '-hash', 'sha256', '-'], stdout=out, check=True)
    rows = []
    for line in target.read_text().splitlines():
        if line.startswith('#') or not line.strip():
            continue
        fields = [item.strip() for item in line.split(',')]
        rows.append(fields[-1])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('case')
    parser.add_argument('--in-game', action='store_true')
    args = parser.parse_args()
    output = ROOT / 'evidence/pixels' / args.case
    output.mkdir(parents=True, exist_ok=True)
    tests = ROOT / 'ra2/work/tests-game'
    videos = {'original': tests / (args.case + '.original') / 'run.mkv', 'generated-c': tests / args.case / 'run.mkv'}
    streams = {}
    decoded = {}
    minimum = {}
    for mode, path in videos.items():
        minimum[mode] = 90
        if args.in_game:
            ingame, scripted = False, False
            for line in (path.parent / 'run.log').read_text(encoding='utf-8', errors='replace').splitlines():
                ingame |= '[game] Capture_Mouse()' in line
                scripted |= '[input] script done' in line
                match = re.search(r'\[record\] frame (\d+) checksum', line)
                if ingame and scripted and match:
                    minimum[mode] = max(90, int(match[1]))
                    break
            else:
                raise ValueError('没有找到战场及输入完成后的画面采样点: ' + mode)
        info = subprocess.check_output([str(FFPROBE), '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,pix_fmt,width,height', '-of', 'json', str(path)])
        streams[mode] = json.loads(info)['streams'][0]
        if streams[mode]['codec_name'] != 'ffv1':
            raise ValueError('像素对照要求 FFV1 无损录像: ' + str(path))
        decoded[mode] = hashes(path, output / (mode + '.framehash'))
    original = {}
    for i, digest in enumerate(decoded['original']):
        if i >= minimum['original']:
            original.setdefault(digest, []).append(i)
    matches = []
    for i, digest in enumerate(decoded['generated-c']):
        if i >= minimum['generated-c'] and digest in original:
            peer = min(original[digest], key=lambda n: abs(n - i))
            matches.append((i, peer, digest))
    selected = None
    if matches:
        # 优先保留录像后半段的共同画面，避免只匹配启动时的黑屏。
        selected = min(matches, key=lambda item: (abs(item[0] - len(decoded['generated-c']) * 0.75), abs(item[1] - item[0])))
        for mode, frame in (('generated-c', selected[0]), ('original', selected[1])):
            subprocess.run([str(FFMPEG), '-v', 'error', '-y', '-i', str(videos[mode]), '-vf', 'select=eq(n\\,%d)' % frame, '-frames:v', '1', str(output / (mode + '.png'))], check=True)
    result = {'case': args.case, 'streams': streams, 'frame_counts': {mode: len(rows) for mode, rows in decoded.items()},
              'exact_matching_c_frames_after_first_90': len(matches), 'unique_common_rgb_hashes': len(set(item[2] for item in matches)),
              'minimum_frame_indices': minimum, 'in_game_only': args.in_game,
              'selected': {'c_frame': selected[0], 'original_frame': selected[1], 'rgb_sha256': selected[2]} if selected else None,
              'whole_recording_identical': decoded['original'] == decoded['generated-c'], 'whole_game_equivalence_verified': False,
              'note': '帧序号按录屏时间采样，不能直接当作固定模拟步；精确匹配仅证明对应画面的 RGB 相同。'}
    (output / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
