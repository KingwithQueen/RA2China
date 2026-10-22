
sub_00705160 0x00705160 size=1184
00705160  8b 44 24 04              mov      eax, dword ptr [esp + 4]
00705164  83 ec 1c                 sub      esp, 0x1c
00705167  53                       push     ebx
00705168  56                       push     esi
00705169  57                       push     edi
0070516A  8b f9                    mov      edi, ecx
0070516C  50                       push     eax
0070516D  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705172  e8 f9 2e e4 ff           call     0x548070
00705177  8b f0                    mov      esi, eax
00705179  32 db                    xor      bl, bl
0070517B  8b 86 40 01 00 00        mov      eax, dword ptr [esi + 0x140]
00705181  f6 c4 01                 test     ah, 1
00705184  74 6a                    je       0x7051f0
00705186  8a 47 79                 mov      al, byte ptr [edi + 0x79]
00705189  84 c0                    test     al, al
0070518B  75 61                    jne      0x7051ee
0070518D  8b 17                    mov      edx, dword ptr [edi]
0070518F  8d 44 24 10              lea      eax, [esp + 0x10]
00705193  50                       push     eax
00705194  8b cf                    mov      ecx, edi
00705196  ff 52 48                 call     dword ptr [edx + 0x48]
00705199  8b c8                    mov      ecx, eax
0070519B  8b 01                    mov      eax, dword ptr [ecx]
0070519D  99                       cdq      
0070519E  81 e2 ff 00 00 00        and      edx, 0xff
007051A4  03 c2                    add      eax, edx
007051A6  c1 f8 08                 sar      eax, 8
007051A9  66 89 44 24 2c           mov      word ptr [esp + 0x2c], ax
007051AE  8b 41 04                 mov      eax, dword ptr [ecx + 4]
007051B1  99                       cdq      
007051B2  81 e2 ff 00 00 00        and      edx, 0xff
007051B8  03 c2                    add      eax, edx
007051BA  8d 54 24 0c              lea      edx, [esp + 0xc]
007051BE  c1 f8 08                 sar      eax, 8
007051C1  66 89 44 24 2e           mov      word ptr [esp + 0x2e], ax
007051C6  8b 4c 24 2c              mov      ecx, dword ptr [esp + 0x2c]
007051CA  89 4c 24 0c              mov      dword ptr [esp + 0xc], ecx
007051CE  52                       push     edx
007051CF  b9 e0 24 83 00           mov      ecx, 0x8324e0
007051D4  e8 97 2e e4 ff           call     0x548070
007051D9  0f be 8e 1b 01 00 00     movsx    ecx, byte ptr [esi + 0x11b]
007051E0  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
007051E7  83 c1 04                 add      ecx, 4
007051EA  3b c1                    cmp      eax, ecx
007051EC  75 02                    jne      0x7051f0
007051EE  b3 01                    mov      bl, 1
007051F0  8b 97 ac 05 00 00        mov      edx, dword ptr [edi + 0x5ac]
007051F6  8a 82 f3 0a 00 00        mov      al, byte ptr [edx + 0xaf3]
007051FC  84 c0                    test     al, al
007051FE  75 11                    jne      0x705211
00705200  6a 11                    push     0x11
00705202  8b cf                    mov      ecx, edi
00705204  e8 07 27 fd ff           call     0x6d7910
00705209  84 c0                    test     al, al
0070520B  0f 84 ce 01 00 00        je       0x7053df
00705211  8a 44 24 30              mov      al, byte ptr [esp + 0x30]
00705215  84 c0                    test     al, al
00705217  74 3d                    je       0x705256
00705219  84 db                    test     bl, bl
0070521B  74 28                    je       0x705245
0070521D  f6 86 28 01 00 00 1f     test     byte ptr [esi + 0x128], 0x1f
00705224  0f 84 b5 01 00 00        je       0x7053df
0070522A  6a 01                    push     1
0070522C  6a 00                    push     0
0070522E  6a 01                    push     1
00705230  68 c0 04 ad 00           push     0xad04c0
00705235  8b ce                    mov      ecx, esi
00705237  e8 e4 16 d7 ff           call     0x476920
0070523C  5f                       pop      edi
0070523D  5e                       pop      esi
0070523E  5b                       pop      ebx
0070523F  83 c4 1c                 add      esp, 0x1c
00705242  c2 08 00                 ret      8
00705245  f6 86 24 01 00 00 1f     test     byte ptr [esi + 0x124], 0x1f
0070524C  0f 84 8d 01 00 00        je       0x7053df
00705252  6a 00                    push     0
00705254  eb d6                    jmp      0x70522c
00705256  84 db                    test     bl, bl
00705258  74 08                    je       0x705262
0070525A  8b b6 e8 00 00 00        mov      esi, dword ptr [esi + 0xe8]
00705260  eb 06                    jmp      0x705268
00705262  8b b6 e4 00 00 00        mov      esi, dword ptr [esi + 0xe4]
00705268  85 f6                    test     esi, esi
0070526A  c7 44 24 30 00 00 00 00  mov      dword ptr [esp + 0x30], 0
00705272  0f 84 67 01 00 00        je       0x7053df
00705278  55                       push     ebp
00705279  8b 06                    mov      eax, dword ptr [esi]
0070527B  8b ce                    mov      ecx, esi
0070527D  ff 90 84 00 00 00        call     dword ptr [eax + 0x84]
00705283  8a 88 fd 01 00 00        mov      cl, byte ptr [eax + 0x1fd]
00705289  84 c9                    test     cl, cl
0070528B  0f 84 2f 01 00 00        je       0x7053c0
00705291  8b 8f b4 01 00 00        mov      ecx, dword ptr [edi + 0x1b4]
00705297  56                       push     esi
00705298  e8 e3 02 de ff           call     0x4e5580
0070529D  84 c0                    test     al, al
0070529F  74 14                    je       0x7052b5
007052A1  8b 8f ac 05 00 00        mov      ecx, dword ptr [edi + 0x5ac]
007052A7  8a 81 a0 0a 00 00        mov      al, byte ptr [ecx + 0xaa0]
007052AD  84 c0                    test     al, al
007052AF  0f 84 0b 01 00 00        je       0x7053c0
007052B5  8b 16                    mov      edx, dword ptr [esi]
007052B7  8d 44 24 20              lea      eax, [esp + 0x20]
007052BB  50                       push     eax
007052BC  8b ce                    mov      ecx, esi
007052BE  ff 52 48                 call     dword ptr [edx + 0x48]
007052C1  50                       push     eax
007052C2  8b cf                    mov      ecx, edi
007052C4  e8 37 fb ec ff           call     0x5d4e00
007052C9  3d 00 40 00 00           cmp      eax, 0x4000
007052CE  0f 8d ec 00 00 00        jge      0x7053c0
007052D4  8a 46 7a                 mov      al, byte ptr [esi + 0x7a]
007052D7  84 c0                    test     al, al
007052D9  0f 85 e1 00 00 00        jne      0x7053c0
007052DF  8b 16                    mov      edx, dword ptr [esi]
007052E1  8b ce                    mov      ecx, esi
007052E3  ff 52 2c                 call     dword ptr [edx + 0x2c]
007052E6  83 f8 0f                 cmp      eax, 0xf
007052E9  75 64                    jne      0x70534f
007052EB  8b 86 a8 05 00 00        mov      eax, dword ptr [esi + 0x5a8]
007052F1  8a 88 14 0c 00 00        mov      cl, byte ptr [eax + 0xc14]
007052F7  84 c9                    test     cl, cl
007052F9  74 54                    je       0x70534f
007052FB  39 be 94 04 00 00        cmp      dword ptr [esi + 0x494], edi
00705301  75 4c                    jne      0x70534f
00705303  8b 8f ac 05 00 00        mov      ecx, dword ptr [edi + 0x5ac]
00705309  8a 81 a0 0a 00 00        mov      al, byte ptr [ecx + 0xaa0]
0070530F  84 c0                    test     al, al
00705311  75 3c                    jne      0x70534f
00705313  8a 96 72 03 00 00        mov      dl, byte ptr [esi + 0x372]
00705319  8b 07                    mov      eax, dword ptr [edi]
0070531B  8b 5e 30                 mov      ebx, dword ptr [esi + 0x30]
0070531E  6a 00                    push     0
00705320  8b cf                    mov      ecx, edi
00705322  88 97 72 03 00 00        mov      byte ptr [edi + 0x372], dl
00705328  ff 90 d8 00 00 00        call     dword ptr [eax + 0xd8]
0070532E  8b 86 b4 01 00 00        mov      eax, dword ptr [esi + 0x1b4]
00705334  8b 17                    mov      edx, dword ptr [edi]
00705336  6a 01                    push     1
00705338  50                       push     eax
00705339  8b cf                    mov      ecx, edi
0070533B  ff 92 78 03 00 00        call     dword ptr [edx + 0x378]
00705341  8b 16                    mov      edx, dword ptr [esi]
00705343  8b ce                    mov      ecx, esi
00705345  ff 92 f0 00 00 00        call     dword ptr [edx + 0xf0]
0070534B  8b f3                    mov      esi, ebx
0070534D  eb 74                    jmp      0x7053c3
0070534F  8d 87 88 00 00 00        lea      eax, [edi + 0x88]
00705355  8b 5e 30                 mov      ebx, dword ptr [esi + 0x30]
00705358  6a 00                    push     0
0070535A  c7 44 24 38 01 00 00 00  mov      dword ptr [esp + 0x38], 1
00705362  8b 08                    mov      ecx, dword ptr [eax]
00705364  8d 6c 24 18              lea      ebp, [esp + 0x18]
00705368  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
0070536C  8b ce                    mov      ecx, esi
0070536E  8b 50 04                 mov      edx, dword ptr [eax + 4]
00705371  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
00705375  8b 16                    mov      edx, dword ptr [esi]
00705377  8b 40 08                 mov      eax, dword ptr [eax + 8]
0070537A  89 44 24 20              mov      dword ptr [esp + 0x20], eax
0070537E  ff 92 84 00 00 00        call     dword ptr [edx + 0x84]
00705384  8b 88 c0 01 00 00        mov      ecx, dword ptr [eax + 0x1c0]
0070538A  8b d5                    mov      edx, ebp
0070538C  e8 cf ea 00 00           call     0x713e60
00705391  8b 06                    mov      eax, dword ptr [esi]
00705393  57                       push     edi
00705394  8b ce                    mov      ecx, esi
00705396  ff 90 dc 00 00 00        call     dword ptr [eax + 0xdc]
0070539C  8b 16                    mov      edx, dword ptr [esi]
0070539E  6a 00                    push     0
007053A0  8b ce                    mov      ecx, esi
007053A2  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
007053A8  8b 06                    mov      eax, dword ptr [esi]
007053AA  8b ce                    mov      ecx, esi
007053AC  ff 90 d0 00 00 00        call     dword ptr [eax + 0xd0]
007053B2  8b 16                    mov      edx, dword ptr [esi]
007053B4  8b ce                    mov      ecx, esi
007053B6  ff 92 f0 00 00 00        call     dword ptr [edx + 0xf0]
007053BC  8b f3                    mov      esi, ebx
007053BE  eb 03                    jmp      0x7053c3
007053C0  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007053C3  85 f6                    test     esi, esi
007053C5  0f 85 ae fe ff ff        jne      0x705279
007053CB  8b 44 24 34              mov      eax, dword ptr [esp + 0x34]
007053CF  5d                       pop      ebp
007053D0  85 c0                    test     eax, eax
007053D2  74 0b                    je       0x7053df
007053D4  8b 07                    mov      eax, dword ptr [edi]
007053D6  56                       push     esi
007053D7  8b cf                    mov      ecx, edi
007053D9  ff 90 f0 03 00 00        call     dword ptr [eax + 0x3f0]
007053DF  5f                       pop      edi
007053E0  5e                       pop      esi
007053E1  5b                       pop      ebx
007053E2  83 c4 1c                 add      esp, 0x1c
007053E5  c2 08 00                 ret      8
007053E8  90                       nop      
007053E9  90                       nop      
007053EA  90                       nop      
007053EB  90                       nop      
007053EC  90                       nop      
007053ED  90                       nop      
007053EE  90                       nop      
007053EF  90                       nop      
007053F0  81 ec 80 00 00 00        sub      esp, 0x80
007053F6  53                       push     ebx
007053F7  55                       push     ebp
007053F8  8b e9                    mov      ebp, ecx
007053FA  8b 9c 24 8c 00 00 00     mov      ebx, dword ptr [esp + 0x8c]
00705401  56                       push     esi
00705402  57                       push     edi
00705403  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
00705409  8a 88 1a 0b 00 00        mov      cl, byte ptr [eax + 0xb1a]
0070540F  84 c9                    test     cl, cl
00705411  74 62                    je       0x705475
00705413  85 db                    test     ebx, ebx
00705415  75 5e                    jne      0x705475
00705417  8b 8d 94 04 00 00        mov      ecx, dword ptr [ebp + 0x494]
0070541D  85 c9                    test     ecx, ecx
0070541F  74 54                    je       0x705475
00705421  8b 85 28 02 00 00        mov      eax, dword ptr [ebp + 0x228]
00705427  85 c0                    test     eax, eax
00705429  74 4a                    je       0x705475
0070542B  3b c8                    cmp      ecx, eax
0070542D  0f 84 c3 15 00 00        je       0x7069f6
00705433  85 c9                    test     ecx, ecx
00705435  74 3e                    je       0x705475
00705437  8b 11                    mov      edx, dword ptr [ecx]
00705439  ff 52 2c                 call     dword ptr [edx + 0x2c]
0070543C  83 f8 0b                 cmp      eax, 0xb
0070543F  75 34                    jne      0x705475
00705441  8b b5 94 04 00 00        mov      esi, dword ptr [ebp + 0x494]
00705447  85 f6                    test     esi, esi
00705449  75 04                    jne      0x70544f
0070544B  33 c0                    xor      eax, eax
0070544D  eb 12                    jmp      0x705461
0070544F  8b 06                    mov      eax, dword ptr [esi]
00705451  8b ce                    mov      ecx, esi
00705453  ff 50 2c                 call     dword ptr [eax + 0x2c]
00705456  83 e8 0b                 sub      eax, 0xb
00705459  f7 d8                    neg      eax
0070545B  1b c0                    sbb      eax, eax
0070545D  f7 d0                    not      eax
0070545F  23 c6                    and      eax, esi
00705461  8b 88 e4 00 00 00        mov      ecx, dword ptr [eax + 0xe4]
00705467  8b 85 28 02 00 00        mov      eax, dword ptr [ebp + 0x228]
0070546D  3b c8                    cmp      ecx, eax
0070546F  0f 84 81 15 00 00        je       0x7069f6
00705475  3b 9d 94 04 00 00        cmp      ebx, dword ptr [ebp + 0x494]
0070547B  75 0e                    jne      0x70548b
0070547D  8a 85 90 01 00 00        mov      al, byte ptr [ebp + 0x190]
00705483  84 c0                    test     al, al
00705485  0f 84 6b 15 00 00        je       0x7069f6
0070548B  8a 85 c8 05 00 00        mov      al, byte ptr [ebp + 0x5c8]
00705491  c6 85 90 01 00 00 00     mov      byte ptr [ebp + 0x190], 0
00705498  84 c0                    test     al, al
0070549A  8b cd                    mov      ecx, ebp
0070549C  74 12                    je       0x7054b0
0070549E  e8 0d 85 dc ff           call     0x4cd9b0
007054A3  5f                       pop      edi
007054A4  5e                       pop      esi
007054A5  5d                       pop      ebp
007054A6  5b                       pop      ebx
007054A7  81 c4 80 00 00 00        add      esp, 0x80
007054AD  c2 08 00                 ret      8
007054B0  e8 5b 1a f3 ff           call     0x636f10
007054B5  84 c0                    test     al, al
007054B7  74 4c                    je       0x705505
007054B9  8b 95 ac 05 00 00        mov      edx, dword ptr [ebp + 0x5ac]
007054BF  8b 82 2c 05 00 00        mov      eax, dword ptr [edx + 0x52c]
007054C5  85 c0                    test     eax, eax
007054C7  7e 3c                    jle      0x705505
007054C9  6a 00                    push     0
007054CB  8b cd                    mov      ecx, ebp
007054CD  e8 3e 19 f3 ff           call     0x636e10
007054D2  8b 10                    mov      edx, dword ptr [eax]
007054D4  8b c8                    mov      ecx, eax
007054D6  ff 52 2c                 call     dword ptr [edx + 0x2c]
007054D9  83 f8 0f                 cmp      eax, 0xf
007054DC  75 27                    jne      0x705505
007054DE  85 db                    test     ebx, ebx
007054E0  0f 84 be 01 00 00        je       0x7056a4
007054E6  f6 43 14 01              test     byte ptr [ebx + 0x14], 1
007054EA  74 19                    je       0x705505
007054EC  53                       push     ebx
007054ED  8b cd                    mov      ecx, ebp
007054EF  e8 3c 19 f3 ff           call     0x636e30
007054F4  84 c0                    test     al, al
007054F6  75 0d                    jne      0x705505
007054F8  8b 45 00                 mov      eax, dword ptr [ebp]
007054FB  6a 03                    push     3
007054FD  8b cd                    mov      ecx, ebp
007054FF  ff 90 54 02 00 00        call     dword ptr [eax + 0x254]
00705505  85 db                    test     ebx, ebx
00705507  0f 84 97 01 00 00        je       0x7056a4
0070550D  8b cd                    mov      ecx, ebp
0070550F  e8 fc 19 f3 ff           call     0x636f10
00705514  84 c0                    test     al, al
00705516  74 6f                    je       0x705587
00705518  8b 55 00                 mov      edx, dword ptr [ebp]
0070551B  8b cd                    mov      ecx, ebp
0070551D  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
00705523  85 c0                    test     eax, eax
00705525  75 60                    jne      0x705587
00705527  8a 85 70 03 00 00        mov      al, byte ptr [ebp + 0x370]
0070552D  84 c0                    test     al, al
0070552F  74 56                    je       0x705587
00705531  6a 00                    push     0
00705533  8b cd                    mov      ecx, ebp
00705535  e8 d6 18 f3 ff           call     0x636e10
0070553A  8b 10                    mov      edx, dword ptr [eax]
0070553C  8b c8                    mov      ecx, eax
0070553E  ff 52 2c                 call     dword ptr [edx + 0x2c]
00705541  83 f8 02                 cmp      eax, 2
00705544  75 41                    jne      0x705587
00705546  6a 00                    push     0
00705548  8b cd                    mov      ecx, ebp
0070554A  e8 c1 18 f3 ff           call     0x636e10
0070554F  8b 88 ac 05 00 00        mov      ecx, dword ptr [eax + 0x5ac]
00705555  8a 91 94 0b 00 00        mov      dl, byte ptr [ecx + 0xb94]
0070555B  84 d2                    test     dl, dl
0070555D  74 28                    je       0x705587
0070555F  8b 10                    mov      edx, dword ptr [eax]
00705561  6a 01                    push     1
00705563  6a 00                    push     0
00705565  8b c8                    mov      ecx, eax
00705567  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
0070556D  8b 45 00                 mov      eax, dword ptr [ebp]
00705570  6a 19                    push     0x19
00705572  8b cd                    mov      ecx, ebp
00705574  ff 90 54 02 00 00        call     dword ptr [eax + 0x254]
0070557A  8b 55 00                 mov      edx, dword ptr [ebp]
0070557D  6a 03                    push     3
0070557F  8b cd                    mov      ecx, ebp
00705581  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
00705587  8b 03                    mov      eax, dword ptr [ebx]
00705589  8b cb                    mov      ecx, ebx
0070558B  ff 50 2c                 call     dword ptr [eax + 0x2c]
0070558E  8b f0                    mov      esi, eax
00705590  83 ee 06                 sub      esi, 6
00705593  f7 de                    neg      esi
00705595  1b f6                    sbb      esi, esi
00705597  f7 d6                    not      esi
00705599  23 f3                    and      esi, ebx
0070559B  8b 55 00                 mov      edx, dword ptr [ebp]
0070559E  8b cd                    mov      ecx, ebp
007055A0  89 74 24 38              mov      dword ptr [esp + 0x38], esi
007055A4  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
007055AA  83 f8 10                 cmp      eax, 0x10
007055AD  74 0d                    je       0x7055bc
007055AF  83 bd a0 00 00 00 10     cmp      dword ptr [ebp + 0xa0], 0x10
007055B6  0f 85 9a 00 00 00        jne      0x705656
007055BC  8b 45 00                 mov      eax, dword ptr [ebp]
007055BF  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
007055C3  51                       push     ecx
007055C4  8b cd                    mov      ecx, ebp
007055C6  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
007055CC  66 8b 10                 mov      dx, word ptr [eax]
007055CF  66 8b 40 02              mov      ax, word ptr [eax + 2]
007055D3  66 03 15 88 1a 85 00     add      dx, word ptr [0x851a88]
007055DA  66 03 05 8a 1a 85 00     add      ax, word ptr [0x851a8a]
007055E1  66 89 54 24 30           mov      word ptr [esp + 0x30], dx
007055E6  66 89 44 24 32           mov      word ptr [esp + 0x32], ax
007055EB  8b 4c 24 30              mov      ecx, dword ptr [esp + 0x30]
007055EF  8d 54 24 34              lea      edx, [esp + 0x34]
007055F3  89 4c 24 34              mov      dword ptr [esp + 0x34], ecx
007055F7  52                       push     edx
007055F8  b9 e0 24 83 00           mov      ecx, 0x8324e0
