
sub_004A3C9B 0x004A3C9B size=2698
004A3C9B  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3C9E  8b 11                    mov      edx, dword ptr [ecx]
004A3CA0  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A3CA6  8b 90 a4 05 00 00        mov      edx, dword ptr [eax + 0x5a4]
004A3CAC  8d 0c f6                 lea      ecx, [esi + esi*8]
004A3CAF  03 d1                    add      edx, ecx
004A3CB1  d9 04 95 a0 0e 85 00     fld      dword ptr [edx*4 + 0x850ea0]
004A3CB8  dd 54 24 18              fst      qword ptr [esp + 0x18]
004A3CBC  dc 1d 08 a7 79 00        fcomp    qword ptr [0x79a708]
004A3CC2  df e0                    fnstsw   ax
004A3CC4  f6 c4 41                 test     ah, 0x41
004A3CC7  75 10                    jne      0x4a3cd9
004A3CC9  c7 44 24 18 00 00 00 00  mov      dword ptr [esp + 0x18], 0
004A3CD1  c7 44 24 1c 00 00 f0 3f  mov      dword ptr [esp + 0x1c], 0x3ff00000
004A3CD9  8d 44 24 50              lea      eax, [esp + 0x50]
004A3CDD  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A3CE1  50                       push     eax
004A3CE2  51                       push     ecx
004A3CE3  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3CE8  e8 83 43 0a 00           call     0x548070
004A3CED  8b c8                    mov      ecx, eax
004A3CEF  e8 6c 20 fd ff           call     0x475d60
004A3CF4  50                       push     eax
004A3CF5  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3CFA  e8 81 65 0b 00           call     0x55a280
004A3CFF  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3D02  8b f0                    mov      esi, eax
004A3D04  81 c2 88 00 00 00        add      edx, 0x88
004A3D0A  8b 02                    mov      eax, dword ptr [edx]
004A3D0C  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A3D10  8d 44 24 44              lea      eax, [esp + 0x44]
004A3D14  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A3D17  50                       push     eax
004A3D18  89 4c 24 4c              mov      dword ptr [esp + 0x4c], ecx
004A3D1C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3D21  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A3D24  89 54 24 50              mov      dword ptr [esp + 0x50], edx
004A3D28  e8 53 65 0b 00           call     0x55a280
004A3D2D  8b f8                    mov      edi, eax
004A3D2F  3b f7                    cmp      esi, edi
004A3D31  7e 45                    jle      0x4a3d78
004A3D33  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3D36  8b 11                    mov      edx, dword ptr [ecx]
004A3D38  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A3D3B  83 f8 01                 cmp      eax, 1
004A3D3E  75 36                    jne      0x4a3d76
004A3D40  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3D43  8b 01                    mov      eax, dword ptr [ecx]
004A3D45  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A3D4B  8b 88 a4 05 00 00        mov      ecx, dword ptr [eax + 0x5a4]
004A3D51  dd 44 24 18              fld      qword ptr [esp + 0x18]
004A3D55  83 f9 01                 cmp      ecx, 1
004A3D58  75 0e                    jne      0x4a3d68
004A3D5A  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A3D60  dc 89 90 06 00 00        fmul     qword ptr [ecx + 0x690]
004A3D66  eb 52                    jmp      0x4a3dba
004A3D68  8b 15 48 98 83 00        mov      edx, dword ptr [0x839848]
004A3D6E  dc 8a a0 06 00 00        fmul     qword ptr [edx + 0x6a0]
004A3D74  eb 44                    jmp      0x4a3dba
004A3D76  3b f7                    cmp      esi, edi
004A3D78  7d 44                    jge      0x4a3dbe
004A3D7A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3D7D  8b 01                    mov      eax, dword ptr [ecx]
004A3D7F  ff 50 2c                 call     dword ptr [eax + 0x2c]
004A3D82  83 f8 01                 cmp      eax, 1
004A3D85  75 37                    jne      0x4a3dbe
004A3D87  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3D8A  8b 11                    mov      edx, dword ptr [ecx]
004A3D8C  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A3D92  8b 88 a4 05 00 00        mov      ecx, dword ptr [eax + 0x5a4]
004A3D98  dd 44 24 18              fld      qword ptr [esp + 0x18]
004A3D9C  83 f9 01                 cmp      ecx, 1
004A3D9F  75 0d                    jne      0x4a3dae
004A3DA1  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A3DA6  dc 88 98 06 00 00        fmul     qword ptr [eax + 0x698]
004A3DAC  eb 0c                    jmp      0x4a3dba
004A3DAE  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A3DB4  dc 89 a8 06 00 00        fmul     qword ptr [ecx + 0x6a8]
004A3DBA  dd 5c 24 18              fstp     qword ptr [esp + 0x18]
004A3DBE  dd 44 24 18              fld      qword ptr [esp + 0x18]
004A3DC2  dc 1d 10 b6 79 00        fcomp    qword ptr [0x79b610]
004A3DC8  df e0                    fnstsw   ax
004A3DCA  f6 c4 40                 test     ah, 0x40
004A3DCD  74 10                    je       0x4a3ddf
004A3DCF  c7 44 24 18 00 00 00 00  mov      dword ptr [esp + 0x18], 0
004A3DD7  c7 44 24 1c 00 00 e0 3f  mov      dword ptr [esp + 0x1c], 0x3fe00000
004A3DDF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3DE2  e8 59 07 13 00           call     0x5d4540
004A3DE7  8b 15 48 98 83 00        mov      edx, dword ptr [0x839848]
004A3DED  dc 9a 68 13 00 00        fcomp    qword ptr [edx + 0x1368]
004A3DF3  dd 44 24 18              fld      qword ptr [esp + 0x18]
004A3DF7  df e0                    fnstsw   ax
004A3DF9  f6 c4 41                 test     ah, 0x41
004A3DFC  74 0a                    je       0x4a3e08
004A3DFE  dc 0d d8 05 7a 00        fmul     qword ptr [0x7a05d8]
004A3E04  dd 54 24 18              fst      qword ptr [esp + 0x18]
004A3E08  83 7d 58 40              cmp      dword ptr [ebp + 0x58], 0x40
004A3E0C  7d 05                    jge      0x4a3e13
004A3E0E  dd 5d 50                 fstp     qword ptr [ebp + 0x50]
004A3E11  eb 22                    jmp      0x4a3e35
004A3E13  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3E16  dc 99 68 04 00 00        fcomp    qword ptr [ecx + 0x468]
004A3E1C  df e0                    fnstsw   ax
004A3E1E  f6 c4 40                 test     ah, 0x40
004A3E21  75 12                    jne      0x4a3e35
004A3E23  8b 54 24 1c              mov      edx, dword ptr [esp + 0x1c]
004A3E27  8b 01                    mov      eax, dword ptr [ecx]
004A3E29  52                       push     edx
004A3E2A  8b 54 24 1c              mov      edx, dword ptr [esp + 0x1c]
004A3E2E  52                       push     edx
004A3E2F  ff 90 c8 04 00 00        call     dword ptr [eax + 0x4c8]
004A3E35  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004A3E39  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3E3C  99                       cdq      
004A3E3D  81 e2 ff 00 00 00        and      edx, 0xff
004A3E43  6a 01                    push     1
004A3E45  03 c2                    add      eax, edx
004A3E47  c1 f8 08                 sar      eax, 8
004A3E4A  66 89 44 24 1c           mov      word ptr [esp + 0x1c], ax
004A3E4F  8b 44 24 40              mov      eax, dword ptr [esp + 0x40]
004A3E53  99                       cdq      
004A3E54  81 e2 ff 00 00 00        and      edx, 0xff
004A3E5A  03 c2                    add      eax, edx
004A3E5C  c1 f8 08                 sar      eax, 8
004A3E5F  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
004A3E64  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004A3E68  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
004A3E6C  8b 11                    mov      edx, dword ptr [ecx]
004A3E6E  8d 44 24 1c              lea      eax, [esp + 0x1c]
004A3E72  50                       push     eax
004A3E73  ff 92 b8 04 00 00        call     dword ptr [edx + 0x4b8]
004A3E79  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3E7C  8b b1 d4 04 00 00        mov      esi, dword ptr [ecx + 0x4d4]
004A3E82  83 fe ff                 cmp      esi, -1
004A3E85  0f 85 00 01 00 00        jne      0x4a3f8b
004A3E8B  8b 11                    mov      edx, dword ptr [ecx]
004A3E8D  8d 44 24 50              lea      eax, [esp + 0x50]
004A3E91  50                       push     eax
004A3E92  ff 52 48                 call     dword ptr [edx + 0x48]
004A3E95  8b 08                    mov      ecx, dword ptr [eax]
004A3E97  8b 55 34                 mov      edx, dword ptr [ebp + 0x34]
004A3E9A  8b 7d 38                 mov      edi, dword ptr [ebp + 0x38]
004A3E9D  8d 75 34                 lea      esi, [ebp + 0x34]
004A3EA0  2b ca                    sub      ecx, edx
004A3EA2  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A3EA5  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A3EA8  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004A3EAC  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A3EAF  2b d7                    sub      edx, edi
004A3EB1  db 44 24 18              fild     dword ptr [esp + 0x18]
004A3EB5  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
004A3EB9  2b c1                    sub      eax, ecx
004A3EBB  db 44 24 1c              fild     dword ptr [esp + 0x1c]
004A3EBF  89 44 24 20              mov      dword ptr [esp + 0x20], eax
004A3EC3  83 ec 08                 sub      esp, 8
004A3EC6  db 44 24 28              fild     dword ptr [esp + 0x28]
004A3ECA  d9 c0                    fld      st(0)
004A3ECC  d8 c9                    fmul     st(1)
004A3ECE  d9 c2                    fld      st(2)
004A3ED0  d8 cb                    fmul     st(3)
004A3ED2  de c1                    faddp    st(1)
004A3ED4  d9 c3                    fld      st(3)
004A3ED6  d8 cc                    fmul     st(4)
004A3ED8  de c1                    faddp    st(1)
004A3EDA  dd 1c 24                 fstp     qword ptr [esp]
004A3EDD  dd d8                    fstp     st(0)
004A3EDF  dd d8                    fstp     st(0)
004A3EE1  dd d8                    fstp     st(0)
004A3EE3  e8 28 65 01 00           call     0x4ba410
004A3EE8  83 c4 08                 add      esp, 8
004A3EEB  e8 20 b2 2d 00           call     0x77f110
004A3EF0  3d 00 02 00 00           cmp      eax, 0x200
004A3EF5  0f 8e a4 00 00 00        jle      0x4a3f9f
004A3EFB  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3EFE  8b 11                    mov      edx, dword ptr [ecx]
004A3F00  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A3F06  8a 90 a0 0a 00 00        mov      dl, byte ptr [eax + 0xaa0]
004A3F0C  8b 06                    mov      eax, dword ptr [esi]
004A3F0E  33 c9                    xor      ecx, ecx
004A3F10  6a 00                    push     0
004A3F12  84 d2                    test     dl, dl
004A3F14  99                       cdq      
004A3F15  0f 95 c1                 setne    cl
004A3F18  81 e2 ff 00 00 00        and      edx, 0xff
004A3F1E  51                       push     ecx
004A3F1F  03 c2                    add      eax, edx
004A3F21  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3F24  c1 f8 08                 sar      eax, 8
004A3F27  66 89 44 24 20           mov      word ptr [esp + 0x20], ax
004A3F2C  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A3F2F  99                       cdq      
004A3F30  81 e2 ff 00 00 00        and      edx, 0xff
004A3F36  03 c2                    add      eax, edx
004A3F38  c1 f8 08                 sar      eax, 8
004A3F3B  66 89 44 24 22           mov      word ptr [esp + 0x22], ax
004A3F40  8b 44 24 20              mov      eax, dword ptr [esp + 0x20]
004A3F44  50                       push     eax
004A3F45  e8 b6 f0 01 00           call     0x4c3000
004A3F4A  84 c0                    test     al, al
004A3F4C  75 34                    jne      0x4a3f82
004A3F4E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3F51  85 c9                    test     ecx, ecx
004A3F53  75 11                    jne      0x4a3f66
004A3F55  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
004A3F59  5f                       pop      edi
004A3F5A  5e                       pop      esi
004A3F5B  5d                       pop      ebp
004A3F5C  c6 01 01                 mov      byte ptr [ecx], 1
004A3F5F  5b                       pop      ebx
004A3F60  83 c4 4c                 add      esp, 0x4c
004A3F63  c2 0c 00                 ret      0xc
004A3F66  8b 11                    mov      edx, dword ptr [ecx]
004A3F68  56                       push     esi
004A3F69  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004A3F6F  84 c0                    test     al, al
004A3F71  75 0f                    jne      0x4a3f82
004A3F73  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3F76  6a 01                    push     1
004A3F78  6a 00                    push     0
004A3F7A  8b 01                    mov      eax, dword ptr [ecx]
004A3F7C  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A3F82  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3F85  8b b1 d4 04 00 00        mov      esi, dword ptr [ecx + 0x4d4]
004A3F8B  83 fe 08                 cmp      esi, 8
004A3F8E  75 02                    jne      0x4a3f92
004A3F90  8b f3                    mov      esi, ebx
004A3F92  83 fe ff                 cmp      esi, -1
004A3F95  74 08                    je       0x4a3f9f
004A3F97  8a 44 24 68              mov      al, byte ptr [esp + 0x68]
004A3F9B  84 c0                    test     al, al
004A3F9D  74 02                    je       0x4a3fa1
004A3F9F  8b f3                    mov      esi, ebx
004A3FA1  83 fe ff                 cmp      esi, -1
004A3FA4  74 29                    je       0x4a3fcf
004A3FA6  8b 4c 24 2c              mov      ecx, dword ptr [esp + 0x2c]
004A3FAA  56                       push     esi
004A3FAB  e8 10 2b fd ff           call     0x476ac0
004A3FB0  85 c0                    test     eax, eax
004A3FB2  74 1b                    je       0x4a3fcf
004A3FB4  8b 40 44                 mov      eax, dword ptr [eax + 0x44]
004A3FB7  83 f8 ff                 cmp      eax, -1
004A3FBA  74 13                    je       0x4a3fcf
004A3FBC  8b 15 ec 5d a3 00        mov      edx, dword ptr [0xa35dec]
004A3FC2  8b 04 82                 mov      eax, dword ptr [edx + eax*4]
004A3FC5  8a 88 fd 01 00 00        mov      cl, byte ptr [eax + 0x1fd]
004A3FCB  84 c9                    test     cl, cl
004A3FCD  75 08                    jne      0x4a3fd7
004A3FCF  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
004A3FD3  84 c0                    test     al, al
004A3FD5  74 08                    je       0x4a3fdf
004A3FD7  8b f3                    mov      esi, ebx
004A3FD9  c6 45 64 01              mov      byte ptr [ebp + 0x64], 1
004A3FDD  eb 04                    jmp      0x4a3fe3
004A3FDF  c6 45 64 00              mov      byte ptr [ebp + 0x64], 0
004A3FE3  8d 04 de                 lea      eax, [esi + ebx*8]
004A3FE6  c6 45 60 00              mov      byte ptr [ebp + 0x60], 0
004A3FEA  89 45 58                 mov      dword ptr [ebp + 0x58], eax
004A3FED  8d 0c 40                 lea      ecx, [eax + eax*2]
004A3FF0  8a 04 8d 80 01 7a 00     mov      al, byte ptr [ecx*4 + 0x7a0180]
004A3FF7  84 c0                    test     al, al
004A3FF9  75 06                    jne      0x4a4001
004A3FFB  8d 14 db                 lea      edx, [ebx + ebx*8]
004A3FFE  89 55 58                 mov      dword ptr [ebp + 0x58], edx
004A4001  8b 45 58                 mov      eax, dword ptr [ebp + 0x58]
004A4004  8d 04 40                 lea      eax, [eax + eax*2]
004A4007  f6 04 85 88 01 7a 00 08  test     byte ptr [eax*4 + 0x7a0188], 8
004A400F  0f 84 a2 05 00 00        je       0x4a45b7
004A4015  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4018  8d 54 24 14              lea      edx, [esp + 0x14]
004A401C  51                       push     ecx
004A401D  52                       push     edx
004A401E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A4023  e8 48 40 0a 00           call     0x548070
004A4028  8b c8                    mov      ecx, eax
004A402A  e8 91 2c fd ff           call     0x476cc0
004A402F  84 c0                    test     al, al
004A4031  75 26                    jne      0x4a4059
004A4033  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A4036  8a 48 76                 mov      cl, byte ptr [eax + 0x76]
004A4039  84 c9                    test     cl, cl
004A403B  75 1c                    jne      0x4a4059
004A403D  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A4040  be 07 00 00 00           mov      esi, 7
004A4045  84 c9                    test     cl, cl
004A4047  0f 85 f0 00 00 00        jne      0x4a413d
004A404D  5f                       pop      edi
004A404E  5e                       pop      esi
004A404F  5d                       pop      ebp
004A4050  32 c0                    xor      al, al
004A4052  5b                       pop      ebx
004A4053  83 c4 4c                 add      esp, 0x4c
004A4056  c2 0c 00                 ret      0xc
004A4059  8b 7d 0c                 mov      edi, dword ptr [ebp + 0xc]
004A405C  8a 47 7d                 mov      al, byte ptr [edi + 0x7d]
004A405F  84 c0                    test     al, al
004A4061  0f 84 dd f9 ff ff        je       0x4a3a44
004A4067  8b c6                    mov      eax, esi
004A4069  8b 54 24 3c              mov      edx, dword ptr [esp + 0x3c]
004A406D  83 e0 07                 and      eax, 7
004A4070  8b 5c 24 38              mov      ebx, dword ptr [esp + 0x38]
004A4074  6a 01                    push     1
004A4076  6a 00                    push     0
004A4078  8d 0c c5 c0 1a 85 00     lea      ecx, [eax*8 + 0x851ac0]
004A407F  8b 04 c5 c0 1a 85 00     mov      eax, dword ptr [eax*8 + 0x851ac0]
004A4086  8b 49 04                 mov      ecx, dword ptr [ecx + 4]
004A4089  03 ca                    add      ecx, edx
004A408B  8b 54 24 48              mov      edx, dword ptr [esp + 0x48]
004A408F  03 c3                    add      eax, ebx
004A4091  89 54 24 48              mov      dword ptr [esp + 0x48], edx
004A4095  89 44 24 40              mov      dword ptr [esp + 0x40], eax
004A4099  89 4c 24 44              mov      dword ptr [esp + 0x44], ecx
004A409D  99                       cdq      
004A409E  81 e2 ff 00 00 00        and      edx, 0xff
004A40A4  03 c2                    add      eax, edx
004A40A6  c1 f8 08                 sar      eax, 8
004A40A9  66 89 44 24 70           mov      word ptr [esp + 0x70], ax
004A40AE  8b c1                    mov      eax, ecx
004A40B0  99                       cdq      
004A40B1  81 e2 ff 00 00 00        and      edx, 0xff
004A40B7  03 c2                    add      eax, edx
004A40B9  8b 54 24 30              mov      edx, dword ptr [esp + 0x30]
004A40BD  c1 f8 08                 sar      eax, 8
004A40C0  66 89 44 24 72           mov      word ptr [esp + 0x72], ax
004A40C5  8b 4c 24 70              mov      ecx, dword ptr [esp + 0x70]
004A40C9  52                       push     edx
004A40CA  8d 44 24 20              lea      eax, [esp + 0x20]
004A40CE  89 4c 24 20              mov      dword ptr [esp + 0x20], ecx
004A40D2  8b 3f                    mov      edi, dword ptr [edi]
004A40D4  56                       push     esi
004A40D5  50                       push     eax
004A40D6  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A40DB  e8 90 3f 0a 00           call     0x548070
004A40E0  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A40E3  50                       push     eax
004A40E4  ff 97 94 01 00 00        call     dword ptr [edi + 0x194]
004A40EA  8b f0                    mov      esi, eax
004A40EC  83 fe 07                 cmp      esi, 7
004A40EF  7d 15                    jge      0x4a4106
004A40F1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A40F4  8b 11                    mov      edx, dword ptr [ecx]
004A40F6  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A40FC  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A4102  84 c9                    test     cl, cl
004A4104  75 35                    jne      0x4a413b
004A4106  83 fe 04                 cmp      esi, 4
004A4109  74 05                    je       0x4a4110
004A410B  83 fe 05                 cmp      esi, 5
004A410E  75 2d                    jne      0x4a413d
004A4110  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4113  8b 01                    mov      eax, dword ptr [ecx]
004A4115  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A411B  8a 88 f3 0a 00 00        mov      cl, byte ptr [eax + 0xaf3]
004A4121  84 c9                    test     cl, cl
004A4123  74 18                    je       0x4a413d
004A4125  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A4129  51                       push     ecx
004A412A  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A412F  e8 3c 3f 0a 00           call     0x548070
004A4134  8b 48 44                 mov      ecx, dword ptr [eax + 0x44]
004A4137  85 c9                    test     ecx, ecx
004A4139  75 02                    jne      0x4a413d
004A413B  33 f6                    xor      esi, esi
004A413D  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4140  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
004A4143  84 c0                    test     al, al
004A4145  0f 84 f9 f8 ff ff        je       0x4a3a44
004A414B  85 f6                    test     esi, esi
004A414D  0f 84 39 04 00 00        je       0x4a458c
004A4153  8b 5c 24 64              mov      ebx, dword ptr [esp + 0x64]
004A4157  83 fe 03                 cmp      esi, 3
004A415A  75 6b                    jne      0x4a41c7
004A415C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004A4160  8d 44 24 68              lea      eax, [esp + 0x68]
004A4164  50                       push     eax
004A4165  51                       push     ecx
004A4166  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A416B  89 54 24 70              mov      dword ptr [esp + 0x70], edx
004A416F  e8 5c 6b 0b 00           call     0x55acd0
004A4174  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A4177  83 cf ff                 or       edi, 0xffffffff
004A417A  83 fe 05                 cmp      esi, 5
004A417D  89 b8 d0 04 00 00        mov      dword ptr [eax + 0x4d0], edi
004A4183  89 7d 58                 mov      dword ptr [ebp + 0x58], edi
004A4186  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A418C  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A4192  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A4197  89 4c 24 38              mov      dword ptr [esp + 0x38], ecx
004A419B  89 54 24 3c              mov      dword ptr [esp + 0x3c], edx
004A419F  89 44 24 40              mov      dword ptr [esp + 0x40], eax
004A41A3  74 09                    je       0x4a41ae
004A41A5  83 fe 04                 cmp      esi, 4
004A41A8  0f 85 22 04 00 00        jne      0x4a45d0
004A41AE  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
004A41B2  6a 01                    push     1
004A41B4  53                       push     ebx
004A41B5  51                       push     ecx
004A41B6  8b cd                    mov      ecx, ebp
004A41B8  e8 b3 e4 ff ff           call     0x4a2670
004A41BD  5f                       pop      edi
004A41BE  5e                       pop      esi
004A41BF  5d                       pop      ebp
004A41C0  5b                       pop      ebx
004A41C1  83 c4 4c                 add      esp, 0x4c
004A41C4  c2 0c 00                 ret      0xc
004A41C7  83 fe 02                 cmp      esi, 2
004A41CA  75 1d                    jne      0x4a41e9
004A41CC  8b 4c 24 64              mov      ecx, dword ptr [esp + 0x64]
004A41D0  8b 54 24 60              mov      edx, dword ptr [esp + 0x60]
004A41D4  6a 01                    push     1
004A41D6  51                       push     ecx
004A41D7  52                       push     edx
004A41D8  8b cd                    mov      ecx, ebp
004A41DA  e8 91 e4 ff ff           call     0x4a2670
004A41DF  5f                       pop      edi
004A41E0  5e                       pop      esi
004A41E1  5d                       pop      ebp
004A41E2  5b                       pop      ebx
004A41E3  83 c4 4c                 add      esp, 0x4c
004A41E6  c2 0c 00                 ret      0xc
004A41E9  83 fe 06                 cmp      esi, 6
004A41EC  0f 85 10 02 00 00        jne      0x4a4402
004A41F2  8b 01                    mov      eax, dword ptr [ecx]
004A41F4  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A41FA  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A4200  84 c9                    test     cl, cl
004A4202  0f 85 6c ff ff ff        jne      0x4a4174
004A4208  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A420B  84 db                    test     bl, bl
004A420D  74 25                    je       0x4a4234
004A420F  c7 81 d0 04 00 00 ff ff ff ff mov      dword ptr [ecx + 0x4d0], 0xffffffff
004A4219  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A421C  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A4221  33 c9                    xor      ecx, ecx
004A4223  81 c2 30 05 00 00        add      edx, 0x530
004A4229  89 02                    mov      dword ptr [edx], eax
004A422B  8b 44 24 54              mov      eax, dword ptr [esp + 0x54]
004A422F  e9 ce 02 00 00           jmp      0x4a4502
004A4234  8b 11                    mov      edx, dword ptr [ecx]
004A4236  8d 44 24 50              lea      eax, [esp + 0x50]
004A423A  50                       push     eax
004A423B  ff 52 48                 call     dword ptr [edx + 0x48]
004A423E  8b 08                    mov      ecx, dword ptr [eax]
004A4240  8b 55 34                 mov      edx, dword ptr [ebp + 0x34]
004A4243  8b 7d 38                 mov      edi, dword ptr [ebp + 0x38]
004A4246  2b ca                    sub      ecx, edx
004A4248  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A424B  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A424E  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A4252  8b 4d 3c                 mov      ecx, dword ptr [ebp + 0x3c]
004A4255  2b d7                    sub      edx, edi
004A4257  2b c1                    sub      eax, ecx
004A4259  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A425D  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A4261  db 44 24 30              fild     dword ptr [esp + 0x30]
004A4265  db 44 24 34              fild     dword ptr [esp + 0x34]
004A4269  db 44 24 2c              fild     dword ptr [esp + 0x2c]
004A426D  83 ec 08                 sub      esp, 8
004A4270  d9 c0                    fld      st(0)
004A4272  d8 c9                    fmul     st(1)
004A4274  d9 c2                    fld      st(2)
004A4276  d8 cb                    fmul     st(3)
004A4278  de c1                    faddp    st(1)
004A427A  d9 c3                    fld      st(3)
004A427C  d8 cc                    fmul     st(4)
004A427E  de c1                    faddp    st(1)
004A4280  dd 1c 24                 fstp     qword ptr [esp]
004A4283  dd d8                    fstp     st(0)
004A4285  dd d8                    fstp     st(0)
004A4287  dd d8                    fstp     st(0)
004A4289  e8 82 61 01 00           call     0x4ba410
004A428E  83 c4 08                 add      esp, 8
004A4291  e8 7a ae 2d 00           call     0x77f110
004A4296  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A429C  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A42A2  0f 8d e9 00 00 00        jge      0x4a4391
004A42A8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A42AB  81 c1 88 00 00 00        add      ecx, 0x88
004A42B1  8b d1                    mov      edx, ecx
004A42B3  8b 02                    mov      eax, dword ptr [edx]
004A42B5  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A42B9  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A42BC  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A42C0  8b 45 3c                 mov      eax, dword ptr [ebp + 0x3c]
004A42C3  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A42C6  2b c2                    sub      eax, edx
004A42C8  99                       cdq      
004A42C9  33 c2                    xor      eax, edx
004A42CB  2b c2                    sub      eax, edx
004A42CD  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A42D3  03 d2                    add      edx, edx
004A42D5  3b c2                    cmp      eax, edx
004A42D7  0f 8d b4 00 00 00        jge      0x4a4391
004A42DD  8b 01                    mov      eax, dword ptr [ecx]
004A42DF  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A42E3  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A42E6  89 54 24 48              mov      dword ptr [esp + 0x48], edx
004A42EA  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A42ED  8d 4c 24 44              lea      ecx, [esp + 0x44]
004A42F1  89 44 24 4c              mov      dword ptr [esp + 0x4c], eax
004A42F5  51                       push     ecx
004A42F6  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A42FB  e8 00 3d 0a 00           call     0x548000
004A4300  83 b8 ec 00 00 00 0a     cmp      dword ptr [eax + 0xec], 0xa
004A4307  0f 84 84 00 00 00        je       0x4a4391
004A430D  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A4312  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A4315  3b c8                    cmp      ecx, eax
004A4317  75 1a                    jne      0x4a4333
004A4319  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A431C  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A4322  3b d1                    cmp      edx, ecx
004A4324  75 0d                    jne      0x4a4333
004A4326  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A4329  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A432F  3b ca                    cmp      ecx, edx
004A4331  74 18                    je       0x4a434b
004A4333  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A4336  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A433C  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A433F  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A4344  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A4347  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A434B  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A434E  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A4354  85 c0                    test     eax, eax
004A4356  75 11                    jne      0x4a4369
004A4358  8b 11                    mov      edx, dword ptr [ecx]
004A435A  6a 01                    push     1
004A435C  6a 00                    push     0
004A435E  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A4364  e9 0b fe ff ff           jmp      0x4a4174
004A4369  e8 42 96 02 00           call     0x4cd9b0
004A436E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4371  6a 01                    push     1
004A4373  6a 00                    push     0
004A4375  8b 01                    mov      eax, dword ptr [ecx]
004A4377  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A437D  84 c0                    test     al, al
004A437F  0f 84 ef fd ff ff        je       0x4a4174
004A4385  5f                       pop      edi
004A4386  5e                       pop      esi
004A4387  5d                       pop      ebp
004A4388  b0 01                    mov      al, 1
004A438A  5b                       pop      ebx
004A438B  83 c4 4c                 add      esp, 0x4c
004A438E  c2 0c 00                 ret      0xc
004A4391  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A4395  51                       push     ecx
004A4396  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A439B  e8 d0 3c 0a 00           call     0x548070
004A43A0  8b c8                    mov      ecx, eax
004A43A2  8b 81 40 01 00 00        mov      eax, dword ptr [ecx + 0x140]
004A43A8  f6 c4 01                 test     ah, 1
004A43AB  74 38                    je       0x4a43e5
004A43AD  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A43B0  c6 44 24 68 01           mov      byte ptr [esp + 0x68], 1
004A43B5  81 c2 88 00 00 00        add      edx, 0x88
004A43BB  0f be b9 1b 01 00 00     movsx    edi, byte ptr [ecx + 0x11b]
004A43C2  8b 02                    mov      eax, dword ptr [edx]
004A43C4  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A43C8  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A43CB  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A43CF  8b 42 08                 mov      eax, dword ptr [edx + 8]
004A43D2  99                       cdq      
004A43D3  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A43D9  2b c7                    sub      eax, edi
004A43DB  99                       cdq      
004A43DC  33 c2                    xor      eax, edx
004A43DE  2b c2                    sub      eax, edx
004A43E0  83 f8 02                 cmp      eax, 2
004A43E3  7f 05                    jg       0x4a43ea
004A43E5  c6 44 24 68 00           mov      byte ptr [esp + 0x68], 0
004A43EA  8b 54 24 68              mov      edx, dword ptr [esp + 0x68]
004A43EE  52                       push     edx
004A43EF  6a 01                    push     1
004A43F1  6a 01                    push     1
004A43F3  68 98 29 85 00           push     0x852998
004A43F8  e8 23 25 fd ff           call     0x476920
004A43FD  e9 72 fd ff ff           jmp      0x4a4174
004A4402  83 fe 01                 cmp      esi, 1
004A4405  0f 85 c6 00 00 00        jne      0x4a44d1
004A440B  8d 44 24 14              lea      eax, [esp + 0x14]
004A440F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A4414  50                       push     eax
004A4415  e8 56 3c 0a 00           call     0x548070
004A441A  8b c8                    mov      ecx, eax
004A441C  e8 1f 43 fd ff           call     0x478740
004A4421  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A4425  84 c0                    test     al, al
004A4427  74 27                    je       0x4a4450
004A4429  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A442C  8b 54 24 60              mov      edx, dword ptr [esp + 0x60]
004A4430  6a 00                    push     0
004A4432  6a 00                    push     0
004A4434  c7 81 d0 04 00 00 ff ff ff ff mov      dword ptr [ecx + 0x4d0], 0xffffffff
004A443E  52                       push     edx
004A443F  8b cd                    mov      ecx, ebp
004A4441  e8 2a e2 ff ff           call     0x4a2670
004A4446  5f                       pop      edi
004A4447  5e                       pop      esi
004A4448  5d                       pop      ebp
004A4449  5b                       pop      ebx
004A444A  83 c4 4c                 add      esp, 0x4c
004A444D  c2 0c 00                 ret      0xc
004A4450  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A4455  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A4458  3b c8                    cmp      ecx, eax
004A445A  75 1a                    jne      0x4a4476
004A445C  8b 4d 44                 mov      ecx, dword ptr [ebp + 0x44]
004A445F  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A4465  3b ca                    cmp      ecx, edx
004A4467  75 0d                    jne      0x4a4476
004A4469  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A446C  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A4472  3b d1                    cmp      edx, ecx
004A4474  74 18                    je       0x4a448e
004A4476  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A4479  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A447E  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A4481  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A4487  89 4d 48                 mov      dword ptr [ebp + 0x48], ecx
004A448A  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A448E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4491  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A4497  85 c0                    test     eax, eax
004A4499  75 18                    jne      0x4a44b3
004A449B  8b 11                    mov      edx, dword ptr [ecx]
004A449D  6a 01                    push     1
004A449F  6a 00                    push     0
004A44A1  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A44A7  5f                       pop      edi
004A44A8  5e                       pop      esi
004A44A9  5d                       pop      ebp
004A44AA  32 c0                    xor      al, al
004A44AC  5b                       pop      ebx
004A44AD  83 c4 4c                 add      esp, 0x4c
004A44B0  c2 0c 00                 ret      0xc
004A44B3  e8 f8 94 02 00           call     0x4cd9b0
004A44B8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A44BB  6a 01                    push     1
004A44BD  6a 00                    push     0
004A44BF  8b 01                    mov      eax, dword ptr [ecx]
004A44C1  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A44C7  5f                       pop      edi
004A44C8  5e                       pop      esi
004A44C9  5d                       pop      ebp
004A44CA  5b                       pop      ebx
004A44CB  83 c4 4c                 add      esp, 0x4c
004A44CE  c2 0c 00                 ret      0xc
004A44D1  83 fe 07                 cmp      esi, 7
004A44D4  0f 85 9a fc ff ff        jne      0x4a4174
004A44DA  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A44DE  84 c0                    test     al, al
004A44E0  74 40                    je       0x4a4522
004A44E2  c7 81 d0 04 00 00 ff ff ff ff mov      dword ptr [ecx + 0x4d0], 0xffffffff
004A44EC  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A44EF  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A44F4  33 c9                    xor      ecx, ecx
004A44F6  81 c2 30 05 00 00        add      edx, 0x530
004A44FC  89 02                    mov      dword ptr [edx], eax
004A44FE  8b 44 24 54              mov      eax, dword ptr [esp + 0x54]
004A4502  89 42 04                 mov      dword ptr [edx + 4], eax
004A4505  6a 00                    push     0
004A4507  6a 00                    push     0
004A4509  89 4a 08                 mov      dword ptr [edx + 8], ecx
004A450C  8b 4c 24 68              mov      ecx, dword ptr [esp + 0x68]
004A4510  51                       push     ecx
004A4511  8b cd                    mov      ecx, ebp
004A4513  e8 58 e1 ff ff           call     0x4a2670
004A4518  5f                       pop      edi
004A4519  5e                       pop      esi
004A451A  5d                       pop      ebp
004A451B  5b                       pop      ebx
004A451C  83 c4 4c                 add      esp, 0x4c
004A451F  c2 0c 00                 ret      0xc
004A4522  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A4527  8b 55 40                 mov      edx, dword ptr [ebp + 0x40]
004A452A  3b d0                    cmp      edx, eax
004A452C  75 1a                    jne      0x4a4548
004A452E  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A4531  8b 35 9c 29 85 00        mov      esi, dword ptr [0x85299c]
004A4537  3b d6                    cmp      edx, esi
004A4539  75 0d                    jne      0x4a4548
004A453B  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A453E  8b 35 a0 29 85 00        mov      esi, dword ptr [0x8529a0]
004A4544  3b d6                    cmp      edx, esi
004A4546  74 18                    je       0x4a4560
004A4548  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A454B  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A4550  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A4553  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A4559  89 55 48                 mov      dword ptr [ebp + 0x48], edx
004A455C  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A4560  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A4566  85 c0                    test     eax, eax
004A4568  0f 84 ca f4 ff ff        je       0x4a3a38
004A456E  e8 3d 94 02 00           call     0x4cd9b0
004A4573  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4576  6a 01                    push     1
004A4578  6a 00                    push     0
004A457A  8b 11                    mov      edx, dword ptr [ecx]
004A457C  ff 92 14 04 00 00        call     dword ptr [edx + 0x414]
004A4582  5f                       pop      edi
004A4583  5e                       pop      esi
004A4584  5d                       pop      ebp
004A4585  5b                       pop      ebx
004A4586  83 c4 4c                 add      esp, 0x4c
004A4589  c2 0c 00                 ret      0xc
004A458C  8d b1 d8 04 00 00        lea      esi, [ecx + 0x4d8]
004A4592  8d b9 d0 04 00 00        lea      edi, [ecx + 0x4d0]
004A4598  b9 16 00 00 00           mov      ecx, 0x16
004A459D  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004A459F  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A45A2  83 cf ff                 or       edi, 0xffffffff
004A45A5  89 ba 28 05 00 00        mov      dword ptr [edx + 0x528], edi
004A45AB  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A45AE  c6 80 7b 05 00 00 01     mov      byte ptr [eax + 0x57b], 1
004A45B5  eb 19                    jmp      0x4a45d0
004A45B7  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A45BA  b9 17 00 00 00           mov      ecx, 0x17
004A45BF  8d b0 d4 04 00 00        lea      esi, [eax + 0x4d4]
004A45C5  8d b8 d0 04 00 00        lea      edi, [eax + 0x4d0]
004A45CB  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004A45CD  83 cf ff                 or       edi, 0xffffffff
004A45D0  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A45D3  8d 75 40                 lea      esi, [ebp + 0x40]
004A45D6  89 b9 2c 05 00 00        mov      dword ptr [ecx + 0x52c], edi
004A45DC  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004A45E0  99                       cdq      
004A45E1  81 e2 ff 00 00 00        and      edx, 0xff
004A45E7  03 c2                    add      eax, edx
004A45E9  c1 f8 08                 sar      eax, 8
004A45EC  66 89 44 24 68           mov      word ptr [esp + 0x68], ax
004A45F1  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
004A45F5  99                       cdq      
004A45F6  81 e2 ff 00 00 00        and      edx, 0xff
004A45FC  03 c2                    add      eax, edx
004A45FE  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A4601  c1 f8 08                 sar      eax, 8
004A4604  66 89 44 24 6a           mov      word ptr [esp + 0x6a], ax
004A4609  8b 44 24 68              mov      eax, dword ptr [esp + 0x68]
004A460D  89 82 50 04 00 00        mov      dword ptr [edx + 0x450], eax
004A4613  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4616  c6 81 7a 05 00 00 00     mov      byte ptr [ecx + 0x57a], 0
004A461D  c7 45 5c 00 00 00 00     mov      dword ptr [ebp + 0x5c], 0
004A4624  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A4629  8b 0e                    mov      ecx, dword ptr [esi]
004A462B  3b c8                    cmp      ecx, eax
004A462D  75 1a                    jne      0x4a4649
004A462F  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A4632  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A4638  3b d1                    cmp      edx, ecx
004A463A  75 0d                    jne      0x4a4649
004A463C  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A463F  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A4645  3b ca                    cmp      ecx, edx
004A4647  74 1e                    je       0x4a4667
004A4649  8b d6                    mov      edx, esi
004A464B  89 02                    mov      dword ptr [edx], eax
004A464D  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A4652  89 42 04                 mov      dword ptr [edx + 4], eax
004A4655  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A465B  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A465F  89 4a 08                 mov      dword ptr [edx + 8], ecx
004A4662  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A4667  8b 4c 24 38              mov      ecx, dword ptr [esp + 0x38]
004A466B  8b 54 24 40              mov      edx, dword ptr [esp + 0x40]
004A466F  3b c8                    cmp      ecx, eax
004A4671  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
004A4675  75 10                    jne      0x4a4687
004A4677  3b 05 9c 29 85 00        cmp      eax, dword ptr [0x85299c]
004A467D  75 08                    jne      0x4a4687
004A467F  3b 15 a0 29 85 00        cmp      edx, dword ptr [0x8529a0]
004A4685  74 77                    je       0x4a46fe
004A4687  8b de                    mov      ebx, esi
004A4689  c6 45 63 01              mov      byte ptr [ebp + 0x63], 1
004A468D  89 0b                    mov      dword ptr [ebx], ecx
004A468F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A4694  89 43 04                 mov      dword ptr [ebx + 4], eax
004A4697  8d 44 24 38              lea      eax, [esp + 0x38]
004A469B  89 53 08                 mov      dword ptr [ebx + 8], edx
004A469E  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A46A1  52                       push     edx
004A46A2  50                       push     eax
004A46A3  e8 58 39 0a 00           call     0x548000
004A46A8  8b c8                    mov      ecx, eax
004A46AA  e8 11 26 fd ff           call     0x476cc0
004A46AF  84 c0                    test     al, al
004A46B1  74 24                    je       0x4a46d7
004A46B3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A46B6  8a 41 76                 mov      al, byte ptr [ecx + 0x76]
004A46B9  84 c0                    test     al, al
004A46BB  75 1a                    jne      0x4a46d7
004A46BD  8d 54 24 38              lea      edx, [esp + 0x38]
004A46C1  6a 01                    push     1
004A46C3  52                       push     edx
004A46C4  8b cd                    mov      ecx, ebp
004A46C6  e8 f5 c4 ff ff           call     0x4a0bc0
004A46CB  5f                       pop      edi
004A46CC  5e                       pop      esi
004A46CD  5d                       pop      ebp
004A46CE  32 c0                    xor      al, al
004A46D0  5b                       pop      ebx
004A46D1  83 c4 4c                 add      esp, 0x4c
004A46D4  c2 0c 00                 ret      0xc
004A46D7  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A46DA  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A46DD  84 c9                    test     cl, cl
004A46DF  74 1d                    je       0x4a46fe
004A46E1  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
004A46E7  89 0e                    mov      dword ptr [esi], ecx
004A46E9  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A46EF  89 56 04                 mov      dword ptr [esi + 4], edx
004A46F2  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A46F7  89 46 08                 mov      dword ptr [esi + 8], eax
004A46FA  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A46FE  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4701  89 7d 58                 mov      dword ptr [ebp + 0x58], edi
004A4704  6a 00                    push     0
004A4706  6a 00                    push     0
004A4708  89 b9 d0 04 00 00        mov      dword ptr [ecx + 0x4d0], edi
004A470E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A4711  8b 11                    mov      edx, dword ptr [ecx]
004A4713  ff 92 c8 04 00 00        call     dword ptr [edx + 0x4c8]
004A4719  5f                       pop      edi
004A471A  5e                       pop      esi
004A471B  5d                       pop      ebp
004A471C  32 c0                    xor      al, al
004A471E  5b                       pop      ebx
004A471F  83 c4 4c                 add      esp, 0x4c
004A4722  c2 0c 00                 ret      0xc
