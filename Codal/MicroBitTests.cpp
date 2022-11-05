#include "MicroBitTests.h"
#include "MicroBit.h"

#ifdef MICROBIT_UBIT_AS_STATIC_OBJECT
extern MicroBit uBit;
#else
extern MicroBit uBit;
#endif

//Send ready signal
void PrintReady(){
    uBit.serial.send("uBitTest|Ready");
}

//Send event code
void PrintCodeSerial(MicroBitEvent e){
    ManagedString source = e.source;
    ManagedString value = e.value;
    
    uBit.serial.send("uBitTest|Event|"+ source + "|" + value + "\n");
}

//Send pre labeled data 
void PrintDataSerial(ManagedString source, ManagedString data){
    ManagedString message  = "uBitTest|Data|" + source + "|" + data + "\n";
    uBit.serial.send(message);
}


//To implement
void PrintHeapSerial(){
}

//User defined label
void PrintMiscSerial(ManagedString label,ManagedString data){
    ManagedString message  = "uBitTest|Label|" + label + "|" + data + "\n";
    uBit.serial.send(message);
}