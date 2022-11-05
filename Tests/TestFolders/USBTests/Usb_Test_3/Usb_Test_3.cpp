#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    while(1){
        uBit.serial.send("Another");
        uBit.sleep(100);
    }
}