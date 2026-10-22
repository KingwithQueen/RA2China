
sub_00427110 0x00427110 size=1280
00427110  83 ec 18                 sub      esp, 0x18
00427113  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00427117  53                       push     ebx
00427118  56                       push     esi
00427119  8b 74 24 28              mov      esi, dword ptr [esp + 0x28]
0042711D  8b 10                    mov      edx, dword ptr [eax]
0042711F  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
00427123  8b 1e                    mov      ebx, dword ptr [esi]
00427125  83 f8 02                 cmp      eax, 2
00427128  d9 04 85 bc f0 7c 00     fld      dword ptr [eax*4 + 0x7cf0bc]
0042712F  57                       push     edi
00427130  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
00427134  d9 5c 24 34              fstp     dword ptr [esp + 0x34]
00427138  89 54 24 18              mov      dword ptr [esp + 0x18], edx
0042713C  0f 85 45 01 00 00        jne      0x427287
00427142  8a 44 24 30              mov      al, byte ptr [esp + 0x30]
00427146  84 c0                    test     al, al
00427148  74 08                    je       0x427152
0042714A  8b bb e8 00 00 00        mov      edi, dword ptr [ebx + 0xe8]
00427150  eb 06                    jmp      0x427158
00427152  8b bb e4 00 00 00        mov      edi, dword ptr [ebx + 0xe4]
00427158  8b 41 3c                 mov      eax, dword ptr [ecx + 0x3c]
0042715B  55                       push     ebp
0042715C  33 ed                    xor      ebp, ebp
0042715E  85 c0                    test     eax, eax
00427160  0f 85 04 01 00 00        jne      0x42726a
00427166  85 ff                    test     edi, edi
00427168  0f 84 f5 00 00 00        je       0x427263
0042716E  8a 47 14                 mov      al, byte ptr [edi + 0x14]
00427171  c0 e8 02                 shr      al, 2
00427174  24 01                    and      al, 1
00427176  88 44 24 2c              mov      byte ptr [esp + 0x2c], al
0042717A  0f 84 ea 00 00 00        je       0x42726a
00427180  dd 87 68 04 00 00        fld      qword ptr [edi + 0x468]
00427186  dc 1d 10 b6 79 00        fcomp    qword ptr [0x79b610]
0042718C  df e0                    fnstsw   ax
0042718E  f6 c4 40                 test     ah, 0x40
00427191  74 11                    je       0x4271a4
00427193  8b b7 d0 04 00 00        mov      esi, dword ptr [edi + 0x4d0]
00427199  83 fe ff                 cmp      esi, -1
0042719C  0f 84 c1 00 00 00        je       0x427263
004271A2  eb 1b                    jmp      0x4271bf
004271A4  8d 4c 24 20              lea      ecx, [esp + 0x20]
004271A8  51                       push     ecx
004271A9  8d 8f e0 02 00 00        lea      ecx, [edi + 0x2e0]
004271AF  e8 2c 1a 09 00           call     0x4b8be0
004271B4  8b 30                    mov      esi, dword ptr [eax]
004271B6  c1 ee 0c                 shr      esi, 0xc
004271B9  46                       inc      esi
004271BA  d1 ee                    shr      esi, 1
004271BC  83 e6 07                 and      esi, 7
004271BF  8b 17                    mov      edx, dword ptr [edi]
004271C1  8d 44 24 24              lea      eax, [esp + 0x24]
004271C5  50                       push     eax
004271C6  8b cf                    mov      ecx, edi
004271C8  ff 92 a0 01 00 00        call     dword ptr [edx + 0x1a0]
004271CE  66 8b 10                 mov      dx, word ptr [eax]
004271D1  83 e6 07                 and      esi, 7
004271D4  66 03 14 b5 70 1a 85 00  add      dx, word ptr [esi*4 + 0x851a70]
004271DC  8d 0c b5 70 1a 85 00     lea      ecx, [esi*4 + 0x851a70]
004271E3  66 8b 0c b5 72 1a 85 00  mov      cx, word ptr [esi*4 + 0x851a72]
004271EB  66 89 54 24 10           mov      word ptr [esp + 0x10], dx
004271F0  66 03 48 02              add      cx, word ptr [eax + 2]
004271F4  8d 44 24 18              lea      eax, [esp + 0x18]
004271F8  50                       push     eax
004271F9  66 89 4c 24 16           mov      word ptr [esp + 0x16], cx
004271FE  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
00427202  b9 e0 24 83 00           mov      ecx, 0x8324e0
00427207  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
0042720B  e8 60 0e 12 00           call     0x548070
00427210  8b f0                    mov      esi, eax
00427212  8b 86 40 01 00 00        mov      eax, dword ptr [esi + 0x140]
00427218  f6 c4 01                 test     ah, 1
0042721B  74 2e                    je       0x42724b
0042721D  8a 47 79                 mov      al, byte ptr [edi + 0x79]
00427220  84 c0                    test     al, al
00427222  75 1f                    jne      0x427243
00427224  8b 17                    mov      edx, dword ptr [edi]
00427226  8b cf                    mov      ecx, edi
00427228  ff 92 a4 01 00 00        call     dword ptr [edx + 0x1a4]
0042722E  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427235  0f be 8e 1b 01 00 00     movsx    ecx, byte ptr [esi + 0x11b]
0042723C  2b c1                    sub      eax, ecx
0042723E  83 f8 02                 cmp      eax, 2
00427241  7e 08                    jle      0x42724b
00427243  8b b6 e8 00 00 00        mov      esi, dword ptr [esi + 0xe8]
00427249  eb 06                    jmp      0x427251
0042724B  8b b6 e4 00 00 00        mov      esi, dword ptr [esi + 0xe4]
00427251  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
00427255  45                       inc      ebp
00427256  83 fd 0a                 cmp      ebp, 0xa
00427259  8b fe                    mov      edi, esi
0042725B  0f 8c 05 ff ff ff        jl       0x427166
00427261  eb 07                    jmp      0x42726a
00427263  8b 41 3c                 mov      eax, dword ptr [ecx + 0x3c]
00427266  85 c0                    test     eax, eax
00427268  74 08                    je       0x427272
0042726A  c7 44 24 38 00 00 80 40  mov      dword ptr [esp + 0x38], 0x40800000
00427272  8b 41 3c                 mov      eax, dword ptr [ecx + 0x3c]
00427275  5d                       pop      ebp
00427276  83 f8 02                 cmp      eax, 2
00427279  75 08                    jne      0x427283
0042727B  c7 44 24 34 00 00 7a 44  mov      dword ptr [esp + 0x34], 0x447a0000
00427283  8b 74 24 2c              mov      esi, dword ptr [esp + 0x2c]
00427287  8b 93 40 01 00 00        mov      edx, dword ptr [ebx + 0x140]
0042728D  f7 c2 00 00 04 00        test     edx, 0x40000
00427293  74 0e                    je       0x4272a3
00427295  d9 44 24 34              fld      dword ptr [esp + 0x34]
00427299  d8 0d cc c4 79 00        fmul     dword ptr [0x79c4cc]
0042729F  d9 5c 24 34              fstp     dword ptr [esp + 0x34]
004272A3  8a 44 24 30              mov      al, byte ptr [esp + 0x30]
004272A7  84 c0                    test     al, al
004272A9  0f 84 b0 00 00 00        je       0x42735f
004272AF  8a 41 01                 mov      al, byte ptr [ecx + 1]
004272B2  84 c0                    test     al, al
004272B4  0f 84 a5 00 00 00        je       0x42735f
004272BA  8b 7c 24 18              mov      edi, dword ptr [esp + 0x18]
004272BE  66 8b 4b 26              mov      cx, word ptr [ebx + 0x26]
004272C2  66 8b 43 24              mov      ax, word ptr [ebx + 0x24]
004272C6  66 2b 4f 26              sub      cx, word ptr [edi + 0x26]
004272CA  66 2b 47 24              sub      ax, word ptr [edi + 0x24]
004272CE  d9 05 f8 b7 79 00        fld      dword ptr [0x79b7f8]
004272D4  0f bf c9                 movsx    ecx, cx
004272D7  0f bf c0                 movsx    eax, ax
004272DA  8d 0c 49                 lea      ecx, [ecx + ecx*2]
004272DD  03 c8                    add      ecx, eax
004272DF  f6 c6 08                 test     dh, 8
004272E2  8b 04 8d 70 c4 79 00     mov      eax, dword ptr [ecx*4 + 0x79c470]
004272E9  74 19                    je       0x427304
004272EB  8b 0c 85 40 c4 79 00     mov      ecx, dword ptr [eax*4 + 0x79c440]
004272F2  83 c0 fc                 add      eax, -4
004272F5  83 e0 07                 and      eax, 7
004272F8  8b 0c 8e                 mov      ecx, dword ptr [esi + ecx*4]
004272FB  8b 14 85 40 c4 79 00     mov      edx, dword ptr [eax*4 + 0x79c440]
00427302  eb 17                    jmp      0x42731b
00427304  8b 0c 85 20 c4 79 00     mov      ecx, dword ptr [eax*4 + 0x79c420]
0042730B  83 c0 fc                 add      eax, -4
0042730E  83 e0 07                 and      eax, 7
00427311  8b 0c 8e                 mov      ecx, dword ptr [esi + ecx*4]
00427314  8b 14 85 20 c4 79 00     mov      edx, dword ptr [eax*4 + 0x79c420]
0042731B  8b 04 96                 mov      eax, dword ptr [esi + edx*4]
0042731E  8b b1 40 01 00 00        mov      esi, dword ptr [ecx + 0x140]
00427324  ba 00 01 00 00           mov      edx, 0x100
00427329  85 f2                    test     edx, esi
0042732B  75 15                    jne      0x427342
0042732D  dd d8                    fstp     st(0)
0042732F  d9 05 c8 c4 79 00        fld      dword ptr [0x79c4c8]
00427335  d8 4c 24 34              fmul     dword ptr [esp + 0x34]
00427339  5f                       pop      edi
0042733A  5e                       pop      esi
0042733B  5b                       pop      ebx
0042733C  83 c4 18                 add      esp, 0x18
0042733F  c2 14 00                 ret      0x14
00427342  85 90 40 01 00 00        test     dword ptr [eax + 0x140], edx
00427348  74 08                    je       0x427352
0042734A  dd d8                    fstp     st(0)
0042734C  d9 05 c4 c4 79 00        fld      dword ptr [0x79c4c4]
00427352  d8 4c 24 34              fmul     dword ptr [esp + 0x34]
00427356  5f                       pop      edi
00427357  5e                       pop      esi
00427358  5b                       pop      ebx
00427359  83 c4 18                 add      esp, 0x18
0042735C  c2 14 00                 ret      0x14
0042735F  d9 44 24 34              fld      dword ptr [esp + 0x34]
00427363  5f                       pop      edi
00427364  5e                       pop      esi
00427365  5b                       pop      ebx
00427366  83 c4 18                 add      esp, 0x18
00427369  c2 14 00                 ret      0x14
0042736C  90                       nop      
0042736D  90                       nop      
0042736E  90                       nop      
0042736F  90                       nop      
00427370  83 ec 4c                 sub      esp, 0x4c
00427373  53                       push     ebx
00427374  55                       push     ebp
00427375  56                       push     esi
00427376  57                       push     edi
00427377  8b 7c 24 64              mov      edi, dword ptr [esp + 0x64]
0042737B  8b 6c 24 60              mov      ebp, dword ptr [esp + 0x60]
0042737F  8b f1                    mov      esi, ecx
00427381  a1 18 26 83 00           mov      eax, dword ptr [0x832618]
00427386  0f bf 4f 02              movsx    ecx, word ptr [edi + 2]
0042738A  0f bf 17                 movsx    edx, word ptr [edi]
0042738D  0f bf 5d 00              movsx    ebx, word ptr [ebp]
00427391  c1 e1 09                 shl      ecx, 9
00427394  03 ca                    add      ecx, edx
00427396  c7 44 24 28 00 00 00 00  mov      dword ptr [esp + 0x28], 0
0042739E  0f bf 55 02              movsx    edx, word ptr [ebp + 2]
004273A2  c1 e2 09                 shl      edx, 9
004273A5  03 d3                    add      edx, ebx
004273A7  8d 0c 88                 lea      ecx, [eax + ecx*4]
004273AA  89 4c 24 38              mov      dword ptr [esp + 0x38], ecx
004273AE  8b 09                    mov      ecx, dword ptr [ecx]
004273B0  8d 04 90                 lea      eax, [eax + edx*4]
004273B3  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004273B7  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
004273BB  8b 00                    mov      eax, dword ptr [eax]
004273BD  85 c0                    test     eax, eax
004273BF  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004273C3  0f 84 65 09 00 00        je       0x427d2e
004273C9  85 c9                    test     ecx, ecx
004273CB  0f 84 5d 09 00 00        je       0x427d2e
004273D1  8b 5c 24 68              mov      ebx, dword ptr [esp + 0x68]
004273D5  8b cb                    mov      ecx, ebx
004273D7  8b 03                    mov      eax, dword ptr [ebx]
004273D9  ff 50 2c                 call     dword ptr [eax + 0x2c]
004273DC  83 f8 02                 cmp      eax, 2
004273DF  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004273E3  74 17                    je       0x4273fc
004273E5  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004273EB  f6 c5 01                 test     ch, 1
004273EE  74 0c                    je       0x4273fc
004273F0  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
004273F7  83 c0 04                 add      eax, 4
004273FA  eb 07                    jmp      0x427403
004273FC  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427403  89 46 34                 mov      dword ptr [esi + 0x34], eax
00427406  8b 13                    mov      edx, dword ptr [ebx]
00427408  8b cb                    mov      ecx, ebx
0042740A  ff 52 2c                 call     dword ptr [edx + 0x2c]
0042740D  83 f8 02                 cmp      eax, 2
00427410  74 17                    je       0x427429
00427412  8a 43 79                 mov      al, byte ptr [ebx + 0x79]
00427415  84 c0                    test     al, al
00427417  74 10                    je       0x427429
00427419  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
0042741D  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427424  83 c0 04                 add      eax, 4
00427427  eb 0b                    jmp      0x427434
00427429  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
0042742D  0f be 81 1b 01 00 00     movsx    eax, byte ptr [ecx + 0x11b]
00427434  89 46 30                 mov      dword ptr [esi + 0x30], eax
00427437  8b 13                    mov      edx, dword ptr [ebx]
00427439  8b cb                    mov      ecx, ebx
0042743B  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
00427441  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
00427447  84 c9                    test     cl, cl
00427449  74 45                    je       0x427490
0042744B  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
0042744F  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
00427455  f6 c5 01                 test     ch, 1
00427458  74 36                    je       0x427490
0042745A  8d 8b 88 00 00 00        lea      ecx, [ebx + 0x88]
00427460  8b 93 88 00 00 00        mov      edx, dword ptr [ebx + 0x88]
00427466  89 54 24 50              mov      dword ptr [esp + 0x50], edx
0042746A  8b 41 04                 mov      eax, dword ptr [ecx + 4]
0042746D  89 44 24 54              mov      dword ptr [esp + 0x54], eax
00427471  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427474  8b 4e 30                 mov      ecx, dword ptr [esi + 0x30]
00427477  99                       cdq      
00427478  f7 3d 00 e8 84 00        idiv     dword ptr [0x84e800]
0042747E  2b c1                    sub      eax, ecx
00427480  99                       cdq      
00427481  33 c2                    xor      eax, edx
00427483  2b c2                    sub      eax, edx
00427485  83 f8 02                 cmp      eax, 2
00427488  7e 06                    jle      0x427490
0042748A  83 c1 04                 add      ecx, 4
0042748D  89 4e 30                 mov      dword ptr [esi + 0x30], ecx
00427490  8b 13                    mov      edx, dword ptr [ebx]
00427492  8b cb                    mov      ecx, ebx
00427494  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
0042749A  8b 80 a4 05 00 00        mov      eax, dword ptr [eax + 0x5a4]
004274A0  8b 56 40                 mov      edx, dword ptr [esi + 0x40]
004274A3  89 46 2c                 mov      dword ptr [esi + 0x2c], eax
004274A6  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
004274AA  c7 46 6c 00 00 00 00     mov      dword ptr [esi + 0x6c], 0
004274B1  8b 4d 00                 mov      ecx, dword ptr [ebp]
004274B4  6a 00                    push     0
004274B6  57                       push     edi
004274B7  89 4e 70                 mov      dword ptr [esi + 0x70], ecx
004274BA  50                       push     eax
004274BB  6a 00                    push     0
004274BD  8b ce                    mov      ecx, esi
004274BF  89 54 24 50              mov      dword ptr [esp + 0x50], edx
004274C3  e8 78 08 00 00           call     0x427d40
004274C8  66 8b 4d 00              mov      cx, word ptr [ebp]
004274CC  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004274D0  66 3b 0f                 cmp      cx, word ptr [edi]
004274D3  75 18                    jne      0x4274ed
004274D5  66 8b 55 02              mov      dx, word ptr [ebp + 2]
004274D9  66 3b 57 02              cmp      dx, word ptr [edi + 2]
004274DD  75 0e                    jne      0x4274ed
004274DF  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
004274E2  8b 4e 34                 mov      ecx, dword ptr [esi + 0x34]
004274E5  3b c1                    cmp      eax, ecx
004274E7  0f 84 41 08 00 00        je       0x427d2e
004274ED  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
004274F0  85 c0                    test     eax, eax
004274F2  74 08                    je       0x4274fc
004274F4  53                       push     ebx
004274F5  8b ce                    mov      ecx, esi
004274F7  e8 d4 10 00 00           call     0x4285d0
004274FC  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
00427500  0f bf 41 26              movsx    eax, word ptr [ecx + 0x26]
00427504  0f af 05 04 e8 84 00     imul     eax, dword ptr [0x84e804]
0042750B  0f bf 51 24              movsx    edx, word ptr [ecx + 0x24]
0042750F  0f be 89 1b 01 00 00     movsx    ecx, byte ptr [ecx + 0x11b]
00427516  03 c2                    add      eax, edx
00427518  8b 56 30                 mov      edx, dword ptr [esi + 0x30]
0042751B  3b d1                    cmp      edx, ecx
0042751D  7e 15                    jle      0x427534
0042751F  8b 56 1c                 mov      edx, dword ptr [esi + 0x1c]
00427522  8b 4e 28                 mov      ecx, dword ptr [esi + 0x28]
00427525  89 0c 82                 mov      dword ptr [edx + eax*4], ecx
00427528  8b 56 20                 mov      edx, dword ptr [esi + 0x20]
0042752B  c7 04 82 00 00 00 00     mov      dword ptr [edx + eax*4], 0
00427532  eb 13                    jmp      0x427547
00427534  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
00427537  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
0042753A  89 14 81                 mov      dword ptr [ecx + eax*4], edx
0042753D  8b 4e 24                 mov      ecx, dword ptr [esi + 0x24]
00427540  c7 04 81 00 00 00 00     mov      dword ptr [ecx + eax*4], 0
00427547  8b 13                    mov      edx, dword ptr [ebx]
00427549  8b cb                    mov      ecx, ebx
0042754B  c6 44 24 12 00           mov      byte ptr [esp + 0x12], 0
00427550  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
00427556  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
0042755C  84 c9                    test     cl, cl
0042755E  0f 84 a4 00 00 00        je       0x427608
00427564  c6 44 24 12 01           mov      byte ptr [esp + 0x12], 1
00427569  33 ed                    xor      ebp, ebp
0042756B  bf 84 c4 79 00           mov      edi, 0x79c484
00427570  8d 44 24 60              lea      eax, [esp + 0x60]
00427574  8d 8b e0 02 00 00        lea      ecx, [ebx + 0x2e0]
0042757A  50                       push     eax
0042757B  e8 60 16 09 00           call     0x4b8be0
00427580  8b 00                    mov      eax, dword ptr [eax]
00427582  c1 e8 0c                 shr      eax, 0xc
00427585  40                       inc      eax
00427586  d1 e8                    shr      eax, 1
00427588  83 e0 07                 and      eax, 7
0042758B  2b c5                    sub      eax, ebp
0042758D  99                       cdq      
0042758E  33 c2                    xor      eax, edx
00427590  2b c2                    sub      eax, edx
00427592  83 f8 02                 cmp      eax, 2
00427595  7e 61                    jle      0x4275f8
00427597  83 f8 06                 cmp      eax, 6
0042759A  7d 5c                    jge      0x4275f8
0042759C  81 ff a4 c4 79 00        cmp      edi, 0x79c4a4
004275A2  74 54                    je       0x4275f8
004275A4  8b 0f                    mov      ecx, dword ptr [edi]
004275A6  8b 54 24 2c              mov      edx, dword ptr [esp + 0x2c]
004275AA  8d 04 8a                 lea      eax, [edx + ecx*4]
004275AD  8b 0c 8a                 mov      ecx, dword ptr [edx + ecx*4]
004275B0  0f bf 41 26              movsx    eax, word ptr [ecx + 0x26]
004275B4  0f af 05 04 e8 84 00     imul     eax, dword ptr [0x84e804]
004275BB  0f bf 51 24              movsx    edx, word ptr [ecx + 0x24]
004275BF  0f be 89 1b 01 00 00     movsx    ecx, byte ptr [ecx + 0x11b]
004275C6  03 c2                    add      eax, edx
004275C8  8b 56 30                 mov      edx, dword ptr [esi + 0x30]
004275CB  41                       inc      ecx
004275CC  3b d1                    cmp      edx, ecx
004275CE  7e 15                    jle      0x4275e5
004275D0  8b 56 1c                 mov      edx, dword ptr [esi + 0x1c]
004275D3  8b 4e 28                 mov      ecx, dword ptr [esi + 0x28]
004275D6  89 0c 82                 mov      dword ptr [edx + eax*4], ecx
004275D9  8b 56 20                 mov      edx, dword ptr [esi + 0x20]
004275DC  c7 04 82 00 00 00 00     mov      dword ptr [edx + eax*4], 0
004275E3  eb 13                    jmp      0x4275f8
004275E5  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
004275E8  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
004275EB  89 14 81                 mov      dword ptr [ecx + eax*4], edx
004275EE  8b 4e 24                 mov      ecx, dword ptr [esi + 0x24]
004275F1  c7 04 81 00 00 00 00     mov      dword ptr [ecx + eax*4], 0
004275F8  83 c7 04                 add      edi, 4
004275FB  45                       inc      ebp
004275FC  81 ff a4 c4 79 00        cmp      edi, 0x79c4a4
00427602  0f 8e 68 ff ff ff        jle      0x427570
00427608  8b 13                    mov      edx, dword ptr [ebx]
0042760A  8b cb                    mov      ecx, ebx
0042760C  ff 52 2c                 call     dword ptr [edx + 0x2c]
