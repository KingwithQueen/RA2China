
sub_00427FB0 0x00427FB0 size=554
00427FB0  83 ec 0c                 sub      esp, 0xc
00427FB3  b0 01                    mov      al, 1
00427FB5  53                       push     ebx
00427FB6  55                       push     ebp
00427FB7  56                       push     esi
00427FB8  8b f1                    mov      esi, ecx
00427FBA  33 db                    xor      ebx, ebx
00427FBC  83 c9 ff                 or       ecx, 0xffffffff
00427FBF  57                       push     edi
00427FC0  88 1e                    mov      byte ptr [esi], bl
00427FC2  88 5e 01                 mov      byte ptr [esi + 1], bl
00427FC5  88 5e 02                 mov      byte ptr [esi + 2], bl
00427FC8  88 46 03                 mov      byte ptr [esi + 3], al
00427FCB  c7 46 04 00 00 80 3f     mov      dword ptr [esi + 4], 0x3f800000
00427FD2  88 46 08                 mov      byte ptr [esi + 8], al
00427FD5  89 5e 18                 mov      dword ptr [esi + 0x18], ebx
00427FD8  89 5e 1c                 mov      dword ptr [esi + 0x1c], ebx
00427FDB  89 5e 20                 mov      dword ptr [esi + 0x20], ebx
00427FDE  89 5e 24                 mov      dword ptr [esi + 0x24], ebx
00427FE1  89 4e 28                 mov      dword ptr [esi + 0x28], ecx
00427FE4  89 4e 2c                 mov      dword ptr [esi + 0x2c], ecx
00427FE7  88 46 38                 mov      byte ptr [esi + 0x38], al
00427FEA  89 5e 3c                 mov      dword ptr [esi + 0x3c], ebx
00427FED  89 4e 6c                 mov      dword ptr [esi + 0x6c], ecx
00427FF0  66 89 5e 70              mov      word ptr [esi + 0x70], bx
00427FF4  66 89 5e 72              mov      word ptr [esi + 0x72], bx
00427FF8  8d 7e 74                 lea      edi, [esi + 0x74]
00427FFB  bd 03 00 00 00           mov      ebp, 3
00428000  53                       push     ebx
00428001  53                       push     ebx
00428002  8b cf                    mov      ecx, edi
00428004  e8 07 35 00 00           call     0x42b510
00428009  c7 07 dc c4 79 00        mov      dword ptr [edi], 0x79c4dc
0042800F  c7 47 14 0a 00 00 00     mov      dword ptr [edi + 0x14], 0xa
00428016  89 5f 10                 mov      dword ptr [edi + 0x10], ebx
00428019  83 c7 18                 add      edi, 0x18
0042801C  4d                       dec      ebp
0042801D  75 e1                    jne      0x428000
0042801F  6a 14                    push     0x14
00428021  e8 f1 9f 35 00           call     0x782017
00428026  8b f8                    mov      edi, eax
00428028  83 c4 04                 add      esp, 4
0042802B  3b fb                    cmp      edi, ebx
0042802D  74 3d                    je       0x42806c
0042802F  68 04 00 04 00           push     0x40004
00428034  89 5f 0c                 mov      dword ptr [edi + 0xc], ebx
00428037  c7 47 10 ff ff ff ff     mov      dword ptr [edi + 0x10], 0xffffffff
0042803E  89 1f                    mov      dword ptr [edi], ebx
00428040  c7 47 04 00 00 01 00     mov      dword ptr [edi + 4], 0x10000
00428047  e8 cb 9f 35 00           call     0x782017
0042804C  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
0042804F  89 47 08                 mov      dword ptr [edi + 8], eax
00428052  83 c4 04                 add      esp, 4
00428055  33 c0                    xor      eax, eax
00428057  3b cb                    cmp      ecx, ebx
00428059  7c 13                    jl       0x42806e
0042805B  8b 4f 08                 mov      ecx, dword ptr [edi + 8]
0042805E  40                       inc      eax
0042805F  89 5c 81 fc              mov      dword ptr [ecx + eax*4 - 4], ebx
00428063  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
00428066  3b c1                    cmp      eax, ecx
00428068  7e f1                    jle      0x42805b
0042806A  eb 02                    jmp      0x42806e
0042806C  33 ff                    xor      edi, edi
0042806E  6a 14                    push     0x14
00428070  89 7e 14                 mov      dword ptr [esi + 0x14], edi
00428073  e8 9f 9f 35 00           call     0x782017
00428078  8b f8                    mov      edi, eax
0042807A  83 c4 04                 add      esp, 4
0042807D  3b fb                    cmp      edi, ebx
0042807F  74 3d                    je       0x4280be
00428081  68 44 9c 00 00           push     0x9c44
00428086  89 5f 0c                 mov      dword ptr [edi + 0xc], ebx
00428089  c7 47 10 ff ff ff ff     mov      dword ptr [edi + 0x10], 0xffffffff
00428090  89 1f                    mov      dword ptr [edi], ebx
00428092  c7 47 04 10 27 00 00     mov      dword ptr [edi + 4], 0x2710
00428099  e8 79 9f 35 00           call     0x782017
0042809E  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
004280A1  89 47 08                 mov      dword ptr [edi + 8], eax
004280A4  83 c4 04                 add      esp, 4
004280A7  33 c0                    xor      eax, eax
004280A9  3b cb                    cmp      ecx, ebx
004280AB  7c 13                    jl       0x4280c0
004280AD  8b 57 08                 mov      edx, dword ptr [edi + 8]
004280B0  40                       inc      eax
004280B1  89 5c 82 fc              mov      dword ptr [edx + eax*4 - 4], ebx
004280B5  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
004280B8  3b c1                    cmp      eax, ecx
004280BA  7e f1                    jle      0x4280ad
004280BC  eb 02                    jmp      0x4280c0
004280BE  33 ff                    xor      edi, edi
004280C0  68 04 00 10 00           push     0x100004
004280C5  89 7e 68                 mov      dword ptr [esi + 0x68], edi
004280C8  e8 4a 9f 35 00           call     0x782017
004280CD  83 c4 04                 add      esp, 4
004280D0  3b c3                    cmp      eax, ebx
004280D2  74 1e                    je       0x4280f2
004280D4  8d 48 08                 lea      ecx, [eax + 8]
004280D7  ba 00 00 01 00           mov      edx, 0x10000
004280DC  89 59 04                 mov      dword ptr [ecx + 4], ebx
004280DF  89 19                    mov      dword ptr [ecx], ebx
004280E1  89 59 fc                 mov      dword ptr [ecx - 4], ebx
004280E4  83 c1 10                 add      ecx, 0x10
004280E7  4a                       dec      edx
004280E8  75 f2                    jne      0x4280dc
004280EA  89 98 00 00 10 00        mov      dword ptr [eax + 0x100000], ebx
004280F0  eb 02                    jmp      0x4280f4
004280F2  33 c0                    xor      eax, eax
004280F4  68 04 00 18 00           push     0x180004
004280F9  89 46 10                 mov      dword ptr [esi + 0x10], eax
004280FC  e8 16 9f 35 00           call     0x782017
00428101  83 c4 04                 add      esp, 4
00428104  3b c3                    cmp      eax, ebx
00428106  74 08                    je       0x428110
00428108  89 98 00 00 18 00        mov      dword ptr [eax + 0x180000], ebx
0042810E  eb 02                    jmp      0x428112
00428110  33 c0                    xor      eax, eax
00428112  89 46 0c                 mov      dword ptr [esi + 0xc], eax
00428115  89 98 00 00 18 00        mov      dword ptr [eax + 0x180000], ebx
0042811B  8b 46 10                 mov      eax, dword ptr [esi + 0x10]
0042811E  33 c9                    xor      ecx, ecx
00428120  89 98 00 00 10 00        mov      dword ptr [eax + 0x100000], ebx
00428126  8b 46 14                 mov      eax, dword ptr [esi + 0x14]
00428129  39 18                    cmp      dword ptr [eax], ebx
0042812B  7c 0e                    jl       0x42813b
0042812D  8b 50 08                 mov      edx, dword ptr [eax + 8]
00428130  41                       inc      ecx
00428131  89 5c 8a fc              mov      dword ptr [edx + ecx*4 - 4], ebx
00428135  8b 10                    mov      edx, dword ptr [eax]
00428137  3b ca                    cmp      ecx, edx
00428139  7e f2                    jle      0x42812d
0042813B  89 18                    mov      dword ptr [eax], ebx
0042813D  8b 46 68                 mov      eax, dword ptr [esi + 0x68]
00428140  33 c9                    xor      ecx, ecx
00428142  39 18                    cmp      dword ptr [eax], ebx
00428144  7c 0e                    jl       0x428154
00428146  8b 50 08                 mov      edx, dword ptr [eax + 8]
00428149  41                       inc      ecx
0042814A  89 5c 8a fc              mov      dword ptr [edx + ecx*4 - 4], ebx
0042814E  8b 10                    mov      edx, dword ptr [eax]
00428150  3b ca                    cmp      ecx, edx
00428152  7e f2                    jle      0x428146
00428154  89 18                    mov      dword ptr [eax], ebx
00428156  8d 86 bc 00 00 00        lea      eax, [esi + 0xbc]
0042815C  8d 4e 74                 lea      ecx, [esi + 0x74]
0042815F  89 44 24 14              mov      dword ptr [esp + 0x14], eax
00428163  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
00428167  8d 6e 4c                 lea      ebp, [esi + 0x4c]
0042816A  c7 44 24 18 03 00 00 00  mov      dword ptr [esp + 0x18], 3
00428172  eb 04                    jmp      0x428178
00428174  8b 4c 24 10              mov      ecx, dword ptr [esp + 0x10]
00428178  89 5d f4                 mov      dword ptr [ebp - 0xc], ebx
0042817B  89 5d 00                 mov      dword ptr [ebp], ebx
0042817E  89 5d 0c                 mov      dword ptr [ebp + 0xc], ebx
00428181  8b 11                    mov      edx, dword ptr [ecx]
00428183  ff 52 0c                 call     dword ptr [edx + 0xc]
00428186  8b 7c 24 14              mov      edi, dword ptr [esp + 0x14]
0042818A  8b 54 24 10              mov      edx, dword ptr [esp + 0x10]
0042818E  b9 fa 00 00 00           mov      ecx, 0xfa
00428193  33 c0                    xor      eax, eax
00428195  f3 ab                    rep stosd dword ptr es:[edi], eax
00428197  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
0042819B  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
0042819F  89 9d 28 0c 00 00        mov      dword ptr [ebp + 0xc28], ebx
004281A5  83 c5 04                 add      ebp, 4
004281A8  83 c2 18                 add      edx, 0x18
004281AB  81 c1 e8 03 00 00        add      ecx, 0x3e8
004281B1  48                       dec      eax
004281B2  89 54 24 10              mov      dword ptr [esp + 0x10], edx
004281B6  89 4c 24 14              mov      dword ptr [esp + 0x14], ecx
004281BA  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004281BE  75 b4                    jne      0x428174
004281C0  68 00 71 02 00           push     0x27100
004281C5  e8 4d 9e 35 00           call     0x782017
004281CA  83 c4 04                 add      esp, 4
004281CD  89 46 64                 mov      dword ptr [esi + 0x64], eax
004281D0  8b c6                    mov      eax, esi
004281D2  5f                       pop      edi
004281D3  5e                       pop      esi
004281D4  5d                       pop      ebp
004281D5  5b                       pop      ebx
004281D6  83 c4 0c                 add      esp, 0xc
004281D9  c3                       ret      
