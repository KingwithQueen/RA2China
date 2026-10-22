
sub_006DFED0 0x006DFED0 size=128
006DFED0  8b 44 24 04              mov      eax, dword ptr [esp + 4]
006DFED4  8b 15 80 02 ac 00        mov      edx, dword ptr [0xac0280]
006DFEDA  8d 48 18                 lea      ecx, [eax + 0x18]
006DFEDD  89 50 18                 mov      dword ptr [eax + 0x18], edx
006DFEE0  8b 15 84 02 ac 00        mov      edx, dword ptr [0xac0284]
006DFEE6  89 51 04                 mov      dword ptr [ecx + 4], edx
006DFEE9  8b 15 88 02 ac 00        mov      edx, dword ptr [0xac0288]
006DFEEF  89 51 08                 mov      dword ptr [ecx + 8], edx
006DFEF2  32 c9                    xor      cl, cl
006DFEF4  88 48 30                 mov      byte ptr [eax + 0x30], cl
006DFEF7  88 48 32                 mov      byte ptr [eax + 0x32], cl
006DFEFA  c2 04 00                 ret      4
006DFEFD  90                       nop      
006DFEFE  90                       nop      
006DFEFF  90                       nop      
006DFF00  8a 44 24 10              mov      al, byte ptr [esp + 0x10]
006DFF04  83 ec 28                 sub      esp, 0x28
006DFF07  84 c0                    test     al, al
006DFF09  53                       push     ebx
006DFF0A  55                       push     ebp
006DFF0B  56                       push     esi
006DFF0C  57                       push     edi
006DFF0D  8b e9                    mov      ebp, ecx
006DFF0F  0f 85 e1 03 00 00        jne      0x6e02f6
006DFF15  8d 44 24 3c              lea      eax, [esp + 0x3c]
006DFF19  b9 e0 24 83 00           mov      ecx, 0x8324e0
006DFF1E  50                       push     eax
006DFF1F  e8 dc 80 e6 ff           call     0x548000
006DFF24  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
006DFF2A  f6 c5 01                 test     ch, 1
006DFF2D  74 17                    je       0x6dff46
006DFF2F  8d 4c 24 3c              lea      ecx, [esp + 0x3c]
006DFF33  51                       push     ecx
006DFF34  b9 e0 24 83 00           mov      ecx, 0x8324e0
006DFF39  e8 c2 80 e6 ff           call     0x548000
006DFF3E  8b b0 e8 00 00 00        mov      esi, dword ptr [eax + 0xe8]
006DFF44  eb 15                    jmp      0x6dff5b
006DFF46  8d 54 24 3c              lea      edx, [esp + 0x3c]
006DFF4A  b9 e0 24 83 00           mov      ecx, 0x8324e0
006DFF4F  52                       push     edx
