Student ID:SLAE-860
Assignment 4

Instructions:
1 - Compile bencoder.nasm using compile.sh and run.  This should output three binary files ending in the extension .hex
2 - Run shconfig4.py, specifying the egg value as one argument, and the output format as another argument.
2a - Example:
                ./shconfig4.py -e 1b2a -f c
3 - The output produced by the python program is a C source file.  For brevity, you can just redirect this to a file.
3a - Example:
                ./shconfig4.py -e 1b2a -f c > shellcode.c
4 - Compile the output and run.
4a - Example:
                gcc -fno-stack-protector -z execstack shellcode.c -o shellcode
                ./shellcode

                Shellcode Length:  89
                #


Explanation of files
-----------------------

    bencoder.nasm (The custom encoder):
        This assembly program encodes the execve-stack shellcode by XOR'ing each byte with a new pseudorandom byte
        obtained from the Intel 'rdrand' CPU instruction.  This creates a key to decode the execve-stack shellcode.
        It writes the pseudorandom bytes obtained by the 'rdrand' instruction into the 'key.hex' file, the encoded
        bytes into the 'enc.hex' file, and the original execve-stack shellcode bytes into the 'raw.hex' file.

    shconfig4.py (Creates the C source file):
        Reads all of the binary .hex files created by the compiled bencoder.nasm program to obtain the hex values.
        It then places the values into a dictionary which is keyed by the filename.  The key and egg value are then
        combined and formatted appropriately to be placed in the C source file.  The egghunter/decoder shellcode bytes
        are then pieced together with the 'enc.hex' bytes from the dictionary as well as the bytes from the egg value
        entered in step 2 above.  The opcodes from the egghunter/decoder combo program were obtained by compiling the
        decoder.nasm program, and then using objdump to display the opcodes.  The create_decoder_shellcode() function
        re-creates these opcodes based on whatever egg value was specified as well as whatever value happens to be in
        the 'enc.hex' key of the dictionary (named 'byte_string_dict') created earlier.  Finally, the program generates
        a C source file and prints it to standard output.  This can be redirected to a file, as seen in the example 3a
        above.

    decoder.nasm (Egghunter & Decoder stub):
        This program searches all valid memory for the egg which is used in this case to locate where
        the key bytes are found in memory.  Once the key bytes are found, the encoded shellcode is XOR'ed byte-by-byte
        and then execution jumps to that memory location, which executes the now-decoded execve-stack shellcode.

        Note:  The egg value supplied, as well as the 'enc_shellcode' bytes are provided as an example, and of course
        would change based on the egg supplied and key generated from the bencoder.nasm program.  This assembly source
        code is present only to show how the opcodes used in the create_decoder_shellcode() function in shconfig4.py
        were obtained.

    compile.sh (compilation shell script):
        Uses NASM to compile the supplied assembly program.

    enc.hex (encoded shellcode):
        These bytes are the encoded shellcode produced by the bencoder.nasm program.

    key.hex (key bytes):
        These bytes serve as the key to decode the encoded shellcode.

    raw.hex (raw shellcode):
        This is the exeve-stack shellcode prior to encoding.  Provided only as an example for examination, and not
        currently used by any program here.