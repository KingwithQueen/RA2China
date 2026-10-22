
sub_0071F590 0x0071F590 size=816
0071F590  83 ec 20                 sub      esp, 0x20
0071F593  53                       push     ebx
0071F594  8b d9                    mov      ebx, ecx
0071F596  8b 0d 60 90 af 00        mov      ecx, dword ptr [0xaf9060]
0071F59C  56                       push     esi
0071F59D  8b 43 28                 mov      eax, dword ptr [ebx + 0x28]
0071F5A0  57                       push     edi
0071F5A1  8d 7b 28                 lea      edi, [ebx + 0x28]
0071F5A4  3b c1                    cmp      eax, ecx
0071F5A6  75 18                    jne      0x71f5c0
0071F5A8  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
0071F5AB  a1 64 90 af 00           mov      eax, dword ptr [0xaf9064]
0071F5B0  3b c8                    cmp      ecx, eax
0071F5B2  75 0c                    jne      0x71f5c0
0071F5B4  8b 57 08                 mov      edx, dword ptr [edi + 8]
0071F5B7  a1 68 90 af 00           mov      eax, dword ptr [0xaf9068]
0071F5BC  3b d0                    cmp      edx, eax
0071F5BE  74 08                    je       0x71f5c8
0071F5C0  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F5C3  57                       push     edi
0071F5C4  8b 01                    mov      eax, dword ptr [ecx]
0071F5C6  eb 28                    jmp      0x71f5f0
0071F5C8  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F5CB  8d 91 88 00 00 00        lea      edx, [ecx + 0x88]
0071F5D1  8b 81 88 00 00 00        mov      eax, dword ptr [ecx + 0x88]
0071F5D7  89 44 24 20              mov      dword ptr [esp + 0x20], eax
0071F5DB  8b 42 04                 mov      eax, dword ptr [edx + 4]
0071F5DE  89 44 24 24              mov      dword ptr [esp + 0x24], eax
0071F5E2  8b 52 08                 mov      edx, dword ptr [edx + 8]
0071F5E5  89 54 24 28              mov      dword ptr [esp + 0x28], edx
0071F5E9  8b 01                    mov      eax, dword ptr [ecx]
0071F5EB  8d 54 24 20              lea      edx, [esp + 0x20]
0071F5EF  52                       push     edx
0071F5F0  ff 90 ec 00 00 00        call     dword ptr [eax + 0xec]
0071F5F6  8b 74 24 30              mov      esi, dword ptr [esp + 0x30]
0071F5FA  c6 44 24 30 00           mov      byte ptr [esp + 0x30], 0
0071F5FF  8b c6                    mov      eax, esi
0071F601  8b 08                    mov      ecx, dword ptr [eax]
0071F603  89 4c 24 14              mov      dword ptr [esp + 0x14], ecx
0071F607  8b 0e                    mov      ecx, dword ptr [esi]
0071F609  8b 50 04                 mov      edx, dword ptr [eax + 4]
0071F60C  89 54 24 18              mov      dword ptr [esp + 0x18], edx
0071F610  8b 40 08                 mov      eax, dword ptr [eax + 8]
0071F613  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
0071F617  a1 60 90 af 00           mov      eax, dword ptr [0xaf9060]
0071F61C  3b c8                    cmp      ecx, eax
0071F61E  75 1d                    jne      0x71f63d
0071F620  8b 56 04                 mov      edx, dword ptr [esi + 4]
0071F623  a1 64 90 af 00           mov      eax, dword ptr [0xaf9064]
0071F628  3b d0                    cmp      edx, eax
0071F62A  75 11                    jne      0x71f63d
0071F62C  8b 46 08                 mov      eax, dword ptr [esi + 8]
0071F62F  8b 0d 68 90 af 00        mov      ecx, dword ptr [0xaf9068]
0071F635  3b c1                    cmp      eax, ecx
0071F637  0f 84 37 02 00 00        je       0x71f874
0071F63D  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F640  8b 11                    mov      edx, dword ptr [ecx]
0071F642  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
0071F648  83 f8 08                 cmp      eax, 8
0071F64B  74 44                    je       0x71f691
0071F64D  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F650  8b 01                    mov      eax, dword ptr [ecx]
0071F652  ff 90 6c 01 00 00        call     dword ptr [eax + 0x16c]
0071F658  83 f8 09                 cmp      eax, 9
0071F65B  74 34                    je       0x71f691
0071F65D  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F660  8b 11                    mov      edx, dword ptr [ecx]
0071F662  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
0071F668  83 f8 07                 cmp      eax, 7
0071F66B  74 24                    je       0x71f691
0071F66D  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F670  8b 01                    mov      eax, dword ptr [ecx]
0071F672  ff 90 6c 01 00 00        call     dword ptr [eax + 0x16c]
0071F678  83 f8 0b                 cmp      eax, 0xb
0071F67B  74 14                    je       0x71f691
0071F67D  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F680  8b 11                    mov      edx, dword ptr [ecx]
0071F682  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
0071F688  83 f8 19                 cmp      eax, 0x19
0071F68B  0f 85 f6 00 00 00        jne      0x71f787
0071F691  8b 43 0c                 mov      eax, dword ptr [ebx + 0xc]
0071F694  55                       push     ebp
0071F695  8b a8 94 04 00 00        mov      ebp, dword ptr [eax + 0x494]
0071F69B  85 ed                    test     ebp, ebp
0071F69D  74 56                    je       0x71f6f5
0071F69F  8b 55 00                 mov      edx, dword ptr [ebp]
0071F6A2  8b cd                    mov      ecx, ebp
0071F6A4  ff 52 2c                 call     dword ptr [edx + 0x2c]
0071F6A7  83 f8 01                 cmp      eax, 1
0071F6AA  75 49                    jne      0x71f6f5
0071F6AC  8b 06                    mov      eax, dword ptr [esi]
0071F6AE  8d 4c 24 14              lea      ecx, [esp + 0x14]
0071F6B2  99                       cdq      
0071F6B3  81 e2 ff 00 00 00        and      edx, 0xff
0071F6B9  51                       push     ecx
0071F6BA  03 c2                    add      eax, edx
0071F6BC  8b cd                    mov      ecx, ebp
0071F6BE  8b f8                    mov      edi, eax
0071F6C0  8b 46 04                 mov      eax, dword ptr [esi + 4]
0071F6C3  99                       cdq      
0071F6C4  81 e2 ff 00 00 00        and      edx, 0xff
0071F6CA  03 c2                    add      eax, edx
0071F6CC  c1 f8 08                 sar      eax, 8
0071F6CF  66 89 44 24 16           mov      word ptr [esp + 0x16], ax
0071F6D4  8b 45 00                 mov      eax, dword ptr [ebp]
0071F6D7  c1 ff 08                 sar      edi, 8
0071F6DA  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
0071F6E0  66 39 38                 cmp      word ptr [eax], di
0071F6E3  75 10                    jne      0x71f6f5
0071F6E5  66 8b 54 24 12           mov      dx, word ptr [esp + 0x12]
0071F6EA  66 39 50 02              cmp      word ptr [eax + 2], dx
0071F6EE  75 05                    jne      0x71f6f5
0071F6F0  c6 44 24 34 01           mov      byte ptr [esp + 0x34], 1
0071F6F5  8b 43 0c                 mov      eax, dword ptr [ebx + 0xc]
0071F6F8  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
0071F6FE  85 c9                    test     ecx, ecx
0071F700  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
0071F704  74 4c                    je       0x71f752
0071F706  8b 11                    mov      edx, dword ptr [ecx]
0071F708  ff 52 2c                 call     dword ptr [edx + 0x2c]
0071F70B  83 f8 02                 cmp      eax, 2
0071F70E  75 42                    jne      0x71f752
0071F710  8b 06                    mov      eax, dword ptr [esi]
0071F712  8b 4c 24 10              mov      ecx, dword ptr [esp + 0x10]
0071F716  99                       cdq      
0071F717  81 e2 ff 00 00 00        and      edx, 0xff
0071F71D  03 c2                    add      eax, edx
0071F71F  8b f8                    mov      edi, eax
0071F721  8b 46 04                 mov      eax, dword ptr [esi + 4]
0071F724  99                       cdq      
0071F725  81 e2 ff 00 00 00        and      edx, 0xff
0071F72B  03 c2                    add      eax, edx
0071F72D  8d 54 24 14              lea      edx, [esp + 0x14]
0071F731  8b e8                    mov      ebp, eax
0071F733  8b 01                    mov      eax, dword ptr [ecx]
0071F735  52                       push     edx
0071F736  c1 ff 08                 sar      edi, 8
0071F739  c1 fd 08                 sar      ebp, 8
0071F73C  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
0071F742  66 39 38                 cmp      word ptr [eax], di
0071F745  75 0b                    jne      0x71f752
0071F747  66 39 68 02              cmp      word ptr [eax + 2], bp
0071F74B  75 05                    jne      0x71f752
0071F74D  c6 44 24 34 01           mov      byte ptr [esp + 0x34], 1
0071F752  8b 43 0c                 mov      eax, dword ptr [ebx + 0xc]
0071F755  5d                       pop      ebp
0071F756  8b b8 94 04 00 00        mov      edi, dword ptr [eax + 0x494]
0071F75C  85 ff                    test     edi, edi
0071F75E  74 27                    je       0x71f787
0071F760  8b 17                    mov      edx, dword ptr [edi]
0071F762  8b cf                    mov      ecx, edi
0071F764  ff 52 2c                 call     dword ptr [edx + 0x2c]
0071F767  83 f8 06                 cmp      eax, 6
0071F76A  75 1b                    jne      0x71f787
0071F76C  56                       push     esi
0071F76D  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F772  e8 89 88 e2 ff           call     0x548000
0071F777  8b c8                    mov      ecx, eax
0071F779  e8 32 20 d5 ff           call     0x4717b0
0071F77E  3b c7                    cmp      eax, edi
0071F780  75 05                    jne      0x71f787
0071F782  c6 44 24 30 01           mov      byte ptr [esp + 0x30], 1
0071F787  8d 44 24 14              lea      eax, [esp + 0x14]
0071F78B  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F790  50                       push     eax
0071F791  e8 6a 88 e2 ff           call     0x548000
0071F796  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
0071F79C  f6 c5 01                 test     ch, 1
0071F79F  74 3d                    je       0x71f7de
0071F7A1  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F7A4  81 c1 88 00 00 00        add      ecx, 0x88
0071F7AA  8b 11                    mov      edx, dword ptr [ecx]
0071F7AC  89 54 24 20              mov      dword ptr [esp + 0x20], edx
0071F7B0  8b 41 04                 mov      eax, dword ptr [ecx + 4]
0071F7B3  89 44 24 24              mov      dword ptr [esp + 0x24], eax
0071F7B7  8b 71 08                 mov      esi, dword ptr [ecx + 8]
0071F7BA  8d 4c 24 14              lea      ecx, [esp + 0x14]
0071F7BE  51                       push     ecx
0071F7BF  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F7C4  e8 b7 aa e3 ff           call     0x55a280
0071F7C9  8b d0                    mov      edx, eax
0071F7CB  a1 98 90 af 00           mov      eax, dword ptr [0xaf9098]
0071F7D0  c6 44 24 0c 01           mov      byte ptr [esp + 0xc], 1
0071F7D5  8d 04 40                 lea      eax, [eax + eax*2]
0071F7D8  03 d0                    add      edx, eax
0071F7DA  3b f2                    cmp      esi, edx
0071F7DC  7f 05                    jg       0x71f7e3
0071F7DE  c6 44 24 0c 00           mov      byte ptr [esp + 0xc], 0
0071F7E3  8b 4c 24 0c              mov      ecx, dword ptr [esp + 0xc]
0071F7E7  8b 54 24 30              mov      edx, dword ptr [esp + 0x30]
0071F7EB  51                       push     ecx
0071F7EC  8d 44 24 18              lea      eax, [esp + 0x18]
0071F7F0  52                       push     edx
0071F7F1  8d 4c 24 28              lea      ecx, [esp + 0x28]
0071F7F5  50                       push     eax
0071F7F6  8d 54 24 20              lea      edx, [esp + 0x20]
0071F7FA  51                       push     ecx
0071F7FB  52                       push     edx
0071F7FC  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F801  e8 fa 87 e2 ff           call     0x548000
0071F806  8b c8                    mov      ecx, eax
0071F808  e8 a3 6c d5 ff           call     0x4764b0
0071F80D  8b 10                    mov      edx, dword ptr [eax]
0071F80F  8d 7b 28                 lea      edi, [ebx + 0x28]
0071F812  8b cf                    mov      ecx, edi
0071F814  89 11                    mov      dword ptr [ecx], edx
0071F816  8b 50 04                 mov      edx, dword ptr [eax + 4]
0071F819  89 51 04                 mov      dword ptr [ecx + 4], edx
0071F81C  8b 40 08                 mov      eax, dword ptr [eax + 8]
0071F81F  89 41 08                 mov      dword ptr [ecx + 8], eax
0071F822  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
0071F825  51                       push     ecx
0071F826  57                       push     edi
0071F827  b9 e0 24 83 00           mov      ecx, 0x8324e0
0071F82C  e8 cf 87 e2 ff           call     0x548000
0071F831  8b c8                    mov      ecx, eax
0071F833  e8 88 74 d5 ff           call     0x476cc0
0071F838  84 c0                    test     al, al
0071F83A  75 4a                    jne      0x71f886
0071F83C  8b 43 0c                 mov      eax, dword ptr [ebx + 0xc]
0071F83F  8a 48 76                 mov      cl, byte ptr [eax + 0x76]
0071F842  84 c9                    test     cl, cl
0071F844  75 40                    jne      0x71f886
0071F846  8b 0d 60 90 af 00        mov      ecx, dword ptr [0xaf9060]
0071F84C  8b d7                    mov      edx, edi
0071F84E  89 0a                    mov      dword ptr [edx], ecx
0071F850  8b 0d 64 90 af 00        mov      ecx, dword ptr [0xaf9064]
0071F856  89 4a 04                 mov      dword ptr [edx + 4], ecx
0071F859  8b 0d 68 90 af 00        mov      ecx, dword ptr [0xaf9068]
0071F85F  89 4a 08                 mov      dword ptr [edx + 8], ecx
0071F862  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
0071F865  84 c9                    test     cl, cl
0071F867  75 1d                    jne      0x71f886
0071F869  5f                       pop      edi
0071F86A  5e                       pop      esi
0071F86B  32 c0                    xor      al, al
0071F86D  5b                       pop      ebx
0071F86E  83 c4 20                 add      esp, 0x20
0071F871  c2 04 00                 ret      4
0071F874  8b 06                    mov      eax, dword ptr [esi]
0071F876  8b d7                    mov      edx, edi
0071F878  89 02                    mov      dword ptr [edx], eax
0071F87A  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
0071F87D  89 4a 04                 mov      dword ptr [edx + 4], ecx
0071F880  8b 46 08                 mov      eax, dword ptr [esi + 8]
0071F883  89 42 08                 mov      dword ptr [edx + 8], eax
0071F886  8b 0f                    mov      ecx, dword ptr [edi]
0071F888  a1 60 90 af 00           mov      eax, dword ptr [0xaf9060]
0071F88D  3b c8                    cmp      ecx, eax
0071F88F  75 19                    jne      0x71f8aa
0071F891  8b 57 04                 mov      edx, dword ptr [edi + 4]
0071F894  a1 64 90 af 00           mov      eax, dword ptr [0xaf9064]
0071F899  3b d0                    cmp      edx, eax
0071F89B  75 0d                    jne      0x71f8aa
0071F89D  8b 47 08                 mov      eax, dword ptr [edi + 8]
0071F8A0  8b 0d 68 90 af 00        mov      ecx, dword ptr [0xaf9068]
0071F8A6  3b c1                    cmp      eax, ecx
0071F8A8  74 19                    je       0x71f8c3
0071F8AA  8b 5b 0c                 mov      ebx, dword ptr [ebx + 0xc]
0071F8AD  57                       push     edi
0071F8AE  8b cb                    mov      ecx, ebx
0071F8B0  8b 13                    mov      edx, dword ptr [ebx]
0071F8B2  ff 92 e8 00 00 00        call     dword ptr [edx + 0xe8]
0071F8B8  5f                       pop      edi
0071F8B9  5e                       pop      esi
0071F8BA  b0 01                    mov      al, 1
0071F8BC  5b                       pop      ebx
0071F8BD  83 c4 20                 add      esp, 0x20
