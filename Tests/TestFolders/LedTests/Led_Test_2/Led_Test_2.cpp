#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    uBit.display.print("1");
    while(1){

    }
}