void sub_0055A660(void) {
    int _fpu_cmp = 0;
    uint32_t _cf = 0;
    int _df = 1;
    uint32_t _flag_k = FK_NONE;
    uint32_t _flag_a = 0, _flag_b = 0;
    uint32_t _itail_tgt = 0;
    RECOMP_REGS_LOCALS
    RECOMP_ENTER(0x0055A660u);

L_0055A660:
    SET_LO8(eax, MEM8(esp + 0x8)); /* 0x0055A660: mov al, byte ptr [esp + 8] */
    PUSH32(esp, ebx); /* 0x0055A664: push ebx */
    ebx = MEM32(esp + 0x8); /* 0x0055A665: mov ebx, dword ptr [esp + 8] */
    PUSH32(esp, ebp); /* 0x0055A669: push ebp */
    PUSH32(esp, esi); /* 0x0055A66A: push esi */
    _flag_a = (uint32_t)(0); _flag_b = (uint32_t)(0);
    esi = 0; /* 0x0055A66B: xor esi, esi */
    _cf = 0;
    _flag_k = FK_TEST;
    edx = (int32_t)(int16_t)MEM16(ebx + 0x2); /* 0x0055A66D: movsx edx, word ptr [ebx + 2] */
    PUSH32(esp, edi); /* 0x0055A671: push edi */
    edi = (int32_t)(int16_t)MEM16(ebx); /* 0x0055A672: movsx edi, word ptr [ebx] */
    /* test LO8(eax), LO8(eax) */ /* 0x0055A675: test al, al */
    _flag_a = (uint32_t)(LO8(eax)) << 24; _flag_b = (uint32_t)(LO8(eax)) << 24;
    _cf = 0;
    _flag_k = FK_NARROW(FK_TEST, 24);
    if (TEST_Z(_flag_a, _flag_b)) goto L_0055A6CD; /* 0x0055A677: je 0x55a6cd */
L_0055A679:
    eax = edx; /* 0x0055A679: mov eax, edx */
    if (9u) _cf = (((eax) >> 23) & 1u); /* 0x0055A67B: shl eax, 9 */
    if (9u) { _flag_a = recomp_flags_pack((eax << 9u), _cf, 0, 0); _flag_b = 0; _flag_k = FK_EFLAGS; }
    eax = eax << 9u; /* 0x0055A67B: shl eax, 9 */
    _flag_a = (uint32_t)(eax); _flag_b = (uint32_t)(edi);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    eax = eax + edi; /* 0x0055A67E: add eax, edi */
    _flag_k = FK_ADD;
    if (/* add result */ recomp_cond(_flag_k, _flag_a, _flag_b, CC_S)) goto L_0055A696; /* 0x0055A680: js 0x55a696 */
L_0055A682:
    /* cmp eax, 0x00040000u */ /* 0x0055A682: cmp eax, 0x40000 */
    _flag_a = (uint32_t)(eax); _flag_b = (uint32_t)(0x00040000u);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_GE(_flag_a, _flag_b)) goto L_0055A696; /* 0x0055A687: jge 0x55a696 */
L_0055A689:
    esi = MEM32(0x832618); /* 0x0055A689: mov esi, dword ptr [0x832618] */
    eax = MEM32(esi + eax * 4); /* 0x0055A68F: mov eax, dword ptr [esi + eax*4] */
    /* test eax, eax */ /* 0x0055A692: test eax, eax */
    _flag_a = (uint32_t)(eax); _flag_b = (uint32_t)(eax);
    _cf = 0;
    _flag_k = FK_TEST;
    if (TEST_NZ(_flag_a, _flag_b)) goto L_0055A6A2; /* 0x0055A694: jne 0x55a6a2 */
L_0055A696:
    eax = MEM32(ebx); /* 0x0055A696: mov eax, dword ptr [ebx] */
    MEM32(0xA6FA1C) = eax; /* 0x0055A698: mov dword ptr [0xa6fa1c], eax */
    eax = 0x00A6F9F8u; /* 0x0055A69D: mov eax, 0xa6f9f8 */
