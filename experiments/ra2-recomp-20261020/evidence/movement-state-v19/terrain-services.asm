0070394F: mov edx, dword ptr [esi]
00703951: mov ecx, esi
00703953: call dword ptr [edx + 0x2c]
00703956: mov ecx, 6
0070395B: cmp eax, ecx
0070395D: je 0x703b5a
00703963: cmp dword ptr [esp + 0x8c], ecx
0070396A: jge 0x7038eb
00703970: mov dword ptr [esp + 0x8c], ecx
00703977: jmp 0x7038ef
0070397C: mov ecx, esi
0070397E: call 0x40dbd0
00703983: test eax, eax
00703985: je 0x70399a
00703987: cmp dword ptr [eax + 0x1b8], 2
0070398E: jne 0x70399a
00703990: mov eax, 1
00703995: jmp 0x703a66
0070399A: mov eax, dword ptr [ebp + 0x5ac]
007039A0: mov cl, byte ptr [eax + 0xaf3]
007039A6: test cl, cl
007039A8: jne 0x7039b7
007039AA: push 0x11
007039AC: mov ecx, ebp
007039AE: call 0x6d7910
007039B3: test al, al
007039B5: je 0x7039ec
007039B7: mov edx, dword ptr [esi]
007039B9: mov ecx, esi
007039BB: call dword ptr [edx + 0x84]
007039C1: mov cl, byte ptr [eax + 0x1fd]
007039C7: test cl, cl
007039C9: je 0x7039ec
007039CB: mov ecx, dword ptr [ebp + 0x1b4]
007039D1: push esi
007039D2: call 0x4e5580
007039D7: test al, al
007039D9: jne 0x7038eb
007039DF: mov byte ptr [esp + 0x88], 1
007039E7: jmp 0x7038ef
007039EC: mov eax, dword ptr [ebp]
007039EF: push 0
007039F1: mov ecx, ebp
007039F3: call dword ptr [eax + 0x39c]
007039F9: cmp dword ptr [eax], 0
007039FC: jne 0x703a12
007039FE: mov ecx, dword ptr [ebp + 0x5ac]
00703A04: mov al, byte ptr [ecx + 0xaa0]
00703A0A: test al, al
00703A0C: je 0x703b5a
00703A12: mov edx, dword ptr [esi]
00703A14: mov ecx, esi
00703A16: call dword ptr [edx + 0x2c]
00703A19: cmp eax, 6
00703A1C: je 0x703a7f
00703A1E: cmp eax, 0x24
00703A21: jne 0x703a61
00703A23: mov eax, dword ptr [ebp]
00703A26: push esi
00703A27: mov ecx, ebp
00703A29: call dword ptr [eax + 0x2b8]
00703A2F: mov edx, dword ptr [ebp]
00703A32: push eax
00703A33: mov ecx, ebp
00703A35: call dword ptr [edx + 0x39c]
00703A3B: mov eax, dword ptr [eax]
00703A3D: test eax, eax