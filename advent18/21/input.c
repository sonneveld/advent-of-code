#include  <stdio.h>

int main() {
    int r0=0, r1=0, r3=0;
    r1 = 0;

    do {
        r3 = r1 | 0x10000;
        r1 = 10905776;

        for(;;) {
            r1 = (((r1 + (r3 & 0x00ff)) & 0x00ffffff ) * 65899) & 0x00ffffff;
            if (r3 < 0x100) { break; }
            r3 >>= 8;
        }

        printf("%d\n", r1);
    } while (r1 != r0);
}
