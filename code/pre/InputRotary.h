#include <SPI.h>
#include <Wire.h>
#include <Adafruit_MCP23008.h>


class InputRotary {
  public:

    InputRotary(void);

    void begin(uint8_t addr);
    uint8_t getPos();  
    bool getButton(uint8_t b);

    bool refresh();

  private:
    Adafruit_MCP23008 mcp;
    bool button[3];

    uint8_t pos;

    uint8_t getBit(uint8_t in);
    uint8_t getBitPos(uint8_t in);
    uint8_t read();   
};
