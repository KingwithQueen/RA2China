00429570 sub esp, 0x18
00429573 mov edx, dword ptr [esp + 0x2c]
00429577 mov eax, dword ptr [esp + 0x20]
0042957B push ebx
0042957C push ebp
0042957D mov edx, dword ptr [edx]
0042957F push esi
00429580 mov esi, dword ptr [esp + 0x30]
00429584 xor ecx, ecx
00429586 xor bx, bx
00429589 cmp eax, esi
0042958B push edi
0042958C mov dword ptr [esp + 0x20], ecx
00429590 mov dword ptr [esp + 0x10], eax
00429594 mov dword ptr [esp + 0x14], edx
00429598 mov byte ptr [esp + 0x30], bl
0042959C jl 0x429685
004295A2 mov edi, dword ptr [esp + 0x2c]
004295A6 lea eax, [edi + eax*4]
004295A9 mov dword ptr [esp + 0x2c], eax
004295AD mov eax, dword ptr [esp + 0x2c]
004295B1 mov edi, dword ptr [eax]
004295B3 cmp edi, -2
004295B6 jne 0x4295cd
004295B8 mov edi, dword ptr [esp + 0x10]
004295BC dec edi
004295BD sub eax, 4
004295C0 mov dword ptr [esp + 0x10], edi
004295C4 mov dword ptr [esp + 0x2c], eax
004295C8 jmp 0x42967b
004295CD add edi, -4
004295D0 and edi, 7
004295D3 mov eax, edi
004295D5 and eax, 7
004295D8 mov si, word ptr [eax*4 + 0x851a70]
004295E0 lea eax, [eax*4 + 0x851a70]
004295E7 add si, cx
004295EA mov cx, word ptr [eax + 2]
004295EE mov bp, word ptr [eax]
004295F1 add cx, bx
004295F4 mov word ptr [esp + 0x18], si
004295F9 mov word ptr [esp + 0x1a], cx
004295FE mov ebx, dword ptr [esp + 0x18]
00429602 mov dword ptr [esp + 0x24], ebx
00429606 mov bx, word ptr [eax + 2]
0042960A add bx, word ptr [esp + 0x16]
0042960F add bp, dx
00429612 mov word ptr [esp + 0x1c], bp
00429617 mov word ptr [esp + 0x1e], bx
0042961C mov edx, dword ptr [esp + 0x1c]
00429620 movsx eax, cx
00429623 mov dword ptr [esp + 0x14], edx
00429627 cdq 
00429628 mov ecx, eax
0042962A movsx eax, si
0042962D xor ecx, edx
0042962F sub ecx, edx
00429631 cdq 
00429632 xor eax, edx
00429634 sub eax, edx
00429636 cmp eax, ecx
00429638 jg 0x42963c
0042963A mov eax, ecx
0042963C cmp eax, dword ptr [esp + 0x20]
00429640 jle 0x429650
00429642 mov cl, byte ptr [esp + 0x30]
00429646 test cl, cl
00429648 jne 0x42969b
0042964A mov dword ptr [esp + 0x20], eax
0042964E jmp 0x429655
00429650 mov byte ptr [esp + 0x30], 1
00429655 mov ecx, dword ptr [esp + 0x10]
00429659 mov eax, dword ptr [esp + 0x2c]
0042965D mov bx, word ptr [esp + 0x26]
00429662 mov esi, dword ptr [esp + 0x34]
00429666 mov edx, dword ptr [esp + 0x14]
0042966A dec ecx
0042966B sub eax, 4
0042966E mov dword ptr [esp + 0x10], ecx
00429672 mov cx, word ptr [esp + 0x24]
00429677 mov dword ptr [esp + 0x2c], eax
0042967B cmp dword ptr [esp + 0x10], esi
0042967F jge 0x4295ad
00429685 mov eax, dword ptr [esp + 0x38]
00429689 mov ecx, dword ptr [esp + 0x3c]
0042968D pop edi
0042968E mov dword ptr [eax], esi
00429690 pop esi
00429691 pop ebp
00429692 mov dword ptr [ecx], edx
00429694 pop ebx
00429695 add esp, 0x18
00429698 ret 0x14
0042969B mov eax, dword ptr [esp + 0x10]
0042969F mov ecx, dword ptr [esp + 0x38]
004296A3 add edi, -4
004296A6 inc eax
004296A7 and edi, 7
004296AA mov dword ptr [ecx], eax
004296AC mov dx, word ptr [edi*4 + 0x851a70]
004296B4 lea eax, [edi*4 + 0x851a70]
004296BB add dx, bp
004296BE pop edi
004296BF mov ax, word ptr [eax + 2]
004296C3 mov word ptr [esp + 0x30], dx
004296C8 mov edx, dword ptr [esp + 0x38]
004296CC add ax, bx
004296CF mov word ptr [esp + 0x32], ax
004296D4 mov ecx, dword ptr [esp + 0x30]
004296D8 pop esi
004296D9 pop ebp
004296DA mov dword ptr [edx], ecx
004296DC pop ebx
004296DD add esp, 0x18
004296E0 ret 0x14
004296E3 nop 
004296E4 nop 
004296E5 nop 
004296E6 nop 
004296E7 nop 
004296E8 nop 
004296E9 nop 
004296EA nop 
004296EB nop 
004296EC nop 
004296ED nop 
004296EE nop 
004296EF nop 