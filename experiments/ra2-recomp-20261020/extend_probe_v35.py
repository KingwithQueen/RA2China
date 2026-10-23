"""Round-28 native boundary cases; keep all previous phase recipes intact."""
from pathlib import Path
R = Path(__file__).resolve().parent
S = R / 'evidence/movement-state-v35'

def change(path, old, new):
    data = path.read_bytes()
    nl = '\r\n' if b'\r\n' in data else '\n'
    text = data.decode('utf-8').replace('\r\n', '\n')
    assert text.count(old) == 1, (path, old[:60])
    path.write_bytes(text.replace(old, new).replace('\n', nl).encode('utf-8'))

p = S / 'overlap_probe.c'
change(p, 'cells[0x180]', 'cells[0x300]')
change(p, 'static uint16_t control,native_cw,native_sw;', 'static uint16_t control,native_cw,native_sw;\nstatic uint32_t native_flags;')
change(p, ' fnstcw native_cw', ' pushfd\n pop native_flags\n fnstcw native_cw')
change(p, 'STOP(sample_stop,04A186Ch)', 'STOP(layer_stop,04A18EFh) STOP(sample_stop,04A186Ch)')
change(p, ' if(native_return){', ''' if(phase==4){entry=0x4A18AB;is=P(cells);ib=P(cells+0x180);cells[0x11B]=(uint8_t)n;cells[0x180+0x11B]=(uint8_t)(n%2?n-4:n/256);U(cells+0x140)=(n>>8)&1?0x100:0;U(cells+0x180+0x140)=(n>>9)&1?0x100:0;units[0][0x79]=(uint8_t)(n>>10);}
 if(native_return){''')
change(p, ' if(phase==2)c->locals[0]=U(frame+0x88);', ' if(phase==2)c->locals[0]=U(frame+0x88);\n if(phase==4)c->locals[0]=U(frame+0x40);')
change(p, ' if(phase==2){patch(0x70346B,P(chain_stop));patch(0x703905,P(chain_empty_stop));}', ' if(phase==2){patch(0x70346B,P(chain_stop));patch(0x703905,P(chain_empty_stop));}\n if(phase==4)patch(0x4A18EF,P(layer_stop));')
change(p, ' else ra2_ground_passage_return_bridge(n%5);', ' else if(phase==4)result=ra2_ground_template_layer_bridge();\n else ra2_ground_passage_return_bridge(n%5);')
change(p, ' if(phase==2)abi|=g_eax!=native_ax;', ''' if(phase==2)abi|=g_eax!=native_ax;
 if(phase==4){abi|=g_eax!=native_ax;uint32_t flags=recomp_eflags(g_flag_k,g_flag_a,g_flag_b,g_flag_cf,0);abi|=((flags^native_flags)&0x8C5u)!=0;}''')
p = R / 'run_lifecycle_part_v35.py'
change(p, "'prepare-type-gate-probe-verified-01.json'", "'prepare-type-gate-probe-verified-01.json','template-layer-probe-verified-01.json'")
print('Added 65536 native template layer cases including live flags')
