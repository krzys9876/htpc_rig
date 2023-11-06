EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Connector:Screw_Terminal_01x03 J6
U 1 1 5F9C313F
P 2050 5850
F 0 "J6" V 2014 5662 50  0000 R CNN
F 1 "OUTPUT_PRE" V 1923 5662 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 2050 5850 50  0001 C CNN
F 3 "~" H 2050 5850 50  0001 C CNN
	1    2050 5850
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1350 7350 1100 7350
Wire Wire Line
	2750 7350 2800 7350
Text Notes 1400 8100 0    50   ~ 0
Wyjście PRE (z przedwzmacniacza) jest domyślnie podłączone
NoConn ~ 2800 7750
Wire Wire Line
	1950 6050 1950 6350
Wire Wire Line
	1950 6350 2200 6350
Wire Wire Line
	2200 6350 2200 7250
Wire Wire Line
	2200 7250 1950 7250
Wire Wire Line
	2850 6350 2300 6350
Wire Wire Line
	2300 6350 2300 7450
Wire Wire Line
	2300 7450 1950 7450
Wire Wire Line
	2400 7650 2400 6250
Wire Wire Line
	2400 6250 2050 6250
Wire Wire Line
	2050 6250 2050 6050
Wire Wire Line
	1950 7650 2400 7650
Wire Wire Line
	2950 6250 2500 6250
Wire Wire Line
	2500 6250 2500 7850
Wire Wire Line
	2500 7850 1950 7850
Wire Wire Line
	2150 6050 2150 6150
Wire Wire Line
	2150 6150 3600 6150
Wire Wire Line
	3600 6150 3600 7250
Wire Wire Line
	3400 7250 3600 7250
Wire Wire Line
	3050 6050 3700 6050
Wire Wire Line
	3700 6050 3700 7450
Wire Wire Line
	3700 7450 3400 7450
Wire Wire Line
	1100 7350 1100 8200
Wire Wire Line
	1350 7750 1200 7750
Wire Wire Line
	1200 7750 1200 8300
NoConn ~ 3400 7650
NoConn ~ 3400 7850
$Comp
L Connector:Screw_Terminal_01x03 J8
U 1 1 5FAD8F41
P 5500 8300
F 0 "J8" H 5580 8342 50  0000 L CNN
F 1 "OUTPUT" H 5580 8251 50  0000 L CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 5500 8300 50  0001 C CNN
F 3 "~" H 5500 8300 50  0001 C CNN
	1    5500 8300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5FB8F213
P 1100 900
F 0 "#PWR0102" H 1100 650 50  0001 C CNN
F 1 "GND" H 1105 727 50  0000 C CNN
F 2 "" H 1100 900 50  0001 C CNN
F 3 "" H 1100 900 50  0001 C CNN
	1    1100 900 
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5FB8FC2D
P 850 800
F 0 "#FLG0101" H 850 875 50  0001 C CNN
F 1 "PWR_FLAG" H 850 973 50  0000 C CNN
F 2 "" H 850 800 50  0001 C CNN
F 3 "~" H 850 800 50  0001 C CNN
	1    850  800 
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG0102
U 1 1 5FB907EC
P 1350 800
F 0 "#FLG0102" H 1350 875 50  0001 C CNN
F 1 "PWR_FLAG" H 1350 973 50  0000 C CNN
F 2 "" H 1350 800 50  0001 C CNN
F 3 "~" H 1350 800 50  0001 C CNN
	1    1350 800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	600  850  850  850 
Wire Wire Line
	850  850  850  800 
Wire Wire Line
	1100 900  1100 850 
Wire Wire Line
	1100 850  1350 850 
Wire Wire Line
	1350 850  1350 800 
$Comp
L Device:C C1
U 1 1 5FD0754C
P 1700 850
F 0 "C1" H 1815 896 50  0000 L CNN
F 1 "100n" H 1815 805 50  0000 L CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 1738 700 50  0001 C CNN
F 3 "~" H 1700 850 50  0001 C CNN
	1    1700 850 
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C2
U 1 1 5FD0805C
P 2050 850
F 0 "C2" H 2168 896 50  0000 L CNN
F 1 "10u" H 2168 805 50  0000 L CNN
F 2 "Capacitor_SMD:C_1210_3225Metric" H 2088 700 50  0001 C CNN
F 3 "~" H 2050 850 50  0001 C CNN
	1    2050 850 
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0108
U 1 1 5FD08E6F
P 1700 1000
F 0 "#PWR0108" H 1700 750 50  0001 C CNN
F 1 "GND" H 1705 827 50  0000 C CNN
F 2 "" H 1700 1000 50  0001 C CNN
F 3 "" H 1700 1000 50  0001 C CNN
	1    1700 1000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1700 700  2050 700 
