00428AE0 sub esp, 0x2c
00428AE3 mov eax, dword ptr [esp + 0x30]
00428AE7 push ebx
00428AE8 mov dword ptr [esp + 0x2c], ecx
00428AEC push ebp
00428AED mov ecx, dword ptr [eax + 8]
00428AF0 mov edx, dword ptr [eax + 0x14]
00428AF3 push esi
00428AF4 push edi
00428AF5 mov edi, dword ptr [eax + 0xc]
00428AF8 mov eax, dword ptr [eax]
00428AFA dec ecx
00428AFB or ebx, 0xffffffff
00428AFE xor ebp, ebp
00428B00 xor esi, esi
00428B02 test ecx, ecx
00428B04 mov dword ptr [esp + 0x30], ecx
00428B08 mov dword ptr [esp + 0x28], ebx
00428B0C mov dword ptr [esp + 0x34], edx
00428B10 mov dword ptr [esp + 0x1c], ebp
00428B14 mov byte ptr [esp + 0x40], 0
00428B19 mov dword ptr [esp + 0x14], esi
00428B1D mov dword ptr [esp + 0x18], eax
00428B21 mov dword ptr [esp + 0x10], eax
00428B25 jle 0x428cdb
00428B2B mov eax, dword ptr [esp + 0x1c]
00428B2F mov edx, dword ptr [esp + 0x14]
00428B33 add eax, edx
00428B35 cmp eax, ecx
00428B37 jge 0x428cae
00428B3D mov dl, byte ptr [esp + 0x40]
00428B41 test dl, dl
00428B43 jne 0x428c23
00428B49 lea edx, [esi + ebp]
00428B4C mov eax, dword ptr [edi + edx*4]
00428B4F mov ecx, eax
00428B51 sub ecx, ebx
00428B53 and ecx, 7
00428B56 cmp eax, ebx
00428B58 jne 0x428b5d
00428B5A inc ebp
00428B5B jmp 0x428ba7
00428B5D cmp ecx, 2
00428B60 je 0x428b67
00428B62 cmp ecx, 6
00428B65 jne 0x428b8d
00428B67 cmp ebx, -1
00428B6A je 0x428b8d
00428B6C cmp ebx, 8
00428B6F je 0x428b8d
00428B71 cmp eax, 8
00428B74 je 0x428b8d
00428B76 mov byte ptr [esp + 0x40], 1
00428B7B mov dword ptr [esp + 0x28], eax
00428B7F mov dword ptr [esp + 0x14], 1
00428B87 mov dword ptr [esp + 0x1c], edx
00428B8B jmp 0x428ba7
00428B8D test al, 1
00428B8F mov esi, edx
00428B91 mov ebp, 1
00428B96 je 0x428b9c
00428B98 mov ebx, eax
00428B9A jmp 0x428b9f
00428B9C or ebx, 0xffffffff
00428B9F mov ecx, dword ptr [esp + 0x10]
00428BA3 mov dword ptr [esp + 0x18], ecx
00428BA7 cmp eax, 8
00428BAA jne 0x428bf5
00428BAC lea edx, [esp + 0x10]
00428BB0 mov ecx, 0x8324e0
00428BB5 push edx
00428BB6 call 0x548070
00428BBB movsx eax, word ptr [eax + 0x116]
00428BC2 cmp eax, -1
00428BC5 je 0x428bdc
00428BC7 mov ecx, dword ptr [0x8661cc]
00428BCD mov edx, dword ptr [ecx + eax*4]
00428BD0 mov eax, dword ptr [edx + 0x28]
00428BD3 mov dword ptr [esp + 0x10], eax
00428BD7 jmp 0x428c9f
00428BDC xor eax, eax
00428BDE mov word ptr [esp + 0x20], ax
00428BE3 mov word ptr [esp + 0x22], ax
00428BE8 mov eax, dword ptr [esp + 0x20]
00428BEC mov dword ptr [esp + 0x10], eax
00428BF0 jmp 0x428c9f
00428BF5 mov cx, word ptr [eax*4 + 0x851a70]
00428BFD mov dx, word ptr [eax*4 + 0x851a72]
00428C05 add cx, word ptr [esp + 0x10]
00428C0A add dx, word ptr [esp + 0x12]
00428C0F mov word ptr [esp + 0x24], cx
00428C14 mov word ptr [esp + 0x26], dx
00428C19 mov eax, dword ptr [esp + 0x24]
00428C1D mov dword ptr [esp + 0x10], eax
00428C21 jmp 0x428c9f
00428C23 mov edx, dword ptr [esp + 0x28]
00428C27 cmp dword ptr [edi + eax*4], edx
00428C2A jne 0x428c32
00428C2C inc dword ptr [esp + 0x14]
00428C30 jmp 0x428ca3
00428C32 mov edx, dword ptr [esp + 0x34]
00428C36 mov ecx, dword ptr [esp + 0x14]
00428C3A lea eax, [esp + 0x18]
00428C3E push eax
00428C3F push ecx
00428C40 lea eax, [edx + esi*4]
00428C43 mov edx, dword ptr [esp + 0x4c]
00428C47 push ebp
00428C48 lea ecx, [edi + esi*4]
00428C4B push eax
00428C4C push ecx
00428C4D mov ecx, dword ptr [esp + 0x4c]
00428C51 push edx
00428C52 call 0x428cf0
00428C57 add esi, eax
00428C59 mov cx, word ptr [esp + 0x18]
00428C5E mov ebp, 1
00428C63 mov byte ptr [esp + 0x40], 0
00428C68 mov eax, dword ptr [edi + esi*4]
00428C6B and eax, 7
00428C6E mov dx, word ptr [eax*4 + 0x851a72]
00428C76 add cx, word ptr [eax*4 + 0x851a70]
00428C7E add dx, word ptr [esp + 0x1a]
00428C83 lea eax, [eax*4 + 0x851a70]
00428C8A mov word ptr [esp + 0x2c], cx
00428C8F mov word ptr [esp + 0x2e], dx
00428C94 mov eax, dword ptr [esp + 0x2c]
00428C98 mov dword ptr [esp + 0x10], eax
00428C9C mov ebx, dword ptr [edi + esi*4]
00428C9F mov ecx, dword ptr [esp + 0x30]
00428CA3 lea edx, [esi + ebp]
00428CA6 cmp edx, ecx
00428CA8 jl 0x428b2b
00428CAE mov al, byte ptr [esp + 0x40]
00428CB2 test al, al
00428CB4 je 0x428cdb
00428CB6 mov edx, dword ptr [esp + 0x34]
00428CBA mov ecx, dword ptr [esp + 0x14]
00428CBE lea eax, [esp + 0x18]
00428CC2 push eax
00428CC3 push ecx
00428CC4 lea eax, [edx + esi*4]
00428CC7 mov edx, dword ptr [esp + 0x4c]
00428CCB push ebp
00428CCC lea ecx, [edi + esi*4]
00428CCF push eax
00428CD0 push ecx
00428CD1 mov ecx, dword ptr [esp + 0x4c]
00428CD5 push edx
00428CD6 call 0x428cf0
00428CDB pop edi
00428CDC pop esi
00428CDD pop ebp
00428CDE pop ebx
00428CDF add esp, 0x2c
00428CE2 ret 8