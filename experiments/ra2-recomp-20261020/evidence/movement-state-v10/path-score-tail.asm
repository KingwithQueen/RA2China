
sub_00427814 0x00427814 size=352
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