Wire Wire Line
	1700 1000 2050 1000
Connection ~ 1700 1000
Wire Wire Line
	600  750  600  850 
$Comp
L Connector:Screw_Terminal_01x02 J12
U 1 1 5FFAE2C4
P 2500 800
F 0 "J12" H 2580 792 50  0000 L CNN
F 1 "POWER" H 2580 701 50  0000 L CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00001_1x02_P5.00mm_Horizontal" H 2500 800 50  0001 C CNN
F 3 "~" H 2500 800 50  0001 C CNN
	1    2500 800 
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 62550052
P 600 750
F 0 "#PWR01" H 600 600 50  0001 C CNN
F 1 "+5V" H 615 923 50  0000 C CNN
F 2 "" H 600 750 50  0001 C CNN
F 3 "" H 600 750 50  0001 C CNN
	1    600  750 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 800  2300 700 
Wire Wire Line
	2300 700  2050 700 
Connection ~ 2050 700 
Wire Wire Line
	2300 900  2300 1000
Wire Wire Line
	2300 1000 2050 1000
Connection ~ 2050 1000
$Comp
L power:+5V #PWR04
U 1 1 6264A72C
P 1700 700
F 0 "#PWR04" H 1700 550 50  0001 C CNN
F 1 "+5V" H 1715 873 50  0000 C CNN
F 2 "" H 1700 700 50  0001 C CNN
F 3 "" H 1700 700 50  0001 C CNN
	1    1700 700 
	1    0    0    -1  
$EndComp
Connection ~ 1700 700 
$Comp
L Connector:Screw_Terminal_01x03 J1
U 1 1 5F86139D
P 2200 1750
F 0 "J1" V 2164 1562 50  0000 R CNN
F 1 "INPUT1" V 2073 1562 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 2200 1750 50  0001 C CNN
F 3 "~" H 2200 1750 50  0001 C CNN
	1    2200 1750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1450 3350 1250 3350
Wire Wire Line
	1250 3350 1250 2200
Wire Wire Line
	1250 2200 2100 2200
Wire Wire Line
	2100 2200 2100 1950
Wire Wire Line
	2200 1950 2200 2100
Wire Wire Line
	2200 2100 1150 2100
Wire Wire Line
	1150 2100 1150 3750
Wire Wire Line
	1150 3750 1450 3750
Wire Wire Line
	2300 3350 2500 3350
$Comp
L Connector:Screw_Terminal_01x03 J10
U 1 1 5F89F82D
P 15500 4200
F 0 "J10" H 15580 4242 50  0000 L CNN
F 1 "INPUT" H 15580 4151 50  0000 L CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 15500 4200 50  0001 C CNN
F 3 "~" H 15500 4200 50  0001 C CNN
	1    15500 4200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 3450 3250 4300
NoConn ~ 3100 3850
NoConn ~ 3100 3650
NoConn ~ 2500 3750
$Comp
L Relay:AZ850P2-x KC1
U 1 1 6264AD8F
P 1750 3350
F 0 "KC1" V 2517 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 2426 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 2300 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 1750 3350 50  0001 C CNN
	1    1750 3350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG1
U 1 1 628ADABE
P 2800 3350
F 0 "KG1" V 3567 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 3476 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 3350 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 2800 3350 50  0001 C CNN
	1    2800 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	2300 1950 2300 3350
Wire Wire Line
	2200 4100 2200 3450
Wire Wire Line
	2200 3450 2050 3450
Wire Wire Line
	2100 4200 2100 3850
Wire Wire Line
	2100 3850 2050 3850
NoConn ~ 2050 3650
NoConn ~ 2050 3250
Wire Wire Line
	3250 3450 3100 3450
$Comp
L power:+5V #PWR05
U 1 1 62D6B7A1
P 1750 2600
F 0 "#PWR05" H 1750 2450 50  0001 C CNN
F 1 "+5V" H 1765 2773 50  0000 C CNN
F 2 "" H 1750 2600 50  0001 C CNN
F 3 "" H 1750 2600 50  0001 C CNN
	1    1750 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1450 2850 1450 2650
