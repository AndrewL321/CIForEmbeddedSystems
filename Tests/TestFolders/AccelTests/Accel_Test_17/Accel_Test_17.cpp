#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    while(1){
        ManagedString z = uBit.accelerometer.getZ();
        PrintDataSerial(DEVICE_ID_ACCELEROMETER,z);

        uBit.sleep(100);
    }
}