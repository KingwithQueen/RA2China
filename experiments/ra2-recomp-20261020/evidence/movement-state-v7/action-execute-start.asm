
sub_006B2FA0 0x006B3000 size=256
006B3000  5e                       pop      esi
006B3001  5d                       pop      ebp
006B3002  b0 01                    mov      al, 1
006B3004  5b                       pop      ebx
006B3005  c2 10 00                 ret      0x10
006B3008  90                       nop      
006B3009  90                       nop      
006B300A  90                       nop      
006B300B  90                       nop      
006B300C  90                       nop      
006B300D  90                       nop      
006B300E  90                       nop      
006B300F  90                       nop      
006B3010  56                       push     esi
006B3011  8b 71 74                 mov      esi, dword ptr [ecx + 0x74]
006B3014  83 fe 04                 cmp      esi, 4
006B3017  7d 35                    jge      0x6b304e
006B3019  85 f6                    test     esi, esi
006B301B  7c 31                    jl       0x6b304e
006B301D  8b c6                    mov      eax, esi
006B301F  c1 e0 04                 shl      eax, 4
006B3022  03 c6                    add      eax, esi
006B3024  8d 04 c0                 lea      eax, [eax + eax*8]
006B3027  8d 04 46                 lea      eax, [esi + eax*2]
006B302A  8d 0c 40                 lea      ecx, [eax + eax*2]
006B302D  8d 0c 8d 20 3a 83 00     lea      ecx, [ecx*4 + 0x833a20]
006B3034  e8 f7 e6 fc ff           call     0x681730
006B3039  84 c0                    test     al, al
006B303B  74 11                    je       0x6b304e
006B303D  56                       push     esi
006B303E  b9 e0 24 83 00           mov      ecx, 0x8324e0
006B3043  e8 48 a9 fc ff           call     0x67d990
006B3048  b0 01                    mov      al, 1
006B304A  5e                       pop      esi
006B304B  c2 10 00                 ret      0x10
006B304E  32 c0                    xor      al, al
006B3050  5e                       pop      esi
006B3051  c2 10 00                 ret      0x10
006B3054  90                       nop      
006B3055  90                       nop      
006B3056  90                       nop      
006B3057  90                       nop      
006B3058  90                       nop      
006B3059  90                       nop      
006B305A  90                       nop      
006B305B  90                       nop      
006B305C  90                       nop      
006B305D  90                       nop      
006B305E  90                       nop      
006B305F  90                       nop      
006B3060  8b 41 74                 mov      eax, dword ptr [ecx + 0x74]
006B3063  8b 15 c8 0a a4 00        mov      edx, dword ptr [0xa40ac8]
006B3069  3b c2                    cmp      eax, edx
006B306B  7d 21                    jge      0x6b308e
006B306D  85 c0                    test     eax, eax
006B306F  7c 1d                    jl       0x6b308e
006B3071  8b 15 bc 0a a4 00        mov      edx, dword ptr [0xa40abc]
006B3077  8b 49 48                 mov      ecx, dword ptr [ecx + 0x48]
006B307A  51                       push     ecx
006B307B  b9 e0 24 83 00           mov      ecx, 0x8324e0
006B3080  8b 04 82                 mov      eax, dword ptr [edx + eax*4]
006B3083  50                       push     eax
006B3084  e8 27 f2 fc ff           call     0x6822b0
006B3089  b0 01                    mov      al, 1
006B308B  c2 10 00                 ret      0x10
006B308E  32 c0                    xor      al, al
006B3090  c2 10 00                 ret      0x10
006B3093  90                       nop      
006B3094  90                       nop      
006B3095  90                       nop      
006B3096  90                       nop      
006B3097  90                       nop      
006B3098  90                       nop      
006B3099  90                       nop      
006B309A  90                       nop      
006B309B  90                       nop      
006B309C  90                       nop      
006B309D  90                       nop      
006B309E  90                       nop      
006B309F  90                       nop      
006B30A0  b8 78 00 00 00           mov      eax, 0x78
006B30A5  c3                       ret      
006B30A6  90                       nop      
006B30A7  90                       nop      
006B30A8  90                       nop      
006B30A9  90                       nop      
006B30AA  90                       nop      
006B30AB  90                       nop      
006B30AC  90                       nop      
006B30AD  90                       nop      
006B30AE  90                       nop      
006B30AF  90                       nop      
006B30B0  b8 2f 00 00 00           mov      eax, 0x2f
006B30B5  c3                       ret      
006B30B6  90                       nop      
006B30B7  90                       nop      
006B30B8  90                       nop      
006B30B9  90                       nop      
006B30BA  90                       nop      
006B30BB  90                       nop      
006B30BC  90                       nop      
006B30BD  90                       nop      
006B30BE  90                       nop      
006B30BF  90                       nop      
006B30C0  8b 41 24                 mov      eax, dword ptr [ecx + 0x24]
006B30C3  c3                       ret      
006B30C4  90                       nop      
006B30C5  90                       nop      
006B30C6  90                       nop      
006B30C7  90                       nop      
006B30C8  90                       nop      
006B30C9  90                       nop      
006B30CA  90                       nop      
006B30CB  90                       nop      
006B30CC  90                       nop      
006B30CD  90                       nop      
006B30CE  90                       nop      
006B30CF  90                       nop      
006B30D0  51                       push     ecx
006B30D1  56                       push     esi
006B30D2  8b f1                    mov      esi, ecx
006B30D4  b2 01                    mov      dl, 1
006B30D6  c7 06 5c c6 7a 00        mov      dword ptr [esi], 0x7ac65c
006B30DC  c7 46 04 40 c6 7a 00     mov      dword ptr [esi + 4], 0x7ac640
006B30E3  c7 46 08 38 c6 7a 00     mov      dword ptr [esi + 8], 0x7ac638
006B30EA  c7 46 0c 30 c6 7a 00     mov      dword ptr [esi + 0xc], 0x7ac630
006B30F1  e8 9a 9a 03 00           call     0x6ecb90
006B30F6  8b 15 b0 0c ac 00        mov      edx, dword ptr [0xac0cb0]
006B30FC  8d 44 24 04              lea      eax, [esp + 4]
