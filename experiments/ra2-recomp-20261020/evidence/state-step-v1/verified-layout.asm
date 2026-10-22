
; 真实模拟帧递增 0x00540676
00540676  8b 15 2c 0d a4 00         mov       edx, dword ptr [0xa40d2c]
0054067C  a1 74 91 ab 00            mov       eax, dword ptr [0xab9174]
00540681  42                        inc       edx
00540682  3b c7                     cmp       eax, edi
00540684  89 15 2c 0d a4 00         mov       dword ptr [0xa40d2c], edx
0054068A  74 11                     je        0x54069d
0054068C  8b ca                     mov       ecx, edx
0054068E  3b c1                     cmp       eax, ecx
00540690  7d 0b                     jge       0x54069d
00540692  e8 89 bd 11 00            call      0x65c420
00540697  89 3d 74 91 ab 00         mov       dword ptr [0xab9174], edi
0054069D  e8 be 02 00 00            call      0x540960

; 对象逻辑更新边界 0x0053D890
0053D890  83 ec 28                  sub       esp, 0x28
0053D893  8b 15 18 eb a6 00         mov       edx, dword ptr [0xa6eb18]
0053D899  89 4c 24 00               mov       dword ptr [esp], ecx
0053D89D  8b 0d 70 61 86 00         mov       ecx, dword ptr [0x866170]
0053D8A3  53                        push      ebx
0053D8A4  55                        push      ebp
0053D8A5  56                        push      esi
0053D8A6  42                        inc       edx
0053D8A7  33 c0                     xor       eax, eax
0053D8A9  83 cb ff                  or        ebx, 0xffffffff
0053D8AC  57                        push      edi
0053D8AD  8b 3d 90 d2 a3 00         mov       edi, dword ptr [0xa3d290]
0053D8B3  89 15 18 eb a6 00         mov       dword ptr [0xa6eb18], edx
0053D8B9  85 c9                     test      ecx, ecx
0053D8BB  a3 44 5d a3 00            mov       dword ptr [0xa35d44], eax
0053D8C0  0f 8e 97 01 00 00         jle       0x53da5d
0053D8C6  8b 0d 64 61 86 00         mov       ecx, dword ptr [0x866164]
0053D8CC  8b 34 81                  mov       esi, dword ptr [ecx + eax*4]
0053D8CF  8a 87 3c 22 00 00         mov       al, byte ptr [edi + 0x223c]
0053D8D5  84 c0                     test      al, al
0053D8D7  74 24                     je        0x53d8fd
0053D8D9  8b 15 b8 ea a6 00         mov       edx, dword ptr [0xa6eab8]
0053D8DF  6a 00                     push      0
0053D8E1  6a 00                     push      0
0053D8E3  52                        push      edx
0053D8E4  6a 00                     push      0
0053D8E6  6a 32                     push      0x32
0053D8E8  8b ce                     mov       ecx, esi
0053D8EA  e8 01 65 17 00            call      0x6b3df0
0053D8EF  84 c0                     test      al, al
0053D8F1  0f 85 47 01 00 00         jne       0x53da3e
0053D8F7  8b 3d 90 d2 a3 00         mov       edi, dword ptr [0xa3d290]
0053D8FD  8a 87 2e 22 00 00         mov       al, byte ptr [edi + 0x222e]
0053D903  84 c0                     test      al, al
0053D905  74 7c                     je        0x53d983
0053D907  a1 b8 ea a6 00            mov       eax, dword ptr [0xa6eab8]
0053D90C  6a 00                     push      0
0053D90E  6a 00                     push      0
0053D910  50                        push      eax
0053D911  6a 00                     push      0
0053D913  6a 1b                     push      0x1b
0053D915  8b ce                     mov       ecx, esi
0053D917  e8 d4 64 17 00            call      0x6b3df0
0053D91C  84 c0                     test      al, al

; 对象编号赋值 0x0040FFD0
0040FFD0  8b 0d 90 d2 a3 00         mov       ecx, dword ptr [0xa3d290]
0040FFD6  85 c9                     test      ecx, ecx
0040FFD8  75 0c                     jne       0x40ffe6
0040FFDA  8b 4c 24 04               mov       ecx, dword ptr [esp + 4]
0040FFDE  33 c0                     xor       eax, eax
0040FFE0  89 41 0c                  mov       dword ptr [ecx + 0xc], eax
0040FFE3  c2 04 00                  ret       4
0040FFE6  e8 85 31 25 00            call      0x663170
0040FFEB  8b 54 24 04               mov       edx, dword ptr [esp + 4]
0040FFEF  89 42 0c                  mov       dword ptr [edx + 0xc], eax
0040FFF2  c2 04 00                  ret       4

; 场景编号递增 0x00663170
00663170  8b 81 14 02 00 00         mov       eax, dword ptr [ecx + 0x214]
00663176  40                        inc       eax
00663177  89 81 14 02 00 00         mov       dword ptr [ecx + 0x214], eax
0066317D  c3                        ret       