Wire Wire Line
	1450 2650 1750 2650
Wire Wire Line
	2050 2650 2050 2850
Wire Wire Line
	1750 2650 1750 2600
Connection ~ 1750 2650
Wire Wire Line
	1750 2650 2050 2650
Wire Wire Line
	2500 2850 2500 2650
Wire Wire Line
	2500 2650 2800 2650
Wire Wire Line
	3100 2650 3100 2850
$Comp
L power:+5V #PWR07
U 1 1 63039390
P 2800 2600
F 0 "#PWR07" H 2800 2450 50  0001 C CNN
F 1 "+5V" H 2815 2773 50  0000 C CNN
F 2 "" H 2800 2600 50  0001 C CNN
F 3 "" H 2800 2600 50  0001 C CNN
	1    2800 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2800 2650 2800 2600
Connection ~ 2800 2650
Wire Wire Line
	2800 2650 3100 2650
Wire Wire Line
	1450 3050 1300 3050
Wire Wire Line
	2050 3050 2200 3050
Wire Wire Line
	2500 3050 2350 3050
Wire Wire Line
	3100 3050 3250 3050
NoConn ~ 3100 3250
Wire Wire Line
	2200 4100 2850 4100
Wire Wire Line
	3250 4300 5700 4300
Wire Wire Line
	2100 4200 2950 4200
$Comp
L Connector:Screw_Terminal_01x03 J2
U 1 1 63BF0DBA
P 4650 1750
F 0 "J2" V 4614 1562 50  0000 R CNN
F 1 "INPUT2" V 4523 1562 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 4650 1750 50  0001 C CNN
F 3 "~" H 4650 1750 50  0001 C CNN
	1    4650 1750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3900 3350 3700 3350
Wire Wire Line
	3700 3350 3700 2200
Wire Wire Line
	3700 2200 4550 2200
Wire Wire Line
	4550 2200 4550 1950
Wire Wire Line
	4650 1950 4650 2100
Wire Wire Line
	4650 2100 3600 2100
Wire Wire Line
	3600 2100 3600 3750
Wire Wire Line
	3600 3750 3900 3750
Wire Wire Line
	4750 3350 4950 3350
Wire Wire Line
	5700 3450 5700 4300
NoConn ~ 5550 3850
NoConn ~ 5550 3650
NoConn ~ 4950 3750
$Comp
L Relay:AZ850P2-x KC2
U 1 1 63BF1CFB
P 4200 3350
F 0 "KC2" V 4967 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 4876 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 4750 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 4200 3350 50  0001 C CNN
	1    4200 3350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG2
U 1 1 63BF1D05
P 5250 3350
F 0 "KG2" V 6017 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 5926 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 5800 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 5250 3350 50  0001 C CNN
	1    5250 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	4750 1950 4750 3350
Wire Wire Line
	4650 4100 4650 3450
Wire Wire Line
	4650 3450 4500 3450
Wire Wire Line
	4550 4200 4550 3850
Wire Wire Line
	4550 3850 4500 3850
NoConn ~ 4500 3650
NoConn ~ 4500 3250
Wire Wire Line
	5700 3450 5550 3450
$Comp
L power:+5V #PWR013
U 1 1 63BF1D17
P 4200 2600
F 0 "#PWR013" H 4200 2450 50  0001 C CNN
F 1 "+5V" H 4215 2773 50  0000 C CNN
F 2 "" H 4200 2600 50  0001 C CNN
F 3 "" H 4200 2600 50  0001 C CNN
	1    4200 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3900 2850 3900 2650
Wire Wire Line
	3900 2650 4200 2650
Wire Wire Line
	4500 2650 4500 2850
Wire Wire Line
	4200 2650 4200 2600
Connection ~ 4200 2650
Wire Wire Line
	4200 2650 4500 2650
Wire Wire Line
	4950 2850 4950 2650
Wire Wire Line
	4950 2650 5250 2650
Wire Wire Line
	5550 2650 5550 2850
$Comp
L power:+5V #PWR018
U 1 1 63BF1D2A
P 5250 2600
F 0 "#PWR018" H 5250 2450 50  0001 C CNN
F 1 "+5V" H 5265 2773 50  0000 C CNN
F 2 "" H 5250 2600 50  0001 C CNN
F 3 "" H 5250 2600 50  0001 C CNN
	1    5250 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	5250 2650 5250 2600
