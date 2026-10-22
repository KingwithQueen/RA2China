
sub_004A3E35 0x004A3E35 size=342
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
