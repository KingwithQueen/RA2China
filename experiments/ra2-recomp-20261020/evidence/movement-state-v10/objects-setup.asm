
sub_007031B1 0x007031B1 size=656
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
