
sub_004A3600 0x004A36ED size=731
004A36ED  83 f9 06                 cmp      ecx, 6
004A36F0  0f 85 45 02 00 00        jne      0x4a393b
004A36F6  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A36F9  8b 01                    mov      eax, dword ptr [ecx]
004A36FB  ff 90 80 00 00 00        call     dword ptr [eax + 0x80]
004A3701  8a 88 a0 0a 00 00        mov      cl, byte ptr [eax + 0xaa0]
004A3707  84 c9                    test     cl, cl
004A3709  0f 85 ef fe ff ff        jne      0x4a35fe
004A370F  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A3713  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3716  84 c0                    test     al, al
004A3718  74 21                    je       0x4a373b
004A371A  89 b1 d0 04 00 00        mov      dword ptr [ecx + 0x4d0], esi
004A3720  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3723  a1 2c 0d a4 00           mov      eax, dword ptr [0xa40d2c]
004A3728  33 c9                    xor      ecx, ecx
004A372A  81 c2 30 05 00 00        add      edx, 0x530
004A3730  89 02                    mov      dword ptr [edx], eax
004A3732  8b 44 24 48              mov      eax, dword ptr [esp + 0x48]
004A3736  e9 c7 0d 00 00           jmp      0x4a4502
004A373B  8b 11                    mov      edx, dword ptr [ecx]
004A373D  8d 44 24 44              lea      eax, [esp + 0x44]
004A3741  50                       push     eax
004A3742  ff 52 48                 call     dword ptr [edx + 0x48]
004A3745  8b 48 08                 mov      ecx, dword ptr [eax + 8]
004A3748  8b 7d 3c                 mov      edi, dword ptr [ebp + 0x3c]
004A374B  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A374E  8b 5d 38                 mov      ebx, dword ptr [ebp + 0x38]
004A3751  8b 00                    mov      eax, dword ptr [eax]
004A3753  2b cf                    sub      ecx, edi
004A3755  2b d3                    sub      edx, ebx
004A3757  51                       push     ecx
004A3758  52                       push     edx
004A3759  8b 55 34                 mov      edx, dword ptr [ebp + 0x34]
004A375C  2b c2                    sub      eax, edx
004A375E  8d 4c 24 58              lea      ecx, [esp + 0x58]
004A3762  50                       push     eax
004A3763  e8 c8 7e f7 ff           call     0x41b630
004A3768  8b 08                    mov      ecx, dword ptr [eax]
004A376A  83 ec 08                 sub      esp, 8
004A376D  89 4c 24 34              mov      dword ptr [esp + 0x34], ecx
004A3771  8b 50 04                 mov      edx, dword ptr [eax + 4]
004A3774  db 44 24 34              fild     dword ptr [esp + 0x34]
004A3778  8b 40 08                 mov      eax, dword ptr [eax + 8]
004A377B  89 54 24 38              mov      dword ptr [esp + 0x38], edx
004A377F  db 44 24 38              fild     dword ptr [esp + 0x38]
004A3783  89 44 24 3c              mov      dword ptr [esp + 0x3c], eax
004A3787  db 44 24 3c              fild     dword ptr [esp + 0x3c]
004A378B  d9 c0                    fld      st(0)
004A378D  d8 c9                    fmul     st(1)
004A378F  d9 c2                    fld      st(2)
004A3791  d8 cb                    fmul     st(3)
004A3793  de c1                    faddp    st(1)
004A3795  d9 c3                    fld      st(3)
004A3797  d8 cc                    fmul     st(4)
004A3799  de c1                    faddp    st(1)
004A379B  dd 1c 24                 fstp     qword ptr [esp]
004A379E  dd d8                    fstp     st(0)
004A37A0  dd d8                    fstp     st(0)
004A37A2  dd d8                    fstp     st(0)
004A37A4  e8 67 6c 01 00           call     0x4ba410
004A37A9  83 c4 08                 add      esp, 8
004A37AC  e8 5f b9 2d 00           call     0x77f110
004A37B1  8b 0d 48 98 83 00        mov      ecx, dword ptr [0x839848]
004A37B7  3b 81 80 13 00 00        cmp      eax, dword ptr [ecx + 0x1380]
004A37BD  0f 8d e7 00 00 00        jge      0x4a38aa
004A37C3  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A37C6  81 c1 88 00 00 00        add      ecx, 0x88
004A37CC  8b d1                    mov      edx, ecx
004A37CE  8b 02                    mov      eax, dword ptr [edx]
004A37D0  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A37D4  8b 42 04                 mov      eax, dword ptr [edx + 4]
004A37D7  89 44 24 48              mov      dword ptr [esp + 0x48], eax
004A37DB  8b 45 3c                 mov      eax, dword ptr [ebp + 0x3c]
004A37DE  8b 52 08                 mov      edx, dword ptr [edx + 8]
004A37E1  2b c2                    sub      eax, edx
004A37E3  99                       cdq      
004A37E4  33 c2                    xor      eax, edx
004A37E6  2b c2                    sub      eax, edx
004A37E8  8b 15 d0 29 85 00        mov      edx, dword ptr [0x8529d0]
004A37EE  03 d2                    add      edx, edx
004A37F0  3b c2                    cmp      eax, edx
004A37F2  0f 8d b2 00 00 00        jge      0x4a38aa
004A37F8  8b 01                    mov      eax, dword ptr [ecx]
004A37FA  89 44 24 2c              mov      dword ptr [esp + 0x2c], eax
004A37FE  8b 51 04                 mov      edx, dword ptr [ecx + 4]
004A3801  89 54 24 30              mov      dword ptr [esp + 0x30], edx
004A3805  8b 41 08                 mov      eax, dword ptr [ecx + 8]
004A3808  8d 4c 24 2c              lea      ecx, [esp + 0x2c]
004A380C  89 44 24 34              mov      dword ptr [esp + 0x34], eax
004A3810  51                       push     ecx
004A3811  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A3816  e8 e5 47 0a 00           call     0x548000
004A381B  83 b8 ec 00 00 00 0a     cmp      dword ptr [eax + 0xec], 0xa
004A3822  0f 84 82 00 00 00        je       0x4a38aa
004A3828  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A382D  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A3830  3b c8                    cmp      ecx, eax
004A3832  75 1a                    jne      0x4a384e
004A3834  8b 55 44                 mov      edx, dword ptr [ebp + 0x44]
004A3837  8b 0d 9c 29 85 00        mov      ecx, dword ptr [0x85299c]
004A383D  3b d1                    cmp      edx, ecx
004A383F  75 0d                    jne      0x4a384e
004A3841  8b 4d 48                 mov      ecx, dword ptr [ebp + 0x48]
004A3844  8b 15 a0 29 85 00        mov      edx, dword ptr [0x8529a0]
004A384A  3b ca                    cmp      ecx, edx
004A384C  74 18                    je       0x4a3866
004A384E  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A3851  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A3857  89 55 44                 mov      dword ptr [ebp + 0x44], edx
004A385A  a1 a0 29 85 00           mov      eax, dword ptr [0x8529a0]
004A385F  89 45 48                 mov      dword ptr [ebp + 0x48], eax
004A3862  c6 45 63 00              mov      byte ptr [ebp + 0x63], 0
004A3866  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A3869  33 ff                    xor      edi, edi
004A386B  39 b9 88 04 00 00        cmp      dword ptr [ecx + 0x488], edi
004A3871  75 10                    jne      0x4a3883
004A3873  8b 11                    mov      edx, dword ptr [ecx]
004A3875  6a 01                    push     1
004A3877  57                       push     edi
004A3878  ff 92 10 04 00 00        call     dword ptr [edx + 0x410]
004A387E  e9 7d fd ff ff           jmp      0x4a3600
004A3883  e8 28 a1 02 00           call     0x4cd9b0
004A3888  8b 4d 0c                 mov      ecx, dword ptr [ebp + 0xc]
004A388B  6a 01                    push     1
004A388D  57                       push     edi
004A388E  8b 01                    mov      eax, dword ptr [ecx]
004A3890  ff 90 14 04 00 00        call     dword ptr [eax + 0x414]
004A3896  84 c0                    test     al, al
004A3898  0f 84 62 fd ff ff        je       0x4a3600
004A389E  5f                       pop      edi
004A389F  5e                       pop      esi
004A38A0  5d                       pop      ebp
004A38A1  b0 01                    mov      al, 1
004A38A3  5b                       pop      ebx
004A38A4  83 c4 4c                 add      esp, 0x4c
004A38A7  c2 0c 00                 ret      0xc
004A38AA  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A38AE  51                       push     ecx
004A38AF  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A38B4  e8 b7 47 0a 00           call     0x548070
004A38B9  8b 88 40 01 00 00        mov      ecx, dword ptr [eax + 0x140]
004A38BF  f6 c5 01                 test     ch, 1
004A38C2  74 49                    je       0x4a390d
004A38C4  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A38C7  81 c2 88 00 00 00        add      edx, 0x88
004A38CD  8b 02                    mov      eax, dword ptr [edx]
004A38CF  89 44 24 44              mov      dword ptr [esp + 0x44], eax
004A38D3  8b 4a 04                 mov      ecx, dword ptr [edx + 4]
004A38D6  89 4c 24 48              mov      dword ptr [esp + 0x48], ecx
004A38DA  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A38DF  8b 7a 08                 mov      edi, dword ptr [edx + 8]
004A38E2  8d 54 24 14              lea      edx, [esp + 0x14]
004A38E6  52                       push     edx
004A38E7  e8 84 47 0a 00           call     0x548070
004A38EC  0f be 88 1b 01 00 00     movsx    ecx, byte ptr [eax + 0x11b]
004A38F3  8b c7                    mov      eax, edi
004A38F5  c6 44 24 68 01           mov      byte ptr [esp + 0x68], 1
004A38FA  99                       cdq      
004A38FB  f7 3d d0 29 85 00        idiv     dword ptr [0x8529d0]
004A3901  2b c1                    sub      eax, ecx
004A3903  99                       cdq      
004A3904  33 c2                    xor      eax, edx
004A3906  2b c2                    sub      eax, edx
004A3908  83 f8 02                 cmp      eax, 2
004A390B  7f 05                    jg       0x4a3912
004A390D  c6 44 24 68 00           mov      byte ptr [esp + 0x68], 0
004A3912  8b 54 24 68              mov      edx, dword ptr [esp + 0x68]
004A3916  8d 44 24 14              lea      eax, [esp + 0x14]
004A391A  52                       push     edx
004A391B  6a 01                    push     1
004A391D  6a 01                    push     1
004A391F  68 98 29 85 00           push     0x852998
004A3924  50                       push     eax
004A3925  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A392A  e8 41 47 0a 00           call     0x548070
004A392F  8b c8                    mov      ecx, eax
004A3931  e8 ea 2f fd ff           call     0x476920
004A3936  e9 c3 fc ff ff           jmp      0x4a35fe
004A393B  83 f9 01                 cmp      ecx, 1
004A393E  0f 85 ba fc ff ff        jne      0x4a35fe
004A3944  8d 4c 24 14              lea      ecx, [esp + 0x14]
004A3948  51                       push     ecx
004A3949  b9 e0 24 83 00           mov      ecx, 0x8324e0
004A394E  e8 1d 47 0a 00           call     0x548070
004A3953  8b c8                    mov      ecx, eax
004A3955  e8 e6 4d fd ff           call     0x478740
004A395A  8a 44 24 64              mov      al, byte ptr [esp + 0x64]
004A395E  84 c0                    test     al, al
004A3960  74 23                    je       0x4a3985
004A3962  8b 55 0c                 mov      edx, dword ptr [ebp + 0xc]
004A3965  8b 44 24 60              mov      eax, dword ptr [esp + 0x60]
004A3969  6a 00                    push     0
004A396B  6a 00                    push     0
004A396D  50                       push     eax
004A396E  8b cd                    mov      ecx, ebp
004A3970  89 b2 d0 04 00 00        mov      dword ptr [edx + 0x4d0], esi
004A3976  e8 f5 ec ff ff           call     0x4a2670
004A397B  5f                       pop      edi
004A397C  5e                       pop      esi
004A397D  5d                       pop      ebp
004A397E  5b                       pop      ebx
004A397F  83 c4 4c                 add      esp, 0x4c
004A3982  c2 0c 00                 ret      0xc
004A3985  a1 98 29 85 00           mov      eax, dword ptr [0x852998]
004A398A  8b 4d 40                 mov      ecx, dword ptr [ebp + 0x40]
004A398D  3b c8                    cmp      ecx, eax
004A398F  75 1e                    jne      0x4a39af
004A3991  8b 4d 44                 mov      ecx, dword ptr [ebp + 0x44]
004A3994  8b 15 9c 29 85 00        mov      edx, dword ptr [0x85299c]
004A399A  3b ca                    cmp      ecx, edx
004A399C  75 11                    jne      0x4a39af
004A399E  8b 55 48                 mov      edx, dword ptr [ebp + 0x48]
004A39A1  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A39A7  3b d1                    cmp      edx, ecx
004A39A9  0f 84 7f f8 ff ff        je       0x4a322e
004A39AF  89 45 40                 mov      dword ptr [ebp + 0x40], eax
004A39B2  a1 9c 29 85 00           mov      eax, dword ptr [0x85299c]
004A39B7  89 45 44                 mov      dword ptr [ebp + 0x44], eax
004A39BA  8b 0d a0 29 85 00        mov      ecx, dword ptr [0x8529a0]
004A39C0  89 4d 48                 mov      dword ptr [ebp + 0x48], ecx
004A39C3  e9 62 f8 ff ff           jmp      0x4a322a
