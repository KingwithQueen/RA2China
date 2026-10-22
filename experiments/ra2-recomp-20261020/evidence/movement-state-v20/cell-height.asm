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