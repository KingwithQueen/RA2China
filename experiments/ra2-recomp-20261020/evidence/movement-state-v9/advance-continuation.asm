
sub_004A1ACD 0x004A1B60 size=1069
004A1B60  8b 44 24 44              mov      eax, dword ptr [esp + 0x44]
004A1B64  83 f8 08                 cmp      eax, 8
004A1B67  0f 84 20 04 00 00        je       0x4a1f8d
004A1B6D  83 f8 ff                 cmp      eax, -1
004A1B70  0f 84 17 04 00 00        je       0x4a1f8d
004A1B76  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
004A1B7A  84 c0                    test     al, al
004A1B7C  0f 84 0b 04 00 00        je       0x4a1f8d
004A1B82  8b 4c 24 58              mov      ecx, dword ptr [esp + 0x58]
004A1B86  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A1B89  39 81 a4 00 7a 00        cmp      dword ptr [ecx + 0x7a00a4], eax
004A1B8F  0f 85 f8 03 00 00        jne      0x4a1f8d
004A1B95  85 c0                    test     eax, eax
004A1B97  0f 84 f0 03 00 00        je       0x4a1f8d
004A1B9D  8b 84 24 a8 00 00 00     mov      eax, dword ptr [esp + 0xa8]
004A1BA4  33 d2                    xor      edx, edx
004A1BA6  8a 70 04                 mov      dh, byte ptr [eax + 4]
004A1BA9  66 89 54 24 6c           mov      word ptr [esp + 0x6c], dx
004A1BAE  8b 54 24 44              mov      edx, dword ptr [esp + 0x44]
004A1BB2  8b 4c 24 6c              mov      ecx, dword ptr [esp + 0x6c]
004A1BB6  c1 e9 0c                 shr      ecx, 0xc
004A1BB9  41                       inc      ecx
004A1BBA  d1 e9                    shr      ecx, 1
004A1BBC  83 e1 07                 and      ecx, 7
004A1BBF  8d 04 ca                 lea      eax, [edx + ecx*8]
004A1BC2  89 44 24 40              mov      dword ptr [esp + 0x40], eax
004A1BC6  8d 04 40                 lea      eax, [eax + eax*2]
004A1BC9  8d 1c 85 80 01 7a 00     lea      ebx, [eax*4 + 0x7a0180]
004A1BD0  8a 04 85 80 01 7a 00     mov      al, byte ptr [eax*4 + 0x7a0180]
004A1BD7  84 c0                    test     al, al
004A1BD9  0f 84 ae 03 00 00        je       0x4a1f8d
004A1BDF  0f be c8                 movsx    ecx, al
004A1BE2  c1 e1 04                 shl      ecx, 4
004A1BE5  8b 81 a8 00 7a 00        mov      eax, dword ptr [ecx + 0x7a00a8]
004A1BEB  85 c0                    test     eax, eax
004A1BED  0f 84 9a 03 00 00        je       0x4a1f8d
004A1BF3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1BF6  8d 75 40                 lea      esi, [ebp + 0x40]
004A1BF9  6a 01                    push     1
004A1BFB  6a 00                    push     0
004A1BFD  8b 91 68 04 00 00        mov      edx, dword ptr [ecx + 0x468]
004A1C03  8b 81 6c 04 00 00        mov      eax, dword ptr [ecx + 0x46c]
004A1C09  89 54 24 7c              mov      dword ptr [esp + 0x7c], edx
004A1C0D  8b 54 24 4c              mov      edx, dword ptr [esp + 0x4c]
004A1C11  83 e2 07                 and      edx, 7
004A1C14  89 84 24 80 00 00 00     mov      dword ptr [esp + 0x80], eax
004A1C1B  8b 06                    mov      eax, dword ptr [esi]
004A1C1D  8b 3c d5 c0 1a 85 00     mov      edi, dword ptr [edx*8 + 0x851ac0]
004A1C24  8d 14 d5 c0 1a 85 00     lea      edx, [edx*8 + 0x851ac0]
004A1C2B  03 c7                    add      eax, edi
004A1C2D  8b 7a 04                 mov      edi, dword ptr [edx + 4]
004A1C30  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A1C33  03 fa                    add      edi, edx
004A1C35  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A1C38  89 44 24 20              mov      dword ptr [esp + 0x20], eax
004A1C3C  89 54 24 28              mov      dword ptr [esp + 0x28], edx
004A1C40  99                       cdq      
004A1C41  81 e2 ff 00 00 00        and      edx, 0xff
004A1C47  89 7c 24 24              mov      dword ptr [esp + 0x24], edi
004A1C4B  03 c2                    add      eax, edx
004A1C4D  c1 f8 08                 sar      eax, 8
004A1C50  66 89 84 24 9c 00 00 00  mov      word ptr [esp + 0x9c], ax
004A1C58  8b c7                    mov      eax, edi
004A1C5A  99                       cdq      
004A1C5B  81 e2 ff 00 00 00        and      edx, 0xff
004A1C61  03 c2                    add      eax, edx
004A1C63  c1 f8 08                 sar      eax, 8
004A1C66  66 89 84 24 9e 00 00 00  mov      word ptr [esp + 0x9e], ax
004A1C6E  8b 84 24 9c 00 00 00     mov      eax, dword ptr [esp + 0x9c]
004A1C75  89 44 24 3c              mov      dword ptr [esp + 0x3c], eax
004A1C79  8b 39                    mov      edi, dword ptr [ecx]
004A1C7B  e8 50 2b 13 00           call     0x5d47d0
004A1C80  8b 4c 24 4c              mov      ecx, dword ptr [esp + 0x4c]
004A1C84  50                       push     eax
004A1C85  8d 54 24 40              lea      edx, [esp + 0x40]
004A1C89  51                       push     ecx
004A1C8A  52                       push     edx
004A1C8B  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1C90  e8 db 63 0a 00           call     0x548070
004A1C95  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1C98  50                       push     eax
004A1C99  ff 97 94 01 00 00        call     dword ptr [edi + 0x194]
004A1C9F  83 f8 06                 cmp      eax, 6
004A1CA2  0f 87 e5 02 00 00        ja       0x4a1f8d
004A1CA8  ff 24 85 4c 26 4a 00     jmp      dword ptr [eax*4 + 0x4a264c]
004A1CAF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1CB2  8b 01                    mov      eax, dword ptr [ecx]
004A1CB4  ff 50 2c                 call     dword ptr [eax + 0x2c]
004A1CB7  83 f8 01                 cmp      eax, 1
004A1CBA  75 17                    jne      0x4a1cd3
004A1CBC  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1CBF  8b 91 ac 05 00 00        mov      edx, dword ptr [ecx + 0x5ac]
004A1CC5  8a 82 a4 0b 00 00        mov      al, byte ptr [edx + 0xba4]
004A1CCB  84 c0                    test     al, al
004A1CCD  0f 84 ba 02 00 00        je       0x4a1f8d
004A1CD3  8b 44 24 40              mov      eax, dword ptr [esp + 0x40]
004A1CD7  c6 45 60 00              mov      byte ptr [ebp + 0x60], 0
004A1CDB  89 45 58                 mov      dword ptr [ebp + 0x58], eax
004A1CDE  89 9c 24 a8 00 00 00     mov      dword ptr [esp + 0xa8], ebx
004A1CE5  0f be 03                 movsx    eax, byte ptr [ebx]
004A1CE8  c1 e0 04                 shl      eax, 4
004A1CEB  89 44 24 58              mov      dword ptr [esp + 0x58], eax
004A1CEF  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
004A1CF4  8b 88 a8 00 7a 00        mov      ecx, dword ptr [eax + 0x7a00a8]
004A1CFA  49                       dec      ecx
004A1CFB  89 4d 5c                 mov      dword ptr [ebp + 0x5c], ecx
004A1CFE  8b 90 a0 00 7a 00        mov      edx, dword ptr [eax + 0x7a00a0]
004A1D04  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A1D09  8b 0e                    mov      ecx, dword ptr [esi]
004A1D0B  3b c8                    cmp      ecx, eax
004A1D0D  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A1D11  75 1a                    jne      0x4a1d2d
004A1D13  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A1D16  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1D1C  3b ca                    cmp      ecx, edx
004A1D1E  75 0d                    jne      0x4a1d2d
004A1D20  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A1D23  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A1D29  3b d1                    cmp      edx, ecx
004A1D2B  74 19                    je       0x4a1d46
004A1D2D  8b ce                    mov      ecx, esi
004A1D2F  89 01                    mov      dword ptr [ecx], eax
004A1D31  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1D37  89 51 04                 mov      dword ptr [ecx + 4], edx
004A1D3A  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A1D3F  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1D43  89 41 08                 mov      dword ptr [ecx + 8], eax
004A1D46  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1D49  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A1D4D  6a 02                    push     2
004A1D4F  8b 11                    mov      edx, dword ptr [ecx]
004A1D51  ff 92 74 01 00 00        call     dword ptr [edx + 0x174]
004A1D57  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1D5A  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1D5E  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A1D61  84 c9                    test     cl, cl
004A1D63  0f 84 d1 08 00 00        je       0x4a263a
004A1D69  8a 48 76                 mov      cl, byte ptr [eax + 0x76]
004A1D6C  84 c9                    test     cl, cl
004A1D6E  0f 85 c6 08 00 00        jne      0x4a263a
004A1D74  8a 48 7a                 mov      cl, byte ptr [eax + 0x7a]
004A1D77  84 c9                    test     cl, cl
004A1D79  0f 85 bb 08 00 00        jne      0x4a263a
004A1D7F  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A1D85  8b 0e                    mov      ecx, dword ptr [esi]
004A1D87  3b ca                    cmp      ecx, edx
004A1D89  75 1a                    jne      0x4a1da5
004A1D8B  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A1D8E  8b 3d 9c 29 85 00        mov      edi, dword ptr [0x85299c]
004A1D94  3b cf                    cmp      ecx, edi
004A1D96  75 0d                    jne      0x4a1da5
004A1D98  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A1D9B  8b 3d a0 29 85 00        mov      edi, dword ptr [0x8529a0]
004A1DA1  3b cf                    cmp      ecx, edi
004A1DA3  74 20                    je       0x4a1dc5
004A1DA5  8b ce                    mov      ecx, esi
004A1DA7  89 11                    mov      dword ptr [ecx], edx
004A1DA9  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1DAF  89 51 04                 mov      dword ptr [ecx + 4], edx
004A1DB2  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A1DB8  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1DBC  89 51 08                 mov      dword ptr [ecx + 8], edx
004A1DBF  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A1DC5  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004A1DC9  8b 7c 24 1c              mov      edi, dword ptr [esp + 0x1c]
004A1DCD  3b ca                    cmp      ecx, edx
004A1DCF  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004A1DD3  75 14                    jne      0x4a1de9
004A1DD5  3b 3d 9c 29 85 00        cmp      edi, dword ptr [0x85299c]
004A1DDB  75 0c                    jne      0x4a1de9
004A1DDD  3b 15 a0 29 85 00        cmp      edx, dword ptr [0x8529a0]
004A1DE3  0f 84 a4 01 00 00        je       0x4a1f8d
004A1DE9  8b de                    mov      ebx, esi
004A1DEB  50                       push     eax
004A1DEC  8d 44 24 1c              lea      eax, [esp + 0x1c]
004A1DF0  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A1DF4  89 0b                    mov      dword ptr [ebx], ecx
004A1DF6  50                       push     eax
004A1DF7  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1DFC  89 7b 04                 mov      dword ptr [ebx + 4], edi
004A1DFF  89 53 08                 mov      dword ptr [ebx + 8], edx
004A1E02  e8 f9 61 0a 00           call     0x548000
004A1E07  8b c8                    mov      ecx, eax
004A1E09  e8 b2 4e fd ff           call     0x476cc0
004A1E0E  84 c0                    test     al, al
004A1E10  74 55                    je       0x4a1e67
004A1E12  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E15  8a 41 76                 mov      al, byte ptr [ecx + 0x76]
004A1E18  84 c0                    test     al, al
004A1E1A  75 4b                    jne      0x4a1e67
004A1E1C  8d 54 24 18              lea      edx, [esp + 0x18]
004A1E20  6a 01                    push     1
004A1E22  52                       push     edx
004A1E23  8b cd                    mov      ecx, ebp
004A1E25  e8 96 ed ff ff           call     0x4a0bc0
004A1E2A  8b 44 24 78              mov      eax, dword ptr [esp + 0x78]
004A1E2E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E31  50                       push     eax
004A1E32  8b 44 24 78              mov      eax, dword ptr [esp + 0x78]
004A1E36  8b 11                    mov      edx, dword ptr [ecx]
004A1E38  50                       push     eax
004A1E39  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A1E3F  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1E42  b9 17 00 00 00           mov      ecx, 0x17
004A1E47  8d b0 d4 04 00 00        lea      esi, [eax + 0x4d4]
004A1E4D  8d b8 d0 04 00 00        lea      edi, [eax + 0x4d0]
004A1E53  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004A1E55  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E58  c7 81 2c 05 00 00 ff ff ff ff mov      dword ptr [ecx + 0x52c], 0xffffffff
004A1E62  e9 26 01 00 00           jmp      0x4a1f8d
004A1E67  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1E6A  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A1E6D  84 c9                    test     cl, cl
004A1E6F  0f 84 18 01 00 00        je       0x4a1f8d
004A1E75  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A1E7B  89 0e                    mov      dword ptr [esi], ecx
004A1E7D  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1E83  89 56 04                 mov      dword ptr [esi + 4], edx
004A1E86  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A1E8B  89 46 08                 mov      dword ptr [esi + 8], eax
004A1E8E  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1E92  e9 f6 00 00 00           jmp      0x4a1f8d
004A1E97  8d 54 24 18              lea      edx, [esp + 0x18]
004A1E9B  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1EA0  52                       push     edx
004A1EA1  e8 5a 61 0a 00           call     0x548000
004A1EA6  8b c8                    mov      ecx, eax
004A1EA8  e8 93 68 fd ff           call     0x478740
004A1EAD  e9 db 00 00 00           jmp      0x4a1f8d
004A1EB2  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004A1EB6  8d 4c 24 40              lea      ecx, [esp + 0x40]
004A1EBA  99                       cdq      
004A1EBB  81 e2 ff 00 00 00        and      edx, 0xff
004A1EC1  51                       push     ecx
004A1EC2  03 c2                    add      eax, edx
004A1EC4  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1EC9  c1 f8 08                 sar      eax, 8
004A1ECC  66 89 84 24 a0 00 00 00  mov      word ptr [esp + 0xa0], ax
004A1ED4  8b 44 24 20              mov      eax, dword ptr [esp + 0x20]
004A1ED8  99                       cdq      
004A1ED9  81 e2 ff 00 00 00        and      edx, 0xff
004A1EDF  03 c2                    add      eax, edx
004A1EE1  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A1EE4  c1 f8 08                 sar      eax, 8
004A1EE7  66 89 84 24 a2 00 00 00  mov      word ptr [esp + 0xa2], ax
004A1EEF  8b 84 24 a0 00 00 00     mov      eax, dword ptr [esp + 0xa0]
004A1EF6  52                       push     edx
004A1EF7  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A1EFB  e8 d0 8d 0b 00           call     0x55acd0
004A1F00  e9 88 00 00 00           jmp      0x4a1f8d
004A1F05  8d 44 24 18              lea      eax, [esp + 0x18]
004A1F09  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F0E  50                       push     eax
004A1F0F  e8 ec 60 0a 00           call     0x548000
004A1F14  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004A1F1A  f6 c5 01                 test     ch, 1
004A1F1D  74 49                    je       0x4a1f68
004A1F1F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1F22  81 c1 88 00 00 00        add      ecx, 0x88
004A1F28  8b 11                    mov      edx, dword ptr [ecx]
004A1F2A  89 54 24 5c              mov      dword ptr [esp + 0x5c], edx
004A1F2E  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A1F31  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004A1F35  8b 79 08                 mov      edi, dword ptr [ecx + 8]
004A1F38  8d 4c 24 18              lea      ecx, [esp + 0x18]
004A1F3C  51                       push     ecx
004A1F3D  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F42  e8 b9 60 0a 00           call     0x548000
004A1F47  0f be 88 1b 01 00 00     movsx    ecx, byte ptr [eax + 0x11b]
004A1F4E  8b c7                    mov      eax, edi
004A1F50  c6 44 24 14 01           mov      byte ptr [esp + 0x14], 1
004A1F55  99                       cdq      
004A1F56  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A1F5C  2b c1                    sub      eax, ecx
004A1F5E  99                       cdq      
004A1F5F  33 c2                    xor      eax, edx
004A1F61  2b c2                    sub      eax, edx
004A1F63  83 f8 02                 cmp      eax, 2
004A1F66  7f 05                    jg       0x4a1f6d
004A1F68  c6 44 24 14 00           mov      byte ptr [esp + 0x14], 0
004A1F6D  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004A1F71  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F76  52                       push     edx
004A1F77  6a 01                    push     1
004A1F79  6a 01                    push     1
004A1F7B  68 98 29 85 00           push     0x852998
004A1F80  56                       push     esi
004A1F81  e8 7a 60 0a 00           call     0x548000
004A1F86  8b c8                    mov      ecx, eax
004A1F88  e8 93 49 fd ff           call     0x476920
