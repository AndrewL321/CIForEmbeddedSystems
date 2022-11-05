#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    while(1){
        ManagedString y = uBit.accelerometer.getY();
        PrintDataSerial(DEVICE_ID_ACCELEROMETER,y);

        uBit.sleep(100);
    }
}