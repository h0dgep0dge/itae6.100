#include <stdio.h>
#include <unistd.h>

int main() {
    unsigned char msb,lsb;
    unsigned short o;
    int r;
    while(1) {
        if(read(0,&msb,1) == 0) break;
        if(read(0,&lsb,1) == 0) break;
        o = (msb<<8) | lsb;
        printf("%u \n",o);
    }
    
    return 0;
}
