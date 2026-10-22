"""保存可独立回退的移动模块源码/程序，不覆盖已有快照。"""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    stage = ROOT / 'evidence/movement-state-v2'
    report = json.loads((stage / 'runs' / args.run / 'comparison.json').read_text(encoding='utf-8'))
    exe = ROOT / 'ra2/build-original-c/ra2.exe'
    assert report['passed'] and hashlib.sha256(exe.read_bytes()).hexdigest() == report['exe_sha256']
    destination = stage / 'parts' / args.name
    assert destination.resolve().parent == (stage / 'parts').resolve()
    destination.mkdir(exist_ok=False)
    paths = {item['path'] for item in json.loads((stage / 'baseline/manifest.json').read_text(encoding='utf-8'))}
    paths.update(['ra2/build-original-c/ra2.exe', 'ra2/src/recomp/gen_game/recomp_0046.c', 'build-state-probes.ps1'])
    # 只保存已经接入 CMake 的模块，不能把尚未接入的候选代码混入已验证快照。
    cmake = (ROOT / 'ra2/CMakeLists.txt').read_text(encoding='utf-8')
    for folder in ['ra2/src/gameplay', 'ra2/src/runtime']:
        for path in (ROOT / folder).glob('ground_*'):
            stem = path.with_suffix('.c').relative_to(ROOT / 'ra2').as_posix()
            if stem in cmake:
                paths.add(path.relative_to(ROOT).as_posix())
    manifest = []
    for relative in sorted(paths):
        source = ROOT / relative
        assert source.resolve().is_relative_to(ROOT.resolve())
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        manifest.append({'path': relative, 'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
    (destination / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    (destination / 'validation-source.json').write_text(json.dumps({'run': args.run, 'exe_sha256': report['exe_sha256']}, indent=2), encoding='utf-8')
    print(json.dumps({'snapshot': str(destination), 'files': len(manifest), 'exe_sha256': report['exe_sha256']}))


if __name__ == '__main__':
    main()
