from pathlib import Path
ROOT=Path(__file__).resolve().parent
path=ROOT/'ra2/src/recomp/gen_game/recomp_0010.c'
text=path.read_text(encoding='utf-8').replace('ra2_ground_template_select_bridge();','ra2_ground_template_select_bridge(0);')
assert 'template_resume_at_004A3F9F_v6' not in text
for label,entry in [('004A3F9F',1),('004A3FA1',2)]:
    needle='L_'+label+':\n'
    print(label,'shared entries',text.count(needle))
    assert text.count(needle)>0
    text=text.replace(needle,needle+f'''    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    uint32_t template_resume_at_{label}_v6 = ra2_ground_template_select_bridge({entry});
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (template_resume_at_{label}_v6 == 0x4A4015) goto L_004A4015;
    goto L_004A45B7;
''')
path.write_text(text,encoding='utf-8',newline='\n')
path=ROOT/'make_template_probe_v6.py'
text=path.read_text(encoding='utf-8')
text=text.replace('boundary_count=phase==0 ? 2 : 0','boundary_count=(phase==0 || phase>=3) ? 2 : 0')
text=text.replace("'if (phase > 2)'","'if (phase > 4)'")
text=text.replace('0x4A3F8B,0x4A45B7,0x4A45D0','0x4A3F8B,0x4A45B7,0x4A45D0,0x4A3F9F,0x4A3FA1')
text=text.replace('if (phase==0) resume=ra2_ground_template_select_bridge();',
    'if (phase==0 || phase>=3) resume=ra2_ground_template_select_bridge(phase==0 ? 0 : phase==3 ? 1 : 2);')
path.write_text(text,encoding='utf-8',newline='\n')
