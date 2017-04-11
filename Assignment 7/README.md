#Assignment 7 - Write your own crypter

###Student ID: SLAE-860

For this assignment, I decided to chain the encoder & egghunter used in assignment #4 to the AES encrypter implemented here.

The encrypter utilizes the CBC method of AES-128 encryption using the [AES implementation written by kokke](https://github.com/kokke/tiny-AES128-C)

Dependencies
-----------------------

    Python 3.5+
    NASM
    GCC
    Files:
        aes.c
        aes.h
        bencoder.nasm
        compile.sh
        shconfig.py
    
Usage
-----------------------

    1. ./compile.sh bencoder
        This uses NASM to compile the assembly source for the encoder.
        
    2. ./bencoder
        This should produce three files:  enc.hex, key.hex, and raw.hex.
            enc.hex contains the encoded shellcode bytes
            key.hex contains the key used by the decoder stub to decode the encoded shellcode bytes
            raw.hex contains the original shellcode that was encoded by the "bencoder" program
    3.  ./shconfig.py -e <egg value> -f asm --encrypt_with_key <key for AES encryption>
            <egg value>: This should be 4 valid hexadecimal characters only
            <key for AES encryption>: This is the key you are using to encrypt the bytes which comprise the decoder stub & egghunter
    4.  gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
    5.  ./shellcode
   
           
Explanation of files
-----------------------

    bencoder.nasm (The custom encoder):
        This assembly program encodes the execve-stack shellcode by XOR'ing each byte with a new pseudorandom byte
        obtained from the Intel 'rdrand' CPU instruction.  This creates a key to decode the execve-stack shellcode.
        It writes the pseudorandom bytes obtained by the 'rdrand' instruction into the 'key.hex' file, the encoded
        bytes into the 'enc.hex' file, and the original execve-stack shellcode bytes into the 'raw.hex' file.

    shconfig.py 
    (Creates, compiles and executes C source file for encryption, captures encryption program output and writes C source
     file for decryption):
        Reads all of the binary .hex files created by the compiled bencoder.nasm program to obtain the hex values.
        It then places the values into a dictionary which is keyed by the filename.  The key and egg value are then
        combined and formatted appropriately to be placed in the C source file.  The egghunter/decoder shellcode bytes
        are then pieced together with the 'enc.hex' bytes from the dictionary as well as the bytes from the egg value
        entered in step 2 above.  The opcodes from the egghunter/decoder combo program were obtained by compiling the
        decoder.nasm program, and then using objdump to display the opcodes.  The create_decoder_shellcode() function
        re-creates these opcodes based on whatever egg value was specified as well as whatever value happens to be 
        associated with the 'enc.hex' key of the dictionary (named 'byte_string_dict') created earlier.  A C source file
        is then written (encrypt.c) and GCC is called to compile it.  The encrypt program is then executed, which
        outputs the variable declaration for the encrypted shellcode bytes to be used by the decryption program.
        The C source file for decryption/shellcode execution is then written (shellcode.c).

    encrypt.c
        This is the C source file written and compiled by the shconfig.py program which returns a string which is the
        variable declaration for the encrypted decoder/egghunter shellcode that contains the encoded execve() shellcode.
        Compiling and then running this program will print the encrypted version of the bytes entered into the in[] 
        uint8_t array, in the form of the variable declaration which shconfig.py places into the shellcode.c source 
        file.
    
    shellcode.c
        This is the C source file used to decrypt and execute the encrypted decoder/egghunter shellcode stub which will
        decode and then execute the execve() shellcode.
    
    compile.sh (compilation shell script):
        Uses NASM to compile the supplied assembly program.

    enc.hex (encoded shellcode):
        These bytes are the encoded shellcode produced by the bencoder.nasm program.

    key.hex (key bytes):
        These bytes serve as the key to decode the encoded shellcode.

    raw.hex (raw shellcode):
        This is the exeve-stack shellcode prior to encoding.  Provided only as an example for examination, and not
        currently used by any program here.


Program Flow
-------------------------

                                                     raw.hex
     +---------------+                                                  +---------------+
     | Raw Execve()  +-------->  ./bencoder +------> key.hex +--------> | Key to decode | +----+
     |  Shellcode    |                                                  +---------------+      |
     +---------------+                               enc.hex                                   |
                                                        +                                      v
                                                        |                                +->./shconfig.py
                                                        +---->-----------------+         |        +
                                                              |Encoded Execve()| +-------+        |
                                                              |   Shellcode    |                  |                      +--->./shconfig.py  +-----> shellcode.c
                                                              +----------------+                  |                      |
                                                                                                  v                      |
                                                            +------------------------+    +-->encrypt.c +---CBC-Method---+                    +-----------------------+
                                                            |         aes.c          |    |                                                   |  +----------------+   |
                                                            |         aes.h          +----+                                                   |  |Encoded Execve()|   |
                                                            | <tiny-AES128 by kokke> |                                                        |  |   Shellcode    |   |
                                                            |                        |                                                        |  +----------------+   |
                                                            +------------------------+                                                        |                       |
                                                                                                                                              |   AES-128 Encrypted   |
                                                                                                                                              |   Encoded Shellcode   |
                                                                                                                                              +-----------------------+
