004A1F8D: mov ecx, dword ptr [ebp + 0x5c]
004A1F90: mov eax, dword ptr [esp + 0x3c]
004A1F94: inc ecx
004A1F95: cmp eax, 7
004A1F98: mov dword ptr [ebp + 0x5c], ecx
004A1F9B: jg 0x4a166a
004A1FA1: mov eax, dword ptr [esp + 0x3c]
004A1FA5: xor edi, edi
004A1FA7: cmp eax, edi
004A1FA9: mov dword ptr [ebp + 0x4c], eax
004A1FAC: jle 0x4a263a
004A1FB2: mov eax, dword ptr [ebp + 0x58]
004A1FB5: cmp eax, -1
004A1FB8: jle 0x4a263a
004A1FBE: lea ecx, [eax + eax*2]
004A1FC1: lea eax, [ecx*4 + 0x7a0180]
004A1FC8: mov cl, byte ptr [ebp + 0x60]
004A1FCB: test cl, cl
004A1FCD: je 0x4a230e
004A1FD3: movsx eax, byte ptr [eax + 1]
004A1FD7: jmp 0x4a2311
004A1FDC: mov edi, dword ptr [ebp + 0xc]
004A1FDF: lea esi, [ebp + 0x40]
004A1FE2: lea eax, [edi + 0x88]
004A1FE8: mov ecx, dword ptr [edi + 0x88]
004A1FEE: mov edx, dword ptr [eax + 4]
004A1FF1: mov eax, dword ptr [eax + 8]
004A1FF4: mov dword ptr [esp + 0x64], eax
004A1FF8: mov eax, dword ptr [esi]
004A1FFA: sub eax, ecx
004A1FFC: mov ecx, dword ptr [esi + 4]
004A1FFF: sub ecx, edx
004A2001: cdq 
004A2002: mov ebx, eax
004A2004: mov eax, ecx
004A2006: xor ebx, edx
004A2008: sub ebx, edx
004A200A: cdq 
004A200B: xor eax, edx
004A200D: sub eax, edx
004A200F: add ebx, eax
004A2011: mov dword ptr [esp + 0x34], ebx
004A2015: fild dword ptr [esp + 0x34]
004A2019: fmul qword ptr [0x7a05d0]
004A201F: fsubr qword ptr [0x79a708]
004A2025: fmul qword ptr [0x7a05c8]
004A202B: call 0x77f110
004A2030: mov ebx, dword ptr [esp + 0x3c]
004A2034: mov byte ptr [edi + 0x5a0], 1
004A203B: mov ecx, dword ptr [ebp + 0xc]
004A203E: add ebx, eax
004A2040: mov dword ptr [esp + 0x3c], ebx
004A2044: mov byte ptr [ecx + 0x5a1], 0
004A204B: mov ebx, dword ptr [ebp + 0xc]
004A204E: lea edx, [ebx + 0x88]
004A2054: mov eax, dword ptr [ebx + 0x88]
004A205A: mov ecx, dword ptr [edx + 4]
004A205D: mov edx, dword ptr [edx + 8]
004A2060: mov dword ptr [esp + 0x64], edx
004A2064: cdq 
004A2065: and edx, 0xff
004A206B: add eax, edx
004A206D: mov edi, eax
004A206F: mov eax, ecx
004A2071: cdq 
004A2072: and edx, 0xff
004A2078: add eax, edx
004A207A: sar eax, 8
004A207D: mov word ptr [esp + 0x36], ax
004A2082: mov eax, dword ptr [esi]
004A2084: cdq 
004A2085: and edx, 0xff
004A208B: add eax, edx
004A208D: mov ecx, eax
004A208F: mov eax, dword ptr [esi + 4]
004A2092: cdq 
004A2093: and edx, 0xff
004A2099: add eax, edx
004A209B: sar edi, 8
004A209E: sar ecx, 8
004A20A1: sar eax, 8
004A20A4: cmp di, cx
004A20A7: jne 0x4a20b0
004A20A9: cmp word ptr [esp + 0x36], ax
004A20AE: je 0x4a20e4
004A20B0: mov eax, dword ptr [ebx]
004A20B2: push 0
004A20B4: mov ecx, ebx
004A20B6: call dword ptr [eax + 0x11c]
004A20BC: mov ecx, dword ptr [ebp + 0xc]
004A20BF: push esi
004A20C0: mov edx, dword ptr [ecx]
004A20C2: call dword ptr [edx + 0x19c]
004A20C8: mov ecx, dword ptr [ebp + 0xc]
004A20CB: push 0
004A20CD: mov eax, dword ptr [ecx]
004A20CF: call dword ptr [eax + 0x1b4]
004A20D5: mov ecx, dword ptr [ebp + 0xc]
004A20D8: push 1
004A20DA: mov edx, dword ptr [ecx]
004A20DC: call dword ptr [edx + 0x11c]
004A20E2: jmp 0x4a2112
004A20E4: mov al, byte ptr [ebx + 0x74]
004A20E7: mov byte ptr [ebx + 0x74], 0
004A20EB: mov ecx, dword ptr [ebp + 0xc]
004A20EE: push esi
004A20EF: mov byte ptr [esp + 0x17], al
004A20F3: mov edx, dword ptr [ecx]
004A20F5: call dword ptr [edx + 0x19c]
004A20FB: mov ecx, dword ptr [ebp + 0xc]
004A20FE: push 0
004A2100: mov eax, dword ptr [ecx]
004A2102: call dword ptr [eax + 0x1b4]
004A2108: mov ecx, dword ptr [ebp + 0xc]
004A210B: mov dl, byte ptr [esp + 0x13]
004A210F: mov byte ptr [ecx + 0x74], dl
004A2112: mov eax, dword ptr [0x852998]
004A2117: mov ecx, dword ptr [esi]
004A2119: cmp ecx, eax
004A211B: jne 0x4a2137
004A211D: mov ecx, dword ptr [esi + 4]
004A2120: mov edx, dword ptr [0x85299c]
004A2126: cmp ecx, edx
004A2128: jne 0x4a2137
004A212A: mov edx, dword ptr [esi + 8]
004A212D: mov ecx, dword ptr [0x8529a0]
004A2133: cmp edx, ecx
004A2135: je 0x4a2150
004A2137: mov ecx, esi
004A2139: mov dword ptr [ecx], eax
004A213B: mov edx, dword ptr [0x85299c]
004A2141: mov dword ptr [ecx + 4], edx
004A2144: mov eax, dword ptr [0x8529a0]
004A2149: mov byte ptr [ebp + 0x63], 0
004A214D: mov dword ptr [ecx + 8], eax
004A2150: mov eax, dword ptr [ebp + 0xc]
004A2153: mov dword ptr [ebp + 0x58], 0xffffffff
004A215A: mov dword ptr [ebp + 0x5c], 0
004A2161: mov byte ptr [esp + 0x13], 0
004A2166: mov ecx, dword ptr [eax + 0x494]
004A216C: test ecx, ecx
004A216E: je 0x4a224d
004A2174: mov edx, dword ptr [ecx]
004A2176: push eax
004A2177: lea eax, [esp + 0x60]
004A217B: push eax
004A217C: call dword ptr [edx + 0x4c]
004A217F: mov ecx, eax
004A2181: mov eax, dword ptr [ecx]
004A2183: cdq 
004A2184: and edx, 0xff
004A218A: add eax, edx
004A218C: mov edi, eax
004A218E: mov eax, dword ptr [ecx + 4]
004A2191: mov ecx, dword ptr [ebp + 0xc]
004A2194: cdq 
004A2195: and edx, 0xff
004A219B: add eax, edx
004A219D: mov edx, dword ptr [ecx]
004A219F: mov ebx, eax
004A21A1: lea eax, [esp + 0x24]
004A21A5: push eax
004A21A6: sar edi, 8
004A21A9: sar ebx, 8
004A21AC: call dword ptr [edx + 0x1a0]
004A21B2: cmp word ptr [eax], di
004A21B5: jne 0x4a224d
004A21BB: cmp word ptr [eax + 2], bx
004A21BF: jne 0x4a224d
004A21C5: mov ecx, dword ptr [ebp + 0xc]
004A21C8: lea eax, [esp + 0x5c]
004A21CC: push ecx
004A21CD: push eax
004A21CE: mov edx, dword ptr [ecx]
004A21D0: call dword ptr [edx + 0x4c]
004A21D3: mov eax, dword ptr [eax + 8]
004A21D6: mov ecx, dword ptr [ebp + 0x3c]
004A21D9: sub eax, ecx
004A21DB: mov ecx, dword ptr [0x8529d0]
004A21E1: cdq 
004A21E2: xor eax, edx
004A21E4: sub eax, edx
004A21E6: lea edx, [ecx + ecx]
004A21E9: cmp eax, edx
004A21EB: jge 0x4a224d
004A21ED: mov ecx, dword ptr [0x852998]
004A21F3: lea eax, [ebp + 0x34]
004A21F6: mov byte ptr [esp + 0x13], 1
004A21FB: mov dword ptr [eax], ecx
004A21FD: mov edx, dword ptr [0x85299c]
004A2203: mov dword ptr [eax + 4], edx
004A2206: mov ecx, dword ptr [0x8529a0]
004A220C: mov dword ptr [eax + 8], ecx
004A220F: mov eax, dword ptr [0x852998]
004A2214: cmp dword ptr [esi], eax
004A2216: jne 0x4a2232
004A2218: mov edx, dword ptr [esi + 4]
004A221B: mov ecx, dword ptr [0x85299c]
004A2221: cmp edx, ecx
004A2223: jne 0x4a2232
004A2225: mov ecx, dword ptr [esi + 8]
004A2228: mov edx, dword ptr [0x8529a0]
004A222E: cmp ecx, edx
004A2230: je 0x4a2249
004A2232: mov dword ptr [esi], eax
004A2234: mov edx, dword ptr [0x85299c]
004A223A: mov dword ptr [esi + 4], edx
004A223D: mov eax, dword ptr [0x8529a0]
004A2242: mov dword ptr [esi + 8], eax
004A2245: mov byte ptr [ebp + 0x63], 0
004A2249: mov byte ptr [ebp + 0x63], 0
004A224D: mov ecx, dword ptr [ebp + 0xc]
004A2250: push 2
004A2252: mov edx, dword ptr [ecx]
004A2254: call dword ptr [edx + 0x174]
004A225A: mov ecx, dword ptr [ebp + 0xc]
004A225D: mov al, byte ptr [ecx + 0x7d]
004A2260: test al, al
004A2262: je 0x4a22cd
004A2264: mov al, byte ptr [ecx + 0x76]
004A2267: test al, al
004A2269: jne 0x4a22cd
004A226B: mov al, byte ptr [ecx + 0x7a]
004A226E: test al, al
004A2270: jne 0x4a22cd
004A2272: mov al, byte ptr [esp + 0x13]
004A2276: test al, al
004A2278: je 0x4a22be
004A227A: call 0x4cd9b0
004A227F: mov eax, dword ptr [ebp + 0xc]
004A2282: mov dword ptr [eax + 0x4d0], 0xffffffff
004A228C: mov ecx, dword ptr [ebp + 0xc]
004A228F: mov edx, dword ptr [ecx]
004A2291: call dword ptr [edx + 0x16c]
004A2297: cmp eax, 2
004A229A: jne 0x4a22be
004A229C: mov ecx, dword ptr [ebp + 0xc]
004A229F: push 1
004A22A1: push 0
004A22A3: mov eax, dword ptr [ecx]
004A22A5: call dword ptr [eax + 0x414]
004A22AB: test al, al
004A22AD: je 0x4a22be
004A22AF: pop edi
004A22B0: pop esi
004A22B1: pop ebp
004A22B2: mov al, 1
004A22B4: pop ebx
004A22B5: add esp, 0xe4
004A22BB: ret 4
004A22BE: mov ecx, dword ptr [ebp + 0xc]
004A22C1: mov edx, dword ptr [ecx]
004A22C3: call dword ptr [edx + 0x490]
004A22C9: test al, al
004A22CB: je 0x4a22dc
004A22CD: pop edi
004A22CE: pop esi
004A22CF: pop ebp
004A22D0: mov al, 1
004A22D2: pop ebx
004A22D3: add esp, 0xe4
004A22D9: ret 4
004A22DC: mov eax, dword ptr [ebp + 0xc]
004A22DF: mov cl, byte ptr [eax + 0x7d]
004A22E2: test cl, cl
004A22E4: jne 0x4a1fa1
004A22EA: pop edi
004A22EB: pop esi
004A22EC: pop ebp
004A22ED: xor al, al
004A22EF: pop ebx
004A22F0: add esp, 0xe4
004A22F6: ret 4
004A22F9: mov dword ptr [ecx + 0x4d0], edi
004A22FF: pop edi
004A2300: pop esi
004A2301: pop ebp
004A2302: xor al, al
004A2304: pop ebx
004A2305: add esp, 0xe4
004A230B: ret 4
004A230E: movsx eax, byte ptr [eax]
004A2311: mov edx, dword ptr [ebp + 0x5c]
004A2314: shl eax, 4
004A2317: lea ecx, [edx + edx*2]
004A231A: mov eax, dword ptr [eax + 0x7a00a0]
004A2320: mov esi, dword ptr [eax + ecx*4]
004A2323: lea ecx, [eax + ecx*4]
004A2326: cmp esi, edi
004A2328: mov eax, dword ptr [ecx + 4]
004A232B: mov dword ptr [esp + 0x8c], esi
004A2332: mov dword ptr [esp + 0x90], eax
004A2339: jne 0x4a2347
004A233B: cmp eax, edi
004A233D: jne 0x4a2347
004A233F: cmp edx, edi
004A2341: jne 0x4a263a
004A2347: mov eax, dword ptr [ebp + 0xc]
004A234A: add eax, 0x88
004A234F: mov edx, eax
004A2351: mov esi, dword ptr [edx]
004A2353: mov dword ptr [esp + 0x80], esi
004A235A: mov esi, dword ptr [edx + 4]
004A235D: mov dword ptr [esp + 0x84], esi
004A2364: mov edx, dword ptr [edx + 8]
004A2367: mov dword ptr [esp + 0x88], edx
004A236E: mov ecx, dword ptr [ecx + 8]
004A2371: mov dword ptr [esp + 0x34], ecx
004A2375: mov esi, dword ptr [eax]
004A2377: mov ebx, dword ptr [eax + 4]
004A237A: mov edx, dword ptr [eax + 8]
004A237D: lea eax, [esp + 0x34]
004A2381: mov dword ptr [esp + 0x64], edx
004A2385: lea ecx, [esp + 0x8c]
004A238C: push eax
004A238D: lea edx, [esp + 0xb0]
004A2394: push ecx
004A2395: push edx
004A2396: mov ecx, ebp
004A2398: call 0x4a4740
004A239D: mov ecx, dword ptr [eax]
004A239F: mov edx, dword ptr [ebp + 0xc]
004A23A2: mov eax, dword ptr [eax + 4]
004A23A5: add edx, 0x88
004A23AB: sub eax, ebx
004A23AD: sub ecx, esi
004A23AF: mov ebx, edx
004A23B1: mov dword ptr [esp + 0xc4], ecx
004A23B8: mov dword ptr [esp + 0xc8], eax
004A23BF: mov dword ptr [esp + 0xcc], edi
004A23C6: mov edx, dword ptr [ebx]
004A23C8: add ecx, edx
004A23CA: mov esi, dword ptr [ebx + 4]
004A23CD: add eax, esi
004A23CF: mov ebx, dword ptr [ebx + 8]
004A23D2: mov dword ptr [esp + 0x78], eax
004A23D6: lea eax, [esp + 0x74]
004A23DA: mov dword ptr [esp + 0x74], ecx
004A23DE: push eax
004A23DF: mov ecx, 0x8324e0
004A23E4: mov dword ptr [esp + 0x80], ebx
004A23EB: call 0x548000
004A23F0: fild dword ptr [ebp + 0x4c]
004A23F3: push ecx
004A23F4: lea ecx, [esp + 0xc8]
004A23FB: lea edx, [esp + 0xbc]
004A2402: mov esi, eax
004A2404: fmul qword ptr [0x7a05c0]
004A240A: mov dword ptr [esp + 0xbc], edi
004A2411: mov dword ptr [esp + 0xc0], edi
004A2418: mov dword ptr [esp + 0xc4], edi
004A241F: fstp dword ptr [esp]
004A2422: push ecx
004A2423: lea ecx, [esp + 0x64]
004A2427: call 0x7220c0
004A242C: mov edi, dword ptr [esp + 0x80]
004A2433: mov edx, eax
004A2435: mov eax, dword ptr [edx]
004A2437: mov dword ptr [esp + 0xc4], eax
004A243E: add eax, edi
004A2440: mov ecx, dword ptr [edx + 4]
004A2443: mov edi, dword ptr [esp + 0x84]
004A244A: mov dword ptr [esp + 0xc8], ecx
004A2451: add ecx, edi
004A2453: mov edx, dword ptr [edx + 8]
004A2456: mov edi, dword ptr [esp + 0x88]
004A245D: mov dword ptr [esp + 0x24], eax
004A2461: mov dword ptr [esp + 0xcc], edx
004A2468: lea eax, [esp + 0x80]
004A246F: add edx, edi
004A2471: mov dword ptr [esp + 0x28], ecx
004A2475: push eax
004A2476: mov ecx, 0x8324e0
004A247B: mov dword ptr [esp + 0x30], edx
004A247F: call 0x548000
004A2484: mov edi, eax
004A2486: lea ecx, [esp + 0x24]
004A248A: mov dword ptr [esp + 0x6c], edi
004A248E: push ecx
004A248F: mov ecx, 0x8324e0
004A2494: call 0x548000
004A2499: mov edx, dword ptr [ebp + 0xc]
004A249C: add edx, 0x88
004A24A2: cmp eax, esi
004A24A4: mov ebx, edx
004A24A6: mov ecx, dword ptr [ebx]
004A24A8: mov dword ptr [esp + 0x18], ecx
004A24AC: mov edx, dword ptr [ebx + 4]
004A24AF: mov dword ptr [esp + 0x1c], edx
004A24B3: mov ebx, dword ptr [ebx + 8]
004A24B6: mov dword ptr [esp + 0x20], ebx
004A24BA: je 0x4a24dc
004A24BC: cmp eax, edi
004A24BE: je 0x4a24dc
004A24C0: cmp dword ptr [ebp + 0x4c], 3
004A24C4: jle 0x4a24f4
004A24C6: mov ecx, dword ptr [esp + 0x74]
004A24CA: mov edx, dword ptr [esp + 0x78]
004A24CE: mov ebx, dword ptr [esp + 0x7c]
004A24D2: mov dword ptr [esp + 0x18], ecx
004A24D6: mov dword ptr [esp + 0x1c], edx
004A24DA: jmp 0x4a24f0
004A24DC: mov ecx, dword ptr [esp + 0x24]
004A24E0: mov edx, dword ptr [esp + 0x28]
004A24E4: mov ebx, dword ptr [esp + 0x2c]
004A24E8: mov dword ptr [esp + 0x18], ecx
004A24EC: mov dword ptr [esp + 0x1c], edx
004A24F0: mov dword ptr [esp + 0x20], ebx
004A24F4: lea eax, [esp + 0xd0]
004A24FB: mov dword ptr [esp + 0xd0], ecx
004A2502: push eax
004A2503: mov ecx, 0x8324e0
004A2508: mov dword ptr [esp + 0xd8], edx
004A250F: mov dword ptr [esp + 0xdc], ebx
004A2516: call 0x548000
004A251B: mov ecx, dword ptr [ebp + 0xc]
004A251E: mov dword ptr [esp + 0x54], eax
004A2522: lea edx, [ecx + 0x88]
004A2528: mov eax, dword ptr [ecx + 0x88]
004A252E: mov edi, dword ptr [edx + 4]
004A2531: mov edx, dword ptr [edx + 8]
004A2534: mov dword ptr [esp + 0x64], edx
004A2538: cdq 
004A2539: and edx, 0xff
004A253F: add eax, edx
004A2541: mov esi, eax
004A2543: mov eax, edi
004A2545: cdq 
004A2546: and edx, 0xff
004A254C: add eax, edx
004A254E: mov edi, eax
004A2550: mov eax, dword ptr [esp + 0x18]
004A2554: cdq 
004A2555: and edx, 0xff
004A255B: add eax, edx
004A255D: mov ebx, eax
004A255F: mov eax, dword ptr [esp + 0x1c]
004A2563: cdq 
004A2564: and edx, 0xff
004A256A: add eax, edx
004A256C: sar esi, 8
004A256F: sar ebx, 8
004A2572: sar edi, 8
004A2575: sar eax, 8
004A2578: cmp bx, si
004A257B: jne 0x4a2586
004A257D: cmp ax, di
004A2580: je 0x4a2607
004A2586: mov eax, dword ptr [ecx]
004A2588: push 0
004A258A: call dword ptr [eax + 0x11c]
004A2590: mov ecx, dword ptr [ebp + 0xc]
004A2593: lea eax, [esp + 0x18]
004A2597: push eax
004A2598: mov edx, dword ptr [ecx]
004A259A: call dword ptr [edx + 0x19c]
004A25A0: mov ecx, dword ptr [esp + 0x6c]
004A25A4: mov eax, dword ptr [esp + 0x54]
004A25A8: movsx edx, byte ptr [ecx + 0x11b]
004A25AF: movsx esi, byte ptr [eax + 0x11b]
004A25B6: sub edx, 4
004A25B9: cmp esi, edx
004A25BB: mov edx, 0x100
004A25C0: jne 0x4a25d1
004A25C2: test dword ptr [eax + 0x140], edx
004A25C8: je 0x4a25d9
004A25CA: mov esi, dword ptr [ebp + 0xc]
004A25CD: mov byte ptr [esi + 0x79], 1
004A25D1: test dword ptr [eax + 0x140], edx
004A25D7: jne 0x4a25e8
004A25D9: test dword ptr [ecx + 0x140], edx
004A25DF: je 0x4a25e8
004A25E1: mov eax, dword ptr [ebp + 0xc]
004A25E4: mov byte ptr [eax + 0x79], 0
004A25E8: mov ebp, dword ptr [ebp + 0xc]
004A25EB: push 1
004A25ED: mov ecx, ebp
004A25EF: mov edx, dword ptr [ebp]
004A25F2: call dword ptr [edx + 0x11c]
004A25F8: pop edi
004A25F9: pop esi
004A25FA: pop ebp
004A25FB: xor al, al
004A25FD: pop ebx
004A25FE: add esp, 0xe4
004A2604: ret 4
004A2607: mov bl, byte ptr [ecx + 0x74]
004A260A: mov byte ptr [ecx + 0x74], 0
004A260E: mov ecx, dword ptr [ebp + 0xc]
004A2611: lea edx, [esp + 0x18]
004A2615: push edx
004A2616: mov eax, dword ptr [ecx]
004A2618: call dword ptr [eax + 0x19c]
004A261E: mov eax, dword ptr [ebp + 0xc]
004A2621: pop edi
004A2622: pop esi
004A2623: pop ebp
004A2624: mov byte ptr [eax + 0x74], bl
004A2627: xor al, al
004A2629: pop ebx
004A262A: add esp, 0xe4
004A2630: ret 4
004A2633: mov dword ptr [ebp + 0x4c], 0
004A263A: pop edi
004A263B: pop esi
004A263C: pop ebp
004A263D: xor al, al
004A263F: pop ebx
004A2640: add esp, 0xe4
004A2646: ret 4
004A2649: lea ecx, [ecx]
004A264C: scasd eax, dword ptr es:[edi]
004A264D: sbb al, 0x4a
004A264F: add byte ptr [edi - 0x50ffb5e2], dl
004A2655: sbb al, 0x4a
004A2657: add byte ptr [edx - 0x72ffb5e2], dh
004A265D: pop ds
004A265E: dec edx
004A265F: add byte ptr [ebp + 0x5004a1f], cl
004A2665: pop ds
004A2666: dec edx
004A2667: add byte ptr [eax - 0x6f6f6f70], dl
004A266D: nop 
004A266E: nop 
004A266F: nop 