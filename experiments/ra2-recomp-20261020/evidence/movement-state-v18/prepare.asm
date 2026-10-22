004A2670: sub esp, 0x4c
004A2673: push ebx
004A2674: push ebp
004A2675: mov ebp, ecx
004A2677: push esi
004A2678: mov ecx, dword ptr [ebp + 4]
004A267B: push edi
004A267C: mov eax, dword ptr [ebp + 0xc]
004A267F: mov ebx, dword ptr [eax + 0x4d0]
004A2685: lea eax, [ebp + 4]
004A2688: push eax
004A2689: mov dword ptr [esp + 0x18], eax
004A268D: call dword ptr [ecx + 0x10]
004A2690: test al, al
004A2692: jne 0x4a2710
004A2694: cmp ebx, -1
004A2697: jne 0x4a2710
004A2699: mov byte ptr [ebp + 0x61], al
004A269C: mov eax, dword ptr [0x852998]
004A26A1: cmp dword ptr [ebp + 0x40], eax
004A26A4: jne 0x4a26c0
004A26A6: mov edx, dword ptr [ebp + 0x44]
004A26A9: mov ecx, dword ptr [0x85299c]
004A26AF: cmp edx, ecx
004A26B1: jne 0x4a26c0
004A26B3: mov ecx, dword ptr [ebp + 0x48]
004A26B6: mov edx, dword ptr [0x8529a0]
004A26BC: cmp ecx, edx
004A26BE: je 0x4a26d8
004A26C0: mov dword ptr [ebp + 0x40], eax
004A26C3: mov edx, dword ptr [0x85299c]
004A26C9: mov dword ptr [ebp + 0x44], edx
004A26CC: mov eax, dword ptr [0x8529a0]
004A26D1: mov dword ptr [ebp + 0x48], eax
004A26D4: mov byte ptr [ebp + 0x63], 0
004A26D8: mov ecx, dword ptr [ebp + 0xc]
004A26DB: mov edx, dword ptr [ecx]
004A26DD: call dword ptr [edx + 0x16c]
004A26E3: cmp eax, 2
004A26E6: jne 0x4a3a44
004A26EC: mov ebp, dword ptr [ebp + 0xc]
004A26EF: push 1
004A26F1: push 0
004A26F3: mov ecx, ebp
004A26F5: mov eax, dword ptr [ebp]
004A26F8: call dword ptr [eax + 0x414]
004A26FE: mov ecx, dword ptr [esp + 0x60]
004A2702: pop edi
004A2703: pop esi
004A2704: pop ebp
004A2705: mov byte ptr [ecx], al
004A2707: xor al, al
004A2709: pop ebx
004A270A: add esp, 0x4c
004A270D: ret 0xc
004A2710: mov edx, dword ptr [ebp + 0x34]
004A2713: mov eax, dword ptr [0x852998]
004A2718: lea edi, [ebp + 0x34]
004A271B: cmp edx, eax
004A271D: jne 0x4a273c
004A271F: mov eax, dword ptr [edi + 4]
004A2722: mov ecx, dword ptr [0x85299c]
004A2728: cmp eax, ecx
004A272A: jne 0x4a273c
004A272C: mov ecx, dword ptr [edi + 8]
004A272F: mov eax, dword ptr [0x8529a0]
004A2734: cmp ecx, eax
004A2736: je 0x4a3a44
004A273C: mov ecx, dword ptr [ebp + 0xc]
004A273F: mov edx, dword ptr [ecx]
004A2741: call dword ptr [edx + 0x1bc]
004A2747: test al, al
004A2749: jne 0x4a3a44
004A274F: mov ecx, dword ptr [ebp + 0xc]
004A2752: mov eax, dword ptr [ecx]
004A2754: call dword ptr [eax + 0x1c0]
004A275A: test al, al
004A275C: jne 0x4a3a44
004A2762: mov ecx, dword ptr [ebp + 0xc]
004A2765: mov ecx, dword ptr [ecx + 0x238]
004A276B: test ecx, ecx
004A276D: je 0x4a2784
004A276F: call 0x68a680
004A2774: test eax, eax
004A2776: je 0x4a2784
004A2778: pop edi
004A2779: pop esi
004A277A: pop ebp
004A277B: mov al, 1
004A277D: pop ebx
004A277E: add esp, 0x4c
004A2781: ret 0xc
004A2784: mov ecx, dword ptr [ebp + 0xc]
004A2787: mov edx, dword ptr [ecx]
004A2789: call dword ptr [edx + 0x324]
004A278F: test al, al
004A2791: jne 0x4a4385
004A2797: mov ecx, dword ptr [ebp + 0xc]
004A279A: mov eax, dword ptr [ecx]
004A279C: call dword ptr [eax + 0x328]
004A27A2: test al, al
004A27A4: jne 0x4a4385
004A27AA: cmp ebx, -1
004A27AD: je 0x4a285e
004A27B3: mov ecx, dword ptr [ebp + 0xc]
004A27B6: mov ecx, dword ptr [ecx + 0x494]
004A27BC: test ecx, ecx
004A27BE: je 0x4a27ca
004A27C0: mov edx, dword ptr [ecx]
004A27C2: call dword ptr [edx + 0x2c]
004A27C5: cmp eax, 1
004A27C8: je 0x4a27e1
004A27CA: mov eax, dword ptr [ebp + 0xc]
004A27CD: mov ecx, dword ptr [eax + 0x494]
004A27D3: test ecx, ecx
004A27D5: je 0x4a2855
004A27D7: mov edx, dword ptr [ecx]
004A27D9: call dword ptr [edx + 0x2c]
004A27DC: cmp eax, 0xf
004A27DF: jne 0x4a2855
004A27E1: mov ecx, dword ptr [ebp + 0xc]
004A27E4: lea edx, [esp + 0x44]
004A27E8: push edx
004A27E9: mov eax, dword ptr [ecx]
004A27EB: call dword ptr [eax + 0x48]
004A27EE: mov ecx, dword ptr [eax + 8]
004A27F1: mov esi, dword ptr [edi + 8]
004A27F4: mov edx, dword ptr [eax + 4]
004A27F7: mov eax, dword ptr [eax]
004A27F9: sub ecx, esi
004A27FB: mov esi, dword ptr [edi + 4]
004A27FE: sub edx, esi
004A2800: mov esi, dword ptr [edi]
004A2802: push ecx
004A2803: sub eax, esi
004A2805: push edx
004A2806: push eax
004A2807: lea ecx, [esp + 0x24]
004A280B: call 0x41b630
004A2810: mov ecx, dword ptr [eax]
004A2812: mov dword ptr [esp + 0x2c], ecx
004A2816: lea ecx, [esp + 0x2c]
004A281A: mov edx, dword ptr [eax + 4]
004A281D: mov dword ptr [esp + 0x30], edx
004A2821: mov eax, dword ptr [eax + 8]
004A2824: mov dword ptr [esp + 0x34], eax
004A2828: call 0x41b780
004A282D: cdq 
004A282E: and edx, 0xff
004A2834: add eax, edx
004A2836: sar eax, 8
004A2839: cmp eax, 0x18
004A283C: jge 0x4a2855
004A283E: mov ecx, dword ptr [ebp + 0xc]
004A2841: mov dword ptr [ecx + eax*4 + 0x4d0], 0xffffffff
004A284C: mov edx, dword ptr [ebp + 0xc]
004A284F: mov ebx, dword ptr [edx + 0x4d0]
004A2855: cmp ebx, -1
004A2858: jne 0x4a32ca
004A285E: mov eax, dword ptr [ebp + 0xc]
004A2861: mov ebx, dword ptr [0xa40d2c]
004A2867: mov edx, dword ptr [eax + 0x530]
004A286D: lea esi, [eax + 0x530]
004A2873: cmp edx, -1
004A2876: mov eax, dword ptr [esi + 8]
004A2879: je 0x4a2885
004A287B: mov ecx, ebx
004A287D: sub ecx, edx
004A287F: cmp ecx, eax
004A2881: jge 0x4a288d
004A2883: sub eax, ecx
004A2885: test eax, eax
004A2887: jne 0x4a3a44
004A288D: mov eax, dword ptr [0x839848]
004A2892: fld qword ptr [eax + 0x13c8]
004A2898: fmul qword ptr [0x79b608]
004A289E: call 0x77f110
004A28A3: mov ecx, dword ptr [esp + 0x48]
004A28A7: mov dword ptr [esi], ebx
004A28A9: mov dword ptr [esi + 4], ecx
004A28AC: mov dword ptr [esi + 8], eax
004A28AF: mov eax, dword ptr [edi]
004A28B1: mov ecx, dword ptr [ebp + 0xc]
004A28B4: cdq 
004A28B5: and edx, 0xff
004A28BB: push 0
004A28BD: add eax, edx
004A28BF: push 0
004A28C1: sar eax, 8
004A28C4: mov word ptr [esp + 0x20], ax
004A28C9: mov eax, dword ptr [edi + 4]
004A28CC: cdq 
004A28CD: and edx, 0xff
004A28D3: add eax, edx
004A28D5: sar eax, 8
004A28D8: mov word ptr [esp + 0x22], ax
004A28DD: mov edx, dword ptr [esp + 0x20]
004A28E1: push edx
004A28E2: call 0x4c3000
004A28E7: mov ecx, dword ptr [ebp + 0xc]
004A28EA: test al, al
004A28EC: jne 0x4a2f7a
004A28F2: test ecx, ecx
004A28F4: jne 0x4a2909
004A28F6: mov eax, dword ptr [esp + 0x60]
004A28FA: pop edi
004A28FB: pop esi
004A28FC: pop ebp
004A28FD: mov byte ptr [eax], 1
004A2900: xor al, al
004A2902: pop ebx
004A2903: add esp, 0x4c
004A2906: ret 0xc
004A2909: mov edx, dword ptr [ecx]
004A290B: push edi
004A290C: call dword ptr [edx + 0x2ac]
004A2912: test al, al
004A2914: jne 0x4a2934
004A2916: mov ebp, dword ptr [ebp + 0xc]
004A2919: push 1
004A291B: push 0
004A291D: mov ecx, ebp
004A291F: mov eax, dword ptr [ebp]
004A2922: call dword ptr [eax + 0x410]
004A2928: pop edi
004A2929: pop esi
004A292A: pop ebp
004A292B: xor al, al
004A292D: pop ebx
004A292E: add esp, 0x4c
004A2931: ret 0xc
004A2934: mov ecx, dword ptr [edi]
004A2936: mov eax, dword ptr [0x852998]
004A293B: cmp ecx, eax
004A293D: jne 0x4a295c
004A293F: mov edx, dword ptr [edi + 4]
004A2942: mov eax, dword ptr [0x85299c]
004A2947: cmp edx, eax
004A2949: jne 0x4a295c
004A294B: mov eax, dword ptr [edi + 8]
004A294E: mov ecx, dword ptr [0x8529a0]
004A2954: cmp eax, ecx
004A2956: je 0x4a3a44
004A295C: mov ecx, dword ptr [ebp + 0xc]
004A295F: call 0x4c8d60
004A2964: test al, al
004A2966: jne 0x4a2a83
004A296C: mov ecx, dword ptr [ebp + 0xc]
004A296F: lea eax, [esp + 0x44]
004A2973: push eax
004A2974: mov edx, dword ptr [ecx]
004A2976: call dword ptr [edx + 0x48]
004A2979: mov ecx, dword ptr [eax + 8]
004A297C: mov edx, dword ptr [edi + 8]
004A297F: mov esi, dword ptr [edi + 4]
004A2982: mov ebx, dword ptr [edi]
004A2984: sub ecx, edx
004A2986: mov edx, dword ptr [eax + 4]
004A2989: mov eax, dword ptr [eax]
004A298B: sub edx, esi
004A298D: push ecx
004A298E: sub eax, ebx
004A2990: push edx
004A2991: push eax
004A2992: lea ecx, [esp + 0x24]
004A2996: call 0x41b630
004A299B: mov ecx, dword ptr [eax]
004A299D: mov dword ptr [esp + 0x2c], ecx
004A29A1: lea ecx, [esp + 0x2c]
004A29A5: mov edx, dword ptr [eax + 4]
004A29A8: mov dword ptr [esp + 0x30], edx
004A29AC: mov eax, dword ptr [eax + 8]
004A29AF: mov dword ptr [esp + 0x34], eax
004A29B3: call 0x41b780
004A29B8: mov ecx, dword ptr [0x839848]
004A29BE: cmp eax, dword ptr [ecx + 0x1380]
004A29C4: jge 0x4a2a83
004A29CA: mov ecx, dword ptr [ebp + 0xc]
004A29CD: mov edx, dword ptr [ecx]
004A29CF: call dword ptr [edx + 0x16c]
004A29D5: cmp eax, 2
004A29D8: je 0x4a29ee
004A29DA: mov ecx, dword ptr [ebp + 0xc]
004A29DD: mov eax, dword ptr [ecx]
004A29DF: call dword ptr [eax + 0x16c]
004A29E5: cmp eax, 0xb
004A29E8: jne 0x4a2a83
004A29EE: mov eax, dword ptr [0x852998]
004A29F3: mov ecx, dword ptr [ebp + 0x40]
004A29F6: cmp ecx, eax
004A29F8: jne 0x4a2a14
004A29FA: mov ecx, dword ptr [ebp + 0x44]
004A29FD: mov edx, dword ptr [0x85299c]
004A2A03: cmp ecx, edx
004A2A05: jne 0x4a2a14
004A2A07: mov edx, dword ptr [ebp + 0x48]
004A2A0A: mov ecx, dword ptr [0x8529a0]
004A2A10: cmp edx, ecx
004A2A12: je 0x4a2a2c
004A2A14: mov dword ptr [ebp + 0x40], eax
004A2A17: mov eax, dword ptr [0x85299c]
004A2A1C: mov dword ptr [ebp + 0x44], eax
004A2A1F: mov ecx, dword ptr [0x8529a0]
004A2A25: mov dword ptr [ebp + 0x48], ecx
004A2A28: mov byte ptr [ebp + 0x63], 0
004A2A2C: mov ecx, dword ptr [ebp + 0xc]
004A2A2F: mov eax, dword ptr [ecx + 0x488]
004A2A35: test eax, eax
004A2A37: jne 0x4a2a5f
004A2A39: mov edx, dword ptr [ecx]
004A2A3B: push 1
004A2A3D: push 0
004A2A3F: call dword ptr [edx + 0x410]
004A2A45: mov ecx, dword ptr [ebp + 0xc]
004A2A48: mov al, byte ptr [ecx + 0x7d]
004A2A4B: test al, al
004A2A4D: jne 0x4a2eac
004A2A53: pop edi
004A2A54: pop esi
004A2A55: pop ebp
004A2A56: xor al, al
004A2A58: pop ebx
004A2A59: add esp, 0x4c
004A2A5C: ret 0xc
004A2A5F: call 0x4cd9b0
004A2A64: mov ecx, dword ptr [ebp + 0xc]
004A2A67: push 1
004A2A69: push 0
004A2A6B: mov eax, dword ptr [ecx]
004A2A6D: call dword ptr [eax + 0x414]
004A2A73: test al, al
004A2A75: je 0x4a2a45
004A2A77: pop edi
004A2A78: pop esi
004A2A79: pop ebp
004A2A7A: mov al, 1
004A2A7C: pop ebx
004A2A7D: add esp, 0x4c
004A2A80: ret 0xc
004A2A83: mov ecx, dword ptr [ebp + 0xc]
004A2A86: lea edx, [esp + 0x64]
004A2A8A: push edx
004A2A8B: add ecx, 0x2e0
004A2A91: call 0x4b8be0
004A2A96: mov ecx, dword ptr [ebp + 0xc]
004A2A99: mov edi, eax
004A2A9B: lea edx, [esp + 0x44]
004A2A9F: mov eax, dword ptr [ecx]
004A2AA1: push edx
004A2AA2: call dword ptr [eax + 0x48]
004A2AA5: mov esi, eax
004A2AA7: push 1
004A2AA9: mov eax, dword ptr [esi]
004A2AAB: cdq 
004A2AAC: and edx, 0xff
004A2AB2: add eax, edx
004A2AB4: mov ecx, eax
004A2AB6: mov eax, dword ptr [esi + 4]
004A2AB9: cdq 
004A2ABA: and edx, 0xff
004A2AC0: add eax, edx
004A2AC2: mov edx, dword ptr [edi]
004A2AC4: shr edx, 0xc
004A2AC7: sar ecx, 8
004A2ACA: sar eax, 8
004A2ACD: inc edx
004A2ACE: shr edx, 1
004A2AD0: and edx, 7
004A2AD3: add cx, word ptr [edx*4 + 0x851a70]
004A2ADB: lea edx, [edx*4 + 0x851a70]
004A2AE2: mov word ptr [esp + 0x64], cx
004A2AE7: mov cx, word ptr [edx + 2]
004A2AEB: add cx, ax
004A2AEE: lea eax, [esp + 0x6c]
004A2AF2: mov word ptr [esp + 0x66], cx
004A2AF7: mov edx, dword ptr [esp + 0x64]
004A2AFB: push eax
004A2AFC: mov ecx, 0x8324e0
004A2B01: mov dword ptr [esp + 0x70], edx
004A2B05: call 0x55a660
004A2B0A: test al, al
004A2B0C: je 0x4a2dfd
004A2B12: lea ecx, [esp + 0x60]
004A2B16: push ecx
004A2B17: mov ecx, dword ptr [ebp + 0xc]
004A2B1A: add ecx, 0x2e0
004A2B20: call 0x4b8be0
004A2B25: mov esi, dword ptr [eax]
004A2B27: mov ecx, dword ptr [ebp + 0xc]
004A2B2A: shr esi, 0xc
004A2B2D: mov edi, dword ptr [ecx]
004A2B2F: inc esi
004A2B30: xor ebx, ebx
004A2B32: push 1
004A2B34: shr esi, 1
004A2B36: push ebx
004A2B37: and esi, 7
004A2B3A: call 0x5d47d0
004A2B3F: push eax
004A2B40: lea edx, [esp + 0x74]
004A2B44: push esi
004A2B45: push edx
004A2B46: mov ecx, 0x8324e0
004A2B4B: call 0x548070
004A2B50: mov ecx, dword ptr [ebp + 0xc]
004A2B53: push eax
004A2B54: call dword ptr [edi + 0x194]
004A2B5A: cmp eax, 3
004A2B5D: jne 0x4a2b7f
004A2B5F: mov edx, dword ptr [ebp + 0xc]
004A2B62: mov eax, dword ptr [esp + 0x68]
004A2B66: lea ecx, [esp + 0x60]
004A2B6A: mov dword ptr [esp + 0x60], eax
004A2B6E: push ecx
004A2B6F: push edx
004A2B70: mov ecx, 0x8324e0
004A2B75: call 0x55acd0
004A2B7A: jmp 0x4a2dfd
004A2B7F: cmp eax, 6
004A2B82: jne 0x4a2dfd
004A2B88: lea eax, [esp + 0x68]
004A2B8C: mov ecx, 0x8324e0
004A2B91: push eax
004A2B92: call 0x548070
004A2B97: mov ecx, dword ptr [ebp + 0xc]
004A2B9A: mov edi, eax
004A2B9C: add ecx, 0x88
004A2BA2: push ebx
004A2BA3: mov edx, dword ptr [ecx]
004A2BA5: mov dword ptr [esp + 0x48], edx
004A2BA9: mov eax, dword ptr [ecx + 4]
004A2BAC: movsx edx, word ptr [esp + 0x6e]
004A2BB1: mov esi, dword ptr [ecx + 8]
004A2BB4: mov dword ptr [esp + 0x4c], eax
004A2BB8: movsx ecx, word ptr [esp + 0x6c]
004A2BBD: shl ecx, 8
004A2BC0: add ecx, 0x80
004A2BC6: lea eax, [esp + 0x1c]
004A2BCA: shl edx, 8
004A2BCD: mov dword ptr [esp + 0x1c], ecx
004A2BD1: add edx, 0x80
004A2BD7: push eax
004A2BD8: mov ecx, 0x8324e0
004A2BDD: mov dword ptr [esp + 0x24], edx
004A2BE1: mov dword ptr [esp + 0x28], ebx
004A2BE5: mov dword ptr [esp + 0x34], ebx
004A2BE9: mov dword ptr [esp + 0x38], ebx
004A2BED: call 0x55a280
004A2BF2: mov ecx, dword ptr [0x8529d0]
004A2BF8: lea edx, [eax + ecx*2]
004A2BFB: lea ecx, [esp + 0x30]
004A2BFF: cmp esi, edx
004A2C01: setg al
004A2C04: push eax
004A2C05: push ecx
004A2C06: mov ecx, edi
004A2C08: call 0x471660
004A2C0D: cmp eax, ebx
004A2C0F: je 0x4a2dfd
004A2C15: mov edx, dword ptr [ebp + 0xc]
004A2C18: push eax
004A2C19: mov ecx, dword ptr [edx + 0x1b4]
004A2C1F: call 0x4e5580
004A2C24: test al, al
004A2C26: je 0x4a2dfd
004A2C2C: mov ecx, dword ptr [ebp + 0xc]
004A2C2F: mov eax, dword ptr [ecx]
004A2C31: call dword ptr [eax + 0x80]
004A2C37: mov cl, byte ptr [eax + 0xaa0]
004A2C3D: test cl, cl
004A2C3F: jne 0x4a2dfd
004A2C45: mov ecx, dword ptr [ebp + 0xc]
004A2C48: lea eax, [esp + 0x44]
004A2C4C: push eax
004A2C4D: mov edx, dword ptr [ecx]
004A2C4F: call dword ptr [edx + 0x48]
004A2C52: mov ecx, dword ptr [eax + 8]
004A2C55: mov esi, dword ptr [ebp + 0x3c]
004A2C58: mov edx, dword ptr [eax + 4]
004A2C5B: mov eax, dword ptr [eax]
004A2C5D: sub ecx, esi
004A2C5F: push ecx
004A2C60: mov ecx, dword ptr [ebp + 0x38]
004A2C63: sub edx, ecx
004A2C65: mov ecx, dword ptr [ebp + 0x34]
004A2C68: sub eax, ecx
004A2C6A: push edx
004A2C6B: push eax
004A2C6C: lea ecx, [esp + 0x24]
004A2C70: call 0x41b630
004A2C75: mov ecx, dword ptr [eax]
004A2C77: mov dword ptr [esp + 0x2c], ecx
004A2C7B: lea ecx, [esp + 0x2c]
004A2C7F: mov edx, dword ptr [eax + 4]
004A2C82: mov dword ptr [esp + 0x30], edx
004A2C86: mov eax, dword ptr [eax + 8]
004A2C89: mov dword ptr [esp + 0x34], eax
004A2C8D: call 0x41b780
004A2C92: mov ecx, dword ptr [0x839848]
004A2C98: cmp eax, dword ptr [ecx + 0x1380]
004A2C9E: jge 0x4a2da0
004A2CA4: mov ecx, dword ptr [ebp + 0xc]
004A2CA7: call 0x636f10
004A2CAC: test al, al
004A2CAE: jne 0x4a2da0
004A2CB4: mov ecx, dword ptr [ebp + 0xc]
004A2CB7: add ecx, 0x88
004A2CBD: mov edx, ecx
004A2CBF: mov eax, dword ptr [edx]
004A2CC1: mov dword ptr [esp + 0x44], eax
004A2CC5: mov eax, dword ptr [edx + 4]
004A2CC8: mov dword ptr [esp + 0x48], eax
004A2CCC: mov eax, dword ptr [ebp + 0x3c]
004A2CCF: mov edx, dword ptr [edx + 8]
004A2CD2: sub eax, edx
004A2CD4: cdq 
004A2CD5: xor eax, edx
004A2CD7: sub eax, edx
004A2CD9: mov edx, dword ptr [0x8529d0]
004A2CDF: add edx, edx
004A2CE1: cmp eax, edx
004A2CE3: jge 0x4a2da0
004A2CE9: mov eax, dword ptr [ecx]
004A2CEB: mov dword ptr [esp + 0x2c], eax
004A2CEF: mov edx, dword ptr [ecx + 4]
004A2CF2: mov dword ptr [esp + 0x30], edx
004A2CF6: mov eax, dword ptr [ecx + 8]
004A2CF9: lea ecx, [esp + 0x2c]
004A2CFD: mov dword ptr [esp + 0x34], eax
004A2D01: push ecx
004A2D02: mov ecx, 0x8324e0
004A2D07: call 0x548000
004A2D0C: cmp dword ptr [eax + 0xec], 0xa
004A2D13: je 0x4a2da0
004A2D19: mov eax, dword ptr [0x852998]
004A2D1E: mov ecx, dword ptr [ebp + 0x40]
004A2D21: cmp ecx, eax
004A2D23: jne 0x4a2d3f
004A2D25: mov edx, dword ptr [ebp + 0x44]
004A2D28: mov ecx, dword ptr [0x85299c]
004A2D2E: cmp edx, ecx
004A2D30: jne 0x4a2d3f
004A2D32: mov ecx, dword ptr [ebp + 0x48]
004A2D35: mov edx, dword ptr [0x8529a0]
004A2D3B: cmp ecx, edx
004A2D3D: je 0x4a2d57
004A2D3F: mov dword ptr [ebp + 0x40], eax
004A2D42: mov edx, dword ptr [0x85299c]
004A2D48: mov dword ptr [ebp + 0x44], edx
004A2D4B: mov eax, dword ptr [0x8529a0]
004A2D50: mov dword ptr [ebp + 0x48], eax
004A2D53: mov byte ptr [ebp + 0x63], 0
004A2D57: mov ecx, dword ptr [ebp + 0xc]
004A2D5A: cmp dword ptr [ecx + 0x488], ebx
004A2D60: jne 0x4a2d79
004A2D62: mov edx, dword ptr [ecx]
004A2D64: push 1
004A2D66: push ebx
004A2D67: call dword ptr [edx + 0x410]
004A2D6D: pop edi
004A2D6E: pop esi
004A2D6F: pop ebp
004A2D70: xor al, al
004A2D72: pop ebx
004A2D73: add esp, 0x4c
004A2D76: ret 0xc
004A2D79: call 0x4cd9b0
004A2D7E: mov ecx, dword ptr [ebp + 0xc]
004A2D81: push 1
004A2D83: push ebx
004A2D84: mov eax, dword ptr [ecx]
004A2D86: call dword ptr [eax + 0x414]
004A2D8C: test al, al
004A2D8E: je 0x4a3a44
004A2D94: pop edi
004A2D95: pop esi
004A2D96: pop ebp
004A2D97: mov al, 1
004A2D99: pop ebx
004A2D9A: add esp, 0x4c
004A2D9D: ret 0xc
004A2DA0: mov eax, dword ptr [edi + 0x140]
004A2DA6: test ah, 1
004A2DA9: je 0x4a2de3
004A2DAB: mov ecx, dword ptr [ebp + 0xc]
004A2DAE: mov byte ptr [esp + 0x60], 1
004A2DB3: add ecx, 0x88
004A2DB9: mov edx, dword ptr [ecx]
004A2DBB: mov dword ptr [esp + 0x44], edx
004A2DBF: mov eax, dword ptr [ecx + 4]
004A2DC2: mov dword ptr [esp + 0x48], eax
004A2DC6: mov eax, dword ptr [ecx + 8]
004A2DC9: cdq 
004A2DCA: idiv dword ptr [0x8529d0]
004A2DD0: movsx ecx, byte ptr [edi + 0x11b]
004A2DD7: sub eax, ecx
004A2DD9: cdq 
004A2DDA: xor eax, edx
004A2DDC: sub eax, edx
004A2DDE: cmp eax, 2
004A2DE1: jg 0x4a2de8
004A2DE3: mov byte ptr [esp + 0x60], 0
004A2DE8: mov edx, dword ptr [esp + 0x60]
004A2DEC: mov ecx, edi
004A2DEE: push edx
004A2DEF: push 1
004A2DF1: push 1
004A2DF3: push 0x852998
004A2DF8: call 0x476920
004A2DFD: mov ecx, dword ptr [ebp + 0xc]
004A2E00: mov eax, dword ptr [ecx + 0x53c]
004A2E06: test eax, eax
004A2E08: jle 0x4a2e16
004A2E0A: dec eax
004A2E0B: mov dword ptr [ecx + 0x53c], eax
004A2E11: jmp 0x4a2eac
004A2E16: mov eax, dword ptr [0x852998]
004A2E1B: mov edx, dword ptr [ebp + 0x40]
004A2E1E: cmp edx, eax
004A2E20: jne 0x4a2e3c
004A2E22: mov edx, dword ptr [ebp + 0x44]
004A2E25: mov esi, dword ptr [0x85299c]
004A2E2B: cmp edx, esi
004A2E2D: jne 0x4a2e3c
004A2E2F: mov edx, dword ptr [ebp + 0x48]
004A2E32: mov esi, dword ptr [0x8529a0]
004A2E38: cmp edx, esi
004A2E3A: je 0x4a2e54
004A2E3C: mov dword ptr [ebp + 0x40], eax
004A2E3F: mov eax, dword ptr [0x85299c]
004A2E44: mov dword ptr [ebp + 0x44], eax
004A2E47: mov edx, dword ptr [0x8529a0]
004A2E4D: mov dword ptr [ebp + 0x48], edx
004A2E50: mov byte ptr [ebp + 0x63], 0
004A2E54: mov eax, dword ptr [ecx + 0x488]
004A2E5A: test eax, eax
004A2E5C: jne 0x4a2f52
004A2E62: mov eax, dword ptr [ecx]
004A2E64: push 1
004A2E66: push 0
004A2E68: call dword ptr [eax + 0x410]
004A2E6E: mov eax, dword ptr [ebp + 0xc]
004A2E71: mov cl, byte ptr [eax + 0x7d]
004A2E74: test cl, cl
004A2E76: je 0x4a3a44
004A2E7C: mov cl, byte ptr [eax + 0x57a]
004A2E82: test cl, cl
004A2E84: je 0x4a2ea2
004A2E86: mov eax, dword ptr [0x839848]
004A2E8B: push 0
004A2E8D: mov edx, 0x2000
004A2E92: push 0x3f800000
004A2E97: mov ecx, dword ptr [eax + 0x620]
004A2E9D: call 0x713db0
004A2EA2: mov ecx, dword ptr [ebp + 0xc]
004A2EA5: mov byte ptr [ecx + 0x57a], 0
004A2EAC: mov eax, dword ptr [esp + 0x14]
004A2EB0: push eax
004A2EB1: mov edx, dword ptr [eax]
004A2EB3: call dword ptr [edx + 0x10]
004A2EB6: test al, al
004A2EB8: jne 0x4a2efd
004A2EBA: mov ecx, dword ptr [ebp + 0xc]
004A2EBD: mov eax, dword ptr [ecx + 0x228]
004A2EC3: test eax, eax
004A2EC5: je 0x4a2efd
004A2EC7: mov edx, dword ptr [ecx]
004A2EC9: push eax
004A2ECA: call dword ptr [edx + 0x354]
004A2ED0: test al, al
004A2ED2: jne 0x4a2efd
004A2ED4: mov eax, dword ptr [ebp + 0xc]
004A2ED7: mov byte ptr [eax + 0x578], 1
004A2EDE: mov ecx, dword ptr [ebp + 0xc]
004A2EE1: mov ecx, dword ptr [ecx + 0x4c4]
004A2EE7: test ecx, ecx
004A2EE9: je 0x4a2ef0
004A2EEB: call 0x6baa30
004A2EF0: mov ecx, dword ptr [ebp + 0xc]
004A2EF3: push 0
004A2EF5: mov edx, dword ptr [ecx]
004A2EF7: call dword ptr [edx + 0x370]
004A2EFD: mov eax, dword ptr [0x852998]
004A2F02: mov ecx, dword ptr [ebp + 0x40]
004A2F05: cmp ecx, eax
004A2F07: jne 0x4a2f23
004A2F09: mov ecx, dword ptr [ebp + 0x44]
004A2F0C: mov edx, dword ptr [0x85299c]
004A2F12: cmp ecx, edx
004A2F14: jne 0x4a2f23
004A2F16: mov edx, dword ptr [ebp + 0x48]
004A2F19: mov ecx, dword ptr [0x8529a0]
004A2F1F: cmp edx, ecx
004A2F21: je 0x4a2f3b
004A2F23: mov dword ptr [ebp + 0x40], eax
004A2F26: mov eax, dword ptr [0x85299c]
004A2F2B: mov dword ptr [ebp + 0x44], eax
004A2F2E: mov ecx, dword ptr [0x8529a0]
004A2F34: mov dword ptr [ebp + 0x48], ecx
004A2F37: mov byte ptr [ebp + 0x63], 0
004A2F3B: pop edi
004A2F3C: mov dword ptr [ebp + 0x58], 0xffffffff
004A2F43: mov byte ptr [ebp + 0x61], 0
004A2F47: pop esi
004A2F48: pop ebp
004A2F49: xor al, al
004A2F4B: pop ebx
004A2F4C: add esp, 0x4c
004A2F4F: ret 0xc
004A2F52: call 0x4cd9b0
004A2F57: mov ecx, dword ptr [ebp + 0xc]
004A2F5A: push 1
004A2F5C: push 0
004A2F5E: mov edx, dword ptr [ecx]
004A2F60: call dword ptr [edx + 0x414]
004A2F66: test al, al
004A2F68: je 0x4a2e6e
004A2F6E: pop edi
004A2F6F: pop esi
004A2F70: pop ebp
004A2F71: mov al, 1
004A2F73: pop ebx
004A2F74: add esp, 0x4c
004A2F77: ret 0xc
004A2F7A: cmp dword ptr [ecx + 0x4d0], 8
004A2F81: je 0x4a3a44
004A2F87: mov edx, dword ptr [ecx]
004A2F89: lea eax, [esp + 0x44]
004A2F8D: push eax
004A2F8E: call dword ptr [edx + 0x48]
004A2F91: mov esi, eax
004A2F93: push 1
004A2F95: mov eax, dword ptr [esi]
004A2F97: cdq 
004A2F98: and edx, 0xff
004A2F9E: add eax, edx
004A2FA0: mov ecx, eax
004A2FA2: mov eax, dword ptr [esi + 4]
004A2FA5: cdq 
004A2FA6: and edx, 0xff
004A2FAC: add eax, edx
004A2FAE: mov edx, dword ptr [ebp + 0xc]
004A2FB1: sar ecx, 8
004A2FB4: mov edx, dword ptr [edx + 0x4d0]
004A2FBA: and edx, 7
004A2FBD: sar eax, 8
004A2FC0: mov si, word ptr [edx*4 + 0x851a70]
004A2FC8: lea edx, [edx*4 + 0x851a70]
004A2FCF: add si, cx
004A2FD2: mov cx, word ptr [edx + 2]
004A2FD6: mov word ptr [esp + 0x1c], si
004A2FDB: add cx, ax
004A2FDE: lea eax, [esp + 0x28]
004A2FE2: mov word ptr [esp + 0x1e], cx
004A2FE7: mov edx, dword ptr [esp + 0x1c]
004A2FEB: push eax
004A2FEC: mov ecx, 0x8324e0
004A2FF1: mov dword ptr [esp + 0x2c], edx
004A2FF5: call 0x55a660
004A2FFA: test al, al
004A2FFC: je 0x4a32b4
004A3002: mov ecx, dword ptr [ebp + 0xc]
004A3005: push 1
004A3007: push 0
004A3009: mov esi, dword ptr [ecx]
004A300B: call 0x5d47d0
004A3010: mov ecx, dword ptr [ebp + 0xc]
004A3013: push eax
004A3014: lea eax, [esp + 0x30]
004A3018: mov edx, dword ptr [ecx + 0x4d0]
004A301E: mov ecx, 0x8324e0
004A3023: push edx
004A3024: push eax
004A3025: call 0x548070
004A302A: mov ecx, dword ptr [ebp + 0xc]
004A302D: push eax
004A302E: call dword ptr [esi + 0x194]
004A3034: cmp eax, 3
004A3037: jne 0x4a3059
004A3039: mov ecx, dword ptr [esp + 0x24]
004A303D: mov eax, dword ptr [ebp + 0xc]
004A3040: lea edx, [esp + 0x28]
004A3044: mov dword ptr [esp + 0x28], ecx
004A3048: push edx
004A3049: push eax
004A304A: mov ecx, 0x8324e0
004A304F: call 0x55acd0
004A3054: jmp 0x4a32b4
004A3059: cmp eax, 6
004A305C: jne 0x4a32b4
004A3062: lea ecx, [esp + 0x24]
004A3066: push ecx
004A3067: mov ecx, 0x8324e0
004A306C: call 0x548070
004A3071: movsx edx, word ptr [esp + 0x24]
004A3076: mov ecx, dword ptr [ebp + 0xc]
004A3079: mov esi, eax
004A307B: movsx eax, word ptr [esp + 0x26]
004A3080: shl edx, 8
004A3083: shl eax, 8
004A3086: add edx, 0x80
004A308C: add eax, 0x80
004A3091: xor ebx, ebx
004A3093: add ecx, 0x88
004A3099: mov dword ptr [esp + 0x18], edx
004A309D: mov dword ptr [esp + 0x1c], eax
004A30A1: mov dword ptr [esp + 0x20], ebx
004A30A5: mov edx, dword ptr [ecx]
004A30A7: push ebx
004A30A8: mov dword ptr [esp + 0x48], edx
004A30AC: mov eax, dword ptr [ecx + 4]
004A30AF: mov dword ptr [esp + 0x4c], eax
004A30B3: mov edi, dword ptr [ecx + 8]
004A30B6: lea ecx, [esp + 0x1c]
004A30BA: push ecx
004A30BB: mov ecx, 0x8324e0
004A30C0: mov dword ptr [esp + 0x34], ebx
004A30C4: mov dword ptr [esp + 0x38], ebx
004A30C8: call 0x55a280
004A30CD: mov edx, dword ptr [0x8529d0]
004A30D3: lea eax, [eax + edx*2]
004A30D6: lea edx, [esp + 0x30]
004A30DA: cmp edi, eax
004A30DC: setg cl
004A30DF: push ecx
004A30E0: push edx
004A30E1: mov ecx, esi
004A30E3: call 0x471660
004A30E8: cmp eax, ebx
004A30EA: je 0x4a32b4
004A30F0: push eax
004A30F1: mov eax, dword ptr [ebp + 0xc]
004A30F4: mov ecx, dword ptr [eax + 0x1b4]
004A30FA: call 0x4e5580
004A30FF: test al, al
004A3101: je 0x4a32b4
004A3107: mov ecx, dword ptr [ebp + 0xc]
004A310A: mov edx, dword ptr [ecx]
004A310C: call dword ptr [edx + 0x80]
004A3112: mov cl, byte ptr [eax + 0xaa0]
004A3118: test cl, cl
004A311A: jne 0x4a32b4
004A3120: mov ecx, dword ptr [ebp + 0xc]
004A3123: lea edx, [esp + 0x44]
004A3127: push edx
004A3128: mov eax, dword ptr [ecx]
004A312A: call dword ptr [eax + 0x48]
004A312D: mov ecx, dword ptr [eax + 8]
004A3130: mov edx, dword ptr [ebp + 0x3c]
004A3133: mov edi, dword ptr [ebp + 0x38]
004A3136: mov ebx, dword ptr [ebp + 0x34]
004A3139: sub ecx, edx
004A313B: mov edx, dword ptr [eax + 4]
004A313E: mov eax, dword ptr [eax]
004A3140: sub edx, edi
004A3142: push ecx
004A3143: sub eax, ebx
004A3145: push edx
004A3146: push eax
004A3147: lea ecx, [esp + 0x24]
004A314B: call 0x41b630
004A3150: mov ecx, dword ptr [eax]
004A3152: mov dword ptr [esp + 0x2c], ecx
004A3156: lea ecx, [esp + 0x2c]
004A315A: mov edx, dword ptr [eax + 4]
004A315D: mov dword ptr [esp + 0x30], edx
004A3161: mov eax, dword ptr [eax + 8]
004A3164: mov dword ptr [esp + 0x34], eax
004A3168: call 0x41b780
004A316D: mov ecx, dword ptr [0x839848]
004A3173: cmp eax, dword ptr [ecx + 0x1380]
004A3179: jge 0x4a3257
004A317F: mov ecx, dword ptr [ebp + 0xc]
004A3182: call 0x636f10
004A3187: test al, al
004A3189: jne 0x4a3257
004A318F: mov ecx, dword ptr [ebp + 0xc]
004A3192: add ecx, 0x88
004A3198: mov edx, ecx
004A319A: mov eax, dword ptr [edx]
004A319C: mov dword ptr [esp + 0x44], eax
004A31A0: mov eax, dword ptr [edx + 4]
004A31A3: mov dword ptr [esp + 0x48], eax
004A31A7: mov eax, dword ptr [ebp + 0x3c]
004A31AA: mov edx, dword ptr [edx + 8]
004A31AD: sub eax, edx
004A31AF: cdq 
004A31B0: xor eax, edx
004A31B2: sub eax, edx
004A31B4: mov edx, dword ptr [0x8529d0]
004A31BA: add edx, edx
004A31BC: cmp eax, edx
004A31BE: jge 0x4a3257
004A31C4: mov eax, dword ptr [ecx]
004A31C6: mov dword ptr [esp + 0x2c], eax
004A31CA: mov edx, dword ptr [ecx + 4]
004A31CD: mov dword ptr [esp + 0x30], edx
004A31D1: mov eax, dword ptr [ecx + 8]
004A31D4: lea ecx, [esp + 0x2c]
004A31D8: mov dword ptr [esp + 0x34], eax
004A31DC: push ecx
004A31DD: mov ecx, 0x8324e0
004A31E2: call 0x548000
004A31E7: cmp dword ptr [eax + 0xec], 0xa
004A31EE: je 0x4a3257
004A31F0: mov eax, dword ptr [0x852998]
004A31F5: mov ecx, dword ptr [ebp + 0x40]
004A31F8: cmp ecx, eax
004A31FA: jne 0x4a3216
004A31FC: mov edx, dword ptr [ebp + 0x44]
004A31FF: mov ecx, dword ptr [0x85299c]
004A3205: cmp edx, ecx
004A3207: jne 0x4a3216
004A3209: mov ecx, dword ptr [ebp + 0x48]
004A320C: mov edx, dword ptr [0x8529a0]
004A3212: cmp ecx, edx
004A3214: je 0x4a322e
004A3216: mov dword ptr [ebp + 0x40], eax
004A3219: mov edx, dword ptr [0x85299c]
004A321F: mov dword ptr [ebp + 0x44], edx
004A3222: mov eax, dword ptr [0x8529a0]
004A3227: mov dword ptr [ebp + 0x48], eax
004A322A: mov byte ptr [ebp + 0x63], 0
004A322E: mov ecx, dword ptr [ebp + 0xc]
004A3231: mov eax, dword ptr [ecx + 0x488]
004A3237: test eax, eax
004A3239: jne 0x4a44b3
004A323F: mov edx, dword ptr [ecx]
004A3241: push 1
004A3243: push 0
004A3245: call dword ptr [edx + 0x410]
004A324B: pop edi
004A324C: pop esi
004A324D: pop ebp
004A324E: xor al, al
004A3250: pop ebx
004A3251: add esp, 0x4c
004A3254: ret 0xc
004A3257: mov eax, dword ptr [esi + 0x140]
004A325D: test ah, 1
004A3260: je 0x4a329a
004A3262: mov ecx, dword ptr [ebp + 0xc]
004A3265: mov byte ptr [esp + 0x18], 1
004A326A: add ecx, 0x88
004A3270: mov edx, dword ptr [ecx]
004A3272: mov dword ptr [esp + 0x44], edx
004A3276: mov eax, dword ptr [ecx + 4]
004A3279: mov dword ptr [esp + 0x48], eax
004A327D: mov eax, dword ptr [ecx + 8]
004A3280: cdq 
004A3281: idiv dword ptr [0x8529d0]
004A3287: movsx ecx, byte ptr [esi + 0x11b]
004A328E: sub eax, ecx
004A3290: cdq 
004A3291: xor eax, edx
004A3293: sub eax, edx
004A3295: cmp eax, 2
004A3298: jg 0x4a329f
004A329A: mov byte ptr [esp + 0x18], 0
004A329F: mov edx, dword ptr [esp + 0x18]
004A32A3: mov ecx, esi
004A32A5: push edx
004A32A6: push 1
004A32A8: push 1
004A32AA: push 0x852998
004A32AF: call 0x476920
004A32B4: mov eax, dword ptr [ebp + 0xc]
004A32B7: mov dword ptr [eax + 0x53c], 0xa
004A32C1: mov ecx, dword ptr [ebp + 0xc]
004A32C4: mov ebx, dword ptr [ecx + 0x4d0]
004A32CA: cmp ebx, 8
004A32CD: je 0x4a3a44
004A32D3: mov edx, dword ptr [ebp + 0xc]
004A32D6: mov esi, ebx
004A32D8: add edx, 0x88
004A32DE: and esi, 7
004A32E1: mov eax, dword ptr [edx]
004A32E3: lea esi, [esi*8 + 0x851ac0]
004A32EA: mov ecx, dword ptr [edx + 4]
004A32ED: mov edx, dword ptr [edx + 8]
004A32F0: push edx
004A32F1: mov edx, dword ptr [esi + 4]
004A32F4: add edx, ecx
004A32F6: mov ecx, dword ptr [esi]
004A32F8: add ecx, eax
004A32FA: push edx
004A32FB: push ecx
004A32FC: lea ecx, [esp + 0x50]
004A3300: call 0x41b630
004A3305: mov edx, dword ptr [eax]
004A3307: mov dword ptr [esp + 0x38], edx
004A330B: mov ecx, dword ptr [eax + 4]
004A330E: mov dword ptr [esp + 0x3c], ecx
004A3312: mov edx, dword ptr [eax + 8]
004A3315: mov eax, dword ptr [ebp + 0xc]
004A3318: add eax, 0x88
004A331D: mov dword ptr [esp + 0x40], edx
004A3321: mov ecx, dword ptr [eax]
004A3323: mov dword ptr [esp + 0x2c], ecx
004A3327: lea ecx, [esp + 0x2c]
004A332B: mov edx, dword ptr [eax + 4]
004A332E: push ecx
004A332F: mov dword ptr [esp + 0x34], edx
004A3333: mov ecx, 0x8324e0
004A3338: mov eax, dword ptr [eax + 8]
004A333B: mov dword ptr [esp + 0x38], eax
004A333F: call 0x548000
004A3344: mov ecx, dword ptr [ebp + 0xc]
004A3347: movsx eax, byte ptr [eax + 0x11b]
004A334E: mov dl, byte ptr [ecx + 0x79]
004A3351: neg dl
004A3353: sbb edx, edx
004A3355: add ecx, 0x88
004A335B: and edx, 4
004A335E: add edx, eax
004A3360: mov edi, edx
004A3362: mov edx, ecx
004A3364: mov eax, dword ptr [edx]
004A3366: mov ecx, dword ptr [edx + 4]
004A3369: mov edx, dword ptr [edx + 8]
004A336C: push edx
004A336D: mov edx, dword ptr [esi + 4]
004A3370: add edx, ecx
004A3372: mov ecx, dword ptr [esi]
004A3374: add ecx, eax
004A3376: push edx
004A3377: push ecx
004A3378: lea ecx, [esp + 0x50]
004A337C: call 0x41b630
004A3381: mov edx, dword ptr [eax]
004A3383: mov dword ptr [esp + 0x2c], edx
004A3387: mov ecx, dword ptr [eax + 4]
004A338A: mov dword ptr [esp + 0x30], ecx
004A338E: mov ecx, 0x8324e0
004A3393: mov edx, dword ptr [eax + 8]
004A3396: lea eax, [esp + 0x2c]
004A339A: push eax
004A339B: mov dword ptr [esp + 0x38], edx
004A339F: call 0x548000
004A33A4: mov edx, dword ptr [eax + 0x140]
004A33AA: mov ecx, dword ptr [ebp + 0xc]
004A33AD: shr edx, 8
004A33B0: xor eax, eax
004A33B2: and edx, 1
004A33B5: mov al, byte ptr [ecx + 0x79]
004A33B8: xor edx, eax
004A33BA: je 0x4a33c3
004A33BC: mov byte ptr [ecx + 0x57b], 1
004A33C3: mov ecx, dword ptr [ebp + 0xc]
004A33C6: mov edx, dword ptr [ecx]
004A33C8: call dword ptr [edx + 0x27c]
004A33CE: test al, al
004A33D0: jne 0x4a33de
004A33D2: pop edi
004A33D3: pop esi
004A33D4: pop ebp
004A33D5: mov al, 1
004A33D7: pop ebx
004A33D8: add esp, 0x4c
004A33DB: ret 0xc
004A33DE: mov eax, dword ptr [esp + 0x38]
004A33E2: lea ecx, [esp + 0x28]
004A33E6: cdq 
004A33E7: and edx, 0xff
004A33ED: push ecx
004A33EE: add eax, edx
004A33F0: mov ecx, 0x8324e0
004A33F5: sar eax, 8
004A33F8: mov word ptr [esp + 0x1c], ax
004A33FD: mov eax, dword ptr [esp + 0x40]
004A3401: cdq 
004A3402: and edx, 0xff
004A3408: add eax, edx
004A340A: mov edx, dword ptr [ebp + 0xc]
004A340D: sar eax, 8
004A3410: mov word ptr [esp + 0x1e], ax
004A3415: mov eax, dword ptr [esp + 0x1c]
004A3419: push edx
004A341A: mov dword ptr [esp + 0x30], eax
004A341E: call 0x55acd0
004A3423: test al, al
004A3425: jne 0x4a3433
004A3427: pop edi
004A3428: pop esi
004A3429: pop ebp
004A342A: mov al, 1
004A342C: pop ebx
004A342D: add esp, 0x4c
004A3430: ret 0xc
004A3433: mov ecx, dword ptr [ebp + 0xc]
004A3436: lea eax, [esp + 0x2c]
004A343A: push eax
004A343B: add ecx, 0x2e0
004A3441: call 0x4b8be0
004A3446: mov ax, word ptr [eax]
004A3449: mov ecx, ebx
004A344B: shl ecx, 0xd
004A344E: sub ax, cx
004A3451: movsx eax, ax
004A3454: cdq 
004A3455: mov esi, eax
004A3457: xor eax, eax
004A3459: xor esi, edx
004A345B: sub esi, edx
004A345D: cdq 
004A345E: xor eax, edx
004A3460: sub eax, edx
004A3462: cmp eax, esi
004A3464: jge 0x4a3486
004A3466: mov eax, dword ptr [esp + 0x14]
004A346A: mov word ptr [esp + 0x68], cx
004A346F: mov edx, dword ptr [esp + 0x68]
004A3473: mov ecx, dword ptr [eax]
004A3475: push edx
004A3476: push eax
004A3477: call dword ptr [ecx + 0x4c]
004A347A: pop edi
004A347B: pop esi
004A347C: pop ebp
004A347D: mov al, 1
004A347F: pop ebx
004A3480: add esp, 0x4c
004A3483: ret 0xc
004A3486: mov eax, dword ptr [esp + 0x38]
004A348A: lea ecx, [esp + 0x14]
004A348E: cdq 
004A348F: and edx, 0xff
004A3495: push ecx
004A3496: add eax, edx
004A3498: mov ecx, 0x8324e0
004A349D: sar eax, 8
004A34A0: mov word ptr [esp + 0x1c], ax
004A34A5: mov eax, dword ptr [esp + 0x40]
004A34A9: cdq 
004A34AA: and edx, 0xff
004A34B0: add eax, edx
004A34B2: sar eax, 8
004A34B5: mov word ptr [esp + 0x1e], ax
004A34BA: mov eax, dword ptr [esp + 0x1c]
004A34BE: mov dword ptr [esp + 0x18], eax
004A34C2: call 0x548070
004A34C7: mov ecx, dword ptr [ebp + 0xc]
004A34CA: mov esi, eax
004A34CC: push 0
004A34CE: mov dword ptr [esp + 0x30], esi
004A34D2: mov edx, dword ptr [ecx]
004A34D4: mov byte ptr [esp + 0x17], 0
004A34D9: call dword ptr [edx + 0x11c]
004A34DF: mov ecx, dword ptr [ebp + 0xc]
004A34E2: push 1
004A34E4: push 0
004A34E6: push edi
004A34E7: mov eax, dword ptr [ecx]
004A34E9: push ebx
004A34EA: push esi
004A34EB: call dword ptr [eax + 0x194]
004A34F1: mov ecx, dword ptr [ebp + 0xc]
004A34F4: push 1
004A34F6: mov dword ptr [esp + 0x1c], eax
004A34FA: mov edx, dword ptr [ecx]
004A34FC: call dword ptr [edx + 0x11c]
004A3502: cmp dword ptr [esp + 0x18], 7
004A3507: jge 0x4a351e
004A3509: mov ecx, dword ptr [ebp + 0xc]
004A350C: mov eax, dword ptr [ecx]
004A350E: call dword ptr [eax + 0x80]
004A3514: mov cl, byte ptr [eax + 0xaa0]
004A351A: test cl, cl
004A351C: jne 0x4a3548
004A351E: mov eax, dword ptr [esp + 0x18]
004A3522: cmp eax, 5
004A3525: je 0x4a352c
004A3527: cmp eax, 4
004A352A: jne 0x4a3550
004A352C: mov ecx, dword ptr [ebp + 0xc]
004A352F: mov edx, dword ptr [ecx]
004A3531: call dword ptr [edx + 0x80]
004A3537: mov cl, byte ptr [eax + 0xaf3]
004A353D: test cl, cl
004A353F: je 0x4a3550
004A3541: mov eax, dword ptr [esi + 0x44]
004A3544: test eax, eax
004A3546: jne 0x4a3550
004A3548: mov dword ptr [esp + 0x18], 0
004A3550: mov eax, dword ptr [esi + 0x44]
004A3553: mov ecx, dword ptr [esp + 0x18]
004A3557: or esi, 0xffffffff
004A355A: cmp eax, esi
004A355C: je 0x4a35d6
004A355E: test ecx, ecx
004A3560: jne 0x4a35da
004A3562: mov ecx, dword ptr [0xa35dec]
004A3568: mov edx, dword ptr [ecx + eax*4]
004A356B: mov al, byte ptr [edx + 0x1fd]
004A3571: test al, al
004A3573: je 0x4a357a
004A3575: mov byte ptr [esp + 0x13], 1
004A357A: lea edx, [esp + 0x14]
004A357E: mov ecx, 0x8324e0
004A3583: push edx
004A3584: call 0x548070
004A3589: movsx ecx, byte ptr [eax + 0x11b]
004A3590: mov eax, edi
004A3592: sub eax, ecx
004A3594: cdq 
004A3595: xor eax, edx
004A3597: sub eax, edx
004A3599: cmp eax, 2
004A359C: jge 0x4a3c92
004A35A2: lea edx, [esp + 0x14]
004A35A6: mov ecx, 0x8324e0
004A35AB: push edx
004A35AC: call 0x548070
004A35B1: movsx eax, byte ptr [eax + 0x11b]
004A35B8: lea ecx, [esp + 0x14]
004A35BC: mov dword ptr [esp + 0x28], eax
004A35C0: push ecx
004A35C1: mov ecx, 0x8324e0
004A35C6: call 0x548070
004A35CB: mov esi, dword ptr [eax + 0xec]
004A35D1: jmp 0x4a3c9b
004A35D6: test ecx, ecx
004A35D8: je 0x4a357a
004A35DA: cmp ecx, 3
004A35DD: jne 0x4a36ed
004A35E3: mov edx, dword ptr [ebp + 0xc]
004A35E6: mov eax, dword ptr [esp + 0x14]
004A35EA: lea ecx, [esp + 0x68]
004A35EE: mov dword ptr [esp + 0x68], eax
004A35F2: push ecx
004A35F3: push edx
004A35F4: mov ecx, 0x8324e0
004A35F9: call 0x55acd0
004A35FE: xor edi, edi
004A3600: mov eax, dword ptr [0x852998]
004A3605: mov ecx, dword ptr [ebp + 0x40]
004A3608: lea ebx, [ebp + 0x40]
004A360B: cmp ecx, eax
004A360D: jne 0x4a3629
004A360F: mov ecx, dword ptr [ebx + 4]
004A3612: mov edx, dword ptr [0x85299c]
004A3618: cmp ecx, edx
004A361A: jne 0x4a3629
004A361C: mov edx, dword ptr [ebx + 8]
004A361F: mov ecx, dword ptr [0x8529a0]
004A3625: cmp edx, ecx
004A3627: je 0x4a3642
004A3629: mov ecx, ebx
004A362B: mov dword ptr [ecx], eax
004A362D: mov edx, dword ptr [0x85299c]
004A3633: mov dword ptr [ecx + 4], edx
004A3636: mov eax, dword ptr [0x8529a0]
004A363B: mov byte ptr [ebp + 0x63], 0
004A363F: mov dword ptr [ecx + 8], eax
004A3642: mov eax, dword ptr [esp + 0x18]
004A3646: cmp eax, 2
004A3649: jne 0x4a3a8e
004A364F: mov eax, dword ptr [ebp + 0xc]
004A3652: mov cl, byte ptr [eax + 0x5a1]
004A3658: test cl, cl
004A365A: jne 0x4a3689
004A365C: mov byte ptr [eax + 0x5a1], 1
004A3663: mov edx, dword ptr [ebp + 0xc]
004A3666: mov ecx, dword ptr [0x839848]
004A366C: mov eax, dword ptr [0xa40d2c]
004A3671: add edx, 0x558
004A3677: mov ecx, dword ptr [ecx + 0x13d0]
004A367D: mov dword ptr [edx], eax
004A367F: mov eax, dword ptr [esp + 0x54]
004A3683: mov dword ptr [edx + 4], eax
004A3686: mov dword ptr [edx + 8], ecx
004A3689: mov ecx, dword ptr [ebp + 0xc]
004A368C: mov edi, dword ptr [0xa40d2c]
004A3692: mov esi, dword ptr [ecx + 0x530]
004A3698: mov eax, dword ptr [ecx + 0x538]
004A369E: cmp esi, -1
004A36A1: je 0x4a36ad
004A36A3: mov edx, edi
004A36A5: sub edx, esi
004A36A7: cmp edx, eax
004A36A9: jge 0x4a36b5
004A36AB: sub eax, edx
004A36AD: test eax, eax
004A36AF: jne 0x4a3a98
004A36B5: mov al, byte ptr [ecx + 0x5a1]
004A36BB: test al, al
004A36BD: je 0x4a39c8
004A36C3: mov edx, dword ptr [ecx + 0x558]
004A36C9: mov eax, dword ptr [ecx + 0x560]
004A36CF: cmp edx, -1
004A36D2: je 0x4a36de
004A36D4: sub edi, edx
004A36D6: mov edx, edi
004A36D8: cmp edx, eax
004A36DA: jge 0x4a36e6
004A36DC: sub eax, edx
004A36DE: test eax, eax
004A36E0: jne 0x4a39c8
004A36E6: mov bl, 1
004A36E8: jmp 0x4a39ca
004A36ED: cmp ecx, 6
004A36F0: jne 0x4a393b
004A36F6: mov ecx, dword ptr [ebp + 0xc]
004A36F9: mov eax, dword ptr [ecx]
004A36FB: call dword ptr [eax + 0x80]
004A3701: mov cl, byte ptr [eax + 0xaa0]
004A3707: test cl, cl
004A3709: jne 0x4a35fe
004A370F: mov al, byte ptr [esp + 0x64]
004A3713: mov ecx, dword ptr [ebp + 0xc]
004A3716: test al, al
004A3718: je 0x4a373b
004A371A: mov dword ptr [ecx + 0x4d0], esi
004A3720: mov edx, dword ptr [ebp + 0xc]
004A3723: mov eax, dword ptr [0xa40d2c]
004A3728: xor ecx, ecx
004A372A: add edx, 0x530
004A3730: mov dword ptr [edx], eax
004A3732: mov eax, dword ptr [esp + 0x48]
004A3736: jmp 0x4a4502
004A373B: mov edx, dword ptr [ecx]
004A373D: lea eax, [esp + 0x44]
004A3741: push eax
004A3742: call dword ptr [edx + 0x48]
004A3745: mov ecx, dword ptr [eax + 8]
004A3748: mov edi, dword ptr [ebp + 0x3c]
004A374B: mov edx, dword ptr [eax + 4]
004A374E: mov ebx, dword ptr [ebp + 0x38]
004A3751: mov eax, dword ptr [eax]
004A3753: sub ecx, edi
004A3755: sub edx, ebx
004A3757: push ecx
004A3758: push edx
004A3759: mov edx, dword ptr [ebp + 0x34]
004A375C: sub eax, edx
004A375E: lea ecx, [esp + 0x58]
004A3762: push eax
004A3763: call 0x41b630
004A3768: mov ecx, dword ptr [eax]
004A376A: sub esp, 8
004A376D: mov dword ptr [esp + 0x34], ecx
004A3771: mov edx, dword ptr [eax + 4]
004A3774: fild dword ptr [esp + 0x34]
004A3778: mov eax, dword ptr [eax + 8]
004A377B: mov dword ptr [esp + 0x38], edx
004A377F: fild dword ptr [esp + 0x38]
004A3783: mov dword ptr [esp + 0x3c], eax
004A3787: fild dword ptr [esp + 0x3c]
004A378B: fld st(0)
004A378D: fmul st(1)
004A378F: fld st(2)
004A3791: fmul st(3)
004A3793: faddp st(1)
004A3795: fld st(3)
004A3797: fmul st(4)
004A3799: faddp st(1)
004A379B: fstp qword ptr [esp]
004A379E: fstp st(0)
004A37A0: fstp st(0)
004A37A2: fstp st(0)
004A37A4: call 0x4ba410
004A37A9: add esp, 8
004A37AC: call 0x77f110
004A37B1: mov ecx, dword ptr [0x839848]
004A37B7: cmp eax, dword ptr [ecx + 0x1380]
004A37BD: jge 0x4a38aa
004A37C3: mov ecx, dword ptr [ebp + 0xc]
004A37C6: add ecx, 0x88
004A37CC: mov edx, ecx
004A37CE: mov eax, dword ptr [edx]
004A37D0: mov dword ptr [esp + 0x44], eax
004A37D4: mov eax, dword ptr [edx + 4]
004A37D7: mov dword ptr [esp + 0x48], eax
004A37DB: mov eax, dword ptr [ebp + 0x3c]
004A37DE: mov edx, dword ptr [edx + 8]
004A37E1: sub eax, edx
004A37E3: cdq 
004A37E4: xor eax, edx
004A37E6: sub eax, edx
004A37E8: mov edx, dword ptr [0x8529d0]
004A37EE: add edx, edx
004A37F0: cmp eax, edx
004A37F2: jge 0x4a38aa
004A37F8: mov eax, dword ptr [ecx]
004A37FA: mov dword ptr [esp + 0x2c], eax
004A37FE: mov edx, dword ptr [ecx + 4]
004A3801: mov dword ptr [esp + 0x30], edx
004A3805: mov eax, dword ptr [ecx + 8]
004A3808: lea ecx, [esp + 0x2c]
004A380C: mov dword ptr [esp + 0x34], eax
004A3810: push ecx
004A3811: mov ecx, 0x8324e0
004A3816: call 0x548000
004A381B: cmp dword ptr [eax + 0xec], 0xa
004A3822: je 0x4a38aa
004A3828: mov eax, dword ptr [0x852998]
004A382D: mov ecx, dword ptr [ebp + 0x40]
004A3830: cmp ecx, eax
004A3832: jne 0x4a384e
004A3834: mov edx, dword ptr [ebp + 0x44]
004A3837: mov ecx, dword ptr [0x85299c]
004A383D: cmp edx, ecx
004A383F: jne 0x4a384e
004A3841: mov ecx, dword ptr [ebp + 0x48]
004A3844: mov edx, dword ptr [0x8529a0]
004A384A: cmp ecx, edx
004A384C: je 0x4a3866
004A384E: mov dword ptr [ebp + 0x40], eax
004A3851: mov edx, dword ptr [0x85299c]
004A3857: mov dword ptr [ebp + 0x44], edx
004A385A: mov eax, dword ptr [0x8529a0]
004A385F: mov dword ptr [ebp + 0x48], eax
004A3862: mov byte ptr [ebp + 0x63], 0
004A3866: mov ecx, dword ptr [ebp + 0xc]
004A3869: xor edi, edi
004A386B: cmp dword ptr [ecx + 0x488], edi
004A3871: jne 0x4a3883
004A3873: mov edx, dword ptr [ecx]
004A3875: push 1
004A3877: push edi
004A3878: call dword ptr [edx + 0x410]
004A387E: jmp 0x4a3600
004A3883: call 0x4cd9b0
004A3888: mov ecx, dword ptr [ebp + 0xc]
004A388B: push 1
004A388D: push edi
004A388E: mov eax, dword ptr [ecx]
004A3890: call dword ptr [eax + 0x414]
004A3896: test al, al
004A3898: je 0x4a3600
004A389E: pop edi
004A389F: pop esi
004A38A0: pop ebp
004A38A1: mov al, 1
004A38A3: pop ebx
004A38A4: add esp, 0x4c
004A38A7: ret 0xc
004A38AA: lea ecx, [esp + 0x14]
004A38AE: push ecx
004A38AF: mov ecx, 0x8324e0
004A38B4: call 0x548070
004A38B9: mov ecx, dword ptr [eax + 0x140]
004A38BF: test ch, 1
004A38C2: je 0x4a390d
004A38C4: mov edx, dword ptr [ebp + 0xc]
004A38C7: add edx, 0x88
004A38CD: mov eax, dword ptr [edx]
004A38CF: mov dword ptr [esp + 0x44], eax
004A38D3: mov ecx, dword ptr [edx + 4]
004A38D6: mov dword ptr [esp + 0x48], ecx
004A38DA: mov ecx, 0x8324e0
004A38DF: mov edi, dword ptr [edx + 8]
004A38E2: lea edx, [esp + 0x14]
004A38E6: push edx
004A38E7: call 0x548070
004A38EC: movsx ecx, byte ptr [eax + 0x11b]
004A38F3: mov eax, edi
004A38F5: mov byte ptr [esp + 0x68], 1
004A38FA: cdq 
004A38FB: idiv dword ptr [0x8529d0]
004A3901: sub eax, ecx
004A3903: cdq 
004A3904: xor eax, edx
004A3906: sub eax, edx
004A3908: cmp eax, 2
004A390B: jg 0x4a3912
004A390D: mov byte ptr [esp + 0x68], 0
004A3912: mov edx, dword ptr [esp + 0x68]
004A3916: lea eax, [esp + 0x14]
004A391A: push edx
004A391B: push 1
004A391D: push 1
004A391F: push 0x852998
004A3924: push eax
004A3925: mov ecx, 0x8324e0
004A392A: call 0x548070
004A392F: mov ecx, eax
004A3931: call 0x476920
004A3936: jmp 0x4a35fe
004A393B: cmp ecx, 1
004A393E: jne 0x4a35fe
004A3944: lea ecx, [esp + 0x14]
004A3948: push ecx
004A3949: mov ecx, 0x8324e0
004A394E: call 0x548070
004A3953: mov ecx, eax
004A3955: call 0x478740
004A395A: mov al, byte ptr [esp + 0x64]
004A395E: test al, al
004A3960: je 0x4a3985
004A3962: mov edx, dword ptr [ebp + 0xc]
004A3965: mov eax, dword ptr [esp + 0x60]
004A3969: push 0
004A396B: push 0
004A396D: push eax
004A396E: mov ecx, ebp
004A3970: mov dword ptr [edx + 0x4d0], esi
004A3976: call 0x4a2670
004A397B: pop edi
004A397C: pop esi
004A397D: pop ebp
004A397E: pop ebx
004A397F: add esp, 0x4c
004A3982: ret 0xc
004A3985: mov eax, dword ptr [0x852998]
004A398A: mov ecx, dword ptr [ebp + 0x40]
004A398D: cmp ecx, eax
004A398F: jne 0x4a39af
004A3991: mov ecx, dword ptr [ebp + 0x44]
004A3994: mov edx, dword ptr [0x85299c]
004A399A: cmp ecx, edx
004A399C: jne 0x4a39af
004A399E: mov edx, dword ptr [ebp + 0x48]
004A39A1: mov ecx, dword ptr [0x8529a0]
004A39A7: cmp edx, ecx
004A39A9: je 0x4a322e
004A39AF: mov dword ptr [ebp + 0x40], eax
004A39B2: mov eax, dword ptr [0x85299c]
004A39B7: mov dword ptr [ebp + 0x44], eax
004A39BA: mov ecx, dword ptr [0x8529a0]
004A39C0: mov dword ptr [ebp + 0x48], ecx
004A39C3: jmp 0x4a322a
004A39C8: xor bl, bl
004A39CA: mov eax, dword ptr [ebp + 0x34]
004A39CD: lea esi, [ebp + 0x34]
004A39D0: cdq 
004A39D1: and edx, 0xff
004A39D7: add eax, edx
004A39D9: sar eax, 8
004A39DC: mov word ptr [esp + 0x68], ax
004A39E1: mov eax, dword ptr [esi + 4]
004A39E4: cdq 
004A39E5: and edx, 0xff
004A39EB: add eax, edx
004A39ED: xor edx, edx
004A39EF: sar eax, 8
004A39F2: test bl, bl
004A39F4: setne dl
004A39F7: inc edx
004A39F8: mov word ptr [esp + 0x6a], ax
004A39FD: mov eax, dword ptr [esp + 0x68]
004A3A01: push edx
004A3A02: push 0
004A3A04: push eax
004A3A05: call 0x4c3000
004A3A0A: mov ecx, dword ptr [ebp + 0xc]
004A3A0D: test ecx, ecx
004A3A0F: jne 0x4a3a24
004A3A11: mov ecx, dword ptr [esp + 0x60]
004A3A15: pop edi
004A3A16: pop esi
004A3A17: pop ebp
004A3A18: mov byte ptr [ecx], 1
004A3A1B: xor al, al
004A3A1D: pop ebx
004A3A1E: add esp, 0x4c
004A3A21: ret 0xc
004A3A24: test al, al
004A3A26: jne 0x4a3a50
004A3A28: mov edx, dword ptr [ecx]
004A3A2A: push esi
004A3A2B: call dword ptr [edx + 0x2ac]
004A3A31: test al, al
004A3A33: jne 0x4a3a50
004A3A35: mov ecx, dword ptr [ebp + 0xc]
004A3A38: mov eax, dword ptr [ecx]
004A3A3A: push 1
004A3A3C: push 0
004A3A3E: call dword ptr [eax + 0x410]
004A3A44: pop edi
004A3A45: pop esi
004A3A46: pop ebp
004A3A47: xor al, al
004A3A49: pop ebx
004A3A4A: add esp, 0x4c
004A3A4D: ret 0xc
004A3A50: mov ecx, dword ptr [0x839848]
004A3A56: mov esi, dword ptr [0xa40d2c]
004A3A5C: fld qword ptr [ecx + 0x13c8]
004A3A62: fmul qword ptr [0x79b608]
004A3A68: call 0x77f110
004A3A6D: mov edx, dword ptr [ebp + 0xc]
004A3A70: mov ecx, dword ptr [esp + 0x54]
004A3A74: add edx, 0x530
004A3A7A: pop edi
004A3A7B: mov dword ptr [edx], esi
004A3A7D: pop esi
004A3A7E: pop ebp
004A3A7F: pop ebx
004A3A80: mov dword ptr [edx + 4], ecx
004A3A83: mov dword ptr [edx + 8], eax
004A3A86: mov al, 1
004A3A88: add esp, 0x4c
004A3A8B: ret 0xc
004A3A8E: cmp eax, 5
004A3A91: je 0x4a3acf
004A3A93: cmp eax, 4
004A3A96: je 0x4a3aca
004A3A98: mov edx, dword ptr [ebp + 0xc]
004A3A9B: mov al, byte ptr [edx + 0x57a]
004A3AA1: test al, al
004A3AA3: je 0x4a3bfd
004A3AA9: mov eax, dword ptr [0x839848]
004A3AAE: push 0
004A3AB0: mov edx, 0x2000
004A3AB5: push 0x3f800000
004A3ABA: mov ecx, dword ptr [eax + 0x620]
004A3AC0: call 0x713db0
004A3AC5: jmp 0x4a3bfd
004A3ACA: or esi, 0xffffffff
004A3ACD: xor edi, edi
004A3ACF: mov al, byte ptr [esp + 0x64]
004A3AD3: test al, al
004A3AD5: je 0x4a3b14
004A3AD7: mov ecx, dword ptr [ebp + 0xc]
004A3ADA: push edi
004A3ADB: push edi
004A3ADC: mov dword ptr [ecx + 0x4d0], esi
004A3AE2: mov edx, dword ptr [ebp + 0xc]
004A3AE5: mov eax, dword ptr [0xa40d2c]
004A3AEA: add edx, 0x530
004A3AF0: xor ecx, ecx
004A3AF2: mov dword ptr [edx], eax
004A3AF4: mov eax, dword ptr [esp + 0x5c]
004A3AF8: mov dword ptr [edx + 4], eax
004A3AFB: mov dword ptr [edx + 8], ecx
004A3AFE: mov ecx, dword ptr [esp + 0x68]
004A3B02: push ecx
004A3B03: mov ecx, ebp
004A3B05: call 0x4a2670
004A3B0A: pop edi
004A3B0B: pop esi
004A3B0C: pop ebp
004A3B0D: pop ebx
004A3B0E: add esp, 0x4c
004A3B11: ret 0xc
004A3B14: lea edx, [esp + 0x2c]
004A3B18: push edi
004A3B19: lea eax, [esp + 0x18]
004A3B1D: push edx
004A3B1E: push eax
004A3B1F: mov ecx, 0x8324e0
004A3B24: mov dword ptr [esp + 0x38], edi
004A3B28: mov dword ptr [esp + 0x3c], edi
004A3B2C: call 0x548070
004A3B31: mov ecx, eax
004A3B33: call 0x471830
004A3B38: test eax, eax
004A3B3A: je 0x4a3ba3
004A3B3C: lea ecx, [esp + 0x2c]
004A3B40: push edi
004A3B41: lea edx, [esp + 0x18]
004A3B45: push ecx
004A3B46: push edx
004A3B47: mov ecx, 0x8324e0
004A3B4C: mov dword ptr [esp + 0x38], edi
004A3B50: mov dword ptr [esp + 0x3c], edi
004A3B54: call 0x548070
004A3B59: mov ecx, eax
004A3B5B: call 0x471830
004A3B60: push eax
004A3B61: mov eax, dword ptr [ebp + 0xc]
004A3B64: mov ecx, dword ptr [eax + 0x1b4]
004A3B6A: call 0x4e5580
004A3B6F: test al, al
004A3B71: jne 0x4a3bfd
004A3B77: mov ecx, dword ptr [ebp + 0xc]
004A3B7A: push edi
004A3B7B: lea edx, [esp + 0x30]
004A3B7F: mov dword ptr [esp + 0x30], edi
004A3B83: mov dword ptr [esp + 0x34], edi
004A3B87: mov esi, dword ptr [ecx]
004A3B89: push edi
004A3B8A: lea eax, [esp + 0x1c]
004A3B8E: push edx
004A3B8F: push eax
004A3B90: mov ecx, 0x8324e0
004A3B95: call 0x548070
004A3B9A: mov ecx, eax
004A3B9C: call 0x471830
004A3BA1: jmp 0x4a3bf1
004A3BA3: lea ecx, [esp + 0x14]
004A3BA7: push ecx
004A3BA8: mov ecx, 0x8324e0
004A3BAD: call 0x548070
004A3BB2: cmp dword ptr [eax + 0x44], esi
004A3BB5: je 0x4a3bfd
004A3BB7: lea edx, [esp + 0x14]
004A3BBB: mov ecx, 0x8324e0
004A3BC0: push edx
004A3BC1: call 0x548070
004A3BC6: mov eax, dword ptr [eax + 0x44]
004A3BC9: mov ecx, dword ptr [0xa35dec]
004A3BCF: mov edx, dword ptr [ecx + eax*4]
004A3BD2: mov al, byte ptr [edx + 0x278]
004A3BD8: test al, al
004A3BDA: je 0x4a3bfd
004A3BDC: mov eax, dword ptr [ebp + 0xc]
004A3BDF: lea ecx, [esp + 0x14]
004A3BE3: push edi
004A3BE4: push ecx
004A3BE5: mov esi, dword ptr [eax]
004A3BE7: mov ecx, 0x8324e0
004A3BEC: call 0x548070
004A3BF1: mov ecx, dword ptr [ebp + 0xc]
004A3BF4: push eax
004A3BF5: push 1
004A3BF7: call dword ptr [esi + 0x1dc]
004A3BFD: cmp dword ptr [esp + 0x18], 7
004A3C02: jne 0x4a3c75
004A3C04: mov al, byte ptr [esp + 0x64]
004A3C08: test al, al
004A3C0A: je 0x4a3c34
004A3C0C: mov edx, dword ptr [ebp + 0xc]
004A3C0F: xor ecx, ecx
004A3C11: mov dword ptr [edx + 0x4d0], 0xffffffff
004A3C1B: mov edx, dword ptr [ebp + 0xc]
004A3C1E: mov eax, dword ptr [0xa40d2c]
004A3C23: add edx, 0x530
004A3C29: mov dword ptr [edx], eax
004A3C2B: mov eax, dword ptr [esp + 0x54]
004A3C2F: jmp 0x4a4502
004A3C34: mov eax, dword ptr [0x852998]
004A3C39: mov ecx, dword ptr [ebx]
004A3C3B: cmp ecx, eax
004A3C3D: jne 0x4a3c5d
004A3C3F: mov edx, dword ptr [0x85299c]
004A3C45: mov ecx, dword ptr [ebx + 4]
004A3C48: cmp ecx, edx
004A3C4A: jne 0x4a3c5d
004A3C4C: mov ecx, dword ptr [0x8529a0]
004A3C52: mov edx, dword ptr [ebx + 8]
004A3C55: cmp edx, ecx
004A3C57: je 0x4a322e
004A3C5D: mov dword ptr [ebx], eax
004A3C5F: mov edx, dword ptr [0x85299c]
004A3C65: mov dword ptr [ebx + 4], edx
004A3C68: mov eax, dword ptr [0x8529a0]
004A3C6D: mov dword ptr [ebx + 8], eax
004A3C70: jmp 0x4a322a
004A3C75: mov ecx, dword ptr [ebp + 0xc]
004A3C78: pop edi
004A3C79: pop esi
004A3C7A: mov al, 1
004A3C7C: mov byte ptr [ecx + 0x57a], 0
004A3C83: mov dword ptr [ebp + 0x58], 0xffffffff
004A3C8A: pop ebp
004A3C8B: pop ebx
004A3C8C: add esp, 0x4c
004A3C8F: ret 0xc
004A3C92: mov dword ptr [esp + 0x28], edi
004A3C96: mov esi, 1
004A3C9B: mov ecx, dword ptr [ebp + 0xc]
004A3C9E: mov edx, dword ptr [ecx]
004A3CA0: call dword ptr [edx + 0x80]
004A3CA6: mov edx, dword ptr [eax + 0x5a4]
004A3CAC: lea ecx, [esi + esi*8]
004A3CAF: add edx, ecx
004A3CB1: fld dword ptr [edx*4 + 0x850ea0]
004A3CB8: fst qword ptr [esp + 0x18]
004A3CBC: fcomp qword ptr [0x79a708]
004A3CC2: fnstsw ax
004A3CC4: test ah, 0x41
004A3CC7: jne 0x4a3cd9
004A3CC9: mov dword ptr [esp + 0x18], 0
004A3CD1: mov dword ptr [esp + 0x1c], 0x3ff00000
004A3CD9: lea eax, [esp + 0x50]
004A3CDD: lea ecx, [esp + 0x14]
004A3CE1: push eax
004A3CE2: push ecx
004A3CE3: mov ecx, 0x8324e0
004A3CE8: call 0x548070
004A3CED: mov ecx, eax
004A3CEF: call 0x475d60
004A3CF4: push eax
004A3CF5: mov ecx, 0x8324e0
004A3CFA: call 0x55a280
004A3CFF: mov edx, dword ptr [ebp + 0xc]
004A3D02: mov esi, eax
004A3D04: add edx, 0x88
004A3D0A: mov eax, dword ptr [edx]
004A3D0C: mov dword ptr [esp + 0x44], eax
004A3D10: lea eax, [esp + 0x44]
004A3D14: mov ecx, dword ptr [edx + 4]
004A3D17: push eax
004A3D18: mov dword ptr [esp + 0x4c], ecx
004A3D1C: mov ecx, 0x8324e0
004A3D21: mov edx, dword ptr [edx + 8]
004A3D24: mov dword ptr [esp + 0x50], edx
004A3D28: call 0x55a280
004A3D2D: mov edi, eax
004A3D2F: cmp esi, edi
004A3D31: jle 0x4a3d78
004A3D33: mov ecx, dword ptr [ebp + 0xc]
004A3D36: mov edx, dword ptr [ecx]
004A3D38: call dword ptr [edx + 0x2c]
004A3D3B: cmp eax, 1
004A3D3E: jne 0x4a3d76
004A3D40: mov ecx, dword ptr [ebp + 0xc]
004A3D43: mov eax, dword ptr [ecx]
004A3D45: call dword ptr [eax + 0x80]
004A3D4B: mov ecx, dword ptr [eax + 0x5a4]
004A3D51: fld qword ptr [esp + 0x18]
004A3D55: cmp ecx, 1
004A3D58: jne 0x4a3d68
004A3D5A: mov ecx, dword ptr [0x839848]
004A3D60: fmul qword ptr [ecx + 0x690]
004A3D66: jmp 0x4a3dba
004A3D68: mov edx, dword ptr [0x839848]
004A3D6E: fmul qword ptr [edx + 0x6a0]
004A3D74: jmp 0x4a3dba
004A3D76: cmp esi, edi
004A3D78: jge 0x4a3dbe
004A3D7A: mov ecx, dword ptr [ebp + 0xc]
004A3D7D: mov eax, dword ptr [ecx]
004A3D7F: call dword ptr [eax + 0x2c]
004A3D82: cmp eax, 1
004A3D85: jne 0x4a3dbe
004A3D87: mov ecx, dword ptr [ebp + 0xc]
004A3D8A: mov edx, dword ptr [ecx]
004A3D8C: call dword ptr [edx + 0x80]
004A3D92: mov ecx, dword ptr [eax + 0x5a4]
004A3D98: fld qword ptr [esp + 0x18]
004A3D9C: cmp ecx, 1
004A3D9F: jne 0x4a3dae
004A3DA1: mov eax, dword ptr [0x839848]
004A3DA6: fmul qword ptr [eax + 0x698]
004A3DAC: jmp 0x4a3dba
004A3DAE: mov ecx, dword ptr [0x839848]
004A3DB4: fmul qword ptr [ecx + 0x6a8]
004A3DBA: fstp qword ptr [esp + 0x18]
004A3DBE: fld qword ptr [esp + 0x18]
004A3DC2: fcomp qword ptr [0x79b610]
004A3DC8: fnstsw ax
004A3DCA: test ah, 0x40
004A3DCD: je 0x4a3ddf
004A3DCF: mov dword ptr [esp + 0x18], 0
004A3DD7: mov dword ptr [esp + 0x1c], 0x3fe00000
004A3DDF: mov ecx, dword ptr [ebp + 0xc]
004A3DE2: call 0x5d4540
004A3DE7: mov edx, dword ptr [0x839848]
004A3DED: fcomp qword ptr [edx + 0x1368]
004A3DF3: fld qword ptr [esp + 0x18]
004A3DF7: fnstsw ax
004A3DF9: test ah, 0x41
004A3DFC: je 0x4a3e08
004A3DFE: fmul qword ptr [0x7a05d8]
004A3E04: fst qword ptr [esp + 0x18]
004A3E08: cmp dword ptr [ebp + 0x58], 0x40
004A3E0C: jge 0x4a3e13
004A3E0E: fstp qword ptr [ebp + 0x50]
004A3E11: jmp 0x4a3e35
004A3E13: mov ecx, dword ptr [ebp + 0xc]
004A3E16: fcomp qword ptr [ecx + 0x468]
004A3E1C: fnstsw ax
004A3E1E: test ah, 0x40
004A3E21: jne 0x4a3e35
004A3E23: mov edx, dword ptr [esp + 0x1c]
004A3E27: mov eax, dword ptr [ecx]
004A3E29: push edx
004A3E2A: mov edx, dword ptr [esp + 0x1c]
004A3E2E: push edx
004A3E2F: call dword ptr [eax + 0x4c8]
004A3E35: mov eax, dword ptr [esp + 0x38]
004A3E39: mov ecx, dword ptr [ebp + 0xc]
004A3E3C: cdq 
004A3E3D: and edx, 0xff
004A3E43: push 1
004A3E45: add eax, edx
004A3E47: sar eax, 8
004A3E4A: mov word ptr [esp + 0x1c], ax
004A3E4F: mov eax, dword ptr [esp + 0x40]
004A3E53: cdq 
004A3E54: and edx, 0xff
004A3E5A: add eax, edx
004A3E5C: sar eax, 8
004A3E5F: mov word ptr [esp + 0x1e], ax
004A3E64: mov eax, dword ptr [esp + 0x1c]
004A3E68: mov dword ptr [esp + 0x1c], eax
004A3E6C: mov edx, dword ptr [ecx]
004A3E6E: lea eax, [esp + 0x1c]
004A3E72: push eax
004A3E73: call dword ptr [edx + 0x4b8]
004A3E79: mov ecx, dword ptr [ebp + 0xc]
004A3E7C: mov esi, dword ptr [ecx + 0x4d4]
004A3E82: cmp esi, -1
004A3E85: jne 0x4a3f8b
004A3E8B: mov edx, dword ptr [ecx]
004A3E8D: lea eax, [esp + 0x50]
004A3E91: push eax
004A3E92: call dword ptr [edx + 0x48]
004A3E95: mov ecx, dword ptr [eax]
004A3E97: mov edx, dword ptr [ebp + 0x34]
004A3E9A: mov edi, dword ptr [ebp + 0x38]
004A3E9D: lea esi, [ebp + 0x34]
004A3EA0: sub ecx, edx
004A3EA2: mov edx, dword ptr [eax + 4]
004A3EA5: mov eax, dword ptr [eax + 8]
004A3EA8: mov dword ptr [esp + 0x18], ecx
004A3EAC: mov ecx, dword ptr [esi + 8]
004A3EAF: sub edx, edi
004A3EB1: fild dword ptr [esp + 0x18]
004A3EB5: mov dword ptr [esp + 0x1c], edx
004A3EB9: sub eax, ecx
004A3EBB: fild dword ptr [esp + 0x1c]
004A3EBF: mov dword ptr [esp + 0x20], eax
004A3EC3: sub esp, 8
004A3EC6: fild dword ptr [esp + 0x28]
004A3ECA: fld st(0)
004A3ECC: fmul st(1)
004A3ECE: fld st(2)
004A3ED0: fmul st(3)
004A3ED2: faddp st(1)
004A3ED4: fld st(3)
004A3ED6: fmul st(4)
004A3ED8: faddp st(1)
004A3EDA: fstp qword ptr [esp]
004A3EDD: fstp st(0)
004A3EDF: fstp st(0)
004A3EE1: fstp st(0)
004A3EE3: call 0x4ba410
004A3EE8: add esp, 8
004A3EEB: call 0x77f110
004A3EF0: cmp eax, 0x200
004A3EF5: jle 0x4a3f9f
004A3EFB: mov ecx, dword ptr [ebp + 0xc]
004A3EFE: mov edx, dword ptr [ecx]
004A3F00: call dword ptr [edx + 0x80]
004A3F06: mov dl, byte ptr [eax + 0xaa0]
004A3F0C: mov eax, dword ptr [esi]
004A3F0E: xor ecx, ecx
004A3F10: push 0
004A3F12: test dl, dl
004A3F14: cdq 
004A3F15: setne cl
004A3F18: and edx, 0xff
004A3F1E: push ecx
004A3F1F: add eax, edx
004A3F21: mov ecx, dword ptr [ebp + 0xc]
004A3F24: sar eax, 8
004A3F27: mov word ptr [esp + 0x20], ax
004A3F2C: mov eax, dword ptr [esi + 4]
004A3F2F: cdq 
004A3F30: and edx, 0xff
004A3F36: add eax, edx
004A3F38: sar eax, 8
004A3F3B: mov word ptr [esp + 0x22], ax
004A3F40: mov eax, dword ptr [esp + 0x20]
004A3F44: push eax
004A3F45: call 0x4c3000
004A3F4A: test al, al
004A3F4C: jne 0x4a3f82
004A3F4E: mov ecx, dword ptr [ebp + 0xc]
004A3F51: test ecx, ecx
004A3F53: jne 0x4a3f66
004A3F55: mov ecx, dword ptr [esp + 0x60]
004A3F59: pop edi
004A3F5A: pop esi
004A3F5B: pop ebp
004A3F5C: mov byte ptr [ecx], 1
004A3F5F: pop ebx
004A3F60: add esp, 0x4c
004A3F63: ret 0xc
004A3F66: mov edx, dword ptr [ecx]
004A3F68: push esi
004A3F69: call dword ptr [edx + 0x2ac]
004A3F6F: test al, al
004A3F71: jne 0x4a3f82
004A3F73: mov ecx, dword ptr [ebp + 0xc]
004A3F76: push 1
004A3F78: push 0
004A3F7A: mov eax, dword ptr [ecx]
004A3F7C: call dword ptr [eax + 0x410]
004A3F82: mov ecx, dword ptr [ebp + 0xc]
004A3F85: mov esi, dword ptr [ecx + 0x4d4]
004A3F8B: cmp esi, 8
004A3F8E: jne 0x4a3f92
004A3F90: mov esi, ebx
004A3F92: cmp esi, -1
004A3F95: je 0x4a3f9f
004A3F97: mov al, byte ptr [esp + 0x68]
004A3F9B: test al, al
004A3F9D: je 0x4a3fa1
004A3F9F: mov esi, ebx
004A3FA1: cmp esi, -1
004A3FA4: je 0x4a3fcf
004A3FA6: mov ecx, dword ptr [esp + 0x2c]
004A3FAA: push esi
004A3FAB: call 0x476ac0
004A3FB0: test eax, eax
004A3FB2: je 0x4a3fcf
004A3FB4: mov eax, dword ptr [eax + 0x44]
004A3FB7: cmp eax, -1
004A3FBA: je 0x4a3fcf
004A3FBC: mov edx, dword ptr [0xa35dec]
004A3FC2: mov eax, dword ptr [edx + eax*4]
004A3FC5: mov cl, byte ptr [eax + 0x1fd]
004A3FCB: test cl, cl
004A3FCD: jne 0x4a3fd7
004A3FCF: mov al, byte ptr [esp + 0x13]
004A3FD3: test al, al
004A3FD5: je 0x4a3fdf
004A3FD7: mov esi, ebx
004A3FD9: mov byte ptr [ebp + 0x64], 1
004A3FDD: jmp 0x4a3fe3
004A3FDF: mov byte ptr [ebp + 0x64], 0
004A3FE3: lea eax, [esi + ebx*8]
004A3FE6: mov byte ptr [ebp + 0x60], 0
004A3FEA: mov dword ptr [ebp + 0x58], eax
004A3FED: lea ecx, [eax + eax*2]
004A3FF0: mov al, byte ptr [ecx*4 + 0x7a0180]
004A3FF7: test al, al
004A3FF9: jne 0x4a4001
004A3FFB: lea edx, [ebx + ebx*8]
004A3FFE: mov dword ptr [ebp + 0x58], edx
004A4001: mov eax, dword ptr [ebp + 0x58]
004A4004: lea eax, [eax + eax*2]
004A4007: test byte ptr [eax*4 + 0x7a0188], 8
004A400F: je 0x4a45b7
004A4015: mov ecx, dword ptr [ebp + 0xc]
004A4018: lea edx, [esp + 0x14]
004A401C: push ecx
004A401D: push edx
004A401E: mov ecx, 0x8324e0
004A4023: call 0x548070
004A4028: mov ecx, eax
004A402A: call 0x476cc0
004A402F: test al, al
004A4031: jne 0x4a4059
004A4033: mov eax, dword ptr [ebp + 0xc]
004A4036: mov cl, byte ptr [eax + 0x76]
004A4039: test cl, cl
004A403B: jne 0x4a4059
004A403D: mov cl, byte ptr [eax + 0x7d]
004A4040: mov esi, 7
004A4045: test cl, cl
004A4047: jne 0x4a413d
004A404D: pop edi
004A404E: pop esi
004A404F: pop ebp
004A4050: xor al, al
004A4052: pop ebx
004A4053: add esp, 0x4c
004A4056: ret 0xc
004A4059: mov edi, dword ptr [ebp + 0xc]
004A405C: mov al, byte ptr [edi + 0x7d]
004A405F: test al, al
004A4061: je 0x4a3a44
004A4067: mov eax, esi
004A4069: mov edx, dword ptr [esp + 0x3c]
004A406D: and eax, 7
004A4070: mov ebx, dword ptr [esp + 0x38]
004A4074: push 1
004A4076: push 0
004A4078: lea ecx, [eax*8 + 0x851ac0]
004A407F: mov eax, dword ptr [eax*8 + 0x851ac0]
004A4086: mov ecx, dword ptr [ecx + 4]
004A4089: add ecx, edx
004A408B: mov edx, dword ptr [esp + 0x48]
004A408F: add eax, ebx
004A4091: mov dword ptr [esp + 0x48], edx
004A4095: mov dword ptr [esp + 0x40], eax
004A4099: mov dword ptr [esp + 0x44], ecx
004A409D: cdq 
004A409E: and edx, 0xff
004A40A4: add eax, edx
004A40A6: sar eax, 8
004A40A9: mov word ptr [esp + 0x70], ax
004A40AE: mov eax, ecx
004A40B0: cdq 
004A40B1: and edx, 0xff
004A40B7: add eax, edx
004A40B9: mov edx, dword ptr [esp + 0x30]
004A40BD: sar eax, 8
004A40C0: mov word ptr [esp + 0x72], ax
004A40C5: mov ecx, dword ptr [esp + 0x70]
004A40C9: push edx
004A40CA: lea eax, [esp + 0x20]
004A40CE: mov dword ptr [esp + 0x20], ecx
004A40D2: mov edi, dword ptr [edi]
004A40D4: push esi
004A40D5: push eax
004A40D6: mov ecx, 0x8324e0
004A40DB: call 0x548070
004A40E0: mov ecx, dword ptr [ebp + 0xc]
004A40E3: push eax
004A40E4: call dword ptr [edi + 0x194]
004A40EA: mov esi, eax
004A40EC: cmp esi, 7
004A40EF: jge 0x4a4106
004A40F1: mov ecx, dword ptr [ebp + 0xc]
004A40F4: mov edx, dword ptr [ecx]
004A40F6: call dword ptr [edx + 0x80]
004A40FC: mov cl, byte ptr [eax + 0xaa0]
004A4102: test cl, cl
004A4104: jne 0x4a413b
004A4106: cmp esi, 4
004A4109: je 0x4a4110
004A410B: cmp esi, 5
004A410E: jne 0x4a413d
004A4110: mov ecx, dword ptr [ebp + 0xc]
004A4113: mov eax, dword ptr [ecx]
004A4115: call dword ptr [eax + 0x80]
004A411B: mov cl, byte ptr [eax + 0xaf3]
004A4121: test cl, cl
004A4123: je 0x4a413d
004A4125: lea ecx, [esp + 0x14]
004A4129: push ecx
004A412A: mov ecx, 0x8324e0
004A412F: call 0x548070
004A4134: mov ecx, dword ptr [eax + 0x44]
004A4137: test ecx, ecx
004A4139: jne 0x4a413d
004A413B: xor esi, esi
004A413D: mov ecx, dword ptr [ebp + 0xc]
004A4140: mov al, byte ptr [ecx + 0x7d]
004A4143: test al, al
004A4145: je 0x4a3a44
004A414B: test esi, esi
004A414D: je 0x4a458c
004A4153: mov ebx, dword ptr [esp + 0x64]
004A4157: cmp esi, 3
004A415A: jne 0x4a41c7
004A415C: mov edx, dword ptr [esp + 0x14]
004A4160: lea eax, [esp + 0x68]
004A4164: push eax
004A4165: push ecx
004A4166: mov ecx, 0x8324e0
004A416B: mov dword ptr [esp + 0x70], edx
004A416F: call 0x55acd0
004A4174: mov eax, dword ptr [ebp + 0xc]
004A4177: or edi, 0xffffffff
004A417A: cmp esi, 5
004A417D: mov dword ptr [eax + 0x4d0], edi
004A4183: mov dword ptr [ebp + 0x58], edi
004A4186: mov ecx, dword ptr [0x852998]
004A418C: mov edx, dword ptr [0x85299c]
004A4192: mov eax, dword ptr [0x8529a0]
004A4197: mov dword ptr [esp + 0x38], ecx
004A419B: mov dword ptr [esp + 0x3c], edx
004A419F: mov dword ptr [esp + 0x40], eax
004A41A3: je 0x4a41ae
004A41A5: cmp esi, 4
004A41A8: jne 0x4a45d0
004A41AE: mov ecx, dword ptr [esp + 0x60]
004A41B2: push 1
004A41B4: push ebx
004A41B5: push ecx
004A41B6: mov ecx, ebp
004A41B8: call 0x4a2670
004A41BD: pop edi
004A41BE: pop esi
004A41BF: pop ebp
004A41C0: pop ebx
004A41C1: add esp, 0x4c
004A41C4: ret 0xc
004A41C7: cmp esi, 2
004A41CA: jne 0x4a41e9
004A41CC: mov ecx, dword ptr [esp + 0x64]
004A41D0: mov edx, dword ptr [esp + 0x60]
004A41D4: push 1
004A41D6: push ecx
004A41D7: push edx
004A41D8: mov ecx, ebp
004A41DA: call 0x4a2670
004A41DF: pop edi
004A41E0: pop esi
004A41E1: pop ebp
004A41E2: pop ebx
004A41E3: add esp, 0x4c
004A41E6: ret 0xc
004A41E9: cmp esi, 6
004A41EC: jne 0x4a4402
004A41F2: mov eax, dword ptr [ecx]
004A41F4: call dword ptr [eax + 0x80]
004A41FA: mov cl, byte ptr [eax + 0xaa0]
004A4200: test cl, cl
004A4202: jne 0x4a4174
004A4208: mov ecx, dword ptr [ebp + 0xc]
004A420B: test bl, bl
004A420D: je 0x4a4234
004A420F: mov dword ptr [ecx + 0x4d0], 0xffffffff
004A4219: mov edx, dword ptr [ebp + 0xc]
004A421C: mov eax, dword ptr [0xa40d2c]
004A4221: xor ecx, ecx
004A4223: add edx, 0x530
004A4229: mov dword ptr [edx], eax
004A422B: mov eax, dword ptr [esp + 0x54]
004A422F: jmp 0x4a4502
004A4234: mov edx, dword ptr [ecx]
004A4236: lea eax, [esp + 0x50]
004A423A: push eax
004A423B: call dword ptr [edx + 0x48]
004A423E: mov ecx, dword ptr [eax]
004A4240: mov edx, dword ptr [ebp + 0x34]
004A4243: mov edi, dword ptr [ebp + 0x38]
004A4246: sub ecx, edx
004A4248: mov edx, dword ptr [eax + 4]
004A424B: mov eax, dword ptr [eax + 8]
004A424E: mov dword ptr [esp + 0x2c], ecx
004A4252: mov ecx, dword ptr [ebp + 0x3c]
004A4255: sub edx, edi
004A4257: sub eax, ecx
004A4259: mov dword ptr [esp + 0x30], edx
004A425D: mov dword ptr [esp + 0x34], eax
004A4261: fild dword ptr [esp + 0x30]
004A4265: fild dword ptr [esp + 0x34]
004A4269: fild dword ptr [esp + 0x2c]
004A426D: sub esp, 8
004A4270: fld st(0)
004A4272: fmul st(1)
004A4274: fld st(2)
004A4276: fmul st(3)
004A4278: faddp st(1)
004A427A: fld st(3)
004A427C: fmul st(4)
004A427E: faddp st(1)
004A4280: fstp qword ptr [esp]
004A4283: fstp st(0)
004A4285: fstp st(0)
004A4287: fstp st(0)
004A4289: call 0x4ba410
004A428E: add esp, 8
004A4291: call 0x77f110
004A4296: mov ecx, dword ptr [0x839848]
004A429C: cmp eax, dword ptr [ecx + 0x1380]
004A42A2: jge 0x4a4391
004A42A8: mov ecx, dword ptr [ebp + 0xc]
004A42AB: add ecx, 0x88
004A42B1: mov edx, ecx
004A42B3: mov eax, dword ptr [edx]
004A42B5: mov dword ptr [esp + 0x44], eax
004A42B9: mov eax, dword ptr [edx + 4]
004A42BC: mov dword ptr [esp + 0x48], eax
004A42C0: mov eax, dword ptr [ebp + 0x3c]
004A42C3: mov edx, dword ptr [edx + 8]
004A42C6: sub eax, edx
004A42C8: cdq 
004A42C9: xor eax, edx
004A42CB: sub eax, edx
004A42CD: mov edx, dword ptr [0x8529d0]
004A42D3: add edx, edx
004A42D5: cmp eax, edx
004A42D7: jge 0x4a4391
004A42DD: mov eax, dword ptr [ecx]
004A42DF: mov dword ptr [esp + 0x44], eax
004A42E3: mov edx, dword ptr [ecx + 4]
004A42E6: mov dword ptr [esp + 0x48], edx
004A42EA: mov eax, dword ptr [ecx + 8]
004A42ED: lea ecx, [esp + 0x44]
004A42F1: mov dword ptr [esp + 0x4c], eax
004A42F5: push ecx
004A42F6: mov ecx, 0x8324e0
004A42FB: call 0x548000
004A4300: cmp dword ptr [eax + 0xec], 0xa
004A4307: je 0x4a4391
004A430D: mov eax, dword ptr [0x852998]
004A4312: mov ecx, dword ptr [ebp + 0x40]
004A4315: cmp ecx, eax
004A4317: jne 0x4a4333
004A4319: mov edx, dword ptr [ebp + 0x44]
004A431C: mov ecx, dword ptr [0x85299c]
004A4322: cmp edx, ecx
004A4324: jne 0x4a4333
004A4326: mov ecx, dword ptr [ebp + 0x48]
004A4329: mov edx, dword ptr [0x8529a0]
004A432F: cmp ecx, edx
004A4331: je 0x4a434b
004A4333: mov dword ptr [ebp + 0x40], eax
004A4336: mov edx, dword ptr [0x85299c]
004A433C: mov dword ptr [ebp + 0x44], edx
004A433F: mov eax, dword ptr [0x8529a0]
004A4344: mov dword ptr [ebp + 0x48], eax
004A4347: mov byte ptr [ebp + 0x63], 0
004A434B: mov ecx, dword ptr [ebp + 0xc]
004A434E: mov eax, dword ptr [ecx + 0x488]
004A4354: test eax, eax
004A4356: jne 0x4a4369
004A4358: mov edx, dword ptr [ecx]
004A435A: push 1
004A435C: push 0
004A435E: call dword ptr [edx + 0x410]
004A4364: jmp 0x4a4174
004A4369: call 0x4cd9b0
004A436E: mov ecx, dword ptr [ebp + 0xc]
004A4371: push 1
004A4373: push 0
004A4375: mov eax, dword ptr [ecx]
004A4377: call dword ptr [eax + 0x414]
004A437D: test al, al
004A437F: je 0x4a4174
004A4385: pop edi
004A4386: pop esi
004A4387: pop ebp
004A4388: mov al, 1
004A438A: pop ebx
004A438B: add esp, 0x4c
004A438E: ret 0xc
004A4391: lea ecx, [esp + 0x14]
004A4395: push ecx
004A4396: mov ecx, 0x8324e0
004A439B: call 0x548070
004A43A0: mov ecx, eax
004A43A2: mov eax, dword ptr [ecx + 0x140]
004A43A8: test ah, 1
004A43AB: je 0x4a43e5
004A43AD: mov edx, dword ptr [ebp + 0xc]
004A43B0: mov byte ptr [esp + 0x68], 1
004A43B5: add edx, 0x88
004A43BB: movsx edi, byte ptr [ecx + 0x11b]
004A43C2: mov eax, dword ptr [edx]
004A43C4: mov dword ptr [esp + 0x44], eax
004A43C8: mov eax, dword ptr [edx + 4]
004A43CB: mov dword ptr [esp + 0x48], eax
004A43CF: mov eax, dword ptr [edx + 8]
004A43D2: cdq 
004A43D3: idiv dword ptr [0x8529d0]
004A43D9: sub eax, edi
004A43DB: cdq 
004A43DC: xor eax, edx
004A43DE: sub eax, edx
004A43E0: cmp eax, 2
004A43E3: jg 0x4a43ea
004A43E5: mov byte ptr [esp + 0x68], 0
004A43EA: mov edx, dword ptr [esp + 0x68]
004A43EE: push edx
004A43EF: push 1
004A43F1: push 1
004A43F3: push 0x852998
004A43F8: call 0x476920
004A43FD: jmp 0x4a4174
004A4402: cmp esi, 1
004A4405: jne 0x4a44d1
004A440B: lea eax, [esp + 0x14]
004A440F: mov ecx, 0x8324e0
004A4414: push eax
004A4415: call 0x548070
004A441A: mov ecx, eax
004A441C: call 0x478740
004A4421: mov al, byte ptr [esp + 0x64]
004A4425: test al, al
004A4427: je 0x4a4450
004A4429: mov ecx, dword ptr [ebp + 0xc]
004A442C: mov edx, dword ptr [esp + 0x60]
004A4430: push 0
004A4432: push 0
004A4434: mov dword ptr [ecx + 0x4d0], 0xffffffff
004A443E: push edx
004A443F: mov ecx, ebp
004A4441: call 0x4a2670
004A4446: pop edi
004A4447: pop esi
004A4448: pop ebp
004A4449: pop ebx
004A444A: add esp, 0x4c
004A444D: ret 0xc
004A4450: mov eax, dword ptr [0x852998]
004A4455: mov ecx, dword ptr [ebp + 0x40]
004A4458: cmp ecx, eax
004A445A: jne 0x4a4476
004A445C: mov ecx, dword ptr [ebp + 0x44]
004A445F: mov edx, dword ptr [0x85299c]
004A4465: cmp ecx, edx
004A4467: jne 0x4a4476
004A4469: mov edx, dword ptr [ebp + 0x48]
004A446C: mov ecx, dword ptr [0x8529a0]
004A4472: cmp edx, ecx
004A4474: je 0x4a448e
004A4476: mov dword ptr [ebp + 0x40], eax
004A4479: mov eax, dword ptr [0x85299c]
004A447E: mov dword ptr [ebp + 0x44], eax
004A4481: mov ecx, dword ptr [0x8529a0]
004A4487: mov dword ptr [ebp + 0x48], ecx
004A448A: mov byte ptr [ebp + 0x63], 0
004A448E: mov ecx, dword ptr [ebp + 0xc]
004A4491: mov eax, dword ptr [ecx + 0x488]
004A4497: test eax, eax
004A4499: jne 0x4a44b3
004A449B: mov edx, dword ptr [ecx]
004A449D: push 1
004A449F: push 0
004A44A1: call dword ptr [edx + 0x410]
004A44A7: pop edi
004A44A8: pop esi
004A44A9: pop ebp
004A44AA: xor al, al
004A44AC: pop ebx
004A44AD: add esp, 0x4c
004A44B0: ret 0xc
004A44B3: call 0x4cd9b0
004A44B8: mov ecx, dword ptr [ebp + 0xc]
004A44BB: push 1
004A44BD: push 0
004A44BF: mov eax, dword ptr [ecx]
004A44C1: call dword ptr [eax + 0x414]
004A44C7: pop edi
004A44C8: pop esi
004A44C9: pop ebp
004A44CA: pop ebx
004A44CB: add esp, 0x4c
004A44CE: ret 0xc
004A44D1: cmp esi, 7
004A44D4: jne 0x4a4174
004A44DA: mov al, byte ptr [esp + 0x64]
004A44DE: test al, al
004A44E0: je 0x4a4522
004A44E2: mov dword ptr [ecx + 0x4d0], 0xffffffff
004A44EC: mov edx, dword ptr [ebp + 0xc]
004A44EF: mov eax, dword ptr [0xa40d2c]
004A44F4: xor ecx, ecx
004A44F6: add edx, 0x530
004A44FC: mov dword ptr [edx], eax
004A44FE: mov eax, dword ptr [esp + 0x54]
004A4502: mov dword ptr [edx + 4], eax
004A4505: push 0
004A4507: push 0
004A4509: mov dword ptr [edx + 8], ecx
004A450C: mov ecx, dword ptr [esp + 0x68]
004A4510: push ecx
004A4511: mov ecx, ebp
004A4513: call 0x4a2670
004A4518: pop edi
004A4519: pop esi
004A451A: pop ebp
004A451B: pop ebx
004A451C: add esp, 0x4c
004A451F: ret 0xc
004A4522: mov eax, dword ptr [0x852998]
004A4527: mov edx, dword ptr [ebp + 0x40]
004A452A: cmp edx, eax
004A452C: jne 0x4a4548
004A452E: mov edx, dword ptr [ebp + 0x44]
004A4531: mov esi, dword ptr [0x85299c]
004A4537: cmp edx, esi
004A4539: jne 0x4a4548
004A453B: mov edx, dword ptr [ebp + 0x48]
004A453E: mov esi, dword ptr [0x8529a0]
004A4544: cmp edx, esi
004A4546: je 0x4a4560
004A4548: mov dword ptr [ebp + 0x40], eax
004A454B: mov eax, dword ptr [0x85299c]
004A4550: mov dword ptr [ebp + 0x44], eax
004A4553: mov edx, dword ptr [0x8529a0]
004A4559: mov dword ptr [ebp + 0x48], edx
004A455C: mov byte ptr [ebp + 0x63], 0
004A4560: mov eax, dword ptr [ecx + 0x488]
004A4566: test eax, eax
004A4568: je 0x4a3a38
004A456E: call 0x4cd9b0
004A4573: mov ecx, dword ptr [ebp + 0xc]
004A4576: push 1
004A4578: push 0
004A457A: mov edx, dword ptr [ecx]
004A457C: call dword ptr [edx + 0x414]
004A4582: pop edi
004A4583: pop esi
004A4584: pop ebp
004A4585: pop ebx
004A4586: add esp, 0x4c
004A4589: ret 0xc
004A458C: lea esi, [ecx + 0x4d8]
004A4592: lea edi, [ecx + 0x4d0]
004A4598: mov ecx, 0x16
004A459D: rep movsd dword ptr es:[edi], dword ptr [esi]
004A459F: mov edx, dword ptr [ebp + 0xc]
004A45A2: or edi, 0xffffffff
004A45A5: mov dword ptr [edx + 0x528], edi
004A45AB: mov eax, dword ptr [ebp + 0xc]
004A45AE: mov byte ptr [eax + 0x57b], 1
004A45B5: jmp 0x4a45d0
004A45B7: mov eax, dword ptr [ebp + 0xc]
004A45BA: mov ecx, 0x17
004A45BF: lea esi, [eax + 0x4d4]
004A45C5: lea edi, [eax + 0x4d0]
004A45CB: rep movsd dword ptr es:[edi], dword ptr [esi]
004A45CD: or edi, 0xffffffff
004A45D0: mov ecx, dword ptr [ebp + 0xc]
004A45D3: lea esi, [ebp + 0x40]
004A45D6: mov dword ptr [ecx + 0x52c], edi
004A45DC: mov eax, dword ptr [esp + 0x38]
004A45E0: cdq 
004A45E1: and edx, 0xff
004A45E7: add eax, edx
004A45E9: sar eax, 8
004A45EC: mov word ptr [esp + 0x68], ax
004A45F1: mov eax, dword ptr [esp + 0x3c]
004A45F5: cdq 
004A45F6: and edx, 0xff
004A45FC: add eax, edx
004A45FE: mov edx, dword ptr [ebp + 0xc]
004A4601: sar eax, 8
004A4604: mov word ptr [esp + 0x6a], ax
004A4609: mov eax, dword ptr [esp + 0x68]
004A460D: mov dword ptr [edx + 0x450], eax
004A4613: mov ecx, dword ptr [ebp + 0xc]
004A4616: mov byte ptr [ecx + 0x57a], 0
004A461D: mov dword ptr [ebp + 0x5c], 0
004A4624: mov eax, dword ptr [0x852998]
004A4629: mov ecx, dword ptr [esi]
004A462B: cmp ecx, eax
004A462D: jne 0x4a4649
004A462F: mov edx, dword ptr [esi + 4]
004A4632: mov ecx, dword ptr [0x85299c]
004A4638: cmp edx, ecx
004A463A: jne 0x4a4649
004A463C: mov ecx, dword ptr [esi + 8]
004A463F: mov edx, dword ptr [0x8529a0]
004A4645: cmp ecx, edx
004A4647: je 0x4a4667
004A4649: mov edx, esi
004A464B: mov dword ptr [edx], eax
004A464D: mov eax, dword ptr [0x85299c]
004A4652: mov dword ptr [edx + 4], eax
004A4655: mov ecx, dword ptr [0x8529a0]
004A465B: mov byte ptr [ebp + 0x63], 0
004A465F: mov dword ptr [edx + 8], ecx
004A4662: mov eax, dword ptr [0x852998]
004A4667: mov ecx, dword ptr [esp + 0x38]
004A466B: mov edx, dword ptr [esp + 0x40]
004A466F: cmp ecx, eax
004A4671: mov eax, dword ptr [esp + 0x3c]
004A4675: jne 0x4a4687
004A4677: cmp eax, dword ptr [0x85299c]
004A467D: jne 0x4a4687
004A467F: cmp edx, dword ptr [0x8529a0]
004A4685: je 0x4a46fe
004A4687: mov ebx, esi
004A4689: mov byte ptr [ebp + 0x63], 1
004A468D: mov dword ptr [ebx], ecx
004A468F: mov ecx, 0x8324e0
004A4694: mov dword ptr [ebx + 4], eax
004A4697: lea eax, [esp + 0x38]
004A469B: mov dword ptr [ebx + 8], edx
004A469E: mov edx, dword ptr [ebp + 0xc]
004A46A1: push edx
004A46A2: push eax
004A46A3: call 0x548000
004A46A8: mov ecx, eax
004A46AA: call 0x476cc0
004A46AF: test al, al
004A46B1: je 0x4a46d7
004A46B3: mov ecx, dword ptr [ebp + 0xc]
004A46B6: mov al, byte ptr [ecx + 0x76]
004A46B9: test al, al
004A46BB: jne 0x4a46d7
004A46BD: lea edx, [esp + 0x38]
004A46C1: push 1
004A46C3: push edx
004A46C4: mov ecx, ebp
004A46C6: call 0x4a0bc0
004A46CB: pop edi
004A46CC: pop esi
004A46CD: pop ebp
004A46CE: xor al, al
004A46D0: pop ebx
004A46D1: add esp, 0x4c
004A46D4: ret 0xc
004A46D7: mov eax, dword ptr [ebp + 0xc]
004A46DA: mov cl, byte ptr [eax + 0x7d]
004A46DD: test cl, cl
004A46DF: je 0x4a46fe
004A46E1: mov ecx, dword ptr [0x852998]
004A46E7: mov dword ptr [esi], ecx
004A46E9: mov edx, dword ptr [0x85299c]
004A46EF: mov dword ptr [esi + 4], edx
004A46F2: mov eax, dword ptr [0x8529a0]
004A46F7: mov dword ptr [esi + 8], eax
004A46FA: mov byte ptr [ebp + 0x63], 0
004A46FE: mov ecx, dword ptr [ebp + 0xc]
004A4701: mov dword ptr [ebp + 0x58], edi
004A4704: push 0
004A4706: push 0
004A4708: mov dword ptr [ecx + 0x4d0], edi
004A470E: mov ecx, dword ptr [ebp + 0xc]
004A4711: mov edx, dword ptr [ecx]
004A4713: call dword ptr [edx + 0x4c8]
004A4719: pop edi
004A471A: pop esi
004A471B: pop ebp
004A471C: xor al, al
004A471E: pop ebx
004A471F: add esp, 0x4c
004A4722: ret 0xc
004A4725: nop 
004A4726: nop 
004A4727: nop 
004A4728: nop 
004A4729: nop 
004A472A: nop 
004A472B: nop 
004A472C: nop 
004A472D: nop 
004A472E: nop 
004A472F: nop 
004A4730: ret 
004A4731: nop 
004A4732: nop 
004A4733: nop 
004A4734: nop 
004A4735: nop 
004A4736: nop 
004A4737: nop 
004A4738: nop 
004A4739: nop 
004A473A: nop 
004A473B: nop 
004A473C: nop 
004A473D: nop 
004A473E: nop 
004A473F: nop 