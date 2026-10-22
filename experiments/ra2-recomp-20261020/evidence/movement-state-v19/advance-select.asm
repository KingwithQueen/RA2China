004A15E0: pop ebp
004A15E1: xor al, al
004A15E3: pop ebx
004A15E4: add esp, 0xe4
004A15EA: ret 4
004A15ED: or edi, 0xffffffff
004A15F0: cmp edx, 7
004A15F3: jle 0x4a1fa1
004A15F9: mov edx, dword ptr [ebp + 0x58]
004A15FC: lea edx, [edx + edx*2]
004A15FF: lea esi, [edx*4 + 0x7a0180]
004A1606: mov dl, byte ptr [ebp + 0x60]
004A1609: test dl, dl
004A160B: mov dword ptr [esp + 0xa8], esi
004A1612: je 0x4a161a
004A1614: movsx edx, byte ptr [esi + 1]
004A1618: jmp 0x4a161d
004A161A: movsx edx, byte ptr [esi]
004A161D: shl edx, 4
004A1620: mov dword ptr [esp + 0x58], edx
004A1624: cmp eax, edi
004A1626: mov edx, dword ptr [edx + 0x7a00a0]
004A162C: mov dword ptr [esp + 0x38], edx
004A1630: jl 0x4a22f9
004A1636: cmp eax, 8
004A1639: jg 0x4a22f9
004A163F: mov byte ptr [esp + 0x13], 0
004A1644: je 0x4a166a
004A1646: cmp eax, edi
004A1648: je 0x4a166a
004A164A: xor ecx, ecx
004A164C: mov ch, byte ptr [esi + 4]
004A164F: mov word ptr [esp + 0x14], cx
004A1654: mov edx, dword ptr [esp + 0x14]
004A1658: shr edx, 0xc
004A165B: inc edx
004A165C: shr edx, 1
004A165E: and edx, 7
004A1661: cmp edx, eax
004A1663: je 0x4a166a
004A1665: mov byte ptr [esp + 0x13], 1
004A166A: mov eax, dword ptr [ebp + 0x5c]
004A166D: mov esi, dword ptr [esp + 0x38]
004A1671: mov ebx, dword ptr [esp + 0x3c]
004A1675: lea ecx, [eax + eax*2]
004A1678: sub ebx, 7
004A167B: mov dword ptr [esp + 0x3c], ebx
004A167F: mov edx, dword ptr [esi + ecx*4]
004A1682: lea ecx, [esi + ecx*4]
004A1685: test edx, edx
004A1687: mov ecx, dword ptr [ecx + 4]
004A168A: mov dword ptr [esp + 0x8c], edx
004A1691: mov dword ptr [esp + 0x90], ecx
004A1698: jne 0x4a16a6
004A169A: test ecx, ecx
004A169C: jne 0x4a16a6
004A169E: test eax, eax
004A16A0: jne 0x4a1fdc
004A16A6: mov ecx, dword ptr [ebp + 0xc]
004A16A9: mov edx, dword ptr [ecx]