
sub_0071E61C 0x0071F077 size=1214
0071F077  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F07A  8b 33                    mov      esi, dword ptr [ebx]
0071F07C  8b 7b 04                 mov      edi, dword ptr [ebx + 4]
0071F07F  c6 45 36 01              mov      byte ptr [ebp + 0x36], 1
0071F083  8b 11                    mov      edx, dword ptr [ecx]
0071F085  8d 44 24 3c              lea      eax, [esp + 0x3c]
0071F089  50                       push     eax
0071F08A  ff 52 48                 call     dword ptr [edx + 0x48]
0071F08D  8b 08                    mov      ecx, dword ptr [eax]
0071F08F  8b 40 04                 mov      eax, dword ptr [eax + 4]
0071F092  2b c7                    sub      eax, edi
0071F094  2b ce                    sub      ecx, esi
0071F096  89 44 24 28              mov      dword ptr [esp + 0x28], eax
0071F09A  89 4c 24 24              mov      dword ptr [esp + 0x24], ecx
0071F09E  db 44 24 28              fild     dword ptr [esp + 0x28]
0071F0A2  db 44 24 24              fild     dword ptr [esp + 0x24]
0071F0A6  83 ec 08                 sub      esp, 8
0071F0A9  d9 c0                    fld      st(0)
0071F0AB  d8 c9                    fmul     st(1)
0071F0AD  d9 c2                    fld      st(2)
0071F0AF  d8 cb                    fmul     st(3)
0071F0B1  de c1                    faddp    st(1)
0071F0B3  dd 1c 24                 fstp     qword ptr [esp]
0071F0B6  dd d8                    fstp     st(0)
0071F0B8  dd d8                    fstp     st(0)
0071F0BA  e8 51 b3 d9 ff           call     0x4ba410
0071F0BF  83 c4 08                 add      esp, 8
0071F0C2  e8 49 00 06 00           call     0x77f110
0071F0C7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F0CA  83 f8 11                 cmp      eax, 0x11
0071F0CD  0f 8d 03 02 00 00        jge      0x71f2d6
0071F0D3  8b 11                    mov      edx, dword ptr [ecx]
0071F0D5  6a 00                    push     0
0071F0D7  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
0071F0DD  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F0E0  83 c9 ff                 or       ecx, 0xffffffff
0071F0E3  39 88 d0 04 00 00        cmp      dword ptr [eax + 0x4d0], ecx
0071F0E9  75 06                    jne      0x71f0f1
0071F0EB  89 88 d4 04 00 00        mov      dword ptr [eax + 0x4d4], ecx
0071F0F1  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F0F4  b9 17 00 00 00           mov      ecx, 0x17
0071F0F9  53                       push     ebx
0071F0FA  8d b0 d4 04 00 00        lea      esi, [eax + 0x4d4]
0071F100  8d b8 d0 04 00 00        lea      edi, [eax + 0x4d0]
0071F106  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
0071F108  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F10B  c7 80 2c 05 00 00 ff ff ff ff mov      dword ptr [eax + 0x52c], 0xffffffff
0071F115  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F118  8b 11                    mov      edx, dword ptr [ecx]
0071F11A  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
0071F120  8b 03                    mov      eax, dword ptr [ebx]
0071F122  6a 00                    push     0
0071F124  99                       cdq      
0071F125  81 e2 ff 00 00 00        and      edx, 0xff
0071F12B  03 c2                    add      eax, edx
0071F12D  c1 f8 08                 sar      eax, 8
0071F130  66 89 44 24 50           mov      word ptr [esp + 0x50], ax
0071F135  8b 43 04                 mov      eax, dword ptr [ebx + 4]
0071F138  99                       cdq      
0071F139  81 e2 ff 00 00 00        and      edx, 0xff
0071F13F  03 c2                    add      eax, edx
0071F141  c1 f8 08                 sar      eax, 8
0071F144  66 89 44 24 52           mov      word ptr [esp + 0x52], ax
0071F149  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F14C  8b 4c 24 50              mov      ecx, dword ptr [esp + 0x50]
0071F150  89 88 50 04 00 00        mov      dword ptr [eax + 0x450], ecx
0071F156  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F159  8b 11                    mov      edx, dword ptr [ecx]
0071F15B  ff 92 b4 01 00 00        call     dword ptr [edx + 0x1b4]
0071F161  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F164  68 60 90 af 00           push     0xaf9060
0071F169  8b cd                    mov      ecx, ebp
0071F16B  c6 80 a1 05 00 00 00     mov      byte ptr [eax + 0x5a1], 0
0071F172  e8 19 04 00 00           call     0x71f590
0071F177  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F17A  83 b9 d0 04 00 00 ff     cmp      dword ptr [ecx + 0x4d0], -1
0071F181  75 0c                    jne      0x71f18f
0071F183  8b 11                    mov      edx, dword ptr [ecx]
0071F185  6a 00                    push     0
0071F187  6a 00                    push     0
0071F189  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
0071F18F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F192  6a 02                    push     2
0071F194  8b 01                    mov      eax, dword ptr [ecx]
0071F196  ff 90 74 01 00 00        call     dword ptr [eax + 0x174]
0071F19C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F19F  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
0071F1A2  84 c0                    test     al, al
0071F1A4  0f 84 92 03 00 00        je       0x71f53c
0071F1AA  8a 41 76                 mov      al, byte ptr [ecx + 0x76]
0071F1AD  84 c0                    test     al, al
0071F1AF  0f 85 87 03 00 00        jne      0x71f53c
0071F1B5  8a 41 7a                 mov      al, byte ptr [ecx + 0x7a]
0071F1B8  84 c0                    test     al, al
0071F1BA  0f 85 7c 03 00 00        jne      0x71f53c
0071F1C0  8b 55 1c                 mov      edx, dword ptr [ebp + 0x1c]
0071F1C3  a1 60 90 af 00           mov      eax, dword ptr [0xaf9060]
0071F1C8  3b d0                    cmp      edx, eax
0071F1CA  75 1d                    jne      0x71f1e9
0071F1CC  8b 45 20                 mov      eax, dword ptr [ebp + 0x20]
0071F1CF  8b 15 64 90 af 00        mov      edx, dword ptr [0xaf9064]
0071F1D5  3b c2                    cmp      eax, edx
0071F1D7  75 10                    jne      0x71f1e9
0071F1D9  8b 55 24                 mov      edx, dword ptr [ebp + 0x24]
0071F1DC  a1 68 90 af 00           mov      eax, dword ptr [0xaf9068]
0071F1E1  3b d0                    cmp      edx, eax
0071F1E3  0f 84 88 00 00 00        je       0x71f271
0071F1E9  8b 45 1c                 mov      eax, dword ptr [ebp + 0x1c]
0071F1EC  6a 00                    push     0
0071F1EE  99                       cdq      
0071F1EF  81 e2 ff 00 00 00        and      edx, 0xff
0071F1F5  03 c2                    add      eax, edx
0071F1F7  8b f0                    mov      esi, eax
0071F1F9  8b 45 20                 mov      eax, dword ptr [ebp + 0x20]
0071F1FC  99                       cdq      
0071F1FD  81 e2 ff 00 00 00        and      edx, 0xff
0071F203  03 c2                    add      eax, edx
0071F205  8d 54 24 40              lea      edx, [esp + 0x40]
0071F209  8b f8                    mov      edi, eax
0071F20B  8b 01                    mov      eax, dword ptr [ecx]
0071F20D  52                       push     edx
0071F20E  c1 fe 08                 sar      esi, 8
0071F211  c1 ff 08                 sar      edi, 8
0071F214  ff 50 4c                 call     dword ptr [eax + 0x4c]
0071F217  89 44 24 4c              mov      dword ptr [esp + 0x4c], eax
0071F21B  8b 00                    mov      eax, dword ptr [eax]
0071F21D  99                       cdq      
0071F21E  81 e2 ff 00 00 00        and      edx, 0xff
0071F224  03 c2                    add      eax, edx
0071F226  8b c8                    mov      ecx, eax
0071F228  8b 44 24 4c              mov      eax, dword ptr [esp + 0x4c]
0071F22C  c1 f9 08                 sar      ecx, 8
0071F22F  8b 40 04                 mov      eax, dword ptr [eax + 4]
0071F232  99                       cdq      
0071F233  81 e2 ff 00 00 00        and      edx, 0xff
0071F239  03 c2                    add      eax, edx
0071F23B  c1 f8 08                 sar      eax, 8
0071F23E  66 3b ce                 cmp      cx, si
0071F241  75 72                    jne      0x71f2b5
0071F243  66 3b c7                 cmp      ax, di
0071F246  75 6d                    jne      0x71f2b5
0071F248  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F24B  8d 44 24 3c              lea      eax, [esp + 0x3c]
0071F24F  6a 00                    push     0
0071F251  50                       push     eax
0071F252  8b 11                    mov      edx, dword ptr [ecx]
0071F254  ff 52 4c                 call     dword ptr [edx + 0x4c]
0071F257  8b 40 08                 mov      eax, dword ptr [eax + 8]
0071F25A  8b 4d 24                 mov      ecx, dword ptr [ebp + 0x24]
0071F25D  2b c1                    sub      eax, ecx
0071F25F  8b 0d 98 90 af 00        mov      ecx, dword ptr [0xaf9098]
0071F265  99                       cdq      
0071F266  33 c2                    xor      eax, edx
0071F268  2b c2                    sub      eax, edx
0071F26A  8d 14 09                 lea      edx, [ecx + ecx]
0071F26D  3b c2                    cmp      eax, edx
0071F26F  7d 44                    jge      0x71f2b5
0071F271  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F274  6a 01                    push     1
0071F276  6a 00                    push     0
0071F278  8b 01                    mov      eax, dword ptr [ecx]
0071F27A  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
0071F280  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F283  6a 00                    push     0
0071F285  6a 00                    push     0
0071F287  8b 11                    mov      edx, dword ptr [ecx]
0071F289  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
0071F28F  a1 60 90 af 00           mov      eax, dword ptr [0xaf9060]
0071F294  89 03                    mov      dword ptr [ebx], eax
0071F296  8b 0d 64 90 af 00        mov      ecx, dword ptr [0xaf9064]
0071F29C  8d 45 04                 lea      eax, [ebp + 4]
0071F29F  89 4b 04                 mov      dword ptr [ebx + 4], ecx
0071F2A2  8b 15 68 90 af 00        mov      edx, dword ptr [0xaf9068]
0071F2A8  50                       push     eax
0071F2A9  8b 08                    mov      ecx, dword ptr [eax]
0071F2AB  89 53 08                 mov      dword ptr [ebx + 8], edx
0071F2AE  ff 51 48                 call     dword ptr [ecx + 0x48]
0071F2B1  c6 45 36 00              mov      byte ptr [ebp + 0x36], 0
0071F2B5  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F2B8  6a 01                    push     1
0071F2BA  8b 11                    mov      edx, dword ptr [ecx]
0071F2BC  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
0071F2C2  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F2C5  5f                       pop      edi
0071F2C6  5e                       pop      esi
0071F2C7  5d                       pop      ebp
0071F2C8  c6 80 7a 05 00 00 00     mov      byte ptr [eax + 0x57a], 0
0071F2CF  5b                       pop      ebx
0071F2D0  83 c4 38                 add      esp, 0x38
0071F2D3  c2 04 00                 ret      4
0071F2D6  8b 01                    mov      eax, dword ptr [ecx]
0071F2D8  ff 90 24 03 00 00        call     dword ptr [eax + 0x324]
0071F2DE  84 c0                    test     al, al
0071F2E0  74 18                    je       0x71f2fa
0071F2E2  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F2E5  5f                       pop      edi
0071F2E6  c6 45 36 00              mov      byte ptr [ebp + 0x36], 0
0071F2EA  5e                       pop      esi
0071F2EB  5d                       pop      ebp
0071F2EC  c6 80 7a 05 00 00 00     mov      byte ptr [eax + 0x57a], 0
0071F2F3  5b                       pop      ebx
0071F2F4  83 c4 38                 add      esp, 0x38
0071F2F7  c2 04 00                 ret      4
0071F2FA  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F2FD  68 00 00 f0 3f           push     0x3ff00000
0071F302  6a 00                    push     0
0071F304  8b 11                    mov      edx, dword ptr [ecx]
0071F306  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
0071F30C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F30F  8b 01                    mov      eax, dword ptr [ecx]
0071F311  ff 90 bc 04 00 00        call     dword ptr [eax + 0x4bc]
0071F317  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F31A  89 44 24 14              mov      dword ptr [esp + 0x14], eax
0071F31E  8d 44 24 3c              lea      eax, [esp + 0x3c]
0071F322  c6 81 a1 05 00 00 00     mov      byte ptr [ecx + 0x5a1], 0
0071F329  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F32C  50                       push     eax
0071F32D  8b 11                    mov      edx, dword ptr [ecx]
0071F32F  ff 52 48                 call     dword ptr [edx + 0x48]
0071F332  8b 13                    mov      edx, dword ptr [ebx]
0071F334  8b 08                    mov      ecx, dword ptr [eax]
0071F336  89 54 24 24              mov      dword ptr [esp + 0x24], edx
0071F33A  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
0071F33E  db 44 24 24              fild     dword ptr [esp + 0x24]
0071F342  83 ec 08                 sub      esp, 8
0071F345  83 ec 08                 sub      esp, 8
0071F348  da 64 24 2c              fisub    dword ptr [esp + 0x2c]
0071F34C  dd 5c 24 08              fstp     qword ptr [esp + 8]
0071F350  db 40 04                 fild     dword ptr [eax + 4]
0071F353  da 63 04                 fisub    dword ptr [ebx + 4]
0071F356  dd 1c 24                 fstp     qword ptr [esp]
0071F359  e8 a2 b2 d9 ff           call     0x4ba600
0071F35E  dc 25 30 b6 79 00        fsub     qword ptr [0x79b630]
0071F364  83 c4 10                 add      esp, 0x10
0071F367  dc 0d 28 b6 79 00        fmul     qword ptr [0x79b628]
0071F36D  e8 9e fd 05 00           call     0x77f110
0071F372  8b 4d 04                 mov      ecx, dword ptr [ebp + 4]
0071F375  66 8b f0                 mov      si, ax
0071F378  66 89 74 24 24           mov      word ptr [esp + 0x24], si
0071F37D  8b 54 24 24              mov      edx, dword ptr [esp + 0x24]
0071F381  8d 45 04                 lea      eax, [ebp + 4]
0071F384  52                       push     edx
0071F385  50                       push     eax
0071F386  ff 51 4c                 call     dword ptr [ecx + 0x4c]
0071F389  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F38C  8d 54 24 24              lea      edx, [esp + 0x24]
0071F390  52                       push     edx
0071F391  8b 01                    mov      eax, dword ptr [ecx]
0071F393  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
0071F399  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F39C  8b 00                    mov      eax, dword ptr [eax]
0071F39E  81 c1 88 00 00 00        add      ecx, 0x88
0071F3A4  89 44 24 4c              mov      dword ptr [esp + 0x4c], eax
0071F3A8  8b 11                    mov      edx, dword ptr [ecx]
0071F3AA  89 54 24 3c              mov      dword ptr [esp + 0x3c], edx
0071F3AE  8b 41 04                 mov      eax, dword ptr [ecx + 4]
0071F3B1  89 44 24 40              mov      dword ptr [esp + 0x40], eax
0071F3B5  8b 79 08                 mov      edi, dword ptr [ecx + 8]
0071F3B8  0f bf ce                 movsx    ecx, si
0071F3BB  81 e9 ff 3f 00 00        sub      ecx, 0x3fff
0071F3C1  89 4c 24 24              mov      dword ptr [esp + 0x24], ecx
0071F3C5  db 44 24 24              fild     dword ptr [esp + 0x24]
0071F3C9  dc 0d 20 b6 79 00        fmul     qword ptr [0x79b620]
0071F3CF  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
0071F3D3  db 44 24 14              fild     dword ptr [esp + 0x14]
0071F3D7  8b 5c 24 28              mov      ebx, dword ptr [esp + 0x28]
0071F3DB  8b 54 24 24              mov      edx, dword ptr [esp + 0x24]
0071F3DF  53                       push     ebx
0071F3E0  52                       push     edx
0071F3E1  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
0071F3E5  db 44 24 48              fild     dword ptr [esp + 0x48]
0071F3E9  dd 5c 24 1c              fstp     qword ptr [esp + 0x1c]
0071F3ED  e8 8e b0 d9 ff           call     0x4ba480
0071F3F2  dc 4c 24 24              fmul     qword ptr [esp + 0x24]
0071F3F6  dc 6c 24 1c              fsubr    qword ptr [esp + 0x1c]
0071F3FA  e8 11 fd 05 00           call     0x77f110
0071F3FF  8b f0                    mov      esi, eax
0071F401  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
0071F405  53                       push     ebx
0071F406  50                       push     eax
0071F407  e8 c4 b0 d9 ff           call     0x4ba4d0
0071F40C  dc 4c 24 2c              fmul     qword ptr [esp + 0x2c]
0071F410  83 c4 10                 add      esp, 0x10
0071F413  da 44 24 3c              fiadd    dword ptr [esp + 0x3c]
0071F417  e8 f4 fc 05 00           call     0x77f110
0071F41C  89 44 24 30              mov      dword ptr [esp + 0x30], eax
0071F420  89 74 24 34              mov      dword ptr [esp + 0x34], esi
0071F424  99                       cdq      
0071F425  81 e2 ff 00 00 00        and      edx, 0xff
0071F42B  89 7c 24 38              mov      dword ptr [esp + 0x38], edi
0071F42F  03 c2                    add      eax, edx
0071F431  8b c8                    mov      ecx, eax
0071F433  8b c6                    mov      eax, esi
0071F435  99                       cdq      
0071F436  81 e2 ff 00 00 00        and      edx, 0xff
0071F43C  03 c2                    add      eax, edx
0071F43E  c1 f9 08                 sar      ecx, 8
0071F441  c1 f8 08                 sar      eax, 8
0071F444  66 39 4c 24 4c           cmp      word ptr [esp + 0x4c], cx
0071F449  66 89 4c 24 1c           mov      word ptr [esp + 0x1c], cx
0071F44E  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
0071F453  8b 54 24 1c              mov      edx, dword ptr [esp + 0x1c]
0071F457  89 54 24 10              mov      dword ptr [esp + 0x10], edx
0071F45B  75 0b                    jne      0x71f468
0071F45D  66 39 44 24 4e           cmp      word ptr [esp + 0x4e], ax
0071F462  0f 84 de 00 00 00        je       0x71f546
0071F468  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F46B  6a 00                    push     0
0071F46D  8b 01                    mov      eax, dword ptr [ecx]
0071F46F  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
0071F475  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F478  8d 44 24 30              lea      eax, [esp + 0x30]
0071F47C  50                       push     eax
0071F47D  8b 11                    mov      edx, dword ptr [ecx]
0071F47F  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
0071F485  8d 4c 24 4c              lea      ecx, [esp + 0x4c]
0071F489  51                       push     ecx
0071F48A  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F48F  e8 dc 8b e2 ff           call     0x548070
0071F494  8d 54 24 10              lea      edx, [esp + 0x10]
0071F498  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F49D  52                       push     edx
0071F49E  8b f0                    mov      esi, eax
0071F4A0  e8 cb 8b e2 ff           call     0x548070
0071F4A5  0f be 96 1b 01 00 00     movsx    edx, byte ptr [esi + 0x11b]
0071F4AC  0f be b8 1b 01 00 00     movsx    edi, byte ptr [eax + 0x11b]
0071F4B3  83 ea 04                 sub      edx, 4
0071F4B6  b9 00 01 00 00           mov      ecx, 0x100
0071F4BB  3b fa                    cmp      edi, edx
0071F4BD  75 0f                    jne      0x71f4ce
0071F4BF  85 88 40 01 00 00        test     dword ptr [eax + 0x140], ecx
0071F4C5  74 0f                    je       0x71f4d6
0071F4C7  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
0071F4CA  c6 42 79 01              mov      byte ptr [edx + 0x79], 1
0071F4CE  85 88 40 01 00 00        test     dword ptr [eax + 0x140], ecx
0071F4D4  75 0f                    jne      0x71f4e5
0071F4D6  85 8e 40 01 00 00        test     dword ptr [esi + 0x140], ecx
0071F4DC  74 07                    je       0x71f4e5
0071F4DE  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
0071F4E1  c6 40 79 00              mov      byte ptr [eax + 0x79], 0
0071F4E5  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F4E8  6a 00                    push     0
0071F4EA  8b 11                    mov      edx, dword ptr [ecx]
0071F4EC  ff 92 b4 01 00 00        call     dword ptr [edx + 0x1b4]
0071F4F2  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F4F5  6a 01                    push     1
0071F4F7  8b 01                    mov      eax, dword ptr [ecx]
0071F4F9  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
0071F4FF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
0071F502  81 c1 88 00 00 00        add      ecx, 0x88
0071F508  8b 11                    mov      edx, dword ptr [ecx]
0071F50A  89 54 24 3c              mov      dword ptr [esp + 0x3c], edx
0071F50E  8d 54 24 3c              lea      edx, [esp + 0x3c]
0071F512  8b 41 04                 mov      eax, dword ptr [ecx + 4]
0071F515  52                       push     edx
0071F516  89 44 24 44              mov      dword ptr [esp + 0x44], eax
0071F51A  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
0071F51D  89 4c 24 48              mov      dword ptr [esp + 0x48], ecx
0071F521  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F526  e8 d5 8a e2 ff           call     0x548000
0071F52B  8b c8                    mov      ecx, eax
0071F52D  e8 fe c5 d5 ff           call     0x47bb30
0071F532  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
