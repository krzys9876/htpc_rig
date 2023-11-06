#include <SPI.h>
#include <Wire.h>
#include <Adafruit_MCP23017.h>


class VolumeRotary {
  public:

    VolumeRotary(void);

    void begin(uint8_t addr1, uint8_t addr2);
    uint8_t getPos();

    bool refresh();

  private:
    Adafruit_MCP23017 mcp1, mcp2;

    uint8_t pos;

    uint8_t getBit(uint16_t in, boolean skip0=true);
    uint8_t getBitPos(uint16_t in1,uint16_t in2);
    uint16_t read1();   
    uint16_t read2();  
};
