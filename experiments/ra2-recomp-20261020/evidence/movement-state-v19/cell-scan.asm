00703182: cmp dword ptr [esp + 0x80], 8
0070318A: jne 0x7031bd
0070318C: test esi, esi
0070318E: je 0x703b5a
00703194: mov esi, dword ptr [esi + 0x28]
00703197: test si, si
0070319A: mov dword ptr [esp + 0x84], esi
007031A1: jne 0x7031b1
007031A3: cmp word ptr [esp + 0x86], si
007031AB: je 0x703b5a
007031B1: pop edi
007031B2: pop esi
007031B3: pop ebp
007031B4: xor eax, eax
007031B6: pop ebx
007031B7: add esp, 0x68
007031BA: ret 0x14
007031BD: test esi, esi
007031BF: je 0x7031f2
007031C1: mov ecx, dword ptr [esp + 0x80]
007031C8: mov edx, dword ptr [esi + 0x2c]
007031CB: mov eax, ecx
007031CD: sub eax, edx
007031CF: cdq
007031D0: xor eax, edx
007031D2: sub eax, edx
007031D4: cmp eax, 2
007031D7: jle 0x7031f2
007031D9: cmp eax, 6
007031DC: jge 0x7031f2
007031DE: cmp ecx, -1
007031E1: je 0x7031f2
007031E3: pop edi
007031E4: pop esi
007031E5: pop ebp
007031E6: mov eax, 7
007031EB: pop ebx
007031EC: add esp, 0x68
007031EF: ret 0x14
007031F2: mov edi, dword ptr [esp + 0x80]
007031F9: mov ecx, ebx
007031FB: lea esi, [edi - 4]
007031FE: and esi, 7
00703201: push esi
00703202: call 0x476ac0
00703207: mov ecx, eax
00703209: call 0x47a130
0070320E: mov ecx, eax
00703210: test ecx, ecx
00703212: je 0x70323e
00703214: mov edx, dword ptr [ecx + 0x2c]
00703217: mov eax, esi
00703219: sub eax, edx
0070321B: cdq
0070321C: xor eax, edx
0070321E: sub eax, edx
00703220: cmp eax, 2
00703223: jle 0x70323e
00703225: cmp eax, 6
00703228: jge 0x70323e
0070322A: cmp edi, -1
0070322D: je 0x70323e
0070322F: pop edi
00703230: pop esi
00703231: pop ebp
00703232: mov eax, 7
00703237: pop ebx
00703238: add esp, 0x68
0070323B: ret 0x14
0070323E: mov esi, dword ptr [esp + 0x88]
00703245: mov eax, dword ptr [ebp]
00703248: lea ecx, [esp + 0x11]
0070324C: push esi
0070324D: lea edx, [esp + 0x88]
00703254: push ecx
00703255: push edx
00703256: push edi
00703257: push ebx
00703258: mov ecx, ebp
0070325A: call dword ptr [eax + 0x198]
00703260: cmp eax, 7
00703263: jne 0x70326f
00703265: pop edi
00703266: pop esi
00703267: pop ebp
00703268: pop ebx
00703269: add esp, 0x68
0070326C: ret 0x14
0070326F: mov eax, dword ptr [esp + 0x84]
00703276: cmp eax, -1
00703279: je 0x7032b5
0070327B: mov ecx, dword ptr [ebx + 0x140]
00703281: test ch, 1
00703284: je 0x7032b5
00703286: movsx ecx, byte ptr [ebx + 0x11b]
0070328D: add ecx, 4
00703290: cmp eax, ecx
00703292: jne 0x7032b5
00703294: mov ecx, dword ptr [ebx + 0x128]
0070329A: mov dl, byte ptr [ebx + 0x128]
007032A0: shr ecx, 5
007032A3: and cl, 1
007032A6: mov byte ptr [esp + 0x12], dl
007032AA: mov byte ptr [esp + 0x13], cl
007032AE: mov ecx, dword ptr [ebx + 0x58]
007032B1: mov dword ptr [esp + 0x18], ecx
007032B5: mov ecx, dword ptr [0xa40774]
007032BB: test ecx, ecx
007032BD: jne 0x7032ff
007032BF: push 1
007032C1: push ebx
007032C2: mov ecx, 0x8324e0
007032C7: call 0x55a740
007032CC: test al, al
007032CE: jne 0x7032f8
007032D0: mov edx, dword ptr [ebp]
007032D3: mov ecx, ebp
007032D5: call dword ptr [edx + 0x2f4]
007032DB: test al, al
007032DD: jne 0x7032f8
007032DF: mov al, byte ptr [ebp + 0x32d]
007032E5: test al, al
007032E7: je 0x7032f8
007032E9: pop edi
007032EA: pop esi
007032EB: pop ebp
007032EC: mov eax, 7
007032F1: pop ebx
007032F2: add esp, 0x68
007032F5: ret 0x14
007032F8: mov eax, dword ptr [esp + 0x84]
007032FF: mov ecx, dword ptr [esp + 0x8c]
00703306: mov edx, dword ptr [esp + 0x80]
0070330D: push ecx
0070330E: push esi
0070330F: push eax
00703310: push edx
00703311: push ebx
00703312: mov ecx, ebp
00703314: call 0x4c86e0
00703319: mov edi, eax
0070331B: cmp edi, 7
0070331E: mov dword ptr [esp + 0x8c], edi
00703325: jne 0x703331
00703327: pop edi
00703328: pop esi
00703329: pop ebp
0070332A: pop ebx
0070332B: add esp, 0x68
0070332E: ret 0x14
00703331: mov eax, dword ptr [ebx + 0x44]
00703334: cmp eax, -1
00703337: je 0x703439