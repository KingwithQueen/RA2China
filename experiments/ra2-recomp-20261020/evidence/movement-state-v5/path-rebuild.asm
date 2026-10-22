
sub_004C3000 0x004C3000 size=2247
004C3000  b8 9c 1f 00 00           mov      eax, 0x1f9c
004C3005  e8 46 08 2c 00           call     0x783850
004C300A  8b 84 24 a4 1f 00 00     mov      eax, dword ptr [esp + 0x1fa4]
004C3011  53                       push     ebx
004C3012  55                       push     ebp
004C3013  56                       push     esi
004C3014  85 c0                    test     eax, eax
004C3016  8b e9                    mov      ebp, ecx
004C3018  75 0a                    jne      0x4c3024
004C301A  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
004C3024  0f bf 84 24 ac 1f 00 00  movsx    eax, word ptr [esp + 0x1fac]
004C302C  0f bf 8c 24 ae 1f 00 00  movsx    ecx, word ptr [esp + 0x1fae]
004C3034  8b 55 00                 mov      edx, dword ptr [ebp]
004C3037  c7 44 24 20 00 00 00 00  mov      dword ptr [esp + 0x20], 0
004C303F  c1 e0 08                 shl      eax, 8
004C3042  05 80 00 00 00           add      eax, 0x80
004C3047  c1 e1 08                 shl      ecx, 8
004C304A  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004C304E  81 c1 80 00 00 00        add      ecx, 0x80
004C3054  8d 44 24 18              lea      eax, [esp + 0x18]
004C3058  89 4c 24 1c              mov      dword ptr [esp + 0x1c], ecx
004C305C  50                       push     eax
004C305D  8b cd                    mov      ecx, ebp
004C305F  ff 92 ac 02 00 00        call     dword ptr [edx + 0x2ac]
004C3065  84 c0                    test     al, al
004C3067  75 16                    jne      0x4c307f
004C3069  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
004C3073  5e                       pop      esi
004C3074  5d                       pop      ebp
004C3075  5b                       pop      ebx
004C3076  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C307C  c2 0c 00                 ret      0xc
004C307F  0f bf b4 24 ac 1f 00 00  movsx    esi, word ptr [esp + 0x1fac]
004C3087  8b 55 00                 mov      edx, dword ptr [ebp]
004C308A  57                       push     edi
004C308B  0f bf bc 24 b2 1f 00 00  movsx    edi, word ptr [esp + 0x1fb2]
004C3093  8d 44 24 40              lea      eax, [esp + 0x40]
004C3097  8b cd                    mov      ecx, ebp
004C3099  c1 e6 08                 shl      esi, 8
004C309C  c1 e7 08                 shl      edi, 8
004C309F  50                       push     eax
004C30A0  81 c6 80 00 00 00        add      esi, 0x80
004C30A6  81 c7 80 00 00 00        add      edi, 0x80
004C30AC  ff 52 48                 call     dword ptr [edx + 0x48]
004C30AF  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004C30B2  8b 50 04                 mov      edx, dword ptr [eax + 4]
004C30B5  8b 00                    mov      eax, dword ptr [eax]
004C30B7  2b d7                    sub      edx, edi
004C30B9  51                       push     ecx
004C30BA  2b c6                    sub      eax, esi
004C30BC  52                       push     edx
004C30BD  50                       push     eax
004C30BE  8d 4c 24 40              lea      ecx, [esp + 0x40]
004C30C2  e8 69 85 f5 ff           call     0x41b630
004C30C7  8b 08                    mov      ecx, dword ptr [eax]
004C30C9  83 ec 08                 sub      esp, 8
004C30CC  89 4c 24 24              mov      dword ptr [esp + 0x24], ecx
004C30D0  8b 50 04                 mov      edx, dword ptr [eax + 4]
004C30D3  db 44 24 24              fild     dword ptr [esp + 0x24]
004C30D7  8b 40 08                 mov      eax, dword ptr [eax + 8]
004C30DA  89 54 24 28              mov      dword ptr [esp + 0x28], edx
004C30DE  db 44 24 28              fild     dword ptr [esp + 0x28]
004C30E2  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004C30E6  db 44 24 2c              fild     dword ptr [esp + 0x2c]
004C30EA  d9 c0                    fld      st(0)
004C30EC  d8 c9                    fmul     st(1)
004C30EE  d9 c2                    fld      st(2)
004C30F0  d8 cb                    fmul     st(3)
004C30F2  de c1                    faddp    st(1)
004C30F4  d9 c3                    fld      st(3)
004C30F6  d8 cc                    fmul     st(4)
004C30F8  de c1                    faddp    st(1)
004C30FA  dd 1c 24                 fstp     qword ptr [esp]
004C30FD  dd d8                    fstp     st(0)
004C30FF  dd d8                    fstp     st(0)
004C3101  dd d8                    fstp     st(0)
004C3103  e8 08 73 ff ff           call     0x4ba410
004C3108  83 c4 08                 add      esp, 8
004C310B  e8 00 c0 2b 00           call     0x77f110
004C3110  8b 8d c4 04 00 00        mov      ecx, dword ptr [ebp + 0x4c4]
004C3116  8b f0                    mov      esi, eax
004C3118  85 c9                    test     ecx, ecx
004C311A  89 74 24 28              mov      dword ptr [esp + 0x28], esi
004C311E  74 0b                    je       0x4c312b
004C3120  e8 7b b5 1f 00           call     0x6be6a0
004C3125  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004C3129  eb 10                    jmp      0x4c313b
004C312B  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004C3131  8b 91 80 13 00 00        mov      edx, dword ptr [ecx + 0x1380]
004C3137  89 54 24 14              mov      dword ptr [esp + 0x14], edx
004C313B  8b 45 00                 mov      eax, dword ptr [ebp]
004C313E  8b cd                    mov      ecx, ebp
004C3140  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004C3146  8a 98 a0 0a 00 00        mov      bl, byte ptr [eax + 0xaa0]
004C314C  8b 7d 00                 mov      edi, dword ptr [ebp]
004C314F  6a 01                    push     1
004C3151  6a 00                    push     0
004C3153  6a ff                    push     -1
004C3155  8d 8c 24 bc 1f 00 00     lea      ecx, [esp + 0x1fbc]
004C315C  6a ff                    push     -1
004C315E  51                       push     ecx
004C315F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3164  e8 07 4f 08 00           call     0x548070
004C3169  50                       push     eax
004C316A  8b cd                    mov      ecx, ebp
004C316C  ff 97 94 01 00 00        call     dword ptr [edi + 0x194]
004C3172  83 f8 06                 cmp      eax, 6
004C3175  0f 85 3d 02 00 00        jne      0x4c33b8
004C317B  3b 74 24 14              cmp      esi, dword ptr [esp + 0x14]
004C317F  0f 8e 5b 03 00 00        jle      0x4c34e0
004C3185  84 db                    test     bl, bl
004C3187  0f 85 53 03 00 00        jne      0x4c34e0
004C318D  8b 55 00                 mov      edx, dword ptr [ebp]
004C3190  8b cd                    mov      ecx, ebp
004C3192  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C3198  8b 80 00 05 00 00        mov      eax, dword ptr [eax + 0x500]
004C319E  8b 55 00                 mov      edx, dword ptr [ebp]
004C31A1  8b cd                    mov      ecx, ebp
004C31A3  8b 34 85 00 12 7a 00     mov      esi, dword ptr [eax*4 + 0x7a1200]
004C31AA  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C31B0  8a 88 f5 0a 00 00        mov      cl, byte ptr [eax + 0xaf5]
004C31B6  84 c9                    test     cl, cl
004C31B8  74 22                    je       0x4c31dc
004C31BA  8d 84 24 b0 1f 00 00     lea      eax, [esp + 0x1fb0]
004C31C1  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C31C6  50                       push     eax
004C31C7  e8 a4 4e 08 00           call     0x548070
004C31CC  8b c8                    mov      ecx, eax
004C31CE  e8 2d 90 fb ff           call     0x47c200
004C31D3  84 c0                    test     al, al
004C31D5  c6 44 24 14 01           mov      byte ptr [esp + 0x14], 1
004C31DA  75 05                    jne      0x4c31e1
004C31DC  c6 44 24 14 00           mov      byte ptr [esp + 0x14], 0
004C31E1  8b 55 00                 mov      edx, dword ptr [ebp]
004C31E4  8a 5d 79                 mov      bl, byte ptr [ebp + 0x79]
004C31E7  8d 44 24 30              lea      eax, [esp + 0x30]
004C31EB  bf 01 00 00 00           mov      edi, 1
004C31F0  6a 00                    push     0
004C31F2  50                       push     eax
004C31F3  8b cd                    mov      ecx, ebp
004C31F5  89 7c 24 28              mov      dword ptr [esp + 0x28], edi
004C31F9  ff 92 a0 01 00 00        call     dword ptr [edx + 0x1a0]
004C31FF  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004C3203  50                       push     eax
004C3204  57                       push     edi
004C3205  51                       push     ecx
004C3206  57                       push     edi
004C3207  8b d7                    mov      edx, edi
004C3209  8b 45 00                 mov      eax, dword ptr [ebp]
004C320C  6a 00                    push     0
004C320E  52                       push     edx
004C320F  57                       push     edi
004C3210  53                       push     ebx
004C3211  56                       push     esi
004C3212  53                       push     ebx
004C3213  8d 4c 24 44              lea      ecx, [esp + 0x44]
004C3217  56                       push     esi
004C3218  51                       push     ecx
004C3219  8b cd                    mov      ecx, ebp
004C321B  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
004C3221  50                       push     eax
004C3222  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3227  e8 c4 c6 08 00           call     0x54f8f0
004C322C  8b 55 00                 mov      edx, dword ptr [ebp]
004C322F  50                       push     eax
004C3230  8b cd                    mov      ecx, ebp
004C3232  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C3238  8b 80 a4 05 00 00        mov      eax, dword ptr [eax + 0x5a4]
004C323E  8d 8c 24 dc 1f 00 00     lea      ecx, [esp + 0x1fdc]
004C3245  50                       push     eax
004C3246  8d 54 24 5c              lea      edx, [esp + 0x5c]
004C324A  51                       push     ecx
004C324B  52                       push     edx
004C324C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3251  e8 8a d0 08 00           call     0x5502e0
004C3256  8b 00                    mov      eax, dword ptr [eax]
004C3258  0f bf b4 24 b2 1f 00 00  movsx    esi, word ptr [esp + 0x1fb2]
004C3260  89 44 24 10              mov      dword ptr [esp + 0x10], eax
004C3264  0f bf 7c 24 12           movsx    edi, word ptr [esp + 0x12]
004C3269  8b c7                    mov      eax, edi
004C326B  0f bf 9c 24 b0 1f 00 00  movsx    ebx, word ptr [esp + 0x1fb0]
004C3273  2b c6                    sub      eax, esi
004C3275  99                       cdq      
004C3276  8b c8                    mov      ecx, eax
004C3278  0f bf 44 24 10           movsx    eax, word ptr [esp + 0x10]
004C327D  33 ca                    xor      ecx, edx
004C327F  89 44 24 30              mov      dword ptr [esp + 0x30], eax
004C3283  2b c3                    sub      eax, ebx
004C3285  2b ca                    sub      ecx, edx
004C3287  99                       cdq      
004C3288  33 c2                    xor      eax, edx
004C328A  2b c2                    sub      eax, edx
004C328C  3b c1                    cmp      eax, ecx
004C328E  89 44 24 18              mov      dword ptr [esp + 0x18], eax
004C3292  7f 04                    jg       0x4c3298
004C3294  89 4c 24 18              mov      dword ptr [esp + 0x18], ecx
004C3298  66 8b 4c 24 10           mov      cx, word ptr [esp + 0x10]
004C329D  66 3b 0d 00 5f 86 00     cmp      cx, word ptr [0x865f00]
004C32A4  75 12                    jne      0x4c32b8
004C32A6  66 8b 54 24 12           mov      dx, word ptr [esp + 0x12]
004C32AB  66 3b 15 02 5f 86 00     cmp      dx, word ptr [0x865f02]
004C32B2  0f 84 28 02 00 00        je       0x4c34e0
004C32B8  8b 44 24 30              mov      eax, dword ptr [esp + 0x30]
004C32BC  83 ec 08                 sub      esp, 8
004C32BF  c1 e7 08                 shl      edi, 8
004C32C2  c1 e6 08                 shl      esi, 8
004C32C5  c1 e0 08                 shl      eax, 8
004C32C8  81 c7 80 00 00 00        add      edi, 0x80
004C32CE  81 c6 80 00 00 00        add      esi, 0x80
004C32D4  c1 e3 08                 shl      ebx, 8
004C32D7  05 80 00 00 00           add      eax, 0x80
004C32DC  81 c3 80 00 00 00        add      ebx, 0x80
004C32E2  2b f7                    sub      esi, edi
004C32E4  2b d8                    sub      ebx, eax
004C32E6  89 74 24 28              mov      dword ptr [esp + 0x28], esi
004C32EA  89 5c 24 24              mov      dword ptr [esp + 0x24], ebx
004C32EE  db 44 24 28              fild     dword ptr [esp + 0x28]
004C32F2  db 44 24 24              fild     dword ptr [esp + 0x24]
004C32F6  d9 c0                    fld      st(0)
004C32F8  d8 c9                    fmul     st(1)
004C32FA  d9 c2                    fld      st(2)
004C32FC  d8 cb                    fmul     st(3)
004C32FE  de c1                    faddp    st(1)
004C3300  dd 1c 24                 fstp     qword ptr [esp]
004C3303  dd d8                    fstp     st(0)
004C3305  dd d8                    fstp     st(0)
004C3307  e8 04 71 ff ff           call     0x4ba410
004C330C  83 c4 08                 add      esp, 8
004C330F  e8 fc bd 2b 00           call     0x77f110
004C3314  3b 44 24 28              cmp      eax, dword ptr [esp + 0x28]
004C3318  0f 8d c2 01 00 00        jge      0x4c34e0
004C331E  8a 44 24 14              mov      al, byte ptr [esp + 0x14]
004C3322  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3327  f6 d8                    neg      al
004C3329  1b c0                    sbb      eax, eax
004C332B  f7 d8                    neg      eax
004C332D  48                       dec      eax
004C332E  50                       push     eax
004C332F  8d 84 24 b4 1f 00 00     lea      eax, [esp + 0x1fb4]
004C3336  50                       push     eax
004C3337  e8 34 4d 08 00           call     0x548070
004C333C  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004C3342  8d 54 24 14              lea      edx, [esp + 0x14]
004C3346  c1 e9 08                 shr      ecx, 8
004C3349  80 e1 01                 and      cl, 1
004C334C  51                       push     ecx
004C334D  52                       push     edx
004C334E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3353  e8 18 4d 08 00           call     0x548070
004C3358  8b 80 40 01 00 00        mov      eax, dword ptr [eax + 0x140]
004C335E  8d 8c 24 b8 1f 00 00     lea      ecx, [esp + 0x1fb8]
004C3365  c1 e8 08                 shr      eax, 8
004C3368  24 01                    and      al, 1
004C336A  8d 54 24 18              lea      edx, [esp + 0x18]
004C336E  50                       push     eax
004C336F  55                       push     ebp
004C3370  51                       push     ecx
004C3371  52                       push     edx
004C3372  b9 c8 15 83 00           mov      ecx, 0x8315c8
004C3377  e8 b4 76 f6 ff           call     0x42aa30
004C337C  8b 4c 24 18              mov      ecx, dword ptr [esp + 0x18]
004C3380  83 c1 06                 add      ecx, 6
004C3383  3b c1                    cmp      eax, ecx
004C3385  0f 8f 55 01 00 00        jg       0x4c34e0
004C338B  8b 75 00                 mov      esi, dword ptr [ebp]
004C338E  8d 54 24 10              lea      edx, [esp + 0x10]
004C3392  6a 01                    push     1
004C3394  52                       push     edx
004C3395  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C339A  e8 d1 4c 08 00           call     0x548070
004C339F  50                       push     eax
004C33A0  8b cd                    mov      ecx, ebp
004C33A2  ff 96 10 04 00 00        call     dword ptr [esi + 0x410]
004C33A8  8b 44 24 10              mov      eax, dword ptr [esp + 0x10]
004C33AC  89 84 24 b0 1f 00 00     mov      dword ptr [esp + 0x1fb0], eax
004C33B3  e9 28 01 00 00           jmp      0x4c34e0
004C33B8  83 f8 07                 cmp      eax, 7
004C33BB  0f 85 1f 01 00 00        jne      0x4c34e0
004C33C1  84 db                    test     bl, bl
004C33C3  0f 85 17 01 00 00        jne      0x4c34e0
004C33C9  8d 8c 24 b0 1f 00 00     lea      ecx, [esp + 0x1fb0]
004C33D0  51                       push     ecx
004C33D1  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C33D6  e8 95 4c 08 00           call     0x548070
004C33DB  8b c8                    mov      ecx, eax
004C33DD  e8 ce e3 fa ff           call     0x4717b0
004C33E2  85 c0                    test     eax, eax
004C33E4  0f 84 f6 00 00 00        je       0x4c34e0
004C33EA  8b 55 00                 mov      edx, dword ptr [ebp]
004C33ED  8b cd                    mov      ecx, ebp
004C33EF  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C33F5  8b 80 00 05 00 00        mov      eax, dword ptr [eax + 0x500]
004C33FB  8b 55 00                 mov      edx, dword ptr [ebp]
004C33FE  8b cd                    mov      ecx, ebp
004C3400  8b 34 85 00 12 7a 00     mov      esi, dword ptr [eax*4 + 0x7a1200]
004C3407  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C340D  8a 88 f5 0a 00 00        mov      cl, byte ptr [eax + 0xaf5]
004C3413  84 c9                    test     cl, cl
004C3415  74 22                    je       0x4c3439
004C3417  8d 84 24 b0 1f 00 00     lea      eax, [esp + 0x1fb0]
004C341E  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3423  50                       push     eax
004C3424  e8 47 4c 08 00           call     0x548070
004C3429  8b c8                    mov      ecx, eax
004C342B  e8 d0 8d fb ff           call     0x47c200
004C3430  84 c0                    test     al, al
004C3432  c6 44 24 18 01           mov      byte ptr [esp + 0x18], 1
004C3437  75 05                    jne      0x4c343e
004C3439  c6 44 24 18 00           mov      byte ptr [esp + 0x18], 0
004C343E  8b 55 00                 mov      edx, dword ptr [ebp]
004C3441  8a 5d 79                 mov      bl, byte ptr [ebp + 0x79]
004C3444  8d 44 24 2c              lea      eax, [esp + 0x2c]
004C3448  bf 01 00 00 00           mov      edi, 1
004C344D  6a 00                    push     0
004C344F  50                       push     eax
004C3450  8b cd                    mov      ecx, ebp
004C3452  89 7c 24 28              mov      dword ptr [esp + 0x28], edi
004C3456  ff 92 a0 01 00 00        call     dword ptr [edx + 0x1a0]
004C345C  8b 4c 24 1c              mov      ecx, dword ptr [esp + 0x1c]
004C3460  50                       push     eax
004C3461  57                       push     edi
004C3462  51                       push     ecx
004C3463  57                       push     edi
004C3464  8b d7                    mov      edx, edi
004C3466  8b 45 00                 mov      eax, dword ptr [ebp]
004C3469  6a 00                    push     0
004C346B  52                       push     edx
004C346C  57                       push     edi
004C346D  53                       push     ebx
004C346E  56                       push     esi
004C346F  53                       push     ebx
004C3470  8d 4c 24 54              lea      ecx, [esp + 0x54]
004C3474  56                       push     esi
004C3475  51                       push     ecx
004C3476  8b cd                    mov      ecx, ebp
004C3478  ff 90 a0 01 00 00        call     dword ptr [eax + 0x1a0]
004C347E  50                       push     eax
004C347F  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3484  e8 67 c4 08 00           call     0x54f8f0
004C3489  8b 55 00                 mov      edx, dword ptr [ebp]
004C348C  50                       push     eax
004C348D  8b cd                    mov      ecx, ebp
004C348F  ff 92 80 00 00 00        call     dword ptr [edx + 0x80]
004C3495  8b 80 a4 05 00 00        mov      eax, dword ptr [eax + 0x5a4]
004C349B  8d 8c 24 dc 1f 00 00     lea      ecx, [esp + 0x1fdc]
004C34A2  50                       push     eax
004C34A3  8d 54 24 60              lea      edx, [esp + 0x60]
004C34A7  51                       push     ecx
004C34A8  52                       push     edx
004C34A9  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C34AE  e8 2d ce 08 00           call     0x5502e0
004C34B3  8b 00                    mov      eax, dword ptr [eax]
004C34B5  8b 75 00                 mov      esi, dword ptr [ebp]
004C34B8  8d 4c 24 14              lea      ecx, [esp + 0x14]
004C34BC  57                       push     edi
004C34BD  51                       push     ecx
004C34BE  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C34C3  89 44 24 1c              mov      dword ptr [esp + 0x1c], eax
004C34C7  e8 a4 4b 08 00           call     0x548070
004C34CC  50                       push     eax
004C34CD  8b cd                    mov      ecx, ebp
004C34CF  ff 96 10 04 00 00        call     dword ptr [esi + 0x410]
004C34D5  8b 54 24 14              mov      edx, dword ptr [esp + 0x14]
004C34D9  89 94 24 b0 1f 00 00     mov      dword ptr [esp + 0x1fb0], edx
004C34E0  8b 45 00                 mov      eax, dword ptr [ebp]
004C34E3  6a 00                    push     0
004C34E5  8b cd                    mov      ecx, ebp
004C34E7  ff 90 1c 01 00 00        call     dword ptr [eax + 0x11c]
004C34ED  8b 9c 24 b4 1f 00 00     mov      ebx, dword ptr [esp + 0x1fb4]
004C34F4  85 db                    test     ebx, ebx
004C34F6  75 0a                    jne      0x4c3502
004C34F8  c7 85 d0 04 00 00 ff ff ff ff mov      dword ptr [ebp + 0x4d0], 0xffffffff
004C3502  8b 8c 24 b8 1f 00 00     mov      ecx, dword ptr [esp + 0x1fb8]
004C3509  8d 54 24 6c              lea      edx, [esp + 0x6c]
004C350D  51                       push     ecx
004C350E  53                       push     ebx
004C350F  6a 00                    push     0
004C3511  68 d0 07 00 00           push     0x7d0
004C3516  8d 84 24 c0 1f 00 00     lea      eax, [esp + 0x1fc0]
004C351D  52                       push     edx
004C351E  50                       push     eax
004C351F  8b cd                    mov      ecx, ebp
004C3521  e8 2a 7e ff ff           call     0x4bb350
004C3526  8b f8                    mov      edi, eax
004C3528  85 ff                    test     edi, edi
004C352A  89 7c 24 14              mov      dword ptr [esp + 0x14], edi
004C352E  74 4b                    je       0x4c357b
004C3530  8b 47 04                 mov      eax, dword ptr [edi + 4]
004C3533  85 c0                    test     eax, eax
004C3535  74 44                    je       0x4c357b
004C3537  8b 55 00                 mov      edx, dword ptr [ebp]
004C353A  8b f7                    mov      esi, edi
004C353C  b9 08 00 00 00           mov      ecx, 8
004C3541  8d 7c 24 4c              lea      edi, [esp + 0x4c]
004C3545  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004C3547  8d 44 24 4c              lea      eax, [esp + 0x4c]
004C354B  8b cd                    mov      ecx, ebp
004C354D  50                       push     eax
004C354E  ff 92 c4 04 00 00        call     dword ptr [edx + 0x4c4]
004C3554  8b 4c 24 14              mov      ecx, dword ptr [esp + 0x14]
004C3558  b8 18 00 00 00           mov      eax, 0x18
004C355D  2b c3                    sub      eax, ebx
004C355F  8b 49 08                 mov      ecx, dword ptr [ecx + 8]
004C3562  3b c8                    cmp      ecx, eax
004C3564  7d 02                    jge      0x4c3568
004C3566  8b c1                    mov      eax, ecx
004C3568  8b c8                    mov      ecx, eax
004C356A  8d 74 24 6c              lea      esi, [esp + 0x6c]
004C356E  8d bc 9d d0 04 00 00     lea      edi, [ebp + ebx*4 + 0x4d0]
004C3575  f3 a5                    rep movsd dword ptr es:[edi], dword ptr [esi]
004C3577  8b 7c 24 14              mov      edi, dword ptr [esp + 0x14]
004C357B  8b 55 00                 mov      edx, dword ptr [ebp]
004C357E  6a 01                    push     1
004C3580  8b cd                    mov      ecx, ebp
004C3582  ff 92 1c 01 00 00        call     dword ptr [edx + 0x11c]
004C3588  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004C358D  8d 9d 30 05 00 00        lea      ebx, [ebp + 0x530]
004C3593  8b d3                    mov      edx, ebx
004C3595  33 c9                    xor      ecx, ecx
004C3597  89 02                    mov      dword ptr [edx], eax
004C3599  8b 44 24 38              mov      eax, dword ptr [esp + 0x38]
004C359D  89 42 04                 mov      dword ptr [edx + 4], eax
004C35A0  89 4a 08                 mov      dword ptr [edx + 8], ecx
004C35A3  8b 55 00                 mov      edx, dword ptr [ebp]
004C35A6  8b cd                    mov      ecx, ebp
004C35A8  ff 52 2c                 call     dword ptr [edx + 0x2c]
004C35AB  83 f8 01                 cmp      eax, 1
004C35AE  0f 85 0d 01 00 00        jne      0x4c36c1
004C35B4  83 bd d0 04 00 00 ff     cmp      dword ptr [ebp + 0x4d0], -1
004C35BB  0f 84 00 01 00 00        je       0x4c36c1
004C35C1  8b b5 b0 05 00 00        mov      esi, dword ptr [ebp + 0x5b0]
004C35C7  33 c0                    xor      eax, eax
004C35C9  85 ff                    test     edi, edi
004C35CB  74 06                    je       0x4c35d3
004C35CD  8b 47 08                 mov      eax, dword ptr [edi + 8]
004C35D0  83 e8 02                 sub      eax, 2
004C35D3  8b 8c 24 b0 1f 00 00     mov      ecx, dword ptr [esp + 0x1fb0]
004C35DA  85 f6                    test     esi, esi
004C35DC  89 4c 24 10              mov      dword ptr [esp + 0x10], ecx
004C35E0  0f 84 db 00 00 00        je       0x4c36c1
004C35E6  8a 8d b8 05 00 00        mov      cl, byte ptr [ebp + 0x5b8]
004C35EC  84 c9                    test     cl, cl
004C35EE  0f 85 cd 00 00 00        jne      0x4c36c1
004C35F4  8d 54 84 6c              lea      edx, [esp + eax*4 + 0x6c]
004C35F8  89 54 24 28              mov      dword ptr [esp + 0x28], edx
004C35FC  8d 44 24 10              lea      eax, [esp + 0x10]
004C3600  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3605  50                       push     eax
004C3606  e8 65 4a 08 00           call     0x548070
004C360B  8b 4c 24 28              mov      ecx, dword ptr [esp + 0x28]
004C360F  8b 11                    mov      edx, dword ptr [ecx]
004C3611  83 c2 04                 add      edx, 4
004C3614  81 e2 07 00 00 80        and      edx, 0x80000007
004C361A  79 05                    jns      0x4c3621
004C361C  4a                       dec      edx
004C361D  83 ca f8                 or       edx, 0xfffffff8
004C3620  42                       inc      edx
004C3621  52                       push     edx
004C3622  8b c8                    mov      ecx, eax
004C3624  e8 97 34 fb ff           call     0x476ac0
004C3629  8b 40 24                 mov      eax, dword ptr [eax + 0x24]
004C362C  89 44 24 10              mov      dword ptr [esp + 0x10], eax
004C3630  8b 8e 94 04 00 00        mov      ecx, dword ptr [esi + 0x494]
004C3636  85 c9                    test     ecx, ecx
004C3638  74 3b                    je       0x4c3675
004C363A  8b 11                    mov      edx, dword ptr [ecx]
004C363C  8d 44 24 34              lea      eax, [esp + 0x34]
004C3640  6a 00                    push     0
004C3642  50                       push     eax
004C3643  ff 52 4c                 call     dword ptr [edx + 0x4c]
004C3646  8b f8                    mov      edi, eax
004C3648  8b 07                    mov      eax, dword ptr [edi]
004C364A  99                       cdq      
004C364B  81 e2 ff 00 00 00        and      edx, 0xff
004C3651  03 c2                    add      eax, edx
004C3653  8b c8                    mov      ecx, eax
004C3655  8b 47 04                 mov      eax, dword ptr [edi + 4]
004C3658  99                       cdq      
004C3659  81 e2 ff 00 00 00        and      edx, 0xff
004C365F  03 c2                    add      eax, edx
004C3661  c1 f9 08                 sar      ecx, 8
004C3664  c1 f8 08                 sar      eax, 8
004C3667  66 3b 4c 24 10           cmp      cx, word ptr [esp + 0x10]
004C366C  75 07                    jne      0x4c3675
004C366E  66 3b 44 24 12           cmp      ax, word ptr [esp + 0x12]
004C3673  74 3a                    je       0x4c36af
004C3675  8b 16                    mov      edx, dword ptr [esi]
004C3677  6a 00                    push     0
004C3679  6a 02                    push     2
004C367B  8b ce                    mov      ecx, esi
004C367D  ff 92 d0 01 00 00        call     dword ptr [edx + 0x1d0]
004C3683  8b 3e                    mov      edi, dword ptr [esi]
004C3685  8d 44 24 10              lea      eax, [esp + 0x10]
004C3689  6a 01                    push     1
004C368B  50                       push     eax
004C368C  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3691  e8 da 49 08 00           call     0x548070
004C3696  50                       push     eax
004C3697  8b ce                    mov      ecx, esi
004C3699  ff 97 10 04 00 00        call     dword ptr [edi + 0x410]
004C369F  8b 4c 24 10              mov      ecx, dword ptr [esp + 0x10]
004C36A3  6a 00                    push     0
004C36A5  6a 00                    push     0
004C36A7  51                       push     ecx
004C36A8  8b ce                    mov      ecx, esi
004C36AA  e8 51 f9 ff ff           call     0x4c3000
004C36AF  8b b6 b0 05 00 00        mov      esi, dword ptr [esi + 0x5b0]
004C36B5  85 f6                    test     esi, esi
004C36B7  0f 85 3f ff ff ff        jne      0x4c35fc
004C36BD  8b 7c 24 14              mov      edi, dword ptr [esp + 0x14]
004C36C1  85 ff                    test     edi, edi
004C36C3  5f                       pop      edi
004C36C4  74 26                    je       0x4c36ec
004C36C6  8b 55 00                 mov      edx, dword ptr [ebp]
004C36C9  8d 44 24 28              lea      eax, [esp + 0x28]
004C36CD  50                       push     eax
004C36CE  8b cd                    mov      ecx, ebp
004C36D0  ff 92 a0 01 00 00        call     dword ptr [edx + 0x1a0]
004C36D6  8b 08                    mov      ecx, dword ptr [eax]
004C36D8  5e                       pop      esi
004C36D9  89 8d 50 04 00 00        mov      dword ptr [ebp + 0x450], ecx
004C36DF  5d                       pop      ebp
004C36E0  b0 01                    mov      al, 1
004C36E2  5b                       pop      ebx
004C36E3  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C36E9  c2 0c 00                 ret      0xc
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
004C3720  8d 85 88 00 00 00        lea      eax, [ebp + 0x88]
004C3726  8b d0                    mov      edx, eax
004C3728  8b 02                    mov      eax, dword ptr [edx]
004C372A  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004C372D  8b 52 08                 mov      edx, dword ptr [edx + 8]
004C3730  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004C3734  99                       cdq      
004C3735  81 e2 ff 00 00 00        and      edx, 0xff
004C373B  03 c2                    add      eax, edx
004C373D  8b f0                    mov      esi, eax
004C373F  8b c1                    mov      eax, ecx
004C3741  99                       cdq      
004C3742  0f bf 8c 24 ae 1f 00 00  movsx    ecx, word ptr [esp + 0x1fae]
004C374A  81 e2 ff 00 00 00        and      edx, 0xff
004C3750  03 c2                    add      eax, edx
004C3752  c1 f8 08                 sar      eax, 8
004C3755  0f bf c0                 movsx    eax, ax
004C3758  2b c1                    sub      eax, ecx
004C375A  99                       cdq      
004C375B  8b c8                    mov      ecx, eax
004C375D  33 ca                    xor      ecx, edx
004C375F  c1 fe 08                 sar      esi, 8
004C3762  2b ca                    sub      ecx, edx
004C3764  0f bf 94 24 ac 1f 00 00  movsx    edx, word ptr [esp + 0x1fac]
004C376C  0f bf c6                 movsx    eax, si
004C376F  2b c2                    sub      eax, edx
004C3771  99                       cdq      
004C3772  33 c2                    xor      eax, edx
004C3774  2b c2                    sub      eax, edx
004C3776  3b c1                    cmp      eax, ecx
004C3778  7f 02                    jg       0x4c377c
004C377A  8b c1                    mov      eax, ecx
004C377C  83 f8 01                 cmp      eax, 1
004C377F  7f 2c                    jg       0x4c37ad
004C3781  8a 45 79                 mov      al, byte ptr [ebp + 0x79]
004C3784  84 c0                    test     al, al
004C3786  0f 85 2c 01 00 00        jne      0x4c38b8
004C378C  8d 84 24 ac 1f 00 00     lea      eax, [esp + 0x1fac]
004C3793  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C3798  50                       push     eax
004C3799  e8 d2 48 08 00           call     0x548070
004C379E  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004C37A4  f6 c5 01                 test     ch, 1
004C37A7  0f 84 0b 01 00 00        je       0x4c38b8
004C37AD  8b 85 c4 04 00 00        mov      eax, dword ptr [ebp + 0x4c4]
004C37B3  85 c0                    test     eax, eax
004C37B5  74 56                    je       0x4c380d
004C37B7  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37BD  85 c0                    test     eax, eax
004C37BF  75 0a                    jne      0x4c37cb
004C37C1  68 03 40 00 80           push     0x80004003
004C37C6  e8 75 21 2d 00           call     0x795940
004C37CB  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37D1  50                       push     eax
004C37D2  8b 08                    mov      ecx, dword ptr [eax]
004C37D4  ff 91 b0 00 00 00        call     dword ptr [ecx + 0xb0]
004C37DA  8b 8d c4 04 00 00        mov      ecx, dword ptr [ebp + 0x4c4]
004C37E0  6a 00                    push     0
004C37E2  6a ff                    push     -1
004C37E4  55                       push     ebp
004C37E5  e8 c6 57 1f 00           call     0x6b8fb0
004C37EA  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C37F0  85 c0                    test     eax, eax
004C37F2  75 0a                    jne      0x4c37fe
004C37F4  68 03 40 00 80           push     0x80004003
004C37F9  e8 42 21 2d 00           call     0x795940
004C37FE  8b 85 64 05 00 00        mov      eax, dword ptr [ebp + 0x564]
004C3804  50                       push     eax
004C3805  8b 10                    mov      edx, dword ptr [eax]
004C3807  ff 92 b4 00 00 00        call     dword ptr [edx + 0xb4]
004C380D  8b 45 00                 mov      eax, dword ptr [ebp]
004C3810  6a 01                    push     1
004C3812  6a 00                    push     0
004C3814  8b cd                    mov      ecx, ebp
004C3816  ff 90 10 04 00 00        call     dword ptr [eax + 0x410]
004C381C  8b 55 00                 mov      edx, dword ptr [ebp]
004C381F  6a 00                    push     0
004C3821  8b cd                    mov      ecx, ebp
004C3823  ff 92 70 03 00 00        call     dword ptr [edx + 0x370]
004C3829  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
004C382F  e8 bc 1a 03 00           call     0x4f52f0
004C3834  84 c0                    test     al, al
004C3836  75 71                    jne      0x4c38a9
004C3838  8b 45 00                 mov      eax, dword ptr [ebp]
004C383B  6a 00                    push     0
004C383D  6a 0b                    push     0xb
004C383F  8b cd                    mov      ecx, ebp
004C3841  ff 90 d0 01 00 00        call     dword ptr [eax + 0x1d0]
004C3847  a1 98 d2 a3 00           mov      eax, dword ptr [0xa3d298]
004C384C  85 c0                    test     eax, eax
004C384E  74 68                    je       0x4c38b8
004C3850  8d 4c 24 28              lea      ecx, [esp + 0x28]
004C3854  55                       push     ebp
004C3855  51                       push     ecx
004C3856  8b 8d b4 01 00 00        mov      ecx, dword ptr [ebp + 0x1b4]
004C385C  e8 0f 7a 02 00           call     0x4eb270
004C3861  8b 00                    mov      eax, dword ptr [eax]
004C3863  66 3b 05 00 5f 86 00     cmp      ax, word ptr [0x865f00]
004C386A  89 44 24 14              mov      dword ptr [esp + 0x14], eax
004C386E  75 0e                    jne      0x4c387e
004C3870  66 8b 54 24 16           mov      dx, word ptr [esp + 0x16]
004C3875  66 3b 15 02 5f 86 00     cmp      dx, word ptr [0x865f02]
004C387C  74 3a                    je       0x4c38b8
004C387E  8b 75 00                 mov      esi, dword ptr [ebp]
004C3881  8d 44 24 14              lea      eax, [esp + 0x14]
004C3885  6a 01                    push     1
004C3887  50                       push     eax
004C3888  b9 e0 24 83 00           mov      ecx, 0x8324e0
004C388D  e8 de 47 08 00           call     0x548070
004C3892  50                       push     eax
004C3893  8b cd                    mov      ecx, ebp
004C3895  ff 96 10 04 00 00        call     dword ptr [esi + 0x410]
004C389B  5e                       pop      esi
004C389C  5d                       pop      ebp
004C389D  32 c0                    xor      al, al
004C389F  5b                       pop      ebx
004C38A0  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C38A6  c2 0c 00                 ret      0xc
004C38A9  8b 55 00                 mov      edx, dword ptr [ebp]
004C38AC  6a 00                    push     0
004C38AE  6a 05                    push     5
004C38B0  8b cd                    mov      ecx, ebp
004C38B2  ff 92 d0 01 00 00        call     dword ptr [edx + 0x1d0]
004C38B8  5e                       pop      esi
004C38B9  5d                       pop      ebp
004C38BA  32 c0                    xor      al, al
004C38BC  5b                       pop      ebx
004C38BD  81 c4 9c 1f 00 00        add      esp, 0x1f9c
004C38C3  c2 0c 00                 ret      0xc
004C38C6  90                       nop      
