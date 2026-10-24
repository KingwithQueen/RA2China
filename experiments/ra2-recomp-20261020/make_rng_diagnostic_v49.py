"""Read-only RNG call provenance; independent host, no production source changes."""
from run_batch_v49 import *
import shlex
out=S/'baseline-observer';out.mkdir();entries=[]
for p in [S/n for n in ['bridge_catalog_observer.c','bridge-catalog-observer.exe','bridge-catalog-build-arguments.json']]+[R/n for n in ['make_bridge_catalog_v49.py','build-bridge-catalog-v49.ps1','run_bridge_catalog_v49.py']]:
 d=out/p.name;shutil.copy2(p,d);entries.append(dict(path=p.name,sha256=sha(d)))
write(out/'manifest.json',entries)
t=(S/'bridge_catalog_observer.c').read_text(encoding='utf-8')
logger=r'''
/* 独立只读诊断：不调用随机服务、不修改世界和随机状态。 */
void fixture_rng_observe(uint32_t kind,uint32_t context,uint32_t caller,uint32_t low,uint32_t high,uint32_t si,uint32_t di)
{
    uint32_t frame=U32(FRAME_ADDRESS),scenario=U32(0xA3D290);
    if(frame<1027 || frame>1046 || !scenario || context!=scenario+0x218) return;
    static FILE *output;
    if(!output){char path[MAX_PATH+16];snprintf(path,sizeof(path),"%s.rng.jsonl",state_path);output=fopen(path,"wb");if(!output)fail("RNG diagnostic output");}
    uint32_t ids[2]={0,0},values[2]={si,di};
    for(unsigned j=0;j<2;++j)for(uint32_t i=0;i<U32(0xA40C30);++i){uint32_t p=U32(U32(0xA40C24)+i*4);if(p==values[j])ids[j]=U32(p+0x10);}
    uint32_t a=U32(context+4),b=U32(context+8);
    if(a>=250 || b>=250)fail("RNG diagnostic index");
    fprintf(output,"{\"frame\":%u,\"kind\":%u,\"caller\":%u,\"indices\":[%u,%u],\"bounds\":[%d,%d],\"word\":%u,\"object_ids\":[%u,%u]}\n",frame,kind,caller,a,b,(int32_t)low,(int32_t)high,U32(context+12+a*4)^U32(context+12+b*4),ids[0],ids[1]);
    fflush(output);
}
'''
hooks=''
for kind,name,context,return_offset in [(0,'next','24',36),(1,'range','24',36),(2,'draw','20',52)]:
 hooks+='static void *rng_'+name+'_trampoline;\nstatic __declspec(naked) void rng_'+name+'_hook(void){__asm{\n'
 hooks+='pushfd\npushad\nmov ebp,esp\nsub esp,528\nand esp,-16\nfxsave [esp]\n'
 hooks+='push dword ptr [ebp]\npush dword ptr [ebp+4]\n'
 if kind==1:hooks+='push dword ptr [ebp+44]\npush dword ptr [ebp+40]\n'
 else:hooks+='push 0\npush 0\n'
 hooks+=f'push dword ptr [ebp+{return_offset}]\npush dword ptr [ebp+{context}]\npush {kind}\ncall fixture_rng_observe\nadd esp,28\nfxrstor [esp]\nmov esp,ebp\npopad\npopfd\njmp dword ptr [rng_{name}_trampoline]\n}}}}\n'
marker='void ra2_state_install_original(uint32_t base)'
assert t.count(marker)==1;t=t.replace(marker,logger+hooks+'\n'+marker)
marker='    install_hook(0x0053D890, tick_bytes'
assert t.count(marker)==1
t=t.replace(marker,'''    static const uint8_t rng_next_bytes[]={0x8B,0x41,0x04,0x8B,0x51,0x08};
    static const uint8_t rng_range_bytes[]={0x8B,0x44,0x24,0x04,0x8B,0xD1};
    static const uint8_t rng_draw_bytes[]={0x8B,0x4A,0x04,0x8B,0x74,0x8A,0x0C};
    install_hook(0x638848,rng_next_bytes,sizeof(rng_next_bytes),rng_next_hook,&rng_next_trampoline);
    install_hook(0x6388A0,rng_range_bytes,sizeof(rng_range_bytes),rng_range_hook,&rng_range_trampoline);
    install_hook(0x6388F7,rng_draw_bytes,sizeof(rng_draw_bytes),rng_draw_hook,&rng_draw_trampoline);
'''+marker)
(S/'rng_observer.c').write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0035.c';t=p.read_text(encoding='utf-8')
declaration='extern void fixture_rng_observe(uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t,uint32_t);\n'
t=declaration+t
for va in ['00638840','006388A0']:
 marker=f'    RECOMP_ENTER(0x{va}u);';assert t.count(marker)==1;t=t.replace(marker,'    uint32_t fixture_caller=g_cur_func;\n'+marker)
for va,call in [('00638848','0,ecx,fixture_caller,0,0,esi,edi'),('006388A0','1,ecx,fixture_caller,MEM32(esp+4),MEM32(esp+8),esi,edi'),('006388F7','2,edx,fixture_caller,ebx,ebx+edi,esi,edi')]:
 marker='L_'+va+':';assert t.count(marker)==1;t=t.replace(marker,marker+'\n    fixture_rng_observe('+call+');')
(S/'rng_recomp_0035.c').write_text(t,encoding='utf-8',newline='\n')
commands=read(R/'ra2/build-original-c/compile_commands.json');data=read(S/'bridge-catalog-build-arguments.json')
data['compiles'][0]=[a.replace('bridge_catalog_observer','rng_observer') for a in data['compiles'][0]]+['/utf-8']
e=next(e for e in commands if e['file'].replace('\\','/').endswith('/gen_game/recomp_0035.c'))
args=[a.strip('"') for a in shlex.split(e['command'],posix=False)][1:]
args=[('/Fo'+str(S/'rng_recomp_0035.obj')) if a.startswith('/Fo') else ('/Fd'+str(S/'rng_recomp_0035.pdb')) if a.startswith('/Fd') else str(S/'rng_recomp_0035.c') if a.replace('\\','/').endswith('/gen_game/recomp_0035.c') else a for a in args]
args+=['/I'+str(R/'ra2/src/recomp/gen_game'),'/utf-8'];data['compiles'].append(args)
data['link']=[str(S/'rng_recomp_0035.obj') if a.replace('\\','/').endswith('/gen_game/recomp_0035.c.obj') else a.replace('bridge_catalog_observer','rng_observer').replace('bridge-catalog-observer','rng-observer') for a in data['link']]
write(S/'rng-build-arguments.json',data)
p=R/'build-bridge-catalog-v49.ps1';(R/'build-rng-diagnostic-v49.ps1').write_text(p.read_text(encoding='utf-8').replace('bridge-catalog-build-arguments','rng-build-arguments'),encoding='utf-8',newline='\n')
p=R/'run_bridge_catalog_v49.py';(R/'run_rng_diagnostic_v49.py').write_text(p.read_text(encoding='utf-8').replace('bridge-catalog-observer.exe','rng-observer.exe'),encoding='utf-8',newline='\n')
write(S/'rng-diagnostic-inputs.json',dict(passed=True,production_exe_sha256=sha(R/'ra2/build-original-c/ra2.exe'),generated_source_sha256=sha(R/'ra2/src/recomp/gen_game/recomp_0035.c'),observer_sha256=sha(S/'rng_observer.c'),copied_generated_sha256=sha(S/'rng_recomp_0035.c'),frame_range=[1027,1046],read_only=True,production_rng_unchanged=True))
