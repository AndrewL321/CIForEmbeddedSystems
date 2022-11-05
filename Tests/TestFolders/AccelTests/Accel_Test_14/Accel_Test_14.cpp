#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    while(1){
        ManagedString x = uBit.accelerometer.getX();
        PrintDataSerial(DEVICE_ID_ACCELEROMETER,x);

        uBit.sleep(100);
    }
}