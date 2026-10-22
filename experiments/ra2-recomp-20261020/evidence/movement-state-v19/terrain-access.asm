0047A130: mov ax, word ptr [ecx + 0x116]
0047A137: test ax, ax
0047A13A: jl 0x47a153
0047A13C: mov ecx, dword ptr [0x8661d8]
0047A142: movsx eax, ax
0047A145: cmp eax, ecx
0047A147: jge 0x47a153
0047A149: mov ecx, dword ptr [0x8661cc]
0047A14F: mov eax, dword ptr [ecx + eax*4]
0047A152: ret
0047A153: xor eax, eax
0047A155: ret
0047A156: nop
0047A157: nop
0047A158: nop
0047A159: nop
0047A15A: nop
0047A15B: nop
0047A15C: nop
0047A15D: nop
0047A15E: nop
0047A15F: nop
0047A160: sub esp, 0x28
0047A163: push ebp
0047A164: mov ebp, ecx
0047A166: xor ecx, ecx
0047A168: mov eax, dword ptr [ebp + 0xe4]
0047A16E: test eax, eax
0047A170: je 0x47a188
0047A172: lea edx, [esp + 4]
0047A176: cmp ecx, 0xa
0047A179: jge 0x47a188
0047A17B: mov dword ptr [edx], eax
0047A17D: mov eax, dword ptr [eax + 0x30]
0047A180: inc ecx
0047A181: add edx, 4
0047A184: test eax, eax
0047A186: jne 0x47a176
0047A188: test ecx, ecx
0047A18A: jle 0x47a1ed
0047A18C: push ebx
0047A18D: push esi
0047A18E: push edi
0047A18F: lea edi, [esp + 0x10]
0047A193: mov ebx, ecx
0047A195: mov esi, dword ptr [edi]
0047A197: push 0
0047A199: mov ecx, esi
0047A19B: mov eax, dword ptr [esi]
0047A19D: call dword ptr [eax + 0x1b4]
0047A1A3: mov edx, dword ptr [esi]
0047A1A5: mov ecx, esi
0047A1A7: call dword ptr [edx + 0x2c]
0047A1AA: cmp eax, 1
0047A1AD: je 0x47a1bb
0047A1AF: mov eax, dword ptr [esi]
0047A1B1: mov ecx, esi
0047A1B3: call dword ptr [eax + 0x2c]
0047A1B6: cmp eax, 2
0047A1B9: jne 0x47a1e4
0047A1BB: mov eax, dword ptr [esi + 0x564]
0047A1C1: test eax, eax
0047A1C3: jne 0x47a1cf
0047A1C5: push 0x80004003
0047A1CA: call 0x795940
0047A1CF: mov esi, dword ptr [esi + 0x564]
0047A1D5: xor edx, edx
0047A1D7: mov dl, byte ptr [ebp + 0x11c]
0047A1DD: mov ecx, dword ptr [esi]
0047A1DF: push edx
0047A1E0: push esi
0047A1E1: call dword ptr [ecx + 0x7c]
0047A1E4: add edi, 4
0047A1E7: dec ebx
0047A1E8: jne 0x47a195
0047A1EA: pop edi
0047A1EB: pop esi
0047A1EC: pop ebx
0047A1ED: pop ebp
0047A1EE: add esp, 0x28
0047A1F1: ret
0047A1F2: nop
0047A1F3: nop
0047A1F4: nop
0047A1F5: nop
0047A1F6: nop
0047A1F7: nop
0047A1F8: nop
0047A1F9: nop
0047A1FA: nop
0047A1FB: nop
0047A1FC: nop
0047A1FD: nop
0047A1FE: nop
0047A1FF: nop
0047A200: mov ecx, dword ptr [ecx + 0x44]
0047A203: call 0x5dc0b0
0047A208: cmp eax, -1
0047A20B: je 0x47a21a
0047A20D: mov ecx, dword ptr [0xac0b34]
0047A213: mov edx, dword ptr [ecx + eax*4]
0047A216: mov eax, dword ptr [edx + 0x60]
0047A219: ret
0047A21A: xor eax, eax
0047A21C: ret
0047A21D: nop
0047A21E: nop
0047A21F: nop
0047A220: mov ecx, dword ptr [ecx + 0x44]
0047A223: jmp 0x5dc0b0
0047A228: nop
0047A229: nop
0047A22A: nop
0047A22B: nop
0047A22C: nop
0047A22D: nop
0047A22E: nop
0047A22F: nop
0047A230: push esi
0047A231: mov esi, ecx
0047A233: mov ecx, dword ptr [esi + 0x44]
0047A236: call 0x5dc0b0
0047A23B: cmp eax, -1
0047A23E: jne 0x47a244
0047A240: xor eax, eax
0047A242: pop esi
0047A243: ret
0047A244: mov ecx, dword ptr [0xac0b34]
0047A24A: mov edx, dword ptr [ecx + eax*4]
0047A24D: xor eax, eax