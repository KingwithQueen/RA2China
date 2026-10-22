00427CBB mov ecx, dword ptr [esp + 0x28]
00427CBF cmp ecx, 0x2710
00427CC5 je 0x427d1b
00427CC7 mov eax, dword ptr [esp + 0x14]
00427CCB test eax, eax
00427CCD je 0x427d1b
00427CCF cmp ecx, dword ptr [esp + 0x70]
00427CD3 je 0x427d1b
00427CD5 cmp dword ptr [eax + 0xc], 2
00427CD9 jl 0x427d1b
00427CDB mov ecx, dword ptr [esp + 0x6c]
00427CDF push ecx
00427CE0 push eax
00427CE1 mov ecx, esi
00427CE3 call 0x428370
00427CE8 mov ebx, dword ptr [esp + 0x68]
00427CEC mov edi, eax
00427CEE push ebx
00427CEF push edi
00427CF0 mov ecx, esi
00427CF2 call 0x428ae0
00427CF7 push ebx
00427CF8 push edi
00427CF9 mov ecx, esi
00427CFB call 0x4290c0
00427D00 mov eax, dword ptr [esi + 0x3c]
00427D03 test eax, eax
00427D05 je 0x427d0f
00427D07 push ebx
00427D08 mov ecx, esi
00427D0A call 0x4285d0
00427D0F mov eax, edi
00427D11 pop edi
00427D12 pop esi
00427D13 pop ebp
00427D14 pop ebx
00427D15 add esp, 0x4c
00427D18 ret 0x18
00427D1B mov ebx, dword ptr [esp + 0x68]
00427D1F mov eax, dword ptr [esi + 0x3c]
00427D22 test eax, eax
00427D24 je 0x427d2e
00427D26 push ebx
00427D27 mov ecx, esi
00427D29 call 0x4285d0
00427D2E pop edi
00427D2F pop esi
00427D30 pop ebp
00427D31 xor eax, eax
00427D33 pop ebx
00427D34 add esp, 0x4c
00427D37 ret 0x18