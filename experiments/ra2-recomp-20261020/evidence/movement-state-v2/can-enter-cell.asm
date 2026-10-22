
sub_00703040 0x00703040 size=2952
00703040  83 ec 68                 sub      esp, 0x68
00703043  53                       push     ebx
00703044  8b 5c 24 70              mov      ebx, dword ptr [esp + 0x70]
00703048  55                       push     ebp
00703049  8b e9                    mov      ebp, ecx
0070304B  8b 83 40 01 00 00        mov      eax, dword ptr [ebx + 0x140]
00703051  56                       push     esi
00703052  f6 c4 01                 test     ah, 1
00703055  57                       push     edi
00703056  89 6c 24 14              mov      dword ptr [esp + 0x14], ebp
0070305A  74 26                    je       0x703082
0070305C  8b 84 24 84 00 00 00     mov      eax, dword ptr [esp + 0x84]
00703063  83 f8 ff                 cmp      eax, -1
00703066  74 13                    je       0x70307b
00703068  0f be 8b 1b 01 00 00     movsx    ecx, byte ptr [ebx + 0x11b]
0070306F  2b c1                    sub      eax, ecx
00703071  99                       cdq      
00703072  33 c2                    xor      eax, edx
00703074  2b c2                    sub      eax, edx
00703076  83 f8 01                 cmp      eax, 1
00703079  7e 07                    jle      0x703082
0070307B  c6 44 24 11 01           mov      byte ptr [esp + 0x11], 1
00703080  eb 05                    jmp      0x703087
00703082  c6 44 24 11 00           mov      byte ptr [esp + 0x11], 0
00703087  8b 83 24 01 00 00        mov      eax, dword ptr [ebx + 0x124]
0070308D  8a 93 24 01 00 00        mov      dl, byte ptr [ebx + 0x124]
00703093  c1 e8 05                 shr      eax, 5
00703096  24 01                    and      al, 1
00703098  8b cb                    mov      ecx, ebx
0070309A  88 44 24 13              mov      byte ptr [esp + 0x13], al
0070309E  8b 43 54                 mov      eax, dword ptr [ebx + 0x54]
007030A1  88 54 24 12              mov      byte ptr [esp + 0x12], dl
007030A5  89 44 24 18              mov      dword ptr [esp + 0x18], eax
007030A9  e8 82 70 d7 ff           call     0x47a130
007030AE  8b 8d ac 05 00 00        mov      ecx, dword ptr [ebp + 0x5ac]
007030B4  8b f0                    mov      esi, eax
007030B6  8b 81 94 0b 00 00        mov      eax, dword ptr [ecx + 0xb94]
007030BC  83 f8 ff                 cmp      eax, -1
007030BF  0f 84 bd 00 00 00        je       0x703182
007030C5  8b bb ec 00 00 00        mov      edi, dword ptr [ebx + 0xec]
007030CB  83 ff 0a                 cmp      edi, 0xa
007030CE  75 79                    jne      0x703149
007030D0  8b 53 38                 mov      edx, dword ptr [ebx + 0x38]
007030D3  8b 0d d4 0c a4 00        mov      ecx, dword ptr [0xa40cd4]
007030D9  8b 0c 91                 mov      ecx, dword ptr [ecx + edx*4]
007030DC  8b 91 b4 02 00 00        mov      edx, dword ptr [ecx + 0x2b4]
007030E2  83 fa 05                 cmp      edx, 5
007030E5  75 09                    jne      0x7030f0
007030E7  83 b9 b8 02 00 00 03     cmp      dword ptr [ecx + 0x2b8], 3
007030EE  74 0e                    je       0x7030fe
007030F0  83 fa 04                 cmp      edx, 4
007030F3  75 21                    jne      0x703116
007030F5  83 b9 b8 02 00 00 03     cmp      dword ptr [ecx + 0x2b8], 3
007030FC  75 18                    jne      0x703116
007030FE  80 bb 1a 01 00 00 02     cmp      byte ptr [ebx + 0x11a], 2
00703105  74 42                    je       0x703149
00703107  5f                       pop      edi
00703108  5e                       pop      esi
00703109  5d                       pop      ebp
0070310A  b8 07 00 00 00           mov      eax, 7
0070310F  5b                       pop      ebx
00703110  83 c4 68                 add      esp, 0x68
00703113  c2 14 00                 ret      0x14
00703116  83 fa 03                 cmp      edx, 3
00703119  75 2e                    jne      0x703149
0070311B  83 b9 b8 02 00 00 04     cmp      dword ptr [ecx + 0x2b8], 4
00703122  74 0d                    je       0x703131
00703124  3b d2                    cmp      edx, edx
00703126  75 21                    jne      0x703149
00703128  83 b9 b8 02 00 00 05     cmp      dword ptr [ecx + 0x2b8], 5
0070312F  75 18                    jne      0x703149
00703131  80 bb 1a 01 00 00 06     cmp      byte ptr [ebx + 0x11a], 6
00703138  74 0f                    je       0x703149
0070313A  5f                       pop      edi
0070313B  5e                       pop      esi
0070313C  5d                       pop      ebp
0070313D  b8 07 00 00 00           mov      eax, 7
00703142  5b                       pop      ebx
00703143  83 c4 68                 add      esp, 0x68
00703146  c2 14 00                 ret      0x14
00703149  3b f8                    cmp      edi, eax
0070314B  74 35                    je       0x703182
0070314D  83 ff 0a                 cmp      edi, 0xa
00703150  74 30                    je       0x703182
00703152  8b 43 44                 mov      eax, dword ptr [ebx + 0x44]
00703155  3d ed 00 00 00           cmp      eax, 0xed
0070315A  7c 17                    jl       0x703173
0070315C  3d ee 00 00 00           cmp      eax, 0xee
00703161  7f 10                    jg       0x703173
00703163  0f be 93 1b 01 00 00     movsx    edx, byte ptr [ebx + 0x11b]
0070316A  39 94 24 84 00 00 00     cmp      dword ptr [esp + 0x84], edx
00703171  75 0f                    jne      0x703182
00703173  5f                       pop      edi
00703174  5e                       pop      esi
00703175  5d                       pop      ebp
00703176  b8 07 00 00 00           mov      eax, 7
0070317B  5b                       pop      ebx
0070317C  83 c4 68                 add      esp, 0x68
0070317F  c2 14 00                 ret      0x14
00703182  83 bc 24 80 00 00 00 08  cmp      dword ptr [esp + 0x80], 8
0070318A  75 31                    jne      0x7031bd
0070318C  85 f6                    test     esi, esi
0070318E  0f 84 c6 09 00 00        je       0x703b5a
00703194  8b 76 28                 mov      esi, dword ptr [esi + 0x28]
00703197  66 85 f6                 test     si, si
0070319A  89 b4 24 84 00 00 00     mov      dword ptr [esp + 0x84], esi
007031A1  75 0e                    jne      0x7031b1
007031A3  66 39 b4 24 86 00 00 00  cmp      word ptr [esp + 0x86], si
007031AB  0f 84 a9 09 00 00        je       0x703b5a
007031B1  5f                       pop      edi
007031B2  5e                       pop      esi
007031B3  5d                       pop      ebp
007031B4  33 c0                    xor      eax, eax
007031B6  5b                       pop      ebx
007031B7  83 c4 68                 add      esp, 0x68
007031BA  c2 14 00                 ret      0x14
007031BD  85 f6                    test     esi, esi
007031BF  74 31                    je       0x7031f2
007031C1  8b 8c 24 80 00 00 00     mov      ecx, dword ptr [esp + 0x80]
007031C8  8b 56 2c                 mov      edx, dword ptr [esi + 0x2c]
007031CB  8b c1                    mov      eax, ecx
007031CD  2b c2                    sub      eax, edx
007031CF  99                       cdq      
007031D0  33 c2                    xor      eax, edx
007031D2  2b c2                    sub      eax, edx
007031D4  83 f8 02                 cmp      eax, 2
007031D7  7e 19                    jle      0x7031f2
007031D9  83 f8 06                 cmp      eax, 6
007031DC  7d 14                    jge      0x7031f2
007031DE  83 f9 ff                 cmp      ecx, -1
007031E1  74 0f                    je       0x7031f2
007031E3  5f                       pop      edi
007031E4  5e                       pop      esi
007031E5  5d                       pop      ebp
007031E6  b8 07 00 00 00           mov      eax, 7
007031EB  5b                       pop      ebx
007031EC  83 c4 68                 add      esp, 0x68
007031EF  c2 14 00                 ret      0x14
007031F2  8b bc 24 80 00 00 00     mov      edi, dword ptr [esp + 0x80]
007031F9  8b cb                    mov      ecx, ebx
007031FB  8d 77 fc                 lea      esi, [edi - 4]
007031FE  83 e6 07                 and      esi, 7
00703201  56                       push     esi
00703202  e8 b9 38 d7 ff           call     0x476ac0
00703207  8b c8                    mov      ecx, eax
00703209  e8 22 6f d7 ff           call     0x47a130
0070320E  8b c8                    mov      ecx, eax
00703210  85 c9                    test     ecx, ecx
00703212  74 2a                    je       0x70323e
00703214  8b 51 2c                 mov      edx, dword ptr [ecx + 0x2c]
00703217  8b c6                    mov      eax, esi
00703219  2b c2                    sub      eax, edx
0070321B  99                       cdq      
0070321C  33 c2                    xor      eax, edx
0070321E  2b c2                    sub      eax, edx
00703220  83 f8 02                 cmp      eax, 2
00703223  7e 19                    jle      0x70323e
00703225  83 f8 06                 cmp      eax, 6
00703228  7d 14                    jge      0x70323e
0070322A  83 ff ff                 cmp      edi, -1
0070322D  74 0f                    je       0x70323e
0070322F  5f                       pop      edi
00703230  5e                       pop      esi
00703231  5d                       pop      ebp
00703232  b8 07 00 00 00           mov      eax, 7
00703237  5b                       pop      ebx
00703238  83 c4 68                 add      esp, 0x68
0070323B  c2 14 00                 ret      0x14
0070323E  8b b4 24 88 00 00 00     mov      esi, dword ptr [esp + 0x88]
00703245  8b 45 00                 mov      eax, dword ptr [ebp]
00703248  8d 4c 24 11              lea      ecx, [esp + 0x11]
0070324C  56                       push     esi
0070324D  8d 94 24 88 00 00 00     lea      edx, [esp + 0x88]
00703254  51                       push     ecx
00703255  52                       push     edx
00703256  57                       push     edi
00703257  53                       push     ebx
00703258  8b cd                    mov      ecx, ebp
0070325A  ff 90 98 01 00 00        call     dword ptr [eax + 0x198]
00703260  83 f8 07                 cmp      eax, 7
00703263  75 0a                    jne      0x70326f
00703265  5f                       pop      edi
00703266  5e                       pop      esi
00703267  5d                       pop      ebp
00703268  5b                       pop      ebx
00703269  83 c4 68                 add      esp, 0x68
0070326C  c2 14 00                 ret      0x14
0070326F  8b 84 24 84 00 00 00     mov      eax, dword ptr [esp + 0x84]
00703276  83 f8 ff                 cmp      eax, -1
00703279  74 3a                    je       0x7032b5
0070327B  8b 8b 40 01 00 00        mov      ecx, dword ptr [ebx + 0x140]
00703281  f6 c5 01                 test     ch, 1
00703284  74 2f                    je       0x7032b5
00703286  0f be 8b 1b 01 00 00     movsx    ecx, byte ptr [ebx + 0x11b]
0070328D  83 c1 04                 add      ecx, 4
00703290  3b c1                    cmp      eax, ecx
00703292  75 21                    jne      0x7032b5
00703294  8b 8b 28 01 00 00        mov      ecx, dword ptr [ebx + 0x128]
0070329A  8a 93 28 01 00 00        mov      dl, byte ptr [ebx + 0x128]
007032A0  c1 e9 05                 shr      ecx, 5
007032A3  80 e1 01                 and      cl, 1
007032A6  88 54 24 12              mov      byte ptr [esp + 0x12], dl
007032AA  88 4c 24 13              mov      byte ptr [esp + 0x13], cl
007032AE  8b 4b 58                 mov      ecx, dword ptr [ebx + 0x58]
007032B1  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
007032B5  8b 0d 74 07 a4 00        mov      ecx, dword ptr [0xa40774]
007032BB  85 c9                    test     ecx, ecx
007032BD  75 40                    jne      0x7032ff
007032BF  6a 01                    push     1
007032C1  53                       push     ebx
007032C2  b9 e0 24 83 00           mov      ecx, 0x8324e0
007032C7  e8 74 74 e5 ff           call     0x55a740
007032CC  84 c0                    test     al, al
007032CE  75 28                    jne      0x7032f8
007032D0  8b 55 00                 mov      edx, dword ptr [ebp]
007032D3  8b cd                    mov      ecx, ebp
007032D5  ff 92 f4 02 00 00        call     dword ptr [edx + 0x2f4]
007032DB  84 c0                    test     al, al
007032DD  75 19                    jne      0x7032f8
007032DF  8a 85 2d 03 00 00        mov      al, byte ptr [ebp + 0x32d]
007032E5  84 c0                    test     al, al
007032E7  74 0f                    je       0x7032f8
007032E9  5f                       pop      edi
007032EA  5e                       pop      esi
007032EB  5d                       pop      ebp
007032EC  b8 07 00 00 00           mov      eax, 7
007032F1  5b                       pop      ebx
007032F2  83 c4 68                 add      esp, 0x68
007032F5  c2 14 00                 ret      0x14
007032F8  8b 84 24 84 00 00 00     mov      eax, dword ptr [esp + 0x84]
007032FF  8b 8c 24 8c 00 00 00     mov      ecx, dword ptr [esp + 0x8c]
00703306  8b 94 24 80 00 00 00     mov      edx, dword ptr [esp + 0x80]
0070330D  51                       push     ecx
0070330E  56                       push     esi
0070330F  50                       push     eax
00703310  52                       push     edx
00703311  53                       push     ebx
00703312  8b cd                    mov      ecx, ebp
00703314  e8 c7 53 dc ff           call     0x4c86e0
00703319  8b f8                    mov      edi, eax
0070331B  83 ff 07                 cmp      edi, 7
0070331E  89 bc 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], edi
00703325  75 0a                    jne      0x703331
00703327  5f                       pop      edi
00703328  5e                       pop      esi
00703329  5d                       pop      ebp
0070332A  5b                       pop      ebx
0070332B  83 c4 68                 add      esp, 0x68
0070332E  c2 14 00                 ret      0x14
00703331  8b 43 44                 mov      eax, dword ptr [ebx + 0x44]
00703334  83 f8 ff                 cmp      eax, -1
00703337  0f 84 fc 00 00 00        je       0x703439
0070333D  8b 0d ec 5d a3 00        mov      ecx, dword ptr [0xa35dec]
00703343  8b 34 81                 mov      esi, dword ptr [ecx + eax*4]
00703346  8a 86 7a 02 00 00        mov      al, byte ptr [esi + 0x27a]
0070334C  84 c0                    test     al, al
0070334E  74 27                    je       0x703377
00703350  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
00703356  e8 95 1f df ff           call     0x4f52f0
0070335B  84 c0                    test     al, al
0070335D  75 18                    jne      0x703377
0070335F  a1 98 d2 a3 00           mov      eax, dword ptr [0xa3d298]
00703364  85 c0                    test     eax, eax
00703366  75 0f                    jne      0x703377
00703368  5f                       pop      edi
00703369  5e                       pop      esi
0070336A  5d                       pop      ebp
0070336B  b8 07 00 00 00           mov      eax, 7
00703370  5b                       pop      ebx
00703371  83 c4 68                 add      esp, 0x68
00703374  c2 14 00                 ret      0x14
00703377  8a 86 78 02 00 00        mov      al, byte ptr [esi + 0x278]
0070337D  84 c0                    test     al, al
0070337F  0f 84 b4 00 00 00        je       0x703439
00703385  8a 86 fd 01 00 00        mov      al, byte ptr [esi + 0x1fd]
0070338B  84 c0                    test     al, al
0070338D  74 32                    je       0x7033c1
0070338F  8b 95 ac 05 00 00        mov      edx, dword ptr [ebp + 0x5ac]
00703395  8a 82 f3 0a 00 00        mov      al, byte ptr [edx + 0xaf3]
0070339B  84 c0                    test     al, al
0070339D  75 0d                    jne      0x7033ac
0070339F  6a 11                    push     0x11
007033A1  8b cd                    mov      ecx, ebp
007033A3  e8 68 45 fd ff           call     0x6d7910
007033A8  84 c0                    test     al, al
007033AA  74 15                    je       0x7033c1
007033AC  8b 43 50                 mov      eax, dword ptr [ebx + 0x50]
007033AF  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
007033B5  50                       push     eax
007033B6  e8 45 21 de ff           call     0x4e5500
007033BB  84 c0                    test     al, al
007033BD  74 7a                    je       0x703439
007033BF  eb 67                    jmp      0x703428
007033C1  8b 55 00                 mov      edx, dword ptr [ebp]
007033C4  8b cd                    mov      ecx, ebp
007033C6  ff 92 8c 02 00 00        call     dword ptr [edx + 0x28c]
007033CC  84 c0                    test     al, al
007033CE  0f 84 86 07 00 00        je       0x703b5a
007033D4  8b 45 00                 mov      eax, dword ptr [ebp]
007033D7  6a 00                    push     0
007033D9  8b cd                    mov      ecx, ebp
007033DB  ff 90 9c 03 00 00        call     dword ptr [eax + 0x39c]
007033E1  8b 08                    mov      ecx, dword ptr [eax]
007033E3  8b 81 ac 00 00 00        mov      eax, dword ptr [ecx + 0xac]
007033E9  8a 88 44 01 00 00        mov      cl, byte ptr [eax + 0x144]
007033EF  84 c9                    test     cl, cl
007033F1  75 22                    jne      0x703415
007033F3  8a 88 46 01 00 00        mov      cl, byte ptr [eax + 0x146]
007033F9  84 c9                    test     cl, cl
007033FB  74 09                    je       0x703406
007033FD  83 be 9c 00 00 00 06     cmp      dword ptr [esi + 0x9c], 6
00703404  74 0f                    je       0x703415
00703406  5f                       pop      edi
00703407  5e                       pop      esi
00703408  5d                       pop      ebp
00703409  b8 07 00 00 00           mov      eax, 7
0070340E  5b                       pop      ebx
0070340F  83 c4 68                 add      esp, 0x68
00703412  c2 14 00                 ret      0x14
00703415  8b 53 50                 mov      edx, dword ptr [ebx + 0x50]
00703418  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
0070341E  52                       push     edx
0070341F  e8 dc 20 de ff           call     0x4e5500
00703424  84 c0                    test     al, al
00703426  74 29                    je       0x703451
00703428  83 ff 04                 cmp      edi, 4
0070342B  7d 0c                    jge      0x703439
0070342D  bf 04 00 00 00           mov      edi, 4
00703432  89 bc 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], edi
00703439  8a 44 24 11              mov      al, byte ptr [esp + 0x11]
0070343D  c6 84 24 88 00 00 00 00  mov      byte ptr [esp + 0x88], 0
00703445  84 c0                    test     al, al
00703447  74 14                    je       0x70345d
00703449  8b b3 e8 00 00 00        mov      esi, dword ptr [ebx + 0xe8]
0070344F  eb 12                    jmp      0x703463
00703451  83 ff 05                 cmp      edi, 5
00703454  7d e3                    jge      0x703439
00703456  bf 05 00 00 00           mov      edi, 5
0070345B  eb d5                    jmp      0x703432
0070345D  8b b3 e4 00 00 00        mov      esi, dword ptr [ebx + 0xe4]
00703463  85 f6                    test     esi, esi
00703465  0f 84 9a 04 00 00        je       0x703905
0070346B  3b ee                    cmp      ebp, esi
0070346D  0f 84 22 06 00 00        je       0x703a95
00703473  8b 85 88 05 00 00        mov      eax, dword ptr [ebp + 0x588]
00703479  85 c0                    test     eax, eax
0070347B  74 42                    je       0x7034bf
0070347D  8b 48 28                 mov      ecx, dword ptr [eax + 0x28]
00703480  85 c9                    test     ecx, ecx
00703482  74 3b                    je       0x7034bf
00703484  8b 01                    mov      eax, dword ptr [ecx]
00703486  8d 54 24 2c              lea      edx, [esp + 0x2c]
0070348A  52                       push     edx
0070348B  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
00703491  8d 4c 24 30              lea      ecx, [esp + 0x30]
00703495  8b f8                    mov      edi, eax
00703497  8b 06                    mov      eax, dword ptr [esi]
00703499  51                       push     ecx
0070349A  8b ce                    mov      ecx, esi
0070349C  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
007034A2  66 8b 10                 mov      dx, word ptr [eax]
007034A5  66 3b 17                 cmp      dx, word ptr [edi]
007034A8  75 0e                    jne      0x7034b8
007034AA  66 8b 40 02              mov      ax, word ptr [eax + 2]
007034AE  66 3b 47 02              cmp      ax, word ptr [edi + 2]
007034B2  0f 84 f9 fc ff ff        je       0x7031b1
007034B8  8b bc 24 8c 00 00 00     mov      edi, dword ptr [esp + 0x8c]
007034BF  8a 46 14                 mov      al, byte ptr [esi + 0x14]
007034C2  8b cd                    mov      ecx, ebp
007034C4  24 01                    and      al, 1
007034C6  f6 d8                    neg      al
007034C8  1b c0                    sbb      eax, eax
007034CA  23 c6                    and      eax, esi
007034CC  50                       push     eax
007034CD  e8 5e 39 f3 ff           call     0x636e30
007034D2  84 c0                    test     al, al
007034D4  74 20                    je       0x7034f6
007034D6  8b 16                    mov      edx, dword ptr [esi]
007034D8  8b ce                    mov      ecx, esi
007034DA  ff 52 2c                 call     dword ptr [edx + 0x2c]
007034DD  83 f8 06                 cmp      eax, 6
007034E0  75 14                    jne      0x7034f6
007034E2  53                       push     ebx
007034E3  8b ce                    mov      ecx, esi
007034E5  e8 06 06 d5 ff           call     0x453af0
007034EA  84 c0                    test     al, al
007034EC  75 08                    jne      0x7034f6
007034EE  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007034F1  e9 07 04 00 00           jmp      0x7038fd
007034F6  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
007034FC  8a 88 b0 0b 00 00        mov      cl, byte ptr [eax + 0xbb0]
00703502  84 c9                    test     cl, cl
00703504  74 20                    je       0x703526
00703506  8b 16                    mov      edx, dword ptr [esi]
00703508  8b ce                    mov      ecx, esi
0070350A  ff 52 2c                 call     dword ptr [edx + 0x2c]
0070350D  83 f8 01                 cmp      eax, 1
00703510  75 14                    jne      0x703526
00703512  8b 86 ac 05 00 00        mov      eax, dword ptr [esi + 0x5ac]
00703518  8a 88 b0 0b 00 00        mov      cl, byte ptr [eax + 0xbb0]
0070351E  84 c9                    test     cl, cl
00703520  0f 85 8b fc ff ff        jne      0x7031b1
00703526  8b 16                    mov      edx, dword ptr [esi]
00703528  8b ce                    mov      ecx, esi
0070352A  ff 52 2c                 call     dword ptr [edx + 0x2c]
0070352D  83 f8 06                 cmp      eax, 6
00703530  0f 85 5d 01 00 00        jne      0x703693
00703536  8b 86 18 04 00 00        mov      eax, dword ptr [esi + 0x418]
0070353C  8a 88 51 13 00 00        mov      cl, byte ptr [eax + 0x1351]
00703542  84 c9                    test     cl, cl
00703544  74 66                    je       0x7035ac
00703546  8b ce                    mov      ecx, esi
00703548  e8 33 a3 d4 ff           call     0x44d880
0070354D  84 c0                    test     al, al
0070354F  75 53                    jne      0x7035a4
00703551  8b 85 b4 01 00 00        mov      eax, dword ptr [ebp + 0x1b4]
00703557  8b 8e b4 01 00 00        mov      ecx, dword ptr [esi + 0x1b4]
0070355D  50                       push     eax
0070355E  e8 dd 1f de ff           call     0x4e5540
00703563  84 c0                    test     al, al
00703565  74 19                    je       0x703580
00703567  83 ff 03                 cmp      edi, 3
0070356A  7d 38                    jge      0x7035a4
0070356C  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
0070356F  bf 03 00 00 00           mov      edi, 3
00703574  89 bc 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], edi
0070357B  e9 7d 03 00 00           jmp      0x7038fd
00703580  8b 55 00                 mov      edx, dword ptr [ebp]
00703583  8b cd                    mov      ecx, ebp
00703585  ff 92 8c 02 00 00        call     dword ptr [edx + 0x28c]
0070358B  84 c0                    test     al, al
0070358D  0f 84 c7 05 00 00        je       0x703b5a
00703593  83 ff 05                 cmp      edi, 5
00703596  7d 0c                    jge      0x7035a4
00703598  bf 05 00 00 00           mov      edi, 5
0070359D  89 bc 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], edi
007035A4  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007035A7  e9 51 03 00 00           jmp      0x7038fd
007035AC  83 bc 24 80 00 00 00 ff  cmp      dword ptr [esp + 0x80], -1
007035B4  74 29                    je       0x7035df
007035B6  8a 88 49 13 00 00        mov      cl, byte ptr [eax + 0x1349]
007035BC  84 c9                    test     cl, cl
007035BE  74 1f                    je       0x7035df
007035C0  8b cb                    mov      ecx, ebx
007035C2  e8 e9 e1 d6 ff           call     0x4717b0
007035C7  3b c6                    cmp      eax, esi
007035C9  75 14                    jne      0x7035df
007035CB  53                       push     ebx
007035CC  8b ce                    mov      ecx, esi
007035CE  e8 1d 05 d5 ff           call     0x453af0
007035D3  84 c0                    test     al, al
007035D5  75 08                    jne      0x7035df
007035D7  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007035DA  e9 1e 03 00 00           jmp      0x7038fd
007035DF  8b 86 18 04 00 00        mov      eax, dword ptr [esi + 0x418]
007035E5  8a 88 85 13 00 00        mov      cl, byte ptr [eax + 0x1385]
007035EB  84 c9                    test     cl, cl
007035ED  74 08                    je       0x7035f7
007035EF  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007035F2  e9 06 03 00 00           jmp      0x7038fd
007035F7  8a 88 59 13 00 00        mov      cl, byte ptr [eax + 0x1359]
007035FD  84 c9                    test     cl, cl
007035FF  74 18                    je       0x703619
00703601  8b 8e ec 04 00 00        mov      ecx, dword ptr [esi + 0x4ec]
00703607  83 f9 0c                 cmp      ecx, 0xc
0070360A  74 05                    je       0x703611
0070360C  83 f9 08                 cmp      ecx, 8
0070360F  75 08                    jne      0x703619
00703611  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
00703614  e9 e4 02 00 00           jmp      0x7038fd
00703619  8a 88 5a 13 00 00        mov      cl, byte ptr [eax + 0x135a]
0070361F  84 c9                    test     cl, cl
00703621  74 1c                    je       0x70363f
00703623  8b 86 b4 01 00 00        mov      eax, dword ptr [esi + 0x1b4]
00703629  8a 88 42 01 00 00        mov      cl, byte ptr [eax + 0x142]
0070362F  84 c9                    test     cl, cl
00703631  0f 85 23 05 00 00        jne      0x703b5a
00703637  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
0070363A  e9 be 02 00 00           jmp      0x7038fd
0070363F  8a 88 14 12 00 00        mov      cl, byte ptr [eax + 0x1214]
00703645  84 c9                    test     cl, cl
00703647  74 4a                    je       0x703693
00703649  66 8b 4b 24              mov      cx, word ptr [ebx + 0x24]
0070364D  66 8b 53 26              mov      dx, word ptr [ebx + 0x26]
00703651  66 03 0d 78 1a 85 00     add      cx, word ptr [0x851a78]
00703658  66 03 15 7a 1a 85 00     add      dx, word ptr [0x851a7a]
0070365F  66 89 4c 24 1c           mov      word ptr [esp + 0x1c], cx
00703664  8d 4c 24 20              lea      ecx, [esp + 0x20]
00703668  66 89 54 24 1e           mov      word ptr [esp + 0x1e], dx
0070366D  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00703671  51                       push     ecx
00703672  b9 e0 24 83 00           mov      ecx, 0x8324e0
00703677  89 44 24 24              mov      dword ptr [esp + 0x24], eax
0070367B  e8 f0 49 e4 ff           call     0x548070
00703680  8b c8                    mov      ecx, eax
00703682  e8 29 e1 d6 ff           call     0x4717b0
00703687  3b c6                    cmp      eax, esi
00703689  74 08                    je       0x703693
0070368B  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
0070368E  e9 6a 02 00 00           jmp      0x7038fd
00703693  8b 55 00                 mov      edx, dword ptr [ebp]
00703696  8b cd                    mov      ecx, ebp
00703698  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
0070369E  83 f8 07                 cmp      eax, 7
007036A1  75 18                    jne      0x7036bb
007036A3  3b b5 94 04 00 00        cmp      esi, dword ptr [ebp + 0x494]
007036A9  75 10                    jne      0x7036bb
007036AB  8b 06                    mov      eax, dword ptr [esi]
007036AD  8b ce                    mov      ecx, esi
007036AF  ff 50 2c                 call     dword ptr [eax + 0x2c]
007036B2  83 f8 01                 cmp      eax, 1
007036B5  0f 84 f6 fa ff ff        je       0x7031b1
007036BB  8b 55 00                 mov      edx, dword ptr [ebp]
007036BE  8b cd                    mov      ecx, ebp
007036C0  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
007036C6  83 f8 0b                 cmp      eax, 0xb
007036C9  75 0c                    jne      0x7036d7
007036CB  39 b5 b0 01 00 00        cmp      dword ptr [ebp + 0x1b0], esi
007036D1  0f 84 83 04 00 00        je       0x703b5a
007036D7  f6 46 14 04              test     byte ptr [esi + 0x14], 4
007036DB  74 45                    je       0x703722
007036DD  8b 86 94 04 00 00        mov      eax, dword ptr [esi + 0x494]
007036E3  89 74 24 20              mov      dword ptr [esp + 0x20], esi
007036E7  85 c0                    test     eax, eax
007036E9  75 33                    jne      0x70371e
007036EB  8d 8e e0 02 00 00        lea      ecx, [esi + 0x2e0]
007036F1  e8 9a 55 db ff           call     0x4b8c90
007036F6  84 c0                    test     al, al
007036F8  75 24                    jne      0x70371e
007036FA  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
00703700  85 c0                    test     eax, eax
00703702  75 0a                    jne      0x70370e
00703704  68 03 40 00 80           push     0x80004003
00703709  e8 32 22 09 00           call     0x795940
0070370E  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
00703714  50                       push     eax
00703715  8b 08                    mov      ecx, dword ptr [eax]
00703717  ff 51 10                 call     dword ptr [ecx + 0x10]
0070371A  84 c0                    test     al, al
0070371C  74 0c                    je       0x70372a
0070371E  b3 01                    mov      bl, 1
00703720  eb 0a                    jmp      0x70372c
00703722  c7 44 24 20 00 00 00 00  mov      dword ptr [esp + 0x20], 0
0070372A  32 db                    xor      bl, bl
0070372C  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
00703732  56                       push     esi
00703733  e8 48 1e de ff           call     0x4e5580
00703738  84 c0                    test     al, al
0070373A  0f 84 3c 02 00 00        je       0x70397c
00703740  84 db                    test     bl, bl
00703742  0f 84 07 02 00 00        je       0x70394f
00703748  8b 5c 24 14              mov      ebx, dword ptr [esp + 0x14]
0070374C  8d 54 24 34              lea      edx, [esp + 0x34]
00703750  52                       push     edx
00703751  8d 8b e0 02 00 00        lea      ecx, [ebx + 0x2e0]
00703757  e8 84 54 db ff           call     0x4b8be0
0070375C  8b 28                    mov      ebp, dword ptr [eax]
0070375E  8d 44 24 38              lea      eax, [esp + 0x38]
00703762  c1 ed 0c                 shr      ebp, 0xc
00703765  45                       inc      ebp
00703766  50                       push     eax
00703767  d1 ed                    shr      ebp, 1
00703769  8d 8e e0 02 00 00        lea      ecx, [esi + 0x2e0]
0070376F  83 e5 07                 and      ebp, 7
00703772  e8 69 54 db ff           call     0x4b8be0
00703777  66 8b 08                 mov      cx, word ptr [eax]
0070377A  8d 96 88 00 00 00        lea      edx, [esi + 0x88]
00703780  66 81 c1 ff 7f           add      cx, 0x7fff
00703785  83 ec 08                 sub      esp, 8
00703788  8b 02                    mov      eax, dword ptr [edx]
0070378A  66 89 4c 24 2c           mov      word ptr [esp + 0x2c], cx
0070378F  89 44 24 5c              mov      dword ptr [esp + 0x5c], eax
00703793  8d 83 88 00 00 00        lea      eax, [ebx + 0x88]
00703799  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
0070379C  8b 7c 24 2c              mov      edi, dword ptr [esp + 0x2c]
007037A0  db 44 24 5c              fild     dword ptr [esp + 0x5c]
007037A4  89 4c 24 60              mov      dword ptr [esp + 0x60], ecx
007037A8  8b 08                    mov      ecx, dword ptr [eax]
007037AA  8b 52 08                 mov      edx, dword ptr [edx + 8]
007037AD  89 4c 24 50              mov      dword ptr [esp + 0x50], ecx
007037B1  da 64 24 50              fisub    dword ptr [esp + 0x50]
007037B5  89 54 24 64              mov      dword ptr [esp + 0x64], edx
007037B9  8b 50 04                 mov      edx, dword ptr [eax + 4]
007037BC  89 54 24 54              mov      dword ptr [esp + 0x54], edx
007037C0  83 ec 08                 sub      esp, 8
007037C3  8b 40 08                 mov      eax, dword ptr [eax + 8]
007037C6  c1 ef 0c                 shr      edi, 0xc
007037C9  47                       inc      edi
007037CA  89 44 24 60              mov      dword ptr [esp + 0x60], eax
007037CE  d1 ef                    shr      edi, 1
007037D0  dd 5c 24 08              fstp     qword ptr [esp + 8]
007037D4  db 44 24 5c              fild     dword ptr [esp + 0x5c]
007037D8  83 e7 07                 and      edi, 7
007037DB  da 64 24 68              fisub    dword ptr [esp + 0x68]
007037DF  dd 1c 24                 fstp     qword ptr [esp]
007037E2  e8 19 6e db ff           call     0x4ba600
007037E7  dc 25 30 b6 79 00        fsub     qword ptr [0x79b630]
007037ED  83 c4 10                 add      esp, 0x10
007037F0  dc 0d 28 b6 79 00        fmul     qword ptr [0x79b628]
007037F6  e8 15 b9 07 00           call     0x77f110
007037FB  3b ef                    cmp      ebp, edi
007037FD  66 89 44 24 28           mov      word ptr [esp + 0x28], ax
00703802  0f 85 8d 00 00 00        jne      0x703895
00703808  8b 16                    mov      edx, dword ptr [esi]
0070380A  8d 44 24 60              lea      eax, [esp + 0x60]
0070380E  50                       push     eax
0070380F  8b ce                    mov      ecx, esi
00703811  ff 52 48                 call     dword ptr [edx + 0x48]
00703814  8b 13                    mov      edx, dword ptr [ebx]
00703816  8b f8                    mov      edi, eax
00703818  8d 44 24 6c              lea      eax, [esp + 0x6c]
0070381C  8b cb                    mov      ecx, ebx
0070381E  50                       push     eax
0070381F  ff 52 48                 call     dword ptr [edx + 0x48]
00703822  8b 08                    mov      ecx, dword ptr [eax]
00703824  8b 17                    mov      edx, dword ptr [edi]
00703826  8b 5f 08                 mov      ebx, dword ptr [edi + 8]
00703829  2b ca                    sub      ecx, edx
0070382B  8b 50 04                 mov      edx, dword ptr [eax + 4]
0070382E  8b 40 08                 mov      eax, dword ptr [eax + 8]
00703831  89 4c 24 3c              mov      dword ptr [esp + 0x3c], ecx
00703835  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
00703838  2b d1                    sub      edx, ecx
0070383A  2b c3                    sub      eax, ebx
0070383C  89 54 24 40              mov      dword ptr [esp + 0x40], edx
00703840  89 44 24 44              mov      dword ptr [esp + 0x44], eax
00703844  db 44 24 40              fild     dword ptr [esp + 0x40]
00703848  db 44 24 44              fild     dword ptr [esp + 0x44]
0070384C  db 44 24 3c              fild     dword ptr [esp + 0x3c]
00703850  83 ec 08                 sub      esp, 8
00703853  d9 c0                    fld      st(0)
00703855  d8 c9                    fmul     st(1)
00703857  d9 c2                    fld      st(2)
00703859  d8 cb                    fmul     st(3)
0070385B  de c1                    faddp    st(1)
0070385D  d9 c3                    fld      st(3)
0070385F  d8 cc                    fmul     st(4)
00703861  de c1                    faddp    st(1)
00703863  dd 1c 24                 fstp     qword ptr [esp]
00703866  dd d8                    fstp     st(0)
00703868  dd d8                    fstp     st(0)
0070386A  dd d8                    fstp     st(0)
0070386C  e8 9f 6b db ff           call     0x4ba410
00703871  83 c4 08                 add      esp, 8
00703874  e8 97 b8 07 00           call     0x77f110
00703879  3d ff 01 00 00           cmp      eax, 0x1ff
0070387E  7f 15                    jg       0x703895
00703880  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
00703884  c1 e9 0c                 shr      ecx, 0xc
00703887  41                       inc      ecx
00703888  d1 e9                    shr      ecx, 1
0070388A  83 e1 07                 and      ecx, 7
0070388D  3b cd                    cmp      ecx, ebp
0070388F  0f 84 c5 02 00 00        je       0x703b5a
00703895  8b 7c 24 20              mov      edi, dword ptr [esp + 0x20]
00703899  8a 87 a0 05 00 00        mov      al, byte ptr [edi + 0x5a0]
0070389F  84 c0                    test     al, al
007038A1  74 0c                    je       0x7038af
007038A3  8b 17                    mov      edx, dword ptr [edi]
007038A5  8b cf                    mov      ecx, edi
007038A7  ff 52 2c                 call     dword ptr [edx + 0x2c]
007038AA  83 f8 0f                 cmp      eax, 0xf
007038AD  75 27                    jne      0x7038d6
007038AF  8b 87 64 05 00 00        mov      eax, dword ptr [edi + 0x564]
007038B5  85 c0                    test     eax, eax
007038B7  75 0a                    jne      0x7038c3
007038B9  68 03 40 00 80           push     0x80004003
007038BE  e8 7d 20 09 00           call     0x795940
007038C3  8b 87 64 05 00 00        mov      eax, dword ptr [edi + 0x564]
007038C9  50                       push     eax
007038CA  8b 08                    mov      ecx, dword ptr [eax]
007038CC  ff 91 a4 00 00 00        call     dword ptr [ecx + 0xa4]
007038D2  84 c0                    test     al, al
007038D4  74 15                    je       0x7038eb
007038D6  83 bc 24 8c 00 00 00 02  cmp      dword ptr [esp + 0x8c], 2
007038DE  7d 0b                    jge      0x7038eb
007038E0  c7 84 24 8c 00 00 00 02 00 00 00 mov      dword ptr [esp + 0x8c], 2
007038EB  8b 6c 24 14              mov      ebp, dword ptr [esp + 0x14]
007038EF  8b 76 30                 mov      esi, dword ptr [esi + 0x30]
007038F2  8b 5c 24 7c              mov      ebx, dword ptr [esp + 0x7c]
007038F6  8b bc 24 8c 00 00 00     mov      edi, dword ptr [esp + 0x8c]
007038FD  85 f6                    test     esi, esi
007038FF  0f 85 66 fb ff ff        jne      0x70346b
00703905  8a 44 24 11              mov      al, byte ptr [esp + 0x11]
00703909  84 c0                    test     al, al
0070390B  0f 85 98 01 00 00        jne      0x703aa9
00703911  8b 83 ec 00 00 00        mov      eax, dword ptr [ebx + 0xec]
00703917  8b 95 ac 05 00 00        mov      edx, dword ptr [ebp + 0x5ac]
0070391D  8d 0c c0                 lea      ecx, [eax + eax*8]
00703920  8b 82 a4 05 00 00        mov      eax, dword ptr [edx + 0x5a4]
00703926  03 c8                    add      ecx, eax
00703928  d9 04 8d a0 0e 85 00     fld      dword ptr [ecx*4 + 0x850ea0]
0070392F  d8 1d 38 a7 79 00        fcomp    dword ptr [0x79a738]
00703935  df e0                    fnstsw   ax
00703937  f6 c4 40                 test     ah, 0x40
0070393A  0f 84 69 01 00 00        je       0x703aa9
00703940  5f                       pop      edi
00703941  5e                       pop      esi
00703942  5d                       pop      ebp
00703943  b8 07 00 00 00           mov      eax, 7
00703948  5b                       pop      ebx
00703949  83 c4 68                 add      esp, 0x68
0070394C  c2 14 00                 ret      0x14
0070394F  8b 16                    mov      edx, dword ptr [esi]
00703951  8b ce                    mov      ecx, esi
00703953  ff 52 2c                 call     dword ptr [edx + 0x2c]
00703956  b9 06 00 00 00           mov      ecx, 6
0070395B  3b c1                    cmp      eax, ecx
0070395D  0f 84 f7 01 00 00        je       0x703b5a
00703963  39 8c 24 8c 00 00 00     cmp      dword ptr [esp + 0x8c], ecx
0070396A  0f 8d 7b ff ff ff        jge      0x7038eb
00703970  89 8c 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], ecx
00703977  e9 73 ff ff ff           jmp      0x7038ef
0070397C  8b ce                    mov      ecx, esi
0070397E  e8 4d a2 d0 ff           call     0x40dbd0
00703983  85 c0                    test     eax, eax
00703985  74 13                    je       0x70399a
00703987  83 b8 b8 01 00 00 02     cmp      dword ptr [eax + 0x1b8], 2
0070398E  75 0a                    jne      0x70399a
00703990  b8 01 00 00 00           mov      eax, 1
00703995  e9 cc 00 00 00           jmp      0x703a66
0070399A  8b 85 ac 05 00 00        mov      eax, dword ptr [ebp + 0x5ac]
007039A0  8a 88 f3 0a 00 00        mov      cl, byte ptr [eax + 0xaf3]
007039A6  84 c9                    test     cl, cl
007039A8  75 0d                    jne      0x7039b7
007039AA  6a 11                    push     0x11
007039AC  8b cd                    mov      ecx, ebp
007039AE  e8 5d 3f fd ff           call     0x6d7910
007039B3  84 c0                    test     al, al
007039B5  74 35                    je       0x7039ec
007039B7  8b 16                    mov      edx, dword ptr [esi]
007039B9  8b ce                    mov      ecx, esi
007039BB  ff 92 84 00 00 00        call     dword ptr [edx + 0x84]
007039C1  8a 88 fd 01 00 00        mov      cl, byte ptr [eax + 0x1fd]
007039C7  84 c9                    test     cl, cl
007039C9  74 21                    je       0x7039ec
007039CB  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
007039D1  56                       push     esi
007039D2  e8 a9 1b de ff           call     0x4e5580
007039D7  84 c0                    test     al, al
007039D9  0f 85 0c ff ff ff        jne      0x7038eb
007039DF  c6 84 24 88 00 00 00 01  mov      byte ptr [esp + 0x88], 1
007039E7  e9 03 ff ff ff           jmp      0x7038ef
007039EC  8b 45 00                 mov      eax, dword ptr [ebp]
007039EF  6a 00                    push     0
007039F1  8b cd                    mov      ecx, ebp
007039F3  ff 90 9c 03 00 00        call     dword ptr [eax + 0x39c]
007039F9  83 38 00                 cmp      dword ptr [eax], 0
007039FC  75 14                    jne      0x703a12
007039FE  8b 8d ac 05 00 00        mov      ecx, dword ptr [ebp + 0x5ac]
00703A04  8a 81 a0 0a 00 00        mov      al, byte ptr [ecx + 0xaa0]
00703A0A  84 c0                    test     al, al
00703A0C  0f 84 48 01 00 00        je       0x703b5a
00703A12  8b 16                    mov      edx, dword ptr [esi]
00703A14  8b ce                    mov      ecx, esi
00703A16  ff 52 2c                 call     dword ptr [edx + 0x2c]
00703A19  83 f8 06                 cmp      eax, 6
00703A1C  74 61                    je       0x703a7f
00703A1E  83 f8 24                 cmp      eax, 0x24
00703A21  75 3e                    jne      0x703a61
00703A23  8b 45 00                 mov      eax, dword ptr [ebp]
00703A26  56                       push     esi
00703A27  8b cd                    mov      ecx, ebp
00703A29  ff 90 b8 02 00 00        call     dword ptr [eax + 0x2b8]
00703A2F  8b 55 00                 mov      edx, dword ptr [ebp]
00703A32  50                       push     eax
00703A33  8b cd                    mov      ecx, ebp
00703A35  ff 92 9c 03 00 00        call     dword ptr [edx + 0x39c]
00703A3B  8b 00                    mov      eax, dword ptr [eax]
00703A3D  85 c0                    test     eax, eax
00703A3F  0f 84 15 01 00 00        je       0x703b5a
00703A45  8b 80 ac 00 00 00        mov      eax, dword ptr [eax + 0xac]
00703A4B  85 c0                    test     eax, eax
00703A4D  0f 84 07 01 00 00        je       0x703b5a
00703A53  8a 88 46 01 00 00        mov      cl, byte ptr [eax + 0x146]
00703A59  84 c9                    test     cl, cl
00703A5B  0f 84 f9 00 00 00        je       0x703b5a
00703A61  b8 05 00 00 00           mov      eax, 5
00703A66  39 84 24 8c 00 00 00     cmp      dword ptr [esp + 0x8c], eax
00703A6D  0f 8d 78 fe ff ff        jge      0x7038eb
00703A73  89 84 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], eax
00703A7A  e9 70 fe ff ff           jmp      0x7038ef
00703A7F  8b 86 18 04 00 00        mov      eax, dword ptr [esi + 0x418]
00703A85  8a 88 50 13 00 00        mov      cl, byte ptr [eax + 0x1350]
00703A8B  84 c9                    test     cl, cl
00703A8D  0f 85 c7 00 00 00        jne      0x703b5a
00703A93  eb cc                    jmp      0x703a61
00703A95  8a 44 24 12              mov      al, byte ptr [esp + 0x12]
00703A99  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
00703A9E  24 df                    and      al, 0xdf
00703AA0  88 44 24 12              mov      byte ptr [esp + 0x12], al
00703AA4  e9 46 fe ff ff           jmp      0x7038ef
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
