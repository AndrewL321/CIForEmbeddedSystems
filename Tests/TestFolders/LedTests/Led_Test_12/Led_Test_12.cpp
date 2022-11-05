#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    MicroBitImage image(5,5);

    uBit.display.print(image);
    while(1){

    }
}