Connection ~ 5250 2650
Wire Wire Line
	5250 2650 5550 2650
Wire Wire Line
	3900 3050 3750 3050
Wire Wire Line
	4500 3050 4650 3050
Wire Wire Line
	4950 3050 4800 3050
Wire Wire Line
	5550 3050 5700 3050
NoConn ~ 5550 3250
Connection ~ 4550 4200
Wire Wire Line
	4550 4200 7000 4200
Connection ~ 4650 4100
Wire Wire Line
	4650 4100 7100 4100
Connection ~ 5700 4300
Wire Wire Line
	5700 4300 8150 4300
$Comp
L Connector:Screw_Terminal_01x03 J3
U 1 1 63C9B070
P 7100 1750
F 0 "J3" V 7064 1562 50  0000 R CNN
F 1 "INPUT3" V 6973 1562 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 7100 1750 50  0001 C CNN
F 3 "~" H 7100 1750 50  0001 C CNN
	1    7100 1750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6350 3350 6150 3350
Wire Wire Line
	6150 3350 6150 2200
Wire Wire Line
	6150 2200 7000 2200
Wire Wire Line
	7000 2200 7000 1950
Wire Wire Line
	7100 1950 7100 2100
Wire Wire Line
	7100 2100 6050 2100
Wire Wire Line
	6050 2100 6050 3750
Wire Wire Line
	6050 3750 6350 3750
Wire Wire Line
	7200 3350 7400 3350
Wire Wire Line
	8150 3450 8150 4300
NoConn ~ 8000 3850
NoConn ~ 8000 3650
NoConn ~ 7400 3750
$Comp
L Relay:AZ850P2-x KC3
U 1 1 63C9C0A5
P 6650 3350
F 0 "KC3" V 7417 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 7326 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 7200 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 6650 3350 50  0001 C CNN
	1    6650 3350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG3
U 1 1 63C9C0AF
P 7700 3350
F 0 "KG3" V 8467 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 8376 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 8250 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 7700 3350 50  0001 C CNN
	1    7700 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	7200 1950 7200 3350
Wire Wire Line
	7100 4100 7100 3450
Wire Wire Line
	7100 3450 6950 3450
Wire Wire Line
	7000 4200 7000 3850
Wire Wire Line
	7000 3850 6950 3850
NoConn ~ 6950 3650
NoConn ~ 6950 3250
Wire Wire Line
	8150 3450 8000 3450
$Comp
L power:+5V #PWR019
U 1 1 63C9C0C1
P 6650 2600
F 0 "#PWR019" H 6650 2450 50  0001 C CNN
F 1 "+5V" H 6665 2773 50  0000 C CNN
F 2 "" H 6650 2600 50  0001 C CNN
F 3 "" H 6650 2600 50  0001 C CNN
	1    6650 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 2850 6350 2650
Wire Wire Line
	6350 2650 6650 2650
Wire Wire Line
	6950 2650 6950 2850
Wire Wire Line
	6650 2650 6650 2600
Connection ~ 6650 2650
Wire Wire Line
	6650 2650 6950 2650
Wire Wire Line
	7400 2850 7400 2650
Wire Wire Line
	7400 2650 7700 2650
Wire Wire Line
	8000 2650 8000 2850
$Comp
L power:+5V #PWR020
U 1 1 63C9C0D4
P 7700 2600
F 0 "#PWR020" H 7700 2450 50  0001 C CNN
F 1 "+5V" H 7715 2773 50  0000 C CNN
F 2 "" H 7700 2600 50  0001 C CNN
F 3 "" H 7700 2600 50  0001 C CNN
	1    7700 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	7700 2650 7700 2600
Connection ~ 7700 2650
Wire Wire Line
	7700 2650 8000 2650
Wire Wire Line
	6350 3050 6200 3050
Wire Wire Line
	6950 3050 7100 3050
Wire Wire Line
	7400 3050 7250 3050
Wire Wire Line
	8000 3050 8150 3050
NoConn ~ 8000 3250
Connection ~ 7000 4200
Wire Wire Line
	7000 4200 9550 4200
Connection ~ 7100 4100
Wire Wire Line
	7100 4100 9650 4100
Connection ~ 8150 4300
Wire Wire Line
	8150 4300 10700 4300
