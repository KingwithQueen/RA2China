
sub_004C3000 0x004C3000 size=149
004C3000  b8 9c 1f 00 00           mov      eax, 0x1f9c
004C3005  e8 46 08 2c 00           call     0x783850
004C300A  8b 84 24 a4 1f 00 00     mov      eax, dword ptr [esp + 0x1fa4]
004C3011  53                       push     ebx
004C3012  55                       push     ebp
004C3013  56                       push     esi
004C3014  85 c0                    test     eax, eax
004C3016  8b e9                    mov      ebp, ecx
004C3018  75 0a                    jne      0x4c3024
004C301A  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
004C3024  0f bf 84 24 ac 1f 00 00  movsx    eax, word ptr [esp + 0x1fac]
004C302C  0f bf 8c 24 ae 1f 00 00  movsx    ecx, word ptr [esp + 0x1fae]
004C3034  8b 55 00                 mov      edx, dword ptr [ebp]
004C3037  c7 44 24 20 00 00 00 00  mov      dword ptr [esp + 0x20], 0
004C303F  c1 e0 08                 shl      eax, 8
004C3042  05 80 00 00 00           add      eax, 0x80
004C3047  c1 e1 08                 shl      ecx, 8
004C304A  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004C304E  81 c1 80 00 00 00        add      ecx, 0x80
004C3054  8d 44 24 18              lea      eax, [esp + 0x18]
004C3058  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
004C305C  50                       push     eax
004C305D  8b cd                    mov      ecx, ebp
004C305F  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004C3065  84 c0                    test     al, al
004C3067  75 16                    jne      0x4c307f
004C3069  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
004C3073  5e                       pop      esi
004C3074  5d                       pop      ebp
004C3075  5b                       pop      ebx
004C3076  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C307C  c2 0c 00                 ret      0xc
004C307F  0f bf b4 24 ac 1f 00 00  movsx    esi, word ptr [esp + 0x1fac]
004C3087  8b 55 00                 mov      edx, dword ptr [ebp]
004C308A  57                       push     edi
004C308B  0f bf bc 24 b2 1f 00 00  movsx    edi, word ptr [esp + 0x1fb2]