; Techno 全局列表 0x006C11E1
006C11E1  a1 28 0c a4 00            mov       eax, dword ptr [0xa40c28]
006C11E6  8b 0d 30 0c a4 00         mov       ecx, dword ptr [0xa40c30]
006C11EC  3b c8                     cmp       ecx, eax
006C11EE  7c 2c                     jl        0x6c121c
006C11F0  38 1d 2d 0c a4 00         cmp       byte ptr [0xa40c2d], bl
006C11F6  75 04                     jne       0x6c11fc
006C11F8  3b c3                     cmp       eax, ebx
006C11FA  75 38                     jne       0x6c1234
006C11FC  8b 0d 34 0c a4 00         mov       ecx, dword ptr [0xa40c34]
006C1202  3b cb                     cmp       ecx, ebx
006C1204  7e 2e                     jle       0x6c1234
006C1206  8b 15 20 0c a4 00         mov       edx, dword ptr [0xa40c20]
006C120C  03 c1                     add       eax, ecx
006C120E  53                        push      ebx
006C120F  50                        push      eax
006C1210  b9 20 0c a4 00            mov       ecx, 0xa40c20
006C1215  ff 52 08                  call      dword ptr [edx + 8]
006C1218  84 c0                     test      al, al
006C121A  74 18                     je        0x6c1234
006C121C  8b 0d 30 0c a4 00         mov       ecx, dword ptr [0xa40c30]
006C1222  8b c1                     mov       eax, ecx
006C1224  41                        inc       ecx
006C1225  89 0d 30 0c a4 00         mov       dword ptr [0xa40c30], ecx
006C122B  8b 0d 24 0c a4 00         mov       ecx, dword ptr [0xa40c24]
006C1231  89 34 81                  mov       dword ptr [ecx + eax*4], esi

; 模拟 RNG 构造 0x00638790
00638790  83 ec 14                  sub       esp, 0x14
00638793  33 c0                     xor       eax, eax
00638795  53                        push      ebx
00638796  89 4c 24 0c               mov       dword ptr [esp + 0xc], ecx
0063879A  89 41 04                  mov       dword ptr [ecx + 4], eax
0063879D  c7 41 08 67 00 00 00      mov       dword ptr [ecx + 8], 0x67
006387A4  55                        push      ebp
006387A5  83 c1 0c                  add       ecx, 0xc
006387A8  56                        push      esi
006387A9  57                        push      edi
006387AA  89 4c 24 10               mov       dword ptr [esp + 0x10], ecx
006387AE  c7 44 24 14 fa 00 00 00   mov       dword ptr [esp + 0x14], 0xfa
006387B6  eb 04                     jmp       0x6387bc
006387B8  8b 44 24 20               mov       eax, dword ptr [esp + 0x20]
006387BC  8b 6c 24 28               mov       ebp, dword ptr [esp + 0x28]
006387C0  8b f0                     mov       esi, eax
006387C2  40                        inc       eax
006387C3  33 db                     xor       ebx, ebx
006387C5  89 44 24 20               mov       dword ptr [esp + 0x20], eax
006387C9  8b 93 ac e4 7e 00         mov       edx, dword ptr [ebx + 0x7ee4ac]
006387CF  8b c6                     mov       eax, esi
006387D1  33 d6                     xor       edx, esi
006387D3  83 c3 04                  add       ebx, 4
006387D6  8b f2                     mov       esi, edx
006387D8  c1 fa 10                  sar       edx, 0x10
006387DB  81 e6 ff ff 00 00         and       esi, 0xffff
006387E1  8b fa                     mov       edi, edx
006387E3  0f af d7                  imul      edx, edi
006387E6  0f af fe                  imul      edi, esi
006387E9  8b ce                     mov       ecx, esi
006387EB  0f af ce                  imul      ecx, esi
006387EE  f7 d2                     not       edx
006387F0  03 d1                     add       edx, ecx
006387F2  8b ca                     mov       ecx, edx
006387F4  c1 f9 10                  sar       ecx, 0x10
006387F7  c1 e2 10                  shl       edx, 0x10
006387FA  0b ca                     or        ecx, edx
006387FC  8b 93 f8 e4 7e 00         mov       edx, dword ptr [ebx + 0x7ee4f8]
00638802  33 ca                     xor       ecx, edx
00638804  03 cf                     add       ecx, edi
00638806  33 cd                     xor       ecx, ebp
00638808  83 fb 10                  cmp       ebx, 0x10
0063880B  8b f1                     mov       esi, ecx
0063880D  8b e8                     mov       ebp, eax
0063880F  7c b8                     jl        0x6387c9
00638811  8b 44 24 10               mov       eax, dword ptr [esp + 0x10]
00638815  89 30                     mov       dword ptr [eax], esi
00638817  83 c0 04                  add       eax, 4
0063881A  89 44 24 10               mov       dword ptr [esp + 0x10], eax
0063881E  8b 44 24 14               mov       eax, dword ptr [esp + 0x14]
00638822  48                        dec       eax
00638823  89 44 24 14               mov       dword ptr [esp + 0x14], eax
00638827  75 8f                     jne       0x6387b8
00638829  8b 44 24 18               mov       eax, dword ptr [esp + 0x18]
0063882D  5f                        pop       edi
0063882E  5e                        pop       esi
0063882F  5d                        pop       ebp
00638830  c6 00 00                  mov       byte ptr [eax], 0
00638833  5b                        pop       ebx
00638834  83 c4 14                  add       esp, 0x14

