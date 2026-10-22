
sub_0042764A 0x0042764A size=1712
0042764A  8b 4c 24 70              mov      ecx, dword ptr [esp + 0x70]
0042764E  8b 44 24 28              mov      eax, dword ptr [esp + 0x28]
00427652  33 d2                    xor      edx, edx
00427654  3b c1                    cmp      eax, ecx
00427656  0f 8d 5f 06 00 00        jge      0x427cbb
0042765C  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427660  8b 7c 24 38              mov      edi, dword ptr [esp + 0x38]
00427664  8b 08                    mov      ecx, dword ptr [eax]
00427666  8b 01                    mov      eax, dword ptr [ecx]
00427668  3b c7                    cmp      eax, edi
0042766A  89 44 24 20              mov      dword ptr [esp + 0x20], eax
0042766E  75 0e                    jne      0x42767e
00427670  8b 49 04                 mov      ecx, dword ptr [ecx + 4]
00427673  8b 7e 34                 mov      edi, dword ptr [esi + 0x34]
00427676  3b cf                    cmp      ecx, edi
00427678  0f 84 3d 06 00 00        je       0x427cbb
0042767E  8b 00                    mov      eax, dword ptr [eax]
00427680  89 54 24 1c              mov      dword ptr [esp + 0x1c], edx
00427684  83 c0 24                 add      eax, 0x24
00427687  89 54 24 18              mov      dword ptr [esp + 0x18], edx
0042768B  0f bf 48 02              movsx    ecx, word ptr [eax + 2]
0042768F  0f af 0d 04 e8 84 00     imul     ecx, dword ptr [0x84e804]
00427696  0f bf 00                 movsx    eax, word ptr [eax]
00427699  03 c8                    add      ecx, eax
0042769B  89 4c 24 3c              mov      dword ptr [esp + 0x3c], ecx
0042769F  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
004276A3  83 f8 08                 cmp      eax, 8
004276A6  75 40                    jne      0x4276e8
004276A8  8b 4c 24 20              mov      ecx, dword ptr [esp + 0x20]
004276AC  8b 11                    mov      edx, dword ptr [ecx]
004276AE  0f bf 82 16 01 00 00     movsx    eax, word ptr [edx + 0x116]
004276B5  83 f8 ff                 cmp      eax, -1
004276B8  74 27                    je       0x4276e1
004276BA  8b 0d cc 61 86 00        mov      ecx, dword ptr [0x8661cc]
004276C0  8b 14 81                 mov      edx, dword ptr [ecx + eax*4]
004276C3  8b 42 28                 mov      eax, dword ptr [edx + 0x28]
004276C6  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004276CA  0f bf 4c 24 62           movsx    ecx, word ptr [esp + 0x62]
004276CF  0f bf d0                 movsx    edx, ax
004276D2  a1 18 26 83 00           mov      eax, dword ptr [0x832618]
004276D7  c1 e1 09                 shl      ecx, 9
004276DA  03 ca                    add      ecx, edx
004276DC  8d 04 88                 lea      eax, [eax + ecx*4]
004276DF  eb 15                    jmp      0x4276f6
004276E1  b8 08 e8 84 00           mov      eax, 0x84e808
004276E6  eb 0e                    jmp      0x4276f6
004276E8  8b 0c 85 84 c4 79 00     mov      ecx, dword ptr [eax*4 + 0x79c484]
004276EF  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
004276F3  8d 04 8a                 lea      eax, [edx + ecx*4]
004276F6  8b 18                    mov      ebx, dword ptr [eax]
004276F8  89 44 24 24              mov      dword ptr [esp + 0x24], eax
004276FC  85 db                    test     ebx, ebx
004276FE  0f 84 7a 03 00 00        je       0x427a7e
00427704  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00427708  8d 4b 24                 lea      ecx, [ebx + 0x24]
0042770B  83 f8 08                 cmp      eax, 8
0042770E  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
00427712  74 0d                    je       0x427721
00427714  8b 3c 85 38 c8 84 00     mov      edi, dword ptr [eax*4 + 0x84c838]
0042771B  8b 44 24 3c              mov      eax, dword ptr [esp + 0x3c]
0042771F  eb 0e                    jmp      0x42772f
00427721  0f bf 79 02              movsx    edi, word ptr [ecx + 2]
00427725  0f af 3d 04 e8 84 00     imul     edi, dword ptr [0x84e804]
0042772C  0f bf 01                 movsx    eax, word ptr [ecx]
0042772F  03 f8                    add      edi, eax
00427731  8b 83 40 01 00 00        mov      eax, dword ptr [ebx + 0x140]
00427737  f6 c4 01                 test     ah, 1
0042773A  74 1b                    je       0x427757
0042773C  0f be 93 1b 01 00 00     movsx    edx, byte ptr [ebx + 0x11b]
00427743  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
00427746  c6 44 24 60 00           mov      byte ptr [esp + 0x60], 0
0042774B  2b c2                    sub      eax, edx
0042774D  99                       cdq      
0042774E  33 c2                    xor      eax, edx
00427750  2b c2                    sub      eax, edx
00427752  83 f8 01                 cmp      eax, 1
00427755  7f 05                    jg       0x42775c
00427757  c6 44 24 60 01           mov      byte ptr [esp + 0x60], 1
0042775C  51                       push     ecx
0042775D  b9 e0 24 83 00           mov      ecx, 0x8324e0
00427762  e8 49 83 12 00           call     0x54fab0
00427767  8b 0d 4c 25 83 00        mov      ecx, dword ptr [0x83254c]
0042776D  8d 04 80                 lea      eax, [eax + eax*4]
00427770  8b 54 24 40              mov      edx, dword ptr [esp + 0x40]
00427774  8d 04 41                 lea      eax, [ecx + eax*2]
00427777  0f bf 08                 movsx    ecx, word ptr [eax]
0042777A  8b 46 28                 mov      eax, dword ptr [esi + 0x28]
0042777D  89 4c 24 4c              mov      dword ptr [esp + 0x4c], ecx
00427781  39 04 8a                 cmp      dword ptr [edx + ecx*4], eax
00427784  74 1e                    je       0x4277a4
00427786  8a 4c 24 60              mov      cl, byte ptr [esp + 0x60]
0042778A  84 c9                    test     cl, cl
0042778C  74 53                    je       0x4277e1
0042778E  8a 8b 22 01 00 00        mov      cl, byte ptr [ebx + 0x122]
00427794  84 c9                    test     cl, cl
00427796  75 0c                    jne      0x4277a4
00427798  8a 4c 24 74              mov      cl, byte ptr [esp + 0x74]
0042779C  84 c9                    test     cl, cl
0042779E  0f 85 da 02 00 00        jne      0x427a7e
004277A4  8a 4c 24 60              mov      cl, byte ptr [esp + 0x60]
004277A8  84 c9                    test     cl, cl
004277AA  74 35                    je       0x4277e1
004277AC  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
004277AF  8d 2c bd 00 00 00 00     lea      ebp, [edi*4]
004277B6  89 6c 24 2c              mov      dword ptr [esp + 0x2c], ebp
004277BA  39 04 29                 cmp      dword ptr [ecx + ebp], eax
004277BD  75 55                    jne      0x427814
004277BF  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004277C3  8b 46 24                 mov      eax, dword ptr [esi + 0x24]
004277C6  d9 42 04                 fld      dword ptr [edx + 4]
004277C9  dc 05 d0 c4 79 00        fadd     qword ptr [0x79c4d0]
004277CF  d9 04 28                 fld      dword ptr [eax + ebp]
004277D2  de d9                    fcompp   
004277D4  df e0                    fnstsw   ax
004277D6  f6 c4 01                 test     ah, 1
004277D9  0f 85 9f 02 00 00        jne      0x427a7e
004277DF  eb 33                    jmp      0x427814
004277E1  8b 4e 1c                 mov      ecx, dword ptr [esi + 0x1c]
004277E4  8d 2c bd 00 00 00 00     lea      ebp, [edi*4]
004277EB  89 6c 24 2c              mov      dword ptr [esp + 0x2c], ebp
004277EF  39 04 29                 cmp      dword ptr [ecx + ebp], eax
004277F2  75 20                    jne      0x427814
004277F4  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004277F8  8b 46 20                 mov      eax, dword ptr [esi + 0x20]
004277FB  d9 42 04                 fld      dword ptr [edx + 4]
004277FE  dc 05 d0 c4 79 00        fadd     qword ptr [0x79c4d0]
00427804  d9 04 28                 fld      dword ptr [eax + ebp]
00427807  de d9                    fcompp   
00427809  df e0                    fnstsw   ax
0042780B  f6 c4 01                 test     ah, 1
0042780E  0f 85 6a 02 00 00        jne      0x427a7e
00427814  8a 46 08                 mov      al, byte ptr [esi + 8]
00427817  8b 4c 24 20              mov      ecx, dword ptr [esp + 0x20]
0042781B  8b 7c 24 68              mov      edi, dword ptr [esp + 0x68]
0042781F  50                       push     eax
00427820  8b 01                    mov      eax, dword ptr [ecx]
00427822  8b 4e 30                 mov      ecx, dword ptr [esi + 0x30]
00427825  8b 17                    mov      edx, dword ptr [edi]
00427827  50                       push     eax
00427828  8b 44 24 20              mov      eax, dword ptr [esp + 0x20]
0042782C  51                       push     ecx
0042782D  50                       push     eax
0042782E  53                       push     ebx
0042782F  8b cf                    mov      ecx, edi
00427831  ff 92 94 01 00 00        call     dword ptr [edx + 0x194]
00427837  8b d8                    mov      ebx, eax
00427839  8a 44 24 12              mov      al, byte ptr [esp + 0x12]
0042783D  84 c0                    test     al, al
0042783F  74 07                    je       0x427848
00427841  83 fb 07                 cmp      ebx, 7
00427844  7d 02                    jge      0x427848
00427846  33 db                    xor      ebx, ebx
00427848  83 7c 24 18 08           cmp      dword ptr [esp + 0x18], 8
0042784D  74 31                    je       0x427880
0042784F  8a 44 24 60              mov      al, byte ptr [esp + 0x60]
00427853  8b 54 24 20              mov      edx, dword ptr [esp + 0x20]
00427857  84 c0                    test     al, al
00427859  57                       push     edi
0042785A  8b 7c 24 28              mov      edi, dword ptr [esp + 0x28]
0042785E  0f 94 c1                 sete     cl
00427861  53                       push     ebx
00427862  51                       push     ecx
00427863  57                       push     edi
00427864  52                       push     edx
00427865  8b ce                    mov      ecx, esi
00427867  e8 a4 f8 ff ff           call     0x427110
0042786C  d8 4e 04                 fmul     dword ptr [esi + 4]
0042786F  8b 44 24 18              mov      eax, dword ptr [esp + 0x18]
00427873  d8 04 85 dc f0 7c 00     fadd     dword ptr [eax*4 + 0x7cf0dc]
0042787A  d9 5c 24 34              fstp     dword ptr [esp + 0x34]
0042787E  eb 47                    jmp      0x4278c7
00427880  8b 4c 24 20              mov      ecx, dword ptr [esp + 0x20]
00427884  8b 54 24 30              mov      edx, dword ptr [esp + 0x30]
00427888  8b 39                    mov      edi, dword ptr [ecx]
0042788A  0f bf 4a 02              movsx    ecx, word ptr [edx + 2]
0042788E  0f bf 47 26              movsx    eax, word ptr [edi + 0x26]
00427892  83 c7 24                 add      edi, 0x24
00427895  2b c1                    sub      eax, ecx
00427897  99                       cdq      
00427898  8b c8                    mov      ecx, eax
0042789A  0f bf 07                 movsx    eax, word ptr [edi]
0042789D  33 ca                    xor      ecx, edx
0042789F  2b ca                    sub      ecx, edx
004278A1  8b 54 24 30              mov      edx, dword ptr [esp + 0x30]
004278A5  0f bf 12                 movsx    edx, word ptr [edx]
004278A8  2b c2                    sub      eax, edx
004278AA  99                       cdq      
004278AB  33 c2                    xor      eax, edx
004278AD  2b c2                    sub      eax, edx
004278AF  3b c1                    cmp      eax, ecx
004278B1  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004278B5  7f 04                    jg       0x4278bb
004278B7  89 4c 24 34              mov      dword ptr [esp + 0x34], ecx
004278BB  db 44 24 34              fild     dword ptr [esp + 0x34]
004278BF  8b 7c 24 24              mov      edi, dword ptr [esp + 0x24]
004278C3  d9 5c 24 34              fstp     dword ptr [esp + 0x34]
004278C7  83 fb 07                 cmp      ebx, 7
004278CA  0f 8d 8a 01 00 00        jge      0x427a5a
004278D0  8a 44 24 60              mov      al, byte ptr [esp + 0x60]
004278D4  84 c0                    test     al, al
004278D6  74 12                    je       0x4278ea
004278D8  8b 46 18                 mov      eax, dword ptr [esi + 0x18]
004278DB  8b 0c 28                 mov      ecx, dword ptr [eax + ebp]
004278DE  8b 46 28                 mov      eax, dword ptr [esi + 0x28]
004278E1  3b c8                    cmp      ecx, eax
004278E3  75 16                    jne      0x4278fb
004278E5  e9 94 01 00 00           jmp      0x427a7e
004278EA  8b 56 1c                 mov      edx, dword ptr [esi + 0x1c]
004278ED  8b 4e 28                 mov      ecx, dword ptr [esi + 0x28]
004278F0  8b 04 2a                 mov      eax, dword ptr [edx + ebp]
004278F3  3b c1                    cmp      eax, ecx
004278F5  0f 84 83 01 00 00        je       0x427a7e
004278FB  8b 4c 24 34              mov      ecx, dword ptr [esp + 0x34]
004278FF  8b 54 24 64              mov      edx, dword ptr [esp + 0x64]
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
