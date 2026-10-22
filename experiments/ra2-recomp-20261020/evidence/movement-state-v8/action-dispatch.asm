
sub_006AD640 0x006AD640 size=592
006AD640  83 ec 0c                 sub      esp, 0xc
006AD643  53                       push     ebx
006AD644  55                       push     ebp
006AD645  56                       push     esi
006AD646  8b f1                    mov      esi, ecx
006AD648  57                       push     edi
006AD649  8b 4e 2c                 mov      ecx, dword ptr [esi + 0x2c]
006AD64C  e8 5f 54 00 00           call     0x6b2ab0
006AD651  8b 4e 74                 mov      ecx, dword ptr [esi + 0x74]
006AD654  33 ff                    xor      edi, edi
006AD656  33 db                    xor      ebx, ebx
006AD658  33 ed                    xor      ebp, ebp
006AD65A  83 f8 2b                 cmp      eax, 0x2b
006AD65D  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
006AD661  89 7c 24 18              mov      dword ptr [esp + 0x18], edi
006AD665  89 7c 24 14              mov      dword ptr [esp + 0x14], edi
006AD669  75 10                    jne      0x6ad67b
006AD66B  8b 56 48                 mov      edx, dword ptr [esi + 0x48]
006AD66E  bb 09 00 00 00           mov      ebx, 9
006AD673  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
006AD677  89 54 24 14              mov      dword ptr [esp + 0x14], edx
006AD67B  8b 56 30                 mov      edx, dword ptr [esi + 0x30]
006AD67E  3b d7                    cmp      edx, edi
006AD680  74 3c                    je       0x6ad6be
006AD682  83 f8 28                 cmp      eax, 0x28
006AD685  75 12                    jne      0x6ad699
006AD687  8b aa 98 00 00 00        mov      ebp, dword ptr [edx + 0x98]
006AD68D  bb 05 00 00 00           mov      ebx, 5
006AD692  89 6c 24 10              mov      dword ptr [esp + 0x10], ebp
006AD696  8d 6a 24                 lea      ebp, [edx + 0x24]
006AD699  3b d7                    cmp      edx, edi
006AD69B  74 21                    je       0x6ad6be
006AD69D  83 f8 0c                 cmp      eax, 0xc
006AD6A0  74 05                    je       0x6ad6a7
006AD6A2  83 f8 22                 cmp      eax, 0x22
006AD6A5  75 17                    jne      0x6ad6be
006AD6A7  8b 82 98 00 00 00        mov      eax, dword ptr [edx + 0x98]
006AD6AD  bb 01 00 00 00           mov      ebx, 1
006AD6B2  89 44 24 10              mov      dword ptr [esp + 0x10], eax
006AD6B6  8d 6a 24                 lea      ebp, [edx + 0x24]
006AD6B9  e9 9d 00 00 00           jmp      0x6ad75b
006AD6BE  8b 56 50                 mov      edx, dword ptr [esi + 0x50]
006AD6C1  3b d7                    cmp      edx, edi
006AD6C3  74 19                    je       0x6ad6de
006AD6C5  83 f8 0b                 cmp      eax, 0xb
006AD6C8  75 14                    jne      0x6ad6de
006AD6CA  8b 8a 98 00 00 00        mov      ecx, dword ptr [edx + 0x98]
006AD6D0  bb 02 00 00 00           mov      ebx, 2
006AD6D5  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
006AD6D9  8d 6a 24                 lea      ebp, [edx + 0x24]
006AD6DC  eb 7d                    jmp      0x6ad75b
006AD6DE  8b 56 4c                 mov      edx, dword ptr [esi + 0x4c]
006AD6E1  3b d7                    cmp      edx, edi
006AD6E3  74 19                    je       0x6ad6fe
006AD6E5  83 f8 1a                 cmp      eax, 0x1a
006AD6E8  75 14                    jne      0x6ad6fe
006AD6EA  8b 82 98 00 00 00        mov      eax, dword ptr [edx + 0x98]
006AD6F0  bb 03 00 00 00           mov      ebx, 3
006AD6F5  89 44 24 10              mov      dword ptr [esp + 0x10], eax
006AD6F9  8d 6a 24                 lea      ebp, [edx + 0x24]
006AD6FC  eb 5d                    jmp      0x6ad75b
006AD6FE  83 f8 27                 cmp      eax, 0x27
006AD701  75 1a                    jne      0x6ad71d
006AD703  8a 46 54                 mov      al, byte ptr [esi + 0x54]
006AD706  8d 6e 54                 lea      ebp, [esi + 0x54]
006AD709  84 c0                    test     al, al
006AD70B  bb 04 00 00 00           mov      ebx, 4
006AD710  74 04                    je       0x6ad716
006AD712  3b ef                    cmp      ebp, edi
006AD714  75 45                    jne      0x6ad75b
006AD716  bd cc 6b 7f 00           mov      ebp, 0x7f6bcc
006AD71B  eb 3e                    jmp      0x6ad75b
006AD71D  83 f8 04                 cmp      eax, 4
006AD720  75 0c                    jne      0x6ad72e
006AD722  bb 06 00 00 00           mov      ebx, 6
006AD727  e8 74 81 06 00           call     0x7158a0
006AD72C  eb 2b                    jmp      0x6ad759
006AD72E  83 f8 03                 cmp      eax, 3
006AD731  74 1c                    je       0x6ad74f
006AD733  83 f8 26                 cmp      eax, 0x26
006AD736  74 17                    je       0x6ad74f
006AD738  83 f8 01                 cmp      eax, 1
006AD73B  75 1e                    jne      0x6ad75b
006AD73D  51                       push     ecx
006AD73E  b9 78 5d a3 00           mov      ecx, 0xa35d78
006AD743  bb 08 00 00 00           mov      ebx, 8
006AD748  e8 23 ae 03 00           call     0x6e8570
006AD74D  eb 0a                    jmp      0x6ad759
006AD74F  bb 07 00 00 00           mov      ebx, 7
006AD754  e8 a7 72 06 00           call     0x714a00
006AD759  8b e8                    mov      ebp, eax
006AD75B  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
006AD75F  83 c9 ff                 or       ecx, 0xffffffff
006AD762  8b fa                    mov      edi, edx
006AD764  33 c0                    xor      eax, eax
006AD766  f2 ae                    repne scasb al, byte ptr es:[edi]
006AD768  f7 d1                    not      ecx
006AD76A  49                       dec      ecx
006AD76B  03 d1                    add      edx, ecx
006AD76D  83 fb 09                 cmp      ebx, 9
006AD770  89 54 24 20              mov      dword ptr [esp + 0x20], edx
006AD774  75 37                    jne      0x6ad7ad
006AD776  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
006AD77A  8b 46 40                 mov      eax, dword ptr [esi + 0x40]
006AD77D  51                       push     ecx
006AD77E  8b 4e 3c                 mov      ecx, dword ptr [esi + 0x3c]
006AD781  50                       push     eax
006AD782  8b 46 38                 mov      eax, dword ptr [esi + 0x38]
006AD785  51                       push     ecx
006AD786  8b 4e 34                 mov      ecx, dword ptr [esi + 0x34]
006AD789  50                       push     eax
006AD78A  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
006AD78E  51                       push     ecx
006AD78F  8b 4e 2c                 mov      ecx, dword ptr [esi + 0x2c]
006AD792  50                       push     eax
006AD793  53                       push     ebx
006AD794  51                       push     ecx
006AD795  68 b4 6b 7f 00           push     0x7f6bb4
006AD79A  52                       push     edx
006AD79B  e8 54 49 0d 00           call     0x7820f4
006AD7A0  83 c4 28                 add      esp, 0x28
006AD7A3  5f                       pop      edi
006AD7A4  5e                       pop      esi
006AD7A5  5d                       pop      ebp
006AD7A6  5b                       pop      ebx
006AD7A7  83 c4 0c                 add      esp, 0xc
006AD7AA  c2 04 00                 ret      4
006AD7AD  83 fb 05                 cmp      ebx, 5
006AD7B0  75 32                    jne      0x6ad7e4
006AD7B2  8b 46 74                 mov      eax, dword ptr [esi + 0x74]
006AD7B5  8b 4e 40                 mov      ecx, dword ptr [esi + 0x40]
006AD7B8  50                       push     eax
006AD7B9  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
006AD7BC  51                       push     ecx
006AD7BD  8b 4e 38                 mov      ecx, dword ptr [esi + 0x38]
006AD7C0  50                       push     eax
006AD7C1  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
006AD7C4  51                       push     ecx
006AD7C5  8b 4e 2c                 mov      ecx, dword ptr [esi + 0x2c]
006AD7C8  50                       push     eax
006AD7C9  55                       push     ebp
006AD7CA  53                       push     ebx
006AD7CB  51                       push     ecx
006AD7CC  68 9c 6b 7f 00           push     0x7f6b9c
006AD7D1  52                       push     edx
006AD7D2  e8 1d 49 0d 00           call     0x7820f4
006AD7D7  83 c4 28                 add      esp, 0x28
006AD7DA  5f                       pop      edi
006AD7DB  5e                       pop      esi
006AD7DC  5d                       pop      ebp
006AD7DD  5b                       pop      ebx
006AD7DE  83 c4 0c                 add      esp, 0xc
006AD7E1  c2 04 00                 ret      4
006AD7E4  8b 4e 44                 mov      ecx, dword ptr [esi + 0x44]
006AD7E7  85 db                    test     ebx, ebx
006AD7E9  74 38                    je       0x6ad823
006AD7EB  e8 00 72 07 00           call     0x7249f0
006AD7F0  8b 56 40                 mov      edx, dword ptr [esi + 0x40]
006AD7F3  8b 4e 38                 mov      ecx, dword ptr [esi + 0x38]
006AD7F6  50                       push     eax
006AD7F7  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
006AD7FA  52                       push     edx
006AD7FB  8b 56 34                 mov      edx, dword ptr [esi + 0x34]
006AD7FE  50                       push     eax
006AD7FF  8b 46 2c                 mov      eax, dword ptr [esi + 0x2c]
006AD802  51                       push     ecx
006AD803  8b 4c 24 30              mov      ecx, dword ptr [esp + 0x30]
006AD807  52                       push     edx
006AD808  55                       push     ebp
006AD809  53                       push     ebx
006AD80A  50                       push     eax
006AD80B  68 84 6b 7f 00           push     0x7f6b84
006AD810  51                       push     ecx
006AD811  e8 de 48 0d 00           call     0x7820f4
006AD816  83 c4 28                 add      esp, 0x28
006AD819  5f                       pop      edi
006AD81A  5e                       pop      esi
006AD81B  5d                       pop      ebp
006AD81C  5b                       pop      ebx
006AD81D  83 c4 0c                 add      esp, 0xc
006AD820  c2 04 00                 ret      4
006AD823  e8 c8 71 07 00           call     0x7249f0
006AD828  8b 56 40                 mov      edx, dword ptr [esi + 0x40]
006AD82B  8b 4e 38                 mov      ecx, dword ptr [esi + 0x38]
006AD82E  50                       push     eax
006AD82F  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
006AD832  52                       push     edx
006AD833  8b 56 34                 mov      edx, dword ptr [esi + 0x34]
006AD836  50                       push     eax
006AD837  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
006AD83B  51                       push     ecx
006AD83C  8b 4e 2c                 mov      ecx, dword ptr [esi + 0x2c]
006AD83F  52                       push     edx
006AD840  8b 54 24 34              mov      edx, dword ptr [esp + 0x34]
006AD844  50                       push     eax
006AD845  6a 00                    push     0
006AD847  51                       push     ecx
006AD848  68 6c 6b 7f 00           push     0x7f6b6c
006AD84D  52                       push     edx
006AD84E  e8 a1 48 0d 00           call     0x7820f4
006AD853  83 c4 28                 add      esp, 0x28
006AD856  5f                       pop      edi
006AD857  5e                       pop      esi
006AD858  5d                       pop      ebp
006AD859  5b                       pop      ebx
006AD85A  83 c4 0c                 add      esp, 0xc
006AD85D  c2 04 00                 ret      4
006AD860  51                       push     ecx
006AD861  53                       push     ebx
006AD862  55                       push     ebp
006AD863  56                       push     esi
006AD864  57                       push     edi
006AD865  8b f1                    mov      esi, ecx
006AD867  33 ff                    xor      edi, edi
006AD869  68 c0 e9 7c 00           push     0x7ce9c0
006AD86E  57                       push     edi
006AD86F  89 7e 74                 mov      dword ptr [esi + 0x74], edi
006AD872  e8 4b 56 0d 00           call     0x782ec2
006AD877  50                       push     eax
006AD878  e8 80 55 0d 00           call     0x782dfd
006AD87D  68 c0 e9 7c 00           push     0x7ce9c0
006AD882  57                       push     edi
006AD883  89 46 2c                 mov      dword ptr [esi + 0x2c], eax
006AD886  e8 37 56 0d 00           call     0x782ec2
006AD88B  50                       push     eax