; 模拟 RNG 推进 0x00638840
00638840  80 39 00                  cmp       byte ptr [ecx], 0
00638843  74 03                     je        0x638848
00638845  33 c0                     xor       eax, eax
00638847  c3                        ret       
00638848  8b 41 04                  mov       eax, dword ptr [ecx + 4]
0063884B  8b 51 08                  mov       edx, dword ptr [ecx + 8]
0063884E  56                        push      esi
0063884F  8b 54 91 0c               mov       edx, dword ptr [ecx + edx*4 + 0xc]
00638853  8b 74 81 0c               mov       esi, dword ptr [ecx + eax*4 + 0xc]
00638857  8d 44 81 0c               lea       eax, [ecx + eax*4 + 0xc]
0063885B  33 f2                     xor       esi, edx
0063885D  89 30                     mov       dword ptr [eax], esi
0063885F  8b 51 04                  mov       edx, dword ptr [ecx + 4]
00638862  8b 71 08                  mov       esi, dword ptr [ecx + 8]
00638865  8b 44 91 0c               mov       eax, dword ptr [ecx + edx*4 + 0xc]
00638869  42                        inc       edx
0063886A  46                        inc       esi
0063886B  81 fa fa 00 00 00         cmp       edx, 0xfa
00638871  89 51 04                  mov       dword ptr [ecx + 4], edx
00638874  89 71 08                  mov       dword ptr [ecx + 8], esi
00638877  7c 07                     jl        0x638880
00638879  c7 41 04 00 00 00 00      mov       dword ptr [ecx + 4], 0
00638880  81 fe fa 00 00 00         cmp       esi, 0xfa
00638886  5e                        pop       esi
00638887  7c 07                     jl        0x638890
00638889  c7 41 08 00 00 00 00      mov       dword ptr [ecx + 8], 0
00638890  c3                        ret       

; 方向字段与填充范围 0x004B89D0
004B89D0  8b c1                     mov       eax, ecx
004B89D2  33 c9                     xor       ecx, ecx
004B89D4  66 89 08                  mov       word ptr [eax], cx
004B89D7  66 89 48 04               mov       word ptr [eax + 4], cx
004B89DB  8b 15 2c 0d a4 00         mov       edx, dword ptr [0xa40d2c]
004B89E1  89 48 10                  mov       dword ptr [eax + 0x10], ecx
004B89E4  89 50 08                  mov       dword ptr [eax + 8], edx
004B89E7  66 89 48 14               mov       word ptr [eax + 0x14], cx
004B89EB  c3                        ret       
004B89EC  90                        nop       
004B89ED  90                        nop       
004B89EE  90                        nop       
004B89EF  90                        nop       
004B89F0  8b c1                     mov       eax, ecx
004B89F2  33 c9                     xor       ecx, ecx
004B89F4  66 89 08                  mov       word ptr [eax], cx
004B89F7  66 89 48 04               mov       word ptr [eax + 4], cx
004B89FB  8b 15 2c 0d a4 00         mov       edx, dword ptr [0xa40d2c]
004B8A01  89 48 10                  mov       dword ptr [eax + 0x10], ecx
004B8A04  89 50 08                  mov       dword ptr [eax + 8], edx
004B8A07  66 89 48 14               mov       word ptr [eax + 0x14], cx
004B8A0B  8b 4c 24 04               mov       ecx, dword ptr [esp + 4]
004B8A0F  83 f9 7f                  cmp       ecx, 0x7f
004B8A12  7c 05                     jl        0x4b8a19
004B8A14  b9 7f 00 00 00            mov       ecx, 0x7f
004B8A19  33 d2                     xor       edx, edx
004B8A1B  8a f1                     mov       dh, cl
004B8A1D  66 89 50 14               mov       word ptr [eax + 0x14], dx
004B8A21  c2 04 00                  ret       4

; MEGAMISSION 构造 0x004B6170
004B6170  8b c1                     mov       eax, ecx
004B6172  8b 4c 24 04               mov       ecx, dword ptr [esp + 4]
004B6176  85 c9                     test      ecx, ecx
004B6178  7c 60                     jl        0x4b61da
004B617A  8b 54 24 08               mov       edx, dword ptr [esp + 8]
004B617E  88 48 02                  mov       byte ptr [eax + 2], cl
004B6181  8d 48 07                  lea       ecx, [eax + 7]
004B6184  c6 00 04                  mov       byte ptr [eax], 4
004B6187  c6 40 1d 00               mov       byte ptr [eax + 0x1d], 0
004B618B  89 11                     mov       dword ptr [ecx], edx
004B618D  8a 54 24 0c               mov       dl, byte ptr [esp + 0xc]
004B6191  88 51 04                  mov       byte ptr [ecx + 4], dl
004B6194  8a 4c 24 10               mov       cl, byte ptr [esp + 0x10]
004B6198  88 48 0c                  mov       byte ptr [eax + 0xc], cl
004B619B  8b 4c 24 14               mov       ecx, dword ptr [esp + 0x14]
004B619F  8d 50 0e                  lea       edx, [eax + 0xe]
004B61A2  89 48 0e                  mov       dword ptr [eax + 0xe], ecx
004B61A5  8a 4c 24 18               mov       cl, byte ptr [esp + 0x18]
004B61A9  88 4a 04                  mov       byte ptr [edx + 4], cl
004B61AC  8b 4c 24 1c               mov       ecx, dword ptr [esp + 0x1c]
004B61B0  8d 50 13                  lea       edx, [eax + 0x13]
004B61B3  89 48 13                  mov       dword ptr [eax + 0x13], ecx
004B61B6  8a 4c 24 20               mov       cl, byte ptr [esp + 0x20]
004B61BA  88 4a 04                  mov       byte ptr [edx + 4], cl
004B61BD  8b 4c 24 24               mov       ecx, dword ptr [esp + 0x24]
004B61C1  8d 50 18                  lea       edx, [eax + 0x18]
004B61C4  89 48 18                  mov       dword ptr [eax + 0x18], ecx
004B61C7  8a 4c 24 28               mov       cl, byte ptr [esp + 0x28]
004B61CB  88 4a 04                  mov       byte ptr [edx + 4], cl
004B61CE  8b 15 2c 0d a4 00         mov       edx, dword ptr [0xa40d2c]
004B61D4  89 50 03                  mov       dword ptr [eax + 3], edx
004B61D7  c2 28 00                  ret       0x28
004B61DA  c6 40 02 ff               mov       byte ptr [eax + 2], 0xff
004B61DE  c6 00 00                  mov       byte ptr [eax], 0
004B61E1  8b 0d 2c 0d a4 00         mov       ecx, dword ptr [0xa40d2c]
004B61E7  89 48 03                  mov       dword ptr [eax + 3], ecx
004B61EA  c2 28 00                  ret       0x28

