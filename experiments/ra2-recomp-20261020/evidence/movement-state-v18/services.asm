00548000: push esi
00548001: push edi
00548002: mov edi, dword ptr [esp + 0xc]
00548006: mov eax, dword ptr [edi]
00548008: cdq 
00548009: and edx, 0xff
0054800F: add eax, edx
00548011: mov esi, eax
00548013: mov eax, dword ptr [edi + 4]
00548016: cdq 
00548017: and edx, 0xff
0054801D: add eax, edx
0054801F: sar eax, 8
00548022: mov edx, eax
00548024: sar esi, 8
00548027: shl edx, 9
0054802A: add edx, esi
0054802C: js 0x54804a
0054802E: cmp edx, dword ptr [ecx + 0x13c]
00548034: jge 0x54804a
00548036: mov ecx, dword ptr [ecx + 0x138]
0054803C: mov edx, dword ptr [ecx + edx*4]
0054803F: test edx, edx
00548041: je 0x54804a
00548043: pop edi
00548044: mov eax, edx
00548046: pop esi
00548047: ret 4
0054804A: mov word ptr [esp + 0xc], si
0054804F: mov word ptr [esp + 0xe], ax
00548054: mov edx, dword ptr [esp + 0xc]
00548058: pop edi
00548059: mov dword ptr [0xa6fa1c], edx
0054805F: mov eax, 0xa6f9f8
00548064: pop esi
00548065: ret 4
00548068: nop 
00548069: nop 
0054806A: nop 
0054806B: nop 
0054806C: nop 
0054806D: nop 
0054806E: nop 
0054806F: nop 
00548070: mov edx, dword ptr [esp + 4]
00548074: push esi
00548075: movsx eax, word ptr [edx + 2]
00548079: movsx esi, word ptr [edx]
0054807C: shl eax, 9
0054807F: add eax, esi
00548081: pop esi
00548082: js 0x548098
00548084: cmp eax, 0x40000
00548089: jge 0x548098
0054808B: mov ecx, dword ptr [ecx + 0x138]
00548091: mov eax, dword ptr [ecx + eax*4]
00548094: test eax, eax
00548096: jne 0x5480a5
00548098: mov edx, dword ptr [edx]
0054809A: mov eax, 0xa6f9f8
0054809F: mov dword ptr [0xa6fa1c], edx
005480A5: ret 4
005480A8: nop 
005480A9: nop 
005480AA: nop 
005480AB: nop 
005480AC: nop 
005480AD: nop 
005480AE: nop 
005480AF: nop 
005480B0: mov eax, dword ptr [esp + 4]
005480B4: mov ecx, dword ptr [ecx + 0x138]
005480BA: movsx edx, word ptr [eax + 2]
005480BE: movsx eax, word ptr [eax]
005480C1: shl edx, 9
005480C4: add edx, eax
005480C6: cmp dword ptr [ecx + edx*4], 0
005480CA: setne al
005480CD: ret 4
005480D0: sub esp, 0x10
005480D3: push ebx
005480D4: push ebp
005480D5: push esi
005480D6: mov ebp, ecx
005480D8: push edi
005480D9: mov dword ptr [esp + 0x10], ebp
005480DD: call 0x4e0950
005480E2: mov eax, 0x200
005480E7: mov ecx, ebp
005480E9: mov dword ptr [ebp + 0x148], eax
005480EF: mov dword ptr [ebp + 0x14c], eax
005480F5: mov eax, dword ptr [ebp]