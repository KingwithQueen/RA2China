0077F110 sub esp, 0xc
0077F113 fnstcw word ptr [esp]
0077F116 lea eax, [esp + 4]
0077F11A mov edx, dword ptr [esp]
0077F11D and edx, 0xffff
0077F123 cmp edx, dword ptr [0x7d8964]
0077F129 jne 0x77f136
0077F12B fistp qword ptr [eax]
0077F12D mov edx, dword ptr [eax + 4]
0077F130 mov eax, dword ptr [eax]
0077F132 add esp, 0xc
0077F135 ret 
0077F136 mov edx, dword ptr [0x7d8964]
0077F13C mov dword ptr [esp], edx
0077F13F fldcw word ptr [esp]
0077F142 fistp qword ptr [eax]
0077F144 mov edx, dword ptr [eax + 4]
0077F147 mov eax, dword ptr [eax]
0077F149 add esp, 0xc
0077F14C ret 
0077F14D push ebp
0077F14E mov ebp, esp