; 对象和地图格稳定目标编码 0x006B54A0
006B54A0  56                        push      esi
006B54A1  57                        push      edi
006B54A2  8b 7c 24 0c               mov       edi, dword ptr [esp + 0xc]
006B54A6  8b f1                     mov       esi, ecx
006B54A8  85 ff                     test      edi, edi
006B54AA  74 49                     je        0x6b54f5
006B54AC  8b 07                     mov       eax, dword ptr [edi]
006B54AE  8b cf                     mov       ecx, edi
006B54B0  ff 50 2c                  call      dword ptr [eax + 0x2c]
006B54B3  83 f8 0b                  cmp       eax, 0xb
006B54B6  75 27                     jne       0x6b54df
006B54B8  88 46 04                  mov       byte ptr [esi + 4], al
006B54BB  8b 7f 24                  mov       edi, dword ptr [edi + 0x24]
006B54BE  89 7c 24 0c               mov       dword ptr [esp + 0xc], edi
006B54C2  0f bf 44 24 0e            movsx     eax, word ptr [esp + 0xe]
006B54C7  0f bf d7                  movsx     edx, di
006B54CA  8d 04 80                  lea       eax, [eax + eax*4]
006B54CD  5f                        pop       edi
006B54CE  8d 04 80                  lea       eax, [eax + eax*4]
006B54D1  8d 0c 80                  lea       ecx, [eax + eax*4]
006B54D4  8d 04 ca                  lea       eax, [edx + ecx*8]
006B54D7  89 06                     mov       dword ptr [esi], eax
006B54D9  8b c6                     mov       eax, esi
006B54DB  5e                        pop       esi
006B54DC  c2 04 00                  ret       4
006B54DF  8d 47 04                  lea       eax, [edi + 4]
006B54E2  c6 46 04 34               mov       byte ptr [esi + 4], 0x34
006B54E6  50                        push      eax
006B54E7  8b 08                     mov       ecx, dword ptr [eax]
006B54E9  ff 51 10                  call      dword ptr [ecx + 0x10]
006B54EC  89 06                     mov       dword ptr [esi], eax
006B54EE  8b c6                     mov       eax, esi
006B54F0  5f                        pop       edi
006B54F1  5e                        pop       esi
006B54F2  c2 04 00                  ret       4
006B54F5  c6 46 04 00               mov       byte ptr [esi + 4], 0
006B54F9  c7 06 00 00 00 00         mov       dword ptr [esi], 0
006B54FF  8b c6                     mov       eax, esi
006B5501  5f                        pop       edi
006B5502  5e                        pop       esi
006B5503  c2 04 00                  ret       4

