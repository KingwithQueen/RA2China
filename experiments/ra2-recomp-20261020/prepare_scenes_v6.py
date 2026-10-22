from pathlib import Path
ROOT=Path(__file__).resolve().parent
FOLDER=ROOT/'evidence/movement-state-v6/fixtures'
FOLDER.mkdir(exist_ok=False)
base=(ROOT/'evidence/movement-state-v4/fixtures/dynamic-trucka.MAP').read_text(encoding='ascii')
base=base.replace('0=Player House,TRUCKA,256,67,114,64,Guard,None,0,-1,0,-1,1,1',
    '0=Player House,TRUCKA,256,67,114,64,Guard,None,0,-1,0,-1,1,1\n1=BadGuy1 House,TRUCKA,256,67,111,64,Guard,None,0,-1,0,-1,1,1')
walls=[(x,y) for x in (66,68) for y in range(107,117)]
walls += [(67,107),(67,116)]
base += ''.join(f'{i+1}=Player House,NAWALL,256,{x},{y},0,None,1,0,1,0,0,None,None,None,0,0\n'
    for i,(x,y) in enumerate(walls))
(FOLDER/'cloaked-corridor.MAP').write_text(base+'\n[TRUCKA]\nCloakable=yes\nCloakingSpeed=1\n',encoding='ascii')
text=(ROOT/'run_movement_v5_matrix.py').read_text(encoding='utf-8')
text=text.replace('movement-state-v5','movement-state-v6')
text=text.replace('fingerprint = hashlib', '''cases += [('cloaked-corridor','run_fixture_comparison.py',common+['--range','0:600','--scenario-map',
    str(FIXTURES/'cloaked-corridor.MAP'),'--order','150:1022579:2:67:108'])]
fingerprint = hashlib''')
(ROOT/'run_movement_v6_matrix.py').write_text(text,encoding='utf-8',newline='\n')