$Comp
L Connector:Screw_Terminal_01x03 J4
U 1 1 63CFD7D4
P 9650 1750
F 0 "J4" V 9614 1562 50  0000 R CNN
F 1 "INPUT4" V 9523 1562 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 9650 1750 50  0001 C CNN
F 3 "~" H 9650 1750 50  0001 C CNN
	1    9650 1750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8900 3350 8700 3350
Wire Wire Line
	8700 3350 8700 2200
Wire Wire Line
	8700 2200 9550 2200
Wire Wire Line
	9550 2200 9550 1950
Wire Wire Line
	9650 1950 9650 2100
Wire Wire Line
	9650 2100 8600 2100
Wire Wire Line
	8600 2100 8600 3750
Wire Wire Line
	8600 3750 8900 3750
Wire Wire Line
	9750 3350 9950 3350
Wire Wire Line
	10700 3450 10700 4300
NoConn ~ 10550 3850
NoConn ~ 10550 3650
NoConn ~ 9950 3750
$Comp
L Relay:AZ850P2-x KC4
U 1 1 63CFE8FD
P 9200 3350
F 0 "KC4" V 9967 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 9876 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 9750 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 9200 3350 50  0001 C CNN
	1    9200 3350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG4
U 1 1 63CFE907
P 10250 3350
F 0 "KG4" V 11017 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 10926 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 10800 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 10250 3350 50  0001 C CNN
	1    10250 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	9750 1950 9750 3350
Wire Wire Line
	9650 4100 9650 3450
Wire Wire Line
	9650 3450 9500 3450
Wire Wire Line
	9550 4200 9550 3850
Wire Wire Line
	9550 3850 9500 3850
NoConn ~ 9500 3650
NoConn ~ 9500 3250
Wire Wire Line
	10700 3450 10550 3450
$Comp
L power:+5V #PWR021
U 1 1 63CFE919
P 9200 2600
F 0 "#PWR021" H 9200 2450 50  0001 C CNN
F 1 "+5V" H 9215 2773 50  0000 C CNN
F 2 "" H 9200 2600 50  0001 C CNN
F 3 "" H 9200 2600 50  0001 C CNN
	1    9200 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	8900 2850 8900 2650
Wire Wire Line
	8900 2650 9200 2650
Wire Wire Line
	9500 2650 9500 2850
Wire Wire Line
	9200 2650 9200 2600
Connection ~ 9200 2650
Wire Wire Line
	9200 2650 9500 2650
Wire Wire Line
	9950 2850 9950 2650
Wire Wire Line
	9950 2650 10250 2650
Wire Wire Line
	10550 2650 10550 2850
$Comp
L power:+5V #PWR022
U 1 1 63CFE92C
P 10250 2600
F 0 "#PWR022" H 10250 2450 50  0001 C CNN
F 1 "+5V" H 10265 2773 50  0000 C CNN
F 2 "" H 10250 2600 50  0001 C CNN
F 3 "" H 10250 2600 50  0001 C CNN
	1    10250 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	10250 2650 10250 2600
Connection ~ 10250 2650
Wire Wire Line
	10250 2650 10550 2650
Wire Wire Line
	8900 3050 8750 3050
Wire Wire Line
	9500 3050 9650 3050
Wire Wire Line
	9950 3050 9800 3050
Wire Wire Line
	10550 3050 10700 3050
NoConn ~ 10550 3250
Connection ~ 9550 4200
Wire Wire Line
	9550 4200 12100 4200
Connection ~ 9650 4100
Wire Wire Line
	9650 4100 12200 4100
Connection ~ 10700 4300
Wire Wire Line
	10700 4300 13250 4300
$Comp
L Connector:Screw_Terminal_01x03 J5
U 1 1 63D69704
P 12200 1750
F 0 "J5" V 12164 1562 50  0000 R CNN
F 1 "INPUT5" V 12073 1562 50  0000 R CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00002_1x03_P5.00mm_Horizontal" H 12200 1750 50  0001 C CNN
F 3 "~" H 12200 1750 50  0001 C CNN
	1    12200 1750
	0    -1   -1   0   
$EndComp
Wire Wire Line
	11450 3350 11250 3350
Wire Wire Line
	11250 3350 11250 2200
Wire Wire Line
	11250 2200 12100 2200
Wire Wire Line
	12100 2200 12100 1950
Wire Wire Line
	12200 1950 12200 2100
Wire Wire Line
	12200 2100 11150 2100
