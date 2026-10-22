
sub_004C2EF0 0x004C2EF0 size=272
004C2EF0  83 ec 14                 sub      esp, 0x14
004C2EF3  53                       push     ebx
004C2EF4  56                       push     esi
004C2EF5  8b f1                    mov      esi, ecx
004C2EF7  8b 06                    mov      eax, dword ptr [esi]
004C2EF9  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004C2EFF  8b 98 00 05 00 00        mov      ebx, dword ptr [eax + 0x500]
004C2F05  83 fb ff                 cmp      ebx, -1
004C2F08  75 0a                    jne      0x4c2f14
004C2F0A  5e                       pop      esi
004C2F0B  b0 01                    mov      al, 1
004C2F0D  5b                       pop      ebx
004C2F0E  83 c4 14                 add      esp, 0x14
004C2F11  c2 04 00                 ret      4
004C2F14  57                       push     edi
004C2F15  8b 7c 24 24              mov      edi, dword ptr [esp + 0x24]
004C2F19  8b 07                    mov      eax, dword ptr [edi]
004C2F1B  99                       cdq      
004C2F1C  81 e2 ff 00 00 00        and      edx, 0xff
004C2F22  03 c2                    add      eax, edx
004C2F24  8b c8                    mov      ecx, eax
004C2F26  8b 47 04                 mov      eax, dword ptr [edi + 4]
004C2F29  99                       cdq      
004C2F2A  81 e2 ff 00 00 00        and      edx, 0xff
004C2F30  5f                       pop      edi
004C2F31  03 c2                    add      eax, edx
004C2F33  c1 f9 08                 sar      ecx, 8
004C2F36  c1 f8 08                 sar      eax, 8
004C2F39  66 3b 0d 00 5f 86 00     cmp      cx, word ptr [0x865f00]
004C2F40  66 89 4c 24 20           mov      word ptr [esp + 0x20], cx
004C2F45  66 89 44 24 22           mov      word ptr [esp + 0x22], ax
004C2F4A  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004C2F4E  89 54 24 08              mov      dword ptr [esp + 8], edx
004C2F52  75 13                    jne      0x4c2f67
004C2F54  66 3b 05 02 5f 86 00     cmp      ax, word ptr [0x865f02]
004C2F5B  75 0a                    jne      0x4c2f67
004C2F5D  5e                       pop      esi
004C2F5E  32 c0                    xor      al, al
004C2F60  5b                       pop      ebx
004C2F61  83 c4 14                 add      esp, 0x14
004C2F64  c2 04 00                 ret      4
004C2F67  8b 06                    mov      eax, dword ptr [esi]
004C2F69  8d 4c 24 10              lea      ecx, [esp + 0x10]
004C2F6D  6a 00                    push     0
004C2F6F  51                       push     ecx
004C2F70  8b ce                    mov      ecx, esi
004C2F72  ff 50 4c                 call     dword ptr [eax + 0x4c]
004C2F75  8b c8                    mov      ecx, eax
004C2F77  8b 01                    mov      eax, dword ptr [ecx]
004C2F79  99                       cdq      
004C2F7A  81 e2 ff 00 00 00        and      edx, 0xff
004C2F80  03 c2                    add      eax, edx
004C2F82  c1 f8 08                 sar      eax, 8
004C2F85  66 89 44 24 20           mov      word ptr [esp + 0x20], ax
004C2F8A  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004C2F8D  99                       cdq      
004C2F8E  81 e2 ff 00 00 00        and      edx, 0xff
004C2F94  8b ce                    mov      ecx, esi
004C2F96  03 c2                    add      eax, edx
004C2F98  c1 f8 08                 sar      eax, 8
004C2F9B  66 89 44 24 22           mov      word ptr [esp + 0x22], ax
004C2FA0  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004C2FA4  8b 06                    mov      eax, dword ptr [esi]
004C2FA6  89 54 24 0c              mov      dword ptr [esp + 0xc], edx
004C2FAA  ff 90 f4 02 00 00        call     dword ptr [eax + 0x2f4]
004C2FB0  8d 4c 24 08              lea      ecx, [esp + 8]
004C2FB4  50                       push     eax
004C2FB5  51                       push     ecx
004C2FB6  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C2FBB  e8 b0 50 08 00           call     0x548070
004C2FC0  8b 90 40 01 00 00        mov      edx, dword ptr [eax + 0x140]
004C2FC6  8b 06                    mov      eax, dword ptr [esi]
004C2FC8  c1 ea 08                 shr      edx, 8
004C2FCB  80 e2 01                 and      dl, 1
004C2FCE  8b ce                    mov      ecx, esi
004C2FD0  52                       push     edx
004C2FD1  6a 00                    push     0
004C2FD3  ff 90 b8 00 00 00        call     dword ptr [eax + 0xb8]
004C2FD9  50                       push     eax
004C2FDA  8d 4c 24 14              lea      ecx, [esp + 0x14]
004C2FDE  53                       push     ebx
004C2FDF  8d 54 24 1c              lea      edx, [esp + 0x1c]
004C2FE3  51                       push     ecx
004C2FE4  52                       push     edx
004C2FE5  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C2FEA  e8 d1 c7 08 00           call     0x54f7c0
004C2FEF  5e                       pop      esi
004C2FF0  5b                       pop      ebx
004C2FF1  83 c4 14                 add      esp, 0x14
004C2FF4  c2 04 00                 ret      4
004C2FF7  90                       nop      
004C2FF8  90                       nop      
004C2FF9  90                       nop      
004C2FFA  90                       nop      
004C2FFB  90                       nop      
004C2FFC  90                       nop      
004C2FFD  90                       nop      
004C2FFE  90                       nop      
004C2FFF  90                       nop      
