"""Refine object attribution with saved ESI; link the unchanged parent completion body."""
from run_batch_v49 import *
import shlex
t=(S/'rng_observer.c').read_text(encoding='utf-8')
t=t.replace('uint32_t si,uint32_t di)','uint32_t si,uint32_t di,uint32_t stack)')
t=t.replace('    uint32_t ids[2]={0,0}', '    if(caller==0x4C394A || caller==0x4C38D0) si=U32(stack+12);\n    uint32_t ids[2]={0,0}')
t=t.replace('fxsave [esp]\npush dword ptr [ebp]', 'fxsave [esp]\nlea eax,[ebp+36]\npush eax\npush dword ptr [ebp]').replace('add esp,28','add esp,32')
if (S/'rng_attribution_observer.c').exists():assert (S/'rng_attribution_observer.c').read_bytes()==t.encode('utf-8')
else:(S/'rng_attribution_observer.c').write_text(t,encoding='utf-8',newline='\n')
t=(S/'rng_recomp_0035.c').read_text(encoding='utf-8').replace('uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);','uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);').replace(',esi,edi);',',esi,edi,esp);')
if (S/'rng_attribution_recomp.c').exists():assert (S/'rng_attribution_recomp.c').read_bytes()==t.encode('utf-8')
else:(S/'rng_attribution_recomp.c').write_text(t,encoding='utf-8',newline='\n')
data=read(S/'rng-build-arguments.json')
def rename(a):return a.replace('rng_observer','rng_attribution_observer').replace('rng_recomp_0035','rng_attribution_recomp').replace('rng-observer','rng-attribution')
data=dict(compiles=[[rename(a) for a in v] for v in data['compiles']],link=[rename(a) for a in data['link']])
for name in ['completion','landing']:
 source='ground_'+name+'.c';output='rng_baseline_'+name
 e=next(e for e in read(R/'ra2/build-original-c/compile_commands.json') if e['file'].replace('\\','/').endswith('/gameplay/'+source))
 args=[a.strip('"') for a in shlex.split(e['command'],posix=False)][1:]
 args=[('/Fo'+str(S/(output+'.obj'))) if a.startswith('/Fo') else ('/Fd'+str(S/(output+'.pdb'))) if a.startswith('/Fd') else str(S/'baseline/ra2/src/gameplay'/source) if a.replace('\\','/').endswith('/gameplay/'+source) else a for a in args]
 args+=['/I'+str(R/'ra2/src/gameplay')];data['compiles'].append(args)
 data['link']=[str(S/(output+'.obj')) if a.replace('\\','/').endswith('/gameplay/'+source+'.obj') else a for a in data['link']]
(S/'rng-attribution-build-arguments.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