L_0055A6A2:
    SET_LO8(ebx, MEM8(eax + 0x11C)); /* 0x0055A6A2: mov bl, byte ptr [eax + 0x11c] */
    esi = (int32_t)(int8_t)MEM8(eax + 0x11B); /* 0x0055A6A8: movsx esi, byte ptr [eax + 0x11b] */
    /* test LO8(ebx), LO8(ebx) */ /* 0x0055A6AF: test bl, bl */
    _flag_a = (uint32_t)(LO8(ebx)) << 24; _flag_b = (uint32_t)(LO8(ebx)) << 24;
    _cf = 0;
    _flag_k = FK_NARROW(FK_TEST, 24);
    if (TEST_Z(_flag_a, _flag_b)) goto L_0055A6CD; /* 0x0055A6B1: je 0x55a6cd */
L_0055A6B3:
    eax = MEM32(ecx + 0xFC); /* 0x0055A6B3: mov eax, dword ptr [ecx + 0xfc] */
    ebx = MEM32(ecx + 0xF0); /* 0x0055A6B9: mov ebx, dword ptr [ecx + 0xf0] */
    eax = ebx + eax * 2 + 0x4; /* 0x0055A6BF: lea eax, [ebx + eax*2 + 4] */
    ebx = edx + edi; /* 0x0055A6C3: lea ebx, [edx + edi] */
    _flag_a = (uint32_t)(eax); _flag_b = (uint32_t)(esi);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    eax = eax + esi; /* 0x0055A6C6: add eax, esi */
    _flag_k = FK_ADD;
    /* cmp ebx, eax */ /* 0x0055A6C8: cmp ebx, eax */
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(eax);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_GE(_flag_a, _flag_b)) goto L_0055A6CD; /* 0x0055A6CA: jge 0x55a6cd */
L_0055A6CC:
    _flag_a = (uint32_t)(esi); _flag_b = (uint32_t)(1);
    esi = esi + 1; /* 0x0055A6CC: inc esi */
    _flag_k = FK_INC;
L_0055A6CD:
    ebx = MEM32(ecx + 0xFC); /* 0x0055A6CD: mov ebx, dword ptr [ecx + 0xfc] */
    eax = MEM32(ecx + 0xF0); /* 0x0055A6D3: mov eax, dword ptr [ecx + 0xf0] */
    ebp = edx + edi; /* 0x0055A6D9: lea ebp, [edx + edi] */
    ebx = eax + ebx * 2; /* 0x0055A6DC: lea ebx, [eax + ebx*2] */
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(esi);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    ebx = ebx + esi; /* 0x0055A6DF: add ebx, esi */
    _flag_k = FK_ADD;
    /* cmp ebp, ebx */ /* 0x0055A6E1: cmp ebp, ebx */
    _flag_a = (uint32_t)(ebp); _flag_b = (uint32_t)(ebx);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_LE(_flag_a, _flag_b)) goto L_0055A72E; /* 0x0055A6E3: jle 0x55a72e */
L_0055A6E5:
    ebx = MEM32(ecx + 0x104); /* 0x0055A6E5: mov ebx, dword ptr [ecx + 0x104] */
    ebp = MEM32(ecx + 0xFC); /* 0x0055A6EB: mov ebp, dword ptr [ecx + 0xfc] */
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(ebp);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    ebx = ebx + ebp; /* 0x0055A6F1: add ebx, ebp */
    _flag_k = FK_ADD;
    ebx = eax + ebx * 2 + 0x2; /* 0x0055A6F3: lea ebx, [eax + ebx*2 + 2] */
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(esi);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    ebx = ebx + esi; /* 0x0055A6F7: add ebx, esi */
    _flag_k = FK_ADD;
    esi = edx + edi; /* 0x0055A6F9: lea esi, [edx + edi] */
    /* cmp esi, ebx */ /* 0x0055A6FC: cmp esi, ebx */
    _flag_a = (uint32_t)(esi); _flag_b = (uint32_t)(ebx);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_G(_flag_a, _flag_b)) goto L_0055A72E; /* 0x0055A6FE: jg 0x55a72e */