; MEGAMISSION 执行与生命字段 0x004B6AB8
004B6AB8  8d 4e 07                  lea       ecx, [esi + 7]
004B6ABB  e8 50 ee 1f 00            call      0x6b5910
004B6AC0  8b f8                     mov       edi, eax
004B6AC2  8a 46 1d                  mov       al, byte ptr [esi + 0x1d]
004B6AC5  3c 01                     cmp       al, 1
004B6AC7  75 12                     jne       0x4b6adb
004B6AC9  8b ce                     mov       ecx, esi
004B6ACB  e8 d0 e0 15 00            call      0x614ba0
004B6AD0  5f                        pop       edi
004B6AD1  5e                        pop       esi
004B6AD2  5d                        pop       ebp
004B6AD3  5b                        pop       ebx
004B6AD4  81 c4 70 03 00 00         add       esp, 0x370
004B6ADA  c3                        ret       
004B6ADB  8b d6                     mov       edx, esi
004B6ADD  8b cf                     mov       ecx, edi
004B6ADF  e8 9c e9 15 00            call      0x615480
004B6AE4  85 ff                     test      edi, edi
004B6AE6  0f 84 4b 0e 00 00         je        0x4b7937
004B6AEC  8a 47 7d                  mov       al, byte ptr [edi + 0x7d]
004B6AEF  84 c0                     test      al, al
004B6AF1  0f 84 40 0e 00 00         je        0x4b7937
004B6AF7  8b 47 6c                  mov       eax, dword ptr [edi + 0x6c]
004B6AFA  85 c0                     test      eax, eax
004B6AFC  0f 8e 35 0e 00 00         jle       0x4b7937
004B6B02  8a 47 76                  mov       al, byte ptr [edi + 0x76]
004B6B05  84 c0                     test      al, al
004B6B07  0f 85 2a 0e 00 00         jne       0x4b7937
004B6B0D  8a 46 12                  mov       al, byte ptr [esi + 0x12]
004B6B10  33 db                     xor       ebx, ebx
004B6B12  84 c0                     test      al, al
004B6B14  74 2f                     je        0x4b6b45
004B6B16  8d 4e 0e                  lea       ecx, [esi + 0xe]
004B6B19  e8 c2 ee 1f 00            call      0x6b59e0
004B6B1E  8b d8                     mov       ebx, eax
004B6B20  85 db                     test      ebx, ebx
004B6B22  74 21                     je        0x4b6b45
004B6B24  8a 43 7d                  mov       al, byte ptr [ebx + 0x7d]
004B6B27  84 c0                     test      al, al
004B6B29  0f 84 08 0e 00 00         je        0x4b7937
004B6B2F  8b 43 6c                  mov       eax, dword ptr [ebx + 0x6c]
004B6B32  85 c0                     test      eax, eax
004B6B34  0f 84 fd 0d 00 00         je        0x4b7937
004B6B3A  8a 43 76                  mov       al, byte ptr [ebx + 0x76]
004B6B3D  84 c0                     test      al, al
004B6B3F  0f 85 f2 0d 00 00         jne       0x4b7937
004B6B45  8a 46 17                  mov       al, byte ptr [esi + 0x17]
004B6B48  84 c0                     test      al, al
004B6B4A  74 2f                     je        0x4b6b7b
004B6B4C  8d 4e 13                  lea       ecx, [esi + 0x13]
004B6B4F  e8 8c ee 1f 00            call      0x6b59e0
004B6B54  8b d8                     mov       ebx, eax
004B6B56  85 db                     test      ebx, ebx
004B6B58  74 21                     je        0x4b6b7b
004B6B5A  8a 43 7d                  mov       al, byte ptr [ebx + 0x7d]
004B6B5D  84 c0                     test      al, al
004B6B5F  0f 84 d2 0d 00 00         je        0x4b7937
004B6B65  8b 43 6c                  mov       eax, dword ptr [ebx + 0x6c]
004B6B68  85 c0                     test      eax, eax
004B6B6A  0f 84 c7 0d 00 00         je        0x4b7937
004B6B70  8a 43 76                  mov       al, byte ptr [ebx + 0x76]
004B6B73  84 c0                     test      al, al
004B6B75  0f 85 bc 0d 00 00         jne       0x4b7937
004B6B7B  80 7e 0c 07               cmp       byte ptr [esi + 0xc], 7
004B6B7F  75 43                     jne       0x4b6bc4
004B6B81  83 bf 98 00 00 00 07      cmp       dword ptr [edi + 0x98], 7
004B6B88  75 3a                     jne       0x4b6bc4
004B6B8A  8a 47 14                  mov       al, byte ptr [edi + 0x14]
004B6B8D  c0 e8 02                  shr       al, 2
004B6B90  24 01                     and       al, 1
004B6B92  88 44 24 13               mov       byte ptr [esp + 0x13], al
004B6B96  74 2c                     je        0x4b6bc4
004B6B98  8d 4e 13                  lea       ecx, [esi + 0x13]
004B6B9B  e8 70 ec 1f 00            call      0x6b5810
004B6BA0  8b e8                     mov       ebp, eax
004B6BA2  85 ed                     test      ebp, ebp
004B6BA4  74 1e                     je        0x4b6bc4
004B6BA6  8b 55 00                  mov       edx, dword ptr [ebp]
004B6BA9  8b cd                     mov       ecx, ebp
004B6BAB  ff 52 2c                  call      dword ptr [edx + 0x2c]
004B6BAE  83 f8 06                  cmp       eax, 6
004B6BB1  75 11                     jne       0x4b6bc4
004B6BB3  6a 00                     push      0
004B6BB5  8b cf                     mov       ecx, edi
004B6BB7  e8 54 02 18 00            call      0x636e10
004B6BBC  3b c5                     cmp       eax, ebp
004B6BBE  0f 84 73 0d 00 00         je        0x4b7937
004B6BC4  8a 87 70 03 00 00         mov       al, byte ptr [edi + 0x370]
004B6BCA  84 c0                     test      al, al
004B6BCC  75 0e                     jne       0x4b6bdc
004B6BCE  8b 07                     mov       eax, dword ptr [edi]
004B6BD0  6a 03                     push      3
004B6BD2  8b cf                     mov       ecx, edi
004B6BD4  ff 90 54 02 00 00         call      dword ptr [eax + 0x254]
004B6BDA  eb 46                     jmp       0x4b6c22
004B6BDC  6a 00                     push      0
004B6BDE  8b cf                     mov       ecx, edi
004B6BE0  e8 2b 02 18 00            call      0x636e10
004B6BE5  8b e8                     mov       ebp, eax
004B6BE7  85 ed                     test      ebp, ebp
004B6BE9  74 37                     je        0x4b6c22
004B6BEB  8a 45 7d                  mov       al, byte ptr [ebp + 0x7d]
004B6BEE  84 c0                     test      al, al
004B6BF0  74 30                     je        0x4b6c22
004B6BF2  8b 55 00                  mov       edx, dword ptr [ebp]
004B6BF5  8b cd                     mov       ecx, ebp
004B6BF7  ff 52 2c                  call      dword ptr [edx + 0x2c]
004B6BFA  83 f8 06                  cmp       eax, 6
004B6BFD  75 23                     jne       0x4b6c22
004B6BFF  8b 85 18 04 00 00         mov       eax, dword ptr [ebp + 0x418]
004B6C05  8a 88 4d 13 00 00         mov       cl, byte ptr [eax + 0x134d]
004B6C0B  84 c9                     test      cl, cl
004B6C0D  74 13                     je        0x4b6c22
004B6C0F  8b 17                     mov       edx, dword ptr [edi]
004B6C11  6a 03                     push      3
004B6C13  8b cf                     mov       ecx, edi
004B6C15  ff 92 54 02 00 00         call      dword ptr [edx + 0x254]

