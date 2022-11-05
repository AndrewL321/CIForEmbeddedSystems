#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

int 
main()
{
    uBit.init();

    PrintReady();

    uBit.messageBus.listen(MICROBIT_ID_GESTURE, ACCELEROMETER_EVT_TILT_RIGHT, PrintCodeSerial);
    while(1){
        uBit.sleep(100);
    }
}