L_0055A700:
    esi = MEM32(ecx + 0xF8); /* 0x0055A700: mov esi, dword ptr [ecx + 0xf8] */
    ecx = MEM32(ecx + 0x100); /* 0x0055A706: mov ecx, dword ptr [ecx + 0x100] */
    _flag_a = (uint32_t)(ecx); _flag_b = (uint32_t)(esi);
    _cf = (uint32_t)((uint32_t)(_flag_a + _flag_b) < (uint32_t)_flag_a);
    ecx = ecx + esi; /* 0x0055A70C: add ecx, esi */
    _flag_k = FK_ADD;
    ebx = edi; /* 0x0055A70E: mov ebx, edi */
    if (1u) _cf = (((ecx) >> 31) & 1u); /* 0x0055A710: shl ecx, 1 */
    if (1u) { _flag_a = recomp_flags_pack((ecx << 1u), _cf, 0, 0); _flag_b = 0; _flag_k = FK_EFLAGS; }
    ecx = ecx << 1u; /* 0x0055A710: shl ecx, 1 */
    _flag_a = (uint32_t)(ecx); _flag_b = (uint32_t)(eax);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    ecx = ecx - eax; /* 0x0055A712: sub ecx, eax */
    _flag_k = FK_CMP;
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(edx);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    ebx = ebx - edx; /* 0x0055A714: sub ebx, edx */
    _flag_k = FK_CMP;
    /* cmp ebx, ecx */ /* 0x0055A716: cmp ebx, ecx */
    _flag_a = (uint32_t)(ebx); _flag_b = (uint32_t)(ecx);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_GE(_flag_a, _flag_b)) goto L_0055A72E; /* 0x0055A718: jge 0x55a72e */
L_0055A71A:
    ecx = esi + esi; /* 0x0055A71A: lea ecx, [esi + esi] */
    _flag_a = (uint32_t)(edx); _flag_b = (uint32_t)(edi);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    edx = edx - edi; /* 0x0055A71D: sub edx, edi */
    _flag_k = FK_CMP;
    _flag_a = (uint32_t)(eax); _flag_b = (uint32_t)(ecx);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    eax = eax - ecx; /* 0x0055A71F: sub eax, ecx */
    _flag_k = FK_CMP;
    /* cmp edx, eax */ /* 0x0055A721: cmp edx, eax */
    _flag_a = (uint32_t)(edx); _flag_b = (uint32_t)(eax);
    _cf = (uint32_t)CMP_B(_flag_a, _flag_b);
    _flag_k = FK_CMP;
    if (CMP_GE(_flag_a, _flag_b)) goto L_0055A72E; /* 0x0055A723: jge 0x55a72e */
L_0055A725:
    edi = POP32_VAL(esp); /* 0x0055A725: pop edi */
    esi = POP32_VAL(esp); /* 0x0055A726: pop esi */
    ebp = POP32_VAL(esp); /* 0x0055A727: pop ebp */
    SET_LO8(eax, 1); /* 0x0055A728: mov al, 1 */
    ebx = POP32_VAL(esp); /* 0x0055A72A: pop ebx */
    RECOMP_FLAGS_OUT(); esp += 12; { RECOMP_REGS_OUT(); return; } /* 0x0055A72B: ret 8 */
L_0055A72E:
    edi = POP32_VAL(esp); /* 0x0055A72E: pop edi */
    esi = POP32_VAL(esp); /* 0x0055A72F: pop esi */
    ebp = POP32_VAL(esp); /* 0x0055A730: pop ebp */
    _flag_a = (uint32_t)(0) << 24; _flag_b = (uint32_t)(0) << 24;
    SET_LO8(eax, 0); /* 0x0055A731: xor al, al */
    _cf = 0;
    _flag_k = FK_NARROW(FK_TEST, 24);
    ebx = POP32_VAL(esp); /* 0x0055A733: pop ebx */
    RECOMP_FLAGS_OUT(); esp += 12; { RECOMP_REGS_OUT(); return; } /* 0x0055A734: ret 8 */
    RECOMP_REGS_OUT();
}
