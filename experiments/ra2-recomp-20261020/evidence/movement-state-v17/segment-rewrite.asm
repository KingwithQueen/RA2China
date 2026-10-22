004296F0 sub esp, 0x34
004296F3 mov eax, dword ptr [esp + 0x44]
004296F7 push ebx
004296F8 push ebp
004296F9 push esi
004296FA mov cx, word ptr [eax]
004296FD mov dx, word ptr [eax + 2]
00429701 test cx, cx
00429704 push edi
00429705 mov dword ptr [esp + 0x34], 0
0042970D movsx esi, cx
00429710 movsx eax, dx
00429713 jge 0x429726
00429715 xor ecx, ecx
00429717 test dx, dx
0042971A setge cl
0042971D dec ecx
0042971E and ecx, 2
00429721 add ecx, 5
00429724 jmp 0x429735
00429726 xor ecx, ecx
00429728 test dx, dx
0042972B setge cl
0042972E dec ecx
0042972F and ecx, 0xfffffffe
00429732 add ecx, 3
00429735 mov edx, esi
00429737 mov dword ptr [esp + 0x1c], ecx
0042973B sub edx, eax
0042973D lea ecx, [eax + esi]
00429740 test edx, edx
00429742 jle 0x429751
00429744 xor edx, edx
00429746 test ecx, ecx
00429748 setle dl
0042974B dec edx
0042974C and edx, 2
0042974F jmp 0x42975f
00429751 xor edx, edx
00429753 test ecx, ecx
00429755 setle dl
00429758 dec edx
00429759 and edx, 0xfffffffe
0042975C add edx, 6
0042975F mov dword ptr [esp + 0x20], edx
00429763 cdq 
00429764 mov ecx, eax
00429766 mov eax, esi
00429768 xor ecx, edx
0042976A sub ecx, edx
0042976C cdq 
0042976D xor eax, edx
0042976F sub eax, edx
00429771 cmp eax, ecx
00429773 mov dword ptr [esp + 0x10], eax
00429777 jl 0x42977d
00429779 mov dword ptr [esp + 0x10], ecx
0042977D cmp eax, ecx
0042977F jg 0x429783
00429781 mov eax, ecx
00429783 mov ecx, dword ptr [esp + 0x10]
00429787 mov ebx, dword ptr [esp + 0x58]
0042978B sub eax, ecx
0042978D mov ecx, ebx
0042978F mov dword ptr [esp + 0x14], eax
00429793 call 0x4cafb0
00429798 fst qword ptr [esp + 0x3c]
0042979C fcomp qword ptr [0x79c520]
004297A2 mov eax, dword ptr [ebx + 0x1b4]
004297A8 mov byte ptr [esp + 0x54], 1
004297AD mov dword ptr [esp + 0x30], eax
004297B1 fnstsw ax
004297B3 test ah, 0x41
004297B6 je 0x4297bd
004297B8 mov byte ptr [esp + 0x54], 0
004297BD mov ebp, dword ptr [esp + 0x10]
004297C1 mov dword ptr [esp + 0x18], 0
004297C9 test ebp, ebp
004297CB je 0x4299f1
004297D1 mov edx, dword ptr [esp + 0x50]
004297D5 mov esi, dword ptr [esp + 0x5c]
004297D9 xor cl, cl
004297DB mov eax, dword ptr [edx]
004297DD mov edx, dword ptr [esp + 0x14]
004297E1 test ebp, ebp
004297E3 mov dword ptr [esp + 0x58], eax
004297E7 mov dword ptr [esp + 0x24], edx
004297EB jle 0x4298e2
004297F1 test cl, cl
004297F3 jne 0x4298e2
004297F9 mov ecx, dword ptr [esp + 0x1c]
004297FD and ecx, 7
00429800 mov dx, word ptr [ecx*4 + 0x851a70]
00429808 lea ecx, [ecx*4 + 0x851a70]
0042980F add dx, ax
00429812 mov ax, word ptr [ecx + 2]
00429816 mov word ptr [esp + 0x28], dx
0042981B add ax, word ptr [esp + 0x5a]
00429820 lea edx, [esp + 0x58]
00429824 push edx
00429825 mov word ptr [esp + 0x2e], ax
0042982A mov ecx, dword ptr [esp + 0x2c]
0042982E mov dword ptr [esp + 0x5c], ecx
00429832 mov ecx, 0x8324e0
00429837 call 0x548070
0042983C mov edi, eax
0042983E mov al, byte ptr [esp + 0x54]
00429842 test al, al
00429844 je 0x429877
00429846 mov eax, dword ptr [esp + 0x30]
0042984A lea ecx, [esp + 0x58]
0042984E push eax
0042984F push ecx
00429850 mov ecx, 0x8324e0
00429855 call 0x54e3a0
0042985A mov dword ptr [esp + 0x38], eax
0042985E fild dword ptr [esp + 0x38]
00429862 fmul qword ptr [esp + 0x3c]
00429866 fcomp qword ptr [0x79c518]
0042986C fnstsw ax
0042986E test ah, 1
00429871 jne 0x429877
00429873 inc dword ptr [esp + 0x18]
00429877 mov eax, dword ptr [esp + 0x1c]
0042987B mov edx, dword ptr [ebx]
0042987D push 1
0042987F push 0
00429881 push esi
00429882 push eax
00429883 push edi
00429884 mov ecx, ebx
00429886 call dword ptr [edx + 0x194]
0042988C test eax, eax
0042988E jne 0x4298b5
00429890 test dword ptr [edi + 0x140], 0x40000
0042989A jne 0x4298b5
0042989C mov eax, dword ptr [esp + 0x18]
004298A0 cmp eax, 3
004298A3 jg 0x4298b5
004298A5 mov cl, byte ptr [esp + 0x60]
004298A9 test cl, cl
004298AB jne 0x4298b1
004298AD test eax, eax
004298AF jg 0x4298b5
004298B1 xor cl, cl
004298B3 jmp 0x4298b7
004298B5 mov cl, 1
004298B7 movsx eax, byte ptr [edi + 0x11b]
004298BE sub esi, eax
004298C0 dec ebp
004298C1 cmp esi, 4
004298C4 jne 0x4298d4
004298C6 mov edx, dword ptr [edi + 0x140]
004298CC lea esi, [eax + 4]
004298CF test dh, 1
004298D2 jne 0x4298d6
004298D4 mov esi, eax
004298D6 mov eax, dword ptr [esp + 0x58]
004298DA test ebp, ebp
004298DC jg 0x4297f1
004298E2 mov edx, dword ptr [esp + 0x14]
004298E6 test edx, edx
004298E8 jle 0x4299e9
004298EE jmp 0x4298f4
004298F0 mov eax, dword ptr [esp + 0x58]
004298F4 test cl, cl
004298F6 jne 0x4299ed
004298FC mov ecx, dword ptr [esp + 0x20]
00429900 and ecx, 7
00429903 mov dx, word ptr [ecx*4 + 0x851a72]
0042990B add ax, word ptr [ecx*4 + 0x851a70]
00429913 add dx, word ptr [esp + 0x5a]
00429918 lea ecx, [ecx*4 + 0x851a70]
0042991F lea ecx, [esp + 0x58]
00429923 mov word ptr [esp + 0x2c], ax
00429928 mov word ptr [esp + 0x2e], dx
0042992D mov eax, dword ptr [esp + 0x2c]
00429931 push ecx
00429932 mov ecx, 0x8324e0
00429937 mov dword ptr [esp + 0x5c], eax
0042993B call 0x548070
00429940 mov edi, eax
00429942 mov al, byte ptr [esp + 0x54]
00429946 test al, al
00429948 je 0x42997b
0042994A mov edx, dword ptr [esp + 0x30]
0042994E lea eax, [esp + 0x58]
00429952 push edx
00429953 push eax
00429954 mov ecx, 0x8324e0
00429959 call 0x54e3a0
0042995E mov dword ptr [esp + 0x38], eax
00429962 fild dword ptr [esp + 0x38]
00429966 fmul qword ptr [esp + 0x3c]
0042996A fcomp qword ptr [0x79c518]
00429970 fnstsw ax
00429972 test ah, 1
00429975 jne 0x42997b
00429977 inc dword ptr [esp + 0x18]
0042997B mov eax, dword ptr [esp + 0x20]
0042997F mov edx, dword ptr [ebx]
00429981 push 1
00429983 push 0
00429985 push esi
00429986 push eax
00429987 push edi
00429988 mov ecx, ebx
0042998A call dword ptr [edx + 0x194]
00429990 test eax, eax
00429992 jne 0x4299b9
00429994 test dword ptr [edi + 0x140], 0x40000
0042999E jne 0x4299b9
004299A0 mov eax, dword ptr [esp + 0x18]
004299A4 cmp eax, 3
004299A7 jg 0x4299b9
004299A9 mov cl, byte ptr [esp + 0x60]
004299AD test cl, cl
004299AF jne 0x4299b5
004299B1 test eax, eax
004299B3 jg 0x4299b9
004299B5 xor cl, cl
004299B7 jmp 0x4299bb
004299B9 mov cl, 1
004299BB dec dword ptr [esp + 0x24]
004299BF movsx eax, byte ptr [edi + 0x11b]
004299C6 sub esi, eax
004299C8 cmp esi, 4
004299CB jne 0x4299db
004299CD mov edx, dword ptr [edi + 0x140]
004299D3 lea esi, [eax + 4]
004299D6 test dh, 1
004299D9 jne 0x4299dd
004299DB mov esi, eax
004299DD mov eax, dword ptr [esp + 0x24]
004299E1 test eax, eax
004299E3 jg 0x4298f0
004299E9 test cl, cl
004299EB je 0x429a2b
004299ED mov ebp, dword ptr [esp + 0x10]
004299F1 mov eax, dword ptr [esp + 0x20]
004299F5 mov ecx, dword ptr [esp + 0x1c]
004299F9 mov dword ptr [esp + 0x1c], eax
004299FD mov eax, dword ptr [esp + 0x14]
00429A01 mov dword ptr [esp + 0x10], eax
00429A05 mov eax, dword ptr [esp + 0x34]
00429A09 inc eax
00429A0A mov dword ptr [esp + 0x20], ecx
00429A0E cmp eax, 2
00429A11 mov dword ptr [esp + 0x14], ebp
00429A15 mov dword ptr [esp + 0x34], eax
00429A19 jl 0x4297bd
00429A1F pop edi
00429A20 pop esi
00429A21 pop ebp
00429A22 xor al, al
00429A24 pop ebx
00429A25 add esp, 0x34
00429A28 ret 0x1c
00429A2B mov ecx, dword ptr [esp + 0x10]
00429A2F mov edx, dword ptr [esp + 0x48]
00429A33 test ecx, ecx
00429A35 jle 0x429a3f
00429A37 mov eax, dword ptr [esp + 0x1c]
00429A3B mov edi, edx
00429A3D rep stosd dword ptr es:[edi], eax
00429A3F mov eax, dword ptr [esp + 0x14]
00429A43 test eax, eax
00429A45 jle 0x429a58
00429A47 mov eax, dword ptr [esp + 0x10]
00429A4B mov ecx, dword ptr [esp + 0x14]
00429A4F lea edi, [edx + eax*4]
00429A52 mov eax, dword ptr [esp + 0x20]
00429A56 rep stosd dword ptr es:[edi], eax
00429A58 mov ecx, dword ptr [esp + 0x4c]
00429A5C mov eax, dword ptr [esp + 0x14]
00429A60 mov esi, dword ptr [esp + 0x10]
00429A64 sub ecx, eax
00429A66 sub ecx, esi
00429A68 test ecx, ecx
00429A6A jle 0x429a78
00429A6C add eax, esi
00429A6E lea edi, [edx + eax*4]
00429A71 mov eax, 0xfffffffe
00429A76 rep stosd dword ptr es:[edi], eax
00429A78 pop edi
00429A79 pop esi
00429A7A pop ebp
00429A7B mov al, 1
00429A7D pop ebx
00429A7E add esp, 0x34
00429A81 ret 0x1c
00429A84 nop 
00429A85 nop 
00429A86 nop 
00429A87 nop 
00429A88 nop 
00429A89 nop 
00429A8A nop 
00429A8B nop 
00429A8C nop 
00429A8D nop 
00429A8E nop 
00429A8F nop 
00429A90 push ebx
00429A91 push esi
00429A92 push edi
00429A93 mov edi, 0x832504
00429A98 lea esi, [ecx + 0x4c]
00429A9B sub edi, ecx
00429A9D mov ebx, 3
00429AA2 mov eax, dword ptr [esi - 0xc]
00429AA5 test eax, eax
00429AA7 je 0x429ab2
00429AA9 push eax
00429AAA call 0x781d3b
00429AAF add esp, 4
00429AB2 mov eax, dword ptr [edi + esi]
00429AB5 shl eax, 2
00429AB8 push eax
00429AB9 call 0x782017
00429ABE mov dword ptr [esi - 0xc], eax
00429AC1 mov ecx, dword ptr [edi + esi]
00429AC4 add esp, 4
00429AC7 dec ecx
00429AC8 js 0x429ada
00429ACA lea eax, [eax + ecx*4]
00429ACD inc ecx
00429ACE mov dword ptr [eax], 0
00429AD4 sub eax, 4
00429AD7 dec ecx
00429AD8 jne 0x429ace
00429ADA mov eax, dword ptr [esi]
00429ADC test eax, eax
00429ADE je 0x429ae9
00429AE0 push eax
00429AE1 call 0x781d3b
00429AE6 add esp, 4
00429AE9 mov ecx, dword ptr [edi + esi]
00429AEC shl ecx, 2
00429AEF push ecx
00429AF0 call 0x782017
00429AF5 mov dword ptr [esi], eax
00429AF7 mov ecx, dword ptr [edi + esi]
00429AFA add esp, 4
00429AFD dec ecx
00429AFE js 0x429b10
00429B00 lea eax, [eax + ecx*4]
00429B03 inc ecx
00429B04 mov dword ptr [eax], 0
00429B0A sub eax, 4
00429B0D dec ecx
00429B0E jne 0x429b04
00429B10 mov eax, dword ptr [esi + 0xc]
00429B13 test eax, eax
00429B15 je 0x429b20
00429B17 push eax
00429B18 call 0x781d3b
00429B1D add esp, 4
00429B20 mov edx, dword ptr [edi + esi]
00429B23 shl edx, 2
00429B26 push edx
00429B27 call 0x782017
00429B2C mov dword ptr [esi + 0xc], eax
00429B2F mov ecx, dword ptr [edi + esi]
00429B32 add esp, 4
00429B35 dec ecx
00429B36 js 0x429b48
00429B38 lea eax, [eax + ecx*4]
00429B3B inc ecx
00429B3C mov dword ptr [eax], 0
00429B42 sub eax, 4
00429B45 dec ecx
00429B46 jne 0x429b3c
00429B48 add esi, 4
00429B4B dec ebx
00429B4C jne 0x429aa2
00429B52 pop edi
00429B53 pop esi
00429B54 pop ebx
00429B55 ret 
00429B56 nop 
00429B57 nop 
00429B58 nop 
00429B59 nop 
00429B5A nop 
00429B5B nop 
00429B5C nop 
00429B5D nop 
00429B5E nop 
00429B5F nop 