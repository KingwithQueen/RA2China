
sub_004C34E0 0x004C36EC size=474
004C36EC  8b 15 48 98 83 00        mov      edx, dword ptr [0x839848]
004C36F2  8b 35 2c 0d a4 00        mov      esi, dword ptr [0xa40d2c]
004C36F8  dd 82 c8 13 00 00        fld      qword ptr [edx + 0x13c8]
004C36FE  dc 0d 08 b6 79 00        fmul     qword ptr [0x79b608]
004C3704  e8 07 ba 2b 00           call     0x77f110
004C3709  8b 4c 24 34              mov      ecx, dword ptr [esp + 0x34]
004C370D  8b 55 00                 mov      edx, dword ptr [ebp]
004C3710  89 33                    mov      dword ptr [ebx], esi
004C3712  89 4b 04                 mov      dword ptr [ebx + 4], ecx
004C3715  8b cd                    mov      ecx, ebp
004C3717  89 43 08                 mov      dword ptr [ebx + 8], eax
004C371A  ff 92 8c 04 00 00        call     dword ptr [edx + 0x48c]
004C3720  8d 85 88 00 00 00        lea      eax, [ebp + 0x88]
004C3726  8b d0                    mov      edx, eax
004C3728  8b 02                    mov      eax, dword ptr [edx]
004C372A  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004C372D  8b 52 08                 mov      edx, dword ptr [edx + 8]
004C3730  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004C3734  99                       cdq      
004C3735  81 e2 ff 00 00 00        and      edx, 0xff
004C373B  03 c2                    add      eax, edx
004C373D  8b f0                    mov      esi, eax
004C373F  8b c1                    mov      eax, ecx
004C3741  99                       cdq      
004C3742  0f bf 8c 24 ae 1f 00 00  movsx    ecx, word ptr [esp + 0x1fae]
004C374A  81 e2 ff 00 00 00        and      edx, 0xff
004C3750  03 c2                    add      eax, edx
004C3752  c1 f8 08                 sar      eax, 8
004C3755  0f bf c0                 movsx    eax, ax
004C3758  2b c1                    sub      eax, ecx
004C375A  99                       cdq      
004C375B  8b c8                    mov      ecx, eax
004C375D  33 ca                    xor      ecx, edx
004C375F  c1 fe 08                 sar      esi, 8
004C3762  2b ca                    sub      ecx, edx
004C3764  0f bf 94 24 ac 1f 00 00  movsx    edx, word ptr [esp + 0x1fac]
004C376C  0f bf c6                 movsx    eax, si
004C376F  2b c2                    sub      eax, edx
004C3771  99                       cdq      
004C3772  33 c2                    xor      eax, edx
004C3774  2b c2                    sub      eax, edx
004C3776  3b c1                    cmp      eax, ecx
004C3778  7f 02                    jg       0x4c377c
004C377A  8b c1                    mov      eax, ecx
004C377C  83 f8 01                 cmp      eax, 1
004C377F  7f 2c                    jg       0x4c37ad
004C3781  8a 45 79                 mov      al, byte ptr [ebp + 0x79]
004C3784  84 c0                    test     al, al
004C3786  0f 85 2c 01 00 00        jne      0x4c38b8
004C378C  8d 84 24 ac 1f 00 00     lea      eax, [esp + 0x1fac]
004C3793  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3798  50                       push     eax
004C3799  e8 d2 48 08 00           call     0x548070
004C379E  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004C37A4  f6 c5 01                 test     ch, 1
004C37A7  0f 84 0b 01 00 00        je       0x4c38b8
004C37AD  8b 85 c4 04 00 00        mov      eax, dword ptr [ebp + 0x4c4]
004C37B3  85 c0                    test     eax, eax
004C37B5  74 56                    je       0x4c380d
004C37B7  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37BD  85 c0                    test     eax, eax
004C37BF  75 0a                    jne      0x4c37cb
004C37C1  68 03 40 00 80           push     0x80004003
004C37C6  e8 75 21 2d 00           call     0x795940
004C37CB  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37D1  50                       push     eax
004C37D2  8b 08                    mov      ecx, dword ptr [eax]
004C37D4  ff 91 b0 00 00 00        call     dword ptr [ecx + 0xb0]
004C37DA  8b 8d c4 04 00 00        mov      ecx, dword ptr [ebp + 0x4c4]
004C37E0  6a 00                    push     0
004C37E2  6a ff                    push     -1
004C37E4  55                       push     ebp
004C37E5  e8 c6 57 1f 00           call     0x6b8fb0
004C37EA  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37F0  85 c0                    test     eax, eax
004C37F2  75 0a                    jne      0x4c37fe
004C37F4  68 03 40 00 80           push     0x80004003
004C37F9  e8 42 21 2d 00           call     0x795940
004C37FE  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C3804  50                       push     eax
004C3805  8b 10                    mov      edx, dword ptr [eax]
004C3807  ff 92 b4 00 00 00        call     dword ptr [edx + 0xb4]
004C380D  8b 45 00                 mov      eax, dword ptr [ebp]
004C3810  6a 01                    push     1
004C3812  6a 00                    push     0
004C3814  8b cd                    mov      ecx, ebp
004C3816  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004C381C  8b 55 00                 mov      edx, dword ptr [ebp]
004C381F  6a 00                    push     0
004C3821  8b cd                    mov      ecx, ebp
004C3823  ff 92 70 03 00 00        call     dword ptr [edx + 0x370]
004C3829  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
004C382F  e8 bc 1a 03 00           call     0x4f52f0
004C3834  84 c0                    test     al, al
004C3836  75 71                    jne      0x4c38a9
004C3838  8b 45 00                 mov      eax, dword ptr [ebp]
004C383B  6a 00                    push     0
004C383D  6a 0b                    push     0xb
004C383F  8b cd                    mov      ecx, ebp
004C3841  ff 90 d0 01 00 00        call     dword ptr [eax + 0x1d0]
004C3847  a1 98 d2 a3 00           mov      eax, dword ptr [0xa3d298]
004C384C  85 c0                    test     eax, eax
004C384E  74 68                    je       0x4c38b8
004C3850  8d 4c 24 28              lea      ecx, [esp + 0x28]
004C3854  55                       push     ebp
004C3855  51                       push     ecx
004C3856  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
004C385C  e8 0f 7a 02 00           call     0x4eb270
004C3861  8b 00                    mov      eax, dword ptr [eax]
004C3863  66 3b 05 00 5f 86 00     cmp      ax, word ptr [0x865f00]
004C386A  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004C386E  75 0e                    jne      0x4c387e
004C3870  66 8b 54 24 16           mov      dx, word ptr [esp + 0x16]
004C3875  66 3b 15 02 5f 86 00     cmp      dx, word ptr [0x865f02]
004C387C  74 3a                    je       0x4c38b8
004C387E  8b 75 00                 mov      esi, dword ptr [ebp]
004C3881  8d 44 24 14              lea      eax, [esp + 0x14]
004C3885  6a 01                    push     1
004C3887  50                       push     eax
004C3888  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C388D  e8 de 47 08 00           call     0x548070
004C3892  50                       push     eax
004C3893  8b cd                    mov      ecx, ebp
004C3895  ff 96 10 04 00 00        call     dword ptr [esi + 0x410]
004C389B  5e                       pop      esi
004C389C  5d                       pop      ebp
004C389D  32 c0                    xor      al, al
004C389F  5b                       pop      ebx
004C38A0  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C38A6  c2 0c 00                 ret      0xc
004C38A9  8b 55 00                 mov      edx, dword ptr [ebp]
004C38AC  6a 00                    push     0
004C38AE  6a 05                    push     5
004C38B0  8b cd                    mov      ecx, ebp
004C38B2  ff 92 d0 01 00 00        call     dword ptr [edx + 0x1d0]
004C38B8  5e                       pop      esi
004C38B9  5d                       pop      ebp
004C38BA  32 c0                    xor      al, al
004C38BC  5b                       pop      ebx
004C38BD  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C38C3  c2 0c 00                 ret      0xc
