#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    while(1){
        ManagedString data = uBit.display.readLightLevel();
        ManagedString source = DEVICE_ID_LIGHT_SENSOR;
        PrintDataSerial(source,data);
        uBit.sleep(100);
    }
}