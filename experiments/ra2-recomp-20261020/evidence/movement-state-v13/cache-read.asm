
sub_004276F6 0x004276F6 size=286
004276F6  8b 18                    mov      ebx, dword ptr [eax]
004276F8  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004276FC  85 db                    test     ebx, ebx
004276FE  0f 84 7a 03 00 00        je       0x427a7e
00427704  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00427708  8d 4b 24                 lea      ecx, [ebx + 0x24]
0042770B  83 f8 08                 cmp      eax, 8
0042770E  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
00427712  74 0d                    je       0x427721
00427714  8b 3c 85 38 c8 84 00     mov      edi, dword ptr [eax*4 + 0x84c838]
0042771B  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
0042771F  eb 0e                    jmp      0x42772f
00427721  0f bf 79 02              movsx    edi, word ptr [ecx + 2]
00427725  0f af 3d 04 e8 84 00     imul     edi, dword ptr [0x84e804]
0042772C  0f bf 01                 movsx    eax, word ptr [ecx]
0042772F  03 f8                    add      edi, eax
00427731  8b 83 40 01 00 00        mov      eax, dword ptr [ebx + 0x140]
00427737  f6 c4 01                 test     ah, 1
0042773A  74 1b                    je       0x427757
0042773C  0f be 93 1b 01 00 00     movsx    edx, byte ptr [ebx + 0x11b]
00427743  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
00427746  c6 44 24 60 00           mov      byte ptr [esp + 0x60], 0
0042774B  2b c2                    sub      eax, edx
0042774D  99                       cdq      
0042774E  33 c2                    xor      eax, edx
00427750  2b c2                    sub      eax, edx
00427752  83 f8 01                 cmp      eax, 1
00427755  7f 05                    jg       0x42775c
00427757  c6 44 24 60 01           mov      byte ptr [esp + 0x60], 1
0042775C  51                       push     ecx
0042775D  b9 e0 24 83 00           mov      ecx, 0x8324e0
00427762  e8 49 83 12 00           call     0x54fab0
00427767  8b 0d 4c 25 83 00        mov      ecx, dword ptr [0x83254c]
0042776D  8d 04 80                 lea      eax, [eax + eax*4]
00427770  8b 54 24 40              mov      edx, dword ptr [esp + 0x40]
00427774  8d 04 41                 lea      eax, [ecx + eax*2]
00427777  0f bf 08                 movsx    ecx, word ptr [eax]
0042777A  8b 46 28                 mov      eax, dword ptr [esi + 0x28]
0042777D  89 4c 24 4c              mov      dword ptr [esp + 0x4c], ecx
00427781  39 04 8a                 cmp      dword ptr [edx + ecx*4], eax
00427784  74 1e                    je       0x4277a4
00427786  8a 4c 24 60              mov      cl, byte ptr [esp + 0x60]
0042778A  84 c9                    test     cl, cl
0042778C  74 53                    je       0x4277e1
0042778E  8a 8b 22 01 00 00        mov      cl, byte ptr [ebx + 0x122]
00427794  84 c9                    test     cl, cl
00427796  75 0c                    jne      0x4277a4
00427798  8a 4c 24 74              mov      cl, byte ptr [esp + 0x74]
0042779C  84 c9                    test     cl, cl
0042779E  0f 85 da 02 00 00        jne      0x427a7e
004277A4  8a 4c 24 60              mov      cl, byte ptr [esp + 0x60]
004277A8  84 c9                    test     cl, cl
004277AA  74 35                    je       0x4277e1
004277AC  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
004277AF  8d 2c bd 00 00 00 00     lea      ebp, [edi*4]
004277B6  89 6c 24 2c              mov      dword ptr [esp + 0x2c], ebp
004277BA  39 04 29                 cmp      dword ptr [ecx + ebp], eax
004277BD  75 55                    jne      0x427814
004277BF  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004277C3  8b 46 24                 mov      eax, dword ptr [esi + 0x24]
004277C6  d9 42 04                 fld      dword ptr [edx + 4]
004277C9  dc 05 d0 c4 79 00        fadd     qword ptr [0x79c4d0]
004277CF  d9 04 28                 fld      dword ptr [eax + ebp]
004277D2  de d9                    fcompp   
004277D4  df e0                    fnstsw   ax
004277D6  f6 c4 01                 test     ah, 1
004277D9  0f 85 9f 02 00 00        jne      0x427a7e
004277DF  eb 33                    jmp      0x427814
004277E1  8b 4e 1c                 mov      ecx, dword ptr [esi + 0x1c]
004277E4  8d 2c bd 00 00 00 00     lea      ebp, [edi*4]
004277EB  89 6c 24 2c              mov      dword ptr [esp + 0x2c], ebp
004277EF  39 04 29                 cmp      dword ptr [ecx + ebp], eax
004277F2  75 20                    jne      0x427814
004277F4  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004277F8  8b 46 20                 mov      eax, dword ptr [esi + 0x20]
004277FB  d9 42 04                 fld      dword ptr [edx + 4]
004277FE  dc 05 d0 c4 79 00        fadd     qword ptr [0x79c4d0]
00427804  d9 04 28                 fld      dword ptr [eax + ebp]
00427807  de d9                    fcompp   
00427809  df e0                    fnstsw   ax
0042780B  f6 c4 01                 test     ah, 1
0042780E  0f 85 6a 02 00 00        jne      0x427a7e
