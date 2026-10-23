"""Four remaining Prepare epilogues with writes, including overlapping output pointers."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v29'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+='''
void ra2_ground_prepare_written_return_bridge(unsigned entry)
{
    uint32_t frame=g_esp,result=g_eax;
    uint32_t saved_edi=MEM32(frame);
    if(entry==2)
    {
        /* Original pops EDI before the writes, then ESI/EBP/EBX afterward. */
        MEM32(g_ebp+0x58)=UINT32_MAX;
        MEM8(g_ebp+0x61)=0;
        ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result&UINT32_C(0xFFFFFF00));
        g_edi=saved_edi;
        return;
    }
    uint32_t output=MEM32(frame+0x60),saved_esi=MEM32(frame+4),saved_ebp=MEM32(frame+8);
    if(entry==1)result=output;
    else g_ecx=output;
    MEM8(output)=entry==0?(uint8_t)result:1;
    if(entry!=3)result&=UINT32_C(0xFFFFFF00);
    ra2_ground_return_frame(frame,RA2_FRAME_PREPARE,result);
    /* Output may alias saved EDI/ESI/EBP; those were already popped. EBX was not. */
    g_edi=saved_edi;g_esi=saved_esi;g_ebp=saved_ebp;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';data=p.read_bytes();assert b'\r\n' not in data;t=data.decode();t='extern void ra2_ground_prepare_written_return_bridge(unsigned entry);\n'+t
entries=[]
for entry,address,marker in [(0,'004A26FE','    ecx = MEM32(esp + 0x60); /* 0x004A26FE:'),(1,'004A28F6','    eax = MEM32(esp + 0x60); /* 0x004A28F6:'),(2,'004A2F3B','    edi = POP32_VAL(esp); /* 0x004A2F3B:'),(3,'004A3F55','    ecx = MEM32(esp + 0x60); /* 0x004A3F55:')]:
 count=t.count(marker);assert count>0
 t=t.replace(marker,f'''    /* 可读 C：带写回副作用的共享出口，保留读写与出栈顺序。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); ra2_ground_prepare_written_return_bridge({entry});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN(); return;
'''+marker)
 entries.append(dict(entry=entry,address=address,copies=count))
p.write_bytes(t.encode())
(S/'pending/shared-exit-integration.json').write_text(json.dumps(dict(passed=True,entries=entries,unique_entries=len(entries),overlapping_copies=sum(e['copies'] for e in entries),output_alias_order_preserved=True),indent=2)+'\n',encoding='utf-8')
print('Integrated written exits',entries)
