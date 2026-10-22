
sub_006E1960 0x006E1960 size=256
006E1960  8b 44 24 08              mov      eax, dword ptr [esp + 8]
006E1964  85 c0                    test     eax, eax
006E1966  75 08                    jne      0x6e1970
006E1968  b8 03 40 00 80           mov      eax, 0x80004003
006E196D  c2 08 00                 ret      8
006E1970  8b 4c 24 04              mov      ecx, dword ptr [esp + 4]
006E1974  8b 51 30                 mov      edx, dword ptr [ecx + 0x30]
006E1977  85 d2                    test     edx, edx
006E1979  75 20                    jne      0x6e199b
006E197B  56                       push     esi
006E197C  8b f2                    mov      esi, edx
006E197E  3b f0                    cmp      esi, eax
006E1980  74 13                    je       0x6e1995
006E1982  89 41 30                 mov      dword ptr [ecx + 0x30], eax
006E1985  8b 08                    mov      ecx, dword ptr [eax]
006E1987  50                       push     eax
006E1988  ff 51 04                 call     dword ptr [ecx + 4]
006E198B  85 f6                    test     esi, esi
006E198D  74 06                    je       0x6e1995
006E198F  8b 16                    mov      edx, dword ptr [esi]
006E1991  56                       push     esi
006E1992  ff 52 08                 call     dword ptr [edx + 8]
006E1995  33 c0                    xor      eax, eax
006E1997  5e                       pop      esi
006E1998  c2 08 00                 ret      8
006E199B  b8 05 40 00 80           mov      eax, 0x80004005
006E19A0  c2 08 00                 ret      8
006E19A3  90                       nop      
006E19A4  90                       nop      
006E19A5  90                       nop      
006E19A6  90                       nop      
006E19A7  90                       nop      
006E19A8  90                       nop      
006E19A9  90                       nop      
006E19AA  90                       nop      
006E19AB  90                       nop      
006E19AC  90                       nop      
006E19AD  90                       nop      
006E19AE  90                       nop      
006E19AF  90                       nop      
006E19B0  8b 54 24 08              mov      edx, dword ptr [esp + 8]
006E19B4  85 d2                    test     edx, edx
006E19B6  75 08                    jne      0x6e19c0
006E19B8  b8 03 40 00 80           mov      eax, 0x80004003
006E19BD  c2 08 00                 ret      8
006E19C0  8b 4c 24 04              mov      ecx, dword ptr [esp + 4]
006E19C4  8b 41 30                 mov      eax, dword ptr [ecx + 0x30]
006E19C7  85 c0                    test     eax, eax
006E19C9  74 0e                    je       0x6e19d9
006E19CB  89 02                    mov      dword ptr [edx], eax
006E19CD  c7 41 30 00 00 00 00     mov      dword ptr [ecx + 0x30], 0
006E19D4  33 c0                    xor      eax, eax
006E19D6  c2 08 00                 ret      8
006E19D9  b8 01 00 00 00           mov      eax, 1
006E19DE  c2 08 00                 ret      8
006E19E1  90                       nop      
006E19E2  90                       nop      
006E19E3  90                       nop      
006E19E4  90                       nop      
006E19E5  90                       nop      
006E19E6  90                       nop      
006E19E7  90                       nop      
006E19E8  90                       nop      
006E19E9  90                       nop      
006E19EA  90                       nop      
006E19EB  90                       nop      
006E19EC  90                       nop      
006E19ED  90                       nop      
006E19EE  90                       nop      
006E19EF  90                       nop      
006E19F0  56                       push     esi
006E19F1  8b 74 24 08              mov      esi, dword ptr [esp + 8]
006E19F5  8b 4e ec                 mov      ecx, dword ptr [esi - 0x14]
006E19F8  8d 46 ec                 lea      eax, [esi - 0x14]
006E19FB  50                       push     eax
006E19FC  ff 51 10                 call     dword ptr [ecx + 0x10]
006E19FF  84 c0                    test     al, al
006E1A01  75 28                    jne      0x6e1a2b
006E1A03  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
006E1A06  85 c0                    test     eax, eax
006E1A08  74 21                    je       0x6e1a2b
006E1A0A  8a 46 1d                 mov      al, byte ptr [esi + 0x1d]
006E1A0D  84 c0                    test     al, al
006E1A0F  75 1a                    jne      0x6e1a2b
006E1A11  8b 56 f4                 mov      edx, dword ptr [esi - 0xc]
006E1A14  8a 82 10 02 00 00        mov      al, byte ptr [edx + 0x210]
006E1A1A  84 c0                    test     al, al
006E1A1C  75 0d                    jne      0x6e1a2b
006E1A1E  8b 46 20                 mov      eax, dword ptr [esi + 0x20]
006E1A21  85 c0                    test     eax, eax
006E1A23  75 06                    jne      0x6e1a2b
006E1A25  b0 01                    mov      al, 1
006E1A27  5e                       pop      esi
006E1A28  c2 04 00                 ret      4
006E1A2B  32 c0                    xor      al, al
006E1A2D  5e                       pop      esi
006E1A2E  c2 04 00                 ret      4
006E1A31  90                       nop      
006E1A32  90                       nop      
006E1A33  90                       nop      
006E1A34  90                       nop      
006E1A35  90                       nop      
006E1A36  90                       nop      
006E1A37  90                       nop      
006E1A38  90                       nop      
006E1A39  90                       nop      
006E1A3A  90                       nop      
006E1A3B  90                       nop      
006E1A3C  90                       nop      
006E1A3D  90                       nop      
006E1A3E  90                       nop      
006E1A3F  90                       nop      
006E1A40  55                       push     ebp
006E1A41  8b 6c 24 0c              mov      ebp, dword ptr [esp + 0xc]
006E1A45  85 ed                    test     ebp, ebp
006E1A47  56                       push     esi
006E1A48  75 0a                    jne      0x6e1a54
006E1A4A  5e                       pop      esi
006E1A4B  b8 03 40 00 80           mov      eax, 0x80004003
006E1A50  5d                       pop      ebp
006E1A51  c2 08 00                 ret      8
006E1A54  8b 4c 24 0c              mov      ecx, dword ptr [esp + 0xc]
006E1A58  8b 51 30                 mov      edx, dword ptr [ecx + 0x30]
006E1A5B  8d 41 30                 lea      eax, [ecx + 0x30]
006E1A5E  85 d2                    test     edx, edx
