
sub_00504AE0 0x00504AE0 size=272
00504AE0  83 ec 10                 sub      esp, 0x10
00504AE3  56                       push     esi
00504AE4  8b f1                    mov      esi, ecx
00504AE6  8b 86 ac 05 00 00        mov      eax, dword ptr [esi + 0x5ac]
00504AEC  83 f8 1b                 cmp      eax, 0x1b
00504AEF  74 0f                    je       0x504b00
00504AF1  83 f8 1c                 cmp      eax, 0x1c
00504AF4  74 0a                    je       0x504b00
00504AF6  83 f8 1d                 cmp      eax, 0x1d
00504AF9  74 05                    je       0x504b00
00504AFB  83 f8 1e                 cmp      eax, 0x1e
00504AFE  75 0a                    jne      0x504b0a
00504B00  8b 06                    mov      eax, dword ptr [esi]
00504B02  6a 00                    push     0
00504B04  6a 00                    push     0
00504B06  6a 1c                    push     0x1c
00504B08  eb 24                    jmp      0x504b2e
00504B0A  8a 86 c3 05 00 00        mov      al, byte ptr [esi + 0x5c3]
00504B10  84 c0                    test     al, al
00504B12  74 12                    je       0x504b26
00504B14  8b 16                    mov      edx, dword ptr [esi]
00504B16  6a 00                    push     0
00504B18  6a 00                    push     0
00504B1A  6a 02                    push     2
00504B1C  8b ce                    mov      ecx, esi
00504B1E  ff 92 dc 04 00 00        call     dword ptr [edx + 0x4dc]
00504B24  eb 10                    jmp      0x504b36
00504B26  8b 06                    mov      eax, dword ptr [esi]
00504B28  6a 00                    push     0
00504B2A  6a 00                    push     0
00504B2C  6a 00                    push     0
00504B2E  8b ce                    mov      ecx, esi
00504B30  ff 90 dc 04 00 00        call     dword ptr [eax + 0x4dc]
00504B36  53                       push     ebx
00504B37  8d 4c 24 08              lea      ecx, [esp + 8]
00504B3B  57                       push     edi
00504B3C  51                       push     ecx
00504B3D  8d 8e e0 02 00 00        lea      ecx, [esi + 0x2e0]
00504B43  e8 98 40 fb ff           call     0x4b8be0
00504B48  8b 38                    mov      edi, dword ptr [eax]
00504B4A  8d 96 88 00 00 00        lea      edx, [esi + 0x88]
00504B50  8b 1e                    mov      ebx, dword ptr [esi]
00504B52  6a 01                    push     1
00504B54  8b 02                    mov      eax, dword ptr [edx]
00504B56  6a 00                    push     0
00504B58  c1 ef 0c                 shr      edi, 0xc
00504B5B  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
00504B5E  47                       inc      edi
00504B5F  d1 ef                    shr      edi, 1
00504B61  8b 52 08                 mov      edx, dword ptr [edx + 8]
00504B64  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
00504B68  8b ce                    mov      ecx, esi
00504B6A  83 e7 07                 and      edi, 7
00504B6D  89 44 24 18              mov      dword ptr [esp + 0x18], eax
00504B71  89 54 24 20              mov      dword ptr [esp + 0x20], edx
00504B75  e8 56 fc 0c 00           call     0x5d47d0
00504B7A  50                       push     eax
00504B7B  8d 44 24 1c              lea      eax, [esp + 0x1c]
00504B7F  57                       push     edi
00504B80  50                       push     eax
00504B81  b9 e0 24 83 00           mov      ecx, 0x8324e0
00504B86  e8 75 34 04 00           call     0x548000
00504B8B  50                       push     eax
00504B8C  8b ce                    mov      ecx, esi
00504B8E  ff 93 94 01 00 00        call     dword ptr [ebx + 0x194]
00504B94  5f                       pop      edi
00504B95  5b                       pop      ebx
00504B96  85 c0                    test     eax, eax
00504B98  75 12                    jne      0x504bac
00504B9A  8b ce                    mov      ecx, esi
00504B9C  88 86 c4 05 00 00        mov      byte ptr [esi + 0x5c4], al
00504BA2  e8 b9 ff fb ff           call     0x4c4b60
00504BA7  5e                       pop      esi
00504BA8  83 c4 10                 add      esp, 0x10
00504BAB  c3                       ret      
00504BAC  8b ce                    mov      ecx, esi
00504BAE  c6 86 c4 05 00 00 01     mov      byte ptr [esi + 0x5c4], 1
00504BB5  e8 a6 ff fb ff           call     0x4c4b60
00504BBA  5e                       pop      esi
00504BBB  83 c4 10                 add      esp, 0x10
00504BBE  c3                       ret      
00504BBF  90                       nop      
00504BC0  55                       push     ebp
00504BC1  8b ec                    mov      ebp, esp
00504BC3  83 e4 f8                 and      esp, 0xfffffff8
00504BC6  83 ec 44                 sub      esp, 0x44
00504BC9  53                       push     ebx
00504BCA  56                       push     esi
00504BCB  8b 75 08                 mov      esi, dword ptr [ebp + 8]
00504BCE  57                       push     edi
00504BCF  8b c6                    mov      eax, esi
00504BD1  8b f9                    mov      edi, ecx
00504BD3  8b 08                    mov      ecx, dword ptr [eax]
00504BD5  89 4c 24 20              mov      dword ptr [esp + 0x20], ecx
00504BD9  8b cf                    mov      ecx, edi
00504BDB  8b 50 04                 mov      edx, dword ptr [eax + 4]
00504BDE  89 54 24 24              mov      dword ptr [esp + 0x24], edx
00504BE2  8b 17                    mov      edx, dword ptr [edi]
00504BE4  8b 40 08                 mov      eax, dword ptr [eax + 8]
00504BE7  89 44 24 28              mov      dword ptr [esp + 0x28], eax
00504BEB  8d 44 24 38              lea      eax, [esp + 0x38]
00504BEF  50                       push     eax
