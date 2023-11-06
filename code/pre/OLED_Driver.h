/******************************************************************************
* | file        : OLED_Driver.c
* | version     : V1.0
* | date        : 2020-06-16
* | function    : SH1107 Drive function   
******************************************************************************/
#ifndef __OLED_DRIVER_H
#define __OLED_DRIVER_H		

#include "DEV_Config.h"
#include "stdio.h"

/********************************************************************************
function:	
		Define the full screen height length of the display
********************************************************************************/

#define OLED_WIDTH  128//OLED width
#define OLED_HEIGHT 64 //OLED height

void OLED_Init(void);
void OLED_WriteReg(uint8_t Reg);
void OLED_WriteData(uint8_t Data);
void OLED_Clear(void);
void OLED_Display(UBYTE *Image);
UBYTE reverse(UBYTE temp);

#endif  
	 
