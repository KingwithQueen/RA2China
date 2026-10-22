
sub_004B5E60 0x004B5E80 size=1872
004B5E80  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B5E85  8b 0d 84 66 7d 00        mov      ecx, dword ptr [0x7d6684]
004B5E8B  3b c1                    cmp      eax, ecx
004B5E8D  74 0d                    je       0x4b5e9c
004B5E8F  32 c9                    xor      cl, cl
004B5E91  8a c1                    mov      al, cl
004B5E93  fe c1                    inc      cl
004B5E95  88 0d 9c 5b 85 00        mov      byte ptr [0x855b9c], cl
004B5E9B  c3                       ret      
004B5E9C  8a 0d 9c 5b 85 00        mov      cl, byte ptr [0x855b9c]
004B5EA2  8a c1                    mov      al, cl
004B5EA4  fe c1                    inc      cl
004B5EA6  88 0d 9c 5b 85 00        mov      byte ptr [0x855b9c], cl
004B5EAC  c3                       ret      
004B5EAD  90                       nop      
004B5EAE  90                       nop      
004B5EAF  90                       nop      
004B5EB0  8b c1                    mov      eax, ecx
004B5EB2  8b 4c 24 04              mov      ecx, dword ptr [esp + 4]
004B5EB6  85 c9                    test     ecx, ecx
004B5EB8  7c 19                    jl       0x4b5ed3
004B5EBA  88 48 02                 mov      byte ptr [eax + 2], cl
004B5EBD  8b 4c 24 08              mov      ecx, dword ptr [esp + 8]
004B5EC1  c6 00 18                 mov      byte ptr [eax], 0x18
004B5EC4  89 48 07                 mov      dword ptr [eax + 7], ecx
004B5EC7  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B5ECD  89 50 03                 mov      dword ptr [eax + 3], edx
004B5ED0  c2 08 00                 ret      8
004B5ED3  c6 40 02 ff              mov      byte ptr [eax + 2], 0xff
004B5ED7  c6 00 00                 mov      byte ptr [eax], 0
004B5EDA  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B5EE0  89 48 03                 mov      dword ptr [eax + 3], ecx
004B5EE3  c2 08 00                 ret      8
004B5EE6  90                       nop      
004B5EE7  90                       nop      
004B5EE8  90                       nop      
004B5EE9  90                       nop      
004B5EEA  90                       nop      
004B5EEB  90                       nop      
004B5EEC  90                       nop      
004B5EED  90                       nop      
004B5EEE  90                       nop      
004B5EEF  90                       nop      
004B5EF0  53                       push     ebx
004B5EF1  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B5EF5  8b c3                    mov      eax, ebx
004B5EF7  56                       push     esi
004B5EF8  25 ff 00 00 00           and      eax, 0xff
004B5EFD  8b f1                    mov      esi, ecx
004B5EFF  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B5F06  51                       push     ecx
004B5F07  68 90 68 7d 00           push     0x7d6890
004B5F0C  e8 df 09 f5 ff           call     0x4068f0
004B5F11  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B5F15  83 c4 08                 add      esp, 8
004B5F18  85 c0                    test     eax, eax
004B5F1A  7c 25                    jl       0x4b5f41
004B5F1C  8a 4c 24 18              mov      cl, byte ptr [esp + 0x18]
004B5F20  88 46 02                 mov      byte ptr [esi + 2], al
004B5F23  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B5F27  8d 56 07                 lea      edx, [esi + 7]
004B5F2A  88 1e                    mov      byte ptr [esi], bl
004B5F2C  89 02                    mov      dword ptr [edx], eax
004B5F2E  8b c6                    mov      eax, esi
004B5F30  88 4a 04                 mov      byte ptr [edx + 4], cl
004B5F33  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B5F39  89 56 03                 mov      dword ptr [esi + 3], edx
004B5F3C  5e                       pop      esi
004B5F3D  5b                       pop      ebx
004B5F3E  c2 10 00                 ret      0x10
004B5F41  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B5F45  c6 06 00                 mov      byte ptr [esi], 0
004B5F48  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B5F4D  89 46 03                 mov      dword ptr [esi + 3], eax
004B5F50  8b c6                    mov      eax, esi
004B5F52  5e                       pop      esi
004B5F53  5b                       pop      ebx
004B5F54  c2 10 00                 ret      0x10
004B5F57  90                       nop      
004B5F58  90                       nop      
004B5F59  90                       nop      
004B5F5A  90                       nop      
004B5F5B  90                       nop      
004B5F5C  90                       nop      
004B5F5D  90                       nop      
004B5F5E  90                       nop      
004B5F5F  90                       nop      
004B5F60  53                       push     ebx
004B5F61  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B5F65  8b c3                    mov      eax, ebx
004B5F67  56                       push     esi
004B5F68  25 ff 00 00 00           and      eax, 0xff
004B5F6D  8b f1                    mov      esi, ecx
004B5F6F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B5F76  51                       push     ecx
004B5F77  68 90 68 7d 00           push     0x7d6890
004B5F7C  e8 6f 09 f5 ff           call     0x4068f0
004B5F81  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B5F85  83 c4 08                 add      esp, 8
004B5F88  85 c0                    test     eax, eax
004B5F8A  7c 28                    jl       0x4b5fb4
004B5F8C  88 46 02                 mov      byte ptr [esi + 2], al
004B5F8F  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B5F93  88 1e                    mov      byte ptr [esi], bl
004B5F95  66 8b 10                 mov      dx, word ptr [eax]
004B5F98  66 89 56 07              mov      word ptr [esi + 7], dx
004B5F9C  66 8b 40 02              mov      ax, word ptr [eax + 2]
004B5FA0  66 89 46 09              mov      word ptr [esi + 9], ax
004B5FA4  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B5FAA  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B5FAD  8b c6                    mov      eax, esi
004B5FAF  5e                       pop      esi
004B5FB0  5b                       pop      ebx
004B5FB1  c2 0c 00                 ret      0xc
004B5FB4  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B5FB8  c6 06 00                 mov      byte ptr [esi], 0
004B5FBB  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B5FC1  8b c6                    mov      eax, esi
004B5FC3  89 56 03                 mov      dword ptr [esi + 3], edx
004B5FC6  5e                       pop      esi
004B5FC7  5b                       pop      ebx
004B5FC8  c2 0c 00                 ret      0xc
004B5FCB  90                       nop      
004B5FCC  90                       nop      
004B5FCD  90                       nop      
004B5FCE  90                       nop      
004B5FCF  90                       nop      
004B5FD0  53                       push     ebx
004B5FD1  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B5FD5  8b c3                    mov      eax, ebx
004B5FD7  56                       push     esi
004B5FD8  25 ff 00 00 00           and      eax, 0xff
004B5FDD  8b f1                    mov      esi, ecx
004B5FDF  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B5FE6  51                       push     ecx
004B5FE7  68 90 68 7d 00           push     0x7d6890
004B5FEC  e8 ff 08 f5 ff           call     0x4068f0
004B5FF1  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B5FF5  83 c4 08                 add      esp, 8
004B5FF8  85 c0                    test     eax, eax
004B5FFA  7c 15                    jl       0x4b6011
004B5FFC  88 46 02                 mov      byte ptr [esi + 2], al
004B5FFF  88 1e                    mov      byte ptr [esi], bl
004B6001  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B6007  8b c6                    mov      eax, esi
004B6009  89 56 03                 mov      dword ptr [esi + 3], edx
004B600C  5e                       pop      esi
004B600D  5b                       pop      ebx
004B600E  c2 08 00                 ret      8
004B6011  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B6015  c6 06 00                 mov      byte ptr [esi], 0
004B6018  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B601D  89 46 03                 mov      dword ptr [esi + 3], eax
004B6020  8b c6                    mov      eax, esi
004B6022  5e                       pop      esi
004B6023  5b                       pop      ebx
004B6024  c2 08 00                 ret      8
004B6027  90                       nop      
004B6028  90                       nop      
004B6029  90                       nop      
004B602A  90                       nop      
004B602B  90                       nop      
004B602C  90                       nop      
004B602D  90                       nop      
004B602E  90                       nop      
004B602F  90                       nop      
004B6030  53                       push     ebx
004B6031  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B6035  8b c3                    mov      eax, ebx
004B6037  56                       push     esi
004B6038  25 ff 00 00 00           and      eax, 0xff
004B603D  8b f1                    mov      esi, ecx
004B603F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6046  51                       push     ecx
004B6047  68 90 68 7d 00           push     0x7d6890
004B604C  e8 9f 08 f5 ff           call     0x4068f0
004B6051  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6055  83 c4 08                 add      esp, 8
004B6058  85 c0                    test     eax, eax
004B605A  7c 1b                    jl       0x4b6077
004B605C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B6060  88 46 02                 mov      byte ptr [esi + 2], al
004B6063  88 1e                    mov      byte ptr [esi], bl
004B6065  89 56 07                 mov      dword ptr [esi + 7], edx
004B6068  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B606D  89 46 03                 mov      dword ptr [esi + 3], eax
004B6070  8b c6                    mov      eax, esi
004B6072  5e                       pop      esi
004B6073  5b                       pop      ebx
004B6074  c2 0c 00                 ret      0xc
004B6077  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B607B  c6 06 00                 mov      byte ptr [esi], 0
004B607E  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B6084  8b c6                    mov      eax, esi
004B6086  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B6089  5e                       pop      esi
004B608A  5b                       pop      ebx
004B608B  c2 0c 00                 ret      0xc
004B608E  90                       nop      
004B608F  90                       nop      
004B6090  53                       push     ebx
004B6091  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B6095  8b c3                    mov      eax, ebx
004B6097  56                       push     esi
004B6098  25 ff 00 00 00           and      eax, 0xff
004B609D  8b f1                    mov      esi, ecx
004B609F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B60A6  51                       push     ecx
004B60A7  68 90 68 7d 00           push     0x7d6890
004B60AC  e8 3f 08 f5 ff           call     0x4068f0
004B60B1  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B60B5  83 c4 08                 add      esp, 8
004B60B8  85 c0                    test     eax, eax
004B60BA  7c 36                    jl       0x4b60f2
004B60BC  8a 4c 24 18              mov      cl, byte ptr [esp + 0x18]
004B60C0  88 46 02                 mov      byte ptr [esi + 2], al
004B60C3  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B60C7  8d 56 07                 lea      edx, [esi + 7]
004B60CA  88 1e                    mov      byte ptr [esi], bl
004B60CC  89 02                    mov      dword ptr [edx], eax
004B60CE  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004B60D2  88 4a 04                 mov      byte ptr [edx + 4], cl
004B60D5  8a 4c 24 20              mov      cl, byte ptr [esp + 0x20]
004B60D9  8d 56 0c                 lea      edx, [esi + 0xc]
004B60DC  89 46 0c                 mov      dword ptr [esi + 0xc], eax
004B60DF  8b c6                    mov      eax, esi
004B60E1  88 4a 04                 mov      byte ptr [edx + 4], cl
004B60E4  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B60EA  89 56 03                 mov      dword ptr [esi + 3], edx
004B60ED  5e                       pop      esi
004B60EE  5b                       pop      ebx
004B60EF  c2 18 00                 ret      0x18
004B60F2  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B60F6  c6 06 00                 mov      byte ptr [esi], 0
004B60F9  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B60FE  89 46 03                 mov      dword ptr [esi + 3], eax
004B6101  8b c6                    mov      eax, esi
004B6103  5e                       pop      esi
004B6104  5b                       pop      ebx
004B6105  c2 18 00                 ret      0x18
004B6108  90                       nop      
004B6109  90                       nop      
004B610A  90                       nop      
004B610B  90                       nop      
004B610C  90                       nop      
004B610D  90                       nop      
004B610E  90                       nop      
004B610F  90                       nop      
004B6110  56                       push     esi
004B6111  8b f1                    mov      esi, ecx
004B6113  68 a4 68 7d 00           push     0x7d68a4
004B6118  e8 d3 07 f5 ff           call     0x4068f0
004B611D  8b 44 24 0c              mov      eax, dword ptr [esp + 0xc]
004B6121  83 c4 04                 add      esp, 4
004B6124  85 c0                    test     eax, eax
004B6126  7c 32                    jl       0x4b615a
004B6128  8b 4c 24 10              mov      ecx, dword ptr [esp + 0x10]
004B612C  88 46 02                 mov      byte ptr [esi + 2], al
004B612F  8b 44 24 0c              mov      eax, dword ptr [esp + 0xc]
004B6133  c6 06 14                 mov      byte ptr [esi], 0x14
004B6136  89 46 07                 mov      dword ptr [esi + 7], eax
004B6139  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B613D  89 4e 0b                 mov      dword ptr [esi + 0xb], ecx
004B6140  8b 10                    mov      edx, dword ptr [eax]
004B6142  89 56 0f                 mov      dword ptr [esi + 0xf], edx
004B6145  8b 40 04                 mov      eax, dword ptr [eax + 4]
004B6148  89 46 13                 mov      dword ptr [esi + 0x13], eax
004B614B  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B6151  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B6154  8b c6                    mov      eax, esi
004B6156  5e                       pop      esi
004B6157  c2 10 00                 ret      0x10
004B615A  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B615E  c6 06 00                 mov      byte ptr [esi], 0
004B6161  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B6167  8b c6                    mov      eax, esi
004B6169  89 56 03                 mov      dword ptr [esi + 3], edx
004B616C  5e                       pop      esi
004B616D  c2 10 00                 ret      0x10
004B6170  8b c1                    mov      eax, ecx
004B6172  8b 4c 24 04              mov      ecx, dword ptr [esp + 4]
004B6176  85 c9                    test     ecx, ecx
004B6178  7c 60                    jl       0x4b61da
004B617A  8b 54 24 08              mov      edx, dword ptr [esp + 8]
004B617E  88 48 02                 mov      byte ptr [eax + 2], cl
004B6181  8d 48 07                 lea      ecx, [eax + 7]
004B6184  c6 00 04                 mov      byte ptr [eax], 4
004B6187  c6 40 1d 00              mov      byte ptr [eax + 0x1d], 0
004B618B  89 11                    mov      dword ptr [ecx], edx
004B618D  8a 54 24 0c              mov      dl, byte ptr [esp + 0xc]
004B6191  88 51 04                 mov      byte ptr [ecx + 4], dl
004B6194  8a 4c 24 10              mov      cl, byte ptr [esp + 0x10]
004B6198  88 48 0c                 mov      byte ptr [eax + 0xc], cl
004B619B  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
004B619F  8d 50 0e                 lea      edx, [eax + 0xe]
004B61A2  89 48 0e                 mov      dword ptr [eax + 0xe], ecx
004B61A5  8a 4c 24 18              mov      cl, byte ptr [esp + 0x18]
004B61A9  88 4a 04                 mov      byte ptr [edx + 4], cl
004B61AC  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
004B61B0  8d 50 13                 lea      edx, [eax + 0x13]
004B61B3  89 48 13                 mov      dword ptr [eax + 0x13], ecx
004B61B6  8a 4c 24 20              mov      cl, byte ptr [esp + 0x20]
004B61BA  88 4a 04                 mov      byte ptr [edx + 4], cl
004B61BD  8b 4c 24 24              mov      ecx, dword ptr [esp + 0x24]
004B61C1  8d 50 18                 lea      edx, [eax + 0x18]
004B61C4  89 48 18                 mov      dword ptr [eax + 0x18], ecx
004B61C7  8a 4c 24 28              mov      cl, byte ptr [esp + 0x28]
004B61CB  88 4a 04                 mov      byte ptr [edx + 4], cl
004B61CE  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B61D4  89 50 03                 mov      dword ptr [eax + 3], edx
004B61D7  c2 28 00                 ret      0x28
004B61DA  c6 40 02 ff              mov      byte ptr [eax + 2], 0xff
004B61DE  c6 00 00                 mov      byte ptr [eax], 0
004B61E1  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B61E7  89 48 03                 mov      dword ptr [eax + 3], ecx
004B61EA  c2 28 00                 ret      0x28
004B61ED  90                       nop      
004B61EE  90                       nop      
004B61EF  90                       nop      
004B61F0  56                       push     esi
004B61F1  8b f1                    mov      esi, ecx
004B61F3  68 bc 68 7d 00           push     0x7d68bc
004B61F8  e8 f3 06 f5 ff           call     0x4068f0
004B61FD  8b 44 24 0c              mov      eax, dword ptr [esp + 0xc]
004B6201  83 c4 04                 add      esp, 4
004B6204  85 c0                    test     eax, eax
004B6206  7c 5a                    jl       0x4b6262
004B6208  8b 4c 24 0c              mov      ecx, dword ptr [esp + 0xc]
004B620C  8a 54 24 10              mov      dl, byte ptr [esp + 0x10]
004B6210  88 46 02                 mov      byte ptr [esi + 2], al
004B6213  8d 46 07                 lea      eax, [esi + 7]
004B6216  c6 06 05                 mov      byte ptr [esi], 5
004B6219  89 08                    mov      dword ptr [eax], ecx
004B621B  8d 4e 0d                 lea      ecx, [esi + 0xd]
004B621E  88 50 04                 mov      byte ptr [eax + 4], dl
004B6221  8a 44 24 14              mov      al, byte ptr [esp + 0x14]
004B6225  8b 54 24 18              mov      edx, dword ptr [esp + 0x18]
004B6229  88 46 0c                 mov      byte ptr [esi + 0xc], al
004B622C  8a 44 24 1c              mov      al, byte ptr [esp + 0x1c]
004B6230  89 11                    mov      dword ptr [ecx], edx
004B6232  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004B6236  88 41 04                 mov      byte ptr [ecx + 4], al
004B6239  8a 44 24 24              mov      al, byte ptr [esp + 0x24]
004B623D  8d 4e 12                 lea      ecx, [esi + 0x12]
004B6240  89 56 12                 mov      dword ptr [esi + 0x12], edx
004B6243  8b 54 24 2c              mov      edx, dword ptr [esp + 0x2c]
004B6247  89 56 1b                 mov      dword ptr [esi + 0x1b], edx
004B624A  88 41 04                 mov      byte ptr [ecx + 4], al
004B624D  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
004B6251  89 4e 17                 mov      dword ptr [esi + 0x17], ecx
004B6254  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B6259  89 46 03                 mov      dword ptr [esi + 3], eax
004B625C  8b c6                    mov      eax, esi
004B625E  5e                       pop      esi
004B625F  c2 28 00                 ret      0x28
004B6262  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B6266  c6 06 00                 mov      byte ptr [esi], 0
004B6269  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B626F  8b c6                    mov      eax, esi
004B6271  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B6274  5e                       pop      esi
004B6275  c2 28 00                 ret      0x28
004B6278  90                       nop      
004B6279  90                       nop      
004B627A  90                       nop      
004B627B  90                       nop      
004B627C  90                       nop      
004B627D  90                       nop      
004B627E  90                       nop      
004B627F  90                       nop      
004B6280  53                       push     ebx
004B6281  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B6285  8b c3                    mov      eax, ebx
004B6287  56                       push     esi
004B6288  25 ff 00 00 00           and      eax, 0xff
004B628D  8b f1                    mov      esi, ecx
004B628F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6296  51                       push     ecx
004B6297  68 90 68 7d 00           push     0x7d6890
004B629C  e8 4f 06 f5 ff           call     0x4068f0
004B62A1  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B62A5  83 c4 08                 add      esp, 8
004B62A8  85 c0                    test     eax, eax
004B62AA  7c 2a                    jl       0x4b62d6
004B62AC  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B62B0  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
004B62B4  88 46 02                 mov      byte ptr [esi + 2], al
004B62B7  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B62BB  88 1e                    mov      byte ptr [esi], bl
004B62BD  89 56 07                 mov      dword ptr [esi + 7], edx
004B62C0  89 46 0b                 mov      dword ptr [esi + 0xb], eax
004B62C3  89 4e 0f                 mov      dword ptr [esi + 0xf], ecx
004B62C6  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B62CC  8b c6                    mov      eax, esi
004B62CE  89 56 03                 mov      dword ptr [esi + 3], edx
004B62D1  5e                       pop      esi
004B62D2  5b                       pop      ebx
004B62D3  c2 14 00                 ret      0x14
004B62D6  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B62DA  c6 06 00                 mov      byte ptr [esi], 0
004B62DD  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B62E2  89 46 03                 mov      dword ptr [esi + 3], eax
004B62E5  8b c6                    mov      eax, esi
004B62E7  5e                       pop      esi
004B62E8  5b                       pop      ebx
004B62E9  c2 14 00                 ret      0x14
004B62EC  90                       nop      
004B62ED  90                       nop      
004B62EE  90                       nop      
004B62EF  90                       nop      
004B62F0  53                       push     ebx
004B62F1  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B62F5  8b c3                    mov      eax, ebx
004B62F7  56                       push     esi
004B62F8  25 ff 00 00 00           and      eax, 0xff
004B62FD  8b f1                    mov      esi, ecx
004B62FF  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6306  51                       push     ecx
004B6307  68 90 68 7d 00           push     0x7d6890
004B630C  e8 df 05 f5 ff           call     0x4068f0
004B6311  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6315  83 c4 08                 add      esp, 8
004B6318  85 c0                    test     eax, eax
004B631A  7c 3c                    jl       0x4b6358
004B631C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B6320  88 46 02                 mov      byte ptr [esi + 2], al
004B6323  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B6327  88 1e                    mov      byte ptr [esi], bl
004B6329  89 56 07                 mov      dword ptr [esi + 7], edx
004B632C  c7 46 0b ff ff ff ff     mov      dword ptr [esi + 0xb], 0xffffffff
004B6333  c7 46 0f 00 00 00 00     mov      dword ptr [esi + 0xf], 0
004B633A  66 8b 08                 mov      cx, word ptr [eax]
004B633D  66 89 4e 13              mov      word ptr [esi + 0x13], cx
004B6341  66 8b 50 02              mov      dx, word ptr [eax + 2]
004B6345  66 89 56 15              mov      word ptr [esi + 0x15], dx
004B6349  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B634E  89 46 03                 mov      dword ptr [esi + 3], eax
004B6351  8b c6                    mov      eax, esi
004B6353  5e                       pop      esi
004B6354  5b                       pop      ebx
004B6355  c2 10 00                 ret      0x10
004B6358  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B635C  c6 06 00                 mov      byte ptr [esi], 0
004B635F  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B6365  8b c6                    mov      eax, esi
004B6367  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B636A  5e                       pop      esi
004B636B  5b                       pop      ebx
004B636C  c2 10 00                 ret      0x10
004B636F  90                       nop      
004B6370  53                       push     ebx
004B6371  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B6375  8b c3                    mov      eax, ebx
004B6377  56                       push     esi
004B6378  25 ff 00 00 00           and      eax, 0xff
004B637D  8b f1                    mov      esi, ecx
004B637F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6386  51                       push     ecx
004B6387  68 90 68 7d 00           push     0x7d6890
004B638C  e8 5f 05 f5 ff           call     0x4068f0
004B6391  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6395  83 c4 08                 add      esp, 8
004B6398  85 c0                    test     eax, eax
004B639A  7c 3c                    jl       0x4b63d8
004B639C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B63A0  88 46 02                 mov      byte ptr [esi + 2], al
004B63A3  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B63A7  88 1e                    mov      byte ptr [esi], bl
004B63A9  89 46 0b                 mov      dword ptr [esi + 0xb], eax
004B63AC  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004B63B0  89 56 07                 mov      dword ptr [esi + 7], edx
004B63B3  c7 46 0f 00 00 00 00     mov      dword ptr [esi + 0xf], 0
004B63BA  66 8b 08                 mov      cx, word ptr [eax]
004B63BD  66 89 4e 13              mov      word ptr [esi + 0x13], cx
004B63C1  66 8b 50 02              mov      dx, word ptr [eax + 2]
004B63C5  66 89 56 15              mov      word ptr [esi + 0x15], dx
004B63C9  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B63CE  89 46 03                 mov      dword ptr [esi + 3], eax
004B63D1  8b c6                    mov      eax, esi
004B63D3  5e                       pop      esi
004B63D4  5b                       pop      ebx
004B63D5  c2 14 00                 ret      0x14
004B63D8  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B63DC  c6 06 00                 mov      byte ptr [esi], 0
004B63DF  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B63E5  8b c6                    mov      eax, esi
004B63E7  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B63EA  5e                       pop      esi
004B63EB  5b                       pop      ebx
004B63EC  c2 14 00                 ret      0x14
004B63EF  90                       nop      
004B63F0  53                       push     ebx
004B63F1  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B63F5  8b c3                    mov      eax, ebx
004B63F7  56                       push     esi
004B63F8  25 ff 00 00 00           and      eax, 0xff
004B63FD  8b f1                    mov      esi, ecx
004B63FF  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6406  51                       push     ecx
004B6407  68 90 68 7d 00           push     0x7d6890
004B640C  e8 df 04 f5 ff           call     0x4068f0
004B6411  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6415  83 c4 08                 add      esp, 8
004B6418  85 c0                    test     eax, eax
004B641A  7c 3d                    jl       0x4b6459
004B641C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B6420  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
004B6424  88 46 02                 mov      byte ptr [esi + 2], al
004B6427  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B642B  89 46 0b                 mov      dword ptr [esi + 0xb], eax
004B642E  8b 44 24 20              mov      eax, dword ptr [esp + 0x20]
004B6432  88 1e                    mov      byte ptr [esi], bl
004B6434  89 56 07                 mov      dword ptr [esi + 7], edx
004B6437  89 4e 0f                 mov      dword ptr [esi + 0xf], ecx
004B643A  66 8b 10                 mov      dx, word ptr [eax]
004B643D  66 89 56 13              mov      word ptr [esi + 0x13], dx
004B6441  66 8b 40 02              mov      ax, word ptr [eax + 2]
004B6445  66 89 46 15              mov      word ptr [esi + 0x15], ax
004B6449  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B644F  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B6452  8b c6                    mov      eax, esi
004B6454  5e                       pop      esi
004B6455  5b                       pop      ebx
004B6456  c2 18 00                 ret      0x18
004B6459  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B645D  c6 06 00                 mov      byte ptr [esi], 0
004B6460  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B6466  8b c6                    mov      eax, esi
004B6468  89 56 03                 mov      dword ptr [esi + 3], edx
004B646B  5e                       pop      esi
004B646C  5b                       pop      ebx
004B646D  c2 18 00                 ret      0x18
004B6470  53                       push     ebx
004B6471  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B6475  8b c3                    mov      eax, ebx
004B6477  56                       push     esi
004B6478  25 ff 00 00 00           and      eax, 0xff
004B647D  8b f1                    mov      esi, ecx
004B647F  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6486  51                       push     ecx
004B6487  68 90 68 7d 00           push     0x7d6890
004B648C  e8 5f 04 f5 ff           call     0x4068f0
004B6491  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6495  83 c4 08                 add      esp, 8
004B6498  85 c0                    test     eax, eax
004B649A  7c 2e                    jl       0x4b64ca
004B649C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B64A0  88 46 02                 mov      byte ptr [esi + 2], al
004B64A3  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B64A7  88 1e                    mov      byte ptr [esi], bl
004B64A9  89 56 07                 mov      dword ptr [esi + 7], edx
004B64AC  66 8b 08                 mov      cx, word ptr [eax]
004B64AF  66 89 4e 0b              mov      word ptr [esi + 0xb], cx
004B64B3  66 8b 50 02              mov      dx, word ptr [eax + 2]
004B64B7  66 89 56 0d              mov      word ptr [esi + 0xd], dx
004B64BB  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004B64C0  89 46 03                 mov      dword ptr [esi + 3], eax
004B64C3  8b c6                    mov      eax, esi
004B64C5  5e                       pop      esi
004B64C6  5b                       pop      ebx
004B64C7  c2 10 00                 ret      0x10
004B64CA  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B64CE  c6 06 00                 mov      byte ptr [esi], 0
004B64D1  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B64D7  8b c6                    mov      eax, esi
004B64D9  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B64DC  5e                       pop      esi
004B64DD  5b                       pop      ebx
004B64DE  c2 10 00                 ret      0x10
004B64E1  90                       nop      
004B64E2  90                       nop      
004B64E3  90                       nop      
004B64E4  90                       nop      
004B64E5  90                       nop      
004B64E6  90                       nop      
004B64E7  90                       nop      
004B64E8  90                       nop      
004B64E9  90                       nop      
004B64EA  90                       nop      
004B64EB  90                       nop      
004B64EC  90                       nop      
004B64ED  90                       nop      
004B64EE  90                       nop      
004B64EF  90                       nop      
004B64F0  53                       push     ebx
004B64F1  8b 5c 24 0c              mov      ebx, dword ptr [esp + 0xc]
004B64F5  8b c3                    mov      eax, ebx
004B64F7  56                       push     esi
004B64F8  25 ff 00 00 00           and      eax, 0xff
004B64FD  8b f1                    mov      esi, ecx
004B64FF  8b 0c 85 cc 65 7d 00     mov      ecx, dword ptr [eax*4 + 0x7d65cc]
004B6506  51                       push     ecx
004B6507  68 90 68 7d 00           push     0x7d6890
004B650C  e8 df 03 f5 ff           call     0x4068f0
004B6511  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004B6515  83 c4 08                 add      esp, 8
004B6518  85 c0                    test     eax, eax
004B651A  7c 23                    jl       0x4b653f
004B651C  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004B6520  88 46 02                 mov      byte ptr [esi + 2], al
004B6523  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004B6527  88 1e                    mov      byte ptr [esi], bl
004B6529  89 56 07                 mov      dword ptr [esi + 7], edx
004B652C  89 46 0b                 mov      dword ptr [esi + 0xb], eax
004B652F  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B6535  8b c6                    mov      eax, esi
004B6537  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B653A  5e                       pop      esi
004B653B  5b                       pop      ebx
004B653C  c2 10 00                 ret      0x10
004B653F  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B6543  c6 06 00                 mov      byte ptr [esi], 0
004B6546  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B654C  8b c6                    mov      eax, esi
004B654E  89 56 03                 mov      dword ptr [esi + 3], edx
004B6551  5e                       pop      esi
004B6552  5b                       pop      ebx
004B6553  c2 10 00                 ret      0x10
004B6556  90                       nop      
004B6557  90                       nop      
004B6558  90                       nop      
004B6559  90                       nop      
004B655A  90                       nop      
004B655B  90                       nop      
004B655C  90                       nop      
004B655D  90                       nop      
004B655E  90                       nop      
004B655F  90                       nop      
004B6560  8b 44 24 04              mov      eax, dword ptr [esp + 4]
004B6564  83 ec 08                 sub      esp, 8
004B6567  85 c0                    test     eax, eax
004B6569  56                       push     esi
004B656A  8b f1                    mov      esi, ecx
004B656C  7c 39                    jl       0x4b65a7
004B656E  88 46 02                 mov      byte ptr [esi + 2], al
004B6571  8d 44 24 04              lea      eax, [esp + 4]
004B6575  8d 4c 24 10              lea      ecx, [esp + 0x10]
004B6579  50                       push     eax
004B657A  51                       push     ecx
004B657B  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
004B657F  c6 06 29                 mov      byte ptr [esi], 0x29
004B6582  e8 79 cf 06 00           call     0x523500
004B6587  8b 54 24 04              mov      edx, dword ptr [esp + 4]
004B658B  8a 44 24 18              mov      al, byte ptr [esp + 0x18]
004B658F  89 56 08                 mov      dword ptr [esi + 8], edx
004B6592  88 46 07                 mov      byte ptr [esi + 7], al
004B6595  8b 0d 2c 0d a4 00        mov      ecx, dword ptr [0xa40d2c]
004B659B  8b c6                    mov      eax, esi
004B659D  89 4e 03                 mov      dword ptr [esi + 3], ecx
004B65A0  5e                       pop      esi
004B65A1  83 c4 08                 add      esp, 8
004B65A4  c2 0c 00                 ret      0xc
004B65A7  c6 46 02 ff              mov      byte ptr [esi + 2], 0xff
004B65AB  c6 06 00                 mov      byte ptr [esi], 0
004B65AE  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
004B65B4  8b c6                    mov      eax, esi
004B65B6  89 56 03                 mov      dword ptr [esi + 3], edx
004B65B9  5e                       pop      esi
004B65BA  83 c4 08                 add      esp, 8
004B65BD  c2 0c 00                 ret      0xc
004B65C0  81 ec 70 03 00 00        sub      esp, 0x370
004B65C6  33 c0                    xor      eax, eax
004B65C8  53                       push     ebx
004B65C9  55                       push     ebp
004B65CA  56                       push     esi
004B65CB  8b f1                    mov      esi, ecx
