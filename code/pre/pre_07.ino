#include <stdlib.h>
#include <SPI.h>
#include <Wire.h>

#include "VolumeRotary.h"
#include "InputRotary.h"
#include "OutputPre.h"

#include "OLED_Driver.h"
#include "GUI_paint.h"
#include "DEV_Config.h"
#include "Debug.h"


#include "DS1307.h"
DS1307 clock;
RTCDateTime dt, dtt;

#define WIDTH      96
#define HEIGHT     64
#define PAGES       8

#define OLED_RST    9 
#define OLED_DC     8
#define OLED_CS    10
#define SPI_MOSI   11    /* connect to the DIN pin of OLED */
#define SPI_SCK    13     /* connect to the CLK pin of OLED */

#define LEN 48


OutputPre out;
VolumeRotary vol;
InputRotary inp;

//#define VOL_STEPS 23
//#define INPUT_STEPS 5

// stałe
//const uint8_t volStep[23]={128,130,132,134,136,138,140,142,146,150,154,158,162,166,170,175,180,185,190,195,209,232,255};
//const uint8_t volStep[23]={255,167,147,140,134,132,127,124,119,114,111,105,102,96,89,83,78,71,65,60,45,22,0};
//const uint8_t volStep[23]={255,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0};
//const uint8_t volStep[23]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22};
//const uint8_t volStep[23]={23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45};
//const uint8_t volStep[23]={46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68};
//const uint8_t volStep[23]={234,235,236,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255};
//const uint8_t volStep[23]={188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210};

//const uint8_t volStep[VOL_STEPS]={0,57,128,140,148,156,164,170,176,182,206,210,214,218,222,234,238,242,246,250,252,253,254};
const uint8_t volStep[VOL_STEPS]={0,51,135,143,151,159,167,175,183,189,195,201,207,213,219,225,231,235,239,243,247,251,254};

const char* inStrTxt[]={"OFF","DAC","PHONO","MAC","AUX1","AUX2"};
//const char* onoff[]={"OFF","ON"};
const char* mon[]={"Sty","Lut","Mar","Kwi","Maj","Cze","Lip","Sie","Wrz","Paz","Lis","Gru"};

//UBYTE *BlackImage;
UBYTE BlackImage[1024];
char buf[11]; // 30 znaków + null

void setup() {
  Serial.begin(115200);
  Serial.println("Start");

  //pinMode(LED_BYPASS, OUTPUT);
  //pinMode(LED_OUT_OFF, OUTPUT);

  // Initialize DS1307
  Serial.println("Initialize DS1307");;
  clock.begin();

/*
  // If date not set
  if (!clock.isReady()) 
  {
    // Set sketch compiling time
    clock.setDateTime(__DATE__, __TIME__);
  }
*/
  System_Init();
  Serial.print(F("OLED_Init()...\r\n"));
  OLED_Init();
  Driver_Delay_ms(500); 
  //0.Create a new image cache
  UWORD Imagesize = ((OLED_WIDTH % 8 == 0)? (OLED_WIDTH / 8 ): (OLED_WIDTH / 8 + 1)) * OLED_HEIGHT;
  //Serial.print(Imagesize);
  /*if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
      Serial.print(F("Failed to apply for black memory...\r\n"));
      return;
  }*/
  Paint_NewImage(BlackImage, OLED_WIDTH, OLED_HEIGHT, 180, BLACK);  

  //1.Select Image
  Paint_SelectImage(BlackImage);
  Paint_Clear(BLACK);
  Driver_Delay_ms(10); 


  // MCP start
  out.begin(7,6,50);
  vol.begin(4,5);
  inp.begin(3);
  
  Serial.println("Init end");
}


