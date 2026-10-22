
sub_004A1000 0x004A1000 size=1517
004A1000  81 ec e4 00 00 00        sub      esp, 0xe4
004A1006  53                       push     ebx
004A1007  55                       push     ebp
004A1008  8b e9                    mov      ebp, ecx
004A100A  56                       push     esi
004A100B  57                       push     edi
004A100C  8a 45 63                 mov      al, byte ptr [ebp + 0x63]
004A100F  84 c0                    test     al, al
004A1011  74 06                    je       0x4a1019
004A1013  83 7d 58 ff              cmp      dword ptr [ebp + 0x58], -1
004A1017  75 10                    jne      0x4a1029
004A1019  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A101C  83 b8 d0 04 00 00 08     cmp      dword ptr [eax + 0x4d0], 8
004A1023  0f 85 0a 16 00 00        jne      0x4a2633
004A1029  8a 45 62                 mov      al, byte ptr [ebp + 0x62]
004A102C  84 c0                    test     al, al
004A102E  74 19                    je       0x4a1049
004A1030  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1033  8b 11                    mov      edx, dword ptr [ecx]
004A1035  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A103B  8a 88 ab 0a 00 00        mov      cl, byte ptr [eax + 0xaab]
004A1041  84 c9                    test     cl, cl
004A1043  0f 84 ea 15 00 00        je       0x4a2633
004A1049  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A104C  8b 01                    mov      eax, dword ptr [ecx]
004A104E  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A1054  8a 88 59 0b 00 00        mov      cl, byte ptr [eax + 0xb59]
004A105A  84 c9                    test     cl, cl
004A105C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A105F  8b 11                    mov      edx, dword ptr [ecx]
004A1061  0f 84 da 02 00 00        je       0x4a1341
004A1067  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A106A  83 f8 01                 cmp      eax, 1
004A106D  75 17                    jne      0x4a1086
004A106F  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1072  8b 88 ac 05 00 00        mov      ecx, dword ptr [eax + 0x5ac]
004A1078  8a 81 a4 0b 00 00        mov      al, byte ptr [ecx + 0xba4]
004A107E  84 c0                    test     al, al
004A1080  74 04                    je       0x4a1086
004A1082  32 c0                    xor      al, al
004A1084  eb 02                    jmp      0x4a1088
004A1086  b0 01                    mov      al, 1
004A1088  83 7d 58 40              cmp      dword ptr [ebp + 0x58], 0x40
004A108C  0f 8d bd 02 00 00        jge      0x4a134f
004A1092  84 c0                    test     al, al
004A1094  0f 84 b5 02 00 00        je       0x4a134f
004A109A  8d 55 34                 lea      edx, [ebp + 0x34]
004A109D  8b 45 34                 mov      eax, dword ptr [ebp + 0x34]
004A10A0  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004A10A4  8d 44 24 18              lea      eax, [esp + 0x18]
004A10A8  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A10AB  50                       push     eax
004A10AC  89 4c 24 20              mov      dword ptr [esp + 0x20], ecx
004A10B0  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A10B5  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A10B8  89 54 24 24              mov      dword ptr [esp + 0x24], edx
004A10BC  e8 3f 6f 0a 00           call     0x548000
004A10C1  8b b0 40 01 00 00        mov      esi, dword ptr [eax + 0x140]
004A10C7  8b 3d c0 29 85 00        mov      edi, dword ptr [0x8529c0]
004A10CD  81 e6 00 01 00 00        and      esi, 0x100
004A10D3  8d 4c 24 18              lea      ecx, [esp + 0x18]
004A10D7  f7 de                    neg      esi
004A10D9  1b f6                    sbb      esi, esi
004A10DB  51                       push     ecx
004A10DC  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A10E1  23 f7                    and      esi, edi
004A10E3  e8 98 91 0b 00           call     0x55a280
004A10E8  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A10EB  8b 7c 24 18              mov      edi, dword ptr [esp + 0x18]
004A10EF  81 c2 88 00 00 00        add      edx, 0x88
004A10F5  03 c6                    add      eax, esi
004A10F7  8b 5c 24 1c              mov      ebx, dword ptr [esp + 0x1c]
004A10FB  8b f2                    mov      esi, edx
004A10FD  89 44 24 20              mov      dword ptr [esp + 0x20], eax
004A1101  83 ec 08                 sub      esp, 8
004A1104  8b 0e                    mov      ecx, dword ptr [esi]
004A1106  2b cf                    sub      ecx, edi
004A1108  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A110B  89 8c 24 b4 00 00 00     mov      dword ptr [esp + 0xb4], ecx
004A1112  db 84 24 b4 00 00 00     fild     dword ptr [esp + 0xb4]
004A1119  8b 76 08                 mov      esi, dword ptr [esi + 8]
004A111C  2b d3                    sub      edx, ebx
004A111E  89 94 24 b8 00 00 00     mov      dword ptr [esp + 0xb8], edx
004A1125  2b f0                    sub      esi, eax
004A1127  db 84 24 b8 00 00 00     fild     dword ptr [esp + 0xb8]
004A112E  89 b4 24 bc 00 00 00     mov      dword ptr [esp + 0xbc], esi
004A1135  db 84 24 bc 00 00 00     fild     dword ptr [esp + 0xbc]
004A113C  d9 c0                    fld      st(0)
004A113E  d8 c9                    fmul     st(1)
004A1140  d9 c2                    fld      st(2)
004A1142  d8 cb                    fmul     st(3)
004A1144  de c1                    faddp    st(1)
004A1146  d9 c3                    fld      st(3)
004A1148  d8 cc                    fmul     st(4)
004A114A  de c1                    faddp    st(1)
004A114C  dd 1c 24                 fstp     qword ptr [esp]
004A114F  dd d8                    fstp     st(0)
004A1151  dd d8                    fstp     st(0)
004A1153  dd d8                    fstp     st(0)
004A1155  e8 b6 92 01 00           call     0x4ba410
004A115A  83 c4 08                 add      esp, 8
004A115D  e8 ae df 2d 00           call     0x77f110
004A1162  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1165  8b f8                    mov      edi, eax
004A1167  32 db                    xor      bl, bl
004A1169  8b 81 68 04 00 00        mov      eax, dword ptr [ecx + 0x468]
004A116F  8b 91 6c 04 00 00        mov      edx, dword ptr [ecx + 0x46c]
004A1175  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004A1179  8b 01                    mov      eax, dword ptr [ecx]
004A117B  89 54 24 28              mov      dword ptr [esp + 0x28], edx
004A117F  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A1185  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1188  8b f0                    mov      esi, eax
004A118A  8b 11                    mov      edx, dword ptr [ecx]
004A118C  ff 92 38 03 00 00        call     dword ptr [edx + 0x338]
004A1192  89 44 24 30              mov      dword ptr [esp + 0x30], eax
004A1196  8b 86 c8 02 00 00        mov      eax, dword ptr [esi + 0x2c8]
004A119C  3b f8                    cmp      edi, eax
004A119E  7d 3c                    jge      0x4a11dc
004A11A0  db 44 24 30              fild     dword ptr [esp + 0x30]
004A11A4  b3 01                    mov      bl, 1
004A11A6  dc 8e d0 02 00 00        fmul     qword ptr [esi + 0x2d0]
004A11AC  dc 6c 24 24              fsubr    qword ptr [esp + 0x24]
004A11B0  dd 05 48 ea 79 00        fld      qword ptr [0x79ea48]
004A11B6  d8 d9                    fcomp    st(1)
004A11B8  df e0                    fnstsw   ax
004A11BA  f6 c4 41                 test     ah, 0x41
004A11BD  75 17                    jne      0x4a11d6
004A11BF  a1 48 ea 79 00           mov      eax, dword ptr [0x79ea48]
004A11C4  8b 0d 4c ea 79 00        mov      ecx, dword ptr [0x79ea4c]
004A11CA  dd d8                    fstp     st(0)
004A11CC  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004A11D0  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
004A11D4  eb 4d                    jmp      0x4a1223
004A11D6  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
004A11DA  eb 47                    jmp      0x4a1223
004A11DC  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A11DF  8a 82 25 03 00 00        mov      al, byte ptr [edx + 0x325]
004A11E5  84 c0                    test     al, al
004A11E7  74 3a                    je       0x4a1223
004A11E9  db 44 24 30              fild     dword ptr [esp + 0x30]
004A11ED  dc 0d 58 ea 79 00        fmul     qword ptr [0x79ea58]
004A11F3  dc 6c 24 24              fsubr    qword ptr [esp + 0x24]
004A11F7  dd 05 50 ea 79 00        fld      qword ptr [0x79ea50]
004A11FD  d8 d9                    fcomp    st(1)
004A11FF  df e0                    fnstsw   ax
004A1201  f6 c4 41                 test     ah, 0x41
004A1204  75 17                    jne      0x4a121d
004A1206  a1 50 ea 79 00           mov      eax, dword ptr [0x79ea50]
004A120B  8b 0d 54 ea 79 00        mov      ecx, dword ptr [0x79ea54]
004A1211  dd d8                    fstp     st(0)
004A1213  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004A1217  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
004A121B  eb 04                    jmp      0x4a1221
004A121D  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
004A1221  b3 01                    mov      bl, 1
004A1223  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1226  8a 81 9f 05 00 00        mov      al, byte ptr [ecx + 0x59f]
004A122C  84 c0                    test     al, al
004A122E  74 32                    je       0x4a1262
004A1230  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A1233  dc 1d 60 c2 79 00        fcomp    qword ptr [0x79c260]
004A1239  df e0                    fnstsw   ax
004A123B  f6 c4 01                 test     ah, 1
004A123E  74 05                    je       0x4a1245
004A1240  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A1243  eb 06                    jmp      0x4a124b
004A1245  dd 05 60 c2 79 00        fld      qword ptr [0x79c260]
004A124B  dd 54 24 24              fst      qword ptr [esp + 0x24]
004A124F  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A1253  dd 5d 50                 fstp     qword ptr [ebp + 0x50]
004A1256  8b 11                    mov      edx, dword ptr [ecx]
004A1258  50                       push     eax
004A1259  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A125D  e9 8f 00 00 00           jmp      0x4a12f1
004A1262  84 db                    test     bl, bl
004A1264  74 0d                    je       0x4a1273
004A1266  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A126A  8b 11                    mov      edx, dword ptr [ecx]
004A126C  50                       push     eax
004A126D  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A1271  eb 7e                    jmp      0x4a12f1
004A1273  dd 81 68 04 00 00        fld      qword ptr [ecx + 0x468]
004A1279  dc 5d 50                 fcomp    qword ptr [ebp + 0x50]
004A127C  df e0                    fnstsw   ax
004A127E  f6 c4 01                 test     ah, 1
004A1281  74 2e                    je       0x4a12b1
004A1283  dd 86 d8 02 00 00        fld      qword ptr [esi + 0x2d8]
004A1289  dc 81 68 04 00 00        fadd     qword ptr [ecx + 0x468]
004A128F  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A1292  d8 d9                    fcomp    st(1)
004A1294  df e0                    fnstsw   ax
004A1296  f6 c4 01                 test     ah, 1
004A1299  74 05                    je       0x4a12a0
004A129B  dd d8                    fstp     st(0)
004A129D  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A12A0  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
004A12A4  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A12A8  8b 11                    mov      edx, dword ptr [ecx]
004A12AA  50                       push     eax
004A12AB  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A12AF  eb 40                    jmp      0x4a12f1
004A12B1  dd 81 68 04 00 00        fld      qword ptr [ecx + 0x468]
004A12B7  dc 5d 50                 fcomp    qword ptr [ebp + 0x50]
004A12BA  df e0                    fnstsw   ax
004A12BC  f6 c4 41                 test     ah, 0x41
004A12BF  75 37                    jne      0x4a12f8
004A12C1  db 44 24 30              fild     dword ptr [esp + 0x30]
004A12C5  dc 8e d0 02 00 00        fmul     qword ptr [esi + 0x2d0]
004A12CB  dc a9 68 04 00 00        fsubr    qword ptr [ecx + 0x468]
004A12D1  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A12D4  d8 d9                    fcomp    st(1)
004A12D6  df e0                    fnstsw   ax
004A12D8  f6 c4 41                 test     ah, 0x41
004A12DB  75 05                    jne      0x4a12e2
004A12DD  dd d8                    fstp     st(0)
004A12DF  dd 45 50                 fld      qword ptr [ebp + 0x50]
004A12E2  dd 5c 24 24              fstp     qword ptr [esp + 0x24]
004A12E6  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A12EA  8b 11                    mov      edx, dword ptr [ecx]
004A12EC  50                       push     eax
004A12ED  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
004A12F1  50                       push     eax
004A12F2  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A12F8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A12FB  8b 11                    mov      edx, dword ptr [ecx]
004A12FD  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A1300  83 f8 01                 cmp      eax, 1
004A1303  75 4a                    jne      0x4a134f
004A1305  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1308  8b b0 b0 05 00 00        mov      esi, dword ptr [eax + 0x5b0]
004A130E  85 f6                    test     esi, esi
004A1310  74 3d                    je       0x4a134f
004A1312  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1315  8b 16                    mov      edx, dword ptr [esi]
004A1317  8b 88 6c 04 00 00        mov      ecx, dword ptr [eax + 0x46c]
004A131D  51                       push     ecx
004A131E  8b ce                    mov      ecx, esi
004A1320  8b 80 68 04 00 00        mov      eax, dword ptr [eax + 0x468]
004A1326  50                       push     eax
004A1327  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A132D  8b b6 b0 05 00 00        mov      esi, dword ptr [esi + 0x5b0]
004A1333  85 f6                    test     esi, esi
004A1335  74 18                    je       0x4a134f
004A1337  3b b6 b0 05 00 00        cmp      esi, dword ptr [esi + 0x5b0]
004A133D  75 d3                    jne      0x4a1312
004A133F  eb 0e                    jmp      0x4a134f
004A1341  8b 45 54                 mov      eax, dword ptr [ebp + 0x54]
004A1344  50                       push     eax
004A1345  8b 45 50                 mov      eax, dword ptr [ebp + 0x50]
004A1348  50                       push     eax
004A1349  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A134F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1352  8b 11                    mov      edx, dword ptr [ecx]
004A1354  ff 92 bc 04 00 00        call     dword ptr [edx + 0x4bc]
004A135A  8a 94 24 f8 00 00 00     mov      dl, byte ptr [esp + 0xf8]
004A1361  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1364  8b 7d 4c                 mov      edi, dword ptr [ebp + 0x4c]
004A1367  f6 da                    neg      dl
004A1369  1b d2                    sbb      edx, edx
004A136B  f7 d2                    not      edx
004A136D  23 d0                    and      edx, eax
004A136F  8b 81 d0 04 00 00        mov      eax, dword ptr [ecx + 0x4d0]
004A1375  03 d7                    add      edx, edi
004A1377  83 f8 08                 cmp      eax, 8
004A137A  89 54 24 3c              mov      dword ptr [esp + 0x3c], edx
004A137E  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A1382  0f 85 65 02 00 00        jne      0x4a15ed
004A1388  8b 75 58                 mov      esi, dword ptr [ebp + 0x58]
004A138B  83 cf ff                 or       edi, 0xffffffff
004A138E  3b f7                    cmp      esi, edi
004A1390  0f 85 5a 02 00 00        jne      0x4a15f0
004A1396  8b 01                    mov      eax, dword ptr [ecx]
004A1398  6a 00                    push     0
004A139A  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004A13A0  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A13A5  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A13A8  8d 75 40                 lea      esi, [ebp + 0x40]
004A13AB  3b c8                    cmp      ecx, eax
004A13AD  75 1a                    jne      0x4a13c9
004A13AF  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A13B2  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A13B8  3b ca                    cmp      ecx, edx
004A13BA  75 0d                    jne      0x4a13c9
004A13BC  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A13BF  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A13C5  3b d1                    cmp      edx, ecx
004A13C7  74 19                    je       0x4a13e2
004A13C9  8b ce                    mov      ecx, esi
004A13CB  89 01                    mov      dword ptr [ecx], eax
004A13CD  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A13D3  89 51 04                 mov      dword ptr [ecx + 4], edx
004A13D6  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A13DB  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A13DF  89 41 08                 mov      dword ptr [ecx + 8], eax
004A13E2  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A13E5  8b 11                    mov      edx, dword ptr [ecx]
004A13E7  ff 92 a4 01 00 00        call     dword ptr [edx + 0x1a4]
004A13ED  0f bf 90 16 01 00 00     movsx    edx, word ptr [eax + 0x116]
004A13F4  85 d2                    test     edx, edx
004A13F6  0f 8c 7c 01 00 00        jl       0x4a1578
004A13FC  3b 15 d8 61 86 00        cmp      edx, dword ptr [0x8661d8]
004A1402  0f 8d 70 01 00 00        jge      0x4a1578
004A1408  a1 cc 61 86 00           mov      eax, dword ptr [0x8661cc]
004A140D  33 ff                    xor      edi, edi
004A140F  8b 1c 90                 mov      ebx, dword ptr [eax + edx*4]
004A1412  8b 43 28                 mov      eax, dword ptr [ebx + 0x28]
004A1415  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004A1419  0f bf 4c 24 16           movsx    ecx, word ptr [esp + 0x16]
004A141E  0f bf c0                 movsx    eax, ax
004A1421  c1 e0 08                 shl      eax, 8
004A1424  05 80 00 00 00           add      eax, 0x80
004A1429  c1 e1 08                 shl      ecx, 8
004A142C  81 c1 80 00 00 00        add      ecx, 0x80
004A1432  89 06                    mov      dword ptr [esi], eax
004A1434  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1437  89 4e 04                 mov      dword ptr [esi + 4], ecx
004A143A  89 7e 08                 mov      dword ptr [esi + 8], edi
004A143D  b9 17 00 00 00           mov      ecx, 0x17
004A1442  8d b0 d4 04 00 00        lea      esi, [eax + 0x4d4]
004A1448  8d b8 d0 04 00 00        lea      edi, [eax + 0x4d0]
004A144E  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004A1450  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1453  c7 81 2c 05 00 00 ff ff ff ff mov      dword ptr [ecx + 0x52c], 0xffffffff
004A145D  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1460  88 90 74 05 00 00        mov      byte ptr [eax + 0x574], dl
004A1466  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1469  c6 81 75 05 00 00 00     mov      byte ptr [ecx + 0x575], 0
004A1470  8b 53 30                 mov      edx, dword ptr [ebx + 0x30]
004A1473  8b 43 24                 mov      eax, dword ptr [ebx + 0x24]
004A1476  83 e2 07                 and      edx, 7
004A1479  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004A147D  66 03 04 95 70 1a 85 00  add      ax, word ptr [edx*4 + 0x851a70]
004A1485  8d 0c 95 70 1a 85 00     lea      ecx, [edx*4 + 0x851a70]
004A148C  8d 54 24 5c              lea      edx, [esp + 0x5c]
004A1490  66 89 44 24 38           mov      word ptr [esp + 0x38], ax
004A1495  66 8b 41 02              mov      ax, word ptr [ecx + 2]
004A1499  66 03 44 24 16           add      ax, word ptr [esp + 0x16]
004A149E  52                       push     edx
004A149F  66 89 44 24 3e           mov      word ptr [esp + 0x3e], ax
004A14A4  8b 4c 24 3c              mov      ecx, dword ptr [esp + 0x3c]
004A14A8  8d 44 24 18              lea      eax, [esp + 0x18]
004A14AC  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004A14B0  50                       push     eax
004A14B1  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A14B6  e8 b5 6b 0a 00           call     0x548070
004A14BB  8b c8                    mov      ecx, eax
004A14BD  e8 9e 48 fd ff           call     0x475d60
004A14C2  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A14C5  8b 10                    mov      edx, dword ptr [eax]
004A14C7  81 c1 5c 04 00 00        add      ecx, 0x45c
004A14CD  89 11                    mov      dword ptr [ecx], edx
004A14CF  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A14D2  89 51 04                 mov      dword ptr [ecx + 4], edx
004A14D5  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A14D8  89 41 08                 mov      dword ptr [ecx + 8], eax
004A14DB  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A14DE  81 c1 88 00 00 00        add      ecx, 0x88
004A14E4  8b 11                    mov      edx, dword ptr [ecx]
004A14E6  89 54 24 48              mov      dword ptr [esp + 0x48], edx
004A14EA  8d 54 24 48              lea      edx, [esp + 0x48]
004A14EE  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A14F1  52                       push     edx
004A14F2  89 44 24 50              mov      dword ptr [esp + 0x50], eax
004A14F6  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
004A14F9  89 4c 24 54              mov      dword ptr [esp + 0x54], ecx
004A14FD  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1502  e8 79 8d 0b 00           call     0x55a280
004A1507  8b f0                    mov      esi, eax
004A1509  8b 43 28                 mov      eax, dword ptr [ebx + 0x28]
004A150C  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004A1510  8b 9b c0 01 00 00        mov      ebx, dword ptr [ebx + 0x1c0]
004A1516  0f bf 4c 24 16           movsx    ecx, word ptr [esp + 0x16]
004A151B  0f bf c0                 movsx    eax, ax
004A151E  c1 e0 08                 shl      eax, 8
004A1521  c1 e1 08                 shl      ecx, 8
004A1524  05 80 00 00 00           add      eax, 0x80
004A1529  81 c1 80 00 00 00        add      ecx, 0x80
004A152F  8d 54 24 48              lea      edx, [esp + 0x48]
004A1533  89 4c 24 4c              mov      dword ptr [esp + 0x4c], ecx
004A1537  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A153B  c7 44 24 50 00 00 00 00  mov      dword ptr [esp + 0x50], 0
004A1543  52                       push     edx
004A1544  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1549  e8 32 8d 0b 00           call     0x55a280
004A154E  2b c6                    sub      eax, esi
004A1550  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1553  99                       cdq      
004A1554  f7 fb                    idiv     ebx
004A1556  5f                       pop      edi
004A1557  03 c6                    add      eax, esi
004A1559  5e                       pop      esi
004A155A  89 81 64 04 00 00        mov      dword ptr [ecx + 0x464], eax
004A1560  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A1564  c7 45 58 ff ff ff ff     mov      dword ptr [ebp + 0x58], 0xffffffff
004A156B  5d                       pop      ebp
004A156C  32 c0                    xor      al, al
004A156E  5b                       pop      ebx
004A156F  81 c4 e4 00 00 00        add      esp, 0xe4
004A1575  c2 04 00                 ret      4
004A1578  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A157B  8b c6                    mov      eax, esi
004A157D  89 ba d0 04 00 00        mov      dword ptr [edx + 0x4d0], edi
004A1583  89 7d 58                 mov      dword ptr [ebp + 0x58], edi
004A1586  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A158C  89 08                    mov      dword ptr [eax], ecx
004A158E  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1594  89 50 04                 mov      dword ptr [eax + 4], edx
004A1597  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A159D  89 48 08                 mov      dword ptr [eax + 8], ecx
004A15A0  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A15A5  39 06                    cmp      dword ptr [esi], eax
004A15A7  75 1e                    jne      0x4a15c7
004A15A9  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A15AC  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A15B2  3b d1                    cmp      edx, ecx
004A15B4  75 11                    jne      0x4a15c7
004A15B6  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A15B9  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A15BF  3b ca                    cmp      ecx, edx
004A15C1  0f 84 73 10 00 00        je       0x4a263a
004A15C7  89 06                    mov      dword ptr [esi], eax
004A15C9  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A15CF  89 56 04                 mov      dword ptr [esi + 4], edx
004A15D2  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A15D7  89 46 08                 mov      dword ptr [esi + 8], eax
004A15DA  5f                       pop      edi
004A15DB  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A15DF  5e                       pop      esi
004A15E0  5d                       pop      ebp
004A15E1  32 c0                    xor      al, al
004A15E3  5b                       pop      ebx
004A15E4  81 c4 e4 00 00 00        add      esp, 0xe4
004A15EA  c2 04 00                 ret      4
