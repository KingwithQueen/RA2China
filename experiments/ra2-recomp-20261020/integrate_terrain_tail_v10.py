from pathlib import Path
ROOT=Path(__file__).resolve().parent
p=ROOT/'ra2/src/recomp/gen_game/recomp_0046.c';t=p.read_text(encoding='utf-8')
needle='L_00703905:\n';assert needle in t and 'ra2_ground_terrain_tail_bridge()' not in t
code='''    /* 可读 C：地面速度为零时硬阻挡，上层占用跳过地形速度限制。 */
    RECOMP_FLAGS_OUT(); RECOMP_REGS_OUT();
    int terrain_tail_blocked_v10 = ra2_ground_terrain_tail_bridge();
    RECOMP_REGS_IN(); RECOMP_FLAGS_IN();
    if (terrain_tail_blocked_v10) goto L_00703B5A;
    goto L_00703AA9;
'''
t=t.replace(needle,needle+code);p.write_text(t,encoding='utf-8',newline='\n')
