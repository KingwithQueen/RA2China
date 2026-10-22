0054E3A0: mov ecx, dword ptr [esp + 4]
0054E3A4: movsx eax, word ptr [ecx + 2]
0054E3A8: movsx edx, word ptr [ecx]
0054E3AB: shl eax, 9
0054E3AE: add eax, edx
0054E3B0: js 0x54e3c6
0054E3B2: cmp eax, 0x40000
0054E3B7: jge 0x54e3c6
0054E3B9: mov edx, dword ptr [0x832618]
0054E3BF: mov eax, dword ptr [edx + eax*4]
0054E3C2: test eax, eax
0054E3C4: jne 0x54e3d2
0054E3C6: mov eax, dword ptr [ecx]
0054E3C8: mov dword ptr [0xa6fa1c], eax
0054E3CD: mov eax, 0xa6f9f8
0054E3D2: mov ecx, dword ptr [eax + 0x24]
0054E3D5: push esi
0054E3D6: mov dword ptr [esp + 8], ecx
0054E3DA: movsx eax, word ptr [esp + 0xa]
0054E3DF: cdq 
0054E3E0: and edx, 3
0054E3E3: add eax, edx
0054E3E5: sar eax, 2
0054E3E8: mov esi, eax
0054E3EA: shl esi, 6
0054E3ED: add esi, eax
0054E3EF: movsx eax, cx
0054E3F2: cdq 
0054E3F3: and edx, 3
0054E3F6: add eax, edx
0054E3F8: mov edx, dword ptr [esp + 0xc]
0054E3FC: sar eax, 2
0054E3FF: lea ecx, [eax + esi*2]
0054E402: pop esi
0054E403: mov eax, dword ptr [edx + ecx*4 + 0x58dc]
0054E40A: ret 8
0054E40D: nop 
0054E40E: nop 
0054E40F: nop 