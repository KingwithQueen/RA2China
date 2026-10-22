00702E90: mov ecx, dword ptr [ebp + 0x88]
00702E96: mov dword ptr [esp + 0x3c], ecx
00702E9A: lea ecx, [esp + 0x3c]
00702E9E: mov edx, dword ptr [eax + 4]
00702EA1: push ecx
00702EA2: mov ecx, 0x8324e0
00702EA7: mov dword ptr [esp + 0x44], edx
00702EAB: mov eax, dword ptr [eax + 8]
00702EAE: mov dword ptr [esp + 0x48], eax
00702EB2: call 0x548000
00702EB7: mov ecx, eax
00702EB9: call 0x4717b0
00702EBE: test eax, eax
00702EC0: je 0x702f02
00702EC2: mov ecx, dword ptr [eax + 0x418]
00702EC8: mov dl, byte ptr [ecx + 0x1355]
00702ECE: test dl, dl
00702ED0: jne 0x702edc
00702ED2: mov dl, byte ptr [ecx + 0x1356]
00702ED8: test dl, dl
00702EDA: je 0x702f02
00702EDC: mov esi, dword ptr [ebp]
00702EDF: push 1
00702EE1: lea edx, [esp + 0x30]
00702EE5: push eax
00702EE6: push edx
00702EE7: mov ecx, ebp
00702EE9: call 0x6cf130
00702EEE: push eax
00702EEF: mov ecx, 0x8324e0
00702EF4: call 0x548070
00702EF9: push eax
00702EFA: mov ecx, ebp
00702EFC: call dword ptr [esi + 0x410]
00702F02: mov eax, dword ptr [ebp]
00702F05: push 0
00702F07: push 5
00702F09: mov ecx, ebp
00702F0B: call dword ptr [eax + 0x1d0]
00702F11: mov ecx, ebp
00702F13: call 0x5950d0
00702F18: fld qword ptr [eax + 0x10]
00702F1B: fmul qword ptr [0x79b608]
00702F21: call 0x77f110
00702F26: mov ecx, dword ptr [0xa3d290]
00702F2C: push 2
00702F2E: push 0
00702F30: add ecx, 0x218
00702F36: mov esi, eax
00702F38: call 0x6388a0
00702F3D: add eax, esi
00702F3F: pop edi
00702F40: pop esi
00702F41: pop ebp
00702F42: pop ebx
00702F43: add esp, 0x54
00702F46: ret
00702F47: nop
00702F48: mov dword ptr [esi], esp
00702F4A: jo 0x702f4c
00702F4C: leave
00702F4D: sub byte ptr [eax], dh
00702F50: shr byte ptr [edx], 0x70
00702F53: add byte ptr [0x3900702e], bl
00702F59: jo 0x702f5c
00702F5C: nop
00702F5D: nop
00702F5E: nop
00702F5F: nop
00702F60: push esi
00702F61: mov esi, ecx
00702F63: push edi
00702F64: mov eax, dword ptr [esi + 0x5ac]
00702F6A: mov edi, dword ptr [eax + 0x3c8]
00702F70: test edi, edi
00702F72: je 0x70302a
00702F78: mov ecx, dword ptr [0x839848]
00702F7E: xor eax, eax
00702F80: mov edx, dword ptr [ecx + 0x7d8]
00702F86: test edx, edx
00702F88: jle 0x702f9c
00702F8A: mov ecx, dword ptr [ecx + 0x7cc]
00702F90: cmp dword ptr [ecx], edi
00702F92: je 0x702fb5
00702F94: inc eax
00702F95: add ecx, 4
00702F98: cmp eax, edx
00702F9A: jl 0x702f90
00702F9C: mov eax, dword ptr [esi + 0x228]
00702FA2: test eax, eax
00702FA4: jne 0x702fb5
00702FA6: mov ecx, dword ptr [esi + 0x1b4]
00702FAC: call 0x4f52f0
00702FB1: test al, al
00702FB3: je 0x70302a
00702FB5: mov eax, dword ptr [esi + 0xa8]
00702FBB: sub eax, 0
00702FBE: je 0x702fd9
00702FC0: dec eax
00702FC1: jne 0x702ff9
00702FC3: mov al, byte ptr [esi + 0x57c]
00702FC9: test al, al
00702FCB: jne 0x702ff9
00702FCD: mov dword ptr [esi + 0xa8], 0
00702FD7: jmp 0x702ff9
00702FD9: mov ecx, esi
00702FDB: call 0x6fd930
00702FE0: test al, al
00702FE2: je 0x702ff9
00702FE4: mov ecx, esi
00702FE6: call 0x6fdfc0
00702FEB: test al, al
00702FED: je 0x702ff9
00702FEF: mov dword ptr [esi + 0xa8], 1
00702FF9: mov ecx, esi
00702FFB: call 0x5950d0
00703000: fld qword ptr [eax + 0x10]
00703003: fmul qword ptr [0x79b608]
00703009: call 0x77f110
0070300E: mov ecx, dword ptr [0xa3d290]
00703014: push 2
00703016: push 0
00703018: add ecx, 0x218
0070301E: mov esi, eax
00703020: call 0x6388a0
00703025: add eax, esi
00703027: pop edi
00703028: pop esi
00703029: ret
0070302A: mov ecx, esi
0070302C: call 0x4c48e0
00703031: pop edi
00703032: pop esi
00703033: ret
00703034: nop
00703035: nop
00703036: nop
00703037: nop
00703038: nop
00703039: nop
0070303A: nop
0070303B: nop
0070303C: nop
0070303D: nop
0070303E: nop
0070303F: nop
00703040: sub esp, 0x68
00703043: push ebx
00703044: mov ebx, dword ptr [esp + 0x70]
00703048: push ebp
00703049: mov ebp, ecx
0070304B: mov eax, dword ptr [ebx + 0x140]
00703051: push esi
00703052: test ah, 1
00703055: push edi
00703056: mov dword ptr [esp + 0x14], ebp
0070305A: je 0x703082
0070305C: mov eax, dword ptr [esp + 0x84]
00703063: cmp eax, -1
00703066: je 0x70307b
00703068: movsx ecx, byte ptr [ebx + 0x11b]
0070306F: sub eax, ecx
00703071: cdq
00703072: xor eax, edx
00703074: sub eax, edx
00703076: cmp eax, 1
00703079: jle 0x703082
0070307B: mov byte ptr [esp + 0x11], 1
00703080: jmp 0x703087
00703082: mov byte ptr [esp + 0x11], 0
00703087: mov eax, dword ptr [ebx + 0x124]
0070308D: mov dl, byte ptr [ebx + 0x124]
00703093: shr eax, 5
00703096: and al, 1
00703098: mov ecx, ebx
0070309A: mov byte ptr [esp + 0x13], al
0070309E: mov eax, dword ptr [ebx + 0x54]
007030A1: mov byte ptr [esp + 0x12], dl
007030A5: mov dword ptr [esp + 0x18], eax
007030A9: call 0x47a130
007030AE: mov ecx, dword ptr [ebp + 0x5ac]
007030B4: mov esi, eax