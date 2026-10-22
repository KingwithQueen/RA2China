004A43A0 mov ecx, eax
004A43A2 mov eax, dword ptr [ecx + 0x140]
004A43A8 test ah, 1
004A43AB je 0x4a43e5
004A43AD mov edx, dword ptr [ebp + 0xc]
004A43B0 mov byte ptr [esp + 0x68], 1
004A43B5 add edx, 0x88
004A43BB movsx edi, byte ptr [ecx + 0x11b]
004A43C2 mov eax, dword ptr [edx]
004A43C4 mov dword ptr [esp + 0x44], eax
004A43C8 mov eax, dword ptr [edx + 4]
004A43CB mov dword ptr [esp + 0x48], eax
004A43CF mov eax, dword ptr [edx + 8]
004A43D2 cdq 
004A43D3 idiv dword ptr [0x8529d0]
004A43D9 sub eax, edi
004A43DB cdq 
004A43DC xor eax, edx
004A43DE sub eax, edx
004A43E0 cmp eax, 2
004A43E3 jg 0x4a43ea
004A43E5 mov byte ptr [esp + 0x68], 0
004A43EA mov edx, dword ptr [esp + 0x68]
004A43EE push edx
004A43EF push 1
004A43F1 push 1
004A43F3 push 0x852998
004A43F8 call 0x476920
004A43FD jmp 0x4a4174
004A4402 cmp esi, 1
004A4405 jne 0x4a44d1
004A440B lea eax, [esp + 0x14]
004A440F mov ecx, 0x8324e0
004A4414 push eax
004A4415 call 0x548070
004A441A mov ecx, eax
004A441C call 0x478740
004A4421 mov al, byte ptr [esp + 0x64]
004A4425 test al, al
004A4427 je 0x4a4450
004A4429 mov ecx, dword ptr [ebp + 0xc]
004A442C mov edx, dword ptr [esp + 0x60]
004A4430 push 0
004A4432 push 0
004A4434 mov dword ptr [ecx + 0x4d0], 0xffffffff
004A443E push edx
004A443F mov ecx, ebp
004A4441 call 0x4a2670
004A4446 pop edi
004A4447 pop esi
004A4448 pop ebp
004A4449 pop ebx
004A444A add esp, 0x4c
004A444D ret 0xc
004A4450 mov eax, dword ptr [0x852998]
004A4455 mov ecx, dword ptr [ebp + 0x40]
004A4458 cmp ecx, eax
004A445A jne 0x4a4476
004A445C mov ecx, dword ptr [ebp + 0x44]
004A445F mov edx, dword ptr [0x85299c]
004A4465 cmp ecx, edx
004A4467 jne 0x4a4476
004A4469 mov edx, dword ptr [ebp + 0x48]
004A446C mov ecx, dword ptr [0x8529a0]
004A4472 cmp edx, ecx
004A4474 je 0x4a448e
004A4476 mov dword ptr [ebp + 0x40], eax
004A4479 mov eax, dword ptr [0x85299c]
004A447E mov dword ptr [ebp + 0x44], eax
004A4481 mov ecx, dword ptr [0x8529a0]
004A4487 mov dword ptr [ebp + 0x48], ecx
004A448A mov byte ptr [ebp + 0x63], 0
004A448E mov ecx, dword ptr [ebp + 0xc]
004A4491 mov eax, dword ptr [ecx + 0x488]
004A4497 test eax, eax
004A4499 jne 0x4a44b3
004A449B mov edx, dword ptr [ecx]
004A449D push 1
004A449F push 0
004A44A1 call dword ptr [edx + 0x410]
004A44A7 pop edi
004A44A8 pop esi
004A44A9 pop ebp
004A44AA xor al, al
004A44AC pop ebx
004A44AD add esp, 0x4c
004A44B0 ret 0xc
004A44B3 call 0x4cd9b0
004A44B8 mov ecx, dword ptr [ebp + 0xc]
004A44BB push 1
004A44BD push 0
004A44BF mov eax, dword ptr [ecx]
004A44C1 call dword ptr [eax + 0x414]
004A44C7 pop edi
004A44C8 pop esi
004A44C9 pop ebp
004A44CA pop ebx
004A44CB add esp, 0x4c
004A44CE ret 0xc
004A44D1 cmp esi, 7
004A44D4 jne 0x4a4174
004A44DA mov al, byte ptr [esp + 0x64]
004A44DE test al, al
004A44E0 je 0x4a4522
004A44E2 mov dword ptr [ecx + 0x4d0], 0xffffffff
004A44EC mov edx, dword ptr [ebp + 0xc]
004A44EF mov eax, dword ptr [0xa40d2c]
004A44F4 xor ecx, ecx
004A44F6 add edx, 0x530
004A44FC mov dword ptr [edx], eax
004A44FE mov eax, dword ptr [esp + 0x54]
004A4502 mov dword ptr [edx + 4], eax
004A4505 push 0
004A4507 push 0
004A4509 mov dword ptr [edx + 8], ecx
004A450C mov ecx, dword ptr [esp + 0x68]
004A4510 push ecx
004A4511 mov ecx, ebp
004A4513 call 0x4a2670
004A4518 pop edi
004A4519 pop esi
004A451A pop ebp
004A451B pop ebx
004A451C add esp, 0x4c
004A451F ret 0xc
004A4522 mov eax, dword ptr [0x852998]
004A4527 mov edx, dword ptr [ebp + 0x40]
004A452A cmp edx, eax
004A452C jne 0x4a4548
004A452E mov edx, dword ptr [ebp + 0x44]
004A4531 mov esi, dword ptr [0x85299c]
004A4537 cmp edx, esi
004A4539 jne 0x4a4548
004A453B mov edx, dword ptr [ebp + 0x48]
004A453E mov esi, dword ptr [0x8529a0]
004A4544 cmp edx, esi
004A4546 je 0x4a4560
004A4548 mov dword ptr [ebp + 0x40], eax
004A454B mov eax, dword ptr [0x85299c]
004A4550 mov dword ptr [ebp + 0x44], eax
004A4553 mov edx, dword ptr [0x8529a0]
004A4559 mov dword ptr [ebp + 0x48], edx
004A455C mov byte ptr [ebp + 0x63], 0
004A4560 mov eax, dword ptr [ecx + 0x488]
004A4566 test eax, eax
004A4568 je 0x4a3a38
004A456E call 0x4cd9b0
004A4573 mov ecx, dword ptr [ebp + 0xc]
004A4576 push 1
004A4578 push 0
004A457A mov edx, dword ptr [ecx]
004A457C call dword ptr [edx + 0x414]
004A4582 pop edi
004A4583 pop esi
004A4584 pop ebp
004A4585 pop ebx
004A4586 add esp, 0x4c
004A4589 ret 0xc