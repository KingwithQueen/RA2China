00428CF0 sub esp, 0x34
00428CF3 push ebx
00428CF4 push ebp
00428CF5 mov ebp, dword ptr [esp + 0x44]
00428CF9 push esi
00428CFA mov esi, dword ptr [esp + 0x50]
00428CFE push edi
00428CFF mov edx, dword ptr [ebp]
00428D02 mov eax, dword ptr [ebp + esi*4]
00428D06 mov dword ptr [esp + 0x38], edx
00428D0A lea edi, [edx + eax]
00428D0D sar edi, 1
00428D0F mov dword ptr [esp + 0x18], edi
00428D13 lea ecx, [edi + 1]
00428D16 cmp ecx, eax
00428D18 je 0x428d2a
00428D1A cmp ecx, edx
00428D1C je 0x428d2a
00428D1E mov dword ptr [esp + 0x18], 0
00428D26 mov edi, dword ptr [esp + 0x18]
00428D2A cmp edx, 8
00428D2D je 0x429074
00428D33 cmp eax, 8
00428D36 je 0x429074
00428D3C mov eax, dword ptr [esp + 0x5c]
00428D40 mov edx, dword ptr [esp + 0x58]
00428D44 cmp esi, edx
00428D46 mov eax, dword ptr [eax]
00428D48 mov dword ptr [esp + 0x10], eax
00428D4C jge 0x428d57
00428D4E mov dword ptr [esp + 0x58], esi
00428D52 jmp 0x428dd8
00428D57 cmp edx, esi
00428D59 mov dword ptr [esp + 0x58], edx
00428D5D jge 0x428dd8
00428D5F mov ecx, esi
00428D61 mov dword ptr [esp + 0x14], eax
00428D65 sub ecx, edx
00428D67 test ecx, ecx
00428D69 jle 0x428dd4
00428D6B mov ebx, ebp
00428D6D mov ebp, ecx
00428D6F mov eax, dword ptr [ebx]
00428D71 cmp eax, 8
00428D74 jne 0x428dae
00428D76 lea ecx, [esp + 0x14]
00428D7A push ecx
00428D7B mov ecx, 0x8324e0
00428D80 call 0x548070
00428D85 movsx eax, word ptr [eax + 0x116]
00428D8C cmp eax, -1
00428D8F je 0x428d9f
00428D91 mov edx, dword ptr [0x8661cc]
00428D97 mov eax, dword ptr [edx + eax*4]
00428D9A mov eax, dword ptr [eax + 0x28]
00428D9D jmp 0x428dc6
00428D9F push 0
00428DA1 push 0
00428DA3 lea ecx, [esp + 0x3c]
00428DA7 call 0x42ad30
00428DAC jmp 0x428dc4
00428DAE lea ecx, [eax*4 + 0x851a70]
00428DB5 lea edx, [esp + 0x30]
00428DB9 push ecx
00428DBA push edx
00428DBB lea ecx, [esp + 0x1c]
00428DBF call 0x42add0
00428DC4 mov eax, dword ptr [eax]
00428DC6 add ebx, 4
00428DC9 dec ebp
00428DCA mov dword ptr [esp + 0x14], eax
00428DCE jne 0x428d6f
00428DD0 mov ebp, dword ptr [esp + 0x4c]
00428DD4 mov dword ptr [esp + 0x10], eax
00428DD8 mov ebx, dword ptr [esp + 0x48]
00428DDC mov ecx, ebx
00428DDE call 0x4cafb0
00428DE3 mov eax, dword ptr [ebx + 0x1b4]
00428DE9 fstp qword ptr [esp + 0x3c]
00428DED mov dword ptr [esp + 0x30], eax
00428DF1 mov eax, dword ptr [esp + 0x58]
00428DF5 test eax, eax
00428DF7 jle 0x428f93
00428DFD mov ecx, eax
00428DFF mov eax, dword ptr [esp + 0x10]
00428E03 and edi, 7
00428E06 add ecx, ecx
00428E08 mov dword ptr [esp + 0x20], ecx
00428E0C lea ebp, [edi*4 + 0x851a70]
00428E13 jmp 0x428e19
00428E15 mov ecx, dword ptr [esp + 0x20]
00428E19 mov dx, word ptr [ebp]
00428E1D mov dword ptr [esp + 0x1c], ecx
00428E21 add dx, ax
00428E24 mov ax, word ptr [ebp + 2]
00428E28 add ax, word ptr [esp + 0x12]
00428E2D mov word ptr [esp + 0x24], dx
00428E32 xor bl, bl
00428E34 mov word ptr [esp + 0x26], ax
00428E39 mov eax, dword ptr [esp + 0x58]
00428E3D mov edx, dword ptr [esp + 0x24]
00428E41 sub eax, ecx
00428E43 mov ecx, dword ptr [esp + 0x50]
00428E47 add eax, esi
00428E49 mov dword ptr [esp + 0x14], edx
00428E4D lea edx, [esp + 0x14]
00428E51 mov esi, dword ptr [ecx + eax*4]
00428E54 push edx
00428E55 mov ecx, 0x8324e0
00428E5A call 0x548070
00428E5F mov edi, eax
00428E61 mov eax, dword ptr [esp + 0x1c]
00428E65 test eax, eax
00428E67 jle 0x428f2d
00428E6D mov ecx, dword ptr [esp + 0x48]
00428E71 mov edx, dword ptr [esp + 0x18]
00428E75 push 1
00428E77 push 0
00428E79 mov eax, dword ptr [ecx]
00428E7B push esi
00428E7C push edx
00428E7D push edi
00428E7E call dword ptr [eax + 0x194]
00428E84 test eax, eax
00428E86 jne 0x428ec5
00428E88 test dword ptr [edi + 0x140], 0x40000
00428E92 jne 0x428ec5
00428E94 mov eax, dword ptr [esp + 0x30]
00428E98 lea ecx, [esp + 0x10]
00428E9C push eax
00428E9D push ecx
00428E9E mov ecx, 0x8324e0
00428EA3 call 0x54e3a0
00428EA8 mov dword ptr [esp + 0x34], eax
00428EAC fild dword ptr [esp + 0x34]
00428EB0 fmul qword ptr [esp + 0x3c]
00428EB4 fcomp qword ptr [0x79a708]
00428EBA fnstsw ax
00428EBC test ah, 1
00428EBF je 0x428ec5
00428EC1 xor bl, bl
00428EC3 jmp 0x428ec7
00428EC5 mov bl, 1
00428EC7 mov eax, dword ptr [esp + 0x1c]
00428ECB mov dx, word ptr [ebp]
00428ECF add dx, word ptr [esp + 0x14]
00428ED4 dec eax
00428ED5 mov dword ptr [esp + 0x1c], eax
00428ED9 mov ax, word ptr [ebp + 2]
00428EDD add ax, word ptr [esp + 0x16]
00428EE2 mov word ptr [esp + 0x28], dx
00428EE7 lea edx, [esp + 0x14]
00428EEB mov word ptr [esp + 0x2a], ax
00428EF0 mov ecx, dword ptr [esp + 0x28]
00428EF4 mov dword ptr [esp + 0x14], ecx
00428EF8 push edx
00428EF9 mov ecx, 0x8324e0
00428EFE call 0x548070
00428F03 mov edi, eax
00428F05 movsx eax, byte ptr [edi + 0x11b]
00428F0C sub esi, eax
00428F0E cmp esi, 4
00428F11 jne 0x428f21
00428F13 mov ecx, dword ptr [edi + 0x140]
00428F19 lea esi, [eax + 4]
00428F1C test ch, 1
00428F1F jne 0x428f23
00428F21 mov esi, eax
00428F23 test bl, bl
00428F25 je 0x428e61
00428F2B jmp 0x428f35
00428F2D test bl, bl
00428F2F je 0x428fd3
00428F35 mov eax, dword ptr [esp + 0x38]
00428F39 mov cx, word ptr [esp + 0x10]
00428F3E and eax, 7
00428F41 mov esi, dword ptr [esp + 0x20]
00428F45 sub esi, 2
00428F48 add cx, word ptr [eax*4 + 0x851a70]
00428F50 mov dx, word ptr [eax*4 + 0x851a72]
00428F58 add dx, word ptr [esp + 0x12]
00428F5D lea eax, [eax*4 + 0x851a70]
00428F64 mov word ptr [esp + 0x2c], cx
00428F69 mov ecx, dword ptr [esp + 0x58]
00428F6D mov word ptr [esp + 0x2e], dx
00428F72 mov eax, dword ptr [esp + 0x2c]
00428F76 dec ecx
00428F77 mov dword ptr [esp + 0x20], esi
00428F7B mov esi, dword ptr [esp + 0x54]
00428F7F mov dword ptr [esp + 0x10], eax
00428F83 test ecx, ecx
00428F85 mov dword ptr [esp + 0x58], ecx
00428F89 jg 0x428e15
00428F8F mov ebp, dword ptr [esp + 0x4c]
00428F93 mov edx, dword ptr [esp + 0x5c]
00428F97 test esi, esi
00428F99 mov eax, dword ptr [edx]
00428F9B mov dword ptr [esp + 0x4c], eax
00428F9F jle 0x428fc1
00428FA1 mov edi, ebp
00428FA3 mov ebx, esi
00428FA5 mov eax, dword ptr [edi]
00428FA7 lea edx, [esp + 0x4c]
00428FAB push eax
00428FAC lea ecx, [esp + 0x58]
00428FB0 call 0x42ad50
00428FB5 mov eax, dword ptr [eax]
00428FB7 add edi, 4
00428FBA dec ebx
00428FBB mov dword ptr [esp + 0x4c], eax
00428FBF jne 0x428fa5
00428FC1 mov ecx, dword ptr [esp + 0x5c]
00428FC5 pop edi
00428FC6 mov dword ptr [ecx], eax
00428FC8 mov eax, esi
00428FCA pop esi
00428FCB pop ebp
00428FCC pop ebx
00428FCD add esp, 0x34
00428FD0 ret 0x18
00428FD3 mov eax, dword ptr [esp + 0x58]
00428FD7 mov esi, dword ptr [esp + 0x54]
00428FDB mov edx, dword ptr [esp + 0x4c]
00428FDF sub esi, eax
00428FE1 lea ecx, [eax + eax]
00428FE4 test ecx, ecx
00428FE6 lea edi, [edx + esi*4]
00428FE9 jle 0x428ff1
00428FEB mov eax, dword ptr [esp + 0x18]
00428FEF rep stosd dword ptr es:[edi], eax
00428FF1 mov ebp, dword ptr [esp + 0x5c]
00428FF5 test esi, esi
00428FF7 mov eax, dword ptr [ebp]
00428FFA mov dword ptr [esp + 0x5c], eax
00428FFE jle 0x429065
00429000 mov edi, edx
00429002 mov ebx, esi
00429004 mov eax, dword ptr [edi]
00429006 cmp eax, 8
00429009 jne 0x429043
0042900B lea eax, [esp + 0x5c]
0042900F mov ecx, 0x8324e0
00429014 push eax
00429015 call 0x548070
0042901A movsx eax, word ptr [eax + 0x116]
00429021 cmp eax, -1
00429024 je 0x429034
00429026 mov ecx, dword ptr [0x8661cc]
0042902C mov edx, dword ptr [ecx + eax*4]
0042902F mov eax, dword ptr [edx + 0x28]
00429032 jmp 0x42905b
00429034 push 0
00429036 push 0
00429038 lea ecx, [esp + 0x54]
0042903C call 0x42ad30
00429041 jmp 0x429059
00429043 lea eax, [eax*4 + 0x851a70]
0042904A lea ecx, [esp + 0x54]
0042904E push eax
0042904F push ecx
00429050 lea ecx, [esp + 0x64]
00429054 call 0x42add0
00429059 mov eax, dword ptr [eax]
0042905B add edi, 4
0042905E dec ebx
0042905F mov dword ptr [esp + 0x5c], eax
00429063 jne 0x429004
00429065 mov dword ptr [ebp], eax
00429068 mov eax, esi
0042906A pop edi
0042906B pop esi
0042906C pop ebp
0042906D pop ebx
0042906E add esp, 0x34
00429071 ret 0x18
00429074 mov edx, dword ptr [esp + 0x58]
00429078 mov ebp, dword ptr [esp + 0x5c]
0042907C mov eax, dword ptr [ebp]
0042907F lea ebx, [esi + edx]
00429082 test ebx, ebx
00429084 mov dword ptr [esp + 0x5c], eax
00429088 jle 0x4290ac
0042908A mov esi, dword ptr [esp + 0x4c]
0042908E mov edi, ebx
00429090 mov eax, dword ptr [esi]
00429092 lea edx, [esp + 0x5c]
00429096 push eax
00429097 lea ecx, [esp + 0x50]
0042909B call 0x42ad50
004290A0 mov eax, dword ptr [eax]
004290A2 add esi, 4
004290A5 dec edi
004290A6 mov dword ptr [esp + 0x5c], eax
004290AA jne 0x429090
004290AC pop edi
004290AD mov dword ptr [ebp], eax
004290B0 pop esi
004290B1 mov eax, ebx
004290B3 pop ebp
004290B4 pop ebx
004290B5 add esp, 0x34
004290B8 ret 0x18
004290BB nop 
004290BC nop 
004290BD nop 
004290BE nop 
004290BF nop 