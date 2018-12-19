#include <stdio.h>

// direct translation from machine code
int sum_factors_slow(int r3) {
    int r0  = 0;

    for (int r5=1;  r5 <= r3; r5++) {
        for (int r1=1;  r1 <= r3; r1++) {
            if (r1*r5 == r3) {
                r0 += r5;
            }
        }
    }

    return r0;
}

// slightly faster version
int sum_factors(int r3) {
    int r0 = 0;

    for (int r5 = 1; r5<= r3;  r5++) {
        if (r3 % r5 == 0) {
            r0 += r5;
        }
    }

    return r0;
}

int main() {
    printf("%d\n", sum_factors(930));
    printf("%d\n", sum_factors(10551330));

    // printf("%d\n", sum_factors_slow(930));
    // printf("%d\n", sum_factors_slow(10551330));

    return 0;
}
