#include <SPI.h>
#include <Wire.h>
#include <Adafruit_MCP23017.h>

#define VOL_STEPS 23
#define INPUT_STEPS 5

class OutputPre {
    public:

    OutputPre(void);

    void begin(uint8_t addrV, uint8_t addrI,  unsigned long del);
    void setInput(uint8_t in);
    void setVolume(uint8_t v);
    void setDirect(bool in);
    void setOutOff(bool in);
    void clearInput();

  private:

    uint8_t getVolBit(uint8_t bit,uint8_t val);
    
    Adafruit_MCP23017 mcpV;
    Adafruit_MCP23017 mcpI;
    unsigned long relDelay;
};
