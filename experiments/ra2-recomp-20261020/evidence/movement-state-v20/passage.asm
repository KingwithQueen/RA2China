004C86E0 push esi
004C86E1 mov esi, ecx
004C86E3 mov eax, dword ptr [esi + 0x564]
004C86E9 test eax, eax
004C86EB je 0x4c8723
004C86ED mov al, byte ptr [esp + 0x18]
004C86F1 test al, al
004C86F3 je 0x4c8723
004C86F5 mov eax, dword ptr [esp + 8]
004C86F9 push edi
004C86FA mov edi, dword ptr [eax + 0x24]
004C86FD mov eax, dword ptr [esi + 0x564]
004C8703 test eax, eax
004C8705 jne 0x4c8711
004C8707 push 0x80004003
004C870C call 0x795940
004C8711 mov esi, dword ptr [esi + 0x564]
004C8717 push edi
004C8718 push esi
004C8719 mov ecx, dword ptr [esi]
004C871B call dword ptr [ecx + 0x1c]
004C871E pop edi
004C871F pop esi
004C8720 ret 0x14
004C8723 xor eax, eax
004C8725 pop esi
004C8726 ret 0x14
004C8729 nop 
004C872A nop 
004C872B nop 
004C872C nop 
004C872D nop 
004C872E nop 
004C872F nop 
004C8730 push ebx
004C8731 mov ebx, dword ptr [esp + 0xc]
004C8735 push ebp
004C8736 push esi
004C8737 mov esi, dword ptr [esp + 0x20]
004C873B push edi
004C873C mov edi, dword ptr [esp + 0x14]
004C8740 test esi, esi
004C8742 jne 0x4c878c
004C8744 lea eax, [ebx - 4]
004C8747 and eax, 7
004C874A mov cx, word ptr [eax*4 + 0x851a70]
004C8752 mov dx, word ptr [eax*4 + 0x851a72]
004C875A add cx, word ptr [edi + 0x24]
004C875E add dx, word ptr [edi + 0x26]
004C8762 lea eax, [eax*4 + 0x851a70]
004C8769 mov word ptr [esp + 0x24], cx
004C876E lea ecx, [esp + 0x24]
004C8772 mov word ptr [esp + 0x26], dx
004C8777 mov eax, dword ptr [esp + 0x24]
004C877B push ecx
004C877C mov ecx, 0x8324e0
004C8781 mov dword ptr [esp + 0x28], eax
004C8785 call 0x548070
004C878A mov esi, eax
004C878C cmp ebx, -1
004C878F je 0x4c890e
004C8795 test esi, esi
004C8797 je 0x4c892e
004C879D test edi, edi
004C879F je 0x4c892e
004C87A5 mov ebp, dword ptr [esp + 0x1c]
004C87A9 cmp dword ptr [ebp], -1
004C87AD jne 0x4c87de
004C87AF mov eax, dword ptr [esi + 0x140]
004C87B5 test ah, 1
004C87B8 je 0x4c87de
004C87BA movsx edx, byte ptr [esi + 0x11b]
004C87C1 add edx, 4
004C87C4 mov dword ptr [ebp], edx
004C87C7 mov eax, dword ptr [edi + 0x140]
004C87CD test ah, 2
004C87D0 jne 0x4c87de
004C87D2 pop edi
004C87D3 pop esi
004C87D4 pop ebp
004C87D5 mov eax, 7
004C87DA pop ebx
004C87DB ret 0x14
004C87DE mov eax, dword ptr [esi + 0x140]
004C87E4 movsx ebx, byte ptr [edi + 0x11b]
004C87EB and eax, 0x100
004C87F0 mov dword ptr [esp + 0x1c], eax
004C87F4 je 0x4c87ff
004C87F6 movsx ecx, byte ptr [esi + 0x11b]
004C87FD jmp 0x4c8802
004C87FF mov ecx, dword ptr [ebp]
004C8802 sub ecx, ebx
004C8804 mov eax, ecx
004C8806 cdq 
004C8807 xor eax, edx
004C8809 sub eax, edx
004C880B sub eax, 0
004C880E je 0x4c88d8
004C8814 dec eax
004C8815 je 0x4c88a8
004C881B sub eax, 3
004C881E je 0x4c882c
004C8820 pop edi
004C8821 pop esi
004C8822 pop ebp
004C8823 mov eax, 7
004C8828 pop ebx
004C8829 ret 0x14
004C882C movsx eax, byte ptr [esi + 0x11b]
004C8833 lea ecx, [ebx - 4]
004C8836 cmp eax, ecx
004C8838 jne 0x4c885f
004C883A cmp dword ptr [ebp], ebx
004C883D je 0x4c884b
004C883F pop edi
004C8840 pop esi
004C8841 pop ebp
004C8842 mov eax, 7
004C8847 pop ebx
004C8848 ret 0x14
004C884B mov ecx, dword ptr [esp + 0x1c]
004C884F test ecx, ecx
004C8851 jne 0x4c885f
004C8853 pop edi
004C8854 pop esi
004C8855 pop ebp
004C8856 mov eax, 7
004C885B pop ebx
004C885C ret 0x14
004C885F add eax, -4
004C8862 cmp ebx, eax
004C8864 jne 0x4c892e
004C886A mov edi, dword ptr [edi + 0x140]
004C8870 test edi, 0x100
004C8876 jne 0x4c8884
004C8878 pop edi
004C8879 pop esi
004C887A pop ebp
004C887B mov eax, 7
004C8880 pop ebx
004C8881 ret 0x14
004C8884 test edi, 0x200
004C888A jne 0x4c8898
004C888C pop edi
004C888D pop esi
004C888E pop ebp
004C888F mov eax, 7
004C8894 pop ebx
004C8895 ret 0x14
004C8898 mov edx, dword ptr [esp + 0x20]
004C889C pop edi
004C889D pop esi
004C889E pop ebp
004C889F mov byte ptr [edx], 1
004C88A2 xor eax, eax
004C88A4 pop ebx
004C88A5 ret 0x14
004C88A8 test ecx, ecx
004C88AA jle 0x4c88c2
004C88AC mov al, byte ptr [edi + 0x11c]
004C88B2 test al, al
004C88B4 jne 0x4c892e
004C88B6 pop edi
004C88B7 pop esi
004C88B8 pop ebp
004C88B9 mov eax, 7
004C88BE pop ebx
004C88BF ret 0x14
004C88C2 mov al, byte ptr [esi + 0x11c]
004C88C8 test al, al
004C88CA jne 0x4c892e
004C88CC pop edi
004C88CD pop esi
004C88CE pop ebp
004C88CF mov eax, 7
004C88D4 pop ebx
004C88D5 ret 0x14
004C88D8 mov edi, dword ptr [edi + 0x140]
004C88DE test edi, 0x100
004C88E4 je 0x4c88f6
004C88E6 test edi, 0x200
004C88EC je 0x4c88f6
004C88EE mov eax, dword ptr [esp + 0x1c]
004C88F2 test eax, eax
004C88F4 jne 0x4c892e
004C88F6 mov eax, dword ptr [ebp]
004C88F9 cmp eax, -1
004C88FC je 0x4c892e
004C88FE cmp eax, ebx
004C8900 je 0x4c892e
004C8902 pop edi
004C8903 pop esi
004C8904 pop ebp
004C8905 mov eax, 7
004C890A pop ebx
004C890B ret 0x14
004C890E mov eax, dword ptr [esp + 0x1c]
004C8912 cmp dword ptr [eax], -1
004C8915 jne 0x4c892e
004C8917 mov ecx, dword ptr [edi + 0x140]
004C891D test ch, 1
004C8920 je 0x4c892e
004C8922 movsx ecx, byte ptr [edi + 0x11b]
004C8929 add ecx, 4
004C892C mov dword ptr [eax], ecx
004C892E pop edi
004C892F pop esi
004C8930 pop ebp
004C8931 xor eax, eax
004C8933 pop ebx
004C8934 ret 0x14
004C8937 nop 
004C8938 nop 
004C8939 nop 
004C893A nop 
004C893B nop 
004C893C nop 
004C893D nop 
004C893E nop 
004C893F nop 
004C8940 sub esp, 0x24
004C8943 push esi
004C8944 mov esi, ecx
004C8946 mov eax, dword ptr [esi]
004C8948 call dword ptr [eax + 0x2c]
004C894B test eax, eax
004C894D jle 0x4c8a2b
004C8953 cmp eax, 2
004C8956 jg 0x4c8a2b
004C895C mov ecx, esi
004C895E call 0x636f10
004C8963 test al, al
004C8965 je 0x4c8a2b
004C896B push 0
004C896D mov ecx, esi
004C896F call 0x636e20
004C8974 mov edx, dword ptr [eax]
004C8976 mov ecx, eax
004C8978 call dword ptr [edx + 0x2c]
004C897B cmp eax, 6
004C897E jne 0x4c8a2b
004C8984 push 0
004C8986 mov ecx, esi
004C8988 call 0x636e20
004C898D mov eax, dword ptr [eax + 0x418]
004C8993 mov cl, byte ptr [eax + 0x1349]
004C8999 test cl, cl
004C899B je 0x4c8a2b
004C89A1 push edi
004C89A2 push 0
004C89A4 mov ecx, esi
004C89A6 call 0x636e20
004C89AB mov edx, dword ptr [eax]
004C89AD lea ecx, [esp + 0x14]
004C89B1 push ecx
004C89B2 mov ecx, eax
004C89B4 call dword ptr [edx + 0x48]
004C89B7 mov edx, dword ptr [esi]
004C89B9 mov edi, eax
004C89BB lea eax, [esp + 0x20]