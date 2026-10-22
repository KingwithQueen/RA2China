
sub_0049FEF0 0x0049FEF0 size=200
0049FEF0  8b 0d 98 29 85 00        mov      ecx, dword ptr [0x852998]
0049FEF6  56                       push     esi
0049FEF7  57                       push     edi
0049FEF8  8b 7c 24 0c              mov      edi, dword ptr [esp + 0xc]
0049FEFC  8b 47 3c                 mov      eax, dword ptr [edi + 0x3c]
0049FEFF  3b c1                    cmp      eax, ecx
0049FF01  75 18                    jne      0x49ff1b
0049FF03  8b 4f 40                 mov      ecx, dword ptr [edi + 0x40]
0049FF06  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
0049FF0B  3b c8                    cmp      ecx, eax
0049FF0D  75 0c                    jne      0x49ff1b
0049FF0F  8b 57 44                 mov      edx, dword ptr [edi + 0x44]
0049FF12  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
0049FF17  3b d0                    cmp      edx, eax
0049FF19  74 5e                    je       0x49ff79
0049FF1B  8b 4f 08                 mov      ecx, dword ptr [edi + 8]
0049FF1E  8b 01                    mov      eax, dword ptr [ecx]
0049FF20  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
0049FF26  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
0049FF2C  84 c9                    test     cl, cl
0049FF2E  74 49                    je       0x49ff79
0049FF30  8b 47 08                 mov      eax, dword ptr [edi + 8]
0049FF33  8a 88 b8 05 00 00        mov      cl, byte ptr [eax + 0x5b8]
0049FF39  84 c9                    test     cl, cl
0049FF3B  75 3c                    jne      0x49ff79
0049FF3D  8b b0 b0 05 00 00        mov      esi, dword ptr [eax + 0x5b0]
0049FF43  85 f6                    test     esi, esi
0049FF45  74 32                    je       0x49ff79
0049FF47  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
0049FF4D  85 c0                    test     eax, eax
0049FF4F  75 0a                    jne      0x49ff5b
0049FF51  68 03 40 00 80           push     0x80004003
0049FF56  e8 e5 59 2f 00           call     0x795940
0049FF5B  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
0049FF61  50                       push     eax
0049FF62  8b 08                    mov      ecx, dword ptr [eax]
0049FF64  ff 51 48                 call     dword ptr [ecx + 0x48]
0049FF67  8b b6 b0 05 00 00        mov      esi, dword ptr [esi + 0x5b0]
0049FF6D  85 f6                    test     esi, esi
0049FF6F  74 08                    je       0x49ff79
0049FF71  3b b6 b0 05 00 00        cmp      esi, dword ptr [esi + 0x5b0]
0049FF77  75 ce                    jne      0x49ff47
0049FF79  dd 47 4c                 fld      qword ptr [edi + 0x4c]
0049FF7C  dc 1d 48 ea 79 00        fcomp    qword ptr [0x79ea48]
0049FF82  df e0                    fnstsw   ax
0049FF84  f6 c4 01                 test     ah, 1
0049FF87  74 05                    je       0x49ff8e
0049FF89  dd 47 4c                 fld      qword ptr [edi + 0x4c]
0049FF8C  eb 06                    jmp      0x49ff94
0049FF8E  dd 05 48 ea 79 00        fld      qword ptr [0x79ea48]
0049FF94  dd 5f 4c                 fstp     qword ptr [edi + 0x4c]
0049FF97  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
0049FF9D  83 c7 30                 add      edi, 0x30
0049FFA0  89 17                    mov      dword ptr [edi], edx
0049FFA2  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
0049FFA7  89 47 04                 mov      dword ptr [edi + 4], eax
0049FFAA  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
0049FFB0  89 4f 08                 mov      dword ptr [edi + 8], ecx
0049FFB3  5f                       pop      edi
0049FFB4  5e                       pop      esi
0049FFB5  c2 04 00                 ret      4
