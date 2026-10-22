
sub_004C8030 0x004C8030 size=414
004C8030  8b 44 24 04              mov      eax, dword ptr [esp + 4]
004C8034  83 ec 1c                 sub      esp, 0x1c
004C8037  53                       push     ebx
004C8038  55                       push     ebp
004C8039  8b e9                    mov      ebp, ecx
004C803B  33 db                    xor      ebx, ebx
004C803D  56                       push     esi
004C803E  3b c3                    cmp      eax, ebx
004C8040  57                       push     edi
004C8041  89 9d 90 04 00 00        mov      dword ptr [ebp + 0x490], ebx
004C8047  89 85 94 04 00 00        mov      dword ptr [ebp + 0x494], eax
004C804D  0f 84 27 01 00 00        je       0x4c817a
004C8053  8b 8d 5c 02 00 00        mov      ecx, dword ptr [ebp + 0x25c]
004C8059  3b cb                    cmp      ecx, ebx
004C805B  74 0e                    je       0x4c806b
004C805D  8b 01                    mov      eax, dword ptr [ecx]
004C805F  ff 90 f0 00 00 00        call     dword ptr [eax + 0xf0]
004C8065  89 9d 5c 02 00 00        mov      dword ptr [ebp + 0x25c], ebx
004C806B  8b 8d 64 05 00 00        mov      ecx, dword ptr [ebp + 0x564]
004C8071  8d 85 64 05 00 00        lea      eax, [ebp + 0x564]
004C8077  3b cb                    cmp      ecx, ebx
004C8079  89 5c 24 30              mov      dword ptr [esp + 0x30], ebx
004C807D  74 23                    je       0x4c80a2
004C807F  50                       push     eax
004C8080  8d 4c 24 34              lea      ecx, [esp + 0x34]
004C8084  e8 67 cb f8 ff           call     0x454bf0
004C8089  3b c3                    cmp      eax, ebx
004C808B  7d 0d                    jge      0x4c809a
004C808D  3d 02 40 00 80           cmp      eax, 0x80004002
004C8092  74 06                    je       0x4c809a
004C8094  50                       push     eax
004C8095  e8 a6 d8 2c 00           call     0x795940
004C809A  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004C809E  3b c3                    cmp      eax, ebx
004C80A0  75 0e                    jne      0x4c80b0
004C80A2  68 03 40 00 80           push     0x80004003
004C80A7  e8 94 d8 2c 00           call     0x795940
004C80AC  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004C80B0  8b 08                    mov      ecx, dword ptr [eax]
004C80B2  8d 54 24 1c              lea      edx, [esp + 0x1c]
004C80B6  52                       push     edx
004C80B7  50                       push     eax
004C80B8  ff 51 0c                 call     dword ptr [ecx + 0xc]
004C80BB  b9 04 00 00 00           mov      ecx, 4
004C80C0  bf 80 1f 7a 00           mov      edi, 0x7a1f80
004C80C5  8d 74 24 1c              lea      esi, [esp + 0x1c]
004C80C9  33 c0                    xor      eax, eax
004C80CB  f3 a7                    repe cmpsd dword ptr [esi], dword ptr es:[edi]
004C80CD  75 40                    jne      0x4c810f
004C80CF  8b 95 30 05 00 00        mov      edx, dword ptr [ebp + 0x530]
004C80D5  8b 85 38 05 00 00        mov      eax, dword ptr [ebp + 0x538]
004C80DB  8b 35 2c 0d a4 00        mov      esi, dword ptr [0xa40d2c]
004C80E1  83 fa ff                 cmp      edx, -1
004C80E4  74 0a                    je       0x4c80f0
004C80E6  8b ce                    mov      ecx, esi
004C80E8  2b ca                    sub      ecx, edx
004C80EA  3b c8                    cmp      ecx, eax
004C80EC  7d 06                    jge      0x4c80f4
004C80EE  2b c1                    sub      eax, ecx
004C80F0  3b c3                    cmp      eax, ebx
004C80F2  75 1b                    jne      0x4c810f
004C80F4  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
004C80F8  b8 01 00 00 00           mov      eax, 1
004C80FD  89 b5 30 05 00 00        mov      dword ptr [ebp + 0x530], esi
004C8103  89 8d 34 05 00 00        mov      dword ptr [ebp + 0x534], ecx
004C8109  89 85 38 05 00 00        mov      dword ptr [ebp + 0x538], eax
004C810F  8a 85 98 05 00 00        mov      al, byte ptr [ebp + 0x598]
004C8115  84 c0                    test     al, al
004C8117  74 09                    je       0x4c8122
004C8119  c6 85 98 05 00 00 00     mov      byte ptr [ebp + 0x598], 0
004C8120  eb 48                    jmp      0x4c816a
004C8122  8b 8d 94 04 00 00        mov      ecx, dword ptr [ebp + 0x494]
004C8128  8d 44 24 10              lea      eax, [esp + 0x10]
004C812C  55                       push     ebp
004C812D  50                       push     eax
004C812E  8b 11                    mov      edx, dword ptr [ecx]
004C8130  ff 52 4c                 call     dword ptr [edx + 0x4c]
004C8133  8b 30                    mov      esi, dword ptr [eax]
004C8135  8b 78 04                 mov      edi, dword ptr [eax + 4]
004C8138  8b 58 08                 mov      ebx, dword ptr [eax + 8]
004C813B  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C8141  85 c0                    test     eax, eax
004C8143  75 0a                    jne      0x4c814f
004C8145  68 03 40 00 80           push     0x80004003
004C814A  e8 f1 d7 2c 00           call     0x795940
004C814F  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C8155  83 ec 0c                 sub      esp, 0xc
004C8158  8b d4                    mov      edx, esp
004C815A  8b 08                    mov      ecx, dword ptr [eax]
004C815C  50                       push     eax
004C815D  89 32                    mov      dword ptr [edx], esi
004C815F  89 7a 04                 mov      dword ptr [edx + 4], edi
004C8162  89 5a 08                 mov      dword ptr [edx + 8], ebx
004C8165  ff 51 44                 call     dword ptr [ecx + 0x44]
004C8168  33 db                    xor      ebx, ebx
004C816A  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004C816E  3b c3                    cmp      eax, ebx
004C8170  74 58                    je       0x4c81ca
004C8172  8b 08                    mov      ecx, dword ptr [eax]
004C8174  50                       push     eax
004C8175  ff 51 08                 call     dword ptr [ecx + 8]
004C8178  eb 50                    jmp      0x4c81ca
004C817A  8b 55 00                 mov      edx, dword ptr [ebp]
004C817D  8b cd                    mov      ecx, ebp
004C817F  ff 52 2c                 call     dword ptr [edx + 0x2c]
004C8182  83 f8 02                 cmp      eax, 2
004C8185  75 1f                    jne      0x4c81a6
004C8187  8b 8d 98 00 00 00        mov      ecx, dword ptr [ebp + 0x98]
004C818D  b8 01 00 00 00           mov      eax, 1
004C8192  3b c8                    cmp      ecx, eax
004C8194  74 08                    je       0x4c819e
004C8196  39 85 a0 00 00 00        cmp      dword ptr [ebp + 0xa0], eax
004C819C  75 08                    jne      0x4c81a6
004C819E  39 9d 28 02 00 00        cmp      dword ptr [ebp + 0x228], ebx
004C81A4  75 24                    jne      0x4c81ca
004C81A6  39 9d 64 05 00 00        cmp      dword ptr [ebp + 0x564], ebx
004C81AC  75 0a                    jne      0x4c81b8
004C81AE  68 03 40 00 80           push     0x80004003
004C81B3  e8 88 d7 2c 00           call     0x795940
004C81B8  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C81BE  50                       push     eax
004C81BF  8b 08                    mov      ecx, dword ptr [eax]
004C81C1  ff 51 48                 call     dword ptr [ecx + 0x48]
004C81C4  89 9d 94 04 00 00        mov      dword ptr [ebp + 0x494], ebx
