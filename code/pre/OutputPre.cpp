#include "OutputPre.h"

OutputPre::OutputPre() {
}

void OutputPre::begin(uint8_t addrV, uint8_t addrI,  unsigned long del) {
  mcpV.begin(addrV);
  mcpI.begin(addrI);
  relDelay=del;

  for(uint8_t i=0;i<16;i++) {
    mcpV.pinMode(i, OUTPUT);
  }

  for(uint8_t i=0;i<16;i++) {
    mcpI.pinMode(i, OUTPUT);
  }

}

void OutputPre::setVolume(uint8_t nVol) {
  uint8_t vol=nVol;
  uint16_t gpioOut=0;
  
  uint8_t b,gpBit;
  
  for(uint8_t i=0;i<8;i++) {
    b=bitRead(vol,i);
    gpBit=0;
    switch(i) {
      case 0: gpBit=b ? 8 : 9; break;
      case 1: gpBit=b ? 10 : 11; break;
      case 2: gpBit=b ? 12 : 13; break;
      case 3: gpBit=b ? 14 : 15; break;
      case 4: gpBit=b ? 0 : 1; break;
      case 5: gpBit=b ? 2 : 3; break;
      case 6: gpBit=b ? 4 : 5; break;
      case 7: gpBit=b ? 6 : 7; break;
      default: gpBit=0; 
    }
    gpioOut+=1 << gpBit;
  }
  //Serial.println(" OUT: "+String(gpioOut));
  
  mcpV.writeGPIOAB(gpioOut);
  delay(relDelay);
  mcpV.writeGPIOAB(0);
}

void OutputPre::clearInput() {
  setInput(0);
}

void OutputPre::setInput(uint8_t nInp) { 
  uint8_t inp=nInp;
  uint16_t gpioOut=0;
  
  uint8_t b,gpBit;
  for(uint8_t i=0;i<INPUT_STEPS;i++) {
    gpBit=0;
    switch(i) {
      case 0: gpBit=(inp==1)? 8 : 9; break;
      case 1: gpBit=(inp==2) ? 10 : 11; break;
      case 2: gpBit=(inp==3) ? 12 : 13; break;
      case 3: gpBit=(inp==4) ? 14 : 15; break;
      case 4: gpBit=(inp==5) ? 0 : 1; break;
      default: gpBit=0; 
    }
    gpioOut+=1 << gpBit;
  }
  
  //gpioOut+=(direct) ? 1 << 3 : 1 << 4; 

  //Serial.println(" OUT: "+String(gpioOut));

  mcpI.writeGPIOAB(gpioOut);
  delay(relDelay);
  mcpI.writeGPIOAB(0);
}

void OutputPre::setDirect(bool in) {
  //mcpI.digitalWrite(14,in ? 1:0);
}

void OutputPre::setOutOff(bool in) {
  //mcpI.digitalWrite(13,in ? 1:0);
}
