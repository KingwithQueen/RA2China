0055A280 sub esp, 8
0055A283 mov ecx, dword ptr [esp + 0xc]
0055A287 push esi
0055A288 mov eax, dword ptr [ecx]
0055A28A mov edx, dword ptr [ecx + 4]
0055A28D mov dword ptr [esp + 4], eax
0055A291 mov dword ptr [esp + 8], edx
0055A295 cdq 
0055A296 and edx, 0xff
0055A29C add eax, edx
0055A29E mov esi, eax
0055A2A0 mov eax, dword ptr [ecx + 4]
0055A2A3 cdq 
0055A2A4 and edx, 0xff
0055A2AA add eax, edx
0055A2AC sar eax, 8
0055A2AF mov ecx, eax
0055A2B1 sar esi, 8
0055A2B4 shl ecx, 9
0055A2B7 add ecx, esi
0055A2B9 js 0x55a2d0
0055A2BB cmp ecx, dword ptr [0x83261c]
0055A2C1 jge 0x55a2d0
0055A2C3 mov edx, dword ptr [0x832618]
0055A2C9 mov ecx, dword ptr [edx + ecx*4]
0055A2CC test ecx, ecx
0055A2CE jne 0x55a2e8
0055A2D0 mov word ptr [esp + 0x10], si
0055A2D5 mov word ptr [esp + 0x12], ax
0055A2DA mov eax, dword ptr [esp + 0x10]
0055A2DE mov ecx, 0xa6f9f8
0055A2E3 mov dword ptr [0xa6fa1c], eax
0055A2E8 lea edx, [esp + 4]
0055A2EC push edx
0055A2ED call 0x4706c0
0055A2F2 pop esi
0055A2F3 add esp, 8
0055A2F6 ret 4
0055A2F9 nop 
0055A2FA nop 
0055A2FB nop 
0055A2FC nop 
0055A2FD nop 
0055A2FE nop 
0055A2FF nop 
0055A300 sub esp, 0x14
0055A303 push ebx
0055A304 push esi
0055A305 push edi
0055A306 mov edi, ecx
0055A308 mov ebx, 1
0055A30D mov eax, dword ptr [edi + 0xf0]
0055A313 mov dword ptr [edi + 0x108], ebx
0055A319 mov dword ptr [edi + 0x10c], eax
0055A31F lea ecx, [eax - 1]
0055A322 mov dword ptr [edi + 0x110], ecx
0055A328 mov edx, dword ptr [edi + 0x138]
0055A32E shl eax, 0xb
0055A331 mov ecx, edi
0055A333 lea eax, [eax + edx + 4]
0055A337 mov dword ptr [edi + 0x114], eax
0055A33D call 0x55a490
0055A342 mov esi, eax
0055A344 test esi, esi
0055A346 je 0x55a3a9
0055A348 test byte ptr [esi + 0x140], 0x20
0055A34F je 0x55a39c
0055A351 mov eax, dword ptr [esi + 0x12c]
0055A357 mov edx, dword ptr [esi + 0x140]
0055A35D and al, 0xe7
0055A35F and edx, 0xffffffdc
0055A362 mov dword ptr [esi + 0x12c], eax
0055A368 mov dword ptr [esi + 0x140], edx
0055A36E mov byte ptr [esi + 0x138], bl
0055A374 mov ecx, dword ptr [0x83996c]
0055A37A push esi
0055A37B call 0x6aadd0
0055A380 cmp byte ptr [esi + 0x120], 0xfe
0055A387 jne 0x55a39c
0055A389 mov ecx, dword ptr [0xa35db4]
0055A38F push ebx
0055A390 push ecx
0055A391 push esi
0055A392 mov ecx, 0x8324e0
0055A397 call 0x568520
0055A39C mov ecx, edi
0055A39E call 0x55a490
0055A3A3 mov esi, eax
0055A3A5 test esi, esi
0055A3A7 jne 0x55a348
0055A3A9 mov eax, dword ptr [edi + 0xf0]
0055A3AF mov dword ptr [edi + 0x108], ebx
0055A3B5 mov dword ptr [edi + 0x10c], eax
0055A3BB lea edx, [eax - 1]
0055A3BE mov dword ptr [edi + 0x110], edx
0055A3C4 mov ecx, dword ptr [edi + 0x138]
0055A3CA shl eax, 0xb
0055A3CD lea edx, [eax + ecx + 4]
0055A3D1 mov ecx, edi
0055A3D3 mov dword ptr [edi + 0x114], edx
0055A3D9 call 0x55a490
0055A3DE mov esi, eax
0055A3E0 test esi, esi
0055A3E2 je 0x55a484
0055A3E8 mov eax, dword ptr [esi]
0055A3EA lea ecx, [esp + 0x14]
0055A3EE push ecx
0055A3EF mov ecx, esi
0055A3F1 call dword ptr [eax + 0x48]
0055A3F4 mov ecx, eax
0055A3F6 push 0
0055A3F8 mov eax, dword ptr [ecx]
0055A3FA cdq 
0055A3FB and edx, 0xff
0055A401 add eax, edx
0055A403 sar eax, 8
0055A406 mov word ptr [esp + 0x10], ax
0055A40B mov eax, dword ptr [ecx + 4]
0055A40E cdq 
0055A40F and edx, 0xff
0055A415 mov ecx, dword ptr [0x83996c]
0055A41B add eax, edx
0055A41D sar eax, 8
0055A420 mov word ptr [esp + 0x12], ax
0055A425 mov edx, dword ptr [esp + 0x10]
0055A429 lea eax, [esp + 0x14]
0055A42D mov dword ptr [esp + 0x14], edx
0055A431 push eax
0055A432 call 0x6a8d40
0055A437 cmp al, byte ptr [esi + 0x120]
0055A43D je 0x55a473
0055A43F mov byte ptr [esi + 0x120], al
0055A445 mov byte ptr [esi + 0x138], bl
0055A44B mov ecx, dword ptr [0x83996c]
0055A451 push esi
0055A452 call 0x6aadd0
0055A457 cmp byte ptr [esi + 0x120], 0xfe
0055A45E jne 0x55a473
0055A460 mov ecx, dword ptr [0xa35db4]
0055A466 push ebx
0055A467 push ecx
0055A468 push esi
0055A469 mov ecx, 0x8324e0
0055A46E call 0x568520
0055A473 mov ecx, edi
0055A475 call 0x55a490
0055A47A mov esi, eax
0055A47C test esi, esi
0055A47E jne 0x55a3e8
0055A484 pop edi
0055A485 pop esi
0055A486 pop ebx
0055A487 add esp, 0x14
0055A48A ret 
0055A48B nop 
0055A48C nop 
0055A48D nop 
0055A48E nop 
0055A48F nop 
0055A490 mov eax, dword ptr [ecx + 0x110]
0055A496 push ebp
0055A497 mov ebp, dword ptr [ecx + 0x114]
0055A49D push esi
0055A49E test eax, eax
0055A4A0 je 0x55a4d5
0055A4A2 mov esi, dword ptr [ecx + 0x108]
0055A4A8 mov edx, dword ptr [ecx + 0x10c]
0055A4AE inc esi
0055A4AF dec edx
0055A4B0 dec eax
0055A4B1 mov dword ptr [ecx + 0x108], esi
0055A4B7 mov dword ptr [ecx + 0x110], eax
0055A4BD lea eax, [ebp - 0x7fc]
0055A4C3 mov dword ptr [ecx + 0x10c], edx
0055A4C9 mov dword ptr [ecx + 0x114], eax
0055A4CF mov eax, dword ptr [ebp]
0055A4D2 pop esi
0055A4D3 pop ebp
0055A4D4 ret 
0055A4D5 mov edx, dword ptr [ecx + 0x10c]
0055A4DB mov eax, dword ptr [ecx + 0x108]
0055A4E1 mov esi, dword ptr [ecx + 0xf0]
0055A4E7 push edi
0055A4E8 mov dword ptr [ecx + 0x108], edx
0055A4EE mov edi, edx
0055A4F0 sub edx, esi
0055A4F2 mov dword ptr [ecx + 0x10c], eax
0055A4F8 lea edx, [edx + eax - 1]
0055A4FC test dl, 1
0055A4FF je 0x55a50b
0055A501 inc eax
0055A502 dec esi
0055A503 mov dword ptr [ecx + 0x10c], eax
0055A509 jmp 0x55a515
0055A50B inc edi
0055A50C add esi, -2
0055A50F mov dword ptr [ecx + 0x108], edi
0055A515 mov eax, dword ptr [ecx + 0x10c]