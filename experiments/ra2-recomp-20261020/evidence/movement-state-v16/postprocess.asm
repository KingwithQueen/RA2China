004290C0 sub esp, 0x80
004290C6 mov dword ptr [esp + 0x50], ecx
004290CA push ebx
004290CB mov ecx, dword ptr [esp + 0x88]
004290D2 push ebp
004290D3 push esi
004290D4 push edi
004290D5 mov eax, dword ptr [ecx + 8]
004290D8 mov edx, dword ptr [ecx + 0xc]
004290DB mov edi, dword ptr [ecx]
004290DD mov ebp, dword ptr [ecx + 0x14]
004290E0 dec eax
004290E1 xor ebx, ebx
004290E3 xor esi, esi
004290E5 cmp eax, ebx
004290E7 mov dword ptr [esp + 0x1c], edx
004290EB mov dword ptr [esp + 0x68], eax
004290EF mov dword ptr [esp + 0x34], ebx
004290F3 mov dword ptr [esp + 0x80], edi
004290FA mov dword ptr [esp + 0x64], ebp
004290FE mov dword ptr [esp + 0x2c], ebx
00429102 mov dword ptr [esp + 0x28], ebx
00429106 mov word ptr [esp + 0x18], bx
0042910B mov word ptr [esp + 0x1a], bx
00429110 mov word ptr [esp + 0x70], bx
00429115 mov word ptr [esp + 0x72], bx
0042911A mov dword ptr [esp + 0x20], ebx
0042911E mov dword ptr [esp + 0x24], ebx
00429122 mov word ptr [esp + 0x14], bx
00429127 mov word ptr [esp + 0x16], bx
0042912C jle 0x42950a
00429132 mov dword ptr [esp + 0x10], edx
00429136 cmp esi, 0x14
00429139 jge 0x429438
0042913F mov eax, dword ptr [esp + 0x10]
00429143 mov eax, dword ptr [eax]
00429145 cmp eax, 8
00429148 mov dword ptr [esp + 0x6c], eax
0042914C jne 0x4291d9
00429152 mov ax, word ptr [esp + 0x82]
0042915A mov edx, dword ptr [0x851a70]
00429160 add ax, word ptr [0x851a72]
00429167 add edi, edx
00429169 mov word ptr [esp + 0x40], bx
0042916E mov word ptr [esp + 0x42], bx
00429173 mov edx, dword ptr [esp + 0x40]
00429177 mov word ptr [esp + 0x3e], ax
0042917C mov eax, dword ptr [esp + 0x10]
00429180 inc esi
00429181 add eax, 4
00429184 mov word ptr [esp + 0x3c], di
00429189 mov edi, dword ptr [esp + 0x3c]
0042918D mov dword ptr [esp + 0x18], edx
00429191 mov dword ptr [esp + 0x10], eax
00429195 mov word ptr [esp + 0x44], bx
0042919A mov word ptr [esp + 0x46], bx
0042919F mov eax, dword ptr [esp + 0x44]
004291A3 mov word ptr [esp + 0x48], bx
004291A8 mov word ptr [esp + 0x4a], bx
004291AD mov edx, dword ptr [esp + 0x48]
004291B1 mov dword ptr [esp + 0x80], edi
004291B8 mov dword ptr [esp + 0x34], esi
004291BC mov dword ptr [esp + 0x28], ebx
004291C0 mov dword ptr [esp + 0x20], ebx
004291C4 mov dword ptr [esp + 0x24], ebx
004291C8 mov dword ptr [esp + 0x14], eax
004291CC mov dword ptr [esp + 0x2c], esi
004291D0 mov dword ptr [esp + 0x70], edx
004291D4 jmp 0x42942e
004291D9 cmp eax, -2
004291DC jne 0x4291ef
004291DE mov eax, dword ptr [esp + 0x10]
004291E2 inc esi
004291E3 add eax, 4
004291E6 mov dword ptr [esp + 0x10], eax
004291EA jmp 0x42942e
004291EF and eax, 7
004291F2 mov bx, word ptr [eax*4 + 0x851a70]
004291FA mov bp, word ptr [eax*4 + 0x851a72]
00429202 mov cx, word ptr [eax*4 + 0x851a70]
0042920A lea eax, [eax*4 + 0x851a70]
00429211 add cx, word ptr [esp + 0x14]
00429216 add bx, word ptr [esp + 0x18]
0042921B mov ax, word ptr [eax + 2]
0042921F add bp, word ptr [esp + 0x1a]
00429224 add ax, word ptr [esp + 0x16]
00429229 mov word ptr [esp + 0x30], cx
0042922E mov word ptr [esp + 0x50], bx
00429233 mov word ptr [esp + 0x52], bp
00429238 mov word ptr [esp + 0x32], ax
0042923D movsx eax, cx
00429240 cdq 
00429241 mov ecx, eax
00429243 mov eax, dword ptr [esp + 0x20]
00429247 xor ecx, edx
00429249 sub ecx, edx
0042924B cmp ecx, eax
0042924D jl 0x429384
00429253 movsx eax, word ptr [esp + 0x32]
00429258 cdq 
00429259 xor eax, edx
0042925B sub eax, edx
0042925D mov edx, dword ptr [esp + 0x24]
00429261 cmp eax, edx
00429263 jl 0x429384
00429269 mov edx, dword ptr [esp + 0x30]
0042926D mov dword ptr [esp + 0x24], eax
00429271 movsx eax, bp
00429274 mov dword ptr [esp + 0x14], edx
00429278 mov dword ptr [esp + 0x20], ecx
0042927C cdq 
0042927D mov ecx, eax
0042927F movsx eax, bx
00429282 xor ecx, edx
00429284 sub ecx, edx
00429286 cdq 
00429287 xor eax, edx
00429289 sub eax, edx
0042928B cmp eax, ecx
0042928D jg 0x429291
0042928F mov eax, ecx
00429291 mov edx, dword ptr [esp + 0x6c]
00429295 and edx, 7
00429298 mov cx, word ptr [edx*4 + 0x851a70]
004292A0 lea edx, [edx*4 + 0x851a70]
004292A7 add cx, di
004292AA mov dx, word ptr [edx + 2]
004292AE mov word ptr [esp + 0x88], cx
004292B6 add dx, word ptr [esp + 0x82]
004292BE mov ecx, dword ptr [esp + 0x28]
004292C2 cmp ecx, eax
004292C4 mov word ptr [esp + 0x8a], dx
004292CC mov ebx, dword ptr [esp + 0x88]
004292D3 mov edi, ebx
004292D5 mov dword ptr [esp + 0x80], edi
004292DC jge 0x4292e7
004292DE mov dword ptr [esp + 0x28], eax
004292E2 jmp 0x42936b
004292E7 mov edx, dword ptr [esp + 0x34]
004292EB mov ebp, dword ptr [esp + 0x60]
004292EF lea eax, [esp + 0x78]
004292F3 lea ecx, [esp + 0x38]
004292F7 push eax
004292F8 mov eax, dword ptr [esp + 0x20]
004292FC push ecx
004292FD push edx
004292FE push esi
004292FF push eax
00429300 mov ecx, ebp
00429302 mov dword ptr [esp + 0x8c], ebx
00429309 call 0x429570
0042930E mov eax, dword ptr [esp + 0x78]
00429312 mov ecx, dword ptr [esp + 0x8a]
00429319 mov edx, dword ptr [esp + 0x7a]
0042931D sub ebx, eax
0042931F mov eax, dword ptr [esp + 0x38]
00429323 sub ecx, edx
00429325 mov word ptr [esp + 0x4c], bx
0042932A mov word ptr [esp + 0x4e], cx
0042932F mov edx, dword ptr [esp + 0x4c]
00429333 mov ecx, dword ptr [esp + 0x64]
00429337 mov dword ptr [esp + 0x6c], edx
0042933B push 0
0042933D mov edx, dword ptr [ecx + eax*4]
00429340 mov ecx, dword ptr [esp + 0x9c]
00429347 push edx
00429348 lea edx, [esp + 0x74]
0042934C push ecx
0042934D push edx
0042934E mov edx, esi
00429350 lea ecx, [esp + 0x88]
00429357 sub edx, eax
00429359 push ecx
0042935A mov ecx, dword ptr [esp + 0x30]
0042935E inc edx
0042935F push edx
00429360 lea edx, [ecx + eax*4]
00429363 mov ecx, ebp
00429365 push edx
00429366 call 0x4296f0
0042936B mov eax, dword ptr [esp + 0x50]
0042936F inc esi
00429370 mov dword ptr [esp + 0x18], eax
00429374 mov eax, dword ptr [esp + 0x10]
00429378 add eax, 4
0042937B mov dword ptr [esp + 0x10], eax
0042937F jmp 0x429425
00429384 xor ecx, ecx
00429386 cmp word ptr [esp + 0x70], cx
0042938B jne 0x4293b8
0042938D cmp word ptr [esp + 0x72], cx
00429392 jne 0x4293b8
00429394 mov dword ptr [esp + 0x20], ecx
00429398 mov dword ptr [esp + 0x24], ecx
0042939C mov word ptr [esp + 0x54], cx
004293A1 mov word ptr [esp + 0x56], cx
004293A6 mov ecx, dword ptr [esp + 0x54]
004293AA mov dword ptr [esp + 0x70], edi
004293AE mov dword ptr [esp + 0x2c], esi
004293B2 mov dword ptr [esp + 0x14], ecx
004293B6 jmp 0x429425
004293B8 mov edx, dword ptr [esp + 0x2c]
004293BC mov eax, dword ptr [esp + 0x72]
004293C0 mov ebx, dword ptr [esp + 0x70]
004293C4 mov dword ptr [esp + 0x34], edx
004293C8 mov edx, dword ptr [esp + 0x82]
004293CF sub ebx, edi
004293D1 sub eax, edx
004293D3 mov word ptr [esp + 0x58], bx
004293D8 mov word ptr [esp + 0x5a], ax
004293DD mov edx, dword ptr [esp + 0x58]
004293E1 movsx eax, ax
004293E4 mov dword ptr [esp + 0x18], edx
004293E8 mov dword ptr [esp + 0x20], ecx
004293EC mov dword ptr [esp + 0x24], ecx
004293F0 mov word ptr [esp + 0x5c], cx
004293F5 mov word ptr [esp + 0x5e], cx
004293FA mov ecx, dword ptr [esp + 0x5c]
004293FE cdq 
004293FF mov dword ptr [esp + 0x14], ecx
00429403 mov ecx, eax
00429405 movsx eax, bx
00429408 xor ecx, edx
0042940A sub ecx, edx
0042940C cdq 
0042940D xor eax, edx
0042940F sub eax, edx
00429411 cmp eax, ecx
00429413 mov dword ptr [esp + 0x28], eax
00429417 jg 0x42941d
00429419 mov dword ptr [esp + 0x28], ecx
0042941D mov dword ptr [esp + 0x70], edi
00429421 mov dword ptr [esp + 0x2c], esi
00429425 mov ecx, dword ptr [esp + 0x94]
0042942C xor ebx, ebx
0042942E cmp esi, dword ptr [esp + 0x68]
00429432 jl 0x429136
00429438 cmp word ptr [esp + 0x70], bx
0042943D jne 0x42944a
0042943F cmp word ptr [esp + 0x72], bx
00429444 je 0x42950a
0042944A mov eax, dword ptr [esp + 0x82]
00429451 mov ecx, dword ptr [esp + 0x72]
00429455 mov edx, dword ptr [esp + 0x70]
00429459 sub eax, ecx
0042945B movsx eax, ax
0042945E mov ebp, edi
00429460 sub ebp, edx
00429462 cdq 
00429463 mov ecx, eax
00429465 movsx eax, bp
00429468 xor ecx, edx
0042946A sub ecx, edx
0042946C cdq 
0042946D xor eax, edx
0042946F sub eax, edx
00429471 cmp eax, ecx
00429473 jg 0x429477
00429475 mov eax, ecx
00429477 mov edx, dword ptr [esp + 0x2c]
0042947B mov ecx, esi
0042947D sub ecx, edx
0042947F dec ecx
00429480 cmp ecx, eax
00429482 jle 0x429503
00429484 mov ebp, dword ptr [esp + 0x60]
00429488 lea eax, [esp + 0x78]
0042948C lea ecx, [esp + 0x38]
00429490 push eax
00429491 push ecx
00429492 dec esi
00429493 push edx
00429494 mov edx, dword ptr [esp + 0x28]
00429498 push esi
00429499 push edx
0042949A mov ecx, ebp
0042949C mov dword ptr [esp + 0x8c], edi
004294A3 call 0x429570
004294A8 mov eax, dword ptr [esp + 0x78]
004294AC mov edx, dword ptr [esp + 0x7a]
004294B0 sub edi, eax
004294B2 mov eax, dword ptr [esp + 0x82]
004294B9 mov ecx, dword ptr [esp + 0x64]
004294BD sub eax, edx
004294BF mov word ptr [esp + 0x60], di
004294C4 mov word ptr [esp + 0x62], ax
004294C9 mov eax, dword ptr [esp + 0x60]
004294CD push 1
004294CF mov dword ptr [esp + 0x70], eax
004294D3 mov eax, dword ptr [esp + 0x3c]
004294D7 sub esi, eax
004294D9 mov edx, dword ptr [ecx + eax*4]
004294DC mov ecx, dword ptr [esp + 0x9c]
004294E3 push edx
004294E4 lea edx, [esp + 0x74]
004294E8 push ecx
004294E9 push edx
004294EA mov edx, dword ptr [esp + 0x2c]
004294EE lea ecx, [esp + 0x88]
004294F5 inc esi
004294F6 push ecx
004294F7 lea eax, [edx + eax*4]
004294FA push esi
004294FB push eax
004294FC mov ecx, ebp
004294FE call 0x4296f0
00429503 mov ecx, dword ptr [esp + 0x94]
0042950A mov edx, dword ptr [esp + 0x1c]
0042950E xor esi, esi
00429510 mov eax, dword ptr [edx]
00429512 cmp eax, -1
00429515 je 0x42953a
00429517 mov ebp, dword ptr [esp + 0x68]
0042951B mov edi, edx
0042951D cmp esi, ebp
0042951F jge 0x42953a
00429521 cmp eax, -2
00429524 je 0x42952e
00429526 mov eax, dword ptr [edx]
00429528 inc ebx
00429529 mov dword ptr [edi], eax
0042952B add edi, 4
0042952E mov eax, dword ptr [edx + 4]
00429531 add edx, 4
00429534 inc esi
00429535 cmp eax, -1
00429538 jne 0x42951d
0042953A mov eax, dword ptr [ecx + 8]
0042953D mov edx, ebx
0042953F inc eax
00429540 cmp ebx, eax
00429542 jge 0x42955d
00429544 mov eax, dword ptr [esp + 0x1c]
00429548 lea eax, [eax + ebx*4]
0042954B mov dword ptr [eax], 0xffffffff
00429551 mov esi, dword ptr [ecx + 8]
00429554 inc edx
00429555 add eax, 4
00429558 inc esi
00429559 cmp edx, esi
0042955B jl 0x42954b
0042955D inc ebx
0042955E pop edi
0042955F pop esi
00429560 mov dword ptr [ecx + 8], ebx
00429563 pop ebp
00429564 pop ebx
00429565 add esp, 0x80
0042956B ret 8
0042956E nop 
0042956F nop 