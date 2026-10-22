
sub_00703A95 0x00703AA9 size=352
00703AA9  85 ff                    test     edi, edi
00703AAB  0f 85 0b 01 00 00        jne      0x703bbc
00703AB1  8a 84 24 88 00 00 00     mov      al, byte ptr [esp + 0x88]
00703AB8  84 c0                    test     al, al
00703ABA  0f 85 ba 00 00 00        jne      0x703b7a
00703AC0  f6 44 24 12 3f           test     byte ptr [esp + 0x12], 0x3f
00703AC5  0f 84 f1 00 00 00        je       0x703bbc
00703ACB  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
00703ACF  84 c0                    test     al, al
00703AD1  0f 85 e0 00 00 00        jne      0x703bb7
00703AD7  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00703ADB  83 f8 ff                 cmp      eax, -1
00703ADE  74 14                    je       0x703af4
00703AE0  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
00703AE6  50                       push     eax
00703AE7  e8 14 1a de ff           call     0x4e5500
00703AEC  84 c0                    test     al, al
00703AEE  0f 85 c3 00 00 00        jne      0x703bb7
00703AF4  8b 8d ac 05 00 00        mov      ecx, dword ptr [ebp + 0x5ac]
00703AFA  8a 81 f3 0a 00 00        mov      al, byte ptr [ecx + 0xaf3]
00703B00  84 c0                    test     al, al
00703B02  0f 85 b4 00 00 00        jne      0x703bbc
00703B08  6a 11                    push     0x11
00703B0A  8b cd                    mov      ecx, ebp
00703B0C  e8 ff 3d fd ff           call     0x6d7910
00703B11  84 c0                    test     al, al
00703B13  0f 85 a3 00 00 00        jne      0x703bbc
00703B19  8b 95 ac 05 00 00        mov      edx, dword ptr [ebp + 0x5ac]
00703B1F  8a 82 a0 0a 00 00        mov      al, byte ptr [edx + 0xaa0]
00703B25  84 c0                    test     al, al
00703B27  75 40                    jne      0x703b69
00703B29  8b 45 00                 mov      eax, dword ptr [ebp]
00703B2C  6a 00                    push     0
00703B2E  8b cd                    mov      ecx, ebp
00703B30  ff 90 9c 03 00 00        call     dword ptr [eax + 0x39c]
00703B36  83 38 00                 cmp      dword ptr [eax], 0
00703B39  74 1f                    je       0x703b5a
00703B3B  8b 55 00                 mov      edx, dword ptr [ebp]
00703B3E  6a 00                    push     0
00703B40  8b cd                    mov      ecx, ebp
00703B42  ff 92 9c 03 00 00        call     dword ptr [edx + 0x39c]
00703B48  8b 00                    mov      eax, dword ptr [eax]
00703B4A  8b 88 a0 00 00 00        mov      ecx, dword ptr [eax + 0xa0]
00703B50  8a 81 75 02 00 00        mov      al, byte ptr [ecx + 0x275]
00703B56  84 c0                    test     al, al
00703B58  75 0f                    jne      0x703b69
00703B5A  5f                       pop      edi
00703B5B  5e                       pop      esi
00703B5C  5d                       pop      ebp
00703B5D  b8 07 00 00 00           mov      eax, 7
00703B62  5b                       pop      ebx
00703B63  83 c4 68                 add      esp, 0x68
00703B66  c2 14 00                 ret      0x14
00703B69  bf 05 00 00 00           mov      edi, 5
00703B6E  8b c7                    mov      eax, edi
00703B70  5f                       pop      edi
00703B71  5e                       pop      esi
00703B72  5d                       pop      ebp
00703B73  5b                       pop      ebx
00703B74  83 c4 68                 add      esp, 0x68
00703B77  c2 14 00                 ret      0x14
00703B7A  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
00703B7E  84 c0                    test     al, al
00703B80  74 3a                    je       0x703bbc
00703B82  6a 00                    push     0
00703B84  8b cb                    mov      ecx, ebx
00703B86  e8 a5 02 d7 ff           call     0x473e30
00703B8B  85 c0                    test     eax, eax
00703B8D  74 19                    je       0x703ba8
00703B8F  6a 00                    push     0
00703B91  8b cb                    mov      ecx, ebx
00703B93  e8 98 02 d7 ff           call     0x473e30
00703B98  8b 90 ac 05 00 00        mov      edx, dword ptr [eax + 0x5ac]
00703B9E  8a 82 fd 01 00 00        mov      al, byte ptr [edx + 0x1fd]
00703BA4  84 c0                    test     al, al
00703BA6  75 14                    jne      0x703bbc
00703BA8  5f                       pop      edi
00703BA9  5e                       pop      esi
00703BAA  5d                       pop      ebp
00703BAB  b8 02 00 00 00           mov      eax, 2
00703BB0  5b                       pop      ebx
00703BB1  83 c4 68                 add      esp, 0x68
00703BB4  c2 14 00                 ret      0x14
00703BB7  bf 02 00 00 00           mov      edi, 2
00703BBC  8b c7                    mov      eax, edi
00703BBE  5f                       pop      edi
00703BBF  5e                       pop      esi
00703BC0  5d                       pop      ebp
00703BC1  5b                       pop      ebx
00703BC2  83 c4 68                 add      esp, 0x68
00703BC5  c2 14 00                 ret      0x14
00703BC8  90                       nop      
00703BC9  90                       nop      
00703BCA  90                       nop      
00703BCB  90                       nop      
00703BCC  90                       nop      
00703BCD  90                       nop      
00703BCE  90                       nop      
00703BCF  90                       nop      
00703BD0  83 ec 14                 sub      esp, 0x14
00703BD3  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00703BD7  53                       push     ebx
00703BD8  8b 5c 24 1c              mov      ebx, dword ptr [esp + 0x1c]
00703BDC  56                       push     esi
00703BDD  57                       push     edi
00703BDE  50                       push     eax
00703BDF  8b f1                    mov      esi, ecx
00703BE1  53                       push     ebx
00703BE2  e8 59 8b dc ff           call     0x4cc740
00703BE7  8b f8                    mov      edi, eax
00703BE9  83 ff 08                 cmp      edi, 8
00703BEC  89 7c 24 24              mov      dword ptr [esp + 0x24], edi
00703BF0  75 09                    jne      0x703bfb
00703BF2  5f                       pop      edi
00703BF3  5e                       pop      esi
00703BF4  5b                       pop      ebx
00703BF5  83 c4 14                 add      esp, 0x14
00703BF8  c2 08 00                 ret      8
00703BFB  55                       push     ebp
00703BFC  6a ff                    push     -1
00703BFE  8b ce                    mov      ecx, esi
00703C00  e8 eb da fb ff           call     0x6c16f0
00703C05  85 c0                    test     eax, eax
