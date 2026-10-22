
sub_006E0E10 0x006E0E10 size=2272
006E0E10  83 ec 20                 sub      esp, 0x20
006E0E13  53                       push     ebx
006E0E14  55                       push     ebp
006E0E15  56                       push     esi
006E0E16  8b 74 24 30              mov      esi, dword ptr [esp + 0x30]
006E0E1A  33 db                    xor      ebx, ebx
006E0E1C  57                       push     edi
006E0E1D  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E0E20  89 5c 24 2c              mov      dword ptr [esp + 0x2c], ebx
006E0E24  8a 81 05 02 00 00        mov      al, byte ptr [ecx + 0x205]
006E0E2A  84 c0                    test     al, al
006E0E2C  74 23                    je       0x6e0e51
006E0E2E  39 5e 34                 cmp      dword ptr [esi + 0x34], ebx
006E0E31  75 1e                    jne      0x6e0e51
006E0E33  39 99 14 02 00 00        cmp      dword ptr [ecx + 0x214], ebx
006E0E39  75 16                    jne      0x6e0e51
006E0E3B  8b 4e fc                 mov      ecx, dword ptr [esi - 4]
006E0E3E  8d 46 fc                 lea      eax, [esi - 4]
006E0E41  50                       push     eax
006E0E42  ff 51 28                 call     dword ptr [ecx + 0x28]
006E0E45  32 c0                    xor      al, al
006E0E47  5f                       pop      edi
006E0E48  5e                       pop      esi
006E0E49  5d                       pop      ebp
006E0E4A  5b                       pop      ebx
006E0E4B  83 c4 20                 add      esp, 0x20
006E0E4E  c2 04 00                 ret      4
006E0E51  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
006E0E54  3b c3                    cmp      eax, ebx
006E0E56  75 19                    jne      0x6e0e71
006E0E58  8b 91 14 02 00 00        mov      edx, dword ptr [ecx + 0x214]
006E0E5E  3b d3                    cmp      edx, ebx
006E0E60  74 0f                    je       0x6e0e71
006E0E62  89 56 34                 mov      dword ptr [esi + 0x34], edx
006E0E65  32 c0                    xor      al, al
006E0E67  5f                       pop      edi
006E0E68  5e                       pop      esi
006E0E69  5d                       pop      ebp
006E0E6A  5b                       pop      ebx
006E0E6B  83 c4 20                 add      esp, 0x20
006E0E6E  c2 04 00                 ret      4
006E0E71  8a 91 10 02 00 00        mov      dl, byte ptr [ecx + 0x210]
006E0E77  84 d2                    test     dl, dl
006E0E79  0f 85 64 04 00 00        jne      0x6e12e3
006E0E7F  3b c3                    cmp      eax, ebx
006E0E81  0f 8f 93 04 00 00        jg       0x6e131a
006E0E87  8b 16                    mov      edx, dword ptr [esi]
006E0E89  56                       push     esi
006E0E8A  ff 52 10                 call     dword ptr [edx + 0x10]
006E0E8D  84 c0                    test     al, al
006E0E8F  0f 84 4a 08 00 00        je       0x6e16df
006E0E95  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E0E98  8d 6e 24                 lea      ebp, [esi + 0x24]
006E0E9B  8d 81 88 00 00 00        lea      eax, [ecx + 0x88]
006E0EA1  8b f8                    mov      edi, eax
006E0EA3  8b 07                    mov      eax, dword ptr [edi]
006E0EA5  3b 45 00                 cmp      eax, dword ptr [ebp]
006E0EA8  8b 57 04                 mov      edx, dword ptr [edi + 4]
006E0EAB  8b 7f 08                 mov      edi, dword ptr [edi + 8]
006E0EAE  75 0e                    jne      0x6e0ebe
006E0EB0  3b 55 04                 cmp      edx, dword ptr [ebp + 4]
006E0EB3  75 09                    jne      0x6e0ebe
006E0EB5  3b 7d 08                 cmp      edi, dword ptr [ebp + 8]
006E0EB8  0f 84 08 04 00 00        je       0x6e12c6
006E0EBE  8b 55 00                 mov      edx, dword ptr [ebp]
006E0EC1  a1 80 02 ac 00           mov      eax, dword ptr [0xac0280]
006E0EC6  3b d0                    cmp      edx, eax
006E0EC8  75 1d                    jne      0x6e0ee7
006E0ECA  8b 45 04                 mov      eax, dword ptr [ebp + 4]
006E0ECD  8b 15 84 02 ac 00        mov      edx, dword ptr [0xac0284]
006E0ED3  3b c2                    cmp      eax, edx
006E0ED5  75 10                    jne      0x6e0ee7
006E0ED7  8b 55 08                 mov      edx, dword ptr [ebp + 8]
006E0EDA  a1 88 02 ac 00           mov      eax, dword ptr [0xac0288]
006E0EDF  3b d0                    cmp      edx, eax
006E0EE1  0f 84 df 03 00 00        je       0x6e12c6
006E0EE7  e8 94 6d ff ff           call     0x6d7c80
006E0EEC  a1 f8 0c a4 00           mov      eax, dword ptr [0xa40cf8]
006E0EF1  8d 78 ff                 lea      edi, [eax - 1]
006E0EF4  3b fb                    cmp      edi, ebx
006E0EF6  7c 1e                    jl       0x6e0f16
006E0EF8  8b 0d ec 0c a4 00        mov      ecx, dword ptr [0xa40cec]
006E0EFE  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E0F01  8b 0c b9                 mov      ecx, dword ptr [ecx + edi*4]
006E0F04  8b 91 f4 00 00 00        mov      edx, dword ptr [ecx + 0xf4]
006E0F0A  3b d0                    cmp      edx, eax
006E0F0C  75 05                    jne      0x6e0f13
006E0F0E  e8 5d 05 d8 ff           call     0x461470
006E0F13  4f                       dec      edi
006E0F14  79 e2                    jns      0x6e0ef8
006E0F16  68 a8 01 00 00           push     0x1a8
006E0F1B  e8 f7 10 0a 00           call     0x782017
006E0F20  83 c4 04                 add      esp, 4
006E0F23  3b c3                    cmp      eax, ebx
006E0F25  74 3f                    je       0x6e0f66
006E0F27  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E0F2A  53                       push     ebx
006E0F2B  81 c1 88 00 00 00        add      ecx, 0x88
006E0F31  68 00 06 00 00           push     0x600
006E0F36  6a 01                    push     1
006E0F38  53                       push     ebx
006E0F39  8b 11                    mov      edx, dword ptr [ecx]
006E0F3B  89 54 24 24              mov      dword ptr [esp + 0x24], edx
006E0F3F  8b 51 04                 mov      edx, dword ptr [ecx + 4]
006E0F42  89 54 24 28              mov      dword ptr [esp + 0x28], edx
006E0F46  8d 54 24 24              lea      edx, [esp + 0x24]
006E0F4A  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E0F4D  52                       push     edx
006E0F4E  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
006E0F52  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E0F58  8b 91 a0 02 00 00        mov      edx, dword ptr [ecx + 0x2a0]
006E0F5E  8b c8                    mov      ecx, eax
006E0F60  52                       push     edx
006E0F61  e8 aa f1 d3 ff           call     0x420110
006E0F66  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E0F69  8d 54 24 20              lea      edx, [esp + 0x20]
006E0F6D  52                       push     edx
006E0F6E  8b 01                    mov      eax, dword ptr [ecx]
006E0F70  ff 50 48                 call     dword ptr [eax + 0x48]
006E0F73  8b 08                    mov      ecx, dword ptr [eax]
006E0F75  8b 55 00                 mov      edx, dword ptr [ebp]
006E0F78  8b 7d 08                 mov      edi, dword ptr [ebp + 8]
006E0F7B  2b ca                    sub      ecx, edx
006E0F7D  8b 50 04                 mov      edx, dword ptr [eax + 4]
006E0F80  8b 40 08                 mov      eax, dword ptr [eax + 8]
006E0F83  89 4c 24 14              mov      dword ptr [esp + 0x14], ecx
006E0F87  8b 4d 04                 mov      ecx, dword ptr [ebp + 4]
006E0F8A  2b d1                    sub      edx, ecx
006E0F8C  2b c7                    sub      eax, edi
006E0F8E  89 54 24 18              mov      dword ptr [esp + 0x18], edx
006E0F92  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
006E0F96  db 44 24 18              fild     dword ptr [esp + 0x18]
006E0F9A  db 44 24 1c              fild     dword ptr [esp + 0x1c]
006E0F9E  db 44 24 14              fild     dword ptr [esp + 0x14]
006E0FA2  83 ec 08                 sub      esp, 8
006E0FA5  d9 c0                    fld      st(0)
006E0FA7  d8 c9                    fmul     st(1)
006E0FA9  d9 c2                    fld      st(2)
006E0FAB  d8 cb                    fmul     st(3)
006E0FAD  de c1                    faddp    st(1)
006E0FAF  d9 c3                    fld      st(3)
006E0FB1  d8 cc                    fmul     st(4)
006E0FB3  de c1                    faddp    st(1)
006E0FB5  dd 1c 24                 fstp     qword ptr [esp]
006E0FB8  dd d8                    fstp     st(0)
006E0FBA  dd d8                    fstp     st(0)
006E0FBC  dd d8                    fstp     st(0)
006E0FBE  e8 4d 94 dd ff           call     0x4ba410
006E0FC3  83 c4 08                 add      esp, 8
006E0FC6  e8 45 e1 09 00           call     0x77f110
006E0FCB  8d 7e 38                 lea      edi, [esi + 0x38]
006E0FCE  8b d0                    mov      edx, eax
006E0FD0  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E0FD5  8b df                    mov      ebx, edi
006E0FD7  33 c9                    xor      ecx, ecx
006E0FD9  89 54 24 34              mov      dword ptr [esp + 0x34], edx
006E0FDD  89 03                    mov      dword ptr [ebx], eax
006E0FDF  8b 44 24 24              mov      eax, dword ptr [esp + 0x24]
006E0FE3  89 43 04                 mov      dword ptr [ebx + 4], eax
006E0FE6  89 4b 08                 mov      dword ptr [ebx + 8], ecx
006E0FE9  8b 1d 48 98 83 00        mov      ebx, dword ptr [0x839848]
006E0FEF  8a 83 b8 0a 00 00        mov      al, byte ptr [ebx + 0xab8]
006E0FF5  84 c0                    test     al, al
006E0FF7  74 23                    je       0x6e101c
006E0FF9  8b c2                    mov      eax, edx
006E0FFB  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
006E1001  99                       cdq      
006E1002  f7 bb b4 0a 00 00        idiv     dword ptr [ebx + 0xab4]
006E1008  8b d7                    mov      edx, edi
006E100A  89 0a                    mov      dword ptr [edx], ecx
006E100C  8b 4c 24 24              mov      ecx, dword ptr [esp + 0x24]
006E1010  89 4a 04                 mov      dword ptr [edx + 4], ecx
006E1013  89 42 08                 mov      dword ptr [edx + 8], eax
006E1016  8b 1d 48 98 83 00        mov      ebx, dword ptr [0x839848]
006E101C  8b 17                    mov      edx, dword ptr [edi]
006E101E  8b 47 08                 mov      eax, dword ptr [edi + 8]
006E1021  83 fa ff                 cmp      edx, -1
006E1024  74 12                    je       0x6e1038
006E1026  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
006E102C  2b ca                    sub      ecx, edx
006E102E  3b c8                    cmp      ecx, eax
006E1030  7d 04                    jge      0x6e1036
006E1032  2b c1                    sub      eax, ecx
006E1034  eb 02                    jmp      0x6e1038
006E1036  33 c0                    xor      eax, eax
006E1038  8b 9b bc 0a 00 00        mov      ebx, dword ptr [ebx + 0xabc]
006E103E  3b c3                    cmp      eax, ebx
006E1040  7e 04                    jle      0x6e1046
006E1042  8b c7                    mov      eax, edi
006E1044  eb 12                    jmp      0x6e1058
006E1046  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
006E104C  89 5c 24 1c              mov      dword ptr [esp + 0x1c], ebx
006E1050  89 54 24 14              mov      dword ptr [esp + 0x14], edx
006E1054  8d 44 24 14              lea      eax, [esp + 0x14]
006E1058  8b 10                    mov      edx, dword ptr [eax]
006E105A  8b cf                    mov      ecx, edi
006E105C  89 11                    mov      dword ptr [ecx], edx
006E105E  8b 50 04                 mov      edx, dword ptr [eax + 4]
006E1061  89 51 04                 mov      dword ptr [ecx + 4], edx
006E1064  8b 40 08                 mov      eax, dword ptr [eax + 8]
006E1067  8b 54 24 34              mov      edx, dword ptr [esp + 0x34]
006E106B  89 41 08                 mov      dword ptr [ecx + 8], eax
006E106E  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E1074  3b 91 c0 0a 00 00        cmp      edx, dword ptr [ecx + 0xac0]
006E107A  7d 19                    jge      0x6e1095
006E107C  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E1081  8b 89 bc 0a 00 00        mov      ecx, dword ptr [ecx + 0xabc]
006E1087  8b d7                    mov      edx, edi
006E1089  89 02                    mov      dword ptr [edx], eax
006E108B  8b 44 24 24              mov      eax, dword ptr [esp + 0x24]
006E108F  89 42 04                 mov      dword ptr [edx + 4], eax
006E1092  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E1095  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1098  c6 81 05 02 00 00 01     mov      byte ptr [ecx + 0x205], 1
006E109F  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E10A2  8b 11                    mov      edx, dword ptr [ecx]
006E10A4  ff 52 2c                 call     dword ptr [edx + 0x2c]
006E10A7  83 f8 01                 cmp      eax, 1
006E10AA  75 2f                    jne      0x6e10db
006E10AC  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E10AF  8b 88 ac 05 00 00        mov      ecx, dword ptr [eax + 0x5ac]
006E10B5  8a 81 a6 0b 00 00        mov      al, byte ptr [ecx + 0xba6]
006E10BB  84 c0                    test     al, al
006E10BD  74 1c                    je       0x6e10db
006E10BF  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E10C4  8b 54 24 24              mov      edx, dword ptr [esp + 0x24]
006E10C8  33 c9                    xor      ecx, ecx
006E10CA  89 07                    mov      dword ptr [edi], eax
006E10CC  89 57 04                 mov      dword ptr [edi + 4], edx
006E10CF  89 4f 08                 mov      dword ptr [edi + 8], ecx
006E10D2  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E10D5  88 88 05 02 00 00        mov      byte ptr [eax + 0x205], cl
006E10DB  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E10DE  8b 81 80 05 00 00        mov      eax, dword ptr [ecx + 0x580]
006E10E4  85 c0                    test     eax, eax
006E10E6  74 0b                    je       0x6e10f3
006E10E8  8b 88 88 05 00 00        mov      ecx, dword ptr [eax + 0x588]
006E10EE  e8 4d 63 f2 ff           call     0x607440
006E10F3  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E10F6  6a 00                    push     0
006E10F8  8b 11                    mov      edx, dword ptr [ecx]
006E10FA  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
006E1100  8b 7e 08                 mov      edi, dword ptr [esi + 8]
006E1103  8b cf                    mov      ecx, edi
006E1105  8b 07                    mov      eax, dword ptr [edi]
006E1107  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
006E110D  8b 80 fc 04 00 00        mov      eax, dword ptr [eax + 0x4fc]
006E1113  83 f8 ff                 cmp      eax, -1
006E1116  75 11                    jne      0x6e1129
006E1118  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E111E  8b 81 14 02 00 00        mov      eax, dword ptr [ecx + 0x214]
006E1124  83 f8 ff                 cmp      eax, -1
006E1127  74 27                    je       0x6e1150
006E1129  81 c7 88 00 00 00        add      edi, 0x88
006E112F  6a 00                    push     0
006E1131  8b 17                    mov      edx, dword ptr [edi]
006E1133  89 54 24 18              mov      dword ptr [esp + 0x18], edx
006E1137  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
006E113A  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
006E113E  8b c8                    mov      ecx, eax
006E1140  8b 57 08                 mov      edx, dword ptr [edi + 8]
006E1143  89 54 24 20              mov      dword ptr [esp + 0x20], edx
006E1147  8d 54 24 18              lea      edx, [esp + 0x18]
006E114B  e8 10 2d 03 00           call     0x713e60
006E1150  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1153  55                       push     ebp
006E1154  8b 01                    mov      eax, dword ptr [ecx]
006E1156  ff 90 9c 01 00 00        call     dword ptr [eax + 0x19c]
006E115C  8b 45 00                 mov      eax, dword ptr [ebp]
006E115F  99                       cdq      
006E1160  81 e2 ff 00 00 00        and      edx, 0xff
006E1166  03 c2                    add      eax, edx
006E1168  c1 f8 08                 sar      eax, 8
006E116B  66 89 44 24 34           mov      word ptr [esp + 0x34], ax
006E1170  8b 45 04                 mov      eax, dword ptr [ebp + 4]
006E1173  99                       cdq      
006E1174  81 e2 ff 00 00 00        and      edx, 0xff
006E117A  03 c2                    add      eax, edx
006E117C  8d 54 24 10              lea      edx, [esp + 0x10]
006E1180  c1 f8 08                 sar      eax, 8
006E1183  66 89 44 24 36           mov      word ptr [esp + 0x36], ax
006E1188  8b 4c 24 34              mov      ecx, dword ptr [esp + 0x34]
006E118C  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
006E1190  52                       push     edx
006E1191  b9 e0 24 83 00           mov      ecx, 0x8324e0
006E1196  e8 d5 6e e6 ff           call     0x548070
006E119B  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E119E  8b d8                    mov      ebx, eax
006E11A0  55                       push     ebp
006E11A1  8b 01                    mov      eax, dword ptr [ecx]
006E11A3  ff 90 9c 01 00 00        call     dword ptr [eax + 0x19c]
006E11A9  8b 83 40 01 00 00        mov      eax, dword ptr [ebx + 0x140]
006E11AF  f6 c4 01                 test     ah, 1
006E11B2  74 09                    je       0x6e11bd
006E11B4  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E11B7  c6 41 79 01              mov      byte ptr [ecx + 0x79], 1
006E11BB  eb 07                    jmp      0x6e11c4
006E11BD  8b 56 08                 mov      edx, dword ptr [esi + 8]
006E11C0  c6 42 79 00              mov      byte ptr [edx + 0x79], 0
006E11C4  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E11C7  6a 00                    push     0
006E11C9  8b 01                    mov      eax, dword ptr [ecx]
006E11CB  ff 90 b4 01 00 00        call     dword ptr [eax + 0x1b4]
006E11D1  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E11D4  6a 01                    push     1
006E11D6  8b 11                    mov      edx, dword ptr [ecx]
006E11D8  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
006E11DE  8b 7e 08                 mov      edi, dword ptr [esi + 8]
006E11E1  8b cf                    mov      ecx, edi
006E11E3  8b 07                    mov      eax, dword ptr [edi]
006E11E5  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
006E11EB  8b 80 f8 04 00 00        mov      eax, dword ptr [eax + 0x4f8]
006E11F1  83 f8 ff                 cmp      eax, -1
006E11F4  75 11                    jne      0x6e1207
006E11F6  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E11FC  8b 81 10 02 00 00        mov      eax, dword ptr [ecx + 0x210]
006E1202  83 f8 ff                 cmp      eax, -1
006E1205  74 27                    je       0x6e122e
006E1207  81 c7 88 00 00 00        add      edi, 0x88
006E120D  6a 00                    push     0
006E120F  8b 17                    mov      edx, dword ptr [edi]
006E1211  89 54 24 18              mov      dword ptr [esp + 0x18], edx
006E1215  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
006E1218  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
006E121C  8b c8                    mov      ecx, eax
006E121E  8b 57 08                 mov      edx, dword ptr [edi + 8]
006E1221  89 54 24 20              mov      dword ptr [esp + 0x20], edx
006E1225  8d 54 24 18              lea      edx, [esp + 0x18]
006E1229  e8 32 2c 03 00           call     0x713e60
006E122E  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1231  6a 02                    push     2
006E1233  8b 01                    mov      eax, dword ptr [ecx]
006E1235  ff 90 74 01 00 00        call     dword ptr [eax + 0x174]
006E123B  8b 0e                    mov      ecx, dword ptr [esi]
006E123D  56                       push     esi
006E123E  ff 51 48                 call     dword ptr [ecx + 0x48]
006E1241  8b 56 08                 mov      edx, dword ptr [esi + 8]
006E1244  8b cb                    mov      ecx, ebx
006E1246  52                       push     edx
006E1247  e8 74 5a d9 ff           call     0x476cc0
006E124C  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E124F  6a 01                    push     1
006E1251  6a 00                    push     0
006E1253  8b 01                    mov      eax, dword ptr [ecx]
006E1255  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
006E125B  68 a8 01 00 00           push     0x1a8
006E1260  e8 b2 0d 0a 00           call     0x782017
006E1265  83 c4 04                 add      esp, 4
006E1268  85 c0                    test     eax, eax
006E126A  74 41                    je       0x6e12ad
006E126C  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E126F  6a 00                    push     0
006E1271  81 c1 88 00 00 00        add      ecx, 0x88
006E1277  68 00 06 00 00           push     0x600
006E127C  6a 01                    push     1
006E127E  6a 00                    push     0
006E1280  8b 11                    mov      edx, dword ptr [ecx]
006E1282  89 54 24 24              mov      dword ptr [esp + 0x24], edx
006E1286  8b 51 04                 mov      edx, dword ptr [ecx + 4]
006E1289  89 54 24 28              mov      dword ptr [esp + 0x28], edx
006E128D  8d 54 24 24              lea      edx, [esp + 0x24]
006E1291  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E1294  52                       push     edx
006E1295  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
006E1299  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E129F  8b 91 a0 02 00 00        mov      edx, dword ptr [ecx + 0x2a0]
006E12A5  8b c8                    mov      ecx, eax
006E12A7  52                       push     edx
006E12A8  e8 63 ee d3 ff           call     0x420110
006E12AD  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E12B0  c7 80 14 02 00 00 00 00 00 00 mov      dword ptr [eax + 0x214], 0
006E12BA  32 c0                    xor      al, al
006E12BC  5f                       pop      edi
006E12BD  5e                       pop      esi
006E12BE  5d                       pop      ebp
006E12BF  5b                       pop      ebx
006E12C0  83 c4 20                 add      esp, 0x20
006E12C3  c2 04 00                 ret      4
006E12C6  8b 11                    mov      edx, dword ptr [ecx]
006E12C8  6a 01                    push     1
006E12CA  53                       push     ebx
006E12CB  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
006E12D1  8b 06                    mov      eax, dword ptr [esi]
006E12D3  56                       push     esi
006E12D4  ff 50 48                 call     dword ptr [eax + 0x48]
006E12D7  32 c0                    xor      al, al
006E12D9  5f                       pop      edi
006E12DA  5e                       pop      esi
006E12DB  5d                       pop      ebp
006E12DC  5b                       pop      ebx
006E12DD  83 c4 20                 add      esp, 0x20
006E12E0  c2 04 00                 ret      4
006E12E3  3b c3                    cmp      eax, ebx
006E12E5  75 33                    jne      0x6e131a
006E12E7  c6 81 04 02 00 00 01     mov      byte ptr [ecx + 0x204], 1
006E12EE  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E12F3  8d 56 38                 lea      edx, [esi + 0x38]
006E12F6  b9 3c 00 00 00           mov      ecx, 0x3c
006E12FB  89 02                    mov      dword ptr [edx], eax
006E12FD  8b 44 24 24              mov      eax, dword ptr [esp + 0x24]
006E1301  89 42 04                 mov      dword ptr [edx + 4], eax
006E1304  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E1307  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
006E130A  40                       inc      eax
006E130B  89 46 34                 mov      dword ptr [esi + 0x34], eax
006E130E  32 c0                    xor      al, al
006E1310  5f                       pop      edi
006E1311  5e                       pop      esi
006E1312  5d                       pop      ebp
006E1313  5b                       pop      ebx
006E1314  83 c4 20                 add      esp, 0x20
006E1317  c2 04 00                 ret      4
006E131A  83 f8 01                 cmp      eax, 1
006E131D  75 16                    jne      0x6e1335
006E131F  8b 4e fc                 mov      ecx, dword ptr [esi - 4]
006E1322  8d 46 fc                 lea      eax, [esi - 4]
006E1325  50                       push     eax
006E1326  ff 51 28                 call     dword ptr [ecx + 0x28]
006E1329  32 c0                    xor      al, al
006E132B  5f                       pop      edi
006E132C  5e                       pop      esi
006E132D  5d                       pop      ebp
006E132E  5b                       pop      ebx
006E132F  83 c4 20                 add      esp, 0x20
006E1332  c2 04 00                 ret      4
006E1335  83 f8 02                 cmp      eax, 2
006E1338  0f 85 18 01 00 00        jne      0x6e1456
006E133E  68 a8 01 00 00           push     0x1a8
006E1343  e8 cf 0c 0a 00           call     0x782017
006E1348  83 c4 04                 add      esp, 4
006E134B  3b c3                    cmp      eax, ebx
006E134D  74 3f                    je       0x6e138e
006E134F  8b 56 08                 mov      edx, dword ptr [esi + 8]
006E1352  53                       push     ebx
006E1353  81 c2 88 00 00 00        add      edx, 0x88
006E1359  68 00 06 00 00           push     0x600
006E135E  6a 01                    push     1
006E1360  53                       push     ebx
006E1361  8b 0a                    mov      ecx, dword ptr [edx]
006E1363  89 4c 24 24              mov      dword ptr [esp + 0x24], ecx
006E1367  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
006E136A  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
006E136E  8d 4c 24 24              lea      ecx, [esp + 0x24]
006E1372  8b 52 08                 mov      edx, dword ptr [edx + 8]
006E1375  51                       push     ecx
006E1376  89 54 24 30              mov      dword ptr [esp + 0x30], edx
006E137A  8b 15 48 98 83 00        mov      edx, dword ptr [0x839848]
006E1380  8b 8a a0 02 00 00        mov      ecx, dword ptr [edx + 0x2a0]
006E1386  51                       push     ecx
006E1387  8b c8                    mov      ecx, eax
006E1389  e8 82 ed d3 ff           call     0x420110
006E138E  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1391  53                       push     ebx
006E1392  8b 11                    mov      edx, dword ptr [ecx]
006E1394  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
006E139A  8b 7e 08                 mov      edi, dword ptr [esi + 8]
006E139D  8b cf                    mov      ecx, edi
006E139F  8b 07                    mov      eax, dword ptr [edi]
006E13A1  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
006E13A7  8b 80 fc 04 00 00        mov      eax, dword ptr [eax + 0x4fc]
006E13AD  83 f8 ff                 cmp      eax, -1
006E13B0  75 11                    jne      0x6e13c3
006E13B2  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E13B8  8b 81 14 02 00 00        mov      eax, dword ptr [ecx + 0x214]
006E13BE  83 f8 ff                 cmp      eax, -1
006E13C1  74 26                    je       0x6e13e9
006E13C3  81 c7 88 00 00 00        add      edi, 0x88
006E13C9  53                       push     ebx
006E13CA  8b 17                    mov      edx, dword ptr [edi]
006E13CC  89 54 24 18              mov      dword ptr [esp + 0x18], edx
006E13D0  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
006E13D3  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
006E13D7  8b c8                    mov      ecx, eax
006E13D9  8b 57 08                 mov      edx, dword ptr [edi + 8]
006E13DC  89 54 24 20              mov      dword ptr [esp + 0x20], edx
006E13E0  8d 54 24 18              lea      edx, [esp + 0x18]
006E13E4  e8 77 2a 03 00           call     0x713e60
006E13E9  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E13EC  53                       push     ebx
006E13ED  83 ec 0c                 sub      esp, 0xc
006E13F0  c6 80 05 02 00 00 01     mov      byte ptr [eax + 0x205], 1
006E13F7  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E13FA  c6 81 10 02 00 00 00     mov      byte ptr [ecx + 0x210], 0
006E1401  8b 56 08                 mov      edx, dword ptr [esi + 8]
006E1404  c6 82 04 02 00 00 00     mov      byte ptr [edx + 0x204], 0
006E140B  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E140E  8b d4                    mov      edx, esp
006E1410  c6 40 79 00              mov      byte ptr [eax + 0x79], 0
006E1414  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1417  81 c1 1c 02 00 00        add      ecx, 0x21c
006E141D  8b 01                    mov      eax, dword ptr [ecx]
006E141F  89 02                    mov      dword ptr [edx], eax
006E1421  8b 41 04                 mov      eax, dword ptr [ecx + 4]
006E1424  89 42 04                 mov      dword ptr [edx + 4], eax
006E1427  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E142A  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E142D  8d 4e fc                 lea      ecx, [esi - 4]
006E1430  e8 cb ea ff ff           call     0x6dff00
006E1435  8b 7e 34                 mov      edi, dword ptr [esi + 0x34]
006E1438  47                       inc      edi
006E1439  84 c0                    test     al, al
006E143B  89 7e 34                 mov      dword ptr [esi + 0x34], edi
006E143E  8b cf                    mov      ecx, edi
006E1440  0f 84 99 02 00 00        je       0x6e16df
006E1446  41                       inc      ecx
006E1447  32 c0                    xor      al, al
006E1449  89 4e 34                 mov      dword ptr [esi + 0x34], ecx
006E144C  5f                       pop      edi
006E144D  5e                       pop      esi
006E144E  5d                       pop      ebp
006E144F  5b                       pop      ebx
006E1450  83 c4 20                 add      esp, 0x20
006E1453  c2 04 00                 ret      4
006E1456  83 f8 03                 cmp      eax, 3
006E1459  75 4b                    jne      0x6e14a6
006E145B  53                       push     ebx
006E145C  81 c1 1c 02 00 00        add      ecx, 0x21c
006E1462  83 ec 0c                 sub      esp, 0xc
006E1465  8b 01                    mov      eax, dword ptr [ecx]
006E1467  8b d4                    mov      edx, esp
006E1469  89 02                    mov      dword ptr [edx], eax
006E146B  8b 41 04                 mov      eax, dword ptr [ecx + 4]
006E146E  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E1471  89 42 04                 mov      dword ptr [edx + 4], eax
006E1474  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E1477  8d 4e fc                 lea      ecx, [esi - 4]
006E147A  e8 81 ea ff ff           call     0x6dff00
006E147F  84 c0                    test     al, al
006E1481  74 03                    je       0x6e1486
006E1483  ff 46 34                 inc      dword ptr [esi + 0x34]
006E1486  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
006E148B  8b 56 08                 mov      edx, dword ptr [esi + 8]
006E148E  8b 88 ac 0a 00 00        mov      ecx, dword ptr [eax + 0xaac]
006E1494  32 c0                    xor      al, al
006E1496  89 8a 18 02 00 00        mov      dword ptr [edx + 0x218], ecx
006E149C  5f                       pop      edi
006E149D  5e                       pop      esi
006E149E  5d                       pop      ebp
006E149F  5b                       pop      ebx
006E14A0  83 c4 20                 add      esp, 0x20
006E14A3  c2 04 00                 ret      4
006E14A6  83 f8 04                 cmp      eax, 4
006E14A9  75 60                    jne      0x6e150b
006E14AB  6a 01                    push     1
006E14AD  81 c1 1c 02 00 00        add      ecx, 0x21c
006E14B3  83 ec 0c                 sub      esp, 0xc
006E14B6  8b 01                    mov      eax, dword ptr [ecx]
006E14B8  8b d4                    mov      edx, esp
006E14BA  89 02                    mov      dword ptr [edx], eax
006E14BC  8b 41 04                 mov      eax, dword ptr [ecx + 4]
006E14BF  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E14C2  89 42 04                 mov      dword ptr [edx + 4], eax
006E14C5  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E14C8  8d 4e fc                 lea      ecx, [esi - 4]
006E14CB  e8 30 ea ff ff           call     0x6dff00
006E14D0  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E14D3  8d 46 24                 lea      eax, [esi + 0x24]
006E14D6  50                       push     eax
006E14D7  8b 11                    mov      edx, dword ptr [ecx]
006E14D9  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
006E14DF  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E14E2  53                       push     ebx
006E14E3  8b 11                    mov      edx, dword ptr [ecx]
006E14E5  ff 92 b4 01 00 00        call     dword ptr [edx + 0x1b4]
006E14EB  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E14EE  6a 01                    push     1
006E14F0  8b 01                    mov      eax, dword ptr [ecx]
006E14F2  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
006E14F8  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
006E14FB  40                       inc      eax
006E14FC  89 46 34                 mov      dword ptr [esi + 0x34], eax
006E14FF  32 c0                    xor      al, al
006E1501  5f                       pop      edi
006E1502  5e                       pop      esi
006E1503  5d                       pop      ebp
006E1504  5b                       pop      ebx
006E1505  83 c4 20                 add      esp, 0x20
006E1508  c2 04 00                 ret      4
006E150B  83 f8 05                 cmp      eax, 5
006E150E  0f 85 7d 01 00 00        jne      0x6e1691
006E1514  8b 11                    mov      edx, dword ptr [ecx]
006E1516  8d 6e 24                 lea      ebp, [esi + 0x24]
006E1519  55                       push     ebp
006E151A  ff 92 9c 01 00 00        call     dword ptr [edx + 0x19c]
006E1520  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1523  53                       push     ebx
006E1524  8b 01                    mov      eax, dword ptr [ecx]
006E1526  ff 90 b4 01 00 00        call     dword ptr [eax + 0x1b4]
006E152C  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E152F  6a 01                    push     1
006E1531  8b 11                    mov      edx, dword ptr [ecx]
006E1533  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
006E1539  8b 7e 08                 mov      edi, dword ptr [esi + 8]
006E153C  8b cf                    mov      ecx, edi
006E153E  8b 07                    mov      eax, dword ptr [edi]
006E1540  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
006E1546  8b 80 f8 04 00 00        mov      eax, dword ptr [eax + 0x4f8]
006E154C  83 f8 ff                 cmp      eax, -1
006E154F  75 11                    jne      0x6e1562
006E1551  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E1557  8b 81 10 02 00 00        mov      eax, dword ptr [ecx + 0x210]
006E155D  83 f8 ff                 cmp      eax, -1
006E1560  74 26                    je       0x6e1588
006E1562  81 c7 88 00 00 00        add      edi, 0x88
006E1568  53                       push     ebx
006E1569  8b 17                    mov      edx, dword ptr [edi]
006E156B  89 54 24 18              mov      dword ptr [esp + 0x18], edx
006E156F  8b 4f 04                 mov      ecx, dword ptr [edi + 4]
006E1572  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
006E1576  8b c8                    mov      ecx, eax
006E1578  8b 57 08                 mov      edx, dword ptr [edi + 8]
006E157B  89 54 24 20              mov      dword ptr [esp + 0x20], edx
006E157F  8d 54 24 18              lea      edx, [esp + 0x18]
006E1583  e8 d8 28 03 00           call     0x713e60
006E1588  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E158B  8d 54 24 34              lea      edx, [esp + 0x34]
006E158F  6a 01                    push     1
006E1591  52                       push     edx
006E1592  8b 01                    mov      eax, dword ptr [ecx]
006E1594  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
006E159A  50                       push     eax
006E159B  b9 e0 24 83 00           mov      ecx, 0x8324e0
006E15A0  e8 bb 90 e7 ff           call     0x55a660
006E15A5  84 c0                    test     al, al
006E15A7  75 0a                    jne      0x6e15b3
006E15A9  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E15AC  c6 80 2d 03 00 00 00     mov      byte ptr [eax + 0x32d], 0
006E15B3  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E15B6  39 99 14 02 00 00        cmp      dword ptr [ecx + 0x214], ebx
006E15BC  75 1e                    jne      0x6e15dc
006E15BE  8b 45 00                 mov      eax, dword ptr [ebp]
006E15C1  8b 4d 04                 mov      ecx, dword ptr [ebp + 4]
006E15C4  83 ec 0c                 sub      esp, 0xc
006E15C7  8b d4                    mov      edx, esp
006E15C9  89 02                    mov      dword ptr [edx], eax
006E15CB  8b 45 08                 mov      eax, dword ptr [ebp + 8]
006E15CE  89 4a 04                 mov      dword ptr [edx + 4], ecx
006E15D1  8d 4e fc                 lea      ecx, [esi - 4]
006E15D4  89 42 08                 mov      dword ptr [edx + 8], eax
006E15D7  e8 54 ee ff ff           call     0x6e0430
006E15DC  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E15DF  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
006E15E2  84 c0                    test     al, al
006E15E4  0f 84 f5 00 00 00        je       0x6e16df
006E15EA  8b 11                    mov      edx, dword ptr [ecx]
006E15EC  6a 02                    push     2
006E15EE  ff 92 74 01 00 00        call     dword ptr [edx + 0x174]
006E15F4  8b 06                    mov      eax, dword ptr [esi]
006E15F6  56                       push     esi
006E15F7  ff 50 48                 call     dword ptr [eax + 0x48]
006E15FA  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E15FD  53                       push     ebx
006E15FE  e8 4d 58 ff ff           call     0x6d6e50
006E1603  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1606  6a 01                    push     1
006E1608  53                       push     ebx
006E1609  8b 11                    mov      edx, dword ptr [ecx]
006E160B  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
006E1611  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1614  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E1619  8d 56 38                 lea      edx, [esi + 0x38]
006E161C  68 a8 01 00 00           push     0x1a8
006E1621  8b 89 18 02 00 00        mov      ecx, dword ptr [ecx + 0x218]
006E1627  89 02                    mov      dword ptr [edx], eax
006E1629  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
006E162D  89 42 04                 mov      dword ptr [edx + 4], eax
006E1630  89 4a 08                 mov      dword ptr [edx + 8], ecx
006E1633  e8 df 09 0a 00           call     0x782017
006E1638  83 c4 04                 add      esp, 4
006E163B  3b c3                    cmp      eax, ebx
006E163D  74 3f                    je       0x6e167e
006E163F  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E1642  53                       push     ebx
006E1643  81 c1 88 00 00 00        add      ecx, 0x88
006E1649  68 00 06 00 00           push     0x600
006E164E  6a 01                    push     1
006E1650  53                       push     ebx
006E1651  8b 11                    mov      edx, dword ptr [ecx]
006E1653  89 54 24 24              mov      dword ptr [esp + 0x24], edx
006E1657  8b 51 04                 mov      edx, dword ptr [ecx + 4]
006E165A  89 54 24 28              mov      dword ptr [esp + 0x28], edx
006E165E  8d 54 24 24              lea      edx, [esp + 0x24]
006E1662  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
006E1665  52                       push     edx
006E1666  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
006E166A  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
006E1670  8b 91 a0 02 00 00        mov      edx, dword ptr [ecx + 0x2a0]
006E1676  8b c8                    mov      ecx, eax
006E1678  52                       push     edx
006E1679  e8 92 ea d3 ff           call     0x420110
006E167E  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
006E1681  40                       inc      eax
006E1682  89 46 34                 mov      dword ptr [esi + 0x34], eax
006E1685  32 c0                    xor      al, al
006E1687  5f                       pop      edi
006E1688  5e                       pop      esi
006E1689  5d                       pop      ebp
006E168A  5b                       pop      ebx
006E168B  83 c4 20                 add      esp, 0x20
006E168E  c2 04 00                 ret      4
006E1691  83 f8 06                 cmp      eax, 6
006E1694  75 16                    jne      0x6e16ac
006E1696  8b 4e fc                 mov      ecx, dword ptr [esi - 4]
006E1699  8d 46 fc                 lea      eax, [esi - 4]
006E169C  50                       push     eax
006E169D  ff 51 28                 call     dword ptr [ecx + 0x28]
006E16A0  32 c0                    xor      al, al
006E16A2  5f                       pop      edi
006E16A3  5e                       pop      esi
006E16A4  5d                       pop      ebp
006E16A5  5b                       pop      ebx
006E16A6  83 c4 20                 add      esp, 0x20
006E16A9  c2 04 00                 ret      4
006E16AC  83 f8 07                 cmp      eax, 7
006E16AF  75 2e                    jne      0x6e16df
006E16B1  c6 81 05 02 00 00 00     mov      byte ptr [ecx + 0x205], 0
006E16B8  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E16BB  53                       push     ebx
006E16BC  e8 8f 57 ff ff           call     0x6d6e50
006E16C1  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
006E16C4  6a 01                    push     1
006E16C6  53                       push     ebx
006E16C7  8b 11                    mov      edx, dword ptr [ecx]
006E16C9  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
006E16CF  c6 46 30 00              mov      byte ptr [esi + 0x30], 0
006E16D3  8b 46 08                 mov      eax, dword ptr [esi + 8]
006E16D6  89 98 14 02 00 00        mov      dword ptr [eax + 0x214], ebx
006E16DC  89 5e 34                 mov      dword ptr [esi + 0x34], ebx
006E16DF  5f                       pop      edi
006E16E0  5e                       pop      esi
006E16E1  5d                       pop      ebp
006E16E2  32 c0                    xor      al, al
006E16E4  5b                       pop      ebx
006E16E5  83 c4 20                 add      esp, 0x20
006E16E8  c2 04 00                 ret      4
006E16EB  90                       nop      
006E16EC  90                       nop      
006E16ED  90                       nop      
006E16EE  90                       nop      
006E16EF  90                       nop      
