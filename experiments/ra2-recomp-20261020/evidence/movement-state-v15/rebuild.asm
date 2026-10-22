00428370 mov al, byte ptr [0x84e7d4]
00428375 sub esp, 0xc
00428378 test al, 1
0042837A jne 0x428394
0042837C mov dl, al
0042837E push 0x4284d0
00428383 or dl, 1
00428386 mov byte ptr [0x84e7d4], dl
0042838C call 0x78298a
00428391 add esp, 4
00428394 push ebx
00428395 push ebp
00428396 push esi
00428397 mov esi, dword ptr [esp + 0x1c]
0042839B push edi
0042839C fld dword ptr [esi + 8]
0042839F call 0x77f110
004283A4 mov edx, dword ptr [esp + 0x24]
004283A8 mov dword ptr [0x84c814], eax
004283AD mov eax, dword ptr [esi + 0xc]
004283B0 xor edi, edi
004283B2 mov ecx, 0x84c858
004283B7 mov dword ptr [0x84c818], eax
004283BC mov dword ptr [0x84c820], edi
004283C2 mov word ptr [0x84c828], di
004283C9 mov word ptr [0x84c82a], di
004283D0 mov dword ptr [0x84c81c], edx
004283D6 mov dword ptr [0x84c824], ecx
004283DC mov ebp, dword ptr [esi]
004283DE mov eax, dword ptr [esi + 0xc]
004283E1 mov ebx, dword ptr [ebp + 8]
004283E4 sub eax, 2
004283E7 js 0x42848f
004283ED lea edi, [edx + eax*4]
004283F0 sub ecx, edx
004283F2 inc eax
004283F3 mov dword ptr [esp + 0x10], edi
004283F7 mov dword ptr [esp + 0x18], ecx
004283FB mov dword ptr [esp + 0x14], eax
004283FF test ebx, ebx
00428401 je 0x42846d
00428403 mov eax, dword ptr [esp + 0x10]
00428407 mov edx, dword ptr [ebx + 4]
0042840A mov dword ptr [ecx + eax], edx
0042840D mov ecx, dword ptr [ebx]
0042840F mov edx, dword ptr [ebp]
00428412 mov ecx, dword ptr [ecx]
00428414 mov esi, dword ptr [edx]
00428416 add ecx, 0x24
00428419 add esi, 0x24
0042841C movsx edi, word ptr [ecx + 2]
00428420 movsx eax, word ptr [esi + 2]
00428424 sub edi, eax
00428426 mov eax, edi
00428428 cdq 
00428429 xor eax, edx
0042842B sub eax, edx
0042842D cmp eax, 1
00428430 jg 0x428456
00428432 movsx ecx, word ptr [ecx]
00428435 movsx esi, word ptr [esi]
00428438 mov eax, ecx
0042843A sub eax, esi
0042843C cdq 
0042843D xor eax, edx
0042843F sub eax, edx
00428441 cmp eax, 1
00428444 jg 0x428456
00428446 lea edx, [edi + edi*2]
00428449 sub edx, esi
0042844B add edx, ecx
0042844D mov eax, dword ptr [edx*4 + 0x7cf110]
00428454 jmp 0x42845b
00428456 mov eax, 8
0042845B mov ecx, dword ptr [esp + 0x10]
0042845F mov esi, dword ptr [esp + 0x20]
00428463 mov edx, dword ptr [esp + 0x24]
00428467 mov dword ptr [ecx], eax
00428469 mov ecx, dword ptr [esp + 0x18]
0042846D mov edi, dword ptr [esp + 0x10]
00428471 mov eax, dword ptr [esp + 0x14]
00428475 mov ebp, dword ptr [ebp + 8]
00428478 mov ebx, dword ptr [ebx + 8]
0042847B sub edi, 4
0042847E dec eax
0042847F mov dword ptr [esp + 0x10], edi
00428483 mov dword ptr [esp + 0x14], eax
00428487 jne 0x4283ff
0042848D xor edi, edi
0042848F mov eax, dword ptr [esi + 0xc]
00428492 mov dword ptr [edx + eax*4 - 4], 0xffffffff
0042849A mov ecx, dword ptr [ebp]
0042849D mov edx, dword ptr [ecx]
0042849F mov eax, dword ptr [edx + 0x24]
004284A2 mov dword ptr [0x84c810], eax
004284A7 mov eax, dword ptr [0x84c814]
004284AC cmp eax, edi
004284AE pop edi
004284AF pop esi
004284B0 pop ebp
004284B1 pop ebx
004284B2 jne 0x4284be
004284B4 mov dword ptr [0x84c814], 1
004284BE mov eax, 0x84c810
004284C3 add esp, 0xc
004284C6 ret 8