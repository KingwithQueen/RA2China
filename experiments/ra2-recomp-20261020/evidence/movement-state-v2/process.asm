
sub_004A05F0 0x004A05F0 size=1483
004A05F0  83 ec 10                 sub      esp, 0x10
004A05F3  53                       push     ebx
004A05F4  55                       push     ebp
004A05F5  56                       push     esi
004A05F6  8b 74 24 20              mov      esi, dword ptr [esp + 0x20]
004A05FA  57                       push     edi
004A05FB  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A05FE  8b 01                    mov      eax, dword ptr [ecx]
004A0600  ff 90 a4 01 00 00        call     dword ptr [eax + 0x1a4]
004A0606  33 c9                    xor      ecx, ecx
004A0608  8d 7e fc                 lea      edi, [esi - 4]
004A060B  8a 88 1c 01 00 00        mov      cl, byte ptr [eax + 0x11c]
004A0611  8b c1                    mov      eax, ecx
004A0613  8b 4f 1c                 mov      ecx, dword ptr [edi + 0x1c]
004A0616  3b c1                    cmp      eax, ecx
004A0618  74 30                    je       0x4a064a
004A061A  89 4f 20                 mov      dword ptr [edi + 0x20], ecx
004A061D  6a 03                    push     3
004A061F  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A0623  89 47 1c                 mov      dword ptr [edi + 0x1c], eax
004A0626  e8 55 39 fc ff           call     0x463f80
004A062B  8d 57 24                 lea      edx, [edi + 0x24]
004A062E  b8 03 00 00 00           mov      eax, 3
004A0633  8b 4c 24 10              mov      ecx, dword ptr [esp + 0x10]
004A0637  89 0a                    mov      dword ptr [edx], ecx
004A0639  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
004A063D  89 4a 04                 mov      dword ptr [edx + 4], ecx
004A0640  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004A0644  89 4a 08                 mov      dword ptr [edx + 8], ecx
004A0647  89 42 0c                 mov      dword ptr [edx + 0xc], eax
004A064A  8b 46 54                 mov      eax, dword ptr [esi + 0x54]
004A064D  83 cd ff                 or       ebp, 0xffffffff
004A0650  33 db                    xor      ebx, ebx
004A0652  3b c5                    cmp      eax, ebp
004A0654  0f 84 16 01 00 00        je       0x4a0770
004A065A  38 5e 5f                 cmp      byte ptr [esi + 0x5f], bl
004A065D  0f 84 0d 01 00 00        je       0x4a0770
004A0663  53                       push     ebx
004A0664  8b cf                    mov      ecx, edi
004A0666  e8 95 09 00 00           call     0x4a1000
004A066B  84 c0                    test     al, al
004A066D  0f 85 fa 01 00 00        jne      0x4a086d
004A0673  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A0676  38 5a 7d                 cmp      byte ptr [edx + 0x7d], bl
004A0679  0f 84 ee 01 00 00        je       0x4a086d
004A067F  39 6e 54                 cmp      dword ptr [esi + 0x54], ebp
004A0682  0f 85 08 02 00 00        jne      0x4a0890
004A0688  8b 06                    mov      eax, dword ptr [esi]
004A068A  56                       push     esi
004A068B  ff 50 10                 call     dword ptr [eax + 0x10]
004A068E  84 c0                    test     al, al
004A0690  75 0f                    jne      0x4a06a1
004A0692  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A0695  39 a9 d0 04 00 00        cmp      dword ptr [ecx + 0x4d0], ebp
004A069B  0f 84 ef 01 00 00        je       0x4a0890
004A06A1  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A06A4  8b 11                    mov      edx, dword ptr [ecx]
004A06A6  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A06A9  83 f8 01                 cmp      eax, 1
004A06AC  75 0f                    jne      0x4a06bd
004A06AE  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A06B1  38 98 b9 05 00 00        cmp      byte ptr [eax + 0x5b9], bl
004A06B7  0f 85 d3 01 00 00        jne      0x4a0890
004A06BD  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A06C0  88 5c 24 24              mov      byte ptr [esp + 0x24], bl
004A06C4  8b 11                    mov      edx, dword ptr [ecx]
004A06C6  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A06C9  83 f8 01                 cmp      eax, 1
004A06CC  75 5c                    jne      0x4a072a
004A06CE  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A06D1  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A06D7  3b cb                    cmp      ecx, ebx
004A06D9  74 4f                    je       0x4a072a
004A06DB  8b 11                    mov      edx, dword ptr [ecx]
004A06DD  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A06E0  83 f8 0f                 cmp      eax, 0xf
004A06E3  75 45                    jne      0x4a072a
004A06E5  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A06E8  50                       push     eax
004A06E9  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A06EF  8d 44 24 14              lea      eax, [esp + 0x14]
004A06F3  50                       push     eax
004A06F4  8b 11                    mov      edx, dword ptr [ecx]
004A06F6  ff 52 4c                 call     dword ptr [edx + 0x4c]
004A06F9  8b 6e 30                 mov      ebp, dword ptr [esi + 0x30]
004A06FC  8b d0                    mov      edx, eax
004A06FE  8b 02                    mov      eax, dword ptr [edx]
004A0700  3b c5                    cmp      eax, ebp
004A0702  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A0705  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A0708  75 0a                    jne      0x4a0714
004A070A  3b 4e 34                 cmp      ecx, dword ptr [esi + 0x34]
004A070D  75 05                    jne      0x4a0714
004A070F  3b 56 38                 cmp      edx, dword ptr [esi + 0x38]
004A0712  74 16                    je       0x4a072a
004A0714  83 ec 0c                 sub      esp, 0xc
004A0717  8b 1e                    mov      ebx, dword ptr [esi]
004A0719  8b ec                    mov      ebp, esp
004A071B  56                       push     esi
004A071C  89 45 00                 mov      dword ptr [ebp], eax
004A071F  89 4d 04                 mov      dword ptr [ebp + 4], ecx
004A0722  89 55 08                 mov      dword ptr [ebp + 8], edx
004A0725  ff 53 44                 call     dword ptr [ebx + 0x44]
004A0728  33 db                    xor      ebx, ebx
004A072A  53                       push     ebx
004A072B  8d 44 24 28              lea      eax, [esp + 0x28]
004A072F  6a 01                    push     1
004A0731  50                       push     eax
004A0732  8b cf                    mov      ecx, edi
004A0734  e8 37 1f 00 00           call     0x4a2670
004A0739  38 5c 24 24              cmp      byte ptr [esp + 0x24], bl
004A073D  0f 85 2a 01 00 00        jne      0x4a086d
004A0743  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A0746  38 59 7d                 cmp      byte ptr [ecx + 0x7d], bl
004A0749  0f 84 1e 01 00 00        je       0x4a086d
004A074F  6a 01                    push     1
004A0751  8b cf                    mov      ecx, edi
004A0753  e8 a8 08 00 00           call     0x4a1000
004A0758  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A075B  38 5a 7d                 cmp      byte ptr [edx + 0x7d], bl
004A075E  0f 85 2c 01 00 00        jne      0x4a0890
004A0764  32 c0                    xor      al, al
004A0766  5f                       pop      edi
004A0767  5e                       pop      esi
004A0768  5d                       pop      ebp
004A0769  5b                       pop      ebx
004A076A  83 c4 10                 add      esp, 0x10
004A076D  c2 04 00                 ret      4
004A0770  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A0773  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A0779  3b cb                    cmp      ecx, ebx
004A077B  74 5c                    je       0x4a07d9
004A077D  8b 11                    mov      edx, dword ptr [ecx]
004A077F  ff 52 2c                 call     dword ptr [edx + 0x2c]
004A0782  83 f8 0b                 cmp      eax, 0xb
004A0785  75 52                    jne      0x4a07d9
004A0787  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A078A  8d 54 24 24              lea      edx, [esp + 0x24]
004A078E  52                       push     edx
004A078F  8b a9 94 04 00 00        mov      ebp, dword ptr [ecx + 0x494]
004A0795  8b 01                    mov      eax, dword ptr [ecx]
004A0797  83 c5 24                 add      ebp, 0x24
004A079A  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
004A07A0  66 8b 08                 mov      cx, word ptr [eax]
004A07A3  66 3b 4d 00              cmp      cx, word ptr [ebp]
004A07A7  75 30                    jne      0x4a07d9
004A07A9  66 8b 50 02              mov      dx, word ptr [eax + 2]
004A07AD  66 3b 55 02              cmp      dx, word ptr [ebp + 2]
004A07B1  75 26                    jne      0x4a07d9
004A07B3  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004A07B6  39 99 88 04 00 00        cmp      dword ptr [ecx + 0x488], ebx
004A07BC  0f 85 98 00 00 00        jne      0x4a085a
004A07C2  8b 01                    mov      eax, dword ptr [ecx]
004A07C4  6a 01                    push     1
004A07C6  53                       push     ebx
004A07C7  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A07CD  32 c0                    xor      al, al
004A07CF  5f                       pop      edi
004A07D0  5e                       pop      esi
004A07D1  5d                       pop      ebp
004A07D2  5b                       pop      ebx
004A07D3  83 c4 10                 add      esp, 0x10
004A07D6  c2 04 00                 ret      4
004A07D9  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A07DC  83 b9 98 00 00 00 05     cmp      dword ptr [ecx + 0x98], 5
004A07E3  0f 85 90 00 00 00        jne      0x4a0879
004A07E9  38 5e 5f                 cmp      byte ptr [esi + 0x5f], bl
004A07EC  0f 85 87 00 00 00        jne      0x4a0879
004A07F2  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
004A07F5  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A07FB  3b c2                    cmp      eax, edx
004A07FD  75 19                    jne      0x4a0818
004A07FF  8b 56 34                 mov      edx, dword ptr [esi + 0x34]
004A0802  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A0807  3b d0                    cmp      edx, eax
004A0809  75 0d                    jne      0x4a0818
004A080B  8b 46 38                 mov      eax, dword ptr [esi + 0x38]
004A080E  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A0814  3b c2                    cmp      eax, edx
004A0816  74 61                    je       0x4a0879
004A0818  8d 91 88 00 00 00        lea      edx, [ecx + 0x88]
004A081E  8b ea                    mov      ebp, edx
004A0820  8b 45 00                 mov      eax, dword ptr [ebp]
004A0823  3b 46 30                 cmp      eax, dword ptr [esi + 0x30]
004A0826  8b 55 04                 mov      edx, dword ptr [ebp + 4]
004A0829  8b 6d 08                 mov      ebp, dword ptr [ebp + 8]
004A082C  75 4b                    jne      0x4a0879
004A082E  3b 56 34                 cmp      edx, dword ptr [esi + 0x34]
004A0831  75 46                    jne      0x4a0879
004A0833  3b 6e 38                 cmp      ebp, dword ptr [esi + 0x38]
004A0836  75 41                    jne      0x4a0879
004A0838  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004A083B  39 99 88 04 00 00        cmp      dword ptr [ecx + 0x488], ebx
004A0841  75 17                    jne      0x4a085a
004A0843  8b 01                    mov      eax, dword ptr [ecx]
004A0845  6a 01                    push     1
004A0847  53                       push     ebx
004A0848  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004A084E  32 c0                    xor      al, al
004A0850  5f                       pop      edi
004A0851  5e                       pop      esi
004A0852  5d                       pop      ebp
004A0853  5b                       pop      ebx
004A0854  83 c4 10                 add      esp, 0x10
004A0857  c2 04 00                 ret      4
004A085A  e8 51 d1 02 00           call     0x4cd9b0
004A085F  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004A0862  6a 01                    push     1
004A0864  53                       push     ebx
004A0865  8b 11                    mov      edx, dword ptr [ecx]
004A0867  ff 92 14 04 00 00        call     dword ptr [edx + 0x414]
004A086D  32 c0                    xor      al, al
004A086F  5f                       pop      edi
004A0870  5e                       pop      esi
004A0871  5d                       pop      ebp
004A0872  5b                       pop      ebx
004A0873  83 c4 10                 add      esp, 0x10
004A0876  c2 04 00                 ret      4
004A0879  81 c1 e0 02 00 00        add      ecx, 0x2e0
004A087F  e8 0c 84 01 00           call     0x4b8c90
004A0884  84 c0                    test     al, al
004A0886  0f 84 0a 01 00 00        je       0x4a0996
004A088C  c6 46 5e 01              mov      byte ptr [esi + 0x5e], 1
004A0890  8b 0e                    mov      ecx, dword ptr [esi]
004A0892  56                       push     esi
004A0893  ff 91 80 00 00 00        call     dword ptr [ecx + 0x80]
004A0899  84 c0                    test     al, al
004A089B  0f 84 87 00 00 00        je       0x4a0928
004A08A1  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A08A6  b9 0a 00 00 00           mov      ecx, 0xa
004A08AB  99                       cdq      
004A08AC  f7 f9                    idiv     ecx
004A08AE  85 d2                    test     edx, edx
004A08B0  75 76                    jne      0x4a0928
004A08B2  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A08B5  38 59 79                 cmp      byte ptr [ecx + 0x79], bl
004A08B8  75 6e                    jne      0x4a0928
004A08BA  8b 11                    mov      edx, dword ptr [ecx]
004A08BC  ff 92 a4 01 00 00        call     dword ptr [edx + 0x1a4]
004A08C2  83 b8 ec 00 00 00 02     cmp      dword ptr [eax + 0xec], 2
004A08C9  75 5d                    jne      0x4a0928
004A08CB  a1 48 98 83 00           mov      eax, dword ptr [0x839848]
004A08D0  39 98 9c 00 00 00        cmp      dword ptr [eax + 0x9c], ebx
004A08D6  74 50                    je       0x4a0928
004A08D8  68 a8 01 00 00           push     0x1a8
004A08DD  e8 35 17 2e 00           call     0x782017
004A08E2  83 c4 04                 add      esp, 4
004A08E5  3b c3                    cmp      eax, ebx
004A08E7  74 3f                    je       0x4a0928
004A08E9  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A08EC  53                       push     ebx
004A08ED  81 c1 88 00 00 00        add      ecx, 0x88
004A08F3  68 00 06 00 00           push     0x600
004A08F8  6a 01                    push     1
004A08FA  53                       push     ebx
004A08FB  8b 11                    mov      edx, dword ptr [ecx]
004A08FD  89 54 24 20              mov      dword ptr [esp + 0x20], edx
004A0901  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A0904  89 54 24 24              mov      dword ptr [esp + 0x24], edx
004A0908  8d 54 24 20              lea      edx, [esp + 0x20]
004A090C  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
004A090F  52                       push     edx
004A0910  89 4c 24 2c              mov      dword ptr [esp + 0x2c], ecx
004A0914  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A091A  8b 91 9c 00 00 00        mov      edx, dword ptr [ecx + 0x9c]
004A0920  8b c8                    mov      ecx, eax
004A0922  52                       push     edx
004A0923  e8 e8 f7 f7 ff           call     0x420110
004A0928  8b 15 98 29 85 00        mov      edx, dword ptr [0x852998]
004A092E  8b 46 30                 mov      eax, dword ptr [esi + 0x30]
004A0931  3b c2                    cmp      eax, edx
004A0933  75 51                    jne      0x4a0986
004A0935  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A093B  8b 46 34                 mov      eax, dword ptr [esi + 0x34]
004A093E  3b c1                    cmp      eax, ecx
004A0940  75 44                    jne      0x4a0986
004A0942  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A0947  8b 7e 38                 mov      edi, dword ptr [esi + 0x38]
004A094A  3b f8                    cmp      edi, eax
004A094C  75 38                    jne      0x4a0986
004A094E  39 56 3c                 cmp      dword ptr [esi + 0x3c], edx
004A0951  75 33                    jne      0x4a0986
004A0953  39 4e 40                 cmp      dword ptr [esi + 0x40], ecx
004A0956  75 2e                    jne      0x4a0986
004A0958  39 46 44                 cmp      dword ptr [esi + 0x44], eax
004A095B  75 29                    jne      0x4a0986
004A095D  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A0960  83 b9 d0 04 00 00 ff     cmp      dword ptr [ecx + 0x4d0], -1
004A0967  75 1d                    jne      0x4a0986
004A0969  dd 81 68 04 00 00        fld      qword ptr [ecx + 0x468]
004A096F  dc 1d 10 b6 79 00        fcomp    qword ptr [0x79b610]
004A0975  df e0                    fnstsw   ax
004A0977  f6 c4 41                 test     ah, 0x41
004A097A  75 0a                    jne      0x4a0986
004A097C  8b 01                    mov      eax, dword ptr [ecx]
004A097E  53                       push     ebx
004A097F  53                       push     ebx
004A0980  ff 90 c8 04 00 00        call     dword ptr [eax + 0x4c8]
004A0986  8b 0e                    mov      ecx, dword ptr [esi]
004A0988  56                       push     esi
004A0989  ff 51 10                 call     dword ptr [ecx + 0x10]
004A098C  5f                       pop      edi
004A098D  5e                       pop      esi
004A098E  5d                       pop      ebp
004A098F  5b                       pop      ebx
004A0990  83 c4 10                 add      esp, 0x10
004A0993  c2 04 00                 ret      4
004A0996  38 5e 5e                 cmp      byte ptr [esi + 0x5e], bl
004A0999  74 2d                    je       0x4a09c8
004A099B  88 5e 5e                 mov      byte ptr [esi + 0x5e], bl
004A099E  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A09A1  53                       push     ebx
004A09A2  8b 01                    mov      eax, dword ptr [ecx]
004A09A4  ff 90 74 01 00 00        call     dword ptr [eax + 0x174]
004A09AA  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A09AD  38 58 7d                 cmp      byte ptr [eax + 0x7d], bl
004A09B0  74 0a                    je       0x4a09bc
004A09B2  38 58 76                 cmp      byte ptr [eax + 0x76], bl
004A09B5  75 05                    jne      0x4a09bc
004A09B7  38 58 7a                 cmp      byte ptr [eax + 0x7a], bl
004A09BA  74 0c                    je       0x4a09c8
004A09BC  32 c0                    xor      al, al
004A09BE  5f                       pop      edi
004A09BF  5e                       pop      esi
004A09C0  5d                       pop      ebp
004A09C1  5b                       pop      ebx
004A09C2  83 c4 10                 add      esp, 0x10
004A09C5  c2 04 00                 ret      4
004A09C8  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A09CB  8b 11                    mov      edx, dword ptr [ecx]
004A09CD  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A09D3  83 f8 05                 cmp      eax, 5
004A09D6  75 0e                    jne      0x4a09e6
004A09D8  8b 06                    mov      eax, dword ptr [esi]
004A09DA  56                       push     esi
004A09DB  ff 50 10                 call     dword ptr [eax + 0x10]
004A09DE  84 c0                    test     al, al
004A09E0  0f 84 aa fe ff ff        je       0x4a0890
004A09E6  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A09E9  8b 11                    mov      edx, dword ptr [ecx]
004A09EB  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A09F1  83 f8 10                 cmp      eax, 0x10
004A09F4  0f 84 96 fe ff ff        je       0x4a0890
004A09FA  8b 06                    mov      eax, dword ptr [esi]
004A09FC  56                       push     esi
004A09FD  ff 50 10                 call     dword ptr [eax + 0x10]
004A0A00  84 c0                    test     al, al
004A0A02  0f 85 9a 00 00 00        jne      0x4a0aa2
004A0A08  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A0A0B  83 b8 d0 04 00 00 ff     cmp      dword ptr [eax + 0x4d0], -1
004A0A12  0f 85 8a 00 00 00        jne      0x4a0aa2
004A0A18  38 98 25 03 00 00        cmp      byte ptr [eax + 0x325], bl
004A0A1E  74 48                    je       0x4a0a68
004A0A20  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A0A25  8b 4f 40                 mov      ecx, dword ptr [edi + 0x40]
004A0A28  3b c8                    cmp      ecx, eax
004A0A2A  75 1a                    jne      0x4a0a46
004A0A2C  8b 4f 44                 mov      ecx, dword ptr [edi + 0x44]
004A0A2F  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A0A35  3b ca                    cmp      ecx, edx
004A0A37  75 0d                    jne      0x4a0a46
004A0A39  8b 57 48                 mov      edx, dword ptr [edi + 0x48]
004A0A3C  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A0A42  3b d1                    cmp      edx, ecx
004A0A44  74 17                    je       0x4a0a5d
004A0A46  89 47 40                 mov      dword ptr [edi + 0x40], eax
004A0A49  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A0A4E  89 47 44                 mov      dword ptr [edi + 0x44], eax
004A0A51  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A0A57  89 4f 48                 mov      dword ptr [edi + 0x48], ecx
004A0A5A  88 5f 63                 mov      byte ptr [edi + 0x63], bl
004A0A5D  89 5e 4c                 mov      dword ptr [esi + 0x4c], ebx
004A0A60  89 5e 50                 mov      dword ptr [esi + 0x50], ebx
004A0A63  e9 28 fe ff ff           jmp      0x4a0890
004A0A68  8b 88 94 04 00 00        mov      ecx, dword ptr [eax + 0x494]
004A0A6E  3b cb                    cmp      ecx, ebx
004A0A70  0f 84 1a fe ff ff        je       0x4a0890
004A0A76  8b 11                    mov      edx, dword ptr [ecx]
004A0A78  50                       push     eax
004A0A79  8d 44 24 14              lea      eax, [esp + 0x14]
004A0A7D  50                       push     eax
004A0A7E  ff 52 4c                 call     dword ptr [edx + 0x4c]
004A0A81  8b 08                    mov      ecx, dword ptr [eax]
004A0A83  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A0A86  83 ec 0c                 sub      esp, 0xc
004A0A89  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A0A8C  8b 3e                    mov      edi, dword ptr [esi]
004A0A8E  8b ec                    mov      ebp, esp
004A0A90  56                       push     esi
004A0A91  89 4d 00                 mov      dword ptr [ebp], ecx
004A0A94  89 55 04                 mov      dword ptr [ebp + 4], edx
004A0A97  89 45 08                 mov      dword ptr [ebp + 8], eax
004A0A9A  ff 57 44                 call     dword ptr [edi + 0x44]
004A0A9D  e9 ee fd ff ff           jmp      0x4a0890
004A0AA2  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A0AA5  38 99 2d 03 00 00        cmp      byte ptr [ecx + 0x32d], bl
004A0AAB  0f 84 b1 00 00 00        je       0x4a0b62
004A0AB1  8b 11                    mov      edx, dword ptr [ecx]
004A0AB3  ff 92 6c 01 00 00        call     dword ptr [edx + 0x16c]
004A0AB9  83 f8 07                 cmp      eax, 7
004A0ABC  0f 84 a0 00 00 00        je       0x4a0b62
004A0AC2  8b 06                    mov      eax, dword ptr [esi]
004A0AC4  56                       push     esi
004A0AC5  ff 50 10                 call     dword ptr [eax + 0x10]
004A0AC8  84 c0                    test     al, al
004A0ACA  0f 84 92 00 00 00        je       0x4a0b62
004A0AD0  8b 4e 08                 mov      ecx, dword ptr [esi + 8]
004A0AD3  8d 46 30                 lea      eax, [esi + 0x30]
004A0AD6  50                       push     eax
004A0AD7  8b 11                    mov      edx, dword ptr [ecx]
004A0AD9  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004A0ADF  84 c0                    test     al, al
004A0AE1  75 7f                    jne      0x4a0b62
004A0AE3  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A0AE8  8b 4f 40                 mov      ecx, dword ptr [edi + 0x40]
004A0AEB  3b c8                    cmp      ecx, eax
004A0AED  75 1a                    jne      0x4a0b09
004A0AEF  8b 4f 44                 mov      ecx, dword ptr [edi + 0x44]
004A0AF2  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A0AF8  3b ca                    cmp      ecx, edx
004A0AFA  75 0d                    jne      0x4a0b09
004A0AFC  8b 57 48                 mov      edx, dword ptr [edi + 0x48]
004A0AFF  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A0B05  3b d1                    cmp      edx, ecx
004A0B07  74 17                    je       0x4a0b20
004A0B09  89 47 40                 mov      dword ptr [edi + 0x40], eax
004A0B0C  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A0B11  89 47 44                 mov      dword ptr [edi + 0x44], eax
004A0B14  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A0B1A  89 4f 48                 mov      dword ptr [edi + 0x48], ecx
004A0B1D  88 5f 63                 mov      byte ptr [edi + 0x63], bl
004A0B20  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004A0B23  39 99 88 04 00 00        cmp      dword ptr [ecx + 0x488], ebx
004A0B29  75 10                    jne      0x4a0b3b
004A0B2B  8b 11                    mov      edx, dword ptr [ecx]
004A0B2D  6a 01                    push     1
004A0B2F  53                       push     ebx
004A0B30  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A0B36  e9 55 fd ff ff           jmp      0x4a0890
004A0B3B  e8 70 ce 02 00           call     0x4cd9b0
004A0B40  8b 4f 0c                 mov      ecx, dword ptr [edi + 0xc]
004A0B43  6a 01                    push     1
004A0B45  53                       push     ebx
004A0B46  8b 01                    mov      eax, dword ptr [ecx]
004A0B48  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A0B4E  3a c3                    cmp      al, bl
004A0B50  0f 84 3a fd ff ff        je       0x4a0890
004A0B56  32 c0                    xor      al, al
004A0B58  5f                       pop      edi
004A0B59  5e                       pop      esi
004A0B5A  5d                       pop      ebp
004A0B5B  5b                       pop      ebx
004A0B5C  83 c4 10                 add      esp, 0x10
004A0B5F  c2 04 00                 ret      4
004A0B62  53                       push     ebx
004A0B63  8d 4c 24 28              lea      ecx, [esp + 0x28]
004A0B67  6a 01                    push     1
004A0B69  51                       push     ecx
004A0B6A  8b cf                    mov      ecx, edi
004A0B6C  88 5c 24 30              mov      byte ptr [esp + 0x30], bl
004A0B70  e8 fb 1a 00 00           call     0x4a2670
004A0B75  38 5c 24 24              cmp      byte ptr [esp + 0x24], bl
004A0B79  74 0c                    je       0x4a0b87
004A0B7B  32 c0                    xor      al, al
004A0B7D  5f                       pop      edi
004A0B7E  5e                       pop      esi
004A0B7F  5d                       pop      ebp
004A0B80  5b                       pop      ebx
004A0B81  83 c4 10                 add      esp, 0x10
004A0B84  c2 04 00                 ret      4
004A0B87  8b 56 08                 mov      edx, dword ptr [esi + 8]
004A0B8A  38 5a 7d                 cmp      byte ptr [edx + 0x7d], bl
004A0B8D  75 0c                    jne      0x4a0b9b
004A0B8F  32 c0                    xor      al, al
004A0B91  5f                       pop      edi
004A0B92  5e                       pop      esi
004A0B93  5d                       pop      ebp
004A0B94  5b                       pop      ebx
004A0B95  83 c4 10                 add      esp, 0x10
004A0B98  c2 04 00                 ret      4
004A0B9B  53                       push     ebx
004A0B9C  8b cf                    mov      ecx, edi
004A0B9E  e8 5d 04 00 00           call     0x4a1000
004A0BA3  8b 46 08                 mov      eax, dword ptr [esi + 8]
004A0BA6  38 58 7d                 cmp      byte ptr [eax + 0x7d], bl
004A0BA9  0f 85 e1 fc ff ff        jne      0x4a0890
004A0BAF  5f                       pop      edi
004A0BB0  5e                       pop      esi
004A0BB1  5d                       pop      ebp
004A0BB2  32 c0                    xor      al, al
004A0BB4  5b                       pop      ebx
004A0BB5  83 c4 10                 add      esp, 0x10
004A0BB8  c2 04 00                 ret      4
