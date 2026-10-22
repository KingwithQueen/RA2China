005D47D0: push esi
005D47D1: mov esi, ecx
005D47D3: mov eax, dword ptr [esi]
005D47D5: call dword ptr [eax + 0x1a4]
005D47DB: mov cl, byte ptr [esi + 0x79]
005D47DE: pop esi
005D47DF: movsx edx, byte ptr [eax + 0x11b]
005D47E6: neg cl
005D47E8: sbb ecx, ecx
005D47EA: and ecx, 4
005D47ED: add ecx, edx
005D47EF: mov eax, ecx
005D47F1: ret
005D47F2: nop
005D47F3: nop
005D47F4: nop
005D47F5: nop
005D47F6: nop
005D47F7: nop
005D47F8: nop
005D47F9: nop
005D47FA: nop
005D47FB: nop
005D47FC: nop
005D47FD: nop
005D47FE: nop
005D47FF: nop
005D4800: mov eax, dword ptr [ecx + 0x90]
005D4806: ret
005D4807: nop
005D4808: nop
005D4809: nop
005D480A: nop
005D480B: nop
005D480C: nop
005D480D: nop
005D480E: nop
005D480F: nop
005D4810: sub esp, 0xc
005D4813: push esi
005D4814: mov esi, ecx
005D4816: lea eax, [esi + 0x88]
005D481C: mov ecx, dword ptr [esi + 0x88]
005D4822: mov dword ptr [esp + 4], ecx
005D4826: lea ecx, [esp + 4]
005D482A: mov edx, dword ptr [eax + 4]
005D482D: push ecx
005D482E: mov ecx, 0x8324e0
005D4833: mov dword ptr [esp + 0xc], edx
005D4837: mov eax, dword ptr [eax + 8]
005D483A: mov dword ptr [esp + 0x10], eax
005D483E: call 0x55a280
005D4843: mov ecx, dword ptr [esi + 0x90]
005D4849: sub ecx, eax
005D484B: mov al, byte ptr [esi + 0x79]
005D484E: test al, al
005D4850: pop esi
005D4851: je 0x5d4859
005D4853: sub ecx, dword ptr [0xa72f30]
005D4859: mov eax, ecx
005D485B: add esp, 0xc
005D485E: ret
005D485F: nop
005D4860: sub esp, 0xc
005D4863: push esi
005D4864: mov esi, ecx
005D4866: push edi
005D4867: mov edi, dword ptr [esp + 0x18]
005D486B: mov al, byte ptr [esi + 0x79]
005D486E: test al, al
005D4870: je 0x5d4878
005D4872: add edi, dword ptr [0xa72f30]
005D4878: mov al, byte ptr [esi + 0x74]
005D487B: test al, al
005D487D: je 0x5d48d4
005D487F: mov eax, dword ptr [esi]
005D4881: push 0
005D4883: mov ecx, esi
005D4885: call dword ptr [eax + 0x11c]
005D488B: lea ecx, [esi + 0x88]
005D4891: mov edx, dword ptr [esi + 0x88]
005D4897: mov dword ptr [esp + 8], edx
005D489B: lea edx, [esp + 8]