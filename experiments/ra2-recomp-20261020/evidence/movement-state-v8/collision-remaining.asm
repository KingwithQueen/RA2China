
sub_00703040 0x00703182 size=1536
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
