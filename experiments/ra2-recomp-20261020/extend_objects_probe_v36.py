"""Confirmed building gate covers signed passage limits and nonboolean flags."""
from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'evidence/movement-state-v36/objects_probe.c';t=p.read_text(encoding='utf-8')
t=t.replace('0x7039EC,0x703A23','0x7039EC,0x703A23,0x703A7F').replace('phase>9','phase>10')
mark='    const uint32_t entries[]=';assert mark in t
t=t.replace(mark,'    if(phase==10){static const int32_t limits[]={INT32_MIN,-1,0,4,5,6,7,INT32_MAX};MEM32(frame+0x8C)=(uint32_t)limits[n%8];object_type[0x1350]=(uint8_t)(n/8);}\n'+mark,1)
p.write_text(t,encoding='utf-8',newline='\n')