Wire Wire Line
	11150 2100 11150 3750
Wire Wire Line
	11150 3750 11450 3750
Wire Wire Line
	12300 3350 12500 3350
Wire Wire Line
	13250 3450 13250 4300
NoConn ~ 13100 3850
NoConn ~ 13100 3650
NoConn ~ 12500 3750
$Comp
L Relay:AZ850P2-x KC5
U 1 1 63D6A921
P 11750 3350
F 0 "KC5" V 12517 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 12426 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 12300 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 11750 3350 50  0001 C CNN
	1    11750 3350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG5
U 1 1 63D6A92B
P 12800 3350
F 0 "KG5" V 13567 3350 50  0000 C CNN
F 1 "AZ850P2-x" V 13476 3350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 13350 3400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 12800 3350 50  0001 C CNN
	1    12800 3350
	0    1    1    0   
$EndComp
Wire Wire Line
	12300 1950 12300 3350
Wire Wire Line
	12200 4100 12200 3450
Wire Wire Line
	12200 3450 12050 3450
Wire Wire Line
	12100 4200 12100 3850
Wire Wire Line
	12100 3850 12050 3850
NoConn ~ 12050 3650
NoConn ~ 12050 3250
Wire Wire Line
	13250 3450 13100 3450
$Comp
L power:+5V #PWR023
U 1 1 63D6A93D
P 11750 2600
F 0 "#PWR023" H 11750 2450 50  0001 C CNN
F 1 "+5V" H 11765 2773 50  0000 C CNN
F 2 "" H 11750 2600 50  0001 C CNN
F 3 "" H 11750 2600 50  0001 C CNN
	1    11750 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	11450 2850 11450 2650
Wire Wire Line
	11450 2650 11750 2650
Wire Wire Line
	12050 2650 12050 2850
Wire Wire Line
	11750 2650 11750 2600
Connection ~ 11750 2650
Wire Wire Line
	11750 2650 12050 2650
Wire Wire Line
	12500 2850 12500 2650
Wire Wire Line
	12500 2650 12800 2650
Wire Wire Line
	13100 2650 13100 2850
$Comp
L power:+5V #PWR024
U 1 1 63D6A950
P 12800 2600
F 0 "#PWR024" H 12800 2450 50  0001 C CNN
F 1 "+5V" H 12815 2773 50  0000 C CNN
F 2 "" H 12800 2600 50  0001 C CNN
F 3 "" H 12800 2600 50  0001 C CNN
	1    12800 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	12800 2650 12800 2600
Connection ~ 12800 2650
Wire Wire Line
	12800 2650 13100 2650
Wire Wire Line
	11450 3050 11300 3050
Wire Wire Line
	12050 3050 12200 3050
Wire Wire Line
	12500 3050 12350 3050
Wire Wire Line
	13100 3050 13250 3050
NoConn ~ 13100 3250
Connection ~ 12100 4200
Wire Wire Line
	12100 4200 15300 4200
Connection ~ 12200 4100
Wire Wire Line
	12200 4100 15300 4100
Connection ~ 13250 4300
Wire Wire Line
	13250 4300 15300 4300
$Comp
L Relay:AZ850P2-x KC6
U 1 1 63F575E1
P 1650 7350
F 0 "KC6" V 2417 7350 50  0000 C CNN
F 1 "AZ850P2-x" V 2326 7350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 2200 7400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 1650 7350 50  0001 C CNN
	1    1650 7350
	0    1    1    0   
$EndComp
$Comp
L Relay:AZ850P2-x KG6
U 1 1 63F58EE4
P 3100 7350
F 0 "KG6" V 3867 7350 50  0000 C CNN
F 1 "AZ850P2-x" V 3776 7350 50  0000 C CNN
F 2 "Relay_THT:Relay_DPDT_FRT5" H 3650 7400 50  0001 C CNN
F 3 "http://www.azettler.com/pdfs/az850.pdf" H 3100 7350 50  0001 C CNN
	1    3100 7350
	0    1    1    0   
$EndComp
$Comp
L power:+5V #PWR02
U 1 1 6422DF7E
P 1650 6600
F 0 "#PWR02" H 1650 6450 50  0001 C CNN
F 1 "+5V" H 1665 6773 50  0000 C CNN
F 2 "" H 1650 6600 50  0001 C CNN
F 3 "" H 1650 6600 50  0001 C CNN
	1    1650 6600
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 6850 1350 6700
Wire Wire Line
	1350 6700 1650 6700