; 原版事件入队片段 0x004C61A0
004C61A0  8b 44 24 04               mov       eax, dword ptr [esp + 4]
004C61A4  81 ec f8 00 00 00         sub       esp, 0xf8
004C61AA  48                        dec       eax
004C61AB  53                        push      ebx
004C61AC  55                        push      ebp
004C61AD  56                        push      esi
004C61AE  83 f8 3f                  cmp       eax, 0x3f
004C61B1  57                        push      edi
004C61B2  8b f1                     mov       esi, ecx
004C61B4  0f 87 ac 07 00 00         ja        0x4c6966
004C61BA  33 c9                     xor       ecx, ecx
004C61BC  8a 88 ac 69 4c 00         mov       cl, byte ptr [eax + 0x4c69ac]
004C61C2  ff 24 8d 78 69 4c 00      jmp       dword ptr [ecx*4 + 0x4c6978]
004C61C9  8b 16                     mov       edx, dword ptr [esi]
004C61CB  8b ce                     mov       ecx, esi
004C61CD  ff 92 98 00 00 00         call      dword ptr [edx + 0x98]
004C61D3  84 c0                     test      al, al
004C61D5  0f 84 9f 02 00 00         je        0x4c647a
004C61DB  8b 06                     mov       eax, dword ptr [esi]
004C61DD  8b ce                     mov       ecx, esi
004C61DF  ff 90 9c 00 00 00         call      dword ptr [eax + 0x9c]
004C61E5  84 c0                     test      al, al
004C61E7  0f 84 8d 02 00 00         je        0x4c647a
004C61ED  8b 16                     mov       edx, dword ptr [esi]
004C61EF  8b ce                     mov       ecx, esi
004C61F1  ff 52 2c                  call      dword ptr [edx + 0x2c]
004C61F4  8b bc 24 10 01 00 00      mov       edi, dword ptr [esp + 0x110]
004C61FB  83 f8 0f                  cmp       eax, 0xf
004C61FE  75 10                     jne       0x4c6210
004C6200  8b 86 a8 05 00 00         mov       eax, dword ptr [esi + 0x5a8]
004C6206  8a 88 10 0c 00 00         mov       cl, byte ptr [eax + 0xc10]
004C620C  84 c9                     test      cl, cl
004C620E  75 0d                     jne       0x4c621d
004C6210  6a 0e                     push      0xe
004C6212  8b ce                     mov       ecx, esi
004C6214  e8 f7 16 21 00            call      0x6d7910
004C6219  84 c0                     test      al, al
004C621B  74 3c                     je        0x4c6259
004C621D  8b 17                     mov       edx, dword ptr [edi]
004C621F  8b cf                     mov       ecx, edi
004C6221  ff 52 2c                  call      dword ptr [edx + 0x2c]
004C6224  83 f8 06                  cmp       eax, 6
004C6227  75 30                     jne       0x4c6259
004C6229  8b 8e b4 01 00 00         mov       ecx, dword ptr [esi + 0x1b4]
004C622F  57                        push      edi
004C6230  e8 4b f3 01 00            call      0x4e5580
004C6235  84 c0                     test      al, al
004C6237  75 20                     jne       0x4c6259
004C6239  8b 06                     mov       eax, dword ptr [esi]
004C623B  6a 00                     push      0
004C623D  57                        push      edi
004C623E  6a 00                     push      0
004C6240  6a 11                     push      0x11
004C6242  8b ce                     mov       ecx, esi
004C6244  ff 90 20 03 00 00         call      dword ptr [eax + 0x320]
004C624A  b0 01                     mov       al, 1
004C624C  5f                        pop       edi
004C624D  5e                        pop       esi
004C624E  5d                        pop       ebp
004C624F  5b                        pop       ebx
004C6250  81 c4 f8 00 00 00         add       esp, 0xf8
004C6256  c2 0c 00                  ret       0xc
004C6259  8b 16                     mov       edx, dword ptr [esi]
004C625B  6a 00                     push      0
004C625D  6a 00                     push      0
004C625F  57                        push      edi
004C6260  6a 0b                     push      0xb
004C6262  e9 f7 06 00 00            jmp       0x4c695e
004C6267  8b 06                     mov       eax, dword ptr [esi]
004C6269  6a 00                     push      0
004C626B  6a 00                     push      0
004C626D  6a 00                     push      0
004C626F  6a 10                     push      0x10
004C6271  8b ce                     mov       ecx, esi
004C6273  ff 90 20 03 00 00         call      dword ptr [eax + 0x320]
004C6279  b0 01                     mov       al, 1
004C627B  5f                        pop       edi
004C627C  5e                        pop       esi
004C627D  5d                        pop       ebp
004C627E  5b                        pop       ebx
004C627F  81 c4 f8 00 00 00         add       esp, 0xf8
004C6285  c2 0c 00                  ret       0xc
004C6288  56                        push      esi
004C6289  8d 4c 24 58               lea       ecx, [esp + 0x58]
004C628D  e8 0e f2 1e 00            call      0x6b54a0
004C6292  8b 10                     mov       edx, dword ptr [eax]
004C6294  83 ec 08                  sub       esp, 8
004C6297  8b cc                     mov       ecx, esp
004C6299  8a 40 04                  mov       al, byte ptr [eax + 4]
004C629C  6a 0a                     push      0xa
004C629E  89 11                     mov       dword ptr [ecx], edx
004C62A0  88 41 04                  mov       byte ptr [ecx + 4], al
004C62A3  8b 4e 38                  mov       ecx, dword ptr [esi + 0x38]
004C62A6  8b 51 28                  mov       edx, dword ptr [ecx + 0x28]
004C62A9  8d 8c 24 a4 00 00 00      lea       ecx, [esp + 0xa4]
004C62B0  8b 42 30                  mov       eax, dword ptr [edx + 0x30]
004C62B3  50                        push      eax
004C62B4  e8 37 fc fe ff            call      0x4b5ef0
004C62B9  81 3d 38 23 a3 00 80 00 00 00 cmp       dword ptr [0xa32338], 0x80
004C62C3  0f 8d 9d 06 00 00         jge       0x4c6966
004C62C9  8b 0d 40 23 a3 00         mov       ecx, dword ptr [0xa32340]
004C62CF  8b f0                     mov       esi, eax
004C62D1  8d 14 c9                  lea       edx, [ecx + ecx*8]
004C62D4  8d 0c 91                  lea       ecx, [ecx + edx*4]
004C62D7  8d bc 49 44 23 a3 00      lea       edi, [ecx + ecx*2 + 0xa32344]
004C62DE  b9 1b 00 00 00            mov       ecx, 0x1b
004C62E3  f3 a5                     rep movsd dword ptr es:[edi], dword ptr [esi]
004C62E5  66 a5                     movsw     word ptr es:[edi], word ptr [esi]
004C62E7  a4                        movsb     byte ptr es:[edi], byte ptr [esi]
004C62E8  ff 15 24 a5 79 00         call      dword ptr [0x79a524]
004C62EE  8b 0d 40 23 a3 00         mov       ecx, dword ptr [0xa32340]
004C62F4  89 04 8d c4 5a a3 00      mov       dword ptr [ecx*4 + 0xa35ac4], eax
004C62FB  8b 15 40 23 a3 00         mov       edx, dword ptr [0xa32340]
004C6301  a1 38 23 a3 00            mov       eax, dword ptr [0xa32338]
004C6306  42                        inc       edx
004C6307  83 e2 7f                  and       edx, 0x7f
004C630A  40                        inc       eax

