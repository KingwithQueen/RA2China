
sub_004A2670 0x004A2670 size=8373
004A2670  83 ec 4c                 sub      esp, 0x4c
004A2673  53                       push     ebx
004A2674  55                       push     ebp
004A2675  8b e9                    mov      ebp, ecx
004A2677  56                       push     esi
004A2678  8b 4d 04                 mov      ecx, dword ptr [ebp + 4]
004A267B  57                       push     edi
004A267C  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A267F  8b 98 d0 04 00 00        mov      ebx, dword ptr [eax + 0x4d0]
004A2685  8d 45 04                 lea      eax, [ebp + 4]
004A2688  50                       push     eax
004A2689  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004A268D  ff 51 10                 call     dword ptr [ecx + 0x10]
004A2690  84 c0                    test     al, al
004A2692  75 7c                    jne      0x4a2710
004A2694  83 fb ff                 cmp      ebx, -1
004A2697  75 77                    jne      0x4a2710
004A2699  88 45 61                 mov      byte ptr [ebp + 0x61], al
004A269C  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A26A1  39 45 40                 cmp      dword ptr [ebp + 0x40], eax
004A26A4  75 1a                    jne      0x4a26c0
004A26A6  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A26A9  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A26AF  3b d1                    cmp      edx, ecx
004A26B1  75 0d                    jne      0x4a26c0
004A26B3  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A26B6  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A26BC  3b ca                    cmp      ecx, edx
004A26BE  74 18                    je       0x4a26d8
004A26C0  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A26C3  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A26C9  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A26CC  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A26D1  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A26D4  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A26D8  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A26DB  8b 11                    mov      edx, dword ptr [ecx]
004A26DD  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A26E3  83 f8 02                 cmp      eax, 2
004A26E6  0f 85 58 13 00 00        jne      0x4a3a44
004A26EC  8b 6d 0c                 mov      ebp, dword ptr [ebp + 0xc]
004A26EF  6a 01                    push     1
004A26F1  6a 00                    push     0
004A26F3  8b cd                    mov      ecx, ebp
004A26F5  8b 45 00                 mov      eax, dword ptr [ebp]
004A26F8  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A26FE  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
004A2702  5f                       pop      edi
004A2703  5e                       pop      esi
004A2704  5d                       pop      ebp
004A2705  88 01                    mov      byte ptr [ecx], al
004A2707  32 c0                    xor      al, al
004A2709  5b                       pop      ebx
004A270A  83 c4 4c                 add      esp, 0x4c
004A270D  c2 0c 00                 ret      0xc
004A2710  8b 55 34                 mov      edx, dword ptr [ebp + 0x34]
004A2713  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2718  8d 7d 34                 lea      edi, [ebp + 0x34]
004A271B  3b d0                    cmp      edx, eax
004A271D  75 1d                    jne      0x4a273c
004A271F  8b 47 04                 mov      eax, dword ptr [edi + 4]
004A2722  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A2728  3b c1                    cmp      eax, ecx
004A272A  75 10                    jne      0x4a273c
004A272C  8b 4f 08                 mov      ecx, dword ptr [edi + 8]
004A272F  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A2734  3b c8                    cmp      ecx, eax
004A2736  0f 84 08 13 00 00        je       0x4a3a44
004A273C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A273F  8b 11                    mov      edx, dword ptr [ecx]
004A2741  ff 92 bc 01 00 00        call     dword ptr [edx + 0x1bc]
004A2747  84 c0                    test     al, al
004A2749  0f 85 f5 12 00 00        jne      0x4a3a44
004A274F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2752  8b 01                    mov      eax, dword ptr [ecx]
004A2754  ff 90 c0 01 00 00        call     dword ptr [eax + 0x1c0]
004A275A  84 c0                    test     al, al
004A275C  0f 85 e2 12 00 00        jne      0x4a3a44
004A2762  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2765  8b 89 38 02 00 00        mov      ecx, dword ptr [ecx + 0x238]
004A276B  85 c9                    test     ecx, ecx
004A276D  74 15                    je       0x4a2784
004A276F  e8 0c 7f 1e 00           call     0x68a680
004A2774  85 c0                    test     eax, eax
004A2776  74 0c                    je       0x4a2784
004A2778  5f                       pop      edi
004A2779  5e                       pop      esi
004A277A  5d                       pop      ebp
004A277B  b0 01                    mov      al, 1
004A277D  5b                       pop      ebx
004A277E  83 c4 4c                 add      esp, 0x4c
004A2781  c2 0c 00                 ret      0xc
004A2784  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2787  8b 11                    mov      edx, dword ptr [ecx]
004A2789  ff 92 24 03 00 00        call     dword ptr [edx + 0x324]
004A278F  84 c0                    test     al, al
004A2791  0f 85 ee 1b 00 00        jne      0x4a4385
004A2797  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A279A  8b 01                    mov      eax, dword ptr [ecx]
004A279C  ff 90 28 03 00 00        call     dword ptr [eax + 0x328]
004A27A2  84 c0                    test     al, al
004A27A4  0f 85 db 1b 00 00        jne      0x4a4385
004A27AA  83 fb ff                 cmp      ebx, -1
004A27AD  0f 84 ab 00 00 00        je       0x4a285e
004A27B3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A27B6  8b 89 94 04 00 00        mov      ecx, dword ptr [ecx + 0x494]
004A27BC  85 c9                    test     ecx, ecx
004A27BE  74 0a                    je       0x4a27ca
004A27C0  8b 11                    mov      edx, dword ptr [ecx]
004A27C2  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A27C5  83 f8 01                 cmp      eax, 1
004A27C8  74 17                    je       0x4a27e1
004A27CA  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A27CD  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A27D3  85 c9                    test     ecx, ecx
004A27D5  74 7e                    je       0x4a2855
004A27D7  8b 11                    mov      edx, dword ptr [ecx]
004A27D9  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A27DC  83 f8 0f                 cmp      eax, 0xf
004A27DF  75 74                    jne      0x4a2855
004A27E1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A27E4  8d 54 24 44              lea      edx, [esp + 0x44]
004A27E8  52                       push     edx
004A27E9  8b 01                    mov      eax, dword ptr [ecx]
004A27EB  ff 50 48                 call     dword ptr [eax + 0x48]
004A27EE  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A27F1  8b 77 08                 mov      esi, dword ptr [edi + 8]
004A27F4  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A27F7  8b 00                    mov      eax, dword ptr [eax]
004A27F9  2b ce                    sub      ecx, esi
004A27FB  8b 77 04                 mov      esi, dword ptr [edi + 4]
004A27FE  2b d6                    sub      edx, esi
004A2800  8b 37                    mov      esi, dword ptr [edi]
004A2802  51                       push     ecx
004A2803  2b c6                    sub      eax, esi
004A2805  52                       push     edx
004A2806  50                       push     eax
004A2807  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A280B  e8 20 8e f7 ff           call     0x41b630
004A2810  8b 08                    mov      ecx, dword ptr [eax]
004A2812  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A2816  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A281A  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A281D  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A2821  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A2824  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A2828  e8 53 8f f7 ff           call     0x41b780
004A282D  99                       cdq      
004A282E  81 e2 ff 00 00 00        and      edx, 0xff
004A2834  03 c2                    add      eax, edx
004A2836  c1 f8 08                 sar      eax, 8
004A2839  83 f8 18                 cmp      eax, 0x18
004A283C  7d 17                    jge      0x4a2855
004A283E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2841  c7 84 81 d0 04 00 00 ff ff ff ff mov      dword ptr [ecx + eax*4 + 0x4d0], 0xffffffff
004A284C  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A284F  8b 9a d0 04 00 00        mov      ebx, dword ptr [edx + 0x4d0]
004A2855  83 fb ff                 cmp      ebx, -1
004A2858  0f 85 6c 0a 00 00        jne      0x4a32ca
004A285E  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2861  8b 1d 2c 0d a4 00        mov      ebx, dword ptr [0xa40d2c]
004A2867  8b 90 30 05 00 00        mov      edx, dword ptr [eax + 0x530]
004A286D  8d b0 30 05 00 00        lea      esi, [eax + 0x530]
004A2873  83 fa ff                 cmp      edx, -1
004A2876  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A2879  74 0a                    je       0x4a2885
004A287B  8b cb                    mov      ecx, ebx
004A287D  2b ca                    sub      ecx, edx
004A287F  3b c8                    cmp      ecx, eax
004A2881  7d 0a                    jge      0x4a288d
004A2883  2b c1                    sub      eax, ecx
004A2885  85 c0                    test     eax, eax
004A2887  0f 85 b7 11 00 00        jne      0x4a3a44
004A288D  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A2892  dd 80 c8 13 00 00        fld      qword ptr [eax + 0x13c8]
004A2898  dc 0d 08 b6 79 00        fmul     qword ptr [0x79b608]
004A289E  e8 6d c8 2d 00           call     0x77f110
004A28A3  8b 4c 24 48              mov      ecx, dword ptr [esp + 0x48]
004A28A7  89 1e                    mov      dword ptr [esi], ebx
004A28A9  89 4e 04                 mov      dword ptr [esi + 4], ecx
004A28AC  89 46 08                 mov      dword ptr [esi + 8], eax
004A28AF  8b 07                    mov      eax, dword ptr [edi]
004A28B1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A28B4  99                       cdq      
004A28B5  81 e2 ff 00 00 00        and      edx, 0xff
004A28BB  6a 00                    push     0
004A28BD  03 c2                    add      eax, edx
004A28BF  6a 00                    push     0
004A28C1  c1 f8 08                 sar      eax, 8
004A28C4  66 89 44 24 20           mov      word ptr [esp + 0x20], ax
004A28C9  8b 47 04                 mov      eax, dword ptr [edi + 4]
004A28CC  99                       cdq      
004A28CD  81 e2 ff 00 00 00        and      edx, 0xff
004A28D3  03 c2                    add      eax, edx
004A28D5  c1 f8 08                 sar      eax, 8
004A28D8  66 89 44 24 22           mov      word ptr [esp + 0x22], ax
004A28DD  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004A28E1  52                       push     edx
004A28E2  e8 19 07 02 00           call     0x4c3000
004A28E7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A28EA  84 c0                    test     al, al
004A28EC  0f 85 88 06 00 00        jne      0x4a2f7a
004A28F2  85 c9                    test     ecx, ecx
004A28F4  75 13                    jne      0x4a2909
004A28F6  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
004A28FA  5f                       pop      edi
004A28FB  5e                       pop      esi
004A28FC  5d                       pop      ebp
004A28FD  c6 00 01                 mov      byte ptr [eax], 1
004A2900  32 c0                    xor      al, al
004A2902  5b                       pop      ebx
004A2903  83 c4 4c                 add      esp, 0x4c
004A2906  c2 0c 00                 ret      0xc
004A2909  8b 11                    mov      edx, dword ptr [ecx]
004A290B  57                       push     edi
004A290C  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004A2912  84 c0                    test     al, al
004A2914  75 1e                    jne      0x4a2934
004A2916  8b 6d 0c                 mov      ebp, dword ptr [ebp + 0xc]
004A2919  6a 01                    push     1
004A291B  6a 00                    push     0
004A291D  8b cd                    mov      ecx, ebp
004A291F  8b 45 00                 mov      eax, dword ptr [ebp]
004A2922  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A2928  5f                       pop      edi
004A2929  5e                       pop      esi
004A292A  5d                       pop      ebp
004A292B  32 c0                    xor      al, al
004A292D  5b                       pop      ebx
004A292E  83 c4 4c                 add      esp, 0x4c
004A2931  c2 0c 00                 ret      0xc
004A2934  8b 0f                    mov      ecx, dword ptr [edi]
004A2936  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A293B  3b c8                    cmp      ecx, eax
004A293D  75 1d                    jne      0x4a295c
004A293F  8b 57 04                 mov      edx, dword ptr [edi + 4]
004A2942  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A2947  3b d0                    cmp      edx, eax
004A2949  75 11                    jne      0x4a295c
004A294B  8b 47 08                 mov      eax, dword ptr [edi + 8]
004A294E  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2954  3b c1                    cmp      eax, ecx
004A2956  0f 84 e8 10 00 00        je       0x4a3a44
004A295C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A295F  e8 fc 63 02 00           call     0x4c8d60
004A2964  84 c0                    test     al, al
004A2966  0f 85 17 01 00 00        jne      0x4a2a83
004A296C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A296F  8d 44 24 44              lea      eax, [esp + 0x44]
004A2973  50                       push     eax
004A2974  8b 11                    mov      edx, dword ptr [ecx]
004A2976  ff 52 48                 call     dword ptr [edx + 0x48]
004A2979  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A297C  8b 57 08                 mov      edx, dword ptr [edi + 8]
004A297F  8b 77 04                 mov      esi, dword ptr [edi + 4]
004A2982  8b 1f                    mov      ebx, dword ptr [edi]
004A2984  2b ca                    sub      ecx, edx
004A2986  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A2989  8b 00                    mov      eax, dword ptr [eax]
004A298B  2b d6                    sub      edx, esi
004A298D  51                       push     ecx
004A298E  2b c3                    sub      eax, ebx
004A2990  52                       push     edx
004A2991  50                       push     eax
004A2992  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A2996  e8 95 8c f7 ff           call     0x41b630
004A299B  8b 08                    mov      ecx, dword ptr [eax]
004A299D  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A29A1  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A29A5  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A29A8  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A29AC  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A29AF  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A29B3  e8 c8 8d f7 ff           call     0x41b780
004A29B8  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A29BE  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A29C4  0f 8d b9 00 00 00        jge      0x4a2a83
004A29CA  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A29CD  8b 11                    mov      edx, dword ptr [ecx]
004A29CF  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A29D5  83 f8 02                 cmp      eax, 2
004A29D8  74 14                    je       0x4a29ee
004A29DA  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A29DD  8b 01                    mov      eax, dword ptr [ecx]
004A29DF  ff 90 6c 01 00 00        call     dword ptr [eax + 0x16c]
004A29E5  83 f8 0b                 cmp      eax, 0xb
004A29E8  0f 85 95 00 00 00        jne      0x4a2a83
004A29EE  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A29F3  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A29F6  3b c8                    cmp      ecx, eax
004A29F8  75 1a                    jne      0x4a2a14
004A29FA  8b 4d 44                 mov      ecx, dword ptr [ebp + 0x44]
004A29FD  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2A03  3b ca                    cmp      ecx, edx
004A2A05  75 0d                    jne      0x4a2a14
004A2A07  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A2A0A  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2A10  3b d1                    cmp      edx, ecx
004A2A12  74 18                    je       0x4a2a2c
004A2A14  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A2A17  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A2A1C  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A2A1F  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2A25  89 4d 48                 mov      dword ptr [ebp + 0x48], ecx
004A2A28  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A2A2C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2A2F  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A2A35  85 c0                    test     eax, eax
004A2A37  75 26                    jne      0x4a2a5f
004A2A39  8b 11                    mov      edx, dword ptr [ecx]
004A2A3B  6a 01                    push     1
004A2A3D  6a 00                    push     0
004A2A3F  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A2A45  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2A48  8a 41 7d                 mov      al, byte ptr [ecx + 0x7d]
004A2A4B  84 c0                    test     al, al
004A2A4D  0f 85 59 04 00 00        jne      0x4a2eac
004A2A53  5f                       pop      edi
004A2A54  5e                       pop      esi
004A2A55  5d                       pop      ebp
004A2A56  32 c0                    xor      al, al
004A2A58  5b                       pop      ebx
004A2A59  83 c4 4c                 add      esp, 0x4c
004A2A5C  c2 0c 00                 ret      0xc
004A2A5F  e8 4c af 02 00           call     0x4cd9b0
004A2A64  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2A67  6a 01                    push     1
004A2A69  6a 00                    push     0
004A2A6B  8b 01                    mov      eax, dword ptr [ecx]
004A2A6D  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A2A73  84 c0                    test     al, al
004A2A75  74 ce                    je       0x4a2a45
004A2A77  5f                       pop      edi
004A2A78  5e                       pop      esi
004A2A79  5d                       pop      ebp
004A2A7A  b0 01                    mov      al, 1
004A2A7C  5b                       pop      ebx
004A2A7D  83 c4 4c                 add      esp, 0x4c
004A2A80  c2 0c 00                 ret      0xc
004A2A83  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2A86  8d 54 24 64              lea      edx, [esp + 0x64]
004A2A8A  52                       push     edx
004A2A8B  81 c1 e0 02 00 00        add      ecx, 0x2e0
004A2A91  e8 4a 61 01 00           call     0x4b8be0
004A2A96  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2A99  8b f8                    mov      edi, eax
004A2A9B  8d 54 24 44              lea      edx, [esp + 0x44]
004A2A9F  8b 01                    mov      eax, dword ptr [ecx]
004A2AA1  52                       push     edx
004A2AA2  ff 50 48                 call     dword ptr [eax + 0x48]
004A2AA5  8b f0                    mov      esi, eax
004A2AA7  6a 01                    push     1
004A2AA9  8b 06                    mov      eax, dword ptr [esi]
004A2AAB  99                       cdq      
004A2AAC  81 e2 ff 00 00 00        and      edx, 0xff
004A2AB2  03 c2                    add      eax, edx
004A2AB4  8b c8                    mov      ecx, eax
004A2AB6  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A2AB9  99                       cdq      
004A2ABA  81 e2 ff 00 00 00        and      edx, 0xff
004A2AC0  03 c2                    add      eax, edx
004A2AC2  8b 17                    mov      edx, dword ptr [edi]
004A2AC4  c1 ea 0c                 shr      edx, 0xc
004A2AC7  c1 f9 08                 sar      ecx, 8
004A2ACA  c1 f8 08                 sar      eax, 8
004A2ACD  42                       inc      edx
004A2ACE  d1 ea                    shr      edx, 1
004A2AD0  83 e2 07                 and      edx, 7
004A2AD3  66 03 0c 95 70 1a 85 00  add      cx, word ptr [edx*4 + 0x851a70]
004A2ADB  8d 14 95 70 1a 85 00     lea      edx, [edx*4 + 0x851a70]
004A2AE2  66 89 4c 24 64           mov      word ptr [esp + 0x64], cx
004A2AE7  66 8b 4a 02              mov      cx, word ptr [edx + 2]
004A2AEB  66 03 c8                 add      cx, ax
004A2AEE  8d 44 24 6c              lea      eax, [esp + 0x6c]
004A2AF2  66 89 4c 24 66           mov      word ptr [esp + 0x66], cx
004A2AF7  8b 54 24 64              mov      edx, dword ptr [esp + 0x64]
004A2AFB  50                       push     eax
004A2AFC  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2B01  89 54 24 70              mov      dword ptr [esp + 0x70], edx
004A2B05  e8 56 7b 0b 00           call     0x55a660
004A2B0A  84 c0                    test     al, al
004A2B0C  0f 84 eb 02 00 00        je       0x4a2dfd
004A2B12  8d 4c 24 60              lea      ecx, [esp + 0x60]
004A2B16  51                       push     ecx
004A2B17  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2B1A  81 c1 e0 02 00 00        add      ecx, 0x2e0
004A2B20  e8 bb 60 01 00           call     0x4b8be0
004A2B25  8b 30                    mov      esi, dword ptr [eax]
004A2B27  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2B2A  c1 ee 0c                 shr      esi, 0xc
004A2B2D  8b 39                    mov      edi, dword ptr [ecx]
004A2B2F  46                       inc      esi
004A2B30  33 db                    xor      ebx, ebx
004A2B32  6a 01                    push     1
004A2B34  d1 ee                    shr      esi, 1
004A2B36  53                       push     ebx
004A2B37  83 e6 07                 and      esi, 7
004A2B3A  e8 91 1c 13 00           call     0x5d47d0
004A2B3F  50                       push     eax
004A2B40  8d 54 24 74              lea      edx, [esp + 0x74]
004A2B44  56                       push     esi
004A2B45  52                       push     edx
004A2B46  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2B4B  e8 20 55 0a 00           call     0x548070
004A2B50  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2B53  50                       push     eax
004A2B54  ff 97 94 01 00 00        call     dword ptr [edi + 0x194]
004A2B5A  83 f8 03                 cmp      eax, 3
004A2B5D  75 20                    jne      0x4a2b7f
004A2B5F  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A2B62  8b 44 24 68              mov      eax, dword ptr [esp + 0x68]
004A2B66  8d 4c 24 60              lea      ecx, [esp + 0x60]
004A2B6A  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004A2B6E  51                       push     ecx
004A2B6F  52                       push     edx
004A2B70  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2B75  e8 56 81 0b 00           call     0x55acd0
004A2B7A  e9 7e 02 00 00           jmp      0x4a2dfd
004A2B7F  83 f8 06                 cmp      eax, 6
004A2B82  0f 85 75 02 00 00        jne      0x4a2dfd
004A2B88  8d 44 24 68              lea      eax, [esp + 0x68]
004A2B8C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2B91  50                       push     eax
004A2B92  e8 d9 54 0a 00           call     0x548070
004A2B97  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2B9A  8b f8                    mov      edi, eax
004A2B9C  81 c1 88 00 00 00        add      ecx, 0x88
004A2BA2  53                       push     ebx
004A2BA3  8b 11                    mov      edx, dword ptr [ecx]
004A2BA5  89 54 24 48              mov      dword ptr [esp + 0x48], edx
004A2BA9  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A2BAC  0f bf 54 24 6e           movsx    edx, word ptr [esp + 0x6e]
004A2BB1  8b 71 08                 mov      esi, dword ptr [ecx + 8]
004A2BB4  89 44 24 4c              mov      dword ptr [esp + 0x4c], eax
004A2BB8  0f bf 4c 24 6c           movsx    ecx, word ptr [esp + 0x6c]
004A2BBD  c1 e1 08                 shl      ecx, 8
004A2BC0  81 c1 80 00 00 00        add      ecx, 0x80
004A2BC6  8d 44 24 1c              lea      eax, [esp + 0x1c]
004A2BCA  c1 e2 08                 shl      edx, 8
004A2BCD  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
004A2BD1  81 c2 80 00 00 00        add      edx, 0x80
004A2BD7  50                       push     eax
004A2BD8  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2BDD  89 54 24 24              mov      dword ptr [esp + 0x24], edx
004A2BE1  89 5c 24 28              mov      dword ptr [esp + 0x28], ebx
004A2BE5  89 5c 24 34              mov      dword ptr [esp + 0x34], ebx
004A2BE9  89 5c 24 38              mov      dword ptr [esp + 0x38], ebx
004A2BED  e8 8e 76 0b 00           call     0x55a280
004A2BF2  8b 0d d0 29 85 00        mov      ecx, dword ptr [0x8529d0]
004A2BF8  8d 14 48                 lea      edx, [eax + ecx*2]
004A2BFB  8d 4c 24 30              lea      ecx, [esp + 0x30]
004A2BFF  3b f2                    cmp      esi, edx
004A2C01  0f 9f c0                 setg     al
004A2C04  50                       push     eax
004A2C05  51                       push     ecx
004A2C06  8b cf                    mov      ecx, edi
004A2C08  e8 53 ea fc ff           call     0x471660
004A2C0D  3b c3                    cmp      eax, ebx
004A2C0F  0f 84 e8 01 00 00        je       0x4a2dfd
004A2C15  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A2C18  50                       push     eax
004A2C19  8b 8a b4 01 00 00        mov      ecx, dword ptr [edx + 0x1b4]
004A2C1F  e8 5c 29 04 00           call     0x4e5580
004A2C24  84 c0                    test     al, al
004A2C26  0f 84 d1 01 00 00        je       0x4a2dfd
004A2C2C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2C2F  8b 01                    mov      eax, dword ptr [ecx]
004A2C31  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A2C37  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A2C3D  84 c9                    test     cl, cl
004A2C3F  0f 85 b8 01 00 00        jne      0x4a2dfd
004A2C45  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2C48  8d 44 24 44              lea      eax, [esp + 0x44]
004A2C4C  50                       push     eax
004A2C4D  8b 11                    mov      edx, dword ptr [ecx]
004A2C4F  ff 52 48                 call     dword ptr [edx + 0x48]
004A2C52  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A2C55  8b 75 3c                 mov      esi, dword ptr [ebp + 0x3c]
004A2C58  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A2C5B  8b 00                    mov      eax, dword ptr [eax]
004A2C5D  2b ce                    sub      ecx, esi
004A2C5F  51                       push     ecx
004A2C60  8b 4d 38                 mov      ecx, dword ptr [ebp + 0x38]
004A2C63  2b d1                    sub      edx, ecx
004A2C65  8b 4d 34                 mov      ecx, dword ptr [ebp + 0x34]
004A2C68  2b c1                    sub      eax, ecx
004A2C6A  52                       push     edx
004A2C6B  50                       push     eax
004A2C6C  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A2C70  e8 bb 89 f7 ff           call     0x41b630
004A2C75  8b 08                    mov      ecx, dword ptr [eax]
004A2C77  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A2C7B  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A2C7F  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A2C82  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A2C86  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A2C89  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A2C8D  e8 ee 8a f7 ff           call     0x41b780
004A2C92  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A2C98  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A2C9E  0f 8d fc 00 00 00        jge      0x4a2da0
004A2CA4  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2CA7  e8 64 42 19 00           call     0x636f10
004A2CAC  84 c0                    test     al, al
004A2CAE  0f 85 ec 00 00 00        jne      0x4a2da0
004A2CB4  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2CB7  81 c1 88 00 00 00        add      ecx, 0x88
004A2CBD  8b d1                    mov      edx, ecx
004A2CBF  8b 02                    mov      eax, dword ptr [edx]
004A2CC1  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A2CC5  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A2CC8  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A2CCC  8b 45 3c                 mov      eax, dword ptr [ebp + 0x3c]
004A2CCF  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A2CD2  2b c2                    sub      eax, edx
004A2CD4  99                       cdq      
004A2CD5  33 c2                    xor      eax, edx
004A2CD7  2b c2                    sub      eax, edx
004A2CD9  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A2CDF  03 d2                    add      edx, edx
004A2CE1  3b c2                    cmp      eax, edx
004A2CE3  0f 8d b7 00 00 00        jge      0x4a2da0
004A2CE9  8b 01                    mov      eax, dword ptr [ecx]
004A2CEB  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004A2CEF  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A2CF2  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A2CF6  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A2CF9  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A2CFD  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A2D01  51                       push     ecx
004A2D02  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2D07  e8 f4 52 0a 00           call     0x548000
004A2D0C  83 b8 ec 00 00 00 0a     cmp      dword ptr [eax + 0xec], 0xa
004A2D13  0f 84 87 00 00 00        je       0x4a2da0
004A2D19  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2D1E  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A2D21  3b c8                    cmp      ecx, eax
004A2D23  75 1a                    jne      0x4a2d3f
004A2D25  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A2D28  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A2D2E  3b d1                    cmp      edx, ecx
004A2D30  75 0d                    jne      0x4a2d3f
004A2D32  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A2D35  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A2D3B  3b ca                    cmp      ecx, edx
004A2D3D  74 18                    je       0x4a2d57
004A2D3F  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A2D42  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2D48  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A2D4B  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A2D50  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A2D53  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A2D57  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2D5A  39 99 88 04 00 00        cmp      dword ptr [ecx + 0x488], ebx
004A2D60  75 17                    jne      0x4a2d79
004A2D62  8b 11                    mov      edx, dword ptr [ecx]
004A2D64  6a 01                    push     1
004A2D66  53                       push     ebx
004A2D67  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A2D6D  5f                       pop      edi
004A2D6E  5e                       pop      esi
004A2D6F  5d                       pop      ebp
004A2D70  32 c0                    xor      al, al
004A2D72  5b                       pop      ebx
004A2D73  83 c4 4c                 add      esp, 0x4c
004A2D76  c2 0c 00                 ret      0xc
004A2D79  e8 32 ac 02 00           call     0x4cd9b0
004A2D7E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2D81  6a 01                    push     1
004A2D83  53                       push     ebx
004A2D84  8b 01                    mov      eax, dword ptr [ecx]
004A2D86  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A2D8C  84 c0                    test     al, al
004A2D8E  0f 84 b0 0c 00 00        je       0x4a3a44
004A2D94  5f                       pop      edi
004A2D95  5e                       pop      esi
004A2D96  5d                       pop      ebp
004A2D97  b0 01                    mov      al, 1
004A2D99  5b                       pop      ebx
004A2D9A  83 c4 4c                 add      esp, 0x4c
004A2D9D  c2 0c 00                 ret      0xc
004A2DA0  8b 87 40 01 00 00        mov      eax, dword ptr [edi + 0x140]
004A2DA6  f6 c4 01                 test     ah, 1
004A2DA9  74 38                    je       0x4a2de3
004A2DAB  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2DAE  c6 44 24 60 01           mov      byte ptr [esp + 0x60], 1
004A2DB3  81 c1 88 00 00 00        add      ecx, 0x88
004A2DB9  8b 11                    mov      edx, dword ptr [ecx]
004A2DBB  89 54 24 44              mov      dword ptr [esp + 0x44], edx
004A2DBF  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A2DC2  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A2DC6  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A2DC9  99                       cdq      
004A2DCA  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A2DD0  0f be 8f 1b 01 00 00     movsx    ecx, byte ptr [edi + 0x11b]
004A2DD7  2b c1                    sub      eax, ecx
004A2DD9  99                       cdq      
004A2DDA  33 c2                    xor      eax, edx
004A2DDC  2b c2                    sub      eax, edx
004A2DDE  83 f8 02                 cmp      eax, 2
004A2DE1  7f 05                    jg       0x4a2de8
004A2DE3  c6 44 24 60 00           mov      byte ptr [esp + 0x60], 0
004A2DE8  8b 54 24 60              mov      edx, dword ptr [esp + 0x60]
004A2DEC  8b cf                    mov      ecx, edi
004A2DEE  52                       push     edx
004A2DEF  6a 01                    push     1
004A2DF1  6a 01                    push     1
004A2DF3  68 98 29 85 00           push     0x852998
004A2DF8  e8 23 3b fd ff           call     0x476920
004A2DFD  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2E00  8b 81 3c 05 00 00        mov      eax, dword ptr [ecx + 0x53c]
004A2E06  85 c0                    test     eax, eax
004A2E08  7e 0c                    jle      0x4a2e16
004A2E0A  48                       dec      eax
004A2E0B  89 81 3c 05 00 00        mov      dword ptr [ecx + 0x53c], eax
004A2E11  e9 96 00 00 00           jmp      0x4a2eac
004A2E16  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2E1B  8b 55 40                 mov      edx, dword ptr [ebp + 0x40]
004A2E1E  3b d0                    cmp      edx, eax
004A2E20  75 1a                    jne      0x4a2e3c
004A2E22  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A2E25  8b 35 9c 29 85 00        mov      esi, dword ptr [0x85299c]
004A2E2B  3b d6                    cmp      edx, esi
004A2E2D  75 0d                    jne      0x4a2e3c
004A2E2F  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A2E32  8b 35 a0 29 85 00        mov      esi, dword ptr [0x8529a0]
004A2E38  3b d6                    cmp      edx, esi
004A2E3A  74 18                    je       0x4a2e54
004A2E3C  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A2E3F  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A2E44  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A2E47  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A2E4D  89 55 48                 mov      dword ptr [ebp + 0x48], edx
004A2E50  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A2E54  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A2E5A  85 c0                    test     eax, eax
004A2E5C  0f 85 f0 00 00 00        jne      0x4a2f52
004A2E62  8b 01                    mov      eax, dword ptr [ecx]
004A2E64  6a 01                    push     1
004A2E66  6a 00                    push     0
004A2E68  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A2E6E  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2E71  8a 48 7d                 mov      cl, byte ptr [eax + 0x7d]
004A2E74  84 c9                    test     cl, cl
004A2E76  0f 84 c8 0b 00 00        je       0x4a3a44
004A2E7C  8a 88 7a 05 00 00        mov      cl, byte ptr [eax + 0x57a]
004A2E82  84 c9                    test     cl, cl
004A2E84  74 1c                    je       0x4a2ea2
004A2E86  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A2E8B  6a 00                    push     0
004A2E8D  ba 00 20 00 00           mov      edx, 0x2000
004A2E92  68 00 00 80 3f           push     0x3f800000
004A2E97  8b 88 20 06 00 00        mov      ecx, dword ptr [eax + 0x620]
004A2E9D  e8 0e 0f 27 00           call     0x713db0
004A2EA2  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2EA5  c6 81 7a 05 00 00 00     mov      byte ptr [ecx + 0x57a], 0
004A2EAC  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004A2EB0  50                       push     eax
004A2EB1  8b 10                    mov      edx, dword ptr [eax]
004A2EB3  ff 52 10                 call     dword ptr [edx + 0x10]
004A2EB6  84 c0                    test     al, al
004A2EB8  75 43                    jne      0x4a2efd
004A2EBA  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2EBD  8b 81 28 02 00 00        mov      eax, dword ptr [ecx + 0x228]
004A2EC3  85 c0                    test     eax, eax
004A2EC5  74 36                    je       0x4a2efd
004A2EC7  8b 11                    mov      edx, dword ptr [ecx]
004A2EC9  50                       push     eax
004A2ECA  ff 92 54 03 00 00        call     dword ptr [edx + 0x354]
004A2ED0  84 c0                    test     al, al
004A2ED2  75 29                    jne      0x4a2efd
004A2ED4  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A2ED7  c6 80 78 05 00 00 01     mov      byte ptr [eax + 0x578], 1
004A2EDE  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2EE1  8b 89 c4 04 00 00        mov      ecx, dword ptr [ecx + 0x4c4]
004A2EE7  85 c9                    test     ecx, ecx
004A2EE9  74 05                    je       0x4a2ef0
004A2EEB  e8 40 7b 21 00           call     0x6baa30
004A2EF0  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2EF3  6a 00                    push     0
004A2EF5  8b 11                    mov      edx, dword ptr [ecx]
004A2EF7  ff 92 70 03 00 00        call     dword ptr [edx + 0x370]
004A2EFD  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A2F02  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A2F05  3b c8                    cmp      ecx, eax
004A2F07  75 1a                    jne      0x4a2f23
004A2F09  8b 4d 44                 mov      ecx, dword ptr [ebp + 0x44]
004A2F0C  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A2F12  3b ca                    cmp      ecx, edx
004A2F14  75 0d                    jne      0x4a2f23
004A2F16  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A2F19  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2F1F  3b d1                    cmp      edx, ecx
004A2F21  74 18                    je       0x4a2f3b
004A2F23  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A2F26  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A2F2B  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A2F2E  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A2F34  89 4d 48                 mov      dword ptr [ebp + 0x48], ecx
004A2F37  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A2F3B  5f                       pop      edi
004A2F3C  c7 45 58 ff ff ff ff     mov      dword ptr [ebp + 0x58], 0xffffffff
004A2F43  c6 45 61 00              mov      byte ptr [ebp + 0x61], 0
004A2F47  5e                       pop      esi
004A2F48  5d                       pop      ebp
004A2F49  32 c0                    xor      al, al
004A2F4B  5b                       pop      ebx
004A2F4C  83 c4 4c                 add      esp, 0x4c
004A2F4F  c2 0c 00                 ret      0xc
004A2F52  e8 59 aa 02 00           call     0x4cd9b0
004A2F57  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A2F5A  6a 01                    push     1
004A2F5C  6a 00                    push     0
004A2F5E  8b 11                    mov      edx, dword ptr [ecx]
004A2F60  ff 92 14 04 00 00        call     dword ptr [edx + 0x414]
004A2F66  84 c0                    test     al, al
004A2F68  0f 84 00 ff ff ff        je       0x4a2e6e
004A2F6E  5f                       pop      edi
004A2F6F  5e                       pop      esi
004A2F70  5d                       pop      ebp
004A2F71  b0 01                    mov      al, 1
004A2F73  5b                       pop      ebx
004A2F74  83 c4 4c                 add      esp, 0x4c
004A2F77  c2 0c 00                 ret      0xc
004A2F7A  83 b9 d0 04 00 00 08     cmp      dword ptr [ecx + 0x4d0], 8
004A2F81  0f 84 bd 0a 00 00        je       0x4a3a44
004A2F87  8b 11                    mov      edx, dword ptr [ecx]
004A2F89  8d 44 24 44              lea      eax, [esp + 0x44]
004A2F8D  50                       push     eax
004A2F8E  ff 52 48                 call     dword ptr [edx + 0x48]
004A2F91  8b f0                    mov      esi, eax
004A2F93  6a 01                    push     1
004A2F95  8b 06                    mov      eax, dword ptr [esi]
004A2F97  99                       cdq      
004A2F98  81 e2 ff 00 00 00        and      edx, 0xff
004A2F9E  03 c2                    add      eax, edx
004A2FA0  8b c8                    mov      ecx, eax
004A2FA2  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A2FA5  99                       cdq      
004A2FA6  81 e2 ff 00 00 00        and      edx, 0xff
004A2FAC  03 c2                    add      eax, edx
004A2FAE  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A2FB1  c1 f9 08                 sar      ecx, 8
004A2FB4  8b 92 d0 04 00 00        mov      edx, dword ptr [edx + 0x4d0]
004A2FBA  83 e2 07                 and      edx, 7
004A2FBD  c1 f8 08                 sar      eax, 8
004A2FC0  66 8b 34 95 70 1a 85 00  mov      si, word ptr [edx*4 + 0x851a70]
004A2FC8  8d 14 95 70 1a 85 00     lea      edx, [edx*4 + 0x851a70]
004A2FCF  66 03 f1                 add      si, cx
004A2FD2  66 8b 4a 02              mov      cx, word ptr [edx + 2]
004A2FD6  66 89 74 24 1c           mov      word ptr [esp + 0x1c], si
004A2FDB  66 03 c8                 add      cx, ax
004A2FDE  8d 44 24 28              lea      eax, [esp + 0x28]
004A2FE2  66 89 4c 24 1e           mov      word ptr [esp + 0x1e], cx
004A2FE7  8b 54 24 1c              mov      edx, dword ptr [esp + 0x1c]
004A2FEB  50                       push     eax
004A2FEC  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A2FF1  89 54 24 2c              mov      dword ptr [esp + 0x2c], edx
004A2FF5  e8 66 76 0b 00           call     0x55a660
004A2FFA  84 c0                    test     al, al
004A2FFC  0f 84 b2 02 00 00        je       0x4a32b4
004A3002  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3005  6a 01                    push     1
004A3007  6a 00                    push     0
004A3009  8b 31                    mov      esi, dword ptr [ecx]
004A300B  e8 c0 17 13 00           call     0x5d47d0
004A3010  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3013  50                       push     eax
004A3014  8d 44 24 30              lea      eax, [esp + 0x30]
004A3018  8b 91 d0 04 00 00        mov      edx, dword ptr [ecx + 0x4d0]
004A301E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3023  52                       push     edx
004A3024  50                       push     eax
004A3025  e8 46 50 0a 00           call     0x548070
004A302A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A302D  50                       push     eax
004A302E  ff 96 94 01 00 00        call     dword ptr [esi + 0x194]
004A3034  83 f8 03                 cmp      eax, 3
004A3037  75 20                    jne      0x4a3059
004A3039  8b 4c 24 24              mov      ecx, dword ptr [esp + 0x24]
004A303D  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A3040  8d 54 24 28              lea      edx, [esp + 0x28]
004A3044  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
004A3048  52                       push     edx
004A3049  50                       push     eax
004A304A  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A304F  e8 7c 7c 0b 00           call     0x55acd0
004A3054  e9 5b 02 00 00           jmp      0x4a32b4
004A3059  83 f8 06                 cmp      eax, 6
004A305C  0f 85 52 02 00 00        jne      0x4a32b4
004A3062  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A3066  51                       push     ecx
004A3067  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A306C  e8 ff 4f 0a 00           call     0x548070
004A3071  0f bf 54 24 24           movsx    edx, word ptr [esp + 0x24]
004A3076  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3079  8b f0                    mov      esi, eax
004A307B  0f bf 44 24 26           movsx    eax, word ptr [esp + 0x26]
004A3080  c1 e2 08                 shl      edx, 8
004A3083  c1 e0 08                 shl      eax, 8
004A3086  81 c2 80 00 00 00        add      edx, 0x80
004A308C  05 80 00 00 00           add      eax, 0x80
004A3091  33 db                    xor      ebx, ebx
004A3093  81 c1 88 00 00 00        add      ecx, 0x88
004A3099  89 54 24 18              mov      dword ptr [esp + 0x18], edx
004A309D  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
004A30A1  89 5c 24 20              mov      dword ptr [esp + 0x20], ebx
004A30A5  8b 11                    mov      edx, dword ptr [ecx]
004A30A7  53                       push     ebx
004A30A8  89 54 24 48              mov      dword ptr [esp + 0x48], edx
004A30AC  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A30AF  89 44 24 4c              mov      dword ptr [esp + 0x4c], eax
004A30B3  8b 79 08                 mov      edi, dword ptr [ecx + 8]
004A30B6  8d 4c 24 1c              lea      ecx, [esp + 0x1c]
004A30BA  51                       push     ecx
004A30BB  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A30C0  89 5c 24 34              mov      dword ptr [esp + 0x34], ebx
004A30C4  89 5c 24 38              mov      dword ptr [esp + 0x38], ebx
004A30C8  e8 b3 71 0b 00           call     0x55a280
004A30CD  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A30D3  8d 04 50                 lea      eax, [eax + edx*2]
004A30D6  8d 54 24 30              lea      edx, [esp + 0x30]
004A30DA  3b f8                    cmp      edi, eax
004A30DC  0f 9f c1                 setg     cl
004A30DF  51                       push     ecx
004A30E0  52                       push     edx
004A30E1  8b ce                    mov      ecx, esi
004A30E3  e8 78 e5 fc ff           call     0x471660
004A30E8  3b c3                    cmp      eax, ebx
004A30EA  0f 84 c4 01 00 00        je       0x4a32b4
004A30F0  50                       push     eax
004A30F1  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A30F4  8b 88 b4 01 00 00        mov      ecx, dword ptr [eax + 0x1b4]
004A30FA  e8 81 24 04 00           call     0x4e5580
004A30FF  84 c0                    test     al, al
004A3101  0f 84 ad 01 00 00        je       0x4a32b4
004A3107  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A310A  8b 11                    mov      edx, dword ptr [ecx]
004A310C  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A3112  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A3118  84 c9                    test     cl, cl
004A311A  0f 85 94 01 00 00        jne      0x4a32b4
004A3120  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3123  8d 54 24 44              lea      edx, [esp + 0x44]
004A3127  52                       push     edx
004A3128  8b 01                    mov      eax, dword ptr [ecx]
004A312A  ff 50 48                 call     dword ptr [eax + 0x48]
004A312D  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A3130  8b 55 3c                 mov      edx, dword ptr [ebp + 0x3c]
004A3133  8b 7d 38                 mov      edi, dword ptr [ebp + 0x38]
004A3136  8b 5d 34                 mov      ebx, dword ptr [ebp + 0x34]
004A3139  2b ca                    sub      ecx, edx
004A313B  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A313E  8b 00                    mov      eax, dword ptr [eax]
004A3140  2b d7                    sub      edx, edi
004A3142  51                       push     ecx
004A3143  2b c3                    sub      eax, ebx
004A3145  52                       push     edx
004A3146  50                       push     eax
004A3147  8d 4c 24 24              lea      ecx, [esp + 0x24]
004A314B  e8 e0 84 f7 ff           call     0x41b630
004A3150  8b 08                    mov      ecx, dword ptr [eax]
004A3152  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A3156  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A315A  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A315D  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A3161  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A3164  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A3168  e8 13 86 f7 ff           call     0x41b780
004A316D  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A3173  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A3179  0f 8d d8 00 00 00        jge      0x4a3257
004A317F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3182  e8 89 3d 19 00           call     0x636f10
004A3187  84 c0                    test     al, al
004A3189  0f 85 c8 00 00 00        jne      0x4a3257
004A318F  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3192  81 c1 88 00 00 00        add      ecx, 0x88
004A3198  8b d1                    mov      edx, ecx
004A319A  8b 02                    mov      eax, dword ptr [edx]
004A319C  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A31A0  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A31A3  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A31A7  8b 45 3c                 mov      eax, dword ptr [ebp + 0x3c]
004A31AA  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A31AD  2b c2                    sub      eax, edx
004A31AF  99                       cdq      
004A31B0  33 c2                    xor      eax, edx
004A31B2  2b c2                    sub      eax, edx
004A31B4  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A31BA  03 d2                    add      edx, edx
004A31BC  3b c2                    cmp      eax, edx
004A31BE  0f 8d 93 00 00 00        jge      0x4a3257
004A31C4  8b 01                    mov      eax, dword ptr [ecx]
004A31C6  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004A31CA  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A31CD  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A31D1  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A31D4  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A31D8  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A31DC  51                       push     ecx
004A31DD  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A31E2  e8 19 4e 0a 00           call     0x548000
004A31E7  83 b8 ec 00 00 00 0a     cmp      dword ptr [eax + 0xec], 0xa
004A31EE  74 67                    je       0x4a3257
004A31F0  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A31F5  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A31F8  3b c8                    cmp      ecx, eax
004A31FA  75 1a                    jne      0x4a3216
004A31FC  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A31FF  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A3205  3b d1                    cmp      edx, ecx
004A3207  75 0d                    jne      0x4a3216
004A3209  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A320C  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A3212  3b ca                    cmp      ecx, edx
004A3214  74 18                    je       0x4a322e
004A3216  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A3219  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A321F  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A3222  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A3227  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A322A  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A322E  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3231  8b 81 88 04 00 00        mov      eax, dword ptr [ecx + 0x488]
004A3237  85 c0                    test     eax, eax
004A3239  0f 85 74 12 00 00        jne      0x4a44b3
004A323F  8b 11                    mov      edx, dword ptr [ecx]
004A3241  6a 01                    push     1
004A3243  6a 00                    push     0
004A3245  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A324B  5f                       pop      edi
004A324C  5e                       pop      esi
004A324D  5d                       pop      ebp
004A324E  32 c0                    xor      al, al
004A3250  5b                       pop      ebx
004A3251  83 c4 4c                 add      esp, 0x4c
004A3254  c2 0c 00                 ret      0xc
004A3257  8b 86 40 01 00 00        mov      eax, dword ptr [esi + 0x140]
004A325D  f6 c4 01                 test     ah, 1
004A3260  74 38                    je       0x4a329a
004A3262  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3265  c6 44 24 18 01           mov      byte ptr [esp + 0x18], 1
004A326A  81 c1 88 00 00 00        add      ecx, 0x88
004A3270  8b 11                    mov      edx, dword ptr [ecx]
004A3272  89 54 24 44              mov      dword ptr [esp + 0x44], edx
004A3276  8b 41 04                 mov      eax, dword ptr [ecx + 4]
004A3279  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A327D  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A3280  99                       cdq      
004A3281  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A3287  0f be 8e 1b 01 00 00     movsx    ecx, byte ptr [esi + 0x11b]
004A328E  2b c1                    sub      eax, ecx
004A3290  99                       cdq      
004A3291  33 c2                    xor      eax, edx
004A3293  2b c2                    sub      eax, edx
004A3295  83 f8 02                 cmp      eax, 2
004A3298  7f 05                    jg       0x4a329f
004A329A  c6 44 24 18 00           mov      byte ptr [esp + 0x18], 0
004A329F  8b 54 24 18              mov      edx, dword ptr [esp + 0x18]
004A32A3  8b ce                    mov      ecx, esi
004A32A5  52                       push     edx
004A32A6  6a 01                    push     1
004A32A8  6a 01                    push     1
004A32AA  68 98 29 85 00           push     0x852998
004A32AF  e8 6c 36 fd ff           call     0x476920
004A32B4  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A32B7  c7 80 3c 05 00 00 0a 00 00 00 mov      dword ptr [eax + 0x53c], 0xa
004A32C1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A32C4  8b 99 d0 04 00 00        mov      ebx, dword ptr [ecx + 0x4d0]
004A32CA  83 fb 08                 cmp      ebx, 8
004A32CD  0f 84 71 07 00 00        je       0x4a3a44
004A32D3  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A32D6  8b f3                    mov      esi, ebx
004A32D8  81 c2 88 00 00 00        add      edx, 0x88
004A32DE  83 e6 07                 and      esi, 7
004A32E1  8b 02                    mov      eax, dword ptr [edx]
004A32E3  8d 34 f5 c0 1a 85 00     lea      esi, [esi*8 + 0x851ac0]
004A32EA  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A32ED  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A32F0  52                       push     edx
004A32F1  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A32F4  03 d1                    add      edx, ecx
004A32F6  8b 0e                    mov      ecx, dword ptr [esi]
004A32F8  03 c8                    add      ecx, eax
004A32FA  52                       push     edx
004A32FB  51                       push     ecx
004A32FC  8d 4c 24 50              lea      ecx, [esp + 0x50]
004A3300  e8 2b 83 f7 ff           call     0x41b630
004A3305  8b 10                    mov      edx, dword ptr [eax]
004A3307  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A330B  8b 48 04                 mov      ecx, dword ptr [eax + 4]
004A330E  89 4c 24 3c              mov      dword ptr [esp + 0x3c], ecx
004A3312  8b 50 08                 mov      edx, dword ptr [eax + 8]
004A3315  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A3318  05 88 00 00 00           add      eax, 0x88
004A331D  89 54 24 40              mov      dword ptr [esp + 0x40], edx
004A3321  8b 08                    mov      ecx, dword ptr [eax]
004A3323  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A3327  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A332B  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A332E  51                       push     ecx
004A332F  89 54 24 34              mov      dword ptr [esp + 0x34], edx
004A3333  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3338  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A333B  89 44 24 38              mov      dword ptr [esp + 0x38], eax
004A333F  e8 bc 4c 0a 00           call     0x548000
004A3344  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3347  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
004A334E  8a 51 79                 mov      dl, byte ptr [ecx + 0x79]
004A3351  f6 da                    neg      dl
004A3353  1b d2                    sbb      edx, edx
004A3355  81 c1 88 00 00 00        add      ecx, 0x88
004A335B  83 e2 04                 and      edx, 4
004A335E  03 d0                    add      edx, eax
004A3360  8b fa                    mov      edi, edx
004A3362  8b d1                    mov      edx, ecx
004A3364  8b 02                    mov      eax, dword ptr [edx]
004A3366  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A3369  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A336C  52                       push     edx
004A336D  8b 56 04                 mov      edx, dword ptr [esi + 4]
004A3370  03 d1                    add      edx, ecx
004A3372  8b 0e                    mov      ecx, dword ptr [esi]
004A3374  03 c8                    add      ecx, eax
004A3376  52                       push     edx
004A3377  51                       push     ecx
004A3378  8d 4c 24 50              lea      ecx, [esp + 0x50]
004A337C  e8 af 82 f7 ff           call     0x41b630
004A3381  8b 10                    mov      edx, dword ptr [eax]
004A3383  89 54 24 2c              mov      dword ptr [esp + 0x2c], edx
004A3387  8b 48 04                 mov      ecx, dword ptr [eax + 4]
004A338A  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
004A338E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3393  8b 50 08                 mov      edx, dword ptr [eax + 8]
004A3396  8d 44 24 2c              lea      eax, [esp + 0x2c]
004A339A  50                       push     eax
004A339B  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A339F  e8 5c 4c 0a 00           call     0x548000
004A33A4  8b 90 40 01 00 00        mov      edx, dword ptr [eax + 0x140]
004A33AA  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A33AD  c1 ea 08                 shr      edx, 8
004A33B0  33 c0                    xor      eax, eax
004A33B2  83 e2 01                 and      edx, 1
004A33B5  8a 41 79                 mov      al, byte ptr [ecx + 0x79]
004A33B8  33 d0                    xor      edx, eax
004A33BA  74 07                    je       0x4a33c3
004A33BC  c6 81 7b 05 00 00 01     mov      byte ptr [ecx + 0x57b], 1
004A33C3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A33C6  8b 11                    mov      edx, dword ptr [ecx]
004A33C8  ff 92 7c 02 00 00        call     dword ptr [edx + 0x27c]
004A33CE  84 c0                    test     al, al
004A33D0  75 0c                    jne      0x4a33de
004A33D2  5f                       pop      edi
004A33D3  5e                       pop      esi
004A33D4  5d                       pop      ebp
004A33D5  b0 01                    mov      al, 1
004A33D7  5b                       pop      ebx
004A33D8  83 c4 4c                 add      esp, 0x4c
004A33DB  c2 0c 00                 ret      0xc
004A33DE  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004A33E2  8d 4c 24 28              lea      ecx, [esp + 0x28]
004A33E6  99                       cdq      
004A33E7  81 e2 ff 00 00 00        and      edx, 0xff
004A33ED  51                       push     ecx
004A33EE  03 c2                    add      eax, edx
004A33F0  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A33F5  c1 f8 08                 sar      eax, 8
004A33F8  66 89 44 24 1c           mov      word ptr [esp + 0x1c], ax
004A33FD  8b 44 24 40              mov      eax, dword ptr [esp + 0x40]
004A3401  99                       cdq      
004A3402  81 e2 ff 00 00 00        and      edx, 0xff
004A3408  03 c2                    add      eax, edx
004A340A  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A340D  c1 f8 08                 sar      eax, 8
004A3410  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
004A3415  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004A3419  52                       push     edx
004A341A  89 44 24 30              mov      dword ptr [esp + 0x30], eax
004A341E  e8 ad 78 0b 00           call     0x55acd0
004A3423  84 c0                    test     al, al
004A3425  75 0c                    jne      0x4a3433
004A3427  5f                       pop      edi
004A3428  5e                       pop      esi
004A3429  5d                       pop      ebp
004A342A  b0 01                    mov      al, 1
004A342C  5b                       pop      ebx
004A342D  83 c4 4c                 add      esp, 0x4c
004A3430  c2 0c 00                 ret      0xc
004A3433  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3436  8d 44 24 2c              lea      eax, [esp + 0x2c]
004A343A  50                       push     eax
004A343B  81 c1 e0 02 00 00        add      ecx, 0x2e0
004A3441  e8 9a 57 01 00           call     0x4b8be0
004A3446  66 8b 00                 mov      ax, word ptr [eax]
004A3449  8b cb                    mov      ecx, ebx
004A344B  c1 e1 0d                 shl      ecx, 0xd
004A344E  66 2b c1                 sub      ax, cx
004A3451  0f bf c0                 movsx    eax, ax
004A3454  99                       cdq      
004A3455  8b f0                    mov      esi, eax
004A3457  33 c0                    xor      eax, eax
004A3459  33 f2                    xor      esi, edx
004A345B  2b f2                    sub      esi, edx
004A345D  99                       cdq      
004A345E  33 c2                    xor      eax, edx
004A3460  2b c2                    sub      eax, edx
004A3462  3b c6                    cmp      eax, esi
004A3464  7d 20                    jge      0x4a3486
004A3466  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004A346A  66 89 4c 24 68           mov      word ptr [esp + 0x68], cx
004A346F  8b 54 24 68              mov      edx, dword ptr [esp + 0x68]
004A3473  8b 08                    mov      ecx, dword ptr [eax]
004A3475  52                       push     edx
004A3476  50                       push     eax
004A3477  ff 51 4c                 call     dword ptr [ecx + 0x4c]
004A347A  5f                       pop      edi
004A347B  5e                       pop      esi
004A347C  5d                       pop      ebp
004A347D  b0 01                    mov      al, 1
004A347F  5b                       pop      ebx
004A3480  83 c4 4c                 add      esp, 0x4c
004A3483  c2 0c 00                 ret      0xc
004A3486  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004A348A  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A348E  99                       cdq      
004A348F  81 e2 ff 00 00 00        and      edx, 0xff
004A3495  51                       push     ecx
004A3496  03 c2                    add      eax, edx
004A3498  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A349D  c1 f8 08                 sar      eax, 8
004A34A0  66 89 44 24 1c           mov      word ptr [esp + 0x1c], ax
004A34A5  8b 44 24 40              mov      eax, dword ptr [esp + 0x40]
004A34A9  99                       cdq      
004A34AA  81 e2 ff 00 00 00        and      edx, 0xff
004A34B0  03 c2                    add      eax, edx
004A34B2  c1 f8 08                 sar      eax, 8
004A34B5  66 89 44 24 1e           mov      word ptr [esp + 0x1e], ax
004A34BA  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
004A34BE  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004A34C2  e8 a9 4b 0a 00           call     0x548070
004A34C7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A34CA  8b f0                    mov      esi, eax
004A34CC  6a 00                    push     0
004A34CE  89 74 24 30              mov      dword ptr [esp + 0x30], esi
004A34D2  8b 11                    mov      edx, dword ptr [ecx]
004A34D4  c6 44 24 17 00           mov      byte ptr [esp + 0x17], 0
004A34D9  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004A34DF  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A34E2  6a 01                    push     1
004A34E4  6a 00                    push     0
004A34E6  57                       push     edi
004A34E7  8b 01                    mov      eax, dword ptr [ecx]
004A34E9  53                       push     ebx
004A34EA  56                       push     esi
004A34EB  ff 90 94 01 00 00        call     dword ptr [eax + 0x194]
004A34F1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A34F4  6a 01                    push     1
004A34F6  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
004A34FA  8b 11                    mov      edx, dword ptr [ecx]
004A34FC  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004A3502  83 7c 24 18 07           cmp      dword ptr [esp + 0x18], 7
004A3507  7d 15                    jge      0x4a351e
004A3509  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A350C  8b 01                    mov      eax, dword ptr [ecx]
004A350E  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A3514  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A351A  84 c9                    test     cl, cl
004A351C  75 2a                    jne      0x4a3548
004A351E  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004A3522  83 f8 05                 cmp      eax, 5
004A3525  74 05                    je       0x4a352c
004A3527  83 f8 04                 cmp      eax, 4
004A352A  75 24                    jne      0x4a3550
004A352C  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A352F  8b 11                    mov      edx, dword ptr [ecx]
004A3531  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004A3537  8a 88 f3 0a 00 00        mov      cl, byte ptr [eax + 0xaf3]
004A353D  84 c9                    test     cl, cl
004A353F  74 0f                    je       0x4a3550
004A3541  8b 46 44                 mov      eax, dword ptr [esi + 0x44]
004A3544  85 c0                    test     eax, eax
004A3546  75 08                    jne      0x4a3550
004A3548  c7 44 24 18 00 00 00 00  mov      dword ptr [esp + 0x18], 0
004A3550  8b 46 44                 mov      eax, dword ptr [esi + 0x44]
004A3553  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004A3557  83 ce ff                 or       esi, 0xffffffff
004A355A  3b c6                    cmp      eax, esi
004A355C  74 78                    je       0x4a35d6
004A355E  85 c9                    test     ecx, ecx
004A3560  75 78                    jne      0x4a35da
004A3562  8b 0d ec 5d a3 00        mov      ecx, dword ptr [0xa35dec]
004A3568  8b 14 81                 mov      edx, dword ptr [ecx + eax*4]
004A356B  8a 82 fd 01 00 00        mov      al, byte ptr [edx + 0x1fd]
004A3571  84 c0                    test     al, al
004A3573  74 05                    je       0x4a357a
004A3575  c6 44 24 13 01           mov      byte ptr [esp + 0x13], 1
004A357A  8d 54 24 14              lea      edx, [esp + 0x14]
004A357E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3583  52                       push     edx
004A3584  e8 e7 4a 0a 00           call     0x548070
004A3589  0f be 88 1b 01 00 00     movsx    ecx, byte ptr [eax + 0x11b]
004A3590  8b c7                    mov      eax, edi
004A3592  2b c1                    sub      eax, ecx
004A3594  99                       cdq      
004A3595  33 c2                    xor      eax, edx
004A3597  2b c2                    sub      eax, edx
004A3599  83 f8 02                 cmp      eax, 2
004A359C  0f 8d f0 06 00 00        jge      0x4a3c92
004A35A2  8d 54 24 14              lea      edx, [esp + 0x14]
004A35A6  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A35AB  52                       push     edx
004A35AC  e8 bf 4a 0a 00           call     0x548070
004A35B1  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
004A35B8  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A35BC  89 44 24 28              mov      dword ptr [esp + 0x28], eax
004A35C0  51                       push     ecx
004A35C1  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A35C6  e8 a5 4a 0a 00           call     0x548070
004A35CB  8b b0 ec 00 00 00        mov      esi, dword ptr [eax + 0xec]
004A35D1  e9 c5 06 00 00           jmp      0x4a3c9b
004A35D6  85 c9                    test     ecx, ecx
004A35D8  74 a0                    je       0x4a357a
004A35DA  83 f9 03                 cmp      ecx, 3
004A35DD  0f 85 0a 01 00 00        jne      0x4a36ed
004A35E3  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A35E6  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
004A35EA  8d 4c 24 68              lea      ecx, [esp + 0x68]
004A35EE  89 44 24 68              mov      dword ptr [esp + 0x68], eax
004A35F2  51                       push     ecx
004A35F3  52                       push     edx
004A35F4  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A35F9  e8 d2 76 0b 00           call     0x55acd0
004A35FE  33 ff                    xor      edi, edi
004A3600  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A3605  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A3608  8d 5d 40                 lea      ebx, [ebp + 0x40]
004A360B  3b c8                    cmp      ecx, eax
004A360D  75 1a                    jne      0x4a3629
004A360F  8b 4b 04                 mov      ecx, dword ptr [ebx + 4]
004A3612  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3618  3b ca                    cmp      ecx, edx
004A361A  75 0d                    jne      0x4a3629
004A361C  8b 53 08                 mov      edx, dword ptr [ebx + 8]
004A361F  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A3625  3b d1                    cmp      edx, ecx
004A3627  74 19                    je       0x4a3642
004A3629  8b cb                    mov      ecx, ebx
004A362B  89 01                    mov      dword ptr [ecx], eax
004A362D  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3633  89 51 04                 mov      dword ptr [ecx + 4], edx
004A3636  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A363B  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A363F  89 41 08                 mov      dword ptr [ecx + 8], eax
004A3642  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004A3646  83 f8 02                 cmp      eax, 2
004A3649  0f 85 3f 04 00 00        jne      0x4a3a8e
004A364F  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A3652  8a 88 a1 05 00 00        mov      cl, byte ptr [eax + 0x5a1]
004A3658  84 c9                    test     cl, cl
004A365A  75 2d                    jne      0x4a3689
004A365C  c6 80 a1 05 00 00 01     mov      byte ptr [eax + 0x5a1], 1
004A3663  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3666  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A366C  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A3671  81 c2 58 05 00 00        add      edx, 0x558
004A3677  8b 89 d0 13 00 00        mov      ecx, dword ptr [ecx + 0x13d0]
004A367D  89 02                    mov      dword ptr [edx], eax
004A367F  8b 44 24 54              mov      eax, dword ptr [esp + 0x54]
004A3683  89 42 04                 mov      dword ptr [edx + 4], eax
004A3686  89 4a 08                 mov      dword ptr [edx + 8], ecx
004A3689  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A368C  8b 3d 2c 0d a4 00        mov      edi, dword ptr [0xa40d2c]
004A3692  8b b1 30 05 00 00        mov      esi, dword ptr [ecx + 0x530]
004A3698  8b 81 38 05 00 00        mov      eax, dword ptr [ecx + 0x538]
004A369E  83 fe ff                 cmp      esi, -1
004A36A1  74 0a                    je       0x4a36ad
004A36A3  8b d7                    mov      edx, edi
004A36A5  2b d6                    sub      edx, esi
004A36A7  3b d0                    cmp      edx, eax
004A36A9  7d 0a                    jge      0x4a36b5
004A36AB  2b c2                    sub      eax, edx
004A36AD  85 c0                    test     eax, eax
004A36AF  0f 85 e3 03 00 00        jne      0x4a3a98
004A36B5  8a 81 a1 05 00 00        mov      al, byte ptr [ecx + 0x5a1]
004A36BB  84 c0                    test     al, al
004A36BD  0f 84 05 03 00 00        je       0x4a39c8
004A36C3  8b 91 58 05 00 00        mov      edx, dword ptr [ecx + 0x558]
004A36C9  8b 81 60 05 00 00        mov      eax, dword ptr [ecx + 0x560]
004A36CF  83 fa ff                 cmp      edx, -1
004A36D2  74 0a                    je       0x4a36de
004A36D4  2b fa                    sub      edi, edx
004A36D6  8b d7                    mov      edx, edi
004A36D8  3b d0                    cmp      edx, eax
004A36DA  7d 0a                    jge      0x4a36e6
004A36DC  2b c2                    sub      eax, edx
004A36DE  85 c0                    test     eax, eax
004A36E0  0f 85 e2 02 00 00        jne      0x4a39c8
004A36E6  b3 01                    mov      bl, 1
004A36E8  e9 dd 02 00 00           jmp      0x4a39ca
004A36ED  83 f9 06                 cmp      ecx, 6
004A36F0  0f 85 45 02 00 00        jne      0x4a393b
004A36F6  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A36F9  8b 01                    mov      eax, dword ptr [ecx]
004A36FB  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A3701  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A3707  84 c9                    test     cl, cl
004A3709  0f 85 ef fe ff ff        jne      0x4a35fe
004A370F  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A3713  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3716  84 c0                    test     al, al
004A3718  74 21                    je       0x4a373b
004A371A  89 b1 d0 04 00 00        mov      dword ptr [ecx + 0x4d0], esi
004A3720  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3723  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A3728  33 c9                    xor      ecx, ecx
004A372A  81 c2 30 05 00 00        add      edx, 0x530
004A3730  89 02                    mov      dword ptr [edx], eax
004A3732  8b 44 24 48              mov      eax, dword ptr [esp + 0x48]
004A3736  e9 c7 0d 00 00           jmp      0x4a4502
004A373B  8b 11                    mov      edx, dword ptr [ecx]
004A373D  8d 44 24 44              lea      eax, [esp + 0x44]
004A3741  50                       push     eax
004A3742  ff 52 48                 call     dword ptr [edx + 0x48]
004A3745  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A3748  8b 7d 3c                 mov      edi, dword ptr [ebp + 0x3c]
004A374B  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A374E  8b 5d 38                 mov      ebx, dword ptr [ebp + 0x38]
004A3751  8b 00                    mov      eax, dword ptr [eax]
004A3753  2b cf                    sub      ecx, edi
004A3755  2b d3                    sub      edx, ebx
004A3757  51                       push     ecx
004A3758  52                       push     edx
004A3759  8b 55 34                 mov      edx, dword ptr [ebp + 0x34]
004A375C  2b c2                    sub      eax, edx
004A375E  8d 4c 24 58              lea      ecx, [esp + 0x58]
004A3762  50                       push     eax
004A3763  e8 c8 7e f7 ff           call     0x41b630
004A3768  8b 08                    mov      ecx, dword ptr [eax]
004A376A  83 ec 08                 sub      esp, 8
004A376D  89 4c 24 34              mov      dword ptr [esp + 0x34], ecx
004A3771  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A3774  db 44 24 34              fild     dword ptr [esp + 0x34]
004A3778  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A377B  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A377F  db 44 24 38              fild     dword ptr [esp + 0x38]
004A3783  89 44 24 3c              mov      dword ptr [esp + 0x3c], eax
004A3787  db 44 24 3c              fild     dword ptr [esp + 0x3c]
004A378B  d9 c0                    fld      st(0)
004A378D  d8 c9                    fmul     st(1)
004A378F  d9 c2                    fld      st(2)
004A3791  d8 cb                    fmul     st(3)
004A3793  de c1                    faddp    st(1)
004A3795  d9 c3                    fld      st(3)
004A3797  d8 cc                    fmul     st(4)
004A3799  de c1                    faddp    st(1)
004A379B  dd 1c 24                 fstp     qword ptr [esp]
004A379E  dd d8                    fstp     st(0)
004A37A0  dd d8                    fstp     st(0)
004A37A2  dd d8                    fstp     st(0)
004A37A4  e8 67 6c 01 00           call     0x4ba410
004A37A9  83 c4 08                 add      esp, 8
004A37AC  e8 5f b9 2d 00           call     0x77f110
004A37B1  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A37B7  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A37BD  0f 8d e7 00 00 00        jge      0x4a38aa
004A37C3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A37C6  81 c1 88 00 00 00        add      ecx, 0x88
004A37CC  8b d1                    mov      edx, ecx
004A37CE  8b 02                    mov      eax, dword ptr [edx]
004A37D0  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A37D4  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A37D7  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A37DB  8b 45 3c                 mov      eax, dword ptr [ebp + 0x3c]
004A37DE  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A37E1  2b c2                    sub      eax, edx
004A37E3  99                       cdq      
004A37E4  33 c2                    xor      eax, edx
004A37E6  2b c2                    sub      eax, edx
004A37E8  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A37EE  03 d2                    add      edx, edx
004A37F0  3b c2                    cmp      eax, edx
004A37F2  0f 8d b2 00 00 00        jge      0x4a38aa
004A37F8  8b 01                    mov      eax, dword ptr [ecx]
004A37FA  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004A37FE  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A3801  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A3805  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A3808  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A380C  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A3810  51                       push     ecx
004A3811  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3816  e8 e5 47 0a 00           call     0x548000
004A381B  83 b8 ec 00 00 00 0a     cmp      dword ptr [eax + 0xec], 0xa
004A3822  0f 84 82 00 00 00        je       0x4a38aa
004A3828  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A382D  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A3830  3b c8                    cmp      ecx, eax
004A3832  75 1a                    jne      0x4a384e
004A3834  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A3837  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A383D  3b d1                    cmp      edx, ecx
004A383F  75 0d                    jne      0x4a384e
004A3841  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A3844  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A384A  3b ca                    cmp      ecx, edx
004A384C  74 18                    je       0x4a3866
004A384E  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A3851  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3857  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A385A  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A385F  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A3862  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A3866  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3869  33 ff                    xor      edi, edi
004A386B  39 b9 88 04 00 00        cmp      dword ptr [ecx + 0x488], edi
004A3871  75 10                    jne      0x4a3883
004A3873  8b 11                    mov      edx, dword ptr [ecx]
004A3875  6a 01                    push     1
004A3877  57                       push     edi
004A3878  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A387E  e9 7d fd ff ff           jmp      0x4a3600
004A3883  e8 28 a1 02 00           call     0x4cd9b0
004A3888  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A388B  6a 01                    push     1
004A388D  57                       push     edi
004A388E  8b 01                    mov      eax, dword ptr [ecx]
004A3890  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A3896  84 c0                    test     al, al
004A3898  0f 84 62 fd ff ff        je       0x4a3600
004A389E  5f                       pop      edi
004A389F  5e                       pop      esi
004A38A0  5d                       pop      ebp
004A38A1  b0 01                    mov      al, 1
004A38A3  5b                       pop      ebx
004A38A4  83 c4 4c                 add      esp, 0x4c
004A38A7  c2 0c 00                 ret      0xc
004A38AA  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A38AE  51                       push     ecx
004A38AF  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A38B4  e8 b7 47 0a 00           call     0x548070
004A38B9  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004A38BF  f6 c5 01                 test     ch, 1
004A38C2  74 49                    je       0x4a390d
004A38C4  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A38C7  81 c2 88 00 00 00        add      edx, 0x88
004A38CD  8b 02                    mov      eax, dword ptr [edx]
004A38CF  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A38D3  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A38D6  89 4c 24 48              mov      dword ptr [esp + 0x48], ecx
004A38DA  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A38DF  8b 7a 08                 mov      edi, dword ptr [edx + 8]
004A38E2  8d 54 24 14              lea      edx, [esp + 0x14]
004A38E6  52                       push     edx
004A38E7  e8 84 47 0a 00           call     0x548070
004A38EC  0f be 88 1b 01 00 00     movsx    ecx, byte ptr [eax + 0x11b]
004A38F3  8b c7                    mov      eax, edi
004A38F5  c6 44 24 68 01           mov      byte ptr [esp + 0x68], 1
004A38FA  99                       cdq      
004A38FB  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A3901  2b c1                    sub      eax, ecx
004A3903  99                       cdq      
004A3904  33 c2                    xor      eax, edx
004A3906  2b c2                    sub      eax, edx
004A3908  83 f8 02                 cmp      eax, 2
004A390B  7f 05                    jg       0x4a3912
004A390D  c6 44 24 68 00           mov      byte ptr [esp + 0x68], 0
004A3912  8b 54 24 68              mov      edx, dword ptr [esp + 0x68]
004A3916  8d 44 24 14              lea      eax, [esp + 0x14]
004A391A  52                       push     edx
004A391B  6a 01                    push     1
004A391D  6a 01                    push     1
004A391F  68 98 29 85 00           push     0x852998
004A3924  50                       push     eax
004A3925  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A392A  e8 41 47 0a 00           call     0x548070
004A392F  8b c8                    mov      ecx, eax
004A3931  e8 ea 2f fd ff           call     0x476920
004A3936  e9 c3 fc ff ff           jmp      0x4a35fe
004A393B  83 f9 01                 cmp      ecx, 1
004A393E  0f 85 ba fc ff ff        jne      0x4a35fe
004A3944  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A3948  51                       push     ecx
004A3949  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A394E  e8 1d 47 0a 00           call     0x548070
004A3953  8b c8                    mov      ecx, eax
004A3955  e8 e6 4d fd ff           call     0x478740
004A395A  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A395E  84 c0                    test     al, al
004A3960  74 23                    je       0x4a3985
004A3962  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3965  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
004A3969  6a 00                    push     0
004A396B  6a 00                    push     0
004A396D  50                       push     eax
004A396E  8b cd                    mov      ecx, ebp
004A3970  89 b2 d0 04 00 00        mov      dword ptr [edx + 0x4d0], esi
004A3976  e8 f5 ec ff ff           call     0x4a2670
004A397B  5f                       pop      edi
004A397C  5e                       pop      esi
004A397D  5d                       pop      ebp
004A397E  5b                       pop      ebx
004A397F  83 c4 4c                 add      esp, 0x4c
004A3982  c2 0c 00                 ret      0xc
004A3985  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A398A  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A398D  3b c8                    cmp      ecx, eax
004A398F  75 1e                    jne      0x4a39af
004A3991  8b 4d 44                 mov      ecx, dword ptr [ebp + 0x44]
004A3994  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A399A  3b ca                    cmp      ecx, edx
004A399C  75 11                    jne      0x4a39af
004A399E  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A39A1  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A39A7  3b d1                    cmp      edx, ecx
004A39A9  0f 84 7f f8 ff ff        je       0x4a322e
004A39AF  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A39B2  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A39B7  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A39BA  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A39C0  89 4d 48                 mov      dword ptr [ebp + 0x48], ecx
004A39C3  e9 62 f8 ff ff           jmp      0x4a322a
004A39C8  32 db                    xor      bl, bl
004A39CA  8b 45 34                 mov      eax, dword ptr [ebp + 0x34]
004A39CD  8d 75 34                 lea      esi, [ebp + 0x34]
004A39D0  99                       cdq      
004A39D1  81 e2 ff 00 00 00        and      edx, 0xff
004A39D7  03 c2                    add      eax, edx
004A39D9  c1 f8 08                 sar      eax, 8
004A39DC  66 89 44 24 68           mov      word ptr [esp + 0x68], ax
004A39E1  8b 46 04                 mov      eax, dword ptr [esi + 4]
004A39E4  99                       cdq      
004A39E5  81 e2 ff 00 00 00        and      edx, 0xff
004A39EB  03 c2                    add      eax, edx
004A39ED  33 d2                    xor      edx, edx
004A39EF  c1 f8 08                 sar      eax, 8
004A39F2  84 db                    test     bl, bl
004A39F4  0f 95 c2                 setne    dl
004A39F7  42                       inc      edx
004A39F8  66 89 44 24 6a           mov      word ptr [esp + 0x6a], ax
004A39FD  8b 44 24 68              mov      eax, dword ptr [esp + 0x68]
004A3A01  52                       push     edx
004A3A02  6a 00                    push     0
004A3A04  50                       push     eax
004A3A05  e8 f6 f5 01 00           call     0x4c3000
004A3A0A  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3A0D  85 c9                    test     ecx, ecx
004A3A0F  75 13                    jne      0x4a3a24
004A3A11  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
004A3A15  5f                       pop      edi
004A3A16  5e                       pop      esi
004A3A17  5d                       pop      ebp
004A3A18  c6 01 01                 mov      byte ptr [ecx], 1
004A3A1B  32 c0                    xor      al, al
004A3A1D  5b                       pop      ebx
004A3A1E  83 c4 4c                 add      esp, 0x4c
004A3A21  c2 0c 00                 ret      0xc
004A3A24  84 c0                    test     al, al
004A3A26  75 28                    jne      0x4a3a50
004A3A28  8b 11                    mov      edx, dword ptr [ecx]
004A3A2A  56                       push     esi
004A3A2B  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004A3A31  84 c0                    test     al, al
004A3A33  75 1b                    jne      0x4a3a50
004A3A35  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3A38  8b 01                    mov      eax, dword ptr [ecx]
004A3A3A  6a 01                    push     1
004A3A3C  6a 00                    push     0
004A3A3E  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A3A44  5f                       pop      edi
004A3A45  5e                       pop      esi
004A3A46  5d                       pop      ebp
004A3A47  32 c0                    xor      al, al
004A3A49  5b                       pop      ebx
004A3A4A  83 c4 4c                 add      esp, 0x4c
004A3A4D  c2 0c 00                 ret      0xc
004A3A50  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A3A56  8b 35 2c 0d a4 00        mov      esi, dword ptr [0xa40d2c]
004A3A5C  dd 81 c8 13 00 00        fld      qword ptr [ecx + 0x13c8]
004A3A62  dc 0d 08 b6 79 00        fmul     qword ptr [0x79b608]
004A3A68  e8 a3 b6 2d 00           call     0x77f110
004A3A6D  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3A70  8b 4c 24 54              mov      ecx, dword ptr [esp + 0x54]
004A3A74  81 c2 30 05 00 00        add      edx, 0x530
004A3A7A  5f                       pop      edi
004A3A7B  89 32                    mov      dword ptr [edx], esi
004A3A7D  5e                       pop      esi
004A3A7E  5d                       pop      ebp
004A3A7F  5b                       pop      ebx
004A3A80  89 4a 04                 mov      dword ptr [edx + 4], ecx
004A3A83  89 42 08                 mov      dword ptr [edx + 8], eax
004A3A86  b0 01                    mov      al, 1
004A3A88  83 c4 4c                 add      esp, 0x4c
004A3A8B  c2 0c 00                 ret      0xc
004A3A8E  83 f8 05                 cmp      eax, 5
004A3A91  74 3c                    je       0x4a3acf
004A3A93  83 f8 04                 cmp      eax, 4
004A3A96  74 32                    je       0x4a3aca
004A3A98  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3A9B  8a 82 7a 05 00 00        mov      al, byte ptr [edx + 0x57a]
004A3AA1  84 c0                    test     al, al
004A3AA3  0f 84 54 01 00 00        je       0x4a3bfd
004A3AA9  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A3AAE  6a 00                    push     0
004A3AB0  ba 00 20 00 00           mov      edx, 0x2000
004A3AB5  68 00 00 80 3f           push     0x3f800000
004A3ABA  8b 88 20 06 00 00        mov      ecx, dword ptr [eax + 0x620]
004A3AC0  e8 eb 02 27 00           call     0x713db0
004A3AC5  e9 33 01 00 00           jmp      0x4a3bfd
004A3ACA  83 ce ff                 or       esi, 0xffffffff
004A3ACD  33 ff                    xor      edi, edi
004A3ACF  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A3AD3  84 c0                    test     al, al
004A3AD5  74 3d                    je       0x4a3b14
004A3AD7  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3ADA  57                       push     edi
004A3ADB  57                       push     edi
004A3ADC  89 b1 d0 04 00 00        mov      dword ptr [ecx + 0x4d0], esi
004A3AE2  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3AE5  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A3AEA  81 c2 30 05 00 00        add      edx, 0x530
004A3AF0  33 c9                    xor      ecx, ecx
004A3AF2  89 02                    mov      dword ptr [edx], eax
004A3AF4  8b 44 24 5c              mov      eax, dword ptr [esp + 0x5c]
004A3AF8  89 42 04                 mov      dword ptr [edx + 4], eax
004A3AFB  89 4a 08                 mov      dword ptr [edx + 8], ecx
004A3AFE  8b 4c 24 68              mov      ecx, dword ptr [esp + 0x68]
004A3B02  51                       push     ecx
004A3B03  8b cd                    mov      ecx, ebp
004A3B05  e8 66 eb ff ff           call     0x4a2670
004A3B0A  5f                       pop      edi
004A3B0B  5e                       pop      esi
004A3B0C  5d                       pop      ebp
004A3B0D  5b                       pop      ebx
004A3B0E  83 c4 4c                 add      esp, 0x4c
004A3B11  c2 0c 00                 ret      0xc
004A3B14  8d 54 24 2c              lea      edx, [esp + 0x2c]
004A3B18  57                       push     edi
004A3B19  8d 44 24 18              lea      eax, [esp + 0x18]
004A3B1D  52                       push     edx
004A3B1E  50                       push     eax
004A3B1F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3B24  89 7c 24 38              mov      dword ptr [esp + 0x38], edi
004A3B28  89 7c 24 3c              mov      dword ptr [esp + 0x3c], edi
004A3B2C  e8 3f 45 0a 00           call     0x548070
004A3B31  8b c8                    mov      ecx, eax
004A3B33  e8 f8 dc fc ff           call     0x471830
004A3B38  85 c0                    test     eax, eax
004A3B3A  74 67                    je       0x4a3ba3
004A3B3C  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A3B40  57                       push     edi
004A3B41  8d 54 24 18              lea      edx, [esp + 0x18]
004A3B45  51                       push     ecx
004A3B46  52                       push     edx
004A3B47  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3B4C  89 7c 24 38              mov      dword ptr [esp + 0x38], edi
004A3B50  89 7c 24 3c              mov      dword ptr [esp + 0x3c], edi
004A3B54  e8 17 45 0a 00           call     0x548070
004A3B59  8b c8                    mov      ecx, eax
004A3B5B  e8 d0 dc fc ff           call     0x471830
004A3B60  50                       push     eax
004A3B61  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A3B64  8b 88 b4 01 00 00        mov      ecx, dword ptr [eax + 0x1b4]
004A3B6A  e8 11 1a 04 00           call     0x4e5580
004A3B6F  84 c0                    test     al, al
004A3B71  0f 85 86 00 00 00        jne      0x4a3bfd
004A3B77  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3B7A  57                       push     edi
004A3B7B  8d 54 24 30              lea      edx, [esp + 0x30]
004A3B7F  89 7c 24 30              mov      dword ptr [esp + 0x30], edi
004A3B83  89 7c 24 34              mov      dword ptr [esp + 0x34], edi
004A3B87  8b 31                    mov      esi, dword ptr [ecx]
004A3B89  57                       push     edi
004A3B8A  8d 44 24 1c              lea      eax, [esp + 0x1c]
004A3B8E  52                       push     edx
004A3B8F  50                       push     eax
004A3B90  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3B95  e8 d6 44 0a 00           call     0x548070
004A3B9A  8b c8                    mov      ecx, eax
004A3B9C  e8 8f dc fc ff           call     0x471830
004A3BA1  eb 4e                    jmp      0x4a3bf1
004A3BA3  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A3BA7  51                       push     ecx
004A3BA8  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3BAD  e8 be 44 0a 00           call     0x548070
004A3BB2  39 70 44                 cmp      dword ptr [eax + 0x44], esi
004A3BB5  74 46                    je       0x4a3bfd
004A3BB7  8d 54 24 14              lea      edx, [esp + 0x14]
004A3BBB  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3BC0  52                       push     edx
004A3BC1  e8 aa 44 0a 00           call     0x548070
004A3BC6  8b 40 44                 mov      eax, dword ptr [eax + 0x44]
004A3BC9  8b 0d ec 5d a3 00        mov      ecx, dword ptr [0xa35dec]
004A3BCF  8b 14 81                 mov      edx, dword ptr [ecx + eax*4]
004A3BD2  8a 82 78 02 00 00        mov      al, byte ptr [edx + 0x278]
004A3BD8  84 c0                    test     al, al
004A3BDA  74 21                    je       0x4a3bfd
004A3BDC  8b 45 0c                 mov      eax, dword ptr [ebp + 0xc]
004A3BDF  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A3BE3  57                       push     edi
004A3BE4  51                       push     ecx
004A3BE5  8b 30                    mov      esi, dword ptr [eax]
004A3BE7  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3BEC  e8 7f 44 0a 00           call     0x548070
004A3BF1  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3BF4  50                       push     eax
004A3BF5  6a 01                    push     1
004A3BF7  ff 96 dc 01 00 00        call     dword ptr [esi + 0x1dc]
004A3BFD  83 7c 24 18 07           cmp      dword ptr [esp + 0x18], 7
004A3C02  75 71                    jne      0x4a3c75
004A3C04  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A3C08  84 c0                    test     al, al
004A3C0A  74 28                    je       0x4a3c34
004A3C0C  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3C0F  33 c9                    xor      ecx, ecx
004A3C11  c7 82 d0 04 00 00 ff ff ff ff mov      dword ptr [edx + 0x4d0], 0xffffffff
004A3C1B  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3C1E  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A3C23  81 c2 30 05 00 00        add      edx, 0x530
004A3C29  89 02                    mov      dword ptr [edx], eax
004A3C2B  8b 44 24 54              mov      eax, dword ptr [esp + 0x54]
004A3C2F  e9 ce 08 00 00           jmp      0x4a4502
004A3C34  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A3C39  8b 0b                    mov      ecx, dword ptr [ebx]
004A3C3B  3b c8                    cmp      ecx, eax
004A3C3D  75 1e                    jne      0x4a3c5d
004A3C3F  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3C45  8b 4b 04                 mov      ecx, dword ptr [ebx + 4]
004A3C48  3b ca                    cmp      ecx, edx
004A3C4A  75 11                    jne      0x4a3c5d
004A3C4C  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A3C52  8b 53 08                 mov      edx, dword ptr [ebx + 8]
004A3C55  3b d1                    cmp      edx, ecx
004A3C57  0f 84 d1 f5 ff ff        je       0x4a322e
004A3C5D  89 03                    mov      dword ptr [ebx], eax
004A3C5F  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3C65  89 53 04                 mov      dword ptr [ebx + 4], edx
004A3C68  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A3C6D  89 43 08                 mov      dword ptr [ebx + 8], eax
004A3C70  e9 b5 f5 ff ff           jmp      0x4a322a
004A3C75  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3C78  5f                       pop      edi
004A3C79  5e                       pop      esi
004A3C7A  b0 01                    mov      al, 1
004A3C7C  c6 81 7a 05 00 00 00     mov      byte ptr [ecx + 0x57a], 0
004A3C83  c7 45 58 ff ff ff ff     mov      dword ptr [ebp + 0x58], 0xffffffff
004A3C8A  5d                       pop      ebp
004A3C8B  5b                       pop      ebx
004A3C8C  83 c4 4c                 add      esp, 0x4c
004A3C8F  c2 0c 00                 ret      0xc
004A3C92  89 7c 24 28              mov      dword ptr [esp + 0x28], edi
004A3C96  be 01 00 00 00           mov      esi, 1
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