Wire Wire Line
	1950 6700 1950 6850
Wire Wire Line
	1650 6700 1650 6600
Connection ~ 1650 6700
Wire Wire Line
	1650 6700 1950 6700
Wire Wire Line
	2800 6850 2800 6700
Wire Wire Line
	2800 6700 3100 6700
Wire Wire Line
	3400 6700 3400 6850
$Comp
L power:+5V #PWR09
U 1 1 6436CD3F
P 3100 6600
F 0 "#PWR09" H 3100 6450 50  0001 C CNN
F 1 "+5V" H 3115 6773 50  0000 C CNN
F 2 "" H 3100 6600 50  0001 C CNN
F 3 "" H 3100 6600 50  0001 C CNN
	1    3100 6600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 6700 3100 6600
Connection ~ 3100 6700
Wire Wire Line
	3100 6700 3400 6700
Text Label 1300 3050 0    50   ~ 0
R1_R
Text Label 2050 3050 0    50   ~ 0
R1_S
Text Label 2350 3050 0    50   ~ 0
R1_R
Text Label 3100 3050 0    50   ~ 0
R1_S
Text Label 3750 3050 0    50   ~ 0
R2_R
Text Label 4500 3050 0    50   ~ 0
R2_S
Text Label 4800 3050 0    50   ~ 0
R2_R
Text Label 5550 3050 0    50   ~ 0
R2_S
Text Label 6200 3050 0    50   ~ 0
R3_R
Text Label 6950 3050 0    50   ~ 0
R3_S
Text Label 7250 3050 0    50   ~ 0
R3_R
Text Label 8000 3050 0    50   ~ 0
R3_S
Text Label 8750 3050 0    50   ~ 0
R4_R
Text Label 9500 3050 0    50   ~ 0
R4_S
Text Label 9800 3050 0    50   ~ 0
R4_R
Text Label 10550 3050 0    50   ~ 0
R4_S
Text Label 11300 3050 0    50   ~ 0
R5_R
Text Label 12050 3050 0    50   ~ 0
R5_S
Text Label 12350 3050 0    50   ~ 0
R5_R
Text Label 13100 3050 0    50   ~ 0
R5_S
Wire Wire Line
	1350 7050 1100 7050
Wire Wire Line
	1950 7050 2150 7050
Wire Wire Line
	2800 7050 2550 7050
Wire Wire Line
	3400 7050 3550 7050
Text Label 1100 7050 0    50   ~ 0
R6_R
Text Label 1950 7050 0    50   ~ 0
R6_S
Text Label 2550 7050 0    50   ~ 0
R6_R
Text Label 3400 7050 0    50   ~ 0
R6_S
Wire Wire Line
	2750 7350 2750 8400
Wire Wire Line
	5300 8400 2750 8400
Wire Wire Line
	1100 8200 5300 8200
Wire Wire Line
	1200 8300 5300 8300
$Comp
L Connector:Screw_Terminal_01x02 J13
U 1 1 60199B35
P 3200 800
F 0 "J13" H 3280 792 50  0000 L CNN
F 1 "POWER2" H 3280 701 50  0000 L CNN
F 2 "TerminalBlock_RND:TerminalBlock_RND_205-00001_1x02_P5.00mm_Horizontal" H 3200 800 50  0001 C CNN
F 3 "~" H 3200 800 50  0001 C CNN
	1    3200 800 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2300 700  3000 700 
Wire Wire Line
	3000 700  3000 800 
Connection ~ 2300 700 
Wire Wire Line
	2300 1000 3000 1000
Wire Wire Line
	3000 1000 3000 900 
Connection ~ 2300 1000
Wire Wire Line
	3050 4300 3250 4300
Connection ~ 3250 4300
Connection ~ 2950 4200
Wire Wire Line
	2950 4200 4550 4200
Connection ~ 2850 4100
Wire Wire Line
	2850 4100 4650 4100
Wire Wire Line
	3050 4300 3050 6050
Wire Wire Line
	2950 4200 2950 6250
Wire Wire Line
	2850 4100 2850 6350