; 发生差异的整数乘系数和单精度存储 0x004A23F0
004A23F0  db 45 4c                  fild      dword ptr [ebp + 0x4c]
004A23F3  51                        push      ecx
004A23F4  8d 8c 24 c8 00 00 00      lea       ecx, [esp + 0xc8]
004A23FB  8d 94 24 bc 00 00 00      lea       edx, [esp + 0xbc]
004A2402  8b f0                     mov       esi, eax
004A2404  dc 0d c0 05 7a 00         fmul      qword ptr [0x7a05c0]
004A240A  89 bc 24 bc 00 00 00      mov       dword ptr [esp + 0xbc], edi
004A2411  89 bc 24 c0 00 00 00      mov       dword ptr [esp + 0xc0], edi
004A2418  89 bc 24 c4 00 00 00      mov       dword ptr [esp + 0xc4], edi
004A241F  d9 1c 24                  fstp      dword ptr [esp]
004A2422  51                        push      ecx
004A2423  8d 4c 24 64               lea       ecx, [esp + 0x64]
004A2427  e8 94 fc 27 00            call      0x7220c0

; 三维向量插值 0x007220C0
007220C0  83 ec 0c                  sub       esp, 0xc
007220C3  d9 44 24 14               fld       dword ptr [esp + 0x14]
007220C7  dc 2d 08 a7 79 00         fsubr     qword ptr [0x79a708]
007220CD  53                        push      ebx
007220CE  8b 5c 24 14               mov       ebx, dword ptr [esp + 0x14]
007220D2  55                        push      ebp
007220D3  56                        push      esi
007220D4  db 03                     fild      dword ptr [ebx]
007220D6  8b f2                     mov       esi, edx
007220D8  57                        push      edi
007220D9  8b f9                     mov       edi, ecx
007220DB  d8 4c 24 24               fmul      dword ptr [esp + 0x24]
007220DF  db 06                     fild      dword ptr [esi]
007220E1  d8 ca                     fmul      st(2)
007220E3  de c1                     faddp     st(1)
007220E5  e8 26 d0 05 00            call      0x77f110
007220EA  db 43 04                  fild      dword ptr [ebx + 4]
007220ED  8b e8                     mov       ebp, eax
007220EF  d8 4c 24 24               fmul      dword ptr [esp + 0x24]
007220F3  db 46 04                  fild      dword ptr [esi + 4]
007220F6  d8 ca                     fmul      st(2)
007220F8  de c1                     faddp     st(1)
007220FA  e8 11 d0 05 00            call      0x77f110
007220FF  db 43 08                  fild      dword ptr [ebx + 8]
00722102  89 44 24 14               mov       dword ptr [esp + 0x14], eax
00722106  d8 4c 24 24               fmul      dword ptr [esp + 0x24]
0072210A  db 46 08                  fild      dword ptr [esi + 8]
0072210D  d8 ca                     fmul      st(2)
0072210F  de c1                     faddp     st(1)
00722111  e8 fa cf 05 00            call      0x77f110
00722116  8b 54 24 14               mov       edx, dword ptr [esp + 0x14]
0072211A  8b cf                     mov       ecx, edi
0072211C  dd d8                     fstp      st(0)
0072211E  89 29                     mov       dword ptr [ecx], ebp
00722120  89 51 04                  mov       dword ptr [ecx + 4], edx
00722123  89 41 08                  mov       dword ptr [ecx + 8], eax
00722126  8b c7                     mov       eax, edi
00722128  5f                        pop       edi
00722129  5e                        pop       esi
0072212A  5d                        pop       ebp
0072212B  5b                        pop       ebx
0072212C  83 c4 0c                  add       esp, 0xc
0072212F  c2 08 00                  ret       8

