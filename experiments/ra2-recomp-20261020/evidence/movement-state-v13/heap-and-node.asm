
sub_004278C7 0x00427900 size=1600
00427900  54                       push     esp
00427901  24 64                    and      al, 0x64
00427903  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427907  51                       push     ecx
00427908  52                       push     edx
00427909  57                       push     edi
0042790A  50                       push     eax
0042790B  8b ce                    mov      ecx, esi
0042790D  e8 2e 04 00 00           call     0x427d40
00427912  8b d8                    mov      ebx, eax
00427914  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00427918  85 c0                    test     eax, eax
0042791A  89 5c 24 24              mov      dword ptr [esp + 0x24], ebx
0042791E  75 09                    jne      0x427929
00427920  89 5c 24 1c              mov      dword ptr [esp + 0x1c], ebx
00427924  e9 d9 00 00 00           jmp      0x427a02
00427929  d9 43 08                 fld      dword ptr [ebx + 8]
0042792C  d8 58 08                 fcomp    dword ptr [eax + 8]
0042792F  8b 7e 14                 mov      edi, dword ptr [esi + 0x14]
00427932  8b 0f                    mov      ecx, dword ptr [edi]
00427934  df e0                    fnstsw   ax
00427936  f6 c4 01                 test     ah, 1
00427939  41                       inc      ecx
0042793A  8b d1                    mov      edx, ecx
0042793C  74 6c                    je       0x4279aa
0042793E  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00427942  d1 ea                    shr      edx, 1
00427944  8b 40 08                 mov      eax, dword ptr [eax + 8]
00427947  89 44 24 44              mov      dword ptr [esp + 0x44], eax
0042794B  8b 47 04                 mov      eax, dword ptr [edi + 4]
0042794E  3b c8                    cmp      ecx, eax
00427950  73 52                    jae      0x4279a4
00427952  83 f9 01                 cmp      ecx, 1
00427955  76 2c                    jbe      0x427983
00427957  8b 6f 08                 mov      ebp, dword ptr [edi + 8]
0042795A  8b 5c 95 00              mov      ebx, dword ptr [ebp + edx*4]
0042795E  d9 43 08                 fld      dword ptr [ebx + 8]
00427961  d8 5c 24 44              fcomp    dword ptr [esp + 0x44]
00427965  df e0                    fnstsw   ax
00427967  f6 c4 41                 test     ah, 0x41
0042796A  75 0d                    jne      0x427979
0042796C  89 5c 8d 00              mov      dword ptr [ebp + ecx*4], ebx
00427970  8b ca                    mov      ecx, edx
00427972  d1 ea                    shr      edx, 1
00427974  83 f9 01                 cmp      ecx, 1
00427977  77 de                    ja       0x427957
00427979  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
0042797D  8b 5c 24 24              mov      ebx, dword ptr [esp + 0x24]
00427981  eb 04                    jmp      0x427987
00427983  8b 44 24 1c              mov      eax, dword ptr [esp + 0x1c]
00427987  8b 57 08                 mov      edx, dword ptr [edi + 8]
0042798A  89 04 8a                 mov      dword ptr [edx + ecx*4], eax
0042798D  8b 17                    mov      edx, dword ptr [edi]
0042798F  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
00427992  42                       inc      edx
00427993  3b c1                    cmp      eax, ecx
00427995  89 17                    mov      dword ptr [edi], edx
00427997  76 03                    jbe      0x42799c
00427999  89 47 0c                 mov      dword ptr [edi + 0xc], eax
0042799C  3b 47 10                 cmp      eax, dword ptr [edi + 0x10]
0042799F  73 03                    jae      0x4279a4
004279A1  89 47 10                 mov      dword ptr [edi + 0x10], eax
004279A4  89 5c 24 1c              mov      dword ptr [esp + 0x1c], ebx
004279A8  eb 58                    jmp      0x427a02
004279AA  8b 43 08                 mov      eax, dword ptr [ebx + 8]
004279AD  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004279B1  8b 47 04                 mov      eax, dword ptr [edi + 4]
004279B4  d1 ea                    shr      edx, 1
004279B6  3b c8                    cmp      ecx, eax
004279B8  73 48                    jae      0x427a02
004279BA  83 f9 01                 cmp      ecx, 1
004279BD  76 22                    jbe      0x4279e1
004279BF  8b 6f 08                 mov      ebp, dword ptr [edi + 8]
004279C2  8b 5c 95 00              mov      ebx, dword ptr [ebp + edx*4]
004279C6  d9 43 08                 fld      dword ptr [ebx + 8]
004279C9  d8 5c 24 48              fcomp    dword ptr [esp + 0x48]
004279CD  df e0                    fnstsw   ax
004279CF  f6 c4 41                 test     ah, 0x41
004279D2  75 0d                    jne      0x4279e1
004279D4  89 5c 8d 00              mov      dword ptr [ebp + ecx*4], ebx
004279D8  8b ca                    mov      ecx, edx
004279DA  d1 ea                    shr      edx, 1
004279DC  83 f9 01                 cmp      ecx, 1
004279DF  77 de                    ja       0x4279bf
004279E1  8b 57 08                 mov      edx, dword ptr [edi + 8]
004279E4  8b 44 24 24              mov      eax, dword ptr [esp + 0x24]
004279E8  89 04 8a                 mov      dword ptr [edx + ecx*4], eax
004279EB  8b 17                    mov      edx, dword ptr [edi]
004279ED  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004279F0  42                       inc      edx
004279F1  3b c1                    cmp      eax, ecx
004279F3  89 17                    mov      dword ptr [edi], edx
004279F5  76 03                    jbe      0x4279fa
004279F7  89 47 0c                 mov      dword ptr [edi + 0xc], eax
004279FA  3b 47 10                 cmp      eax, dword ptr [edi + 0x10]
004279FD  73 03                    jae      0x427a02
004279FF  89 47 10                 mov      dword ptr [edi + 0x10], eax
00427A02  8a 44 24 60              mov      al, byte ptr [esp + 0x60]
00427A06  84 c0                    test     al, al
00427A08  74 12                    je       0x427a1c
00427A0A  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
00427A0D  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
00427A11  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
00427A14  89 14 01                 mov      dword ptr [ecx + eax], edx
00427A17  8b 4e 24                 mov      ecx, dword ptr [esi + 0x24]
00427A1A  eb 10                    jmp      0x427a2c
00427A1C  8b 4e 1c                 mov      ecx, dword ptr [esi + 0x1c]
00427A1F  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
00427A23  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
00427A26  89 14 01                 mov      dword ptr [ecx + eax], edx
00427A29  8b 4e 20                 mov      ecx, dword ptr [esi + 0x20]
00427A2C  8b 54 24 24              mov      edx, dword ptr [esp + 0x24]
00427A30  8b 52 04                 mov      edx, dword ptr [edx + 4]
00427A33  89 14 01                 mov      dword ptr [ecx + eax], edx
00427A36  8b 46 6c                 mov      eax, dword ptr [esi + 0x6c]
00427A39  8b 54 24 4c              mov      edx, dword ptr [esp + 0x4c]
00427A3D  33 c9                    xor      ecx, ecx
00427A3F  66 8b 8c 46 be 00 00 00  mov      cx, word ptr [esi + eax*2 + 0xbe]
00427A47  3b d1                    cmp      edx, ecx
00427A49  75 33                    jne      0x427a7e
00427A4B  8b 54 24 30              mov      edx, dword ptr [esp + 0x30]
00427A4F  40                       inc      eax
00427A50  89 46 6c                 mov      dword ptr [esi + 0x6c], eax
00427A53  8b 02                    mov      eax, dword ptr [edx]
00427A55  89 46 70                 mov      dword ptr [esi + 0x70], eax
00427A58  eb 24                    jmp      0x427a7e
00427A5A  3b 7c 24 38              cmp      edi, dword ptr [esp + 0x38]
00427A5E  75 1e                    jne      0x427a7e
00427A60  8a 44 24 13              mov      al, byte ptr [esp + 0x13]
00427A64  84 c0                    test     al, al
00427A66  75 16                    jne      0x427a7e
00427A68  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
00427A6B  8b 6e 34                 mov      ebp, dword ptr [esi + 0x34]
00427A6E  2b c5                    sub      eax, ebp
00427A70  99                       cdq      
00427A71  33 c2                    xor      eax, edx
00427A73  2b c2                    sub      eax, edx
00427A75  83 f8 01                 cmp      eax, 1
00427A78  0f 8e 3d 02 00 00        jle      0x427cbb
00427A7E  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00427A82  40                       inc      eax
00427A83  83 f8 08                 cmp      eax, 8
00427A86  89 44 24 18              mov      dword ptr [esp + 0x18], eax
00427A8A  0f 8e 0f fc ff ff        jle      0x42769f
00427A90  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
00427A94  85 c9                    test     ecx, ecx
00427A96  0f 84 fc 00 00 00        je       0x427b98
00427A9C  8b 56 14                 mov      edx, dword ptr [esi + 0x14]
00427A9F  83 3a 00                 cmp      dword ptr [edx], 0
00427AA2  0f 84 ea 01 00 00        je       0x427c92
00427AA8  8b 7a 08                 mov      edi, dword ptr [edx + 8]
00427AAB  d9 41 08                 fld      dword ptr [ecx + 8]
00427AAE  8b 6f 04                 mov      ebp, dword ptr [edi + 4]
00427AB1  d9 45 08                 fld      dword ptr [ebp + 8]
00427AB4  de d9                    fcompp   
00427AB6  89 6c 24 4c              mov      dword ptr [esp + 0x4c], ebp
00427ABA  df e0                    fnstsw   ax
00427ABC  f6 c4 41                 test     ah, 0x41
00427ABF  0f 84 cd 01 00 00        je       0x427c92
00427AC5  89 4f 04                 mov      dword ptr [edi + 4], ecx
00427AC8  8b 3a                    mov      edi, dword ptr [edx]
00427ACA  83 ff 02                 cmp      edi, 2
00427ACD  bb 01 00 00 00           mov      ebx, 1
00427AD2  7c 1d                    jl       0x427af1
00427AD4  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427AD7  8b 48 08                 mov      ecx, dword ptr [eax + 8]
00427ADA  8b 40 04                 mov      eax, dword ptr [eax + 4]
00427ADD  d9 41 08                 fld      dword ptr [ecx + 8]
00427AE0  d9 40 08                 fld      dword ptr [eax + 8]
00427AE3  de d9                    fcompp   
00427AE5  b9 02 00 00 00           mov      ecx, 2
00427AEA  df e0                    fnstsw   ax
00427AEC  f6 c4 41                 test     ah, 0x41
00427AEF  74 05                    je       0x427af6
00427AF1  b9 01 00 00 00           mov      ecx, 1
00427AF6  83 ff 03                 cmp      edi, 3
00427AF9  7c 1f                    jl       0x427b1a
00427AFB  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427AFE  8b 78 0c                 mov      edi, dword ptr [eax + 0xc]
00427B01  8b 04 88                 mov      eax, dword ptr [eax + ecx*4]
00427B04  d9 47 08                 fld      dword ptr [edi + 8]
00427B07  d9 40 08                 fld      dword ptr [eax + 8]
00427B0A  de d9                    fcompp   
00427B0C  df e0                    fnstsw   ax
00427B0E  f6 c4 41                 test     ah, 0x41
00427B11  75 07                    jne      0x427b1a
00427B13  b9 03 00 00 00           mov      ecx, 3
00427B18  eb 05                    jmp      0x427b1f
00427B1A  83 f9 01                 cmp      ecx, 1
00427B1D  74 70                    je       0x427b8f
00427B1F  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427B22  8b 2c 88                 mov      ebp, dword ptr [eax + ecx*4]
00427B25  8b 3c 98                 mov      edi, dword ptr [eax + ebx*4]
00427B28  89 2c 98                 mov      dword ptr [eax + ebx*4], ebp
00427B2B  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427B2E  8b d9                    mov      ebx, ecx
00427B30  89 3c 88                 mov      dword ptr [eax + ecx*4], edi
00427B33  8b 2a                    mov      ebp, dword ptr [edx]
00427B35  8d 3c 09                 lea      edi, [ecx + ecx]
00427B38  8d 44 09 01              lea      eax, [ecx + ecx + 1]
00427B3C  3b fd                    cmp      edi, ebp
00427B3E  89 44 24 60              mov      dword ptr [esp + 0x60], eax
00427B42  7f 1d                    jg       0x427b61
00427B44  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427B47  8b 04 b8                 mov      eax, dword ptr [eax + edi*4]
00427B4A  d9 40 08                 fld      dword ptr [eax + 8]
00427B4D  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427B50  8b 04 88                 mov      eax, dword ptr [eax + ecx*4]
00427B53  d9 40 08                 fld      dword ptr [eax + 8]
00427B56  de d9                    fcompp   
00427B58  df e0                    fnstsw   ax
00427B5A  f6 c4 41                 test     ah, 0x41
00427B5D  75 02                    jne      0x427b61
00427B5F  8b cf                    mov      ecx, edi
00427B61  39 6c 24 60              cmp      dword ptr [esp + 0x60], ebp
00427B65  7f 20                    jg       0x427b87
00427B67  8b 42 08                 mov      eax, dword ptr [edx + 8]
00427B6A  8b 7c 24 60              mov      edi, dword ptr [esp + 0x60]
00427B6E  8b 3c b8                 mov      edi, dword ptr [eax + edi*4]
00427B71  8b 04 88                 mov      eax, dword ptr [eax + ecx*4]
00427B74  d9 47 08                 fld      dword ptr [edi + 8]
00427B77  d9 40 08                 fld      dword ptr [eax + 8]
00427B7A  de d9                    fcompp   
00427B7C  df e0                    fnstsw   ax
00427B7E  f6 c4 41                 test     ah, 0x41
00427B81  75 04                    jne      0x427b87
00427B83  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
00427B87  3b cb                    cmp      ecx, ebx
00427B89  75 94                    jne      0x427b1f
00427B8B  8b 6c 24 4c              mov      ebp, dword ptr [esp + 0x4c]
00427B8F  89 6c 24 14              mov      dword ptr [esp + 0x14], ebp
00427B93  e9 fe 00 00 00           jmp      0x427c96
00427B98  8b 4e 14                 mov      ecx, dword ptr [esi + 0x14]
00427B9B  8b 11                    mov      edx, dword ptr [ecx]
00427B9D  85 d2                    test     edx, edx
00427B9F  75 09                    jne      0x427baa
00427BA1  89 54 24 14              mov      dword ptr [esp + 0x14], edx
00427BA5  e9 fc 00 00 00           jmp      0x427ca6
00427BAA  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427BAD  bb 01 00 00 00           mov      ebx, 1
00427BB2  8b 14 90                 mov      edx, dword ptr [eax + edx*4]
00427BB5  8b 78 04                 mov      edi, dword ptr [eax + 4]
00427BB8  89 50 04                 mov      dword ptr [eax + 4], edx
00427BBB  8b 01                    mov      eax, dword ptr [ecx]
00427BBD  8b 51 08                 mov      edx, dword ptr [ecx + 8]
00427BC0  89 7c 24 4c              mov      dword ptr [esp + 0x4c], edi
00427BC4  c7 04 82 00 00 00 00     mov      dword ptr [edx + eax*4], 0
00427BCB  8b 11                    mov      edx, dword ptr [ecx]
00427BCD  4a                       dec      edx
00427BCE  8b fa                    mov      edi, edx
00427BD0  89 11                    mov      dword ptr [ecx], edx
00427BD2  83 ff 02                 cmp      edi, 2
00427BD5  7c 1d                    jl       0x427bf4
00427BD7  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427BDA  8b 50 08                 mov      edx, dword ptr [eax + 8]
00427BDD  8b 40 04                 mov      eax, dword ptr [eax + 4]
00427BE0  d9 42 08                 fld      dword ptr [edx + 8]
00427BE3  d9 40 08                 fld      dword ptr [eax + 8]
00427BE6  de d9                    fcompp   
00427BE8  ba 02 00 00 00           mov      edx, 2
00427BED  df e0                    fnstsw   ax
00427BEF  f6 c4 41                 test     ah, 0x41
00427BF2  74 05                    je       0x427bf9
00427BF4  ba 01 00 00 00           mov      edx, 1
00427BF9  83 ff 03                 cmp      edi, 3
00427BFC  7c 1f                    jl       0x427c1d
00427BFE  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C01  8b 78 0c                 mov      edi, dword ptr [eax + 0xc]
00427C04  8b 04 90                 mov      eax, dword ptr [eax + edx*4]
00427C07  d9 47 08                 fld      dword ptr [edi + 8]
00427C0A  d9 40 08                 fld      dword ptr [eax + 8]
00427C0D  de d9                    fcompp   
00427C0F  df e0                    fnstsw   ax
00427C11  f6 c4 41                 test     ah, 0x41
00427C14  75 07                    jne      0x427c1d
00427C16  ba 03 00 00 00           mov      edx, 3
00427C1B  eb 05                    jmp      0x427c22
00427C1D  83 fa 01                 cmp      edx, 1
00427C20  74 6c                    je       0x427c8e
00427C22  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C25  8b 2c 90                 mov      ebp, dword ptr [eax + edx*4]
00427C28  8b 3c 98                 mov      edi, dword ptr [eax + ebx*4]
00427C2B  89 2c 98                 mov      dword ptr [eax + ebx*4], ebp
00427C2E  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C31  8b da                    mov      ebx, edx
00427C33  89 3c 90                 mov      dword ptr [eax + edx*4], edi
00427C36  8b 29                    mov      ebp, dword ptr [ecx]
00427C38  8d 3c 12                 lea      edi, [edx + edx]
00427C3B  8d 44 12 01              lea      eax, [edx + edx + 1]
00427C3F  3b fd                    cmp      edi, ebp
00427C41  89 44 24 60              mov      dword ptr [esp + 0x60], eax
00427C45  7f 1d                    jg       0x427c64
00427C47  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C4A  8b 04 b8                 mov      eax, dword ptr [eax + edi*4]
00427C4D  d9 40 08                 fld      dword ptr [eax + 8]
00427C50  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C53  8b 04 90                 mov      eax, dword ptr [eax + edx*4]
00427C56  d9 40 08                 fld      dword ptr [eax + 8]
00427C59  de d9                    fcompp   
00427C5B  df e0                    fnstsw   ax
00427C5D  f6 c4 41                 test     ah, 0x41
00427C60  75 02                    jne      0x427c64
00427C62  8b d7                    mov      edx, edi
00427C64  39 6c 24 60              cmp      dword ptr [esp + 0x60], ebp
00427C68  7f 20                    jg       0x427c8a
00427C6A  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427C6D  8b 7c 24 60              mov      edi, dword ptr [esp + 0x60]
00427C71  8b 3c b8                 mov      edi, dword ptr [eax + edi*4]
00427C74  8b 04 90                 mov      eax, dword ptr [eax + edx*4]
00427C77  d9 47 08                 fld      dword ptr [edi + 8]
00427C7A  d9 40 08                 fld      dword ptr [eax + 8]
00427C7D  de d9                    fcompp   
00427C7F  df e0                    fnstsw   ax
00427C81  f6 c4 41                 test     ah, 0x41
00427C84  75 04                    jne      0x427c8a
00427C86  8b 54 24 60              mov      edx, dword ptr [esp + 0x60]
00427C8A  3b d3                    cmp      edx, ebx
00427C8C  75 94                    jne      0x427c22
00427C8E  8b 4c 24 4c              mov      ecx, dword ptr [esp + 0x4c]
00427C92  89 4c 24 14              mov      dword ptr [esp + 0x14], ecx
00427C96  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427C9A  85 c0                    test     eax, eax
00427C9C  74 08                    je       0x427ca6
00427C9E  8b 10                    mov      edx, dword ptr [eax]
00427CA0  8b 42 04                 mov      eax, dword ptr [edx + 4]
00427CA3  89 46 30                 mov      dword ptr [esi + 0x30], eax
00427CA6  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
00427CAA  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427CAE  41                       inc      ecx
00427CAF  85 c0                    test     eax, eax
00427CB1  89 4c 24 28              mov      dword ptr [esp + 0x28], ecx
00427CB5  0f 85 8f f9 ff ff        jne      0x42764a
00427CBB  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
00427CBF  81 f9 10 27 00 00        cmp      ecx, 0x2710
00427CC5  74 54                    je       0x427d1b
00427CC7  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427CCB  85 c0                    test     eax, eax
00427CCD  74 4c                    je       0x427d1b
00427CCF  3b 4c 24 70              cmp      ecx, dword ptr [esp + 0x70]
00427CD3  74 46                    je       0x427d1b
00427CD5  83 78 0c 02              cmp      dword ptr [eax + 0xc], 2
00427CD9  7c 40                    jl       0x427d1b
00427CDB  8b 4c 24 6c              mov      ecx, dword ptr [esp + 0x6c]
00427CDF  51                       push     ecx
00427CE0  50                       push     eax
00427CE1  8b ce                    mov      ecx, esi
00427CE3  e8 88 06 00 00           call     0x428370
00427CE8  8b 5c 24 68              mov      ebx, dword ptr [esp + 0x68]
00427CEC  8b f8                    mov      edi, eax
00427CEE  53                       push     ebx
00427CEF  57                       push     edi
00427CF0  8b ce                    mov      ecx, esi
00427CF2  e8 e9 0d 00 00           call     0x428ae0
00427CF7  53                       push     ebx
00427CF8  57                       push     edi
00427CF9  8b ce                    mov      ecx, esi
00427CFB  e8 c0 13 00 00           call     0x4290c0
00427D00  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
00427D03  85 c0                    test     eax, eax
00427D05  74 08                    je       0x427d0f
00427D07  53                       push     ebx
00427D08  8b ce                    mov      ecx, esi
00427D0A  e8 c1 08 00 00           call     0x4285d0
00427D0F  8b c7                    mov      eax, edi
00427D11  5f                       pop      edi
00427D12  5e                       pop      esi
00427D13  5d                       pop      ebp
00427D14  5b                       pop      ebx
00427D15  83 c4 4c                 add      esp, 0x4c
00427D18  c2 18 00                 ret      0x18
00427D1B  8b 5c 24 68              mov      ebx, dword ptr [esp + 0x68]
00427D1F  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
00427D22  85 c0                    test     eax, eax
00427D24  74 08                    je       0x427d2e
00427D26  53                       push     ebx
00427D27  8b ce                    mov      ecx, esi
00427D29  e8 a2 08 00 00           call     0x4285d0
00427D2E  5f                       pop      edi
00427D2F  5e                       pop      esi
00427D30  5d                       pop      ebp
00427D31  33 c0                    xor      eax, eax
00427D33  5b                       pop      ebx
00427D34  83 c4 4c                 add      esp, 0x4c
00427D37  c2 18 00                 ret      0x18
00427D3A  90                       nop      
00427D3B  90                       nop      
00427D3C  90                       nop      
00427D3D  90                       nop      
00427D3E  90                       nop      
00427D3F  90                       nop      
00427D40  8b 41 10                 mov      eax, dword ptr [ecx + 0x10]
00427D43  53                       push     ebx
00427D44  55                       push     ebp
00427D45  56                       push     esi
00427D46  8b 90 00 00 10 00        mov      edx, dword ptr [eax + 0x100000]
00427D4C  8b 5c 24 10              mov      ebx, dword ptr [esp + 0x10]
00427D50  8b f2                    mov      esi, edx
00427D52  57                       push     edi
00427D53  c1 e6 04                 shl      esi, 4
00427D56  03 f0                    add      esi, eax
00427D58  42                       inc      edx
00427D59  89 90 00 00 10 00        mov      dword ptr [eax + 0x100000], edx
00427D5F  8b 41 0c                 mov      eax, dword ptr [ecx + 0xc]
00427D62  8b 90 00 00 18 00        mov      edx, dword ptr [eax + 0x180000]
00427D68  8d 3c 52                 lea      edi, [edx + edx*2]
00427D6B  42                       inc      edx
00427D6C  89 90 00 00 18 00        mov      dword ptr [eax + 0x180000], edx
00427D72  8d 3c b8                 lea      edi, [eax + edi*4]
00427D75  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00427D79  85 db                    test     ebx, ebx
00427D7B  89 07                    mov      dword ptr [edi], eax
00427D7D  74 77                    je       0x427df6
00427D7F  8b 0b                    mov      ecx, dword ptr [ebx]
00427D81  89 4f 08                 mov      dword ptr [edi + 8], ecx
00427D84  8b 13                    mov      edx, dword ptr [ebx]
00427D86  8b 00                    mov      eax, dword ptr [eax]
00427D88  8b 0a                    mov      ecx, dword ptr [edx]
00427D8A  0f be 90 1b 01 00 00     movsx    edx, byte ptr [eax + 0x11b]
00427D91  8b 09                    mov      ecx, dword ptr [ecx]
00427D93  89 57 04                 mov      dword ptr [edi + 4], edx
00427D96  f7 80 40 01 00 00 00 01 00 00 test     dword ptr [eax + 0x140], 0x100
00427DA0  74 61                    je       0x427e03
00427DA2  8b a9 40 01 00 00        mov      ebp, dword ptr [ecx + 0x140]
00427DA8  81 e5 00 01 00 00        and      ebp, 0x100
00427DAE  89 6c 24 14              mov      dword ptr [esp + 0x14], ebp
00427DB2  74 1d                    je       0x427dd1
00427DB4  0f be 89 1b 01 00 00     movsx    ecx, byte ptr [ecx + 0x11b]
00427DBB  8b 2b                    mov      ebp, dword ptr [ebx]
00427DBD  83 c1 04                 add      ecx, 4
00427DC0  39 4d 04                 cmp      dword ptr [ebp + 4], ecx
00427DC3  75 08                    jne      0x427dcd
00427DC5  83 c2 04                 add      edx, 4
00427DC8  89 57 04                 mov      dword ptr [edi + 4], edx
00427DCB  eb 36                    jmp      0x427e03
00427DCD  8b 6c 24 14              mov      ebp, dword ptr [esp + 0x14]
00427DD1  85 ed                    test     ebp, ebp
00427DD3  75 2e                    jne      0x427e03
00427DD5  8b 13                    mov      edx, dword ptr [ebx]
00427DD7  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427DDE  2b 42 04                 sub      eax, dword ptr [edx + 4]
00427DE1  83 c0 03                 add      eax, 3
00427DE4  99                       cdq      
00427DE5  33 c2                    xor      eax, edx
00427DE7  2b c2                    sub      eax, edx
00427DE9  83 f8 01                 cmp      eax, 1
00427DEC  7f 15                    jg       0x427e03
00427DEE  8b 47 04                 mov      eax, dword ptr [edi + 4]
00427DF1  83 c0 04                 add      eax, 4
00427DF4  eb 0a                    jmp      0x427e00
00427DF6  c7 47 08 00 00 00 00     mov      dword ptr [edi + 8], 0
00427DFD  8b 41 30                 mov      eax, dword ptr [ecx + 0x30]
00427E00  89 47 04                 mov      dword ptr [edi + 4], eax
00427E03  85 db                    test     ebx, ebx
00427E05  89 3e                    mov      dword ptr [esi], edi
00427E07  74 13                    je       0x427e1c
00427E09  d9 44 24 20              fld      dword ptr [esp + 0x20]
00427E0D  d8 43 04                 fadd     dword ptr [ebx + 4]
00427E10  d9 5e 04                 fstp     dword ptr [esi + 4]
00427E13  8b 4b 0c                 mov      ecx, dword ptr [ebx + 0xc]
00427E16  41                       inc      ecx
00427E17  89 4e 0c                 mov      dword ptr [esi + 0xc], ecx
00427E1A  eb 0e                    jmp      0x427e2a
00427E1C  c7 46 04 00 00 00 00     mov      dword ptr [esi + 4], 0
00427E23  c7 46 0c 01 00 00 00     mov      dword ptr [esi + 0xc], 1
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
00427E87  90                       nop      
00427E88  90                       nop      
00427E89  90                       nop      
00427E8A  90                       nop      
00427E8B  90                       nop      
00427E8C  90                       nop      
00427E8D  90                       nop      
00427E8E  90                       nop      
00427E8F  90                       nop      
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
