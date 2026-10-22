
sub_004A134F 0x004A1540 size=2288
004A1540  00 00                    add      byte ptr [eax], al
004A1542  00 52 b9                 add      byte ptr [edx - 0x47], dl
004A1545  e0 24                    loopne   0x4a156b
004A1547  83 00 e8                 add      dword ptr [eax], -0x18
004A154A  32 8d 0b 00 2b c6        xor      cl, byte ptr [ebp - 0x39d4fff5]
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
