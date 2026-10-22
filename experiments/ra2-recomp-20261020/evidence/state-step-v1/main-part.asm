
sub_0054058C 0x0054058C size=339
0054058C  89 44 24 24              mov      dword ptr [esp + 0x24], eax
00540590  a1 dc eb a6 00           mov      eax, dword ptr [0xa6ebdc]
00540595  f6 c4 01                 test     ah, 1
00540598  74 13                    je       0x5405ad
0054059A  8d 44 24 24              lea      eax, [esp + 0x24]
0054059E  6a 01                    push     1
005405A0  50                       push     eax
005405A1  6a 06                    push     6
005405A3  b9 e0 24 83 00           mov      ecx, 0x8324e0
005405A8  e8 b3 95 f5 ff           call     0x499b60
005405AD  a1 dc eb a6 00           mov      eax, dword ptr [0xa6ebdc]
005405B2  f6 c4 10                 test     ah, 0x10
005405B5  74 13                    je       0x5405ca
005405B7  8d 4c 24 24              lea      ecx, [esp + 0x24]
005405BB  6a 01                    push     1
005405BD  51                       push     ecx
005405BE  6a 02                    push     2
005405C0  b9 e0 24 83 00           mov      ecx, 0x8324e0
005405C5  e8 96 95 f5 ff           call     0x499b60
005405CA  f6 05 dc eb a6 00 01     test     byte ptr [0xa6ebdc], 1
005405D1  74 12                    je       0x5405e5
005405D3  8d 54 24 24              lea      edx, [esp + 0x24]
005405D7  6a 01                    push     1
005405D9  52                       push     edx
005405DA  57                       push     edi
005405DB  b9 e0 24 83 00           mov      ecx, 0x8324e0
005405E0  e8 7b 95 f5 ff           call     0x499b60
005405E5  f6 05 dc eb a6 00 10     test     byte ptr [0xa6ebdc], 0x10
005405EC  74 13                    je       0x540601
005405EE  8d 44 24 24              lea      eax, [esp + 0x24]
005405F2  6a 01                    push     1
005405F4  50                       push     eax
005405F5  6a 04                    push     4
005405F7  b9 e0 24 83 00           mov      ecx, 0x8324e0
005405FC  e8 5f 95 f5 ff           call     0x499b60
00540601  e8 ea 3c 0d 00           call     0x6142f0
00540606  b9 70 dc a3 00           mov      ecx, 0xa3dc70
0054060B  e8 00 50 07 00           call     0x5b5610
00540610  ff 15 24 a5 79 00        call     dword ptr [0x79a524]
00540616  2b 05 6c d5 a3 00        sub      eax, dword ptr [0xa3d56c]
0054061C  3d e8 03 00 00           cmp      eax, 0x3e8
00540621  7e 05                    jle      0x540628
00540623  b8 e8 03 00 00           mov      eax, 0x3e8
00540628  8b 15 70 d5 a3 00        mov      edx, dword ptr [0xa3d570]
0054062E  8b 0d 74 d5 a3 00        mov      ecx, dword ptr [0xa3d574]
00540634  03 d0                    add      edx, eax
00540636  41                       inc      ecx
00540637  89 15 70 d5 a3 00        mov      dword ptr [0xa3d570], edx
0054063D  89 0d 74 d5 a3 00        mov      dword ptr [0xa3d574], ecx
00540643  e8 28 31 0e 00           call     0x623770
00540648  e8 a3 3c 0d 00           call     0x6142f0
0054064D  e8 5e 19 f4 ff           call     0x481fb0
00540652  a0 b1 5d a3 00           mov      al, byte ptr [0xa35db1]
00540657  84 c0                    test     al, al
00540659  75 70                    jne      0x5406cb
0054065B  a0 78 0c a4 00           mov      al, byte ptr [0xa40c78]
00540660  84 c0                    test     al, al
00540662  75 67                    jne      0x5406cb
00540664  a0 50 62 86 00           mov      al, byte ptr [0x866250]
00540669  84 c0                    test     al, al
0054066B  75 5e                    jne      0x5406cb
0054066D  a0 b0 5d a3 00           mov      al, byte ptr [0xa35db0]
00540672  84 c0                    test     al, al
00540674  75 55                    jne      0x5406cb
00540676  8b 15 2c 0d a4 00        mov      edx, dword ptr [0xa40d2c]
0054067C  a1 74 91 ab 00           mov      eax, dword ptr [0xab9174]
00540681  42                       inc      edx
00540682  3b c7                    cmp      eax, edi
00540684  89 15 2c 0d a4 00        mov      dword ptr [0xa40d2c], edx
0054068A  74 11                    je       0x54069d
0054068C  8b ca                    mov      ecx, edx
0054068E  3b c1                    cmp      eax, ecx
00540690  7d 0b                    jge      0x54069d
00540692  e8 89 bd 11 00           call     0x65c420
00540697  89 3d 74 91 ab 00        mov      dword ptr [0xab9174], edi
0054069D  e8 be 02 00 00           call     0x540960
005406A2  e8 69 c8 1a 00           call     0x6ecf10
005406A7  e8 64 39 0d 00           call     0x614010
005406AC  8a 0d 58 09 a4 00        mov      cl, byte ptr [0xa40958]
005406B2  33 c0                    xor      eax, eax
005406B4  5f                       pop      edi
005406B5  5e                       pop      esi
005406B6  84 c9                    test     cl, cl
005406B8  5d                       pop      ebp
005406B9  c6 05 30 eb a6 00 00     mov      byte ptr [0xa6eb30], 0
005406C0  0f 94 c0                 sete     al
005406C3  5b                       pop      ebx
005406C4  81 c4 b4 01 00 00        add      esp, 0x1b4
005406CA  c3                       ret      
005406CB  c6 05 30 eb a6 00 00     mov      byte ptr [0xa6eb30], 0
005406D2  5f                       pop      edi
005406D3  5e                       pop      esi
005406D4  5d                       pop      ebp
005406D5  b0 01                    mov      al, 1
005406D7  5b                       pop      ebx
005406D8  81 c4 b4 01 00 00        add      esp, 0x1b4
005406DE  c3                       ret      
