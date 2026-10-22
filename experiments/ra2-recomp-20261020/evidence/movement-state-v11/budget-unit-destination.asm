
sub_007053F0 0x007053F0 size=5651
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
007055FD  e8 6e 2a e4 ff           call     0x548070
00705602  8b c8                    mov      ecx, eax
00705604  e8 a7 c1 d6 ff           call     0x4717b0
00705609  8b f8                    mov      edi, eax
0070560B  85 ff                    test     edi, edi
0070560D  74 47                    je       0x705656
0070560F  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
00705615  8a 88 a6 0b 00 00        mov      cl, byte ptr [eax + 0xba6]
0070561B  84 c9                    test     cl, cl
0070561D  74 37                    je       0x705656
0070561F  8b 8f 70 02 00 00        mov      ecx, dword ptr [edi + 0x270]
00705625  85 c9                    test     ecx, ecx
00705627  74 08                    je       0x705631
00705629  8b 11                    mov      edx, dword ptr [ecx]
0070562B  ff 92 f0 00 00 00        call     dword ptr [edx + 0xf0]
00705631  8b 8f 74 02 00 00        mov      ecx, dword ptr [edi + 0x274]
00705637  85 c9                    test     ecx, ecx
00705639  74 08                    je       0x705643
0070563B  8b 01                    mov      eax, dword ptr [ecx]
0070563D  ff 90 f0 00 00 00        call     dword ptr [eax + 0xf0]
00705643  8b 87 7c 04 00 00        mov      eax, dword ptr [edi + 0x47c]
00705649  85 c0                    test     eax, eax
0070564B  74 09                    je       0x705656
0070564D  6a 0a                    push     0xa
0070564F  8b cf                    mov      ecx, edi
00705651  e8 7a 79 d4 ff           call     0x44cfd0
00705656  8b 55 00                 mov      edx, dword ptr [ebp]
00705659  8b cd                    mov      ecx, ebp
0070565B  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
00705661  83 cf ff                 or       edi, 0xffffffff
00705664  83 f8 07                 cmp      eax, 7
00705667  74 0d                    je       0x705676
00705669  83 bd a0 00 00 00 07     cmp      dword ptr [ebp + 0xa0], 7
00705670  0f 85 a6 01 00 00        jne      0x70581c
00705676  8b cd                    mov      ecx, ebp
00705678  e8 93 18 f3 ff           call     0x636f10
0070567D  84 c0                    test     al, al
0070567F  0f 85 97 01 00 00        jne      0x70581c
00705685  8b cb                    mov      ecx, ebx
00705687  e8 94 85 d0 ff           call     0x40dc20
0070568C  85 c0                    test     eax, eax
0070568E  74 48                    je       0x7056d8
00705690  8b 10                    mov      edx, dword ptr [eax]
00705692  8b c8                    mov      ecx, eax
00705694  ff 52 2c                 call     dword ptr [edx + 0x2c]
00705697  83 f8 01                 cmp      eax, 1
0070569A  75 3c                    jne      0x7056d8
0070569C  85 db                    test     ebx, ebx
0070569E  75 0b                    jne      0x7056ab
007056A0  33 c0                    xor      eax, eax
007056A2  eb 17                    jmp      0x7056bb
007056A4  33 f6                    xor      esi, esi
007056A6  e9 f0 fe ff ff           jmp      0x70559b
007056AB  8b 03                    mov      eax, dword ptr [ebx]
007056AD  8b cb                    mov      ecx, ebx
007056AF  ff 50 2c                 call     dword ptr [eax + 0x2c]
007056B2  48                       dec      eax
007056B3  f7 d8                    neg      eax
007056B5  1b c0                    sbb      eax, eax
007056B7  f7 d0                    not      eax
007056B9  23 c3                    and      eax, ebx
007056BB  6a 00                    push     0
007056BD  8b cd                    mov      ecx, ebp
007056BF  89 85 f8 03 00 00        mov      dword ptr [ebp + 0x3f8], eax
007056C5  e8 86 17 fd ff           call     0x6d6e50
007056CA  33 db                    xor      ebx, ebx
007056CC  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
007056D3  e9 4a 01 00 00           jmp      0x705822
007056D8  85 f6                    test     esi, esi
007056DA  0f 84 e9 00 00 00        je       0x7057c9
007056E0  8b 16                    mov      edx, dword ptr [esi]
007056E2  8b ce                    mov      ecx, esi
007056E4  ff 52 2c                 call     dword ptr [edx + 0x2c]
007056E7  83 f8 06                 cmp      eax, 6
007056EA  0f 85 d9 00 00 00        jne      0x7057c9
007056F0  8b ce                    mov      ecx, esi
007056F2  e8 19 18 f3 ff           call     0x636f10
007056F7  84 c0                    test     al, al
007056F9  74 65                    je       0x705760
007056FB  53                       push     ebx
007056FC  8b cd                    mov      ecx, ebp
007056FE  e8 4d 17 fd ff           call     0x6d6e50
00705703  8b 86 18 04 00 00        mov      eax, dword ptr [esi + 0x418]
00705709  8a 88 49 13 00 00        mov      cl, byte ptr [eax + 0x1349]
0070570F  84 c9                    test     cl, cl
00705711  0f 84 0b 01 00 00        je       0x705822
00705717  8b cd                    mov      ecx, ebp
00705719  e8 22 ee ec ff           call     0x5d4540
0070571E  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
00705724  dc 99 60 13 00 00        fcomp    qword ptr [ecx + 0x1360]
0070572A  df e0                    fnstsw   ax
0070572C  f6 c4 01                 test     ah, 1
0070572F  74 14                    je       0x705745
00705731  33 db                    xor      ebx, ebx
00705733  89 b5 f8 03 00 00        mov      dword ptr [ebp + 0x3f8], esi
00705739  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
00705740  e9 dd 00 00 00           jmp      0x705822
00705745  8b 55 00                 mov      edx, dword ptr [ebp]
00705748  6a 03                    push     3
0070574A  8b cd                    mov      ecx, ebp
0070574C  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
00705752  33 db                    xor      ebx, ebx
00705754  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
0070575B  e9 c2 00 00 00           jmp      0x705822
00705760  8b 45 00                 mov      eax, dword ptr [ebp]
00705763  8b bd 94 04 00 00        mov      edi, dword ptr [ebp + 0x494]
00705769  56                       push     esi
0070576A  6a 0e                    push     0xe
0070576C  8b cd                    mov      ecx, ebp
0070576E  ff 90 58 02 00 00        call     dword ptr [eax + 0x258]
00705774  83 f8 01                 cmp      eax, 1
00705777  74 2b                    je       0x7057a4
00705779  8b 55 00                 mov      edx, dword ptr [ebp]
0070577C  6a 03                    push     3
0070577E  8b cd                    mov      ecx, ebp
00705780  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
00705786  8b 86 18 04 00 00        mov      eax, dword ptr [esi + 0x418]
0070578C  8a 88 49 13 00 00        mov      cl, byte ptr [eax + 0x1349]
00705792  84 c9                    test     cl, cl
00705794  0f 84 88 00 00 00        je       0x705822
0070579A  53                       push     ebx
0070579B  8b cd                    mov      ecx, ebp
0070579D  e8 ae 16 fd ff           call     0x6d6e50
007057A2  eb 7e                    jmp      0x705822
007057A4  8b 8e 18 04 00 00        mov      ecx, dword ptr [esi + 0x418]
007057AA  8a 81 4d 13 00 00        mov      al, byte ptr [ecx + 0x134d]
007057B0  84 c0                    test     al, al
007057B2  74 6e                    je       0x705822
007057B4  8b 85 94 04 00 00        mov      eax, dword ptr [ebp + 0x494]
007057BA  3b c7                    cmp      eax, edi
007057BC  74 64                    je       0x705822
007057BE  8b d8                    mov      ebx, eax
007057C0  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
007057C7  eb 59                    jmp      0x705822
007057C9  85 db                    test     ebx, ebx
007057CB  74 55                    je       0x705822
007057CD  f6 43 14 01              test     byte ptr [ebx + 0x14], 1
007057D1  74 4f                    je       0x705822
007057D3  8b cb                    mov      ecx, ebx
007057D5  e8 36 17 f3 ff           call     0x636f10
007057DA  84 c0                    test     al, al
007057DC  74 0a                    je       0x7057e8
007057DE  53                       push     ebx
007057DF  8b cd                    mov      ecx, ebp
007057E1  e8 6a 16 fd ff           call     0x6d6e50
007057E6  eb 3a                    jmp      0x705822
007057E8  8b 55 00                 mov      edx, dword ptr [ebp]
007057EB  53                       push     ebx
007057EC  6a 02                    push     2
007057EE  8b cd                    mov      ecx, ebp
007057F0  ff 92 58 02 00 00        call     dword ptr [edx + 0x258]
007057F6  83 f8 01                 cmp      eax, 1
007057F9  75 27                    jne      0x705822
007057FB  8b 45 00                 mov      eax, dword ptr [ebp]
007057FE  6a 0e                    push     0xe
00705800  8b cd                    mov      ecx, ebp
00705802  ff 90 54 02 00 00        call     dword ptr [eax + 0x254]
00705808  83 f8 01                 cmp      eax, 1
0070580B  74 15                    je       0x705822
0070580D  8b 55 00                 mov      edx, dword ptr [ebp]
00705810  6a 03                    push     3
00705812  8b cd                    mov      ecx, ebp
00705814  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
0070581A  eb 06                    jmp      0x705822
0070581C  89 bd d0 04 00 00        mov      dword ptr [ebp + 0x4d0], edi
00705822  85 db                    test     ebx, ebx
00705824  c6 44 24 15 00           mov      byte ptr [esp + 0x15], 0
00705829  0f 84 ee 01 00 00        je       0x705a1d
0070582F  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
00705835  8a 88 f5 0a 00 00        mov      cl, byte ptr [eax + 0xaf5]
0070583B  84 c9                    test     cl, cl
0070583D  0f 84 da 01 00 00        je       0x705a1d
00705843  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
00705849  8d b5 64 05 00 00        lea      esi, [ebp + 0x564]
0070584F  85 c0                    test     eax, eax
00705851  75 0a                    jne      0x70585d
00705853  68 03 40 00 80           push     0x80004003
00705858  e8 e3 00 09 00           call     0x795940
0070585D  8b 06                    mov      eax, dword ptr [esi]
0070585F  50                       push     eax
00705860  8b 08                    mov      ecx, dword ptr [eax]
00705862  ff 51 10                 call     dword ptr [ecx + 0x10]
00705865  84 c0                    test     al, al
00705867  0f 84 b0 01 00 00        je       0x705a1d
0070586D  8b 06                    mov      eax, dword ptr [esi]
0070586F  c7 44 24 30 00 00 00 00  mov      dword ptr [esp + 0x30], 0
00705877  85 c0                    test     eax, eax
00705879  74 23                    je       0x70589e
0070587B  56                       push     esi
0070587C  8d 4c 24 34              lea      ecx, [esp + 0x34]
00705880  e8 6b f3 d4 ff           call     0x454bf0
00705885  85 c0                    test     eax, eax
00705887  7d 0d                    jge      0x705896
00705889  3d 02 40 00 80           cmp      eax, 0x80004002
0070588E  74 06                    je       0x705896
00705890  50                       push     eax
00705891  e8 aa 00 09 00           call     0x795940
00705896  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
0070589A  85 c0                    test     eax, eax
0070589C  75 0e                    jne      0x7058ac
0070589E  68 03 40 00 80           push     0x80004003
007058A3  e8 98 00 09 00           call     0x795940
007058A8  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
007058AC  8b 10                    mov      edx, dword ptr [eax]
007058AE  8d 4c 24 70              lea      ecx, [esp + 0x70]
007058B2  51                       push     ecx
007058B3  50                       push     eax
007058B4  ff 52 0c                 call     dword ptr [edx + 0xc]
007058B7  b9 04 00 00 00           mov      ecx, 4
007058BC  bf 70 1f 7a 00           mov      edi, 0x7a1f70
007058C1  8d 74 24 70              lea      esi, [esp + 0x70]
007058C5  33 d2                    xor      edx, edx
007058C7  f3 a7                    repe cmpsd dword ptr [esi], dword ptr es:[edi]
007058C9  0f 85 40 01 00 00        jne      0x705a0f
007058CF  8b 8d a4 04 00 00        mov      ecx, dword ptr [ebp + 0x4a4]
007058D5  8b 85 ac 04 00 00        mov      eax, dword ptr [ebp + 0x4ac]
007058DB  8d b5 9c 04 00 00        lea      esi, [ebp + 0x49c]
007058E1  3b c1                    cmp      eax, ecx
007058E3  7c 22                    jl       0x705907
007058E5  8a 46 0d                 mov      al, byte ptr [esi + 0xd]
007058E8  84 c0                    test     al, al
007058EA  75 04                    jne      0x7058f0
007058EC  85 c9                    test     ecx, ecx
007058EE  75 3e                    jne      0x70592e
007058F0  8b 46 14                 mov      eax, dword ptr [esi + 0x14]
007058F3  85 c0                    test     eax, eax
007058F5  7e 37                    jle      0x70592e
007058F7  8b 16                    mov      edx, dword ptr [esi]
007058F9  03 c8                    add      ecx, eax
007058FB  6a 00                    push     0
007058FD  51                       push     ecx
007058FE  8b ce                    mov      ecx, esi
00705900  ff 52 08                 call     dword ptr [edx + 8]
00705903  84 c0                    test     al, al
00705905  74 27                    je       0x70592e
00705907  8b 4e 10                 mov      ecx, dword ptr [esi + 0x10]
0070590A  85 c9                    test     ecx, ecx
0070590C  74 14                    je       0x705922
0070590E  8b 46 04                 mov      eax, dword ptr [esi + 4]
00705911  c1 e1 02                 shl      ecx, 2
00705914  51                       push     ecx
00705915  50                       push     eax
00705916  83 c0 04                 add      eax, 4
00705919  50                       push     eax
0070591A  e8 71 d9 07 00           call     0x783290
0070591F  83 c4 0c                 add      esp, 0xc
00705922  8b 56 04                 mov      edx, dword ptr [esi + 4]
00705925  89 1a                    mov      dword ptr [edx], ebx
00705927  8b 46 10                 mov      eax, dword ptr [esi + 0x10]
0070592A  40                       inc      eax
0070592B  89 46 10                 mov      dword ptr [esi + 0x10], eax
0070592E  8b 85 78 04 00 00        mov      eax, dword ptr [ebp + 0x478]
00705934  8d 8d 78 04 00 00        lea      ecx, [ebp + 0x478]
0070593A  ff 50 0c                 call     dword ptr [eax + 0xc]
0070593D  8b 55 00                 mov      edx, dword ptr [ebp]
00705940  8b cd                    mov      ecx, ebp
00705942  ff 92 ac 01 00 00        call     dword ptr [edx + 0x1ac]
00705948  8b d8                    mov      ebx, eax
0070594A  c6 84 24 98 00 00 00 00  mov      byte ptr [esp + 0x98], 0
00705952  85 db                    test     ebx, ebx
00705954  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
0070595B  0f 84 ae 00 00 00        je       0x705a0f
00705961  8b 83 40 01 00 00        mov      eax, dword ptr [ebx + 0x140]
00705967  f6 c4 01                 test     ah, 1
0070596A  0f 84 9f 00 00 00        je       0x705a0f
00705970  8b 45 00                 mov      eax, dword ptr [ebp]
00705973  6a 00                    push     0
00705975  8b cd                    mov      ecx, ebp
00705977  ff 90 b8 00 00 00        call     dword ptr [eax + 0xb8]
0070597D  84 c0                    test     al, al
0070597F  0f 85 8a 00 00 00        jne      0x705a0f
00705985  33 ff                    xor      edi, edi
00705987  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
0070598D  66 89 7c 24 2c           mov      word ptr [esp + 0x2c], di
00705992  66 89 7c 24 2e           mov      word ptr [esp + 0x2e], di
00705997  57                       push     edi
00705998  8b 80 00 05 00 00        mov      eax, dword ptr [eax + 0x500]
0070599E  8d 7c 24 30              lea      edi, [esp + 0x30]
007059A2  b9 01 00 00 00           mov      ecx, 1
007059A7  57                       push     edi
007059A8  6a 00                    push     0
007059AA  6a 00                    push     0
007059AC  8b d1                    mov      edx, ecx
007059AE  51                       push     ecx
007059AF  6a 00                    push     0
007059B1  52                       push     edx
007059B2  51                       push     ecx
007059B3  6a 00                    push     0
007059B5  50                       push     eax
007059B6  8d 73 24                 lea      esi, [ebx + 0x24]
007059B9  6a 00                    push     0
007059BB  50                       push     eax
007059BC  56                       push     esi
007059BD  b9 e0 24 83 00           mov      ecx, 0x8324e0
007059C2  e8 29 9f e4 ff           call     0x54f8f0
007059C7  50                       push     eax
007059C8  6a 01                    push     1
007059CA  8d 4c 24 6c              lea      ecx, [esp + 0x6c]
007059CE  56                       push     esi
007059CF  51                       push     ecx
007059D0  b9 e0 24 83 00           mov      ecx, 0x8324e0
007059D5  e8 06 a9 e4 ff           call     0x5502e0
007059DA  8b 00                    mov      eax, dword ptr [eax]
007059DC  66 3b 05 88 04 ad 00     cmp      ax, word ptr [0xad0488]
007059E3  89 44 24 34              mov      dword ptr [esp + 0x34], eax
007059E7  75 0e                    jne      0x7059f7
007059E9  66 8b 54 24 36           mov      dx, word ptr [esp + 0x36]
007059EE  66 3b 15 8a 04 ad 00     cmp      dx, word ptr [0xad048a]
007059F5  74 18                    je       0x705a0f
007059F7  8d 44 24 34              lea      eax, [esp + 0x34]
007059FB  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705A00  50                       push     eax
00705A01  e8 6a 26 e4 ff           call     0x548070
00705A06  8b d8                    mov      ebx, eax
00705A08  89 9c 24 94 00 00 00     mov      dword ptr [esp + 0x94], ebx
00705A0F  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
00705A13  85 c0                    test     eax, eax
00705A15  74 06                    je       0x705a1d
00705A17  8b 08                    mov      ecx, dword ptr [eax]
00705A19  50                       push     eax
00705A1A  ff 51 08                 call     dword ptr [ecx + 8]
00705A1D  85 db                    test     ebx, ebx
00705A1F  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
00705A24  0f 84 27 03 00 00        je       0x705d51
00705A2A  8b 95 ac 05 00 00        mov      edx, dword ptr [ebp + 0x5ac]
00705A30  8a 82 f5 0a 00 00        mov      al, byte ptr [edx + 0xaf5]
00705A36  84 c0                    test     al, al
00705A38  0f 84 2e 02 00 00        je       0x705c6c
00705A3E  8a 84 24 98 00 00 00     mov      al, byte ptr [esp + 0x98]
00705A45  84 c0                    test     al, al
00705A47  0f 84 13 03 00 00        je       0x705d60
00705A4D  8b 45 00                 mov      eax, dword ptr [ebp]
00705A50  6a 00                    push     0
00705A52  8b cd                    mov      ecx, ebp
00705A54  ff 90 b8 00 00 00        call     dword ptr [eax + 0xb8]
00705A5A  8b 55 00                 mov      edx, dword ptr [ebp]
00705A5D  88 44 24 14              mov      byte ptr [esp + 0x14], al
00705A61  8d 44 24 54              lea      eax, [esp + 0x54]
00705A65  6a 00                    push     0
00705A67  50                       push     eax
00705A68  8b cd                    mov      ecx, ebp
00705A6A  ff 52 4c                 call     dword ptr [edx + 0x4c]
00705A6D  8b c8                    mov      ecx, eax
00705A6F  8b 01                    mov      eax, dword ptr [ecx]
00705A71  99                       cdq      
00705A72  81 e2 ff 00 00 00        and      edx, 0xff
00705A78  03 c2                    add      eax, edx
00705A7A  c1 f8 08                 sar      eax, 8
00705A7D  66 89 44 24 1c           mov      word ptr [esp + 0x1c], ax
00705A82  8b 41 04                 mov      eax, dword ptr [ecx + 4]
00705A85  99                       cdq      
00705A86  81 e2 ff 00 00 00        and      edx, 0xff
00705A8C  03 c2                    add      eax, edx
00705A8E  8d 54 24 2c              lea      edx, [esp + 0x2c]
00705A92  c1 f8 08                 sar      eax, 8
00705A95  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
00705A9A  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
00705A9E  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
00705AA2  52                       push     edx
00705AA3  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705AA8  e8 c3 25 e4 ff           call     0x548070
00705AAD  8b c8                    mov      ecx, eax
00705AAF  e8 4c 67 d7 ff           call     0x47c200
00705AB4  8b bc 24 94 00 00 00     mov      edi, dword ptr [esp + 0x94]
00705ABB  8d 4c 24 54              lea      ecx, [esp + 0x54]
00705ABF  88 44 24 16              mov      byte ptr [esp + 0x16], al
00705AC3  51                       push     ecx
00705AC4  8b 07                    mov      eax, dword ptr [edi]
00705AC6  8b cf                    mov      ecx, edi
00705AC8  ff 50 48                 call     dword ptr [eax + 0x48]
00705ACB  8b c8                    mov      ecx, eax
00705ACD  8b 01                    mov      eax, dword ptr [ecx]
00705ACF  99                       cdq      
00705AD0  81 e2 ff 00 00 00        and      edx, 0xff
00705AD6  03 c2                    add      eax, edx
00705AD8  c1 f8 08                 sar      eax, 8
00705ADB  66 89 44 24 1c           mov      word ptr [esp + 0x1c], ax
00705AE0  8b 41 04                 mov      eax, dword ptr [ecx + 4]
00705AE3  99                       cdq      
00705AE4  81 e2 ff 00 00 00        and      edx, 0xff
00705AEA  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705AEF  03 c2                    add      eax, edx
00705AF1  c1 f8 08                 sar      eax, 8
00705AF4  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
00705AF9  8b 54 24 1c              mov      edx, dword ptr [esp + 0x1c]
00705AFD  8d 44 24 28              lea      eax, [esp + 0x28]
00705B01  89 54 24 28              mov      dword ptr [esp + 0x28], edx
00705B05  50                       push     eax
00705B06  e8 65 25 e4 ff           call     0x548070
00705B0B  8b 98 40 01 00 00        mov      ebx, dword ptr [eax + 0x140]
00705B11  8b c8                    mov      ecx, eax
00705B13  c1 eb 08                 shr      ebx, 8
00705B16  80 e3 01                 and      bl, 1
00705B19  e8 e2 66 d7 ff           call     0x47c200
00705B1E  8b 55 00                 mov      edx, dword ptr [ebp]
00705B21  8b cd                    mov      ecx, ebp
00705B23  88 44 24 17              mov      byte ptr [esp + 0x17], al
00705B27  ff 92 b0 01 00 00        call     dword ptr [edx + 0x1b0]
00705B2D  89 44 24 18              mov      dword ptr [esp + 0x18], eax
00705B31  8a 44 24 14              mov      al, byte ptr [esp + 0x14]
00705B35  84 c0                    test     al, al
00705B37  0f 84 ee 00 00 00        je       0x705c2b
00705B3D  84 db                    test     bl, bl
00705B3F  0f 84 da 00 00 00        je       0x705c1f
00705B45  6a 00                    push     0
00705B47  8d 44 24 30              lea      eax, [esp + 0x30]
00705B4B  6a 03                    push     3
00705B4D  50                       push     eax
00705B4E  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705B53  e8 78 a5 e4 ff           call     0x5500d0
00705B58  6a 00                    push     0
00705B5A  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
00705B5E  6a 03                    push     3
00705B60  51                       push     ecx
00705B61  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705B66  8b f0                    mov      esi, eax
00705B68  e8 63 a5 e4 ff           call     0x5500d0
00705B6D  3b f0                    cmp      esi, eax
00705B6F  0f 85 aa 00 00 00        jne      0x705c1f
00705B75  83 fe ff                 cmp      esi, -1
00705B78  0f 84 a1 00 00 00        je       0x705c1f
00705B7E  8b 15 30 25 83 00        mov      edx, dword ptr [0x832530]
00705B84  c1 e6 04                 shl      esi, 4
00705B87  8a 44 16 08              mov      al, byte ptr [esi + edx + 8]
00705B8B  84 c0                    test     al, al
00705B8D  0f 85 87 00 00 00        jne      0x705c1a
00705B93  8d 44 24 2c              lea      eax, [esp + 0x2c]
00705B97  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
00705B9B  50                       push     eax
00705B9C  8d 54 24 40              lea      edx, [esp + 0x40]
00705BA0  51                       push     ecx
00705BA1  52                       push     edx
00705BA2  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705BA7  e8 34 f6 e5 ff           call     0x5651e0
00705BAC  8b 30                    mov      esi, dword ptr [eax]
00705BAE  8d 44 24 28              lea      eax, [esp + 0x28]
00705BB2  8d 4c 24 28              lea      ecx, [esp + 0x28]
00705BB6  50                       push     eax
00705BB7  8d 54 24 40              lea      edx, [esp + 0x40]
00705BBB  51                       push     ecx
00705BBC  52                       push     edx
00705BBD  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705BC2  89 74 24 28              mov      dword ptr [esp + 0x28], esi
00705BC6  e8 15 f6 e5 ff           call     0x5651e0
00705BCB  8b 00                    mov      eax, dword ptr [eax]
00705BCD  83 ec 08                 sub      esp, 8
00705BD0  89 44 24 44              mov      dword ptr [esp + 0x44], eax
00705BD4  8b 5c 24 46              mov      ebx, dword ptr [esp + 0x46]
00705BD8  2b f0                    sub      esi, eax
00705BDA  8b 44 24 26              mov      eax, dword ptr [esp + 0x26]
00705BDE  2b c3                    sub      eax, ebx
00705BE0  0f bf c0                 movsx    eax, ax
00705BE3  0f bf ce                 movsx    ecx, si
00705BE6  89 44 24 24              mov      dword ptr [esp + 0x24], eax
00705BEA  db 44 24 24              fild     dword ptr [esp + 0x24]
00705BEE  89 4c 24 24              mov      dword ptr [esp + 0x24], ecx
00705BF2  db 44 24 24              fild     dword ptr [esp + 0x24]
00705BF6  d9 c0                    fld      st(0)
00705BF8  d8 c9                    fmul     st(1)
00705BFA  d9 c2                    fld      st(2)
00705BFC  d8 cb                    fmul     st(3)
00705BFE  de c1                    faddp    st(1)
00705C00  dd 1c 24                 fstp     qword ptr [esp]
00705C03  dd d8                    fstp     st(0)
00705C05  dd d8                    fstp     st(0)
00705C07  e8 04 48 db ff           call     0x4ba410
00705C0C  83 c4 08                 add      esp, 8
00705C0F  e8 fc 94 07 00           call     0x77f110
00705C14  66 3d 02 00              cmp      ax, 2
00705C18  7f 05                    jg       0x705c1f
00705C1A  c6 44 24 13 01           mov      byte ptr [esp + 0x13], 1
00705C1F  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
00705C23  84 c0                    test     al, al
00705C25  75 0c                    jne      0x705c33
00705C27  b0 01                    mov      al, 1
00705C29  eb 0c                    jmp      0x705c37
00705C2B  84 db                    test     bl, bl
00705C2D  74 04                    je       0x705c33
00705C2F  b0 01                    mov      al, 1
00705C31  eb 04                    jmp      0x705c37
00705C33  8a 44 24 15              mov      al, byte ptr [esp + 0x15]
00705C37  8a 4c 24 16              mov      cl, byte ptr [esp + 0x16]
00705C3B  84 c9                    test     cl, cl
00705C3D  75 08                    jne      0x705c47
00705C3F  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
00705C43  85 c9                    test     ecx, ecx
00705C45  7d 08                    jge      0x705c4f
00705C47  8a 4c 24 17              mov      cl, byte ptr [esp + 0x17]
00705C4B  84 c9                    test     cl, cl
00705C4D  75 08                    jne      0x705c57
00705C4F  8a 4c 24 13              mov      cl, byte ptr [esp + 0x13]
00705C53  84 c9                    test     cl, cl
00705C55  74 04                    je       0x705c5b
00705C57  84 c0                    test     al, al
00705C59  74 11                    je       0x705c6c
00705C5B  57                       push     edi
00705C5C  8b cd                    mov      ecx, ebp
00705C5E  e8 fd 22 00 00           call     0x707f60
00705C63  89 84 24 94 00 00 00     mov      dword ptr [esp + 0x94], eax
00705C6A  eb 1e                    jmp      0x705c8a
00705C6C  8a 84 24 98 00 00 00     mov      al, byte ptr [esp + 0x98]
00705C73  84 c0                    test     al, al
00705C75  0f 84 e5 00 00 00        je       0x705d60
00705C7B  8b 95 78 04 00 00        mov      edx, dword ptr [ebp + 0x478]
00705C81  8d 8d 78 04 00 00        lea      ecx, [ebp + 0x478]
00705C87  ff 52 0c                 call     dword ptr [edx + 0xc]
00705C8A  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
00705C90  85 c0                    test     eax, eax
00705C92  75 0a                    jne      0x705c9e
00705C94  68 03 40 00 80           push     0x80004003
00705C99  e8 a2 fc 08 00           call     0x795940
00705C9E  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
00705CA4  50                       push     eax
00705CA5  8b 08                    mov      ecx, dword ptr [eax]
00705CA7  ff 91 98 00 00 00        call     dword ptr [ecx + 0x98]
00705CAD  84 c0                    test     al, al
00705CAF  0f 84 ab 00 00 00        je       0x705d60
00705CB5  8b 8d 80 04 00 00        mov      ecx, dword ptr [ebp + 0x480]
00705CBB  8b 85 88 04 00 00        mov      eax, dword ptr [ebp + 0x488]
00705CC1  8d b5 78 04 00 00        lea      esi, [ebp + 0x478]
00705CC7  3b c1                    cmp      eax, ecx
00705CC9  7c 22                    jl       0x705ced
00705CCB  8a 46 0d                 mov      al, byte ptr [esi + 0xd]
00705CCE  84 c0                    test     al, al
00705CD0  75 04                    jne      0x705cd6
00705CD2  85 c9                    test     ecx, ecx
00705CD4  75 45                    jne      0x705d1b
00705CD6  8b 46 14                 mov      eax, dword ptr [esi + 0x14]
00705CD9  85 c0                    test     eax, eax
00705CDB  7e 3e                    jle      0x705d1b
00705CDD  8b 16                    mov      edx, dword ptr [esi]
00705CDF  03 c8                    add      ecx, eax
00705CE1  6a 00                    push     0
00705CE3  51                       push     ecx
00705CE4  8b ce                    mov      ecx, esi
00705CE6  ff 52 08                 call     dword ptr [edx + 8]
00705CE9  84 c0                    test     al, al
00705CEB  74 2e                    je       0x705d1b
00705CED  8b 4e 10                 mov      ecx, dword ptr [esi + 0x10]
00705CF0  85 c9                    test     ecx, ecx
00705CF2  74 14                    je       0x705d08
00705CF4  8b 46 04                 mov      eax, dword ptr [esi + 4]
00705CF7  c1 e1 02                 shl      ecx, 2
00705CFA  51                       push     ecx
00705CFB  50                       push     eax
00705CFC  83 c0 04                 add      eax, 4
00705CFF  50                       push     eax
00705D00  e8 8b d5 07 00           call     0x783290
00705D05  83 c4 0c                 add      esp, 0xc
00705D08  8b 56 04                 mov      edx, dword ptr [esi + 4]
00705D0B  8b 84 24 94 00 00 00     mov      eax, dword ptr [esp + 0x94]
00705D12  89 02                    mov      dword ptr [edx], eax
00705D14  8b 46 10                 mov      eax, dword ptr [esi + 0x10]
00705D17  40                       inc      eax
00705D18  89 46 10                 mov      dword ptr [esi + 0x10], eax
00705D1B  8d 8d 88 00 00 00        lea      ecx, [ebp + 0x88]
00705D21  8b 95 88 00 00 00        mov      edx, dword ptr [ebp + 0x88]
00705D27  89 54 24 54              mov      dword ptr [esp + 0x54], edx
00705D2B  8d 54 24 54              lea      edx, [esp + 0x54]
00705D2F  8b 41 04                 mov      eax, dword ptr [ecx + 4]
00705D32  52                       push     edx
00705D33  89 44 24 5c              mov      dword ptr [esp + 0x5c], eax
00705D37  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
00705D3A  89 4c 24 60              mov      dword ptr [esp + 0x60], ecx
00705D3E  b9 e0 24 83 00           mov      ecx, 0x8324e0
00705D43  e8 b8 22 e4 ff           call     0x548000
00705D48  89 84 24 94 00 00 00     mov      dword ptr [esp + 0x94], eax
00705D4F  eb 0f                    jmp      0x705d60
00705D51  8b 85 78 04 00 00        mov      eax, dword ptr [ebp + 0x478]
00705D57  8d 8d 78 04 00 00        lea      ecx, [ebp + 0x478]
00705D5D  ff 50 0c                 call     dword ptr [eax + 0xc]
00705D60  8b 8d ac 05 00 00        mov      ecx, dword ptr [ebp + 0x5ac]
00705D66  8a 81 e0 0a 00 00        mov      al, byte ptr [ecx + 0xae0]
00705D6C  84 c0                    test     al, al
00705D6E  0f 84 7e 03 00 00        je       0x7060f2
00705D74  8a 85 10 02 00 00        mov      al, byte ptr [ebp + 0x210]
00705D7A  84 c0                    test     al, al
00705D7C  0f 85 70 03 00 00        jne      0x7060f2
00705D82  6a 00                    push     0
00705D84  8b cd                    mov      ecx, ebp
00705D86  e8 85 10 f3 ff           call     0x636e10
00705D8B  8d 9d 64 05 00 00        lea      ebx, [ebp + 0x564]
00705D91  8b f8                    mov      edi, eax
00705D93  c7 44 24 28 00 00 00 00  mov      dword ptr [esp + 0x28], 0
00705D9B  83 3b 00                 cmp      dword ptr [ebx], 0
00705D9E  74 23                    je       0x705dc3
00705DA0  53                       push     ebx
00705DA1  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
00705DA5  e8 46 ee d4 ff           call     0x454bf0
00705DAA  85 c0                    test     eax, eax
00705DAC  7d 0d                    jge      0x705dbb
00705DAE  3d 02 40 00 80           cmp      eax, 0x80004002
00705DB3  74 06                    je       0x705dbb
00705DB5  50                       push     eax
00705DB6  e8 85 fb 08 00           call     0x795940
00705DBB  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
00705DBF  85 c0                    test     eax, eax
00705DC1  75 0e                    jne      0x705dd1
00705DC3  68 03 40 00 80           push     0x80004003
00705DC8  e8 73 fb 08 00           call     0x795940
00705DCD  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
00705DD1  8b 10                    mov      edx, dword ptr [eax]
00705DD3  8d 4c 24 60              lea      ecx, [esp + 0x60]
00705DD7  51                       push     ecx
00705DD8  50                       push     eax
00705DD9  ff 52 0c                 call     dword ptr [edx + 0xc]
00705DDC  85 ff                    test     edi, edi
00705DDE  c6 44 24 14 01           mov      byte ptr [esp + 0x14], 1
00705DE3  0f 84 74 01 00 00        je       0x705f5d
00705DE9  8b 17                    mov      edx, dword ptr [edi]
00705DEB  8b cf                    mov      ecx, edi
00705DED  ff 52 2c                 call     dword ptr [edx + 0x2c]
00705DF0  83 f8 06                 cmp      eax, 6
00705DF3  0f 85 59 01 00 00        jne      0x705f52
00705DF9  8b 07                    mov      eax, dword ptr [edi]
00705DFB  8b cf                    mov      ecx, edi
00705DFD  ff 50 2c                 call     dword ptr [eax + 0x2c]
00705E00  8b f0                    mov      esi, eax
00705E02  83 ee 06                 sub      esi, 6
00705E05  f7 de                    neg      esi
00705E07  1b f6                    sbb      esi, esi
00705E09  f7 d6                    not      esi
00705E0B  23 f7                    and      esi, edi
00705E0D  8b bc 24 94 00 00 00     mov      edi, dword ptr [esp + 0x94]
00705E14  85 ff                    test     edi, edi
00705E16  75 04                    jne      0x705e1c
00705E18  33 c0                    xor      eax, eax
00705E1A  eb 12                    jmp      0x705e2e
00705E1C  8b 17                    mov      edx, dword ptr [edi]
00705E1E  8b cf                    mov      ecx, edi
00705E20  ff 52 2c                 call     dword ptr [edx + 0x2c]
00705E23  83 e8 0b                 sub      eax, 0xb
00705E26  f7 d8                    neg      eax
00705E28  1b c0                    sbb      eax, eax
00705E2A  f7 d0                    not      eax
00705E2C  23 c7                    and      eax, edi
00705E2E  8b 8e 18 04 00 00        mov      ecx, dword ptr [esi + 0x418]
00705E34  8a 91 4d 13 00 00        mov      dl, byte ptr [ecx + 0x134d]
00705E3A  84 d2                    test     dl, dl
00705E3C  0f 84 10 01 00 00        je       0x705f52
00705E42  85 c0                    test     eax, eax
00705E44  0f 84 08 01 00 00        je       0x705f52
00705E4A  6a 00                    push     0
00705E4C  8b c8                    mov      ecx, eax
00705E4E  e8 dd df d6 ff           call     0x473e30
00705E53  85 c0                    test     eax, eax
00705E55  0f 85 f7 00 00 00        jne      0x705f52
00705E5B  b9 04 00 00 00           mov      ecx, 4
00705E60  bf d0 1f 7a 00           mov      edi, 0x7a1fd0
00705E65  8d 74 24 60              lea      esi, [esp + 0x60]
00705E69  33 d2                    xor      edx, edx
00705E6B  f3 a7                    repe cmpsd dword ptr [esi], dword ptr es:[edi]
00705E6D  88 44 24 14              mov      byte ptr [esp + 0x14], al
00705E71  0f 84 db 00 00 00        je       0x705f52
00705E77  8b 03                    mov      eax, dword ptr [ebx]
00705E79  89 54 24 18              mov      dword ptr [esp + 0x18], edx
00705E7D  85 c0                    test     eax, eax
00705E7F  0f 84 83 00 00 00        je       0x705f08
00705E85  53                       push     ebx
00705E86  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
00705E8A  e8 e1 ed d4 ff           call     0x454c70
00705E8F  85 c0                    test     eax, eax
00705E91  7d 0d                    jge      0x705ea0
00705E93  3d 02 40 00 80           cmp      eax, 0x80004002
00705E98  74 06                    je       0x705ea0
00705E9A  50                       push     eax
00705E9B  e8 a0 fa 08 00           call     0x795940
00705EA0  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705EA4  85 c0                    test     eax, eax
00705EA6  74 5b                    je       0x705f03
00705EA8  8b 08                    mov      ecx, dword ptr [eax]
00705EAA  50                       push     eax
00705EAB  ff 51 1c                 call     dword ptr [ecx + 0x1c]
00705EAE  84 c0                    test     al, al
00705EB0  74 51                    je       0x705f03
00705EB2  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705EB6  85 c0                    test     eax, eax
00705EB8  75 0e                    jne      0x705ec8
00705EBA  68 03 40 00 80           push     0x80004003
00705EBF  e8 7c fa 08 00           call     0x795940
00705EC4  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705EC8  8b 10                    mov      edx, dword ptr [eax]
00705ECA  50                       push     eax
00705ECB  ff 52 14                 call     dword ptr [edx + 0x14]
00705ECE  84 c0                    test     al, al
00705ED0  74 31                    je       0x705f03
00705ED2  8b 03                    mov      eax, dword ptr [ebx]
00705ED4  85 c0                    test     eax, eax
00705ED6  74 06                    je       0x705ede
00705ED8  8b 08                    mov      ecx, dword ptr [eax]
00705EDA  50                       push     eax
00705EDB  ff 51 08                 call     dword ptr [ecx + 8]
00705EDE  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705EE2  c7 03 00 00 00 00        mov      dword ptr [ebx], 0
00705EE8  85 c0                    test     eax, eax
00705EEA  75 0e                    jne      0x705efa
00705EEC  68 03 40 00 80           push     0x80004003
00705EF1  e8 4a fa 08 00           call     0x795940
00705EF6  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705EFA  8b 10                    mov      edx, dword ptr [eax]
00705EFC  53                       push     ebx
00705EFD  50                       push     eax
00705EFE  ff 52 10                 call     dword ptr [edx + 0x10]
00705F01  eb 41                    jmp      0x705f44
00705F03  83 3b 00                 cmp      dword ptr [ebx], 0
00705F06  75 0a                    jne      0x705f12
00705F08  68 03 40 00 80           push     0x80004003
00705F0D  e8 2e fa 08 00           call     0x795940
00705F12  8b 03                    mov      eax, dword ptr [ebx]
00705F14  50                       push     eax
00705F15  8b 08                    mov      ecx, dword ptr [eax]
00705F17  ff 51 48                 call     dword ptr [ecx + 0x48]
00705F1A  8b 55 00                 mov      edx, dword ptr [ebp]
00705F1D  6a ff                    push     -1
00705F1F  8b cd                    mov      ecx, ebp
00705F21  ff 92 d8 01 00 00        call     dword ptr [edx + 0x1d8]
00705F27  8b 45 00                 mov      eax, dword ptr [ebp]
00705F2A  6a 00                    push     0
00705F2C  6a 07                    push     7
00705F2E  8b cd                    mov      ecx, ebp
00705F30  ff 90 d0 01 00 00        call     dword ptr [eax + 0x1d0]
00705F36  c6 85 98 05 00 00 01     mov      byte ptr [ebp + 0x598], 1
00705F3D  c6 85 90 01 00 00 01     mov      byte ptr [ebp + 0x190], 1
00705F44  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705F48  85 c0                    test     eax, eax
00705F4A  74 06                    je       0x705f52
00705F4C  8b 08                    mov      ecx, dword ptr [eax]
00705F4E  50                       push     eax
00705F4F  ff 51 08                 call     dword ptr [ecx + 8]
00705F52  80 7c 24 14 01           cmp      byte ptr [esp + 0x14], 1
00705F57  0f 85 87 01 00 00        jne      0x7060e4
00705F5D  b9 04 00 00 00           mov      ecx, 4
00705F62  bf 70 1f 7a 00           mov      edi, 0x7a1f70
00705F67  8d 74 24 60              lea      esi, [esp + 0x60]
00705F6B  33 d2                    xor      edx, edx
00705F6D  f3 a7                    repe cmpsd dword ptr [esi], dword ptr es:[edi]
00705F6F  0f 84 6f 01 00 00        je       0x7060e4
00705F75  8b 03                    mov      eax, dword ptr [ebx]
00705F77  33 ff                    xor      edi, edi
00705F79  3b c7                    cmp      eax, edi
00705F7B  89 7c 24 18              mov      dword ptr [esp + 0x18], edi
00705F7F  74 78                    je       0x705ff9
00705F81  53                       push     ebx
00705F82  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
00705F86  e8 e5 ec d4 ff           call     0x454c70
00705F8B  3b c7                    cmp      eax, edi
00705F8D  7d 0d                    jge      0x705f9c
00705F8F  3d 02 40 00 80           cmp      eax, 0x80004002
00705F94  74 06                    je       0x705f9c
00705F96  50                       push     eax
00705F97  e8 a4 f9 08 00           call     0x795940
00705F9C  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705FA0  3b c7                    cmp      eax, edi
00705FA2  74 55                    je       0x705ff9
00705FA4  8b 08                    mov      ecx, dword ptr [eax]
00705FA6  50                       push     eax
00705FA7  ff 51 1c                 call     dword ptr [ecx + 0x1c]
00705FAA  84 c0                    test     al, al
00705FAC  74 4b                    je       0x705ff9
00705FAE  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705FB2  3b c7                    cmp      eax, edi
00705FB4  75 0e                    jne      0x705fc4
00705FB6  68 03 40 00 80           push     0x80004003
00705FBB  e8 80 f9 08 00           call     0x795940
00705FC0  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705FC4  8b 10                    mov      edx, dword ptr [eax]
00705FC6  50                       push     eax
00705FC7  ff 52 14                 call     dword ptr [edx + 0x14]
00705FCA  84 c0                    test     al, al
00705FCC  74 2b                    je       0x705ff9
00705FCE  8b 03                    mov      eax, dword ptr [ebx]
00705FD0  3b c7                    cmp      eax, edi
00705FD2  74 06                    je       0x705fda
00705FD4  8b 08                    mov      ecx, dword ptr [eax]
00705FD6  50                       push     eax
00705FD7  ff 51 08                 call     dword ptr [ecx + 8]
00705FDA  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705FDE  89 3b                    mov      dword ptr [ebx], edi
00705FE0  3b c7                    cmp      eax, edi
00705FE2  75 0e                    jne      0x705ff2
00705FE4  68 03 40 00 80           push     0x80004003
00705FE9  e8 52 f9 08 00           call     0x795940
00705FEE  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00705FF2  8b 10                    mov      edx, dword ptr [eax]
00705FF4  53                       push     ebx
00705FF5  50                       push     eax
00705FF6  ff 52 10                 call     dword ptr [edx + 0x10]
00705FF9  6a 07                    push     7
00705FFB  57                       push     edi
00705FFC  68 70 1f 7a 00           push     0x7a1f70
00706001  8d 4c 24 28              lea      ecx, [esp + 0x28]
00706005  89 7c 24 28              mov      dword ptr [esp + 0x28], edi
00706009  e8 42 56 d1 ff           call     0x41b650
0070600E  3b c7                    cmp      eax, edi
00706010  7d 0d                    jge      0x70601f
00706012  3d 02 40 00 80           cmp      eax, 0x80004002
00706017  74 06                    je       0x70601f
00706019  50                       push     eax
0070601A  e8 21 f9 08 00           call     0x795940
0070601F  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00706023  3b c7                    cmp      eax, edi
00706025  75 0e                    jne      0x706035
00706027  68 03 40 00 80           push     0x80004003
0070602C  e8 0f f9 08 00           call     0x795940
00706031  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00706035  8b 08                    mov      ecx, dword ptr [eax]
00706037  55                       push     ebp
00706038  50                       push     eax
00706039  ff 51 0c                 call     dword ptr [ecx + 0xc]
0070603C  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
00706040  33 c0                    xor      eax, eax
00706042  3b cf                    cmp      ecx, edi
00706044  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
00706048  74 23                    je       0x70606d
0070604A  8d 54 24 1c              lea      edx, [esp + 0x1c]
0070604E  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
00706052  52                       push     edx
00706053  e8 18 ec d4 ff           call     0x454c70
00706058  3b c7                    cmp      eax, edi
0070605A  7d 0d                    jge      0x706069
0070605C  3d 02 40 00 80           cmp      eax, 0x80004002
00706061  74 06                    je       0x706069
00706063  50                       push     eax
00706064  e8 d7 f8 08 00           call     0x795940
00706069  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
0070606D  8b 74 24 18              mov      esi, dword ptr [esp + 0x18]
00706071  3b f0                    cmp      esi, eax
00706073  74 1b                    je       0x706090
00706075  8d 4c 24 18              lea      ecx, [esp + 0x18]
00706079  89 44 24 18              mov      dword ptr [esp + 0x18], eax
0070607D  e8 9e 8c f9 ff           call     0x69ed20
00706082  3b f7                    cmp      esi, edi
00706084  74 06                    je       0x70608c
00706086  8b 06                    mov      eax, dword ptr [esi]
00706088  56                       push     esi
00706089  ff 50 08                 call     dword ptr [eax + 8]
0070608C  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
00706090  3b c7                    cmp      eax, edi
00706092  74 06                    je       0x70609a
00706094  8b 08                    mov      ecx, dword ptr [eax]
00706096  50                       push     eax
00706097  ff 51 08                 call     dword ptr [ecx + 8]
0070609A  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070609E  3b cf                    cmp      ecx, edi
007060A0  74 26                    je       0x7060c8
007060A2  8b 03                    mov      eax, dword ptr [ebx]
007060A4  8b 11                    mov      edx, dword ptr [ecx]
007060A6  50                       push     eax
007060A7  51                       push     ecx
007060A8  ff 52 0c                 call     dword ptr [edx + 0xc]
007060AB  8b 33                    mov      esi, dword ptr [ebx]
007060AD  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
007060B1  3b f0                    cmp      esi, eax
007060B3  74 13                    je       0x7060c8
007060B5  8b cb                    mov      ecx, ebx
007060B7  89 03                    mov      dword ptr [ebx], eax
007060B9  e8 e2 dd d4 ff           call     0x453ea0
007060BE  3b f7                    cmp      esi, edi
007060C0  74 06                    je       0x7060c8
007060C2  8b 06                    mov      eax, dword ptr [esi]
007060C4  56                       push     esi
007060C5  ff 50 08                 call     dword ptr [eax + 8]
007060C8  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
007060CC  3b c7                    cmp      eax, edi
007060CE  74 06                    je       0x7060d6
007060D0  8b 08                    mov      ecx, dword ptr [eax]
007060D2  50                       push     eax
007060D3  ff 51 08                 call     dword ptr [ecx + 8]
007060D6  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
007060DA  3b c7                    cmp      eax, edi
007060DC  74 06                    je       0x7060e4
007060DE  8b 10                    mov      edx, dword ptr [eax]
007060E0  50                       push     eax
007060E1  ff 52 08                 call     dword ptr [edx + 8]
007060E4  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
007060E8  85 c0                    test     eax, eax
007060EA  74 06                    je       0x7060f2
007060EC  8b 08                    mov      ecx, dword ptr [eax]
007060EE  50                       push     eax
007060EF  ff 51 08                 call     dword ptr [ecx + 8]
007060F2  8b 9c 24 94 00 00 00     mov      ebx, dword ptr [esp + 0x94]
007060F9  85 db                    test     ebx, ebx
007060FB  0f 84 45 04 00 00        je       0x706546
00706101  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
00706107  8d b5 64 05 00 00        lea      esi, [ebp + 0x564]
0070610D  85 c0                    test     eax, eax
0070610F  75 0a                    jne      0x70611b
00706111  68 03 40 00 80           push     0x80004003
00706116  e8 25 f8 08 00           call     0x795940
0070611B  8b 06                    mov      eax, dword ptr [esi]
0070611D  50                       push     eax
0070611E  8b 10                    mov      edx, dword ptr [eax]
00706120  ff 52 10                 call     dword ptr [edx + 0x10]
00706123  84 c0                    test     al, al
00706125  0f 85 1b 04 00 00        jne      0x706546
0070612B  8b 06                    mov      eax, dword ptr [esi]
0070612D  c7 44 24 2c 00 00 00 00  mov      dword ptr [esp + 0x2c], 0
00706135  85 c0                    test     eax, eax
00706137  74 56                    je       0x70618f
00706139  8b ce                    mov      ecx, esi
0070613B  e8 50 7d dc ff           call     0x4cde90
00706140  8b 08                    mov      ecx, dword ptr [eax]
00706142  8d 54 24 28              lea      edx, [esp + 0x28]
00706146  52                       push     edx
00706147  68 08 f2 7c 00           push     0x7cf208
0070614C  50                       push     eax
0070614D  ff 11                    call     dword ptr [ecx]
0070614F  8b f0                    mov      esi, eax
00706151  85 f6                    test     esi, esi
00706153  7d 0d                    jge      0x706162
00706155  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
00706159  e8 a2 eb d9 ff           call     0x4a4d00
0070615E  33 c0                    xor      eax, eax
00706160  eb 0f                    jmp      0x706171
00706162  8b 7c 24 28              mov      edi, dword ptr [esp + 0x28]
00706166  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
0070616A  e8 91 eb d9 ff           call     0x4a4d00
0070616F  8b c7                    mov      eax, edi
00706171  85 f6                    test     esi, esi
00706173  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
00706177  7d 12                    jge      0x70618b
00706179  81 fe 02 40 00 80        cmp      esi, 0x80004002
0070617F  74 0a                    je       0x70618b
00706181  56                       push     esi
00706182  e8 b9 f7 08 00           call     0x795940
00706187  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
0070618B  85 c0                    test     eax, eax
0070618D  75 0e                    jne      0x70619d
0070618F  68 03 40 00 80           push     0x80004003
00706194  e8 a7 f7 08 00           call     0x795940
00706199  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
0070619D  8b 08                    mov      ecx, dword ptr [eax]
0070619F  8d 94 24 80 00 00 00     lea      edx, [esp + 0x80]
007061A6  52                       push     edx
007061A7  50                       push     eax
007061A8  ff 51 0c                 call     dword ptr [ecx + 0xc]
007061AB  b9 04 00 00 00           mov      ecx, 4
007061B0  bf 90 1f 7a 00           mov      edi, 0x7a1f90
007061B5  8d b4 24 80 00 00 00     lea      esi, [esp + 0x80]
007061BC  33 c0                    xor      eax, eax
007061BE  f3 a7                    repe cmpsd dword ptr [esi], dword ptr es:[edi]
007061C0  0f 85 72 03 00 00        jne      0x706538
007061C6  8b 55 00                 mov      edx, dword ptr [ebp]
007061C9  8b cd                    mov      ecx, ebp
007061CB  ff 92 b0 01 00 00        call     dword ptr [edx + 0x1b0]
007061D1  85 c0                    test     eax, eax
007061D3  0f 85 5f 03 00 00        jne      0x706538
007061D9  8b 03                    mov      eax, dword ptr [ebx]
007061DB  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
007061DF  51                       push     ecx
007061E0  8b cb                    mov      ecx, ebx
007061E2  ff 50 48                 call     dword ptr [eax + 0x48]
007061E5  8b 10                    mov      edx, dword ptr [eax]
007061E7  89 54 24 48              mov      dword ptr [esp + 0x48], edx
007061EB  8b 48 04                 mov      ecx, dword ptr [eax + 4]
007061EE  89 4c 24 4c              mov      dword ptr [esp + 0x4c], ecx
007061F2  b9 e0 24 83 00           mov      ecx, 0x8324e0
007061F7  8b 50 08                 mov      edx, dword ptr [eax + 8]
007061FA  8d 44 24 48              lea      eax, [esp + 0x48]
007061FE  50                       push     eax
007061FF  89 54 24 54              mov      dword ptr [esp + 0x54], edx
00706203  e8 78 40 e5 ff           call     0x55a280
00706208  39 44 24 50              cmp      dword ptr [esp + 0x50], eax
0070620C  7d 04                    jge      0x706212
0070620E  89 44 24 50              mov      dword ptr [esp + 0x50], eax
00706212  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
00706216  84 c0                    test     al, al
00706218  0f 85 e8 00 00 00        jne      0x706306
0070621E  8b 55 00                 mov      edx, dword ptr [ebp]
00706221  6a 00                    push     0
00706223  8b cd                    mov      ecx, ebp
00706225  ff 92 b8 00 00 00        call     dword ptr [edx + 0xb8]
0070622B  84 c0                    test     al, al
0070622D  0f 85 d3 00 00 00        jne      0x706306
00706233  8b 03                    mov      eax, dword ptr [ebx]
00706235  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
00706239  51                       push     ecx
0070623A  8b cb                    mov      ecx, ebx
0070623C  ff 50 48                 call     dword ptr [eax + 0x48]
0070623F  50                       push     eax
00706240  b9 e0 24 83 00           mov      ecx, 0x8324e0
00706245  e8 b6 1d e4 ff           call     0x548000
0070624A  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
00706250  f6 c5 01                 test     ch, 1
00706253  0f 85 ad 00 00 00        jne      0x706306
00706259  8b 55 00                 mov      edx, dword ptr [ebp]
0070625C  8d 44 24 1c              lea      eax, [esp + 0x1c]
00706260  6a 00                    push     0
00706262  50                       push     eax
00706263  8b cd                    mov      ecx, ebp
00706265  ff 52 4c                 call     dword ptr [edx + 0x4c]
00706268  50                       push     eax
00706269  b9 e0 24 83 00           mov      ecx, 0x8324e0
0070626E  e8 8d 1d e4 ff           call     0x548000
00706273  8b c8                    mov      ecx, eax
00706275  e8 86 5f d7 ff           call     0x47c200
0070627A  84 c0                    test     al, al
0070627C  0f 84 84 00 00 00        je       0x706306
00706282  8b 13                    mov      edx, dword ptr [ebx]
00706284  8d 44 24 60              lea      eax, [esp + 0x60]
00706288  50                       push     eax
00706289  8b cb                    mov      ecx, ebx
0070628B  ff 52 48                 call     dword ptr [edx + 0x48]
0070628E  50                       push     eax
0070628F  b9 e0 24 83 00           mov      ecx, 0x8324e0
00706294  e8 67 1d e4 ff           call     0x548000
00706299  8b c8                    mov      ecx, eax
0070629B  e8 60 5f d7 ff           call     0x47c200
007062A0  84 c0                    test     al, al
007062A2  74 62                    je       0x706306
007062A4  8b 13                    mov      edx, dword ptr [ebx]
007062A6  8d 44 24 60              lea      eax, [esp + 0x60]
007062AA  50                       push     eax
007062AB  8b cb                    mov      ecx, ebx
007062AD  ff 52 48                 call     dword ptr [edx + 0x48]
007062B0  8b c8                    mov      ecx, eax
007062B2  8b 01                    mov      eax, dword ptr [ecx]
007062B4  99                       cdq      
007062B5  81 e2 ff 00 00 00        and      edx, 0xff
007062BB  03 c2                    add      eax, edx
007062BD  c1 f8 08                 sar      eax, 8
007062C0  66 89 44 24 28           mov      word ptr [esp + 0x28], ax
007062C5  8b 41 04                 mov      eax, dword ptr [ecx + 4]
007062C8  99                       cdq      
007062C9  81 e2 ff 00 00 00        and      edx, 0xff
007062CF  03 c2                    add      eax, edx
007062D1  8d 54 24 1c              lea      edx, [esp + 0x1c]
007062D5  c1 f8 08                 sar      eax, 8
007062D8  66 89 44 24 2a           mov      word ptr [esp + 0x2a], ax
007062DD  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
007062E1  8b 45 00                 mov      eax, dword ptr [ebp]
007062E4  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
007062E8  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
007062EC  52                       push     edx
007062ED  51                       push     ecx
007062EE  8b cd                    mov      ecx, ebp
007062F0  ff 90 a8 01 00 00        call     dword ptr [eax + 0x1a8]
007062F6  50                       push     eax
007062F7  8b cd                    mov      ecx, ebp
007062F9  e8 92 34 00 00           call     0x709790
007062FE  84 c0                    test     al, al
00706300  0f 85 32 02 00 00        jne      0x706538
00706306  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
0070630C  8d 9d 64 05 00 00        lea      ebx, [ebp + 0x564]
00706312  85 c0                    test     eax, eax
00706314  c7 44 24 18 00 00 00 00  mov      dword ptr [esp + 0x18], 0
0070631C  0f 84 8f 00 00 00        je       0x7063b1
00706322  8b cb                    mov      ecx, ebx
00706324  e8 67 7b dc ff           call     0x4cde90
00706329  8b 10                    mov      edx, dword ptr [eax]
0070632B  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
0070632F  51                       push     ecx
00706330  68 30 fc 7c 00           push     0x7cfc30
00706335  50                       push     eax
00706336  ff 12                    call     dword ptr [edx]
00706338  8b f0                    mov      esi, eax
0070633A  85 f6                    test     esi, esi
0070633C  7d 0d                    jge      0x70634b
0070633E  8d 4c 24 18              lea      ecx, [esp + 0x18]
00706342  e8 19 35 e0 ff           call     0x509860
00706347  33 c0                    xor      eax, eax
00706349  eb 0f                    jmp      0x70635a
0070634B  8b 7c 24 1c              mov      edi, dword ptr [esp + 0x1c]
0070634F  8d 4c 24 18              lea      ecx, [esp + 0x18]
00706353  e8 08 35 e0 ff           call     0x509860
00706358  8b c7                    mov      eax, edi
0070635A  85 f6                    test     esi, esi
0070635C  89 44 24 18              mov      dword ptr [esp + 0x18], eax
00706360  7d 12                    jge      0x706374
00706362  81 fe 02 40 00 80        cmp      esi, 0x80004002
00706368  74 0a                    je       0x706374
0070636A  56                       push     esi
0070636B  e8 d0 f5 08 00           call     0x795940
00706370  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00706374  85 c0                    test     eax, eax
00706376  74 39                    je       0x7063b1
00706378  8b 10                    mov      edx, dword ptr [eax]
0070637A  50                       push     eax
0070637B  ff 52 1c                 call     dword ptr [edx + 0x1c]
0070637E  84 c0                    test     al, al
00706380  74 2f                    je       0x7063b1
00706382  8b 03                    mov      eax, dword ptr [ebx]
00706384  85 c0                    test     eax, eax
00706386  74 06                    je       0x70638e
00706388  8b 08                    mov      ecx, dword ptr [eax]
0070638A  50                       push     eax
0070638B  ff 51 08                 call     dword ptr [ecx + 8]
0070638E  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00706392  c7 03 00 00 00 00        mov      dword ptr [ebx], 0
00706398  85 c0                    test     eax, eax
0070639A  75 0e                    jne      0x7063aa
0070639C  68 03 40 00 80           push     0x80004003
007063A1  e8 9a f5 08 00           call     0x795940
007063A6  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
007063AA  8b 10                    mov      edx, dword ptr [eax]
007063AC  53                       push     ebx
007063AD  50                       push     eax
007063AE  ff 52 10                 call     dword ptr [edx + 0x10]
007063B1  6a 07                    push     7
007063B3  6a 00                    push     0
007063B5  68 70 1f 7a 00           push     0x7a1f70
007063BA  8d 4c 24 34              lea      ecx, [esp + 0x34]
007063BE  c7 44 24 34 00 00 00 00  mov      dword ptr [esp + 0x34], 0
007063C6  e8 85 52 d1 ff           call     0x41b650
007063CB  85 c0                    test     eax, eax
007063CD  7d 0d                    jge      0x7063dc
007063CF  3d 02 40 00 80           cmp      eax, 0x80004002
007063D4  74 06                    je       0x7063dc
007063D6  50                       push     eax
007063D7  e8 64 f5 08 00           call     0x795940
007063DC  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
007063E0  85 c0                    test     eax, eax
007063E2  75 0e                    jne      0x7063f2
007063E4  68 03 40 00 80           push     0x80004003
007063E9  e8 52 f5 08 00           call     0x795940
007063EE  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
007063F2  8b 08                    mov      ecx, dword ptr [eax]
007063F4  55                       push     ebp
007063F5  50                       push     eax
007063F6  ff 51 0c                 call     dword ptr [ecx + 0xc]
007063F9  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
007063FD  33 c0                    xor      eax, eax
007063FF  85 c9                    test     ecx, ecx
00706401  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
00706405  74 54                    je       0x70645b
00706407  8d 4c 24 28              lea      ecx, [esp + 0x28]
0070640B  e8 80 7a dc ff           call     0x4cde90
00706410  8b 10                    mov      edx, dword ptr [eax]
00706412  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
00706416  51                       push     ecx
00706417  68 30 fc 7c 00           push     0x7cfc30
0070641C  50                       push     eax
0070641D  ff 12                    call     dword ptr [edx]
0070641F  8b f0                    mov      esi, eax
00706421  85 f6                    test     esi, esi
00706423  7d 0d                    jge      0x706432
00706425  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
00706429  e8 32 34 e0 ff           call     0x509860
0070642E  33 c0                    xor      eax, eax
00706430  eb 0f                    jmp      0x706441
00706432  8b 7c 24 3c              mov      edi, dword ptr [esp + 0x3c]
00706436  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
0070643A  e8 21 34 e0 ff           call     0x509860
0070643F  8b c7                    mov      eax, edi
00706441  85 f6                    test     esi, esi
00706443  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
00706447  7d 12                    jge      0x70645b
00706449  81 fe 02 40 00 80        cmp      esi, 0x80004002
0070644F  74 0a                    je       0x70645b
00706451  56                       push     esi
00706452  e8 e9 f4 08 00           call     0x795940
00706457  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
0070645B  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070645F  3b c8                    cmp      ecx, eax
00706461  74 2c                    je       0x70648f
00706463  8b f1                    mov      esi, ecx
00706465  8b c8                    mov      ecx, eax
00706467  85 c0                    test     eax, eax
00706469  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
0070646D  74 0e                    je       0x70647d
0070646F  8b 10                    mov      edx, dword ptr [eax]
00706471  50                       push     eax
00706472  ff 52 04                 call     dword ptr [edx + 4]
00706475  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
00706479  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
0070647D  85 f6                    test     esi, esi
0070647F  74 0e                    je       0x70648f
00706481  8b 06                    mov      eax, dword ptr [esi]
00706483  56                       push     esi
00706484  ff 50 08                 call     dword ptr [eax + 8]
00706487  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070648B  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
0070648F  85 c0                    test     eax, eax
00706491  74 0a                    je       0x70649d
00706493  8b 08                    mov      ecx, dword ptr [eax]
00706495  50                       push     eax
00706496  ff 51 08                 call     dword ptr [ecx + 8]
00706499  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070649D  85 c9                    test     ecx, ecx
0070649F  74 7b                    je       0x70651c
007064A1  8b 03                    mov      eax, dword ptr [ebx]
007064A3  8b 11                    mov      edx, dword ptr [ecx]
007064A5  50                       push     eax
007064A6  51                       push     ecx
007064A7  ff 52 0c                 call     dword ptr [edx + 0xc]
007064AA  8b 33                    mov      esi, dword ptr [ebx]
007064AC  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
007064B0  3b f0                    cmp      esi, eax
007064B2  74 16                    je       0x7064ca
007064B4  85 c0                    test     eax, eax
007064B6  89 03                    mov      dword ptr [ebx], eax
007064B8  74 06                    je       0x7064c0
007064BA  8b 08                    mov      ecx, dword ptr [eax]
007064BC  50                       push     eax
007064BD  ff 51 04                 call     dword ptr [ecx + 4]
007064C0  85 f6                    test     esi, esi
007064C2  74 06                    je       0x7064ca
007064C4  8b 16                    mov      edx, dword ptr [esi]
007064C6  56                       push     esi
007064C7  ff 52 08                 call     dword ptr [edx + 8]
007064CA  8d 85 88 00 00 00        lea      eax, [ebp + 0x88]
007064D0  8b 8d 88 00 00 00        mov      ecx, dword ptr [ebp + 0x88]
007064D6  89 4c 24 3c              mov      dword ptr [esp + 0x3c], ecx
007064DA  8b 50 04                 mov      edx, dword ptr [eax + 4]
007064DD  89 54 24 40              mov      dword ptr [esp + 0x40], edx
007064E1  8b 40 08                 mov      eax, dword ptr [eax + 8]
007064E4  89 44 24 44              mov      dword ptr [esp + 0x44], eax
007064E8  8b 03                    mov      eax, dword ptr [ebx]
007064EA  85 c0                    test     eax, eax
007064EC  75 0a                    jne      0x7064f8
007064EE  68 03 40 00 80           push     0x80004003
007064F3  e8 48 f4 08 00           call     0x795940
007064F8  8b 33                    mov      esi, dword ptr [ebx]
007064FA  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
007064FE  51                       push     ecx
007064FF  b9 e0 24 83 00           mov      ecx, 0x8324e0
00706504  8b 3e                    mov      edi, dword ptr [esi]
00706506  e8 f5 1a e4 ff           call     0x548000
0070650B  33 d2                    xor      edx, edx
0070650D  8a 90 1c 01 00 00        mov      dl, byte ptr [eax + 0x11c]
00706513  52                       push     edx
00706514  56                       push     esi
00706515  ff 57 7c                 call     dword ptr [edi + 0x7c]
00706518  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070651C  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
00706520  85 c0                    test     eax, eax
00706522  74 0a                    je       0x70652e
00706524  8b 08                    mov      ecx, dword ptr [eax]
00706526  50                       push     eax
00706527  ff 51 08                 call     dword ptr [ecx + 8]
0070652A  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
0070652E  85 c9                    test     ecx, ecx
00706530  74 06                    je       0x706538
00706532  8b 11                    mov      edx, dword ptr [ecx]
00706534  51                       push     ecx
00706535  ff 52 08                 call     dword ptr [edx + 8]
00706538  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
0070653C  85 c0                    test     eax, eax
0070653E  74 06                    je       0x706546
00706540  8b 08                    mov      ecx, dword ptr [eax]
00706542  50                       push     eax
00706543  ff 51 08                 call     dword ptr [ecx + 8]
00706546  8b 5c 24 38              mov      ebx, dword ptr [esp + 0x38]
0070654A  85 db                    test     ebx, ebx
0070654C  0f 84 a8 00 00 00        je       0x7065fa
00706552  8b 93 18 04 00 00        mov      edx, dword ptr [ebx + 0x418]
00706558  8a 82 49 13 00 00        mov      al, byte ptr [edx + 0x1349]
0070655E  84 c0                    test     al, al
00706560  0f 84 94 00 00 00        je       0x7065fa
00706566  8b cb                    mov      ecx, ebx
00706568  e8 a3 09 f3 ff           call     0x636f10
0070656D  84 c0                    test     al, al
0070656F  74 1e                    je       0x70658f
00706571  6a 00                    push     0
00706573  8b cb                    mov      ecx, ebx
00706575  e8 96 08 f3 ff           call     0x636e10
0070657A  3b c5                    cmp      eax, ebp
0070657C  74 11                    je       0x70658f
0070657E  8b bc 24 94 00 00 00     mov      edi, dword ptr [esp + 0x94]
00706585  8b cd                    mov      ecx, ebp
00706587  57                       push     edi
00706588  e8 c3 08 fd ff           call     0x6d6e50
0070658D  eb 72                    jmp      0x706601
0070658F  8b 45 00                 mov      eax, dword ptr [ebp]
00706592  53                       push     ebx
00706593  6a 02                    push     2
00706595  8b cd                    mov      ecx, ebp
00706597  ff 90 58 02 00 00        call     dword ptr [eax + 0x258]
0070659D  83 f8 01                 cmp      eax, 1
007065A0  75 58                    jne      0x7065fa
007065A2  8b 55 00                 mov      edx, dword ptr [ebp]
007065A5  6a 0e                    push     0xe
007065A7  8b cd                    mov      ecx, ebp
007065A9  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
007065AF  83 f8 01                 cmp      eax, 1
007065B2  75 2e                    jne      0x7065e2
007065B4  8b 84 24 98 00 00 00     mov      eax, dword ptr [esp + 0x98]
007065BB  8b 8c 24 94 00 00 00     mov      ecx, dword ptr [esp + 0x94]
007065C2  50                       push     eax
007065C3  51                       push     ecx
007065C4  8b cd                    mov      ecx, ebp
007065C6  e8 65 1a dc ff           call     0x4c8030
007065CB  5f                       pop      edi
007065CC  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
007065D6  5e                       pop      esi
007065D7  5d                       pop      ebp
007065D8  5b                       pop      ebx
007065D9  81 c4 80 00 00 00        add      esp, 0x80
007065DF  c2 08 00                 ret      8
007065E2  8b 55 00                 mov      edx, dword ptr [ebp]
007065E5  6a 03                    push     3
007065E7  8b cd                    mov      ecx, ebp
007065E9  ff 92 54 02 00 00        call     dword ptr [edx + 0x254]
007065EF  33 ff                    xor      edi, edi
007065F1  89 bc 24 94 00 00 00     mov      dword ptr [esp + 0x94], edi
007065F8  eb 07                    jmp      0x706601
007065FA  8b bc 24 94 00 00 00     mov      edi, dword ptr [esp + 0x94]
00706601  6a 00                    push     0
00706603  8b cd                    mov      ecx, ebp
00706605  e8 06 08 f3 ff           call     0x636e10
0070660A  8b f0                    mov      esi, eax
0070660C  85 f6                    test     esi, esi
0070660E  0f 84 d3 00 00 00        je       0x7066e7
00706614  8b 06                    mov      eax, dword ptr [esi]
00706616  8b ce                    mov      ecx, esi
00706618  ff 50 2c                 call     dword ptr [eax + 0x2c]
0070661B  83 f8 06                 cmp      eax, 6
0070661E  0f 85 c3 00 00 00        jne      0x7066e7
00706624  8b 8e 18 04 00 00        mov      ecx, dword ptr [esi + 0x418]
0070662A  8a 81 57 13 00 00        mov      al, byte ptr [ecx + 0x1357]
00706630  84 c0                    test     al, al
00706632  0f 84 af 00 00 00        je       0x7066e7
00706638  83 bd 98 00 00 00 07     cmp      dword ptr [ebp + 0x98], 7
0070663F  0f 84 a2 00 00 00        je       0x7066e7
00706645  81 c6 88 00 00 00        add      esi, 0x88
0070664B  8b 06                    mov      eax, dword ptr [esi]
0070664D  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
00706650  8b 56 08                 mov      edx, dword ptr [esi + 8]
00706653  89 54 24 68              mov      dword ptr [esp + 0x68], edx
00706657  99                       cdq      
00706658  81 e2 ff 00 00 00        and      edx, 0xff
0070665E  03 c2                    add      eax, edx
00706660  c1 f8 08                 sar      eax, 8
00706663  66 89 44 24 3c           mov      word ptr [esp + 0x3c], ax
00706668  8b c1                    mov      eax, ecx
0070666A  99                       cdq      
0070666B  81 e2 ff 00 00 00        and      edx, 0xff
00706671  03 c2                    add      eax, edx
00706673  c1 f8 08                 sar      eax, 8
00706676  66 89 44 24 3e           mov      word ptr [esp + 0x3e], ax
0070667B  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
0070667F  8b 4c 24 3e              mov      ecx, dword ptr [esp + 0x3e]
00706683  83 c0 05                 add      eax, 5
00706686  41                       inc      ecx
00706687  66 89 44 24 38           mov      word ptr [esp + 0x38], ax
0070668C  66 89 4c 24 3a           mov      word ptr [esp + 0x3a], cx
00706691  8b 54 24 38              mov      edx, dword ptr [esp + 0x38]
00706695  8d 44 24 3c              lea      eax, [esp + 0x3c]
00706699  b9 e0 24 83 00           mov      ecx, 0x8324e0
0070669E  50                       push     eax
0070669F  89 54 24 40              mov      dword ptr [esp + 0x40], edx
007066A3  e8 c8 19 e4 ff           call     0x548070
007066A8  3b f8                    cmp      edi, eax
007066AA  74 3b                    je       0x7066e7
007066AC  8b 95 9c 04 00 00        mov      edx, dword ptr [ebp + 0x49c]
007066B2  8d 8d 9c 04 00 00        lea      ecx, [ebp + 0x49c]
007066B8  ff 52 0c                 call     dword ptr [edx + 0xc]
007066BB  8b 85 78 04 00 00        mov      eax, dword ptr [ebp + 0x478]
007066C1  8d 8d 78 04 00 00        lea      ecx, [ebp + 0x478]
007066C7  ff 50 0c                 call     dword ptr [eax + 0xc]
007066CA  85 ff                    test     edi, edi
007066CC  0f 84 24 03 00 00        je       0x7069f6
007066D2  57                       push     edi
007066D3  8b cd                    mov      ecx, ebp
007066D5  e8 d6 24 dc ff           call     0x4c8bb0
007066DA  5f                       pop      edi
007066DB  5e                       pop      esi
007066DC  5d                       pop      ebp
007066DD  5b                       pop      ebx
007066DE  81 c4 80 00 00 00        add      esp, 0x80
007066E4  c2 08 00                 ret      8
007066E7  85 db                    test     ebx, ebx
007066E9  0f 84 f9 00 00 00        je       0x7067e8
007066EF  8b 8d ac 05 00 00        mov      ecx, dword ptr [ebp + 0x5ac]
007066F5  8b 81 bc 03 00 00        mov      eax, dword ptr [ecx + 0x3bc]
007066FB  85 c0                    test     eax, eax
007066FD  0f 8e e5 00 00 00        jle      0x7067e8
00706703  8b 91 bc 03 00 00        mov      edx, dword ptr [ecx + 0x3bc]
00706709  33 c0                    xor      eax, eax
0070670B  85 d2                    test     edx, edx
0070670D  0f 8e d5 00 00 00        jle      0x7067e8
00706713  8b b3 18 04 00 00        mov      esi, dword ptr [ebx + 0x418]
00706719  8b 89 b0 03 00 00        mov      ecx, dword ptr [ecx + 0x3b0]
0070671F  39 31                    cmp      dword ptr [ecx], esi
00706721  74 0d                    je       0x706730
00706723  40                       inc      eax
00706724  83 c1 04                 add      ecx, 4
00706727  3b c2                    cmp      eax, edx
00706729  7c f4                    jl       0x70671f
0070672B  e9 b8 00 00 00           jmp      0x7067e8
00706730  8b 55 00                 mov      edx, dword ptr [ebp]
00706733  8b cd                    mov      ecx, ebp
00706735  ff 52 2c                 call     dword ptr [edx + 0x2c]
00706738  83 f8 01                 cmp      eax, 1
0070673B  0f 85 a7 00 00 00        jne      0x7067e8
00706741  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
00706747  8a 88 a6 0b 00 00        mov      cl, byte ptr [eax + 0xba6]
0070674D  84 c9                    test     cl, cl
0070674F  75 0e                    jne      0x70675f
00706751  8a 88 a7 0b 00 00        mov      cl, byte ptr [eax + 0xba7]
00706757  84 c9                    test     cl, cl
00706759  0f 84 89 00 00 00        je       0x7067e8
0070675F  8b 45 00                 mov      eax, dword ptr [ebp]
00706762  8b cd                    mov      ecx, ebp
00706764  ff 90 6c 01 00 00        call     dword ptr [eax + 0x16c]
0070676A  83 f8 10                 cmp      eax, 0x10
0070676D  74 79                    je       0x7067e8
0070676F  6a 00                    push     0
00706771  8b cd                    mov      ecx, ebp
00706773  e8 98 06 f3 ff           call     0x636e10
00706778  3b c3                    cmp      eax, ebx
0070677A  0f 84 fb 00 00 00        je       0x70687b
00706780  8b cb                    mov      ecx, ebx
00706782  e8 89 07 f3 ff           call     0x636f10
00706787  84 c0                    test     al, al
00706789  0f 85 ec 00 00 00        jne      0x70687b
0070678F  8b 55 00                 mov      edx, dword ptr [ebp]
00706792  53                       push     ebx
00706793  6a 02                    push     2
00706795  8b cd                    mov      ecx, ebp
00706797  ff 92 58 02 00 00        call     dword ptr [edx + 0x258]
0070679D  83 f8 01                 cmp      eax, 1
007067A0  0f 85 d5 00 00 00        jne      0x70687b
007067A6  8b 45 00                 mov      eax, dword ptr [ebp]
007067A9  8b cd                    mov      ecx, ebp
007067AB  ff 90 6c 01 00 00        call     dword ptr [eax + 0x16c]
007067B1  83 f8 07                 cmp      eax, 7
007067B4  0f 84 c1 00 00 00        je       0x70687b
007067BA  8b 55 00                 mov      edx, dword ptr [ebp]
007067BD  8b cd                    mov      ecx, ebp
007067BF  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
007067C5  83 f8 0a                 cmp      eax, 0xa
007067C8  0f 84 ad 00 00 00        je       0x70687b
007067CE  8b 45 00                 mov      eax, dword ptr [ebp]
007067D1  6a 00                    push     0
007067D3  6a 07                    push     7
007067D5  8b cd                    mov      ecx, ebp
007067D7  ff 90 d0 01 00 00        call     dword ptr [eax + 0x1d0]
007067DD  c7 84 24 94 00 00 00 00 00 00 00 mov      dword ptr [esp + 0x94], 0
007067E8  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
007067EE  85 c0                    test     eax, eax
007067F0  75 0a                    jne      0x7067fc
007067F2  68 03 40 00 80           push     0x80004003
007067F7  e8 44 f1 08 00           call     0x795940
007067FC  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
00706802  50                       push     eax
00706803  8b 08                    mov      ecx, dword ptr [eax]
00706805  ff 51 60                 call     dword ptr [ecx + 0x60]
00706808  84 c0                    test     al, al
0070680A  0f 85 cf 01 00 00        jne      0x7069df
00706810  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
00706816  e8 65 94 e1 ff           call     0x51fc80
0070681B  84 c0                    test     al, al
0070681D  0f 85 bc 01 00 00        jne      0x7069df
00706823  8b 55 00                 mov      edx, dword ptr [ebp]
00706826  8b cd                    mov      ecx, ebp
00706828  ff 92 a4 01 00 00        call     dword ptr [edx + 0x1a4]
0070682E  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
00706834  f6 c5 01                 test     ch, 1
00706837  0f 85 a2 01 00 00        jne      0x7069df
0070683D  8b b0 e4 00 00 00        mov      esi, dword ptr [eax + 0xe4]
00706843  85 f6                    test     esi, esi
00706845  0f 84 94 01 00 00        je       0x7069df
0070684B  3b f5                    cmp      esi, ebp
0070684D  74 20                    je       0x70686f
0070684F  8b 06                    mov      eax, dword ptr [esi]
00706851  8b ce                    mov      ecx, esi
00706853  ff 50 2c                 call     dword ptr [eax + 0x2c]
00706856  83 f8 06                 cmp      eax, 6
00706859  75 14                    jne      0x70686f
0070685B  8b 8e 18 04 00 00        mov      ecx, dword ptr [esi + 0x418]
00706861  8a 81 49 13 00 00        mov      al, byte ptr [ecx + 0x1349]
00706867  84 c0                    test     al, al
00706869  0f 85 50 01 00 00        jne      0x7069bf
0070686F  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
00706872  85 f6                    test     esi, esi
00706874  75 d5                    jne      0x70684b
00706876  e9 64 01 00 00           jmp      0x7069df
0070687B  8b 84 24 94 00 00 00     mov      eax, dword ptr [esp + 0x94]
00706882  85 c0                    test     eax, eax
00706884  0f 84 5e ff ff ff        je       0x7067e8
0070688A  8b c8                    mov      ecx, eax
0070688C  8b 11                    mov      edx, dword ptr [ecx]
0070688E  ff 52 2c                 call     dword ptr [edx + 0x2c]
00706891  83 f8 06                 cmp      eax, 6
00706894  0f 85 4e ff ff ff        jne      0x7067e8
0070689A  6a 00                    push     0
0070689C  8b cd                    mov      ecx, ebp
0070689E  e8 6d 05 f3 ff           call     0x636e10
007068A3  3b 84 24 94 00 00 00     cmp      eax, dword ptr [esp + 0x94]
007068AA  0f 84 38 ff ff ff        je       0x7067e8
007068B0  8d 8b 88 00 00 00        lea      ecx, [ebx + 0x88]
007068B6  33 c0                    xor      eax, eax
007068B8  8b d1                    mov      edx, ecx
007068BA  66 89 44 24 34           mov      word ptr [esp + 0x34], ax
007068BF  66 89 44 24 36           mov      word ptr [esp + 0x36], ax
007068C4  6a 00                    push     0
007068C6  8b 02                    mov      eax, dword ptr [edx]
007068C8  be 01 00 00 00           mov      esi, 1
007068CD  8b fe                    mov      edi, esi
007068CF  8b 5a 04                 mov      ebx, dword ptr [edx + 4]
007068D2  8b 52 08                 mov      edx, dword ptr [edx + 8]
007068D5  89 54 24 6c              mov      dword ptr [esp + 0x6c], edx
007068D9  99                       cdq      
007068DA  81 e2 ff 00 00 00        and      edx, 0xff
007068E0  03 c2                    add      eax, edx
007068E2  c1 f8 08                 sar      eax, 8
007068E5  66 89 44 24 3c           mov      word ptr [esp + 0x3c], ax
007068EA  8b c3                    mov      eax, ebx
007068EC  99                       cdq      
007068ED  81 e2 ff 00 00 00        and      edx, 0xff
007068F3  8b 59 04                 mov      ebx, dword ptr [ecx + 4]
007068F6  03 c2                    add      eax, edx
007068F8  c1 f8 08                 sar      eax, 8
007068FB  66 89 44 24 3e           mov      word ptr [esp + 0x3e], ax
00706900  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
00706904  89 44 24 40              mov      dword ptr [esp + 0x40], eax
00706908  8b 01                    mov      eax, dword ptr [ecx]
0070690A  99                       cdq      
0070690B  81 e2 ff 00 00 00        and      edx, 0xff
00706911  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
00706914  03 c2                    add      eax, edx
00706916  89 4c 24 6c              mov      dword ptr [esp + 0x6c], ecx
0070691A  c1 f8 08                 sar      eax, 8
0070691D  66 89 44 24 3c           mov      word ptr [esp + 0x3c], ax
00706922  8b c3                    mov      eax, ebx
00706924  99                       cdq      
00706925  81 e2 ff 00 00 00        and      edx, 0xff
0070692B  8d 4c 24 38              lea      ecx, [esp + 0x38]
0070692F  03 c2                    add      eax, edx
00706931  51                       push     ecx
00706932  c1 f8 08                 sar      eax, 8
00706935  6a 00                    push     0
00706937  66 89 44 24 46           mov      word ptr [esp + 0x46], ax
0070693C  8b 54 24 44              mov      edx, dword ptr [esp + 0x44]
00706940  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
00706946  6a 00                    push     0
00706948  56                       push     esi
00706949  6a 00                    push     0
0070694B  89 54 24 48              mov      dword ptr [esp + 0x48], edx
0070694F  8b 80 00 05 00 00        mov      eax, dword ptr [eax + 0x500]
00706955  57                       push     edi
00706956  56                       push     esi
00706957  6a 00                    push     0
00706959  50                       push     eax
0070695A  6a 00                    push     0
0070695C  8d 54 24 68              lea      edx, [esp + 0x68]
00706960  50                       push     eax
00706961  52                       push     edx
00706962  b9 e0 24 83 00           mov      ecx, 0x8324e0
00706967  e8 84 8f e4 ff           call     0x54f8f0
0070696C  50                       push     eax
0070696D  8d 44 24 5c              lea      eax, [esp + 0x5c]
00706971  6a 02                    push     2
00706973  8d 4c 24 5c              lea      ecx, [esp + 0x5c]
00706977  50                       push     eax
00706978  51                       push     ecx
00706979  b9 e0 24 83 00           mov      ecx, 0x8324e0
0070697E  e8 5d 99 e4 ff           call     0x5502e0
00706983  8b 00                    mov      eax, dword ptr [eax]
00706985  66 3b 05 88 04 ad 00     cmp      ax, word ptr [0xad0488]
0070698C  89 44 24 38              mov      dword ptr [esp + 0x38], eax
00706990  75 12                    jne      0x7069a4
00706992  66 8b 54 24 3a           mov      dx, word ptr [esp + 0x3a]
00706997  66 3b 15 8a 04 ad 00     cmp      dx, word ptr [0xad048a]
0070699E  0f 84 39 fe ff ff        je       0x7067dd
007069A4  8d 44 24 38              lea      eax, [esp + 0x38]
007069A8  b9 e0 24 83 00           mov      ecx, 0x8324e0
007069AD  50                       push     eax
007069AE  e8 bd 16 e4 ff           call     0x548070
007069B3  89 84 24 94 00 00 00     mov      dword ptr [esp + 0x94], eax
007069BA  e9 29 fe ff ff           jmp      0x7067e8
007069BF  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
007069C5  85 c0                    test     eax, eax
007069C7  75 0a                    jne      0x7069d3
007069C9  68 03 40 00 80           push     0x80004003
007069CE  e8 6d ef 08 00           call     0x795940
007069D3  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
007069D9  50                       push     eax
007069DA  8b 10                    mov      edx, dword ptr [eax]
007069DC  ff 52 58                 call     dword ptr [edx + 0x58]
007069DF  8b 84 24 98 00 00 00     mov      eax, dword ptr [esp + 0x98]
007069E6  8b 8c 24 94 00 00 00     mov      ecx, dword ptr [esp + 0x94]
007069ED  50                       push     eax
007069EE  51                       push     ecx
007069EF  8b cd                    mov      ecx, ebp
007069F1  e8 3a 16 dc ff           call     0x4c8030
007069F6  5f                       pop      edi
007069F7  5e                       pop      esi
007069F8  5d                       pop      ebp
007069F9  5b                       pop      ebx
007069FA  81 c4 80 00 00 00        add      esp, 0x80
00706A00  c2 08 00                 ret      8
