
sub_004C34E0 0x004C36EC size=54
004C36EC  8b 15 48 98 83 00        mov      edx, dword ptr [0x839848]
004C36F2  8b 35 2c 0d a4 00        mov      esi, dword ptr [0xa40d2c]
004C36F8  dd 82 c8 13 00 00        fld      qword ptr [edx + 0x13c8]
004C36FE  dc 0d 08 b6 79 00        fmul     qword ptr [0x79b608]
004C3704  e8 07 ba 2b 00           call     0x77f110
004C3709  8b 4c 24 34              mov      ecx, dword ptr [esp + 0x34]
004C370D  8b 55 00                 mov      edx, dword ptr [ebp]
004C3710  89 33                    mov      dword ptr [ebx], esi
004C3712  89 4b 04                 mov      dword ptr [ebx + 4], ecx
004C3715  8b cd                    mov      ecx, ebp
004C3717  89 43 08                 mov      dword ptr [ebx + 8], eax
004C371A  ff 92 8c 04 00 00        call     dword ptr [edx + 0x48c]

sub_004C4B60 0x004C4B60 size=39
004C4B60  56                       push     esi
004C4B61  8b f1                    mov      esi, ecx
004C4B63  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
004C4B69  85 c0                    test     eax, eax
004C4B6B  75 0a                    jne      0x4c4b77
004C4B6D  68 03 40 00 80           push     0x80004003
004C4B72  e8 c9 0d 2d 00           call     0x795940
004C4B77  8b 86 64 05 00 00        mov      eax, dword ptr [esi + 0x564]
004C4B7D  50                       push     eax
004C4B7E  8b 08                    mov      ecx, dword ptr [eax]
004C4B80  ff 51 48                 call     dword ptr [ecx + 0x48]
004C4B83  32 c0                    xor      al, al
004C4B85  5e                       pop      esi
004C4B86  c3                       ret      

sub_0049FF94 0x0049FF97 size=33
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
