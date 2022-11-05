#include "MicroBit.h"
#include "MicroBitTests.h"

MicroBit uBit;

void toDo(MicroBitEvent e){
    PrintCodeSerial(e);
}

int 
main()
{
    uBit.init();

    PrintReady();

    uBit.messageBus.listen(MICROBIT_ID_GESTURE, ACCELEROMETER_EVT_8G, toDo);
    while(1){
        uBit.sleep(100);
    }
}