Text Notes 14750 3900 0    50   ~ 0
Do wejścia PRE (volume jest ZA PRE)
Text Notes 1350 5600 0    50   ~ 0
Z wyjścia PRE (volume jest ZA PRE)
Text Notes 5100 7900 0    50   ~ 0
Do wejścia VOLUME
$Comp
L Connector_Generic:Conn_02x08_Odd_Even J7
U 1 1 5FFDDD48
P 8150 5700
F 0 "J7" H 8200 6217 50  0000 C CNN
F 1 "CONTROL" H 8200 6126 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x08_P2.54mm_Vertical_SMD" H 8150 5700 50  0001 C CNN
F 3 "~" H 8150 5700 50  0001 C CNN
	1    8150 5700
	1    0    0    -1  
$EndComp
Wire Wire Line
	7950 5400 7550 5400
Wire Wire Line
	7950 5500 7550 5500
Wire Wire Line
	7950 5600 7550 5600
Wire Wire Line
	7950 5700 7550 5700
Wire Wire Line
	7950 5800 7550 5800
Wire Wire Line
	7950 5900 7550 5900
Wire Wire Line
	7950 6000 7550 6000
Wire Wire Line
	7950 6100 7550 6100
Wire Wire Line
	8450 5400 8850 5400
Wire Wire Line
	8450 5500 8850 5500
Wire Wire Line
	8450 5600 8850 5600
Wire Wire Line
	8450 5700 8850 5700
Wire Wire Line
	8450 5800 8850 5800
Wire Wire Line
	8450 5900 8850 5900
Wire Wire Line
	8450 6000 8850 6000
Wire Wire Line
	8450 6100 8850 6100
Text Label 7650 5400 0    50   ~ 0
R1_R
Text Label 7650 5500 0    50   ~ 0
R2_R
Text Label 7650 5600 0    50   ~ 0
R3_R
Text Label 7650 5700 0    50   ~ 0
R4_R
Text Label 7650 5800 0    50   ~ 0
R5_R
Text Label 7650 5900 0    50   ~ 0
R6_R
Text Label 7650 6000 0    50   ~ 0
R7_R
Text Label 7650 6100 0    50   ~ 0
R8_R
Text Label 8550 5400 0    50   ~ 0
R1_S
Text Label 8550 5500 0    50   ~ 0
R2_S
Text Label 8550 5600 0    50   ~ 0
R3_S
Text Label 8550 5700 0    50   ~ 0
R4_S
Text Label 8550 5800 0    50   ~ 0
R5_S
Text Label 8550 5900 0    50   ~ 0
R6_S
Text Label 8550 6000 0    50   ~ 0
R7_S
Text Label 8550 6100 0    50   ~ 0
R8_S
NoConn ~ 7550 6000
NoConn ~ 7550 6100
NoConn ~ 8850 6100
NoConn ~ 8850 6000
$Comp
L Mechanical:MountingHole H1
U 1 1 602AD488
P 5000 750
F 0 "H1" H 5100 796 50  0000 L CNN
F 1 "MountingHole" H 5100 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 5000 750 50  0001 C CNN
F 3 "~" H 5000 750 50  0001 C CNN
	1    5000 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 602ADC79
P 5950 750
F 0 "H2" H 6050 796 50  0000 L CNN
F 1 "MountingHole" H 6050 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 5950 750 50  0001 C CNN
F 3 "~" H 5950 750 50  0001 C CNN
	1    5950 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 602ADE95
P 6900 750
F 0 "H3" H 7000 796 50  0000 L CNN
F 1 "MountingHole" H 7000 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 6900 750 50  0001 C CNN
F 3 "~" H 6900 750 50  0001 C CNN
	1    6900 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 602AE0D5
P 7750 750
F 0 "H4" H 7850 796 50  0000 L CNN
F 1 "MountingHole" H 7850 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 7750 750 50  0001 C CNN
F 3 "~" H 7750 750 50  0001 C CNN
	1    7750 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H5
U 1 1 602B8B3D
P 8550 750
F 0 "H5" H 8650 796 50  0000 L CNN
F 1 "MountingHole" H 8650 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 8550 750 50  0001 C CNN
F 3 "~" H 8550 750 50  0001 C CNN
	1    8550 750 
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H6
U 1 1 602B96F1
P 9300 750
F 0 "H6" H 9400 796 50  0000 L CNN
F 1 "MountingHole" H 9400 705 50  0000 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3" H 9300 750 50  0001 C CNN
F 3 "~" H 9300 750 50  0001 C CNN
	1    9300 750 
	1    0    0    -1  
$EndComp
$EndSCHEMATC