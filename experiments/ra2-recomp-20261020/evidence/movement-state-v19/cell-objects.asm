004717B0: mov al, byte ptr [0xa40958]
004717B5: push esi
004717B6: test al, al
004717B8: je 0x4717d7
004717BA: mov esi, dword ptr [ecx + 0xe4]
004717C0: test esi, esi
004717C2: je 0x4717d7
004717C4: mov eax, dword ptr [esi]
004717C6: mov ecx, esi
004717C8: call dword ptr [eax + 0x2c]
004717CB: cmp eax, 6
004717CE: je 0x4717db
004717D0: mov esi, dword ptr [esi + 0x30]
004717D3: test esi, esi
004717D5: jne 0x4717c4
004717D7: xor eax, eax
004717D9: pop esi
004717DA: ret
004717DB: mov eax, esi
004717DD: pop esi
004717DE: ret
004717DF: nop
004717E0: mov al, byte ptr [0xa40958]
004717E5: push esi
004717E6: test al, al
004717E8: je 0x471817
004717EA: mov al, byte ptr [esp + 8]
004717EE: test al, al
004717F0: je 0x4717fa
004717F2: mov esi, dword ptr [ecx + 0xe8]
004717F8: jmp 0x471800
004717FA: mov esi, dword ptr [ecx + 0xe4]
00471800: test esi, esi
00471802: je 0x471817
00471804: mov eax, dword ptr [esi]
00471806: mov ecx, esi
00471808: call dword ptr [eax + 0x2c]
0047180B: cmp eax, 0x24
0047180E: je 0x47181d
00471810: mov esi, dword ptr [esi + 0x30]
00471813: test esi, esi
00471815: jne 0x471804
00471817: xor eax, eax
00471819: pop esi
0047181A: ret 4
0047181D: mov eax, esi
0047181F: pop esi
00471820: ret 4
00471823: nop
00471824: nop
00471825: nop
00471826: nop
00471827: nop
00471828: nop
00471829: nop
0047182A: nop
0047182B: nop
0047182C: nop
0047182D: nop
0047182E: nop
0047182F: nop
00471830: mov al, byte ptr [0xa40958]
00471835: push esi
00471836: push edi
00471837: mov edi, ecx
00471839: test al, al
0047183B: je 0x47185a
0047183D: mov esi, dword ptr [edi + 0xe4]
00471843: test esi, esi
00471845: je 0x47185a
00471847: mov eax, dword ptr [esi]
00471849: mov ecx, esi
0047184B: call dword ptr [eax + 0x2c]
0047184E: cmp eax, 2
00471851: je 0x47189e
00471853: mov esi, dword ptr [esi + 0x30]
00471856: test esi, esi
00471858: jne 0x471847
0047185A: mov ecx, dword ptr [esp + 0x10]
0047185E: mov edx, dword ptr [esp + 0xc]
00471862: push 0
00471864: push ecx
00471865: push edx
00471866: mov ecx, edi
00471868: call 0x471660
0047186D: test eax, eax
0047186F: jne 0x471899
00471871: mov al, byte ptr [0xa40958]
00471876: test al, al
00471878: je 0x471897
0047187A: mov esi, dword ptr [edi + 0xe4]
00471880: test esi, esi
00471882: je 0x471897
00471884: mov eax, dword ptr [esi]
00471886: mov ecx, esi
00471888: call dword ptr [eax + 0x2c]
0047188B: cmp eax, 0x24
0047188E: je 0x4718a2
00471890: mov esi, dword ptr [esi + 0x30]
00471893: test esi, esi
00471895: jne 0x471884
00471897: xor eax, eax
00471899: pop edi
0047189A: pop esi
0047189B: ret 8
0047189E: test esi, esi
004718A0: je 0x47185a
004718A2: mov eax, esi
004718A4: pop edi
004718A5: pop esi
004718A6: ret 8
004718A9: nop
004718AA: nop
004718AB: nop
004718AC: nop
004718AD: nop
004718AE: nop
004718AF: nop
004718B0: mov eax, dword ptr [0xa40774]
004718B5: sub esp, 8
004718B8: push ebx
004718B9: push ebp
004718BA: xor ebp, ebp
004718BC: push esi
004718BD: push edi
004718BE: cmp eax, ebp
004718C0: mov edi, ecx
004718C2: jne 0x471d00
004718C8: mov eax, dword ptr [esp + 0x20]
004718CC: cmp eax, ebp
004718CE: je 0x471930
004718D0: mov cl, byte ptr [eax + 0x1359]
004718D6: test cl, cl
004718D8: je 0x47196d
004718DE: mov al, byte ptr [0xa40958]
004718E3: test al, al
004718E5: je 0x471930
004718E7: mov esi, dword ptr [edi + 0xe4]
004718ED: cmp esi, ebp
004718EF: je 0x47190a
004718F1: mov eax, dword ptr [esi]
004718F3: mov ecx, esi
004718F5: call dword ptr [eax + 0x2c]
004718F8: cmp eax, 6
004718FB: je 0x471906
004718FD: mov esi, dword ptr [esi + 0x30]
00471900: cmp esi, ebp
00471902: jne 0x4718f1
00471904: jmp 0x47190a
00471906: cmp esi, ebp
00471908: jne 0x471961
0047190A: mov al, byte ptr [0xa40958]
0047190F: test al, al
00471911: je 0x471930
00471913: mov esi, dword ptr [edi + 0xe4]
00471919: cmp esi, ebp
0047191B: je 0x471930
0047191D: mov edx, dword ptr [esi]