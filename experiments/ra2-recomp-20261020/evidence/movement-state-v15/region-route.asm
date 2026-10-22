0042A122 test eax, eax
0042A124 je 0x42a1b2
0042A12A mov edx, dword ptr [eax]
0042A12C mov ecx, eax
0042A12E cmp edx, -1
0042A131 mov dword ptr [esp + 0x54], ecx
0042A135 je 0x42a157
0042A137 mov ecx, dword ptr [eax + 4]
0042A13A mov ebx, dword ptr [esp + 0x5c]
0042A13E mov edx, dword ptr [edi + 0x28]
0042A141 mov dword ptr [ebx + ecx*4], edx
0042A144 mov eax, dword ptr [eax]
0042A146 mov edx, dword ptr [edi + 0x64]
0042A149 shl eax, 4
0042A14C add eax, edx
0042A14E cmp dword ptr [eax], -1
0042A151 jne 0x42a137
0042A153 mov ecx, dword ptr [esp + 0x54]
0042A157 mov eax, dword ptr [ecx + 0xc]
0042A15A inc eax
0042A15B mov dword ptr [edi + esi*4 + 0xc74], eax
0042A162 dec eax
0042A163 test eax, eax
0042A165 jle 0x42a191
0042A167 lea edx, [esi + esi*4]
0042A16A lea edx, [edx + edx*4]
0042A16D lea edx, [edx + edx*4]
0042A170 lea edx, [eax + edx*4]
0042A173 lea edx, [edi + edx*2 + 0xbc]
0042A17A mov bx, word ptr [ecx + 4]
0042A17E mov word ptr [edx], bx
0042A181 mov ecx, dword ptr [ecx]
0042A183 mov ebx, dword ptr [edi + 0x64]
0042A186 sub edx, 2
0042A189 shl ecx, 4
0042A18C add ecx, ebx
0042A18E dec eax
0042A18F jne 0x42a17a
0042A191 mov cx, word ptr [ecx + 4]
0042A195 lea eax, [esi + esi*4]
0042A198 lea eax, [eax + eax*4]
0042A19B lea eax, [eax + eax*4]
0042A19E mov word ptr [edi + eax*8 + 0xbc], cx
0042A1A6 dec esi
0042A1A7 mov dword ptr [esp + 0x38], esi
0042A1AB js 0x42a1bd
0042A1AD jmp 0x429bd9