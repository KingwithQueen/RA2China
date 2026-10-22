
sub_004506B0 0x004506B0 size=288
004506B0  83 ec 20                 sub      esp, 0x20
004506B3  8b 81 18 04 00 00        mov      eax, dword ptr [ecx + 0x418]
004506B9  53                       push     ebx
004506BA  8b 91 b4 01 00 00        mov      edx, dword ptr [ecx + 0x1b4]
004506C0  55                       push     ebp
004506C1  8b 98 3c 05 00 00        mov      ebx, dword ptr [eax + 0x53c]
004506C7  56                       push     esi
004506C8  8b c3                    mov      eax, ebx
004506CA  0f af c3                 imul     eax, ebx
004506CD  89 44 24 10              mov      dword ptr [esp + 0x10], eax
004506D1  8b 42 30                 mov      eax, dword ptr [edx + 0x30]
004506D4  66 8b 54 24 30           mov      dx, word ptr [esp + 0x30]
004506D9  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004506DD  66 3b 15 10 ed 84 00     cmp      dx, word ptr [0x84ed10]
004506E4  75 49                    jne      0x45072f
004506E6  66 8b 44 24 32           mov      ax, word ptr [esp + 0x32]
004506EB  66 3b 05 12 ed 84 00     cmp      ax, word ptr [0x84ed12]
004506F2  75 3b                    jne      0x45072f
004506F4  8b 11                    mov      edx, dword ptr [ecx]
004506F6  8d 44 24 20              lea      eax, [esp + 0x20]
004506FA  50                       push     eax
004506FB  ff 52 48                 call     dword ptr [edx + 0x48]
004506FE  8b c8                    mov      ecx, eax
00450700  8b 01                    mov      eax, dword ptr [ecx]
00450702  99                       cdq      
00450703  81 e2 ff 00 00 00        and      edx, 0xff
00450709  03 c2                    add      eax, edx
0045070B  c1 f8 08                 sar      eax, 8
0045070E  66 89 44 24 0c           mov      word ptr [esp + 0xc], ax
00450713  8b 41 04                 mov      eax, dword ptr [ecx + 4]
00450716  99                       cdq      
00450717  81 e2 ff 00 00 00        and      edx, 0xff
0045071D  03 c2                    add      eax, edx
0045071F  c1 f8 08                 sar      eax, 8
00450722  66 89 44 24 0e           mov      word ptr [esp + 0xe], ax
00450727  8b 4c 24 0c              mov      ecx, dword ptr [esp + 0xc]
0045072B  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
0045072F  8b f3                    mov      esi, ebx
00450731  f7 de                    neg      esi
00450733  8b ee                    mov      ebp, esi
00450735  89 74 24 1c              mov      dword ptr [esp + 0x1c], esi
00450739  3b eb                    cmp      ebp, ebx
0045073B  7d 63                    jge      0x4507a0
0045073D  57                       push     edi
0045073E  3b f3                    cmp      esi, ebx
00450740  7d 58                    jge      0x45079a
00450742  8b 54 24 36              mov      edx, dword ptr [esp + 0x36]
00450746  8b fd                    mov      edi, ebp
00450748  0f af fd                 imul     edi, ebp
0045074B  8d 04 2a                 lea      eax, [edx + ebp]
0045074E  66 89 44 24 12           mov      word ptr [esp + 0x12], ax
00450753  8b 4c 24 34              mov      ecx, dword ptr [esp + 0x34]
00450757  8d 14 0e                 lea      edx, [esi + ecx]
0045075A  8b ce                    mov      ecx, esi
0045075C  0f af ce                 imul     ecx, esi
0045075F  66 89 54 24 10           mov      word ptr [esp + 0x10], dx
00450764  8b 44 24 10              mov      eax, dword ptr [esp + 0x10]
00450768  89 44 24 18              mov      dword ptr [esp + 0x18], eax
0045076C  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00450770  03 cf                    add      ecx, edi
00450772  3b c8                    cmp      ecx, eax
00450774  7d 1b                    jge      0x450791
00450776  8d 54 24 18              lea      edx, [esp + 0x18]
0045077A  b9 e0 24 83 00           mov      ecx, 0x8324e0
0045077F  52                       push     edx
00450780  e8 eb 78 0f 00           call     0x548070
00450785  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
00450789  51                       push     ecx
0045078A  8b c8                    mov      ecx, eax
0045078C  e8 ff bb 02 00           call     0x47c390
00450791  46                       inc      esi
00450792  3b f3                    cmp      esi, ebx
00450794  7c bd                    jl       0x450753
00450796  8b 74 24 20              mov      esi, dword ptr [esp + 0x20]
0045079A  45                       inc      ebp
0045079B  3b eb                    cmp      ebp, ebx
0045079D  7c 9f                    jl       0x45073e
0045079F  5f                       pop      edi
004507A0  5e                       pop      esi
004507A1  5d                       pop      ebp
004507A2  5b                       pop      ebx
004507A3  83 c4 20                 add      esp, 0x20
004507A6  c2 04 00                 ret      4
004507A9  90                       nop      
004507AA  90                       nop      
004507AB  90                       nop      
004507AC  90                       nop      
004507AD  90                       nop      
004507AE  90                       nop      
004507AF  90                       nop      
004507B0  83 ec 20                 sub      esp, 0x20
004507B3  53                       push     ebx
004507B4  55                       push     ebp
004507B5  56                       push     esi
004507B6  8b f1                    mov      esi, ecx
004507B8  8b 06                    mov      eax, dword ptr [esi]
004507BA  ff 90 0c 03 00 00        call     dword ptr [eax + 0x30c]
004507C0  84 c0                    test     al, al
004507C2  0f 84 ec 00 00 00        je       0x4508b4
004507C8  8b 8e 18 04 00 00        mov      ecx, dword ptr [esi + 0x418]
