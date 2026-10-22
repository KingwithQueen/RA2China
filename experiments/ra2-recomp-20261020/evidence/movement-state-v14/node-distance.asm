
sub_00427D40 0x00427E2A size=93
00427E2A  8b 54 24 18              mov      edx, dword ptr [esp + 0x18]
00427E2E  8b 5c 24 1c              mov      ebx, dword ptr [esp + 0x1c]
00427E32  83 ec 08                 sub      esp, 8
00427E35  8b 3a                    mov      edi, dword ptr [edx]
00427E37  0f bf 0b                 movsx    ecx, word ptr [ebx]
00427E3A  0f bf 47 24              movsx    eax, word ptr [edi + 0x24]
00427E3E  83 c7 24                 add      edi, 0x24
00427E41  2b c1                    sub      eax, ecx
00427E43  99                       cdq      
00427E44  8b c8                    mov      ecx, eax
00427E46  0f bf 47 02              movsx    eax, word ptr [edi + 2]
00427E4A  33 ca                    xor      ecx, edx
00427E4C  2b ca                    sub      ecx, edx
00427E4E  0f bf 53 02              movsx    edx, word ptr [ebx + 2]
00427E52  2b c2                    sub      eax, edx
00427E54  99                       cdq      
00427E55  33 c2                    xor      eax, edx
00427E57  2b c2                    sub      eax, edx
00427E59  8b d0                    mov      edx, eax
00427E5B  0f af d0                 imul     edx, eax
00427E5E  8b c1                    mov      eax, ecx
00427E60  0f af c1                 imul     eax, ecx
00427E63  03 d0                    add      edx, eax
00427E65  89 54 24 20              mov      dword ptr [esp + 0x20], edx
00427E69  db 44 24 20              fild     dword ptr [esp + 0x20]
00427E6D  dd 1c 24                 fstp     qword ptr [esp]
00427E70  e8 9b 25 09 00           call     0x4ba410
00427E75  d8 46 04                 fadd     dword ptr [esi + 4]
00427E78  83 c4 08                 add      esp, 8
00427E7B  8b c6                    mov      eax, esi
00427E7D  5f                       pop      edi
00427E7E  d9 5e 08                 fstp     dword ptr [esi + 8]
00427E81  5e                       pop      esi
00427E82  5d                       pop      ebp
00427E83  5b                       pop      ebx
00427E84  c2 10 00                 ret      0x10
