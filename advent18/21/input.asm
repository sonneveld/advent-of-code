0000 r1 = 123

0001 r1 = r1 & 456
0002 r1 = r1 == 72
0003 if (r1) goto 0005

0004 goto 0001

0005 r1 = 0

0006 r3 = r1 | 65536
0007 r1 = 10905776

0008 r4 = r3 & 255
0009 r1 = r1 + r4
0010 r1 = r1 & 16777215
0011 r1 = r1 * 65899
0012 r1 = r1 & 16777215
0013 r4 = 256 > r3
0014 if (r4) goto 0016

0015 goto 0017

0016 goto 0028

0017 r4 = 0

0018 r5 = r4 + 1
0019 r5 = r5 * 256
0020 r5 = r5 > r3
0021 if (r5) goto 0023

0022 goto 0024

0023 goto 0026

0024 r4 = r4 + 1
0025 goto 0018

0026 r3 = r4
0027 goto 0008

0028 r4 = r1 == r0
0029 if (r4) goto 0031

0030 goto 0006