00427370 sub esp, 0x4c
00427373 push ebx
00427374 push ebp
00427375 push esi
00427376 push edi
00427377 mov edi, dword ptr [esp + 0x64]
0042737B mov ebp, dword ptr [esp + 0x60]
0042737F mov esi, ecx
00427381 mov eax, dword ptr [0x832618]
00427386 movsx ecx, word ptr [edi + 2]
0042738A movsx edx, word ptr [edi]
0042738D movsx ebx, word ptr [ebp]
00427391 shl ecx, 9
00427394 add ecx, edx
00427396 mov dword ptr [esp + 0x28], 0
0042739E movsx edx, word ptr [ebp + 2]
004273A2 shl edx, 9
004273A5 add edx, ebx
004273A7 lea ecx, [eax + ecx*4]
004273AA mov dword ptr [esp + 0x38], ecx
004273AE mov ecx, dword ptr [ecx]
004273B0 lea eax, [eax + edx*4]
004273B3 mov dword ptr [esp + 0x2c], eax
004273B7 mov dword ptr [esp + 0x30], ecx
004273BB mov eax, dword ptr [eax]
004273BD test eax, eax
004273BF mov dword ptr [esp + 0x60], eax
004273C3 je 0x427d2e
004273C9 test ecx, ecx
004273CB je 0x427d2e
004273D1 mov ebx, dword ptr [esp + 0x68]
004273D5 mov ecx, ebx
004273D7 mov eax, dword ptr [ebx]
004273D9 call dword ptr [eax + 0x2c]
004273DC cmp eax, 2
004273DF mov eax, dword ptr [esp + 0x30]
004273E3 je 0x4273fc
004273E5 mov ecx, dword ptr [eax + 0x140]
004273EB test ch, 1
004273EE je 0x4273fc
004273F0 movsx eax, byte ptr [eax + 0x11b]
004273F7 add eax, 4
004273FA jmp 0x427403
004273FC movsx eax, byte ptr [eax + 0x11b]
00427403 mov dword ptr [esi + 0x34], eax
00427406 mov edx, dword ptr [ebx]
00427408 mov ecx, ebx
0042740A call dword ptr [edx + 0x2c]
0042740D cmp eax, 2
00427410 je 0x427429
00427412 mov al, byte ptr [ebx + 0x79]
00427415 test al, al
00427417 je 0x427429
00427419 mov eax, dword ptr [esp + 0x60]
0042741D movsx eax, byte ptr [eax + 0x11b]
00427424 add eax, 4
00427427 jmp 0x427434
00427429 mov ecx, dword ptr [esp + 0x60]
0042742D movsx eax, byte ptr [ecx + 0x11b]
00427434 mov dword ptr [esi + 0x30], eax
00427437 mov edx, dword ptr [ebx]
00427439 mov ecx, ebx
0042743B call dword ptr [edx + 0x80]
00427441 mov cl, byte ptr [eax + 0xaa0]
00427447 test cl, cl
00427449 je 0x427490
0042744B mov eax, dword ptr [esp + 0x60]
0042744F mov ecx, dword ptr [eax + 0x140]
00427455 test ch, 1
00427458 je 0x427490
0042745A lea ecx, [ebx + 0x88]
00427460 mov edx, dword ptr [ebx + 0x88]
00427466 mov dword ptr [esp + 0x50], edx
0042746A mov eax, dword ptr [ecx + 4]
0042746D mov dword ptr [esp + 0x54], eax
00427471 mov eax, dword ptr [ecx + 8]
00427474 mov ecx, dword ptr [esi + 0x30]
00427477 cdq 
00427478 idiv dword ptr [0x84e800]
0042747E sub eax, ecx
00427480 cdq 
00427481 xor eax, edx
00427483 sub eax, edx
00427485 cmp eax, 2
00427488 jle 0x427490
0042748A add ecx, 4
0042748D mov dword ptr [esi + 0x30], ecx
00427490 mov edx, dword ptr [ebx]
00427492 mov ecx, ebx
00427494 call dword ptr [edx + 0x80]
0042749A mov eax, dword ptr [eax + 0x5a4]
004274A0 mov edx, dword ptr [esi + 0x40]
004274A3 mov dword ptr [esi + 0x2c], eax
004274A6 mov eax, dword ptr [esp + 0x2c]
004274AA mov dword ptr [esi + 0x6c], 0
004274B1 mov ecx, dword ptr [ebp]
004274B4 push 0
004274B6 push edi
004274B7 mov dword ptr [esi + 0x70], ecx
004274BA push eax
004274BB push 0
004274BD mov ecx, esi
004274BF mov dword ptr [esp + 0x50], edx
004274C3 call 0x427d40
004274C8 mov cx, word ptr [ebp]
004274CC mov dword ptr [esp + 0x14], eax
004274D0 cmp cx, word ptr [edi]
004274D3 jne 0x4274ed
004274D5 mov dx, word ptr [ebp + 2]
004274D9 cmp dx, word ptr [edi + 2]
004274DD jne 0x4274ed
004274DF mov eax, dword ptr [esi + 0x30]
004274E2 mov ecx, dword ptr [esi + 0x34]
004274E5 cmp eax, ecx
004274E7 je 0x427d2e
004274ED mov eax, dword ptr [esi + 0x3c]
004274F0 test eax, eax
004274F2 je 0x4274fc
004274F4 push ebx
004274F5 mov ecx, esi
004274F7 call 0x4285d0
004274FC mov ecx, dword ptr [esp + 0x60]
00427500 movsx eax, word ptr [ecx + 0x26]
00427504 imul eax, dword ptr [0x84e804]
0042750B movsx edx, word ptr [ecx + 0x24]
0042750F movsx ecx, byte ptr [ecx + 0x11b]
00427516 add eax, edx
00427518 mov edx, dword ptr [esi + 0x30]
0042751B cmp edx, ecx
0042751D jle 0x427534
0042751F mov edx, dword ptr [esi + 0x1c]
00427522 mov ecx, dword ptr [esi + 0x28]
00427525 mov dword ptr [edx + eax*4], ecx
00427528 mov edx, dword ptr [esi + 0x20]
0042752B mov dword ptr [edx + eax*4], 0
00427532 jmp 0x427547
00427534 mov ecx, dword ptr [esi + 0x18]
00427537 mov edx, dword ptr [esi + 0x28]
0042753A mov dword ptr [ecx + eax*4], edx
0042753D mov ecx, dword ptr [esi + 0x24]
00427540 mov dword ptr [ecx + eax*4], 0
00427547 mov edx, dword ptr [ebx]
00427549 mov ecx, ebx
0042754B mov byte ptr [esp + 0x12], 0
00427550 call dword ptr [edx + 0x80]
00427556 mov cl, byte ptr [eax + 0xaa0]
0042755C test cl, cl
0042755E je 0x427608
00427564 mov byte ptr [esp + 0x12], 1
00427569 xor ebp, ebp
0042756B mov edi, 0x79c484
00427570 lea eax, [esp + 0x60]
00427574 lea ecx, [ebx + 0x2e0]
0042757A push eax
0042757B call 0x4b8be0
00427580 mov eax, dword ptr [eax]
00427582 shr eax, 0xc
00427585 inc eax
00427586 shr eax, 1
00427588 and eax, 7
0042758B sub eax, ebp
0042758D cdq 
0042758E xor eax, edx
00427590 sub eax, edx
00427592 cmp eax, 2
00427595 jle 0x4275f8
00427597 cmp eax, 6
0042759A jge 0x4275f8
0042759C cmp edi, 0x79c4a4
004275A2 je 0x4275f8
004275A4 mov ecx, dword ptr [edi]
004275A6 mov edx, dword ptr [esp + 0x2c]
004275AA lea eax, [edx + ecx*4]
004275AD mov ecx, dword ptr [edx + ecx*4]
004275B0 movsx eax, word ptr [ecx + 0x26]
004275B4 imul eax, dword ptr [0x84e804]
004275BB movsx edx, word ptr [ecx + 0x24]
004275BF movsx ecx, byte ptr [ecx + 0x11b]
004275C6 add eax, edx
004275C8 mov edx, dword ptr [esi + 0x30]
004275CB inc ecx
004275CC cmp edx, ecx
004275CE jle 0x4275e5
004275D0 mov edx, dword ptr [esi + 0x1c]
004275D3 mov ecx, dword ptr [esi + 0x28]
004275D6 mov dword ptr [edx + eax*4], ecx
004275D9 mov edx, dword ptr [esi + 0x20]
004275DC mov dword ptr [edx + eax*4], 0
004275E3 jmp 0x4275f8
004275E5 mov ecx, dword ptr [esi + 0x18]
004275E8 mov edx, dword ptr [esi + 0x28]
004275EB mov dword ptr [ecx + eax*4], edx
004275EE mov ecx, dword ptr [esi + 0x24]
004275F1 mov dword ptr [ecx + eax*4], 0
004275F8 add edi, 4
004275FB inc ebp
004275FC cmp edi, 0x79c4a4
00427602 jle 0x427570
00427608 mov edx, dword ptr [ebx]
0042760A mov ecx, ebx
0042760C call dword ptr [edx + 0x2c]
0042760F cmp eax, 1
00427612 jne 0x427629
00427614 mov eax, dword ptr [ebx + 0x5ac]
0042761A mov byte ptr [esp + 0x13], 1
0042761F mov cl, byte ptr [eax + 0xba4]
00427625 test cl, cl
00427627 jne 0x42762e
00427629 mov byte ptr [esp + 0x13], 0
0042762E mov eax, dword ptr [esp + 0x70]
00427632 test eax, eax
00427634 jge 0x42763e
00427636 mov dword ptr [esp + 0x70], 0xfff7
0042763E mov eax, dword ptr [esp + 0x14]
00427642 test eax, eax
00427644 je 0x427d1f