; 后续差异可继续调查的移动速度入口 0x004C9B10
004C9B10  83 ec 0c                  sub       esp, 0xc
004C9B13  56                        push      esi
004C9B14  8b f1                     mov       esi, ecx
004C9B16  57                        push      edi
004C9B17  8b 06                     mov       eax, dword ptr [esi]
004C9B19  ff 90 80 00 00 00         call      dword ptr [eax + 0x80]
004C9B1F  8b 8e b4 01 00 00         mov       ecx, dword ptr [esi + 0x1b4]
004C9B25  50                        push      eax
004C9B26  e8 f5 be 02 00            call      0x4f5a20
004C9B2B  8b 16                     mov       edx, dword ptr [esi]
004C9B2D  8b ce                     mov       ecx, esi
004C9B2F  dd 5c 24 0c               fstp      qword ptr [esp + 0xc]
004C9B33  ff 92 38 03 00 00         call      dword ptr [edx + 0x338]
004C9B39  89 44 24 08               mov       dword ptr [esp + 8], eax
004C9B3D  db 44 24 08               fild      dword ptr [esp + 8]
004C9B41  dc 4c 24 0c               fmul      qword ptr [esp + 0xc]
004C9B45  dc 8e 70 04 00 00         fmul      qword ptr [esi + 0x470]
004C9B4B  e8 c0 55 2b 00            call      0x77f110
004C9B50  6a 00                     push      0
004C9B52  8b ce                     mov       ecx, esi
004C9B54  89 44 24 0c               mov       dword ptr [esp + 0xc], eax
004C9B58  e8 b3 dd 20 00            call      0x6d7910
004C9B5D  84 c0                     test      al, al
004C9B5F  74 18                     je        0x4c9b79
004C9B61  db 44 24 08               fild      dword ptr [esp + 8]
004C9B65  a1 48 98 83 00            mov       eax, dword ptr [0x839848]
004C9B6A  dc 88 98 05 00 00         fmul      qword ptr [eax + 0x598]
004C9B70  e8 9b 55 2b 00            call      0x77f110
004C9B75  89 44 24 08               mov       dword ptr [esp + 8], eax
004C9B79  db 44 24 08               fild      dword ptr [esp + 8]
004C9B7D  dc 8e 68 04 00 00         fmul      qword ptr [esi + 0x468]
004C9B83  e8 88 55 2b 00            call      0x77f110
004C9B88  8b 16                     mov       edx, dword ptr [esi]
004C9B8A  8b ce                     mov       ecx, esi
004C9B8C  8b f8                     mov       edi, eax
004C9B8E  ff 52 2c                  call      dword ptr [edx + 0x2c]
004C9B91  83 f8 01                  cmp       eax, 1
004C9B94  75 18                     jne       0x4c9bae
004C9B96  8b 86 b4 05 00 00         mov       eax, dword ptr [esi + 0x5b4]
004C9B9C  83 f8 ff                  cmp       eax, -1
004C9B9F  8b c7                     mov       eax, edi
004C9BA1  74 0d                     je        0x4c9bb0
004C9BA3  99                        cdq       
004C9BA4  2b c2                     sub       eax, edx
004C9BA6  5f                        pop       edi
004C9BA7  d1 f8                     sar       eax, 1
004C9BA9  5e                        pop       esi
004C9BAA  83 c4 0c                  add       esp, 0xc
004C9BAD  c3                        ret       
004C9BAE  8b c7                     mov       eax, edi
004C9BB0  5f                        pop       edi
004C9BB1  5e                        pop       esi
004C9BB2  83 c4 0c                  add       esp, 0xc
004C9BB5  c3                        ret       
