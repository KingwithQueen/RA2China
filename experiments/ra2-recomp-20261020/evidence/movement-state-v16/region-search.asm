00429B60 push ebp
00429B61 mov ebp, esp
00429B63 and esp, 0xfffffff8
00429B66 sub esp, 0x5c
00429B69 mov eax, dword ptr [ebp + 0x10]
00429B6C push ebx
00429B6D push esi
00429B6E mov esi, dword ptr [ebp + 0x14]
00429B71 shl eax, 5
00429B74 push edi
00429B75 mov edi, ecx
00429B77 add eax, 0x7e00c4
00429B7C mov dword ptr [esp + 0x1c], edi
00429B80 test esi, esi
00429B82 mov dword ptr [esp + 0x58], eax
00429B86 je 0x429b9f
00429B88 mov ecx, esi
00429B8A call 0x4cafb0
00429B8F mov eax, dword ptr [esi + 0x1b4]
00429B95 fst qword ptr [esp + 0x60]
00429B99 mov dword ptr [esp + 0x40], eax
00429B9D jmp 0x429bb9
00429B9F mov dword ptr [esp + 0x60], 0
00429BA7 mov dword ptr [esp + 0x64], 0
00429BAF mov dword ptr [esp + 0x40], 0
00429BB7 jmp 0x429bcb
00429BB9 fcomp qword ptr [0x79c520]
00429BBF mov byte ptr [esp + 0x10], 1
00429BC4 fnstsw ax
00429BC6 test ah, 0x41
00429BC9 je 0x429bd0
00429BCB mov byte ptr [esp + 0x10], 0
00429BD0 mov esi, 2
00429BD5 mov dword ptr [esp + 0x38], esi
00429BD9 mov eax, dword ptr [edi + 0x68]
00429BDC xor ecx, ecx
00429BDE cmp dword ptr [eax], 0
00429BE1 jl 0x429bf5
00429BE3 mov edx, dword ptr [eax + 8]
00429BE6 inc ecx
00429BE7 mov dword ptr [edx + ecx*4 - 4], 0
00429BEF mov edx, dword ptr [eax]
00429BF1 cmp ecx, edx
00429BF3 jle 0x429be3
00429BF5 mov dword ptr [eax], 0
00429BFB mov eax, dword ptr [ebp + 8]
00429BFE push eax
00429BFF mov ecx, 0x8324e0
00429C04 call 0x54fab0
00429C09 mov edx, dword ptr [0x83254c]
00429C0F lea ecx, [eax + eax*4]
00429C12 lea eax, [edx + ecx*2]
00429C15 mov ecx, 0x8324e0
00429C1A movsx ebx, word ptr [eax + esi*2]
00429C1E mov eax, dword ptr [ebp + 0xc]
00429C21 mov dword ptr [esp + 0x34], ebx
00429C25 push eax
00429C26 call 0x54fab0
00429C2B mov edx, dword ptr [0x83254c]
00429C31 lea ecx, [eax + eax*4]
00429C34 cmp esi, 2
00429C37 lea eax, [edx + ecx*2]
00429C3A movsx eax, word ptr [eax + esi*2]
00429C3E mov dword ptr [esp + 0x3c], eax
00429C42 sete al
00429C45 test al, al
00429C47 mov byte ptr [esp + 0x12], al
00429C4B jne 0x429c57
00429C4D mov ecx, dword ptr [edi + esi*4 + 0x44]
00429C51 mov dword ptr [esp + 0x44], ecx
00429C55 jmp 0x429c5f
00429C57 mov dword ptr [esp + 0x44], 0
00429C5F mov edx, dword ptr [edi + esi*4 + 0x4c]
00429C63 mov eax, dword ptr [edi + esi*4 + 0x40]
00429C67 mov ecx, dword ptr [edi + esi*4 + 0x58]
00429C6B mov dword ptr [esp + 0x24], edx
00429C6F mov edx, dword ptr [edi + 0x28]
00429C72 mov dword ptr [esp + 0x28], ecx
00429C76 mov ecx, dword ptr [esp + 0x3c]
00429C7A mov dword ptr [eax + ebx*4], edx
00429C7D mov edx, dword ptr [edi + 0x28]
00429C80 cmp ebx, ecx
00429C82 mov dword ptr [esp + 0x5c], eax
00429C86 mov dword ptr [eax + ecx*4], edx
00429C89 jne 0x429cb9
00429C8B test esi, esi
00429C8D jne 0x429c98
00429C8F mov eax, dword ptr [edi + 0x64]
00429C92 mov dword ptr [eax + 0xc], esi
00429C95 mov dword ptr [eax + 4], ebx
00429C98 lea eax, [esi + esi*4]
00429C9B lea eax, [eax + eax*4]
00429C9E lea eax, [eax + eax*4]
00429CA1 mov word ptr [edi + eax*8 + 0xbc], bx
00429CA9 mov dword ptr [edi + esi*4 + 0xc74], 1
00429CB4 jmp 0x42a1a6
00429CB9 mov eax, dword ptr [edi + 0x64]
00429CBC xor ecx, ecx
00429CBE mov dword ptr [esp + 0x4c], eax
00429CC2 mov dword ptr [eax], 0xffffffff
00429CC8 mov dword ptr [eax + 4], ebx
00429CCB mov dword ptr [eax + 8], ecx
00429CCE mov dword ptr [eax + 0xc], ecx
00429CD1 mov eax, dword ptr [edi + 0x68]
00429CD4 mov dword ptr [esp + 0x20], eax
00429CD8 mov ecx, dword ptr [eax]
00429CDA inc ecx
00429CDB mov edx, ecx
00429CDD shr edx, 1
00429CDF cmp ecx, dword ptr [eax + 4]
00429CE2 jae 0x429d47
00429CE4 cmp ecx, 1
00429CE7 jbe 0x429d1e
00429CE9 mov eax, dword ptr [esp + 0x20]
00429CED mov eax, dword ptr [eax + 8]
00429CF0 mov dword ptr [esp + 0x50], eax
00429CF4 mov eax, dword ptr [eax + edx*4]
00429CF7 fld dword ptr [eax + 8]
00429CFA fcomp dword ptr [0x79a738]
00429D00 fnstsw ax
00429D02 test ah, 0x41
00429D05 jne 0x429d1e
00429D07 mov eax, dword ptr [esp + 0x50]
00429D0B mov ebx, dword ptr [eax + edx*4]
00429D0E mov dword ptr [eax + ecx*4], ebx
00429D11 mov ebx, dword ptr [esp + 0x34]
00429D15 mov ecx, edx
00429D17 shr edx, 1
00429D19 cmp ecx, 1
00429D1C ja 0x429ce9
00429D1E mov edx, dword ptr [esp + 0x20]
00429D22 mov eax, dword ptr [edx + 8]
00429D25 mov edx, dword ptr [esp + 0x4c]
00429D29 mov dword ptr [eax + ecx*4], edx
00429D2C mov eax, dword ptr [esp + 0x20]
00429D30 mov ecx, dword ptr [eax]
00429D32 inc ecx
00429D33 mov dword ptr [eax], ecx
00429D35 mov ecx, dword ptr [eax + 0xc]
00429D38 cmp edx, ecx
00429D3A jbe 0x429d3f
00429D3C mov dword ptr [eax + 0xc], edx
00429D3F cmp edx, dword ptr [eax + 0x10]
00429D42 jae 0x429d47
00429D44 mov dword ptr [eax + 0x10], edx
00429D47 mov edx, dword ptr [esp + 0x24]
00429D4B mov ecx, dword ptr [edi + 0x28]
00429D4E mov eax, dword ptr [esp + 0x28]
00429D52 mov dword ptr [esp + 0x2c], 1
00429D5A mov dword ptr [edx + ebx*4], ecx
00429D5D mov dword ptr [eax + ebx*4], 0
00429D64 mov ecx, dword ptr [edi + 0x68]
00429D67 mov edx, dword ptr [ecx]
00429D69 test edx, edx
00429D6B jne 0x429d71
00429D6D xor eax, eax
00429D6F jmp 0x429d97
00429D71 mov eax, dword ptr [ecx + 8]
00429D74 push 1
00429D76 mov edx, dword ptr [eax + edx*4]
00429D79 mov ebx, dword ptr [eax + 4]
00429D7C mov dword ptr [eax + 4], edx
00429D7F mov eax, dword ptr [ecx]
00429D81 mov edx, dword ptr [ecx + 8]
00429D84 mov dword ptr [edx + eax*4], 0
00429D8B mov edx, dword ptr [ecx]
00429D8D dec edx
00429D8E mov dword ptr [ecx], edx
00429D90 call 0x42b560
00429D95 mov eax, ebx
00429D97 lea edx, [esi + esi*2]
00429D9A mov dword ptr [esp + 0x14], eax
00429D9E shl edx, 3
00429DA1 mov dword ptr [esp + 0x20], edx
00429DA5 mov ebx, dword ptr [edx + edi + 0x84]
00429DAC test ebx, ebx
00429DAE sete byte ptr [esp + 0x13]
00429DB3 test eax, eax
00429DB5 je 0x42a1b2
00429DBB mov ecx, dword ptr [eax + 4]
00429DBE mov ebx, dword ptr [esp + 0x3c]
00429DC2 cmp ecx, ebx
00429DC4 mov dword ptr [esp + 0x48], ecx
00429DC8 je 0x42a122
00429DCE lea eax, [ecx + ecx*8]
00429DD1 mov ecx, dword ptr [edx + 0x83256c]
00429DD7 mov edx, dword ptr [ecx + eax*4 + 4]
00429DDB lea eax, [ecx + eax*4]
00429DDE mov ecx, dword ptr [eax + 0x10]
00429DE1 test ecx, ecx
00429DE3 jle 0x42a010
00429DE9 mov eax, dword ptr [esp + 0x2c]
00429DED mov dword ptr [esp + 0x34], edx
00429DF1 shl eax, 4
00429DF4 mov dword ptr [esp + 0x30], eax
00429DF8 mov dword ptr [esp + 0x50], ecx
00429DFC mov eax, dword ptr [esp + 0x34]
00429E00 mov ecx, dword ptr [esp + 0x20]
00429E04 xor esi, esi
00429E06 mov dword ptr [esp + 0x18], 0
00429E0E mov ebx, dword ptr [eax]
00429E10 mov dl, byte ptr [eax + 4]
00429E13 mov byte ptr [esp + 0x11], dl
00429E17 mov edx, dword ptr [ecx + 0x83256c]
00429E1D lea eax, [ebx + ebx*8]
00429E20 mov dword ptr [esp + 0x4c], ebx
00429E24 mov si, word ptr [edx + eax*4 + 0x18]
00429E29 lea eax, [edx + eax*4]
00429E2C mov edx, dword ptr [eax + 0x1c]
00429E2F mov al, byte ptr [esp + 0x10]
00429E33 test al, al
00429E35 mov dword ptr [esp + 0x54], edx
00429E39 je 0x429e6e
00429E3B mov eax, dword ptr [esp + 0x48]
00429E3F mov ecx, dword ptr [esp + 0x38]
00429E43 mov edx, dword ptr [esp + 0x40]
00429E47 push ebx
00429E48 push eax
00429E49 push ecx
00429E4A push edx
00429E4B mov ecx, 0x8324e0
00429E50 call 0x567d20
00429E55 mov dword ptr [esp + 0x18], eax
00429E59 fild dword ptr [esp + 0x18]
00429E5D fmul qword ptr [esp + 0x60]
00429E61 call 0x77f110
00429E66 mov edx, dword ptr [esp + 0x54]
00429E6A mov dword ptr [esp + 0x18], eax
00429E6E mov al, byte ptr [esp + 0x11]
00429E72 test al, al
00429E74 je 0x429e7e
00429E76 fld qword ptr [0x79c528]
00429E7C jmp 0x429e84
00429E7E fld qword ptr [0x79b610]
00429E84 mov eax, dword ptr [esp + 0x14]
00429E88 mov ecx, dword ptr [edi + 0x28]
00429E8B fld dword ptr [edx*4 + 0x79c4a4]
00429E92 fadd dword ptr [eax + 8]
00429E95 mov eax, dword ptr [esp + 0x24]
00429E99 fiadd dword ptr [esp + 0x18]
00429E9D cmp dword ptr [eax + ebx*4], ecx
00429EA0 fadd st(1)
00429EA2 fstp dword ptr [esp + 0x18]
00429EA6 fstp st(0)
00429EA8 jne 0x429ec0
00429EAA mov eax, dword ptr [esp + 0x28]
00429EAE fld dword ptr [eax + ebx*4]
00429EB1 fcomp dword ptr [esp + 0x18]
00429EB5 fnstsw ax
00429EB7 test ah, 0x41
00429EBA jne 0x429ff6
00429EC0 mov al, byte ptr [esp + 0x12]
00429EC4 test al, al
00429EC6 jne 0x429eda
00429EC8 mov eax, dword ptr [esp + 0x44]
00429ECC cmp dword ptr [eax + esi*4], ecx
00429ECF je 0x429eda
00429ED1 cmp edx, 1
00429ED4 jne 0x429ff6
00429EDA mov ecx, dword ptr [esp + 0x58]
00429EDE cmp dword ptr [ecx + edx*4], 1
00429EE2 jne 0x429ff6
00429EE8 mov al, byte ptr [esp + 0x13]
00429EEC test al, al
00429EEE jne 0x429f36
00429EF0 mov edx, dword ptr [esp + 0x48]
00429EF4 mov ecx, ebx
00429EF6 cmp bx, dx
00429EF9 mov eax, edx
00429EFB jae 0x429f01
00429EFD mov eax, ebx
00429EFF mov ecx, edx
00429F01 mov edx, dword ptr [esp + 0x20]
00429F05 and eax, 0xffff
00429F0A shl eax, 0x10
00429F0D and ecx, 0xffff
00429F13 or eax, ecx
00429F15 mov ecx, dword ptr [edx + edi + 0x84]
00429F1C dec ecx
00429F1D js 0x429f36
00429F1F mov edx, dword ptr [edx + edi + 0x78]
00429F23 lea edx, [edx + ecx*4]
00429F26 cmp dword ptr [edx], eax
00429F28 je 0x429ff6
00429F2E dec ecx
00429F2F sub edx, 4
00429F32 test ecx, ecx
00429F34 jge 0x429f26
00429F36 mov edx, dword ptr [esp + 0x1c]
00429F3A mov ecx, dword ptr [esp + 0x30]
00429F3E mov eax, dword ptr [edx + 0x64]
00429F41 mov dword ptr [eax + ecx + 4], ebx
00429F45 lea esi, [eax + ecx]
00429F48 mov ecx, dword ptr [esp + 0x14]
00429F4C mov edi, ecx
00429F4E sub edi, eax
00429F50 mov eax, dword ptr [esp + 0x18]
00429F54 sar edi, 4
00429F57 mov dword ptr [esi], edi
00429F59 mov dword ptr [esi + 8], eax
00429F5C mov ecx, dword ptr [ecx + 0xc]
00429F5F inc ecx
00429F60 mov dword ptr [esi + 0xc], ecx
00429F63 mov edi, dword ptr [edx + 0x68]
00429F66 mov ecx, dword ptr [edi]
00429F68 mov eax, dword ptr [edi + 4]
00429F6B inc ecx
00429F6C mov edx, ecx
00429F6E shr edx, 1
00429F70 cmp ecx, eax
00429F72 jae 0x429fc5
00429F74 cmp ecx, 1
00429F77 jbe 0x429fa8
00429F79 mov eax, dword ptr [edi + 8]
00429F7C mov eax, dword ptr [eax + edx*4]
00429F7F mov dword ptr [esp + 0x54], eax
00429F83 fld dword ptr [eax + 8]
00429F86 fcomp dword ptr [esp + 0x18]
00429F8A fnstsw ax
00429F8C test ah, 0x41
00429F8F jne 0x429fa8
00429F91 mov eax, dword ptr [edi + 8]
00429F94 mov ebx, dword ptr [esp + 0x54]
00429F98 mov dword ptr [eax + ecx*4], ebx
00429F9B mov ebx, dword ptr [esp + 0x4c]
00429F9F mov ecx, edx
00429FA1 shr edx, 1
00429FA3 cmp ecx, 1
00429FA6 ja 0x429f79
00429FA8 mov edx, dword ptr [edi + 8]
00429FAB mov dword ptr [edx + ecx*4], esi
00429FAE mov ecx, dword ptr [edi]
00429FB0 mov eax, dword ptr [edi + 0xc]
00429FB3 inc ecx
00429FB4 cmp esi, eax
00429FB6 mov dword ptr [edi], ecx
00429FB8 jbe 0x429fbd
00429FBA mov dword ptr [edi + 0xc], esi
00429FBD cmp esi, dword ptr [edi + 0x10]
00429FC0 jae 0x429fc5
00429FC2 mov dword ptr [edi + 0x10], esi
00429FC5 mov eax, dword ptr [esp + 0x1c]
00429FC9 mov edx, dword ptr [esp + 0x24]
00429FCD fld dword ptr [esp + 0x18]
00429FD1 mov ecx, dword ptr [eax + 0x28]
00429FD4 mov eax, dword ptr [esp + 0x28]
00429FD8 mov edi, dword ptr [esp + 0x1c]
00429FDC mov dword ptr [edx + ebx*4], ecx
00429FDF fstp dword ptr [eax + ebx*4]
00429FE2 mov ecx, dword ptr [esp + 0x2c]
00429FE6 mov eax, dword ptr [esp + 0x30]
00429FEA inc ecx
00429FEB add eax, 0x10
00429FEE mov dword ptr [esp + 0x2c], ecx
00429FF2 mov dword ptr [esp + 0x30], eax
00429FF6 mov ecx, dword ptr [esp + 0x34]
00429FFA mov eax, dword ptr [esp + 0x50]
00429FFE add ecx, 8
0042A001 dec eax
0042A002 mov dword ptr [esp + 0x34], ecx
0042A006 mov dword ptr [esp + 0x50], eax
0042A00A jne 0x429dfc
0042A010 mov ecx, dword ptr [edi + 0x68]
0042A013 mov edx, dword ptr [ecx]
0042A015 test edx, edx
0042A017 je 0x42a1b2
0042A01D mov eax, dword ptr [ecx + 8]
0042A020 mov ebx, 1
0042A025 mov edx, dword ptr [eax + edx*4]
0042A028 mov esi, dword ptr [eax + 4]
0042A02B mov dword ptr [eax + 4], edx
0042A02E mov eax, dword ptr [ecx]
0042A030 mov edx, dword ptr [ecx + 8]
0042A033 mov dword ptr [esp + 0x54], esi
0042A037 mov dword ptr [edx + eax*4], 0
0042A03E mov edx, dword ptr [ecx]
0042A040 dec edx
0042A041 mov esi, edx
0042A043 mov dword ptr [ecx], edx
0042A045 cmp esi, 2
0042A048 jl 0x42a067
0042A04A mov eax, dword ptr [ecx + 8]
0042A04D mov edx, dword ptr [eax + 8]
0042A050 mov eax, dword ptr [eax + 4]
0042A053 fld dword ptr [edx + 8]
0042A056 fld dword ptr [eax + 8]
0042A059 fcompp 
0042A05B mov edx, 2
0042A060 fnstsw ax
0042A062 test ah, 0x41
0042A065 je 0x42a06c
0042A067 mov edx, 1
0042A06C cmp esi, 3
0042A06F jl 0x42a090
0042A071 mov eax, dword ptr [ecx + 8]
0042A074 mov esi, dword ptr [eax + 0xc]
0042A077 mov eax, dword ptr [eax + edx*4]
0042A07A fld dword ptr [esi + 8]
0042A07D fld dword ptr [eax + 8]
0042A080 fcompp 
0042A082 fnstsw ax
0042A084 test ah, 0x41
0042A087 jne 0x42a090
0042A089 mov edx, 3
0042A08E jmp 0x42a095
0042A090 cmp edx, 1
0042A093 je 0x42a105
0042A095 mov eax, dword ptr [ecx + 8]
0042A098 mov edi, dword ptr [eax + edx*4]
0042A09B mov esi, dword ptr [eax + ebx*4]
0042A09E mov dword ptr [eax + ebx*4], edi
0042A0A1 mov eax, dword ptr [ecx + 8]
0042A0A4 mov ebx, edx
0042A0A6 mov dword ptr [eax + edx*4], esi
0042A0A9 mov edi, dword ptr [ecx]
0042A0AB lea esi, [edx + edx]
0042A0AE lea eax, [edx + edx + 1]
0042A0B2 cmp esi, edi
0042A0B4 mov dword ptr [esp + 0x34], eax
0042A0B8 jg 0x42a0d7
0042A0BA mov eax, dword ptr [ecx + 8]
0042A0BD mov eax, dword ptr [eax + esi*4]
0042A0C0 fld dword ptr [eax + 8]
0042A0C3 mov eax, dword ptr [ecx + 8]
0042A0C6 mov eax, dword ptr [eax + edx*4]
0042A0C9 fld dword ptr [eax + 8]
0042A0CC fcompp 
0042A0CE fnstsw ax
0042A0D0 test ah, 0x41
0042A0D3 jne 0x42a0d7
0042A0D5 mov edx, esi
0042A0D7 cmp dword ptr [esp + 0x34], edi
0042A0DB jg 0x42a0fd
0042A0DD mov eax, dword ptr [ecx + 8]
0042A0E0 mov esi, dword ptr [esp + 0x34]
0042A0E4 mov esi, dword ptr [eax + esi*4]
0042A0E7 mov eax, dword ptr [eax + edx*4]
0042A0EA fld dword ptr [esi + 8]
0042A0ED fld dword ptr [eax + 8]
0042A0F0 fcompp 
0042A0F2 fnstsw ax
0042A0F4 test ah, 0x41
0042A0F7 jne 0x42a0fd
0042A0F9 mov edx, dword ptr [esp + 0x34]
0042A0FD cmp edx, ebx
0042A0FF jne 0x42a095
0042A101 mov edi, dword ptr [esp + 0x1c]
0042A105 mov eax, dword ptr [esp + 0x54]
0042A109 test eax, eax
0042A10B mov dword ptr [esp + 0x14], eax
0042A10F je 0x42a1b2
0042A115 mov esi, dword ptr [esp + 0x38]
0042A119 mov edx, dword ptr [esp + 0x20]
0042A11D jmp 0x429dbb
0042A122 test eax, eax
0042A124 je 0x42a1b2
0042A12A mov edx, dword ptr [eax]
0042A12C mov ecx, eax
0042A12E cmp edx, -1
0042A131 mov dword ptr [esp + 0x54], ecx
0042A135 je 0x42a157
0042A137 mov ecx, dword ptr [eax + 4]
0042A13A mov ebx, dword ptr [esp + 0x5c]
0042A13E mov edx, dword ptr [edi + 0x28]
0042A141 mov dword ptr [ebx + ecx*4], edx
0042A144 mov eax, dword ptr [eax]
0042A146 mov edx, dword ptr [edi + 0x64]
0042A149 shl eax, 4
0042A14C add eax, edx
0042A14E cmp dword ptr [eax], -1
0042A151 jne 0x42a137
0042A153 mov ecx, dword ptr [esp + 0x54]
0042A157 mov eax, dword ptr [ecx + 0xc]
0042A15A inc eax
0042A15B mov dword ptr [edi + esi*4 + 0xc74], eax
0042A162 dec eax
0042A163 test eax, eax
0042A165 jle 0x42a191
0042A167 lea edx, [esi + esi*4]
0042A16A lea edx, [edx + edx*4]
0042A16D lea edx, [edx + edx*4]
0042A170 lea edx, [eax + edx*4]
0042A173 lea edx, [edi + edx*2 + 0xbc]
0042A17A mov bx, word ptr [ecx + 4]
0042A17E mov word ptr [edx], bx
0042A181 mov ecx, dword ptr [ecx]
0042A183 mov ebx, dword ptr [edi + 0x64]
0042A186 sub edx, 2
0042A189 shl ecx, 4
0042A18C add ecx, ebx
0042A18E dec eax
0042A18F jne 0x42a17a
0042A191 mov cx, word ptr [ecx + 4]
0042A195 lea eax, [esi + esi*4]
0042A198 lea eax, [eax + eax*4]
0042A19B lea eax, [eax + eax*4]
0042A19E mov word ptr [edi + eax*8 + 0xbc], cx
0042A1A6 dec esi
0042A1A7 mov dword ptr [esp + 0x38], esi
0042A1AB js 0x42a1bd
0042A1AD jmp 0x429bd9
0042A1B2 xor al, al
0042A1B4 pop edi
0042A1B5 pop esi
0042A1B6 pop ebx
0042A1B7 mov esp, ebp
0042A1B9 pop ebp
0042A1BA ret 0x10
0042A1BD pop edi
0042A1BE pop esi
0042A1BF mov al, 1
0042A1C1 pop ebx
0042A1C2 mov esp, ebp
0042A1C4 pop ebp
0042A1C5 ret 0x10