
sub_004C9B10 0x004C9B10 size=176
004C9B10  83 ec 0c                 sub      esp, 0xc
004C9B13  56                       push     esi
004C9B14  8b f1                    mov      esi, ecx
004C9B16  57                       push     edi
004C9B17  8b 06                    mov      eax, dword ptr [esi]
004C9B19  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004C9B1F  8b 8e b4 01 00 00        mov      ecx, dword ptr [esi + 0x1b4]
004C9B25  50                       push     eax
004C9B26  e8 f5 be 02 00           call     0x4f5a20
004C9B2B  8b 16                    mov      edx, dword ptr [esi]
004C9B2D  8b ce                    mov      ecx, esi
004C9B2F  dd 5c 24 0c              fstp     qword ptr [esp + 0xc]
004C9B33  ff 92 38 03 00 00        call     dword ptr [edx + 0x338]
004C9B39  89 44 24 08              mov      dword ptr [esp + 8], eax
004C9B3D  db 44 24 08              fild     dword ptr [esp + 8]
004C9B41  dc 4c 24 0c              fmul     qword ptr [esp + 0xc]
004C9B45  dc 8e 70 04 00 00        fmul     qword ptr [esi + 0x470]
004C9B4B  e8 c0 55 2b 00           call     0x77f110
004C9B50  6a 00                    push     0
004C9B52  8b ce                    mov      ecx, esi
004C9B54  89 44 24 0c              mov      dword ptr [esp + 0xc], eax
004C9B58  e8 b3 dd 20 00           call     0x6d7910
004C9B5D  84 c0                    test     al, al
004C9B5F  74 18                    je       0x4c9b79
004C9B61  db 44 24 08              fild     dword ptr [esp + 8]
004C9B65  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004C9B6A  dc 88 98 05 00 00        fmul     qword ptr [eax + 0x598]
004C9B70  e8 9b 55 2b 00           call     0x77f110
004C9B75  89 44 24 08              mov      dword ptr [esp + 8], eax
004C9B79  db 44 24 08              fild     dword ptr [esp + 8]
004C9B7D  dc 8e 68 04 00 00        fmul     qword ptr [esi + 0x468]
004C9B83  e8 88 55 2b 00           call     0x77f110
004C9B88  8b 16                    mov      edx, dword ptr [esi]
004C9B8A  8b ce                    mov      ecx, esi
004C9B8C  8b f8                    mov      edi, eax
004C9B8E  ff 52 2c                 call     dword ptr [edx + 0x2c]
004C9B91  83 f8 01                 cmp      eax, 1
004C9B94  75 18                    jne      0x4c9bae
004C9B96  8b 86 b4 05 00 00        mov      eax, dword ptr [esi + 0x5b4]
004C9B9C  83 f8 ff                 cmp      eax, -1
004C9B9F  8b c7                    mov      eax, edi
004C9BA1  74 0d                    je       0x4c9bb0
004C9BA3  99                       cdq      
004C9BA4  2b c2                    sub      eax, edx
004C9BA6  5f                       pop      edi
004C9BA7  d1 f8                    sar      eax, 1
004C9BA9  5e                       pop      esi
004C9BAA  83 c4 0c                 add      esp, 0xc
004C9BAD  c3                       ret      
004C9BAE  8b c7                    mov      eax, edi
004C9BB0  5f                       pop      edi
004C9BB1  5e                       pop      esi
004C9BB2  83 c4 0c                 add      esp, 0xc
004C9BB5  c3                       ret      
004C9BB6  90                       nop      
004C9BB7  90                       nop      
004C9BB8  90                       nop      
004C9BB9  90                       nop      
004C9BBA  90                       nop      
004C9BBB  90                       nop      
004C9BBC  90                       nop      
004C9BBD  90                       nop      
004C9BBE  90                       nop      
004C9BBF  90                       nop      

