
sub_004A1000 0x004A1000 size=5705
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
004A15ED  83 cf ff                 or       edi, 0xffffffff
004A15F0  83 fa 07                 cmp      edx, 7
004A15F3  0f 8e a8 09 00 00        jle      0x4a1fa1
004A15F9  8b 55 58                 mov      edx, dword ptr [ebp + 0x58]
004A15FC  8d 14 52                 lea      edx, [edx + edx*2]
004A15FF  8d 34 95 80 01 7a 00     lea      esi, [edx*4 + 0x7a0180]
004A1606  8a 55 60                 mov      dl, byte ptr [ebp + 0x60]
004A1609  84 d2                    test     dl, dl
004A160B  89 b4 24 a8 00 00 00     mov      dword ptr [esp + 0xa8], esi
004A1612  74 06                    je       0x4a161a
004A1614  0f be 56 01              movsx    edx, byte ptr [esi + 1]
004A1618  eb 03                    jmp      0x4a161d
004A161A  0f be 16                 movsx    edx, byte ptr [esi]
004A161D  c1 e2 04                 shl      edx, 4
004A1620  89 54 24 58              mov      dword ptr [esp + 0x58], edx
004A1624  3b c7                    cmp      eax, edi
004A1626  8b 92 a0 00 7a 00        mov      edx, dword ptr [edx + 0x7a00a0]
004A162C  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A1630  0f 8c c3 0c 00 00        jl       0x4a22f9
004A1636  83 f8 08                 cmp      eax, 8
004A1639  0f 8f ba 0c 00 00        jg       0x4a22f9
004A163F  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
004A1644  74 24                    je       0x4a166a
004A1646  3b c7                    cmp      eax, edi
004A1648  74 20                    je       0x4a166a
004A164A  33 c9                    xor      ecx, ecx
004A164C  8a 6e 04                 mov      ch, byte ptr [esi + 4]
004A164F  66 89 4c 24 14           mov      word ptr [esp + 0x14], cx
004A1654  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004A1658  c1 ea 0c                 shr      edx, 0xc
004A165B  42                       inc      edx
004A165C  d1 ea                    shr      edx, 1
004A165E  83 e2 07                 and      edx, 7
004A1661  3b d0                    cmp      edx, eax
004A1663  74 05                    je       0x4a166a
004A1665  c6 44 24 13 01           mov      byte ptr [esp + 0x13], 1
004A166A  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A166D  8b 74 24 38              mov      esi, dword ptr [esp + 0x38]
004A1671  8b 5c 24 3c              mov      ebx, dword ptr [esp + 0x3c]
004A1675  8d 0c 40                 lea      ecx, [eax + eax*2]
004A1678  83 eb 07                 sub      ebx, 7
004A167B  89 5c 24 3c              mov      dword ptr [esp + 0x3c], ebx
004A167F  8b 14 8e                 mov      edx, dword ptr [esi + ecx*4]
004A1682  8d 0c 8e                 lea      ecx, [esi + ecx*4]
004A1685  85 d2                    test     edx, edx
004A1687  8b 49 04                 mov      ecx, dword ptr [ecx + 4]
004A168A  89 94 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], edx
004A1691  89 8c 24 90 00 00 00     mov      dword ptr [esp + 0x90], ecx
004A1698  75 0c                    jne      0x4a16a6
004A169A  85 c9                    test     ecx, ecx
004A169C  75 08                    jne      0x4a16a6
004A169E  85 c0                    test     eax, eax
004A16A0  0f 85 36 09 00 00        jne      0x4a1fdc
004A16A6  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A16A9  8b 11                    mov      edx, dword ptr [ecx]
004A16AB  ff 92 bc 00 00 00        call     dword ptr [edx + 0xbc]
004A16B1  84 c0                    test     al, al
004A16B3  74 4e                    je       0x4a1703
004A16B5  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A16B8  8d 81 88 00 00 00        lea      eax, [ecx + 0x88]
004A16BE  8b 91 88 00 00 00        mov      edx, dword ptr [ecx + 0x88]
004A16C4  89 94 24 dc 00 00 00     mov      dword ptr [esp + 0xdc], edx
004A16CB  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A16CE  89 94 24 e0 00 00 00     mov      dword ptr [esp + 0xe0], edx
004A16D5  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A16D8  89 84 24 e4 00 00 00     mov      dword ptr [esp + 0xe4], eax
004A16DF  8b 11                    mov      edx, dword ptr [ecx]
004A16E1  8d 84 24 dc 00 00 00     lea      eax, [esp + 0xdc]
004A16E8  50                       push     eax
004A16E9  ff 92 ec 00 00 00        call     dword ptr [edx + 0xec]
004A16EF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A16F2  c6 81 a0 05 00 00 00     mov      byte ptr [ecx + 0x5a0], 0
004A16F9  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A16FC  c6 82 a1 05 00 00 00     mov      byte ptr [edx + 0x5a1], 0
004A1703  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A1706  85 c0                    test     eax, eax
004A1708  75 1b                    jne      0x4a1725
004A170A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A170D  8d 54 24 24              lea      edx, [esp + 0x24]
004A1711  52                       push     edx
004A1712  8b 01                    mov      eax, dword ptr [ecx]
004A1714  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
004A171A  8b 00                    mov      eax, dword ptr [eax]
004A171C  89 84 24 98 00 00 00     mov      dword ptr [esp + 0x98], eax
004A1723  eb 7d                    jmp      0x4a17a2
004A1725  8d 0c 40                 lea      ecx, [eax + eax*2]
004A1728  8b 54 8e fc              mov      edx, dword ptr [esi + ecx*4 - 4]
004A172C  8d 04 8e                 lea      eax, [esi + ecx*4]
004A172F  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A1733  8d 94 24 80 00 00 00     lea      edx, [esp + 0x80]
004A173A  8b 48 f8                 mov      ecx, dword ptr [eax - 8]
004A173D  8b 40 f4                 mov      eax, dword ptr [eax - 0xc]
004A1740  89 8c 24 84 00 00 00     mov      dword ptr [esp + 0x84], ecx
004A1747  8d 4c 24 30              lea      ecx, [esp + 0x30]
004A174B  89 84 24 80 00 00 00     mov      dword ptr [esp + 0x80], eax
004A1752  51                       push     ecx
004A1753  8d 84 24 c8 00 00 00     lea      eax, [esp + 0xc8]
004A175A  52                       push     edx
004A175B  50                       push     eax
004A175C  8b cd                    mov      ecx, ebp
004A175E  e8 dd 2f 00 00           call     0x4a4740
004A1763  8b 08                    mov      ecx, dword ptr [eax]
004A1765  8b 70 04                 mov      esi, dword ptr [eax + 4]
004A1768  8b c1                    mov      eax, ecx
004A176A  99                       cdq      
004A176B  81 e2 ff 00 00 00        and      edx, 0xff
004A1771  03 c2                    add      eax, edx
004A1773  c1 f8 08                 sar      eax, 8
004A1776  66 89 84 24 a0 00 00 00  mov      word ptr [esp + 0xa0], ax
004A177E  8b c6                    mov      eax, esi
004A1780  99                       cdq      
004A1781  81 e2 ff 00 00 00        and      edx, 0xff
004A1787  03 c2                    add      eax, edx
004A1789  c1 f8 08                 sar      eax, 8
004A178C  66 89 84 24 a2 00 00 00  mov      word ptr [esp + 0xa2], ax
004A1794  8b 8c 24 a0 00 00 00     mov      ecx, dword ptr [esp + 0xa0]
004A179B  89 8c 24 98 00 00 00     mov      dword ptr [esp + 0x98], ecx
004A17A2  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A17A5  8d 14 40                 lea      edx, [eax + eax*2]
004A17A8  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004A17AC  8b 4c 90 08              mov      ecx, dword ptr [eax + edx*4 + 8]
004A17B0  8d 54 24 30              lea      edx, [esp + 0x30]
004A17B4  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
004A17B8  8d 84 24 8c 00 00 00     lea      eax, [esp + 0x8c]
004A17BF  52                       push     edx
004A17C0  8d 8c 24 b0 00 00 00     lea      ecx, [esp + 0xb0]
004A17C7  50                       push     eax
004A17C8  51                       push     ecx
004A17C9  8b cd                    mov      ecx, ebp
004A17CB  e8 70 2f 00 00           call     0x4a4740
004A17D0  8b 08                    mov      ecx, dword ptr [eax]
004A17D2  8b 78 04                 mov      edi, dword ptr [eax + 4]
004A17D5  33 c0                    xor      eax, eax
004A17D7  89 4c 24 48              mov      dword ptr [esp + 0x48], ecx
004A17DB  89 44 24 50              mov      dword ptr [esp + 0x50], eax
004A17DF  8b c1                    mov      eax, ecx
004A17E1  99                       cdq      
004A17E2  81 e2 ff 00 00 00        and      edx, 0xff
004A17E8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A17EB  03 c2                    add      eax, edx
004A17ED  89 7c 24 4c              mov      dword ptr [esp + 0x4c], edi
004A17F1  8b f0                    mov      esi, eax
004A17F3  8b c7                    mov      eax, edi
004A17F5  99                       cdq      
004A17F6  81 e2 ff 00 00 00        and      edx, 0xff
004A17FC  03 c2                    add      eax, edx
004A17FE  8d 91 88 00 00 00        lea      edx, [ecx + 0x88]
004A1804  8b d8                    mov      ebx, eax
004A1806  8b 02                    mov      eax, dword ptr [edx]
004A1808  c1 fe 08                 sar      esi, 8
004A180B  8b 7a 04                 mov      edi, dword ptr [edx + 4]
004A180E  66 89 b4 24 a4 00 00 00  mov      word ptr [esp + 0xa4], si
004A1816  89 bc 24 ec 00 00 00     mov      dword ptr [esp + 0xec], edi
004A181D  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A1820  89 94 24 f0 00 00 00     mov      dword ptr [esp + 0xf0], edx
004A1827  99                       cdq      
004A1828  81 e2 ff 00 00 00        and      edx, 0xff
004A182E  03 c2                    add      eax, edx
004A1830  8b f8                    mov      edi, eax
004A1832  8b 84 24 ec 00 00 00     mov      eax, dword ptr [esp + 0xec]
004A1839  99                       cdq      
004A183A  81 e2 ff 00 00 00        and      edx, 0xff
004A1840  c1 fb 08                 sar      ebx, 8
004A1843  03 c2                    add      eax, edx
004A1845  66 89 9c 24 a6 00 00 00  mov      word ptr [esp + 0xa6], bx
004A184D  8b 94 24 a4 00 00 00     mov      edx, dword ptr [esp + 0xa4]
004A1854  c1 ff 08                 sar      edi, 8
004A1857  c1 f8 08                 sar      eax, 8
004A185A  66 3b f7                 cmp      si, di
004A185D  89 54 24 68              mov      dword ptr [esp + 0x68], edx
004A1861  75 09                    jne      0x4a186c
004A1863  66 3b d8                 cmp      bx, ax
004A1866  0f 84 44 02 00 00        je       0x4a1ab0
004A186C  8b 01                    mov      eax, dword ptr [ecx]
004A186E  6a 00                    push     0
004A1870  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004A1876  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1879  8d 44 24 48              lea      eax, [esp + 0x48]
004A187D  50                       push     eax
004A187E  8b 11                    mov      edx, dword ptr [ecx]
004A1880  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
004A1886  8d 8c 24 98 00 00 00     lea      ecx, [esp + 0x98]
004A188D  51                       push     ecx
004A188E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1893  e8 d8 67 0a 00           call     0x548070
004A1898  8d 54 24 68              lea      edx, [esp + 0x68]
004A189C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A18A1  52                       push     edx
004A18A2  8b f0                    mov      esi, eax
004A18A4  e8 c7 67 0a 00           call     0x548070
004A18A9  8b d8                    mov      ebx, eax
004A18AB  0f be 86 1b 01 00 00     movsx    eax, byte ptr [esi + 0x11b]
004A18B2  0f be 8b 1b 01 00 00     movsx    ecx, byte ptr [ebx + 0x11b]
004A18B9  83 e8 04                 sub      eax, 4
004A18BC  89 5c 24 40              mov      dword ptr [esp + 0x40], ebx
004A18C0  3b c8                    cmp      ecx, eax
004A18C2  b8 00 01 00 00           mov      eax, 0x100
004A18C7  75 0f                    jne      0x4a18d8
004A18C9  85 83 40 01 00 00        test     dword ptr [ebx + 0x140], eax
004A18CF  74 0f                    je       0x4a18e0
004A18D1  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A18D4  c6 42 79 01              mov      byte ptr [edx + 0x79], 1
004A18D8  85 83 40 01 00 00        test     dword ptr [ebx + 0x140], eax
004A18DE  75 0f                    jne      0x4a18ef
004A18E0  85 86 40 01 00 00        test     dword ptr [esi + 0x140], eax
004A18E6  74 07                    je       0x4a18ef
004A18E8  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A18EB  c6 40 79 00              mov      byte ptr [eax + 0x79], 0
004A18EF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A18F2  8b 11                    mov      edx, dword ptr [ecx]
004A18F4  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A18FA  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A1900  84 c9                    test     cl, cl
004A1902  0f 84 19 01 00 00        je       0x4a1a21
004A1908  8b 7d 0c                 mov      edi, dword ptr [ebp + 0xc]
004A190B  8a 87 b8 05 00 00        mov      al, byte ptr [edi + 0x5b8]
004A1911  84 c0                    test     al, al
004A1913  0f 85 08 01 00 00        jne      0x4a1a21
004A1919  8a 47 79                 mov      al, byte ptr [edi + 0x79]
004A191C  84 c0                    test     al, al
004A191E  75 51                    jne      0x4a1971
004A1920  8d 87 88 00 00 00        lea      eax, [edi + 0x88]
004A1926  8b c8                    mov      ecx, eax
004A1928  8b 11                    mov      edx, dword ptr [ecx]
004A192A  89 54 24 5c              mov      dword ptr [esp + 0x5c], edx
004A192E  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A1931  89 54 24 60              mov      dword ptr [esp + 0x60], edx
004A1935  8b 71 08                 mov      esi, dword ptr [ecx + 8]
004A1938  8b 08                    mov      ecx, dword ptr [eax]
004A193A  89 8c 24 d0 00 00 00     mov      dword ptr [esp + 0xd0], ecx
004A1941  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A1944  8d 8c 24 d0 00 00 00     lea      ecx, [esp + 0xd0]
004A194B  89 94 24 d4 00 00 00     mov      dword ptr [esp + 0xd4], edx
004A1952  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A1955  51                       push     ecx
004A1956  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A195B  89 84 24 dc 00 00 00     mov      dword ptr [esp + 0xdc], eax
004A1962  e8 19 89 0b 00           call     0x55a280
004A1967  03 05 c0 29 85 00        add      eax, dword ptr [0x8529c0]
004A196D  3b f0                    cmp      esi, eax
004A196F  7c 17                    jl       0x4a1988
004A1971  8d 54 24 68              lea      edx, [esp + 0x68]
004A1975  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A197A  52                       push     edx
004A197B  e8 f0 66 0a 00           call     0x548070
004A1980  8b 80 e8 00 00 00        mov      eax, dword ptr [eax + 0xe8]
004A1986  eb 15                    jmp      0x4a199d
004A1988  8d 44 24 68              lea      eax, [esp + 0x68]
004A198C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1991  50                       push     eax
004A1992  e8 d9 66 0a 00           call     0x548070
004A1997  8b 80 e4 00 00 00        mov      eax, dword ptr [eax + 0xe4]
004A199D  8b f0                    mov      esi, eax
004A199F  85 f6                    test     esi, esi
004A19A1  74 7e                    je       0x4a1a21
004A19A3  8b 16                    mov      edx, dword ptr [esi]
004A19A5  8b 5e 30                 mov      ebx, dword ptr [esi + 0x30]
004A19A8  8b ce                    mov      ecx, esi
004A19AA  ff 92 84 00 00 00        call     dword ptr [edx + 0x84]
004A19B0  8a 88 fd 01 00 00        mov      cl, byte ptr [eax + 0x1fd]
004A19B6  84 c9                    test     cl, cl
004A19B8  75 5d                    jne      0x4a1a17
004A19BA  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A19C0  8b 06                    mov      eax, dword ptr [esi]
004A19C2  c7 44 24 70 10 27 00 00  mov      dword ptr [esp + 0x70], 0x2710
004A19CA  6a 01                    push     1
004A19CC  8b 91 74 0c 00 00        mov      edx, dword ptr [ecx + 0xc74]
004A19D2  6a 01                    push     1
004A19D4  6a 00                    push     0
004A19D6  52                       push     edx
004A19D7  8d 8c 24 80 00 00 00     lea      ecx, [esp + 0x80]
004A19DE  6a 00                    push     0
004A19E0  51                       push     ecx
004A19E1  8b ce                    mov      ecx, esi
004A19E3  ff 90 58 01 00 00        call     dword ptr [eax + 0x158]
004A19E9  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A19EE  8b 17                    mov      edx, dword ptr [edi]
004A19F0  c7 44 24 70 14 00 00 00  mov      dword ptr [esp + 0x70], 0x14
004A19F8  6a 00                    push     0
004A19FA  8b 88 74 0c 00 00        mov      ecx, dword ptr [eax + 0xc74]
004A1A00  6a 01                    push     1
004A1A02  6a 00                    push     0
004A1A04  51                       push     ecx
004A1A05  8d 84 24 80 00 00 00     lea      eax, [esp + 0x80]
004A1A0C  6a 00                    push     0
004A1A0E  50                       push     eax
004A1A0F  8b cf                    mov      ecx, edi
004A1A11  ff 92 58 01 00 00        call     dword ptr [edx + 0x158]
004A1A17  85 db                    test     ebx, ebx
004A1A19  8b f3                    mov      esi, ebx
004A1A1B  75 86                    jne      0x4a19a3
004A1A1D  8b 5c 24 40              mov      ebx, dword ptr [esp + 0x40]
004A1A21  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1A24  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
004A1A27  84 c0                    test     al, al
004A1A29  0f 84 0b 0c 00 00        je       0x4a263a
004A1A2F  8b 11                    mov      edx, dword ptr [ecx]
004A1A31  6a 01                    push     1
004A1A33  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004A1A39  8b 43 44                 mov      eax, dword ptr [ebx + 0x44]
004A1A3C  83 f8 ff                 cmp      eax, -1
004A1A3F  0f 84 88 00 00 00        je       0x4a1acd
004A1A45  8b 0d ec 5d a3 00        mov      ecx, dword ptr [0xa35dec]
004A1A4B  8b 34 81                 mov      esi, dword ptr [ecx + eax*4]
004A1A4E  8a 45 64                 mov      al, byte ptr [ebp + 0x64]
004A1A51  84 c0                    test     al, al
004A1A53  74 78                    je       0x4a1acd
004A1A55  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1A58  8b 11                    mov      edx, dword ptr [ecx]
004A1A5A  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A1A60  8a 88 f3 0a 00 00        mov      cl, byte ptr [eax + 0xaf3]
004A1A66  84 c9                    test     cl, cl
004A1A68  75 0e                    jne      0x4a1a78
004A1A6A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1A6D  6a 11                    push     0x11
004A1A6F  e8 9c 5e 23 00           call     0x6d7910
004A1A74  84 c0                    test     al, al
004A1A76  74 55                    je       0x4a1acd
004A1A78  8b 86 64 02 00 00        mov      eax, dword ptr [esi + 0x264]
004A1A7E  85 c0                    test     eax, eax
004A1A80  75 4b                    jne      0x4a1acd
004A1A82  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1A85  c6 80 9f 05 00 00 01     mov      byte ptr [eax + 0x59f], 1
004A1A8C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1A8F  8b 11                    mov      edx, dword ptr [ecx]
004A1A91  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A1A97  8a 88 f4 0a 00 00        mov      cl, byte ptr [eax + 0xaf4]
004A1A9D  84 c9                    test     cl, cl
004A1A9F  74 2c                    je       0x4a1acd
004A1AA1  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1AA4  c7 80 8c 02 00 00 0a d7 a3 bc mov      dword ptr [eax + 0x28c], 0xbca3d70a
004A1AAE  eb 1d                    jmp      0x4a1acd
004A1AB0  8a 59 74                 mov      bl, byte ptr [ecx + 0x74]
004A1AB3  c6 41 74 00              mov      byte ptr [ecx + 0x74], 0
004A1AB7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1ABA  8d 44 24 48              lea      eax, [esp + 0x48]
004A1ABE  50                       push     eax
004A1ABF  8b 11                    mov      edx, dword ptr [ecx]
004A1AC1  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
004A1AC7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1ACA  88 59 74                 mov      byte ptr [ecx + 0x74], bl
004A1ACD  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1AD0  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A1AD3  84 c9                    test     cl, cl
004A1AD5  0f 84 5f 0b 00 00        je       0x4a263a
004A1ADB  8a 58 74                 mov      bl, byte ptr [eax + 0x74]
004A1ADE  c6 40 74 00              mov      byte ptr [eax + 0x74], 0
004A1AE2  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1AE5  6a 00                    push     0
004A1AE7  8b 11                    mov      edx, dword ptr [ecx]
004A1AE9  ff 92 b4 01 00 00        call     dword ptr [edx + 0x1b4]
004A1AEF  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1AF2  33 c9                    xor      ecx, ecx
004A1AF4  8d 54 24 54              lea      edx, [esp + 0x54]
004A1AF8  88 58 74                 mov      byte ptr [eax + 0x74], bl
004A1AFB  8a 6c 24 30              mov      ch, byte ptr [esp + 0x30]
004A1AFF  66 89 4c 24 54           mov      word ptr [esp + 0x54], cx
004A1B04  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1B07  52                       push     edx
004A1B08  81 c1 e0 02 00 00        add      ecx, 0x2e0
004A1B0E  e8 fd 6f 01 00           call     0x4b8b10
004A1B13  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A1B16  85 c0                    test     eax, eax
004A1B18  74 46                    je       0x4a1b60
004A1B1A  8b 4c 24 58              mov      ecx, dword ptr [esp + 0x58]
004A1B1E  39 81 ac 00 7a 00        cmp      dword ptr [ecx + 0x7a00ac], eax
004A1B24  75 3a                    jne      0x4a1b60
004A1B26  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1B29  8d 91 88 00 00 00        lea      edx, [ecx + 0x88]
004A1B2F  8b 81 88 00 00 00        mov      eax, dword ptr [ecx + 0x88]
004A1B35  89 84 24 b8 00 00 00     mov      dword ptr [esp + 0xb8], eax
004A1B3C  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A1B3F  89 84 24 bc 00 00 00     mov      dword ptr [esp + 0xbc], eax
004A1B46  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A1B49  89 94 24 c0 00 00 00     mov      dword ptr [esp + 0xc0], edx
004A1B50  8b 01                    mov      eax, dword ptr [ecx]
004A1B52  8d 94 24 b8 00 00 00     lea      edx, [esp + 0xb8]
004A1B59  52                       push     edx
004A1B5A  ff 90 ec 00 00 00        call     dword ptr [eax + 0xec]
004A1B60  8b 44 24 44              mov      eax, dword ptr [esp + 0x44]
004A1B64  83 f8 08                 cmp      eax, 8
004A1B67  0f 84 20 04 00 00        je       0x4a1f8d
004A1B6D  83 f8 ff                 cmp      eax, -1
004A1B70  0f 84 17 04 00 00        je       0x4a1f8d
004A1B76  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
004A1B7A  84 c0                    test     al, al
004A1B7C  0f 84 0b 04 00 00        je       0x4a1f8d
004A1B82  8b 4c 24 58              mov      ecx, dword ptr [esp + 0x58]
004A1B86  8b 45 5c                 mov      eax, dword ptr [ebp + 0x5c]
004A1B89  39 81 a4 00 7a 00        cmp      dword ptr [ecx + 0x7a00a4], eax
004A1B8F  0f 85 f8 03 00 00        jne      0x4a1f8d
004A1B95  85 c0                    test     eax, eax
004A1B97  0f 84 f0 03 00 00        je       0x4a1f8d
004A1B9D  8b 84 24 a8 00 00 00     mov      eax, dword ptr [esp + 0xa8]
004A1BA4  33 d2                    xor      edx, edx
004A1BA6  8a 70 04                 mov      dh, byte ptr [eax + 4]
004A1BA9  66 89 54 24 6c           mov      word ptr [esp + 0x6c], dx
004A1BAE  8b 54 24 44              mov      edx, dword ptr [esp + 0x44]
004A1BB2  8b 4c 24 6c              mov      ecx, dword ptr [esp + 0x6c]
004A1BB6  c1 e9 0c                 shr      ecx, 0xc
004A1BB9  41                       inc      ecx
004A1BBA  d1 e9                    shr      ecx, 1
004A1BBC  83 e1 07                 and      ecx, 7
004A1BBF  8d 04 ca                 lea      eax, [edx + ecx*8]
004A1BC2  89 44 24 40              mov      dword ptr [esp + 0x40], eax
004A1BC6  8d 04 40                 lea      eax, [eax + eax*2]
004A1BC9  8d 1c 85 80 01 7a 00     lea      ebx, [eax*4 + 0x7a0180]
004A1BD0  8a 04 85 80 01 7a 00     mov      al, byte ptr [eax*4 + 0x7a0180]
004A1BD7  84 c0                    test     al, al
004A1BD9  0f 84 ae 03 00 00        je       0x4a1f8d
004A1BDF  0f be c8                 movsx    ecx, al
004A1BE2  c1 e1 04                 shl      ecx, 4
004A1BE5  8b 81 a8 00 7a 00        mov      eax, dword ptr [ecx + 0x7a00a8]
004A1BEB  85 c0                    test     eax, eax
004A1BED  0f 84 9a 03 00 00        je       0x4a1f8d
004A1BF3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1BF6  8d 75 40                 lea      esi, [ebp + 0x40]
004A1BF9  6a 01                    push     1
004A1BFB  6a 00                    push     0
004A1BFD  8b 91 68 04 00 00        mov      edx, dword ptr [ecx + 0x468]
004A1C03  8b 81 6c 04 00 00        mov      eax, dword ptr [ecx + 0x46c]
004A1C09  89 54 24 7c              mov      dword ptr [esp + 0x7c], edx
004A1C0D  8b 54 24 4c              mov      edx, dword ptr [esp + 0x4c]
004A1C11  83 e2 07                 and      edx, 7
004A1C14  89 84 24 80 00 00 00     mov      dword ptr [esp + 0x80], eax
004A1C1B  8b 06                    mov      eax, dword ptr [esi]
004A1C1D  8b 3c d5 c0 1a 85 00     mov      edi, dword ptr [edx*8 + 0x851ac0]
004A1C24  8d 14 d5 c0 1a 85 00     lea      edx, [edx*8 + 0x851ac0]
004A1C2B  03 c7                    add      eax, edi
004A1C2D  8b 7a 04                 mov      edi, dword ptr [edx + 4]
004A1C30  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A1C33  03 fa                    add      edi, edx
004A1C35  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A1C38  89 44 24 20              mov      dword ptr [esp + 0x20], eax
004A1C3C  89 54 24 28              mov      dword ptr [esp + 0x28], edx
004A1C40  99                       cdq      
004A1C41  81 e2 ff 00 00 00        and      edx, 0xff
004A1C47  89 7c 24 24              mov      dword ptr [esp + 0x24], edi
004A1C4B  03 c2                    add      eax, edx
004A1C4D  c1 f8 08                 sar      eax, 8
004A1C50  66 89 84 24 9c 00 00 00  mov      word ptr [esp + 0x9c], ax
004A1C58  8b c7                    mov      eax, edi
004A1C5A  99                       cdq      
004A1C5B  81 e2 ff 00 00 00        and      edx, 0xff
004A1C61  03 c2                    add      eax, edx
004A1C63  c1 f8 08                 sar      eax, 8
004A1C66  66 89 84 24 9e 00 00 00  mov      word ptr [esp + 0x9e], ax
004A1C6E  8b 84 24 9c 00 00 00     mov      eax, dword ptr [esp + 0x9c]
004A1C75  89 44 24 3c              mov      dword ptr [esp + 0x3c], eax
004A1C79  8b 39                    mov      edi, dword ptr [ecx]
004A1C7B  e8 50 2b 13 00           call     0x5d47d0
004A1C80  8b 4c 24 4c              mov      ecx, dword ptr [esp + 0x4c]
004A1C84  50                       push     eax
004A1C85  8d 54 24 40              lea      edx, [esp + 0x40]
004A1C89  51                       push     ecx
004A1C8A  52                       push     edx
004A1C8B  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1C90  e8 db 63 0a 00           call     0x548070
004A1C95  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1C98  50                       push     eax
004A1C99  ff 97 94 01 00 00        call     dword ptr [edi + 0x194]
004A1C9F  83 f8 06                 cmp      eax, 6
004A1CA2  0f 87 e5 02 00 00        ja       0x4a1f8d
004A1CA8  ff 24 85 4c 26 4a 00     jmp      dword ptr [eax*4 + 0x4a264c]
004A1CAF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1CB2  8b 01                    mov      eax, dword ptr [ecx]
004A1CB4  ff 50 2c                 call     dword ptr [eax + 0x2c]
004A1CB7  83 f8 01                 cmp      eax, 1
004A1CBA  75 17                    jne      0x4a1cd3
004A1CBC  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1CBF  8b 91 ac 05 00 00        mov      edx, dword ptr [ecx + 0x5ac]
004A1CC5  8a 82 a4 0b 00 00        mov      al, byte ptr [edx + 0xba4]
004A1CCB  84 c0                    test     al, al
004A1CCD  0f 84 ba 02 00 00        je       0x4a1f8d
004A1CD3  8b 44 24 40              mov      eax, dword ptr [esp + 0x40]
004A1CD7  c6 45 60 00              mov      byte ptr [ebp + 0x60], 0
004A1CDB  89 45 58                 mov      dword ptr [ebp + 0x58], eax
004A1CDE  89 9c 24 a8 00 00 00     mov      dword ptr [esp + 0xa8], ebx
004A1CE5  0f be 03                 movsx    eax, byte ptr [ebx]
004A1CE8  c1 e0 04                 shl      eax, 4
004A1CEB  89 44 24 58              mov      dword ptr [esp + 0x58], eax
004A1CEF  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
004A1CF4  8b 88 a8 00 7a 00        mov      ecx, dword ptr [eax + 0x7a00a8]
004A1CFA  49                       dec      ecx
004A1CFB  89 4d 5c                 mov      dword ptr [ebp + 0x5c], ecx
004A1CFE  8b 90 a0 00 7a 00        mov      edx, dword ptr [eax + 0x7a00a0]
004A1D04  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A1D09  8b 0e                    mov      ecx, dword ptr [esi]
004A1D0B  3b c8                    cmp      ecx, eax
004A1D0D  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A1D11  75 1a                    jne      0x4a1d2d
004A1D13  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A1D16  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1D1C  3b ca                    cmp      ecx, edx
004A1D1E  75 0d                    jne      0x4a1d2d
004A1D20  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A1D23  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A1D29  3b d1                    cmp      edx, ecx
004A1D2B  74 19                    je       0x4a1d46
004A1D2D  8b ce                    mov      ecx, esi
004A1D2F  89 01                    mov      dword ptr [ecx], eax
004A1D31  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1D37  89 51 04                 mov      dword ptr [ecx + 4], edx
004A1D3A  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A1D3F  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1D43  89 41 08                 mov      dword ptr [ecx + 8], eax
004A1D46  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1D49  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A1D4D  6a 02                    push     2
004A1D4F  8b 11                    mov      edx, dword ptr [ecx]
004A1D51  ff 92 74 01 00 00        call     dword ptr [edx + 0x174]
004A1D57  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1D5A  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1D5E  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A1D61  84 c9                    test     cl, cl
004A1D63  0f 84 d1 08 00 00        je       0x4a263a
004A1D69  8a 48 76                 mov      cl, byte ptr [eax + 0x76]
004A1D6C  84 c9                    test     cl, cl
004A1D6E  0f 85 c6 08 00 00        jne      0x4a263a
004A1D74  8a 48 7a                 mov      cl, byte ptr [eax + 0x7a]
004A1D77  84 c9                    test     cl, cl
004A1D79  0f 85 bb 08 00 00        jne      0x4a263a
004A1D7F  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A1D85  8b 0e                    mov      ecx, dword ptr [esi]
004A1D87  3b ca                    cmp      ecx, edx
004A1D89  75 1a                    jne      0x4a1da5
004A1D8B  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A1D8E  8b 3d 9c 29 85 00        mov      edi, dword ptr [0x85299c]
004A1D94  3b cf                    cmp      ecx, edi
004A1D96  75 0d                    jne      0x4a1da5
004A1D98  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A1D9B  8b 3d a0 29 85 00        mov      edi, dword ptr [0x8529a0]
004A1DA1  3b cf                    cmp      ecx, edi
004A1DA3  74 20                    je       0x4a1dc5
004A1DA5  8b ce                    mov      ecx, esi
004A1DA7  89 11                    mov      dword ptr [ecx], edx
004A1DA9  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1DAF  89 51 04                 mov      dword ptr [ecx + 4], edx
004A1DB2  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A1DB8  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1DBC  89 51 08                 mov      dword ptr [ecx + 8], edx
004A1DBF  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A1DC5  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004A1DC9  8b 7c 24 1c              mov      edi, dword ptr [esp + 0x1c]
004A1DCD  3b ca                    cmp      ecx, edx
004A1DCF  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004A1DD3  75 14                    jne      0x4a1de9
004A1DD5  3b 3d 9c 29 85 00        cmp      edi, dword ptr [0x85299c]
004A1DDB  75 0c                    jne      0x4a1de9
004A1DDD  3b 15 a0 29 85 00        cmp      edx, dword ptr [0x8529a0]
004A1DE3  0f 84 a4 01 00 00        je       0x4a1f8d
004A1DE9  8b de                    mov      ebx, esi
004A1DEB  50                       push     eax
004A1DEC  8d 44 24 1c              lea      eax, [esp + 0x1c]
004A1DF0  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A1DF4  89 0b                    mov      dword ptr [ebx], ecx
004A1DF6  50                       push     eax
004A1DF7  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1DFC  89 7b 04                 mov      dword ptr [ebx + 4], edi
004A1DFF  89 53 08                 mov      dword ptr [ebx + 8], edx
004A1E02  e8 f9 61 0a 00           call     0x548000
004A1E07  8b c8                    mov      ecx, eax
004A1E09  e8 b2 4e fd ff           call     0x476cc0
004A1E0E  84 c0                    test     al, al
004A1E10  74 55                    je       0x4a1e67
004A1E12  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E15  8a 41 76                 mov      al, byte ptr [ecx + 0x76]
004A1E18  84 c0                    test     al, al
004A1E1A  75 4b                    jne      0x4a1e67
004A1E1C  8d 54 24 18              lea      edx, [esp + 0x18]
004A1E20  6a 01                    push     1
004A1E22  52                       push     edx
004A1E23  8b cd                    mov      ecx, ebp
004A1E25  e8 96 ed ff ff           call     0x4a0bc0
004A1E2A  8b 44 24 78              mov      eax, dword ptr [esp + 0x78]
004A1E2E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E31  50                       push     eax
004A1E32  8b 44 24 78              mov      eax, dword ptr [esp + 0x78]
004A1E36  8b 11                    mov      edx, dword ptr [ecx]
004A1E38  50                       push     eax
004A1E39  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A1E3F  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1E42  b9 17 00 00 00           mov      ecx, 0x17
004A1E47  8d b0 d4 04 00 00        lea      esi, [eax + 0x4d4]
004A1E4D  8d b8 d0 04 00 00        lea      edi, [eax + 0x4d0]
004A1E53  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004A1E55  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1E58  c7 81 2c 05 00 00 ff ff ff ff mov      dword ptr [ecx + 0x52c], 0xffffffff
004A1E62  e9 26 01 00 00           jmp      0x4a1f8d
004A1E67  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A1E6A  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A1E6D  84 c9                    test     cl, cl
004A1E6F  0f 84 18 01 00 00        je       0x4a1f8d
004A1E75  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A1E7B  89 0e                    mov      dword ptr [esi], ecx
004A1E7D  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A1E83  89 56 04                 mov      dword ptr [esi + 4], edx
004A1E86  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A1E8B  89 46 08                 mov      dword ptr [esi + 8], eax
004A1E8E  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A1E92  e9 f6 00 00 00           jmp      0x4a1f8d
004A1E97  8d 54 24 18              lea      edx, [esp + 0x18]
004A1E9B  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1EA0  52                       push     edx
004A1EA1  e8 5a 61 0a 00           call     0x548000
004A1EA6  8b c8                    mov      ecx, eax
004A1EA8  e8 93 68 fd ff           call     0x478740
004A1EAD  e9 db 00 00 00           jmp      0x4a1f8d
004A1EB2  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004A1EB6  8d 4c 24 40              lea      ecx, [esp + 0x40]
004A1EBA  99                       cdq      
004A1EBB  81 e2 ff 00 00 00        and      edx, 0xff
004A1EC1  51                       push     ecx
004A1EC2  03 c2                    add      eax, edx
004A1EC4  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1EC9  c1 f8 08                 sar      eax, 8
004A1ECC  66 89 84 24 a0 00 00 00  mov      word ptr [esp + 0xa0], ax
004A1ED4  8b 44 24 20              mov      eax, dword ptr [esp + 0x20]
004A1ED8  99                       cdq      
004A1ED9  81 e2 ff 00 00 00        and      edx, 0xff
004A1EDF  03 c2                    add      eax, edx
004A1EE1  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A1EE4  c1 f8 08                 sar      eax, 8
004A1EE7  66 89 84 24 a2 00 00 00  mov      word ptr [esp + 0xa2], ax
004A1EEF  8b 84 24 a0 00 00 00     mov      eax, dword ptr [esp + 0xa0]
004A1EF6  52                       push     edx
004A1EF7  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A1EFB  e8 d0 8d 0b 00           call     0x55acd0
004A1F00  e9 88 00 00 00           jmp      0x4a1f8d
004A1F05  8d 44 24 18              lea      eax, [esp + 0x18]
004A1F09  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F0E  50                       push     eax
004A1F0F  e8 ec 60 0a 00           call     0x548000
004A1F14  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004A1F1A  f6 c5 01                 test     ch, 1
004A1F1D  74 49                    je       0x4a1f68
004A1F1F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A1F22  81 c1 88 00 00 00        add      ecx, 0x88
004A1F28  8b 11                    mov      edx, dword ptr [ecx]
004A1F2A  89 54 24 5c              mov      dword ptr [esp + 0x5c], edx
004A1F2E  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A1F31  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004A1F35  8b 79 08                 mov      edi, dword ptr [ecx + 8]
004A1F38  8d 4c 24 18              lea      ecx, [esp + 0x18]
004A1F3C  51                       push     ecx
004A1F3D  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F42  e8 b9 60 0a 00           call     0x548000
004A1F47  0f be 88 1b 01 00 00     movsx    ecx, byte ptr [eax + 0x11b]
004A1F4E  8b c7                    mov      eax, edi
004A1F50  c6 44 24 14 01           mov      byte ptr [esp + 0x14], 1
004A1F55  99                       cdq      
004A1F56  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A1F5C  2b c1                    sub      eax, ecx
004A1F5E  99                       cdq      
004A1F5F  33 c2                    xor      eax, edx
004A1F61  2b c2                    sub      eax, edx
004A1F63  83 f8 02                 cmp      eax, 2
004A1F66  7f 05                    jg       0x4a1f6d
004A1F68  c6 44 24 14 00           mov      byte ptr [esp + 0x14], 0
004A1F6D  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004A1F71  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A1F76  52                       push     edx
004A1F77  6a 01                    push     1
004A1F79  6a 01                    push     1
004A1F7B  68 98 29 85 00           push     0x852998
004A1F80  56                       push     esi
004A1F81  e8 7a 60 0a 00           call     0x548000
004A1F86  8b c8                    mov      ecx, eax
004A1F88  e8 93 49 fd ff           call     0x476920
004A1F8D  8b 4d 5c                 mov      ecx, dword ptr [ebp + 0x5c]
004A1F90  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
004A1F94  41                       inc      ecx
004A1F95  83 f8 07                 cmp      eax, 7
004A1F98  89 4d 5c                 mov      dword ptr [ebp + 0x5c], ecx
004A1F9B  0f 8f c9 f6 ff ff        jg       0x4a166a
004A1FA1  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
004A1FA5  33 ff                    xor      edi, edi
004A1FA7  3b c7                    cmp      eax, edi
004A1FA9  89 45 4c                 mov      dword ptr [ebp + 0x4c], eax
004A1FAC  0f 8e 88 06 00 00        jle      0x4a263a
004A1FB2  8b 45 58                 mov      eax, dword ptr [ebp + 0x58]
004A1FB5  83 f8 ff                 cmp      eax, -1
004A1FB8  0f 8e 7c 06 00 00        jle      0x4a263a
004A1FBE  8d 0c 40                 lea      ecx, [eax + eax*2]
004A1FC1  8d 04 8d 80 01 7a 00     lea      eax, [ecx*4 + 0x7a0180]
004A1FC8  8a 4d 60                 mov      cl, byte ptr [ebp + 0x60]
004A1FCB  84 c9                    test     cl, cl
004A1FCD  0f 84 3b 03 00 00        je       0x4a230e
004A1FD3  0f be 40 01              movsx    eax, byte ptr [eax + 1]
004A1FD7  e9 35 03 00 00           jmp      0x4a2311
004A1FDC  8b 7d 0c                 mov      edi, dword ptr [ebp + 0xc]
004A1FDF  8d 75 40                 lea      esi, [ebp + 0x40]
004A1FE2  8d 87 88 00 00 00        lea      eax, [edi + 0x88]
004A1FE8  8b 8f 88 00 00 00        mov      ecx, dword ptr [edi + 0x88]
004A1FEE  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A1FF1  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A1FF4  89 44 24 64              mov      dword ptr [esp + 0x64], eax
004A1FF8  8b 06                    mov      eax, dword ptr [esi]
004A1FFA  2b c1                    sub      eax, ecx
004A1FFC  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A1FFF  2b ca                    sub      ecx, edx
004A2001  99                       cdq      
004A2002  8b d8                    mov      ebx, eax
004A2004  8b c1                    mov      eax, ecx
004A2006  33 da                    xor      ebx, edx
004A2008  2b da                    sub      ebx, edx
004A200A  99                       cdq      
004A200B  33 c2                    xor      eax, edx
004A200D  2b c2                    sub      eax, edx
004A200F  03 d8                    add      ebx, eax
004A2011  89 5c 24 34              mov      dword ptr [esp + 0x34], ebx
004A2015  db 44 24 34              fild     dword ptr [esp + 0x34]
004A2019  dc 0d d0 05 7a 00        fmul     qword ptr [0x7a05d0]
004A201F  dc 2d 08 a7 79 00        fsubr    qword ptr [0x79a708]
004A2025  dc 0d c8 05 7a 00        fmul     qword ptr [0x7a05c8]
004A202B  e8 e0 d0 2d 00           call     0x77f110
004A2030  8b 5c 24 3c              mov      ebx, dword ptr [esp + 0x3c]
004A2034  c6 87 a0 05 00 00 01     mov      byte ptr [edi + 0x5a0], 1
004A203B  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A203E  03 d8                    add      ebx, eax
004A2040  89 5c 24 3c              mov      dword ptr [esp + 0x3c], ebx
004A2044  c6 81 a1 05 00 00 00     mov      byte ptr [ecx + 0x5a1], 0
004A204B  8b 5d 0c                 mov      ebx, dword ptr [ebp + 0xc]
004A204E  8d 93 88 00 00 00        lea      edx, [ebx + 0x88]
004A2054  8b 83 88 00 00 00        mov      eax, dword ptr [ebx + 0x88]
004A205A  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A205D  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2060  89 54 24 64              mov      dword ptr [esp + 0x64], edx
004A2064  99                       cdq      
004A2065  81 e2 ff 00 00 00        and      edx, 0xff
004A206B  03 c2                    add      eax, edx
004A206D  8b f8                    mov      edi, eax
004A206F  8b c1                    mov      eax, ecx
004A2071  99                       cdq      
004A2072  81 e2 ff 00 00 00        and      edx, 0xff
004A2078  03 c2                    add      eax, edx
004A207A  c1 f8 08                 sar      eax, 8
004A207D  66 89 44 24 36           mov      word ptr [esp + 0x36], ax
004A2082  8b 06                    mov      eax, dword ptr [esi]
004A2084  99                       cdq      
004A2085  81 e2 ff 00 00 00        and      edx, 0xff
004A208B  03 c2                    add      eax, edx
004A208D  8b c8                    mov      ecx, eax
004A208F  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A2092  99                       cdq      
004A2093  81 e2 ff 00 00 00        and      edx, 0xff
004A2099  03 c2                    add      eax, edx
004A209B  c1 ff 08                 sar      edi, 8
004A209E  c1 f9 08                 sar      ecx, 8
004A20A1  c1 f8 08                 sar      eax, 8
004A20A4  66 3b f9                 cmp      di, cx
004A20A7  75 07                    jne      0x4a20b0
004A20A9  66 39 44 24 36           cmp      word ptr [esp + 0x36], ax
004A20AE  74 34                    je       0x4a20e4
004A20B0  8b 03                    mov      eax, dword ptr [ebx]
004A20B2  6a 00                    push     0
004A20B4  8b cb                    mov      ecx, ebx
004A20B6  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004A20BC  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20BF  56                       push     esi
004A20C0  8b 11                    mov      edx, dword ptr [ecx]
004A20C2  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
004A20C8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20CB  6a 00                    push     0
004A20CD  8b 01                    mov      eax, dword ptr [ecx]
004A20CF  ff 90 b4 01 00 00        call     dword ptr [eax + 0x1b4]
004A20D5  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20D8  6a 01                    push     1
004A20DA  8b 11                    mov      edx, dword ptr [ecx]
004A20DC  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004A20E2  eb 2e                    jmp      0x4a2112
004A20E4  8a 43 74                 mov      al, byte ptr [ebx + 0x74]
004A20E7  c6 43 74 00              mov      byte ptr [ebx + 0x74], 0
004A20EB  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20EE  56                       push     esi
004A20EF  88 44 24 17              mov      byte ptr [esp + 0x17], al
004A20F3  8b 11                    mov      edx, dword ptr [ecx]
004A20F5  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
004A20FB  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A20FE  6a 00                    push     0
004A2100  8b 01                    mov      eax, dword ptr [ecx]
004A2102  ff 90 b4 01 00 00        call     dword ptr [eax + 0x1b4]
004A2108  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A210B  8a 54 24 13              mov      dl, byte ptr [esp + 0x13]
004A210F  88 51 74                 mov      byte ptr [ecx + 0x74], dl
004A2112  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2117  8b 0e                    mov      ecx, dword ptr [esi]
004A2119  3b c8                    cmp      ecx, eax
004A211B  75 1a                    jne      0x4a2137
004A211D  8b 4e 04                 mov      ecx, dword ptr [esi + 4]
004A2120  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2126  3b ca                    cmp      ecx, edx
004A2128  75 0d                    jne      0x4a2137
004A212A  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A212D  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2133  3b d1                    cmp      edx, ecx
004A2135  74 19                    je       0x4a2150
004A2137  8b ce                    mov      ecx, esi
004A2139  89 01                    mov      dword ptr [ecx], eax
004A213B  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2141  89 51 04                 mov      dword ptr [ecx + 4], edx
004A2144  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A2149  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A214D  89 41 08                 mov      dword ptr [ecx + 8], eax
004A2150  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2153  c7 45 58 ff ff ff ff     mov      dword ptr [ebp + 0x58], 0xffffffff
004A215A  c7 45 5c 00 00 00 00     mov      dword ptr [ebp + 0x5c], 0
004A2161  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
004A2166  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A216C  85 c9                    test     ecx, ecx
004A216E  0f 84 d9 00 00 00        je       0x4a224d
004A2174  8b 11                    mov      edx, dword ptr [ecx]
004A2176  50                       push     eax
004A2177  8d 44 24 60              lea      eax, [esp + 0x60]
004A217B  50                       push     eax
004A217C  ff 52 4c                 call     dword ptr [edx + 0x4c]
004A217F  8b c8                    mov      ecx, eax
004A2181  8b 01                    mov      eax, dword ptr [ecx]
004A2183  99                       cdq      
004A2184  81 e2 ff 00 00 00        and      edx, 0xff
004A218A  03 c2                    add      eax, edx
004A218C  8b f8                    mov      edi, eax
004A218E  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A2191  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2194  99                       cdq      
004A2195  81 e2 ff 00 00 00        and      edx, 0xff
004A219B  03 c2                    add      eax, edx
004A219D  8b 11                    mov      edx, dword ptr [ecx]
004A219F  8b d8                    mov      ebx, eax
004A21A1  8d 44 24 24              lea      eax, [esp + 0x24]
004A21A5  50                       push     eax
004A21A6  c1 ff 08                 sar      edi, 8
004A21A9  c1 fb 08                 sar      ebx, 8
004A21AC  ff 92 a0 01 00 00        call     dword ptr [edx + 0x1a0]
004A21B2  66 39 38                 cmp      word ptr [eax], di
004A21B5  0f 85 92 00 00 00        jne      0x4a224d
004A21BB  66 39 58 02              cmp      word ptr [eax + 2], bx
004A21BF  0f 85 88 00 00 00        jne      0x4a224d
004A21C5  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A21C8  8d 44 24 5c              lea      eax, [esp + 0x5c]
004A21CC  51                       push     ecx
004A21CD  50                       push     eax
004A21CE  8b 11                    mov      edx, dword ptr [ecx]
004A21D0  ff 52 4c                 call     dword ptr [edx + 0x4c]
004A21D3  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A21D6  8b 4d 3c                 mov      ecx, dword ptr [ebp + 0x3c]
004A21D9  2b c1                    sub      eax, ecx
004A21DB  8b 0d d0 29 85 00        mov      ecx, dword ptr [0x8529d0]
004A21E1  99                       cdq      
004A21E2  33 c2                    xor      eax, edx
004A21E4  2b c2                    sub      eax, edx
004A21E6  8d 14 09                 lea      edx, [ecx + ecx]
004A21E9  3b c2                    cmp      eax, edx
004A21EB  7d 60                    jge      0x4a224d
004A21ED  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A21F3  8d 45 34                 lea      eax, [ebp + 0x34]
004A21F6  c6 44 24 13 01           mov      byte ptr [esp + 0x13], 1
004A21FB  89 08                    mov      dword ptr [eax], ecx
004A21FD  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2203  89 50 04                 mov      dword ptr [eax + 4], edx
004A2206  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A220C  89 48 08                 mov      dword ptr [eax + 8], ecx
004A220F  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2214  39 06                    cmp      dword ptr [esi], eax
004A2216  75 1a                    jne      0x4a2232
004A2218  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A221B  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A2221  3b d1                    cmp      edx, ecx
004A2223  75 0d                    jne      0x4a2232
004A2225  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A2228  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A222E  3b ca                    cmp      ecx, edx
004A2230  74 17                    je       0x4a2249
004A2232  89 06                    mov      dword ptr [esi], eax
004A2234  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A223A  89 56 04                 mov      dword ptr [esi + 4], edx
004A223D  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A2242  89 46 08                 mov      dword ptr [esi + 8], eax
004A2245  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A2249  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A224D  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2250  6a 02                    push     2
004A2252  8b 11                    mov      edx, dword ptr [ecx]
004A2254  ff 92 74 01 00 00        call     dword ptr [edx + 0x174]
004A225A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A225D  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
004A2260  84 c0                    test     al, al
004A2262  74 69                    je       0x4a22cd
004A2264  8a 41 76                 mov      al, byte ptr [ecx + 0x76]
004A2267  84 c0                    test     al, al
004A2269  75 62                    jne      0x4a22cd
004A226B  8a 41 7a                 mov      al, byte ptr [ecx + 0x7a]
004A226E  84 c0                    test     al, al
004A2270  75 5b                    jne      0x4a22cd
004A2272  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
004A2276  84 c0                    test     al, al
004A2278  74 44                    je       0x4a22be
004A227A  e8 31 b7 02 00           call     0x4cd9b0
004A227F  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2282  c7 80 d0 04 00 00 ff ff ff ff mov      dword ptr [eax + 0x4d0], 0xffffffff
004A228C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A228F  8b 11                    mov      edx, dword ptr [ecx]
004A2291  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A2297  83 f8 02                 cmp      eax, 2
004A229A  75 22                    jne      0x4a22be
004A229C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A229F  6a 01                    push     1
004A22A1  6a 00                    push     0
004A22A3  8b 01                    mov      eax, dword ptr [ecx]
004A22A5  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A22AB  84 c0                    test     al, al
004A22AD  74 0f                    je       0x4a22be
004A22AF  5f                       pop      edi
004A22B0  5e                       pop      esi
004A22B1  5d                       pop      ebp
004A22B2  b0 01                    mov      al, 1
004A22B4  5b                       pop      ebx
004A22B5  81 c4 e4 00 00 00        add      esp, 0xe4
004A22BB  c2 04 00                 ret      4
004A22BE  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A22C1  8b 11                    mov      edx, dword ptr [ecx]
004A22C3  ff 92 90 04 00 00        call     dword ptr [edx + 0x490]
004A22C9  84 c0                    test     al, al
004A22CB  74 0f                    je       0x4a22dc
004A22CD  5f                       pop      edi
004A22CE  5e                       pop      esi
004A22CF  5d                       pop      ebp
004A22D0  b0 01                    mov      al, 1
004A22D2  5b                       pop      ebx
004A22D3  81 c4 e4 00 00 00        add      esp, 0xe4
004A22D9  c2 04 00                 ret      4
004A22DC  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A22DF  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A22E2  84 c9                    test     cl, cl
004A22E4  0f 85 b7 fc ff ff        jne      0x4a1fa1
004A22EA  5f                       pop      edi
004A22EB  5e                       pop      esi
004A22EC  5d                       pop      ebp
004A22ED  32 c0                    xor      al, al
004A22EF  5b                       pop      ebx
004A22F0  81 c4 e4 00 00 00        add      esp, 0xe4
004A22F6  c2 04 00                 ret      4
004A22F9  89 b9 d0 04 00 00        mov      dword ptr [ecx + 0x4d0], edi
004A22FF  5f                       pop      edi
004A2300  5e                       pop      esi
004A2301  5d                       pop      ebp
004A2302  32 c0                    xor      al, al
004A2304  5b                       pop      ebx
004A2305  81 c4 e4 00 00 00        add      esp, 0xe4
004A230B  c2 04 00                 ret      4
004A230E  0f be 00                 movsx    eax, byte ptr [eax]
004A2311  8b 55 5c                 mov      edx, dword ptr [ebp + 0x5c]
004A2314  c1 e0 04                 shl      eax, 4
004A2317  8d 0c 52                 lea      ecx, [edx + edx*2]
004A231A  8b 80 a0 00 7a 00        mov      eax, dword ptr [eax + 0x7a00a0]
004A2320  8b 34 88                 mov      esi, dword ptr [eax + ecx*4]
004A2323  8d 0c 88                 lea      ecx, [eax + ecx*4]
004A2326  3b f7                    cmp      esi, edi
004A2328  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A232B  89 b4 24 8c 00 00 00     mov      dword ptr [esp + 0x8c], esi
004A2332  89 84 24 90 00 00 00     mov      dword ptr [esp + 0x90], eax
004A2339  75 0c                    jne      0x4a2347
004A233B  3b c7                    cmp      eax, edi
004A233D  75 08                    jne      0x4a2347
004A233F  3b d7                    cmp      edx, edi
004A2341  0f 85 f3 02 00 00        jne      0x4a263a
004A2347  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A234A  05 88 00 00 00           add      eax, 0x88
004A234F  8b d0                    mov      edx, eax
004A2351  8b 32                    mov      esi, dword ptr [edx]
004A2353  89 b4 24 80 00 00 00     mov      dword ptr [esp + 0x80], esi
004A235A  8b 72 04                 mov      esi, dword ptr [edx + 4]
004A235D  89 b4 24 84 00 00 00     mov      dword ptr [esp + 0x84], esi
004A2364  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2367  89 94 24 88 00 00 00     mov      dword ptr [esp + 0x88], edx
004A236E  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
004A2371  89 4c 24 34              mov      dword ptr [esp + 0x34], ecx
004A2375  8b 30                    mov      esi, dword ptr [eax]
004A2377  8b 58 04                 mov      ebx, dword ptr [eax + 4]
004A237A  8b 50 08                 mov      edx, dword ptr [eax + 8]
004A237D  8d 44 24 34              lea      eax, [esp + 0x34]
004A2381  89 54 24 64              mov      dword ptr [esp + 0x64], edx
004A2385  8d 8c 24 8c 00 00 00     lea      ecx, [esp + 0x8c]
004A238C  50                       push     eax
004A238D  8d 94 24 b0 00 00 00     lea      edx, [esp + 0xb0]
004A2394  51                       push     ecx
004A2395  52                       push     edx
004A2396  8b cd                    mov      ecx, ebp
004A2398  e8 a3 23 00 00           call     0x4a4740
004A239D  8b 08                    mov      ecx, dword ptr [eax]
004A239F  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A23A2  8b 40 04                 mov      eax, dword ptr [eax + 4]
004A23A5  81 c2 88 00 00 00        add      edx, 0x88
004A23AB  2b c3                    sub      eax, ebx
004A23AD  2b ce                    sub      ecx, esi
004A23AF  8b da                    mov      ebx, edx
004A23B1  89 8c 24 c4 00 00 00     mov      dword ptr [esp + 0xc4], ecx
004A23B8  89 84 24 c8 00 00 00     mov      dword ptr [esp + 0xc8], eax
004A23BF  89 bc 24 cc 00 00 00     mov      dword ptr [esp + 0xcc], edi
004A23C6  8b 13                    mov      edx, dword ptr [ebx]
004A23C8  03 ca                    add      ecx, edx
004A23CA  8b 73 04                 mov      esi, dword ptr [ebx + 4]
004A23CD  03 c6                    add      eax, esi
004A23CF  8b 5b 08                 mov      ebx, dword ptr [ebx + 8]
004A23D2  89 44 24 78              mov      dword ptr [esp + 0x78], eax
004A23D6  8d 44 24 74              lea      eax, [esp + 0x74]
004A23DA  89 4c 24 74              mov      dword ptr [esp + 0x74], ecx
004A23DE  50                       push     eax
004A23DF  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A23E4  89 9c 24 80 00 00 00     mov      dword ptr [esp + 0x80], ebx
004A23EB  e8 10 5c 0a 00           call     0x548000
004A23F0  db 45 4c                 fild     dword ptr [ebp + 0x4c]
004A23F3  51                       push     ecx
004A23F4  8d 8c 24 c8 00 00 00     lea      ecx, [esp + 0xc8]
004A23FB  8d 94 24 bc 00 00 00     lea      edx, [esp + 0xbc]
004A2402  8b f0                    mov      esi, eax
004A2404  dc 0d c0 05 7a 00        fmul     qword ptr [0x7a05c0]
004A240A  89 bc 24 bc 00 00 00     mov      dword ptr [esp + 0xbc], edi
004A2411  89 bc 24 c0 00 00 00     mov      dword ptr [esp + 0xc0], edi
004A2418  89 bc 24 c4 00 00 00     mov      dword ptr [esp + 0xc4], edi
004A241F  d9 1c 24                 fstp     dword ptr [esp]
004A2422  51                       push     ecx
004A2423  8d 4c 24 64              lea      ecx, [esp + 0x64]
004A2427  e8 94 fc 27 00           call     0x7220c0
004A242C  8b bc 24 80 00 00 00     mov      edi, dword ptr [esp + 0x80]
004A2433  8b d0                    mov      edx, eax
004A2435  8b 02                    mov      eax, dword ptr [edx]
004A2437  89 84 24 c4 00 00 00     mov      dword ptr [esp + 0xc4], eax
004A243E  03 c7                    add      eax, edi
004A2440  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A2443  8b bc 24 84 00 00 00     mov      edi, dword ptr [esp + 0x84]
004A244A  89 8c 24 c8 00 00 00     mov      dword ptr [esp + 0xc8], ecx
004A2451  03 cf                    add      ecx, edi
004A2453  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2456  8b bc 24 88 00 00 00     mov      edi, dword ptr [esp + 0x88]
004A245D  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004A2461  89 94 24 cc 00 00 00     mov      dword ptr [esp + 0xcc], edx
004A2468  8d 84 24 80 00 00 00     lea      eax, [esp + 0x80]
004A246F  03 d7                    add      edx, edi
004A2471  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
004A2475  50                       push     eax
004A2476  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A247B  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A247F  e8 7c 5b 0a 00           call     0x548000
004A2484  8b f8                    mov      edi, eax
004A2486  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A248A  89 7c 24 6c              mov      dword ptr [esp + 0x6c], edi
004A248E  51                       push     ecx
004A248F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2494  e8 67 5b 0a 00           call     0x548000
004A2499  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A249C  81 c2 88 00 00 00        add      edx, 0x88
004A24A2  3b c6                    cmp      eax, esi
004A24A4  8b da                    mov      ebx, edx
004A24A6  8b 0b                    mov      ecx, dword ptr [ebx]
004A24A8  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004A24AC  8b 53 04                 mov      edx, dword ptr [ebx + 4]
004A24AF  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
004A24B3  8b 5b 08                 mov      ebx, dword ptr [ebx + 8]
004A24B6  89 5c 24 20              mov      dword ptr [esp + 0x20], ebx
004A24BA  74 20                    je       0x4a24dc
004A24BC  3b c7                    cmp      eax, edi
004A24BE  74 1c                    je       0x4a24dc
004A24C0  83 7d 4c 03              cmp      dword ptr [ebp + 0x4c], 3
004A24C4  7e 2e                    jle      0x4a24f4
004A24C6  8b 4c 24 74              mov      ecx, dword ptr [esp + 0x74]
004A24CA  8b 54 24 78              mov      edx, dword ptr [esp + 0x78]
004A24CE  8b 5c 24 7c              mov      ebx, dword ptr [esp + 0x7c]
004A24D2  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004A24D6  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
004A24DA  eb 14                    jmp      0x4a24f0
004A24DC  8b 4c 24 24              mov      ecx, dword ptr [esp + 0x24]
004A24E0  8b 54 24 28              mov      edx, dword ptr [esp + 0x28]
004A24E4  8b 5c 24 2c              mov      ebx, dword ptr [esp + 0x2c]
004A24E8  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004A24EC  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
004A24F0  89 5c 24 20              mov      dword ptr [esp + 0x20], ebx
004A24F4  8d 84 24 d0 00 00 00     lea      eax, [esp + 0xd0]
004A24FB  89 8c 24 d0 00 00 00     mov      dword ptr [esp + 0xd0], ecx
004A2502  50                       push     eax
004A2503  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2508  89 94 24 d8 00 00 00     mov      dword ptr [esp + 0xd8], edx
004A250F  89 9c 24 dc 00 00 00     mov      dword ptr [esp + 0xdc], ebx
004A2516  e8 e5 5a 0a 00           call     0x548000
004A251B  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A251E  89 44 24 54              mov      dword ptr [esp + 0x54], eax
004A2522  8d 91 88 00 00 00        lea      edx, [ecx + 0x88]
004A2528  8b 81 88 00 00 00        mov      eax, dword ptr [ecx + 0x88]
004A252E  8b 7a 04                 mov      edi, dword ptr [edx + 4]
004A2531  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2534  89 54 24 64              mov      dword ptr [esp + 0x64], edx
004A2538  99                       cdq      
004A2539  81 e2 ff 00 00 00        and      edx, 0xff
004A253F  03 c2                    add      eax, edx
004A2541  8b f0                    mov      esi, eax
004A2543  8b c7                    mov      eax, edi
004A2545  99                       cdq      
004A2546  81 e2 ff 00 00 00        and      edx, 0xff
004A254C  03 c2                    add      eax, edx
004A254E  8b f8                    mov      edi, eax
004A2550  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004A2554  99                       cdq      
004A2555  81 e2 ff 00 00 00        and      edx, 0xff
004A255B  03 c2                    add      eax, edx
004A255D  8b d8                    mov      ebx, eax
004A255F  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004A2563  99                       cdq      
004A2564  81 e2 ff 00 00 00        and      edx, 0xff
004A256A  03 c2                    add      eax, edx
004A256C  c1 fe 08                 sar      esi, 8
004A256F  c1 fb 08                 sar      ebx, 8
004A2572  c1 ff 08                 sar      edi, 8
004A2575  c1 f8 08                 sar      eax, 8
004A2578  66 3b de                 cmp      bx, si
004A257B  75 09                    jne      0x4a2586
004A257D  66 3b c7                 cmp      ax, di
004A2580  0f 84 81 00 00 00        je       0x4a2607
004A2586  8b 01                    mov      eax, dword ptr [ecx]
004A2588  6a 00                    push     0
004A258A  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004A2590  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2593  8d 44 24 18              lea      eax, [esp + 0x18]
004A2597  50                       push     eax
004A2598  8b 11                    mov      edx, dword ptr [ecx]
004A259A  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
004A25A0  8b 4c 24 6c              mov      ecx, dword ptr [esp + 0x6c]
004A25A4  8b 44 24 54              mov      eax, dword ptr [esp + 0x54]
004A25A8  0f be 91 1b 01 00 00     movsx    edx, byte ptr [ecx + 0x11b]
004A25AF  0f be b0 1b 01 00 00     movsx    esi, byte ptr [eax + 0x11b]
004A25B6  83 ea 04                 sub      edx, 4
004A25B9  3b f2                    cmp      esi, edx
004A25BB  ba 00 01 00 00           mov      edx, 0x100
004A25C0  75 0f                    jne      0x4a25d1
004A25C2  85 90 40 01 00 00        test     dword ptr [eax + 0x140], edx
004A25C8  74 0f                    je       0x4a25d9
004A25CA  8b 75 0c                 mov      esi, dword ptr [ebp + 0xc]
004A25CD  c6 46 79 01              mov      byte ptr [esi + 0x79], 1
004A25D1  85 90 40 01 00 00        test     dword ptr [eax + 0x140], edx
004A25D7  75 0f                    jne      0x4a25e8
004A25D9  85 91 40 01 00 00        test     dword ptr [ecx + 0x140], edx
004A25DF  74 07                    je       0x4a25e8
004A25E1  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A25E4  c6 40 79 00              mov      byte ptr [eax + 0x79], 0
004A25E8  8b 6d 0c                 mov      ebp, dword ptr [ebp + 0xc]
004A25EB  6a 01                    push     1
004A25ED  8b cd                    mov      ecx, ebp
004A25EF  8b 55 00                 mov      edx, dword ptr [ebp]
004A25F2  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004A25F8  5f                       pop      edi
004A25F9  5e                       pop      esi
004A25FA  5d                       pop      ebp
004A25FB  32 c0                    xor      al, al
004A25FD  5b                       pop      ebx
004A25FE  81 c4 e4 00 00 00        add      esp, 0xe4
004A2604  c2 04 00                 ret      4
004A2607  8a 59 74                 mov      bl, byte ptr [ecx + 0x74]
004A260A  c6 41 74 00              mov      byte ptr [ecx + 0x74], 0
004A260E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2611  8d 54 24 18              lea      edx, [esp + 0x18]
004A2615  52                       push     edx
004A2616  8b 01                    mov      eax, dword ptr [ecx]
004A2618  ff 90 9c 01 00 00        call     dword ptr [eax + 0x19c]
004A261E  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2621  5f                       pop      edi
004A2622  5e                       pop      esi
004A2623  5d                       pop      ebp
004A2624  88 58 74                 mov      byte ptr [eax + 0x74], bl
004A2627  32 c0                    xor      al, al
004A2629  5b                       pop      ebx
004A262A  81 c4 e4 00 00 00        add      esp, 0xe4
004A2630  c2 04 00                 ret      4
004A2633  c7 45 4c 00 00 00 00     mov      dword ptr [ebp + 0x4c], 0
004A263A  5f                       pop      edi
004A263B  5e                       pop      esi
004A263C  5d                       pop      ebp
004A263D  32 c0                    xor      al, al
004A263F  5b                       pop      ebx
004A2640  81 c4 e4 00 00 00        add      esp, 0xe4
004A2646  c2 04 00                 ret      4
