
sub_00427110 0x00427110 size=608
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