sub_004A1FDC 0x004A2011 size=176
004A2011  89 5c 24 34              mov      dword ptr [esp + 0x34], ebx
004A2015  db 44 24 34              fild     dword ptr [esp + 0x34]
004A2019  dc 0d d0 05 7a 00        fmul     qword ptr [0x7a05d0]
004A201F  dc 2d 08 a7 79 00        fsubr    qword ptr [0x79a708]
004A2025  dc 0d c8 05 7a 00        fmul     qword ptr [0x7a05c8]
004A202B  e8 e0 d0 2d 00           call     0x77f110
004A2030  8b 5c 24 3c              mov      ebx, dword ptr [esp + 0x3c]
004A2034  c6 87 a0 05 00 00 01     mov      byte ptr [edi + 0x5a0], 1
004A203B  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A203E  03 d8                    add      ebx, eax
004A2040  89 5c 24 3c              mov      dword ptr [esp + 0x3c], ebx
004A2044  c6 81 a1 05 00 00 00     mov      byte ptr [ecx + 0x5a1], 0
004A204B  8b 5d 0c                 mov      ebx, dword ptr [ebp + 0xc]
004A204E  8d 93 88 00 00 00        lea      edx, [ebx + 0x88]
004A2054  8b 83 88 00 00 00        mov      eax, dword ptr [ebx + 0x88]
004A205A  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A205D  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2060  89 54 24 64              mov      dword ptr [esp + 0x64], edx
004A2064  99                       cdq      
004A2065  81 e2 ff 00 00 00        and      edx, 0xff
004A206B  03 c2                    add      eax, edx
004A206D  8b f8                    mov      edi, eax
004A206F  8b c1                    mov      eax, ecx
004A2071  99                       cdq      
004A2072  81 e2 ff 00 00 00        and      edx, 0xff
004A2078  03 c2                    add      eax, edx
004A207A  c1 f8 08                 sar      eax, 8
004A207D  66 89 44 24 36           mov      word ptr [esp + 0x36], ax
004A2082  8b 06                    mov      eax, dword ptr [esi]
004A2084  99                       cdq      
004A2085  81 e2 ff 00 00 00        and      edx, 0xff
004A208B  03 c2                    add      eax, edx
004A208D  8b c8                    mov      ecx, eax
004A208F  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A2092  99                       cdq      
004A2093  81 e2 ff 00 00 00        and      edx, 0xff
004A2099  03 c2                    add      eax, edx
004A209B  c1 ff 08                 sar      edi, 8
004A209E  c1 f9 08                 sar      ecx, 8
004A20A1  c1 f8 08                 sar      eax, 8
004A20A4  66 3b f9                 cmp      di, cx
004A20A7  75 07                    jne      0x4a20b0
004A20A9  66 39 44 24 36           cmp      word ptr [esp + 0x36], ax
004A20AE  74 34                    je       0x4a20e4
004A20B0  8b 03                    mov      eax, dword ptr [ebx]
004A20B2  6a 00                    push     0
004A20B4  8b cb                    mov      ecx, ebx
004A20B6  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004A20BC  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20BF  56                       push     esi

sub_007220C0 0x007220C0 size=176
007220C0  83 ec 0c                 sub      esp, 0xc
007220C3  d9 44 24 14              fld      dword ptr [esp + 0x14]
007220C7  dc 2d 08 a7 79 00        fsubr    qword ptr [0x79a708]
007220CD  53                       push     ebx
007220CE  8b 5c 24 14              mov      ebx, dword ptr [esp + 0x14]
007220D2  55                       push     ebp
007220D3  56                       push     esi
007220D4  db 03                    fild     dword ptr [ebx]
007220D6  8b f2                    mov      esi, edx
007220D8  57                       push     edi
007220D9  8b f9                    mov      edi, ecx
007220DB  d8 4c 24 24              fmul     dword ptr [esp + 0x24]
007220DF  db 06                    fild     dword ptr [esi]
007220E1  d8 ca                    fmul     st(2)
007220E3  de c1                    faddp    st(1)
007220E5  e8 26 d0 05 00           call     0x77f110
007220EA  db 43 04                 fild     dword ptr [ebx + 4]
007220ED  8b e8                    mov      ebp, eax
007220EF  d8 4c 24 24              fmul     dword ptr [esp + 0x24]
007220F3  db 46 04                 fild     dword ptr [esi + 4]
007220F6  d8 ca                    fmul     st(2)
007220F8  de c1                    faddp    st(1)
007220FA  e8 11 d0 05 00           call     0x77f110
007220FF  db 43 08                 fild     dword ptr [ebx + 8]
00722102  89 44 24 14              mov      dword ptr [esp + 0x14], eax
00722106  d8 4c 24 24              fmul     dword ptr [esp + 0x24]
0072210A  db 46 08                 fild     dword ptr [esi + 8]
0072210D  d8 ca                    fmul     st(2)
0072210F  de c1                    faddp    st(1)
00722111  e8 fa cf 05 00           call     0x77f110
00722116  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
0072211A  8b cf                    mov      ecx, edi
0072211C  dd d8                    fstp     st(0)
0072211E  89 29                    mov      dword ptr [ecx], ebp
00722120  89 51 04                 mov      dword ptr [ecx + 4], edx
00722123  89 41 08                 mov      dword ptr [ecx + 8], eax
00722126  8b c7                    mov      eax, edi
00722128  5f                       pop      edi
00722129  5e                       pop      esi
0072212A  5d                       pop      ebp
0072212B  5b                       pop      ebx
0072212C  83 c4 0c                 add      esp, 0xc
0072212F  c2 08 00                 ret      8
00722132  90                       nop      
00722133  90                       nop      
00722134  90                       nop      
00722135  90                       nop      
00722136  90                       nop      
00722137  90                       nop      
00722138  90                       nop      
00722139  90                       nop      
0072213A  90                       nop      
0072213B  90                       nop      
0072213C  90                       nop      
0072213D  90                       nop      
0072213E  90                       nop      
0072213F  90                       nop      
00722140  d9 44 24 08              fld      dword ptr [esp + 8]
00722144  dc 2d 08 a7 79 00        fsubr    qword ptr [0x79a708]
0072214A  53                       push     ebx
0072214B  8b 5c 24 08              mov      ebx, dword ptr [esp + 8]
0072214F  55                       push     ebp
00722150  56                       push     esi
00722151  db 03                    fild     dword ptr [ebx]
00722153  57                       push     edi
00722154  8b fa                    mov      edi, edx
00722156  8b f1                    mov      esi, ecx
00722158  d8 4c 24 18              fmul     dword ptr [esp + 0x18]
0072215C  db 07                    fild     dword ptr [edi]
0072215E  d8 ca                    fmul     st(2)
00722160  de c1                    faddp    st(1)
00722162  e8 a9 cf 05 00           call     0x77f110
00722167  db 43 04                 fild     dword ptr [ebx + 4]
0072216A  8b e8                    mov      ebp, eax
0072216C  d8 4c 24 18              fmul     dword ptr [esp + 0x18]

