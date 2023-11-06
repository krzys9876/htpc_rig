#include "VolumeRotary.h"



VolumeRotary::VolumeRotary() {
  pos=0;
}

void VolumeRotary::begin(uint8_t addr1, uint8_t addr2) {
  mcp1.begin(addr1);
  mcp2.begin(addr2);

  for(uint8_t i=0;i<16;i++) {
    mcp1.pinMode(i, INPUT);
    mcp1.pullUp(i, HIGH);
    mcp2.pinMode(i, INPUT);
    mcp2.pullUp(i, HIGH);
  }
}

uint16_t VolumeRotary::read1() {
  return mcp1.readGPIOAB();   
}

uint16_t VolumeRotary::read2() {
  return mcp2.readGPIOAB();   
}

uint8_t VolumeRotary::getPos() {
  return pos;
}

uint8_t VolumeRotary::getBit(uint16_t in, boolean skip0=true) {
  for(uint8_t i=(skip0) ? 1 : 0;i<16;i++) {
    if(bitRead(in,i)) {
      return i+1;
    }
  }
  return 0;
}

uint8_t VolumeRotary::getBitPos(uint16_t in1,uint16_t in2) {
  uint8_t p;
  
  p=getBit(in1,true);
  if(p>1) {
    return p;
  }

  p=getBit(in2,false);
  if(p>0) {
    return p+16;
  } else {
    // gpio1=1 i gpio2=0, to zwracamy 0, ale tylko wtedy
    return 1;
  }
}

bool VolumeRotary::refresh() {
  uint16_t v1=read1();
  uint16_t v2=read2();

  v1=v1 ^ 65535;
  v2=v2 ^ 65535;

  uint8_t pos_n=getBitPos(v1,v2);
  if(pos_n!=pos){
    pos=pos_n;
    return true;
  }
  return false;
}
