"""只重试因场景占地冲突未成立的三格包围；原失败目录保持不变。"""
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parent;S=ROOT/'evidence/movement-state-v8'
p=S/'fixtures/dynamic-far-base.MAP'
data=(S/'fixtures/dynamic-trucka.MAP').read_text(encoding='ascii')
assert 'NAPOWR,256,62,114' in data
data=data.replace('NAPOWR,256,62,114','NAPOWR,256,60,120')
assert not p.exists();p.write_text(data,encoding='ascii',newline='\n')
with (S/'f-ur3.log').open('x',encoding='utf-8') as out:
    result=subprocess.run([sys.executable,'-B',str(ROOT/'run_fixture_comparison.py'),'--tag','f-ur3','--evidence-stage','movement-state-v8',
        '--movement-audit','--seconds','240','--range','0:350','--scenario-map',str(p),'--order','5:1022579:2:70:108',
        '--unit-ring','7:1022579:3'],cwd=ROOT,stdout=out,stderr=subprocess.STDOUT)
raise SystemExit(result.returncode)
