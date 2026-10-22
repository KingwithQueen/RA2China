004706C0 push ebp
004706C1 mov ebp, esp
004706C3 and esp, 0xfffffff8
004706C6 sub esp, 0xc
004706C9 mov al, byte ptr [0x850bb8]
004706CE push esi
004706CF test al, 1
004706D1 mov esi, ecx
004706D3 jne 0x4706e8
004706D5 fild dword ptr [0x850c40]
004706DB or al, 1
004706DD mov byte ptr [0x850bb8], al
004706E2 fstp qword ptr [0x850ba8]
004706E8 test al, 2
004706EA jne 0x470705
004706EC fld qword ptr [0x850ba8]
004706F2 fmul qword ptr [0x79a730]
004706F8 or al, 2
004706FA mov byte ptr [0x850bb8], al
004706FF fstp qword ptr [0x850bd0]
00470705 test al, 4
00470707 jne 0x470db4
0047070D mov ecx, dword ptr [0x850bac]
00470713 or al, 4
00470715 mov byte ptr [0x850bb8], al
0047071A mov eax, dword ptr [0x850ba8]
0047071F mov dword ptr [0x7d2800], eax
00470724 mov edx, eax
00470726 mov dword ptr [0x7d2804], ecx
0047072C mov eax, ecx
0047072E mov dword ptr [0x7d2828], edx
00470734 mov ecx, edx
00470736 mov dword ptr [0x7d282c], eax
0047073B mov edx, eax
0047073D mov dword ptr [0x7d2848], ecx
00470743 mov eax, ecx
00470745 mov dword ptr [0x7d284c], edx
0047074B mov ecx, edx
0047074D fld qword ptr [0x850ba8]
00470753 mov dword ptr [0x7d2850], eax
00470758 mov edx, eax
0047075A mov dword ptr [0x7d2854], ecx
00470760 mov eax, ecx
00470762 mov dword ptr [0x7d2870], edx
00470768 mov ecx, edx
0047076A mov dword ptr [0x7d2874], eax
0047076F mov edx, eax
00470771 mov dword ptr [0x7d2878], ecx
00470777 mov eax, ecx
00470779 mov dword ptr [0x7d287c], edx
0047077F mov ecx, edx
00470781 mov dword ptr [0x7d28a0], eax
00470786 mov edx, eax
00470788 mov dword ptr [0x7d28a4], ecx
0047078E mov eax, ecx
00470790 mov dword ptr [0x7d28c8], edx
00470796 mov ecx, edx
00470798 fchs 
0047079A fstp qword ptr [0x7d2898]
004707A0 mov edx, eax
004707A2 mov dword ptr [0x7d2808], 0
004707AC mov dword ptr [0x7d280c], 0
004707B6 mov dword ptr [0x7d2810], 0
004707C0 mov dword ptr [0x7d2814], 0
004707CA mov dword ptr [0x7d2818], 0
004707D4 mov dword ptr [0x7d281c], 0x3ff00000
004707DE mov dword ptr [0x7d2820], 0
004707E8 mov dword ptr [0x7d2824], 0
004707F2 mov dword ptr [0x7d2830], 0
004707FC mov dword ptr [0x7d2834], 0
00470806 mov dword ptr [0x7d2838], 0
00470810 mov dword ptr [0x7d283c], 0xbff00000
0047081A mov dword ptr [0x7d2840], 0
00470824 mov dword ptr [0x7d2844], 0
0047082E mov dword ptr [0x7d2858], 0
00470838 mov dword ptr [0x7d285c], 0
00470842 mov dword ptr [0x7d2860], 0
0047084C mov dword ptr [0x7d2864], 0
00470856 mov dword ptr [0x7d2868], 0
00470860 mov dword ptr [0x7d286c], 0xbff00000
0047086A mov dword ptr [0x7d2880], 0
00470874 mov dword ptr [0x7d2884], 0
0047087E mov dword ptr [0x7d2888], 0
00470888 mov dword ptr [0x7d288c], 0x3ff00000
00470892 mov dword ptr [0x7d2890], 0
0047089C mov dword ptr [0x7d2894], 0x3ff00000
004708A6 mov dword ptr [0x7d28a8], 0
004708B0 mov dword ptr [0x7d28ac], 0
004708BA mov dword ptr [0x7d28b0], 0
004708C4 mov dword ptr [0x7d28b4], 0xbff00000
004708CE mov dword ptr [0x7d28b8], 0
004708D8 mov dword ptr [0x7d28bc], 0x3ff00000
004708E2 mov dword ptr [0x7d28c0], 0
004708EC mov dword ptr [0x7d28c4], 0
004708F6 mov dword ptr [0x7d28cc], eax
004708FB mov dword ptr [0x7d28d0], 0
00470905 mov dword ptr [0x7d28d4], 0
0047090F mov dword ptr [0x7d28d8], 0
00470919 mov dword ptr [0x7d28dc], 0xbff00000
00470923 mov dword ptr [0x7d28e0], 0
0047092D mov dword ptr [0x7d28e4], 0xbff00000
00470937 mov dword ptr [0x7d28e8], ecx
0047093D mov dword ptr [0x7d28ec], edx
00470943 mov eax, ecx
00470945 mov ecx, edx
00470947 mov dword ptr [0x7d28f0], eax
0047094C mov edx, eax
0047094E fld qword ptr [0x850ba8]
00470954 mov dword ptr [0x7d28f4], ecx
0047095A mov eax, ecx
0047095C mov dword ptr [0x7d2918], edx
00470962 mov ecx, edx
00470964 mov dword ptr [0x7d291c], eax
00470969 mov edx, eax
0047096B mov dword ptr [0x7d2940], ecx
00470971 mov eax, ecx
00470973 mov dword ptr [0x7d2944], edx
00470979 mov ecx, edx
0047097B mov dword ptr [0x7d2960], eax
00470980 mov edx, eax
00470982 mov dword ptr [0x7d2964], ecx
00470988 mov eax, ecx
0047098A mov dword ptr [0x7d2968], edx
00470990 mov ecx, edx
00470992 mov dword ptr [0x7d296c], eax
00470997 mov edx, eax
00470999 fadd st(0), st(0)
0047099B mov dword ptr [0x7d2990], ecx
004709A1 mov eax, ecx
004709A3 mov dword ptr [0x7d2994], edx
004709A9 mov ecx, edx
004709AB mov dword ptr [0x7d29b0], eax
004709B0 mov edx, eax
004709B2 fst qword ptr [0x7d2988]
004709B8 fst qword ptr [0x7d29e0]
004709BE mov eax, ecx
004709C0 mov dword ptr [0x7d28f8], 0
004709CA mov dword ptr [0x7d28fc], 0
004709D4 mov dword ptr [0x7d2900], 0
004709DE mov dword ptr [0x7d2904], 0x3ff00000
004709E8 mov dword ptr [0x7d2908], 0
004709F2 mov dword ptr [0x7d290c], 0xbff00000
004709FC mov dword ptr [0x7d2910], 0
00470A06 mov dword ptr [0x7d2914], 0
00470A10 mov dword ptr [0x7d2920], 0
00470A1A mov dword ptr [0x7d2924], 0
00470A24 mov dword ptr [0x7d2928], 0
00470A2E mov dword ptr [0x7d292c], 0x3ff00000
00470A38 mov dword ptr [0x7d2930], 0
00470A42 mov dword ptr [0x7d2934], 0x3ff00000
00470A4C mov dword ptr [0x7d2938], 0
00470A56 mov dword ptr [0x7d293c], 0
00470A60 mov dword ptr [0x7d2948], 0
00470A6A mov dword ptr [0x7d294c], 0
00470A74 mov dword ptr [0x7d2950], 0
00470A7E mov dword ptr [0x7d2954], 0xbff00000
00470A88 mov dword ptr [0x7d2958], 0
00470A92 mov dword ptr [0x7d295c], 0x3ff00000
00470A9C mov dword ptr [0x7d2970], 0
00470AA6 mov dword ptr [0x7d2974], 0
00470AB0 mov dword ptr [0x7d2978], 0
00470ABA mov dword ptr [0x7d297c], 0xbff00000
00470AC4 mov dword ptr [0x7d2980], 0
00470ACE mov dword ptr [0x7d2984], 0xbff00000
00470AD8 mov dword ptr [0x7d2998], 0
00470AE2 mov dword ptr [0x7d299c], 0
00470AEC mov dword ptr [0x7d29a0], 0
00470AF6 mov dword ptr [0x7d29a4], 0x3ff00000
00470B00 mov dword ptr [0x7d29a8], 0
00470B0A mov dword ptr [0x7d29ac], 0xbff00000
00470B14 mov dword ptr [0x7d29b4], ecx
00470B1A mov dword ptr [0x7d29b8], edx
00470B20 mov dword ptr [0x7d29bc], eax
00470B25 mov dword ptr [0x7d29c0], 0
00470B2F mov dword ptr [0x7d29c4], 0
00470B39 mov dword ptr [0x7d29c8], 0
00470B43 mov dword ptr [0x7d29cc], 0x3ff00000
00470B4D mov dword ptr [0x7d29d0], 0
00470B57 mov dword ptr [0x7d29d4], 0x3ff00000
00470B61 mov dword ptr [0x7d29d8], 0
00470B6B mov dword ptr [0x7d29dc], 0
00470B75 mov dword ptr [0x7d29e8], 0
00470B7F mov dword ptr [0x7d29ec], 0
00470B89 mov dword ptr [0x7d29f0], 0
00470B93 fst qword ptr [0x7d2a08]
00470B99 fst qword ptr [0x7d2a28]
00470B9F fst qword ptr [0x7d2a30]
00470BA5 fstp qword ptr [0x7d2a58]
00470BAB fld qword ptr [0x850ba8]
00470BB1 fmul qword ptr [0x79a728]
00470BB7 mov ecx, edx
00470BB9 mov edx, eax
00470BBB mov dword ptr [0x7d2a00], ecx
00470BC1 mov eax, ecx
00470BC3 mov dword ptr [0x7d2a04], edx
00470BC9 mov ecx, edx
00470BCB fst qword ptr [0x7d2a80]
00470BD1 fst qword ptr [0x7d2a88]
00470BD7 fst qword ptr [0x7d2aa8]
00470BDD fld qword ptr [0x850ba8]
00470BE3 fmul qword ptr [0x79c9b0]
00470BE9 mov dword ptr [0x7d2a50], eax
00470BEE mov edx, eax
00470BF0 mov dword ptr [0x7d2a54], ecx
00470BF6 mov eax, ecx
00470BF8 mov ecx, edx
00470BFA mov dword ptr [0x7d2aa0], edx
00470C00 fst qword ptr [esp + 8]
00470C04 fstp qword ptr [0x7d2ab0]
00470C0A mov dword ptr [0x7d2aa4], eax
00470C0F mov edx, eax
00470C11 mov eax, dword ptr [esp + 8]
00470C15 mov dword ptr [0x7d2af0], ecx
00470C1B mov ecx, dword ptr [esp + 0xc]
00470C1F mov dword ptr [0x7d29f4], 0xbff00000
00470C29 fst qword ptr [0x7d2ad0]
00470C2F fst qword ptr [0x7d2ad8]
00470C35 fstp qword ptr [0x7d2af8]
00470C3B mov dword ptr [0x7d29f8], 0
00470C45 mov dword ptr [0x7d29fc], 0x3ff00000
00470C4F mov dword ptr [0x7d2a10], 0
00470C59 mov dword ptr [0x7d2a14], 0
00470C63 mov dword ptr [0x7d2a18], 0
00470C6D mov dword ptr [0x7d2a1c], 0xbff00000
00470C77 mov dword ptr [0x7d2a20], 0
00470C81 mov dword ptr [0x7d2a24], 0xbff00000
00470C8B mov dword ptr [0x7d2a38], 0
00470C95 mov dword ptr [0x7d2a3c], 0
00470C9F mov dword ptr [0x7d2a40], 0
00470CA9 mov dword ptr [0x7d2a44], 0x3ff00000
00470CB3 mov dword ptr [0x7d2a48], 0
00470CBD mov dword ptr [0x7d2a4c], 0xbff00000
00470CC7 mov dword ptr [0x7d2a60], 0
00470CD1 mov dword ptr [0x7d2a64], 0
00470CDB mov dword ptr [0x7d2a68], 0
00470CE5 mov dword ptr [0x7d2a6c], 0
00470CEF mov dword ptr [0x7d2a70], 0
00470CF9 mov dword ptr [0x7d2a74], 0
00470D03 mov dword ptr [0x7d2a78], 0
00470D0D mov dword ptr [0x7d2a7c], 0
00470D17 mov dword ptr [0x7d2a90], 0
00470D21 mov dword ptr [0x7d2a94], 0
00470D2B mov dword ptr [0x7d2a98], 0
00470D35 mov dword ptr [0x7d2a9c], 0
00470D3F mov dword ptr [0x7d2ab8], 0
00470D49 mov dword ptr [0x7d2abc], 0
00470D53 mov dword ptr [0x7d2ac0], 0
00470D5D mov dword ptr [0x7d2ac4], 0
00470D67 mov dword ptr [0x7d2ac8], 0
00470D71 mov dword ptr [0x7d2acc], 0
00470D7B mov dword ptr [0x7d2ae0], 0
00470D85 mov dword ptr [0x7d2ae4], 0
00470D8F mov dword ptr [0x7d2ae8], 0
00470D99 mov dword ptr [0x7d2aec], 0
00470DA3 mov dword ptr [0x7d2af4], edx
00470DA9 mov dword ptr [0x7d2b00], eax
00470DAE mov dword ptr [0x7d2b04], ecx
00470DB4 movsx edx, byte ptr [esi + 0x11b]
00470DBB imul edx, dword ptr [0x850c40]
00470DC2 mov dword ptr [esp + 4], edx
00470DC6 fild dword ptr [esp + 4]
00470DCA fadd qword ptr [0x79a728]
00470DD0 call 0x77f110
00470DD5 mov cl, byte ptr [esi + 0x11c]
00470DDB mov dword ptr [esp + 8], eax
00470DDF test cl, cl
00470DE1 jbe 0x470e74
00470DE7 mov eax, dword ptr [ebp + 8]
00470DEA and ecx, 0xff
00470DF0 dec ecx
00470DF1 mov edx, dword ptr [eax + 4]
00470DF4 mov eax, dword ptr [eax]
00470DF6 and edx, 0xff
00470DFC lea ecx, [ecx + ecx*4]
00470DFF mov dword ptr [esp + 4], edx
00470E03 and eax, 0xff
00470E08 fild dword ptr [esp + 4]
00470E0C shl ecx, 3
00470E0F mov dword ptr [esp + 4], eax
00470E13 fmul qword ptr [ecx + 0x7d27f0]
00470E19 fmul qword ptr [0x850bd0]
00470E1F fild dword ptr [esp + 4]
00470E23 fmul qword ptr [ecx + 0x7d27e8]
00470E29 fmul qword ptr [0x850bd0]
00470E2F faddp st(1)
00470E31 fadd qword ptr [ecx + 0x7d27f8]
00470E37 fadd qword ptr [ecx + 0x7d2808]
00470E3D fcom qword ptr [0x79b610]
00470E43 fnstsw ax
00470E45 test ah, 1
00470E48 je 0x470e52
00470E4A fstp st(0)
00470E4C fld qword ptr [0x79b610]
00470E52 fcom qword ptr [ecx + 0x7d2800]
00470E58 fnstsw ax
00470E5A test ah, 0x41
00470E5D jne 0x470e67
00470E5F fstp st(0)
00470E61 fld qword ptr [ecx + 0x7d2800]
00470E67 fild dword ptr [esp + 8]
00470E6B fadd st(1)
00470E6D call 0x77f110
00470E72 fstp st(0)
00470E74 pop esi
00470E75 mov esp, ebp
00470E77 pop ebp
00470E78 ret 4