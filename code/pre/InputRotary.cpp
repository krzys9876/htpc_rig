#include "InputRotary.h"



InputRotary::InputRotary() {
  pos=0;
}

void InputRotary::begin(uint8_t addr) {
  mcp.begin(addr);
 
  for(uint8_t i=0;i<8;i++) {
    mcp.pinMode(i, INPUT);
    mcp.pullUp(i, HIGH);
  }
}

uint8_t InputRotary::read() {
  return mcp.readGPIO();   
}

uint8_t InputRotary::getPos() {
  return pos;
}

bool InputRotary::getButton(uint8_t b) {
  return button[b];
}

uint8_t InputRotary::getBit(uint8_t in) {
  for(uint8_t i=0;i<5;i++) {
    if(bitRead(in,i)) {
      return i+1;
    }
  }
  return 0;
}

uint8_t InputRotary::getBitPos(uint8_t in) {
  return getBit(in);
}

bool InputRotary::refresh() {
  uint8_t v=read();
  v=v ^ 255;
  //Serial.print(v);
  bool refr=false;

  for(uint8_t i=0;i<3;i++) {
    bool but=button[i];
    button[i]=bitRead(v,i+5)==1;
    if(but!=button[i]){
      refr=true;
    }
  }

  uint8_t pos_n=getBitPos(v);
  if(pos_n!=pos){
    pos=pos_n;
    refr=true;
  }
  return refr;
}
