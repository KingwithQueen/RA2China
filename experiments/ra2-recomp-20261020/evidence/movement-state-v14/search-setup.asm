
sub_00427370 0x00427370 size=730
00427370  83 ec 4c                 sub      esp, 0x4c
00427373  53                       push     ebx
00427374  55                       push     ebp
00427375  56                       push     esi
00427376  57                       push     edi
00427377  8b 7c 24 64              mov      edi, dword ptr [esp + 0x64]
0042737B  8b 6c 24 60              mov      ebp, dword ptr [esp + 0x60]
0042737F  8b f1                    mov      esi, ecx
00427381  a1 18 26 83 00           mov      eax, dword ptr [0x832618]
00427386  0f bf 4f 02              movsx    ecx, word ptr [edi + 2]
0042738A  0f bf 17                 movsx    edx, word ptr [edi]
0042738D  0f bf 5d 00              movsx    ebx, word ptr [ebp]
00427391  c1 e1 09                 shl      ecx, 9
00427394  03 ca                    add      ecx, edx
00427396  c7 44 24 28 00 00 00 00  mov      dword ptr [esp + 0x28], 0
0042739E  0f bf 55 02              movsx    edx, word ptr [ebp + 2]
004273A2  c1 e2 09                 shl      edx, 9
004273A5  03 d3                    add      edx, ebx
004273A7  8d 0c 88                 lea      ecx, [eax + ecx*4]
004273AA  89 4c 24 38              mov      dword ptr [esp + 0x38], ecx
004273AE  8b 09                    mov      ecx, dword ptr [ecx]
004273B0  8d 04 90                 lea      eax, [eax + edx*4]
004273B3  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004273B7  89 4c 24 30              mov      dword ptr [esp + 0x30], ecx
004273BB  8b 00                    mov      eax, dword ptr [eax]
004273BD  85 c0                    test     eax, eax
004273BF  89 44 24 60              mov      dword ptr [esp + 0x60], eax
004273C3  0f 84 65 09 00 00        je       0x427d2e
004273C9  85 c9                    test     ecx, ecx
004273CB  0f 84 5d 09 00 00        je       0x427d2e
004273D1  8b 5c 24 68              mov      ebx, dword ptr [esp + 0x68]
004273D5  8b cb                    mov      ecx, ebx
004273D7  8b 03                    mov      eax, dword ptr [ebx]
004273D9  ff 50 2c                 call     dword ptr [eax + 0x2c]
004273DC  83 f8 02                 cmp      eax, 2
004273DF  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004273E3  74 17                    je       0x4273fc
004273E5  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004273EB  f6 c5 01                 test     ch, 1
004273EE  74 0c                    je       0x4273fc
004273F0  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
004273F7  83 c0 04                 add      eax, 4
004273FA  eb 07                    jmp      0x427403
004273FC  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427403  89 46 34                 mov      dword ptr [esi + 0x34], eax
00427406  8b 13                    mov      edx, dword ptr [ebx]
00427408  8b cb                    mov      ecx, ebx
0042740A  ff 52 2c                 call     dword ptr [edx + 0x2c]
0042740D  83 f8 02                 cmp      eax, 2
00427410  74 17                    je       0x427429
00427412  8a 43 79                 mov      al, byte ptr [ebx + 0x79]
00427415  84 c0                    test     al, al
00427417  74 10                    je       0x427429
00427419  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
0042741D  0f be 80 1b 01 00 00     movsx    eax, byte ptr [eax + 0x11b]
00427424  83 c0 04                 add      eax, 4
00427427  eb 0b                    jmp      0x427434
00427429  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
0042742D  0f be 81 1b 01 00 00     movsx    eax, byte ptr [ecx + 0x11b]
00427434  89 46 30                 mov      dword ptr [esi + 0x30], eax
00427437  8b 13                    mov      edx, dword ptr [ebx]
00427439  8b cb                    mov      ecx, ebx
0042743B  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
00427441  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
00427447  84 c9                    test     cl, cl
00427449  74 45                    je       0x427490
0042744B  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
0042744F  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
00427455  f6 c5 01                 test     ch, 1
00427458  74 36                    je       0x427490
0042745A  8d 8b 88 00 00 00        lea      ecx, [ebx + 0x88]
00427460  8b 93 88 00 00 00        mov      edx, dword ptr [ebx + 0x88]
00427466  89 54 24 50              mov      dword ptr [esp + 0x50], edx
0042746A  8b 41 04                 mov      eax, dword ptr [ecx + 4]
0042746D  89 44 24 54              mov      dword ptr [esp + 0x54], eax
00427471  8b 41 08                 mov      eax, dword ptr [ecx + 8]
00427474  8b 4e 30                 mov      ecx, dword ptr [esi + 0x30]
00427477  99                       cdq      
00427478  f7 3d 00 e8 84 00        idiv     dword ptr [0x84e800]
0042747E  2b c1                    sub      eax, ecx
00427480  99                       cdq      
00427481  33 c2                    xor      eax, edx
00427483  2b c2                    sub      eax, edx
00427485  83 f8 02                 cmp      eax, 2
00427488  7e 06                    jle      0x427490
0042748A  83 c1 04                 add      ecx, 4
0042748D  89 4e 30                 mov      dword ptr [esi + 0x30], ecx
00427490  8b 13                    mov      edx, dword ptr [ebx]
00427492  8b cb                    mov      ecx, ebx
00427494  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
0042749A  8b 80 a4 05 00 00        mov      eax, dword ptr [eax + 0x5a4]
004274A0  8b 56 40                 mov      edx, dword ptr [esi + 0x40]
004274A3  89 46 2c                 mov      dword ptr [esi + 0x2c], eax
004274A6  8b 44 24 2c              mov      eax, dword ptr [esp + 0x2c]
004274AA  c7 46 6c 00 00 00 00     mov      dword ptr [esi + 0x6c], 0
004274B1  8b 4d 00                 mov      ecx, dword ptr [ebp]
004274B4  6a 00                    push     0
004274B6  57                       push     edi
004274B7  89 4e 70                 mov      dword ptr [esi + 0x70], ecx
004274BA  50                       push     eax
004274BB  6a 00                    push     0
004274BD  8b ce                    mov      ecx, esi
004274BF  89 54 24 50              mov      dword ptr [esp + 0x50], edx
004274C3  e8 78 08 00 00           call     0x427d40
004274C8  66 8b 4d 00              mov      cx, word ptr [ebp]
004274CC  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004274D0  66 3b 0f                 cmp      cx, word ptr [edi]
004274D3  75 18                    jne      0x4274ed
004274D5  66 8b 55 02              mov      dx, word ptr [ebp + 2]
004274D9  66 3b 57 02              cmp      dx, word ptr [edi + 2]
004274DD  75 0e                    jne      0x4274ed
004274DF  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
004274E2  8b 4e 34                 mov      ecx, dword ptr [esi + 0x34]
004274E5  3b c1                    cmp      eax, ecx
004274E7  0f 84 41 08 00 00        je       0x427d2e
004274ED  8b 46 3c                 mov      eax, dword ptr [esi + 0x3c]
004274F0  85 c0                    test     eax, eax
004274F2  74 08                    je       0x4274fc
004274F4  53                       push     ebx
004274F5  8b ce                    mov      ecx, esi
004274F7  e8 d4 10 00 00           call     0x4285d0
004274FC  8b 4c 24 60              mov      ecx, dword ptr [esp + 0x60]
00427500  0f bf 41 26              movsx    eax, word ptr [ecx + 0x26]
00427504  0f af 05 04 e8 84 00     imul     eax, dword ptr [0x84e804]
0042750B  0f bf 51 24              movsx    edx, word ptr [ecx + 0x24]
0042750F  0f be 89 1b 01 00 00     movsx    ecx, byte ptr [ecx + 0x11b]
00427516  03 c2                    add      eax, edx
00427518  8b 56 30                 mov      edx, dword ptr [esi + 0x30]
0042751B  3b d1                    cmp      edx, ecx
0042751D  7e 15                    jle      0x427534
0042751F  8b 56 1c                 mov      edx, dword ptr [esi + 0x1c]
00427522  8b 4e 28                 mov      ecx, dword ptr [esi + 0x28]
00427525  89 0c 82                 mov      dword ptr [edx + eax*4], ecx
00427528  8b 56 20                 mov      edx, dword ptr [esi + 0x20]
0042752B  c7 04 82 00 00 00 00     mov      dword ptr [edx + eax*4], 0
00427532  eb 13                    jmp      0x427547
00427534  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
00427537  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
0042753A  89 14 81                 mov      dword ptr [ecx + eax*4], edx
0042753D  8b 4e 24                 mov      ecx, dword ptr [esi + 0x24]
00427540  c7 04 81 00 00 00 00     mov      dword ptr [ecx + eax*4], 0
00427547  8b 13                    mov      edx, dword ptr [ebx]
00427549  8b cb                    mov      ecx, ebx
0042754B  c6 44 24 12 00           mov      byte ptr [esp + 0x12], 0
00427550  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
00427556  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
0042755C  84 c9                    test     cl, cl
0042755E  0f 84 a4 00 00 00        je       0x427608
00427564  c6 44 24 12 01           mov      byte ptr [esp + 0x12], 1
00427569  33 ed                    xor      ebp, ebp
0042756B  bf 84 c4 79 00           mov      edi, 0x79c484
00427570  8d 44 24 60              lea      eax, [esp + 0x60]
00427574  8d 8b e0 02 00 00        lea      ecx, [ebx + 0x2e0]
0042757A  50                       push     eax
0042757B  e8 60 16 09 00           call     0x4b8be0
00427580  8b 00                    mov      eax, dword ptr [eax]
00427582  c1 e8 0c                 shr      eax, 0xc
00427585  40                       inc      eax
00427586  d1 e8                    shr      eax, 1
00427588  83 e0 07                 and      eax, 7
0042758B  2b c5                    sub      eax, ebp
0042758D  99                       cdq      
0042758E  33 c2                    xor      eax, edx
00427590  2b c2                    sub      eax, edx
00427592  83 f8 02                 cmp      eax, 2
00427595  7e 61                    jle      0x4275f8
00427597  83 f8 06                 cmp      eax, 6
0042759A  7d 5c                    jge      0x4275f8
0042759C  81 ff a4 c4 79 00        cmp      edi, 0x79c4a4
004275A2  74 54                    je       0x4275f8
004275A4  8b 0f                    mov      ecx, dword ptr [edi]
004275A6  8b 54 24 2c              mov      edx, dword ptr [esp + 0x2c]
004275AA  8d 04 8a                 lea      eax, [edx + ecx*4]
004275AD  8b 0c 8a                 mov      ecx, dword ptr [edx + ecx*4]
004275B0  0f bf 41 26              movsx    eax, word ptr [ecx + 0x26]
004275B4  0f af 05 04 e8 84 00     imul     eax, dword ptr [0x84e804]
004275BB  0f bf 51 24              movsx    edx, word ptr [ecx + 0x24]
004275BF  0f be 89 1b 01 00 00     movsx    ecx, byte ptr [ecx + 0x11b]
004275C6  03 c2                    add      eax, edx
004275C8  8b 56 30                 mov      edx, dword ptr [esi + 0x30]
004275CB  41                       inc      ecx
004275CC  3b d1                    cmp      edx, ecx
004275CE  7e 15                    jle      0x4275e5
004275D0  8b 56 1c                 mov      edx, dword ptr [esi + 0x1c]
004275D3  8b 4e 28                 mov      ecx, dword ptr [esi + 0x28]
004275D6  89 0c 82                 mov      dword ptr [edx + eax*4], ecx
004275D9  8b 56 20                 mov      edx, dword ptr [esi + 0x20]
004275DC  c7 04 82 00 00 00 00     mov      dword ptr [edx + eax*4], 0
004275E3  eb 13                    jmp      0x4275f8
004275E5  8b 4e 18                 mov      ecx, dword ptr [esi + 0x18]
004275E8  8b 56 28                 mov      edx, dword ptr [esi + 0x28]
004275EB  89 14 81                 mov      dword ptr [ecx + eax*4], edx
004275EE  8b 4e 24                 mov      ecx, dword ptr [esi + 0x24]
004275F1  c7 04 81 00 00 00 00     mov      dword ptr [ecx + eax*4], 0
004275F8  83 c7 04                 add      edi, 4
004275FB  45                       inc      ebp
004275FC  81 ff a4 c4 79 00        cmp      edi, 0x79c4a4
00427602  0f 8e 68 ff ff ff        jle      0x427570
00427608  8b 13                    mov      edx, dword ptr [ebx]
0042760A  8b cb                    mov      ecx, ebx
0042760C  ff 52 2c                 call     dword ptr [edx + 0x2c]
0042760F  83 f8 01                 cmp      eax, 1
00427612  75 15                    jne      0x427629
00427614  8b 83 ac 05 00 00        mov      eax, dword ptr [ebx + 0x5ac]
0042761A  c6 44 24 13 01           mov      byte ptr [esp + 0x13], 1
0042761F  8a 88 a4 0b 00 00        mov      cl, byte ptr [eax + 0xba4]
00427625  84 c9                    test     cl, cl
00427627  75 05                    jne      0x42762e
00427629  c6 44 24 13 00           mov      byte ptr [esp + 0x13], 0
0042762E  8b 44 24 70              mov      eax, dword ptr [esp + 0x70]
00427632  85 c0                    test     eax, eax
00427634  7d 08                    jge      0x42763e
00427636  c7 44 24 70 f7 ff 00 00  mov      dword ptr [esp + 0x70], 0xfff7
0042763E  8b 44 24 14              mov      eax, dword ptr [esp + 0x14]
00427642  85 c0                    test     eax, eax
00427644  0f 84 d5 06 00 00        je       0x427d1f
