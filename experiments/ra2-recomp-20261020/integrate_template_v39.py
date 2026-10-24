"""Readable loaded-sample, destination-choice and cell-transition continuations."""
from pathlib import Path
import json
R=Path(__file__).resolve().parent;S=R/'evidence/movement-state-v39'
p=R/'ra2/src/runtime/ground_joint_bridge.c';t=p.read_text(encoding='utf-8');t+='''
static void template_compare32(uint32_t a,uint32_t b)
{g_flag_k=FK_CMP;g_flag_a=a;g_flag_b=b;g_flag_cf=a<b;}
uint32_t ra2_ground_template_continuation_bridge(unsigned entry)
{
    uint32_t frame=g_esp;
    if(entry==0)
    {
        uint32_t x=g_esi,sentinel=g_edi,index=g_edx,y=MEM32(g_ecx+4);
        g_eax=y;MEM32(frame+0x8C)=x;MEM32(frame+0x90)=y;
        template_compare32(x,sentinel);if(x!=sentinel)return 0x4A2347;
        template_compare32(y,sentinel);if(y!=sentinel)return 0x4A2347;
        template_compare32(index,sentinel);return index!=sentinel?0x4A263A:0x4A2347;
    }
    if(entry==1)
    {
        uint32_t cell=g_eax,source=g_esi,previous=g_edi,position=g_edx;
        template_compare32(cell,source);
        /* 坐标读取与写回相邻，避免重叠局部坐标被提前缓存。 */
        g_ecx=MEM32(position);MEM32(frame+0x18)=g_ecx;
        g_edx=MEM32(position+4);MEM32(frame+0x1C)=g_edx;
        g_ebx=MEM32(position+8);MEM32(frame+0x20)=g_ebx;
        if(cell==source)return 0x4A24DC;
        template_compare32(cell,previous);if(cell==previous)return 0x4A24DC;
        uint32_t progress=MEM32(g_ebp+0x4C);template_compare32(progress,3);
        return (int32_t)progress<=3?0x4A24F4:0x4A24C6;
    }
    uint32_t owner=g_ecx,position=g_edx;
    int32_t x=(int32_t)MEM32(owner+0x88),y=(int32_t)MEM32(position+4);
    MEM32(frame+0x64)=MEM32(position+8);
    int32_t target_x=(int32_t)MEM32(frame+0x18),target_y=(int32_t)MEM32(frame+0x1C);
    Ra2TemplateCells cells=ra2_ground_template_cells(ra2_ground_sample_adjusted(target_x),ra2_ground_sample_adjusted(target_y),x,y);
    g_esi=(uint32_t)cells.current_x;g_edi=(uint32_t)cells.current_y;
    g_ebx=(uint32_t)cells.target_x;g_eax=(uint32_t)cells.target_y;g_edx=target_y<0?255u:0u;
    unsigned same_x=(uint16_t)cells.target_x==(uint16_t)cells.current_x;
    g_flag_k=FK_NARROW(FK_CMP,16);
    g_flag_a=(uint32_t)(uint16_t)(same_x?cells.target_y:cells.target_x)<<16;
    g_flag_b=(uint32_t)(uint16_t)(same_x?cells.current_y:cells.current_x)<<16;
    g_flag_cf=g_flag_a<g_flag_b;
    return cells.same_cell?0x4A2607:0x4A2586;
}
''';p.write_text(t,encoding='utf-8',newline='\n')
p=R/'ra2/src/recomp/gen_game/recomp_0010.c';t=p.read_text(encoding='utf-8');records=[]
for addr,mode,mark,targets,count in [
 ('004A2326',0,'    /* cmp esi, edi */ /* 0x004A2326:',('004A2347','004A263A'),12),
 ('004A24A2',1,'    /* cmp eax, esi */ /* 0x004A24A2:',('004A24DC','004A24F4','004A24C6'),12),
 ('004A2528',2,'    eax = MEM32(ecx + 0x88); /* 0x004A2528:',('004A2607','004A2586'),13)]:
 assert t.count(mark)==count
 code='    /* 可读接续：保留有效目标选择和原生段内来源。 */\n    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT(); uint32_t continuation_'+addr+'_v39=ra2_ground_template_continuation_bridge('+str(mode)+');\n    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();\n'
 for target in targets[:-1]:code+='    if(continuation_'+addr+'_v39==0x'+target+')goto L_'+target+';\n'
 code+='    goto L_'+targets[-1]+';\n';t=t.replace(mark,code+mark);records.append(dict(entry=addr,copies=count))
p.write_bytes(('extern unsigned ra2_ground_template_continuation_bridge(unsigned entry);\n'+t).encode('utf-8'))
(S/'pending/template-integration.json').write_text(json.dumps(dict(passed=True,entries=records,new_native_entries=0),indent=2)+'\n',encoding='utf-8')
