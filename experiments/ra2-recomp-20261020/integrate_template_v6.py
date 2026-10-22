from pathlib import Path
ROOT=Path(__file__).resolve().parent
path=ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text=path.read_text(encoding='utf-8')
assert 'template_resume_v6' not in text
needle='L_004A3F8B:\n'
print('selector entries:',text.count(needle))
assert text.count(needle)>0
text=text.replace(needle,needle+'''    /* 可读 C：路径方向、碾压直行与模板表回退。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t template_resume_v6 = ra2_ground_template_select_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (template_resume_v6 == 0x4A4015) goto L_004A4015;
    goto L_004A45B7;
''')
for label,skip in [('004A45B7',0),('004A45D0',1)]:
    needle='L_'+label+':\n'
    print('commit entries:',label,text.count(needle))
    text=text.replace(needle,needle+f'''    /* 可读 C：方向队列消耗、候选路段启动与失败状态清理。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    ra2_ground_template_commit_bridge({skip});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    return;
''')
path.write_text(text,encoding='utf-8',newline='\n')
path=ROOT/'ra2/CMakeLists.txt'
text=path.read_text(encoding='utf-8').replace('  src/gameplay/ground_special.c\n','  src/gameplay/ground_special.c\n  src/gameplay/ground_template.c\n')
text+='\nset_source_files_properties(src/gameplay/ground_template.c PROPERTIES COMPILE_OPTIONS "/W4;/WX;/std:c17;/utf-8")\n'
path.write_text(text,encoding='utf-8',newline='\n')