void loop() {
  uint8_t Vpos=0;
  uint8_t Ipos=0;
  bool refreshV=false;
  bool refreshI=false;
  bool refreshT=false;
  bool but[3]={false,false,false};

  while(true) {
  
    if(vol.refresh()) {
      Vpos=vol.getPos();
      refreshV=true;  
    }
    
    if(inp.refresh()) {
      Ipos=inp.getPos();
      for(uint8_t i=0;i<3;i++) {
        but[i]=inp.getButton(i);
      }
      refreshI=true;  
    }
  
    if(refreshV) {
      sprintf(buf,"Vol: ");
      Serial.println(buf);
      sprintf(buf,"%d/%d",Vpos,volStep[Vpos-1]);
      Serial.println(buf);
      out.setVolume(volStep[Vpos-1]);      
    }
  
    if(refreshI) {
      sprintf(buf,"Input: %d ",Ipos);
      Serial.print(buf);
 //     sprintf(buf,"dir: %d ",but[0]);
 //     Serial.print(buf);
 //     sprintf(buf,"o.off: %d ",but[1]);
 //     Serial.println(buf);
      out.clearInput();
      delay(50);
      out.setInput(Ipos);     
      out.setDirect(but[0]);
      out.setOutOff(but[1]); 
    }

    dtt = clock.getDateTime();
    if(dtt.second!=dt.second) {
      dt=dtt;
      refreshT=true;
      sprintf(buf,"%02d:%02d:%02d ",dt.hour,dt.minute,dt.second);
      Serial.print(buf);
      sprintf(buf,"%4d-%02d-%02d ",dt.year,dt.month,dt.day);
      Serial.print(buf);
      sprintf(buf,"%d/%d",Vpos,volStep[Vpos-1]);
      Serial.println(buf);      
    }
      

  if(refreshV or refreshI or refreshT) {
    Paint_Clear(BLACK);
  
    sprintf(buf,"%d",Ipos);
    Paint_DrawString_EN(0, 24, buf, &Font24, WHITE, WHITE);
    Paint_DrawString_EN(34, 14, inStrTxt[Ipos], &Font16, WHITE, WHITE);

    uint8_t percval=(uint8_t)((float)(Vpos-1)/22.0*100);
    sprintf(buf,"%d",percval);
    Paint_DrawString_EN(40, 52, buf, &Font12, WHITE, WHITE);
    sprintf(buf,"%%");
    Paint_DrawString_EN(62, 52, buf, &Font12, WHITE, WHITE);


    // wartość w dB - 0 to -127.5dB, 255 to 0 dB
    float dbval=(float)(255-volStep[Vpos-1])/2.0;
    if(volStep[Vpos-1]<64) {
      dbval=dbval-32.0; // ostatni bit to 32 db, nie 64 - wyjaśnienie w Excelu
    }
    dtostrf(-dbval,5,1,buf);    
    Paint_DrawString_EN(80, 56, buf, &Font8, WHITE, WHITE);
    sprintf(buf,"db");
    Paint_DrawString_EN(112, 56,buf, &Font8, WHITE, WHITE);
    

    //sprintf(buf,"Mute:");
    //Paint_DrawString_EN(34, 30,buf, &Font8, WHITE, WHITE);
    //sprintf(buf,"Direct:");
    //Paint_DrawString_EN(34, 40,buf, &Font8, WHITE, WHITE);
    //onoff[but[1] ? 1:0].toCharArray(buf,sizeof(buf));
    //Paint_DrawString_EN(78, 30,onoff[but[1] ? 1:0], &Font8, WHITE, WHITE);
    //onoff[but[0] ? 1:0].toCharArray(buf,sizeof(buf));
    //Paint_DrawString_EN(78, 40,onoff[but[0] ? 1:0], &Font8, WHITE, WHITE);
    
  
    
    //dt = clock.getDateTime();
    sprintf(buf,"%02d.",dt.day);
    Paint_DrawString_EN(0, 0,buf, &Font12, WHITE, WHITE);
    strcpy(buf,mon[dt.month-1]);
    Paint_DrawString_EN(19, 0,buf, &Font12, WHITE, WHITE);
    sprintf(buf,"%02d:%02d:%02d",dt.hour,dt.minute,dt.second);
    Paint_DrawString_EN(64, 0,buf, &Font12, WHITE, WHITE);

    drawLineH(0,127,12);
    drawLineV(12,63,32);
    drawLineH(32,127,50);
    
    OLED_Display(BlackImage);
    Driver_Delay_ms(10);  
  }
  
  refreshV=false;
  refreshI=false;
  refreshT=false;
  delay(100);
  }
}

void drawLineH(UWORD xs,UWORD xe, UWORD y) {
  for(UWORD i=xs;i<xe+1;i++) {
      Paint_SetPixel(i,y, WHITE);
  }
}

void drawLineV(UWORD ys,UWORD ye, UWORD x) {
  for(UWORD i=ys;i<ye+1;i++) {
      Paint_SetPixel(x,i, WHITE);
  }
}
