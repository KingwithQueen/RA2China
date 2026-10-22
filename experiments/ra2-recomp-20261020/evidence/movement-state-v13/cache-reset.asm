
sub_00427E90 0x00427E90 size=222
00427E90  8b 41 0c                 mov      eax, dword ptr [ecx + 0xc]
00427E93  83 ec 08                 sub      esp, 8
00427E96  56                       push     esi
00427E97  33 f6                    xor      esi, esi
00427E99  89 b0 00 00 18 00        mov      dword ptr [eax + 0x180000], esi
00427E9F  8b 51 10                 mov      edx, dword ptr [ecx + 0x10]
00427EA2  57                       push     edi
00427EA3  89 b2 00 00 10 00        mov      dword ptr [edx + 0x100000], esi
00427EA9  8b 41 14                 mov      eax, dword ptr [ecx + 0x14]
00427EAC  33 d2                    xor      edx, edx
00427EAE  39 30                    cmp      dword ptr [eax], esi
00427EB0  7c 0e                    jl       0x427ec0
00427EB2  8b 78 08                 mov      edi, dword ptr [eax + 8]
00427EB5  42                       inc      edx
00427EB6  89 74 97 fc              mov      dword ptr [edi + edx*4 - 4], esi
00427EBA  8b 38                    mov      edi, dword ptr [eax]
00427EBC  3b d7                    cmp      edx, edi
00427EBE  7e f2                    jle      0x427eb2
00427EC0  89 30                    mov      dword ptr [eax], esi
00427EC2  8b 41 68                 mov      eax, dword ptr [ecx + 0x68]
00427EC5  33 d2                    xor      edx, edx
00427EC7  39 30                    cmp      dword ptr [eax], esi
00427EC9  7c 0e                    jl       0x427ed9
00427ECB  8b 78 08                 mov      edi, dword ptr [eax + 8]
00427ECE  42                       inc      edx
00427ECF  89 74 97 fc              mov      dword ptr [edi + edx*4 - 4], esi
00427ED3  8b 38                    mov      edi, dword ptr [eax]
00427ED5  3b d7                    cmp      edx, edi
00427ED7  7e f2                    jle      0x427ecb
00427ED9  89 30                    mov      dword ptr [eax], esi
00427EDB  8b 41 28                 mov      eax, dword ptr [ecx + 0x28]
00427EDE  40                       inc      eax
00427EDF  89 41 28                 mov      dword ptr [ecx + 0x28], eax
00427EE2  0f 85 80 00 00 00        jne      0x427f68
00427EE8  a1 04 e8 84 00           mov      eax, dword ptr [0x84e804]
00427EED  0f af c0                 imul     eax, eax
00427EF0  48                       dec      eax
00427EF1  78 11                    js       0x427f04
00427EF3  8b 51 18                 mov      edx, dword ptr [ecx + 0x18]
00427EF6  48                       dec      eax
00427EF7  89 74 82 04              mov      dword ptr [edx + eax*4 + 4], esi
00427EFB  8b 51 1c                 mov      edx, dword ptr [ecx + 0x1c]
00427EFE  89 74 82 04              mov      dword ptr [edx + eax*4 + 4], esi
00427F02  79 ef                    jns      0x427ef3
00427F04  b8 04 25 83 00           mov      eax, 0x832504
00427F09  53                       push     ebx
00427F0A  2b c1                    sub      eax, ecx
00427F0C  55                       push     ebp
00427F0D  8d 69 4c                 lea      ebp, [ecx + 0x4c]
00427F10  89 44 24 14              mov      dword ptr [esp + 0x14], eax
00427F14  c7 44 24 10 03 00 00 00  mov      dword ptr [esp + 0x10], 3
00427F1C  8b 14 28                 mov      edx, dword ptr [eax + ebp]
00427F1F  8b 7d f4                 mov      edi, dword ptr [ebp - 0xc]
00427F22  8b 75 00                 mov      esi, dword ptr [ebp]
00427F25  8b 5d 0c                 mov      ebx, dword ptr [ebp + 0xc]
00427F28  4a                       dec      edx
00427F29  78 26                    js       0x427f51
00427F2B  8d 04 96                 lea      eax, [esi + edx*4]
00427F2E  2b fe                    sub      edi, esi
00427F30  2b de                    sub      ebx, esi
00427F32  42                       inc      edx
00427F33  c7 04 07 00 00 00 00     mov      dword ptr [edi + eax], 0
00427F3A  c7 00 00 00 00 00        mov      dword ptr [eax], 0
00427F40  c7 04 03 00 00 00 00     mov      dword ptr [ebx + eax], 0
00427F47  83 e8 04                 sub      eax, 4
00427F4A  4a                       dec      edx
00427F4B  75 e6                    jne      0x427f33
00427F4D  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427F51  8b 54 24 10              mov      edx, dword ptr [esp + 0x10]
00427F55  83 c5 04                 add      ebp, 4
00427F58  4a                       dec      edx
00427F59  89 54 24 10              mov      dword ptr [esp + 0x10], edx
00427F5D  75 bd                    jne      0x427f1c
00427F5F  8b 41 28                 mov      eax, dword ptr [ecx + 0x28]
00427F62  5d                       pop      ebp
00427F63  40                       inc      eax
00427F64  5b                       pop      ebx
00427F65  89 41 28                 mov      dword ptr [ecx + 0x28], eax
00427F68  5f                       pop      edi
00427F69  5e                       pop      esi
00427F6A  83 c4 08                 add      esp, 8
00427F6D  c3                       ret      
