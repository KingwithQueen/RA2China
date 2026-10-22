
sub_006E1730 0x006E1730 size=224
006E1730  8b 44 24 08              mov      eax, dword ptr [esp + 8]
006E1734  85 c0                    test     eax, eax
006E1736  75 08                    jne      0x6e1740
006E1738  b8 03 40 00 80           mov      eax, 0x80004003
006E173D  c2 08 00                 ret      8
006E1740  8b 0d d0 1f 7a 00        mov      ecx, dword ptr [0x7a1fd0]
006E1746  89 08                    mov      dword ptr [eax], ecx
006E1748  8b 15 d4 1f 7a 00        mov      edx, dword ptr [0x7a1fd4]
006E174E  89 50 04                 mov      dword ptr [eax + 4], edx
006E1751  8b 0d d8 1f 7a 00        mov      ecx, dword ptr [0x7a1fd8]
006E1757  89 48 08                 mov      dword ptr [eax + 8], ecx
006E175A  8b 15 dc 1f 7a 00        mov      edx, dword ptr [0x7a1fdc]
006E1760  89 50 0c                 mov      dword ptr [eax + 0xc], edx
006E1763  33 c0                    xor      eax, eax
006E1765  c2 08 00                 ret      8
006E1768  90                       nop      
006E1769  90                       nop      
006E176A  90                       nop      
006E176B  90                       nop      
006E176C  90                       nop      
006E176D  90                       nop      
006E176E  90                       nop      
006E176F  90                       nop      
006E1770  55                       push     ebp
006E1771  56                       push     esi
006E1772  8b 74 24 0c              mov      esi, dword ptr [esp + 0xc]
006E1776  57                       push     edi
006E1777  8b 7c 24 14              mov      edi, dword ptr [esp + 0x14]
006E177B  57                       push     edi
006E177C  56                       push     esi
006E177D  e8 3e bc e5 ff           call     0x53d3c0
006E1782  8b e8                    mov      ebp, eax
006E1784  85 ed                    test     ebp, ebp
006E1786  7c 7b                    jl       0x6e1803
006E1788  85 f6                    test     esi, esi
006E178A  74 37                    je       0x6e17c3
006E178C  c7 06 b4 33 7a 00        mov      dword ptr [esi], 0x7a33b4
006E1792  c7 46 04 ec 32 7a 00     mov      dword ptr [esi + 4], 0x7a32ec
006E1799  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
006E179E  c7 46 44 00 00 00 00     mov      dword ptr [esi + 0x44], 0
006E17A5  89 46 3c                 mov      dword ptr [esi + 0x3c], eax
006E17A8  c7 46 48 00 00 00 00     mov      dword ptr [esi + 0x48], 0
006E17AF  c7 06 70 d2 7a 00        mov      dword ptr [esi], 0x7ad270
006E17B5  c7 46 04 a8 d1 7a 00     mov      dword ptr [esi + 4], 0x7ad1a8
006E17BC  c7 46 18 84 d1 7a 00     mov      dword ptr [esi + 0x18], 0x7ad184
006E17C3  8b 0f                    mov      ecx, dword ptr [edi]
006E17C5  6a 00                    push     0
006E17C7  8d 54 24 18              lea      edx, [esp + 0x18]
006E17CB  6a 01                    push     1
006E17CD  52                       push     edx
006E17CE  57                       push     edi
006E17CF  ff 51 0c                 call     dword ptr [ecx + 0xc]
006E17D2  8a 44 24 14              mov      al, byte ptr [esp + 0x14]
006E17D6  84 c0                    test     al, al
006E17D8  74 29                    je       0x6e1803
006E17DA  8b 46 48                 mov      eax, dword ptr [esi + 0x48]
006E17DD  83 c6 48                 add      esi, 0x48
006E17E0  85 c0                    test     eax, eax
006E17E2  74 06                    je       0x6e17ea
006E17E4  8b 08                    mov      ecx, dword ptr [eax]
006E17E6  50                       push     eax
006E17E7  ff 51 08                 call     dword ptr [ecx + 8]
006E17EA  56                       push     esi
006E17EB  68 90 58 7a 00           push     0x7a5890
006E17F0  57                       push     edi
006E17F1  c7 06 00 00 00 00        mov      dword ptr [esi], 0
006E17F7  ff 15 ec a5 79 00        call     dword ptr [0x79a5ec]
006E17FD  5f                       pop      edi
006E17FE  5e                       pop      esi
006E17FF  5d                       pop      ebp
006E1800  c2 08 00                 ret      8
006E1803  5f                       pop      edi
006E1804  8b c5                    mov      eax, ebp
006E1806  5e                       pop      esi
006E1807  5d                       pop      ebp
006E1808  c2 08 00                 ret      8
006E180B  90                       nop      
006E180C  90                       nop      
006E180D  90                       nop      
006E180E  90                       nop      
006E180F  90                       nop      