sub_004A4740 0x004A4740 size=176
004A4740  8b 51 58                 mov      edx, dword ptr [ecx + 0x58]
004A4743  53                       push     ebx
004A4744  55                       push     ebp
004A4745  8b 6c 24 14              mov      ebp, dword ptr [esp + 0x14]
004A4749  8d 14 52                 lea      edx, [edx + edx*2]
004A474C  56                       push     esi
004A474D  8b 45 00                 mov      eax, dword ptr [ebp]
004A4750  57                       push     edi
004A4751  8b 1c 95 88 01 7a 00     mov      ebx, dword ptr [edx*4 + 0x7a0188]
004A4758  8b 54 24 18              mov      edx, dword ptr [esp + 0x18]
004A475C  f6 c3 01                 test     bl, 1
004A475F  8b 3a                    mov      edi, dword ptr [edx]
004A4761  8b 72 04                 mov      esi, dword ptr [edx + 4]
004A4764  74 15                    je       0x4a477b
004A4766  8b d7                    mov      edx, edi
004A4768  8b fe                    mov      edi, esi
004A476A  8b f2                    mov      esi, edx
004A476C  ba c0 ff ff ff           mov      edx, 0xffffffc0
004A4771  2b d0                    sub      edx, eax
004A4773  81 e2 ff 00 00 00        and      edx, 0xff
004A4779  8b c2                    mov      eax, edx
004A477B  f6 c3 02                 test     bl, 2
004A477E  74 09                    je       0x4a4789
004A4780  f7 d8                    neg      eax
004A4782  f7 df                    neg      edi
004A4784  25 ff 00 00 00           and      eax, 0xff
004A4789  f6 c3 04                 test     bl, 4
004A478C  74 11                    je       0x4a479f
004A478E  ba 80 ff ff ff           mov      edx, 0xffffff80
004A4793  2b d0                    sub      edx, eax
004A4795  f7 de                    neg      esi
004A4797  81 e2 ff 00 00 00        and      edx, 0xff
004A479D  8b c2                    mov      eax, edx
004A479F  89 45 00                 mov      dword ptr [ebp], eax
004A47A2  8b 51 40                 mov      edx, dword ptr [ecx + 0x40]
004A47A5  8b 49 44                 mov      ecx, dword ptr [ecx + 0x44]
004A47A8  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004A47AC  03 d7                    add      edx, edi
004A47AE  03 ce                    add      ecx, esi
004A47B0  5f                       pop      edi
004A47B1  5e                       pop      esi
004A47B2  89 10                    mov      dword ptr [eax], edx
004A47B4  5d                       pop      ebp
004A47B5  89 48 04                 mov      dword ptr [eax + 4], ecx
004A47B8  5b                       pop      ebx
004A47B9  c2 0c 00                 ret      0xc
004A47BC  90                       nop      
004A47BD  90                       nop      
004A47BE  90                       nop      
004A47BF  90                       nop      
004A47C0  8b 49 0c                 mov      ecx, dword ptr [ecx + 0xc]
004A47C3  8d 44 24 04              lea      eax, [esp + 4]
004A47C7  50                       push     eax
004A47C8  51                       push     ecx
004A47C9  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A47CE  e8 fd 64 0b 00           call     0x55acd0
004A47D3  c2 04 00                 ret      4
004A47D6  90                       nop      
004A47D7  90                       nop      
004A47D8  90                       nop      
004A47D9  90                       nop      
004A47DA  90                       nop      
004A47DB  90                       nop      
004A47DC  90                       nop      
004A47DD  90                       nop      
004A47DE  90                       nop      
004A47DF  90                       nop      
004A47E0  b8 02 00 00 00           mov      eax, 2
004A47E5  c2 04 00                 ret      4
004A47E8  90                       nop      
004A47E9  90                       nop      
004A47EA  90                       nop      
004A47EB  90                       nop      
004A47EC  90                       nop      
004A47ED  90                       nop      
004A47EE  90                       nop      
004A47EF  90                       nop      
