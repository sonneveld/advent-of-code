0000 goto 0017

0001 r5 = 1

0002 r1 = 1

0003 r2 = r5 * r1
0004 r2 = r2 == r3
0005 if (r2) goto 0007

0006 goto 0008

0007 r0 = r5 + r0

0008 r1 = r1 + 1
0009 r2 = r1 > r3
0010 if (r2) goto 0012

0011 goto 0003

0012 r5 = r5 + 1
0013 r2 = r5 > r3
0014 if (r2) goto 0016

0015 goto 0002

0016 halt

0017 r3 = r3 + 2
0018 r3 = r3 * r3
0019 r3 = 19 * r3
0020 r3 = r3 * 11
0021 r2 = r2 + 4
0022 r2 = r2 * 22
0023 r2 = r2 + 6
0024 r3 = r3 + r2
0025 if (r0) goto 0027

0026 goto 0001

0027 r2 = 27
0028 r2 = r2 * 28
0029 r2 = 29 + r2
0030 r2 = 30 * r2
0031 r2 = r2 * 14
0032 r2 = r2 * 32
0033 r3 = r3 + r2
0034 r0 = 0
0035 goto 0001
