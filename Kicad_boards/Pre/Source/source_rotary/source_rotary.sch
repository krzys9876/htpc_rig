EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
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
L Interface_Expansion:MCP23008-xSS U1
U 1 1 60268E1C
P 4600 3200
F 0 "U1" H 4600 3981 50  0000 C CNN
F 1 "MCP23008-xSS" H 4600 3890 50  0000 C CNN
F 2 "Package_SO:SSOP-20_5.3x7.2mm_P0.65mm" H 4600 2150 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/MCP23008-MCP23S08-Data-Sheet-20001919F.pdf" H 5900 2000 50  0001 C CNN
	1    4600 3200
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_02x02_Odd_Even J1
U 1 1 602699E5
P 2250 2650
F 0 "J1" H 2300 2867 50  0000 C CNN
F 1 "ARD" H 2300 2776 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical_SMD" H 2250 2650 50  0001 C CNN
F 3 "~" H 2250 2650 50  0001 C CNN
	1    2250 2650
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J7
U 1 1 6026A18E
P 5600 3400
F 0 "J7" H 5680 3392 50  0000 L CNN
F 1 "AUX" H 5680 3301 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x02_P2.54mm_Vertical_SMD" H 5600 3400 50  0001 C CNN
F 3 "~" H 5600 3400 50  0001 C CNN
	1    5600 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5100 3300 5400 3300
Wire Wire Line
	5100 3400 5400 3400
Wire Wire Line
	5100 3500 5400 3500
$Comp
L Connector_Generic:Conn_01x01 J6
U 1 1 6026BAD1
P 5600 3200
F 0 "J6" H 5680 3242 50  0000 L CNN
F 1 "SRC_5" H 5680 3151 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 3200 50  0001 C CNN
F 3 "~" H 5600 3200 50  0001 C CNN
	1    5600 3200
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J5
U 1 1 6026C28A
P 5600 3100
F 0 "J5" H 5680 3142 50  0000 L CNN
F 1 "SRC_4" H 5680 3051 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 3100 50  0001 C CNN
F 3 "~" H 5600 3100 50  0001 C CNN
	1    5600 3100
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J4
U 1 1 6026C4F6
P 5600 3000
F 0 "J4" H 5680 3042 50  0000 L CNN
F 1 "SRC_3" H 5680 2951 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 3000 50  0001 C CNN
F 3 "~" H 5600 3000 50  0001 C CNN
	1    5600 3000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J3
U 1 1 6026C806
P 5600 2900
F 0 "J3" H 5680 2942 50  0000 L CNN
F 1 "SRC_2" H 5680 2851 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 2900 50  0001 C CNN
F 3 "~" H 5600 2900 50  0001 C CNN
	1    5600 2900
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J2
U 1 1 6026CA49
P 5600 2800
F 0 "J2" H 5680 2842 50  0000 L CNN
F 1 "SRC_1" H 5680 2751 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 2800 50  0001 C CNN
F 3 "~" H 5600 2800 50  0001 C CNN
	1    5600 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	5100 2800 5400 2800
Wire Wire Line
	5400 2900 5100 2900
Wire Wire Line
	5100 3000 5400 3000
Wire Wire Line
	5400 3100 5100 3100
Wire Wire Line
	5100 3200 5400 3200
NoConn ~ 4100 3200
$Comp
L power:+5V #PWR02
U 1 1 6026F8F7
P 2250 1850
F 0 "#PWR02" H 2250 1700 50  0001 C CNN
F 1 "+5V" H 2265 2023 50  0000 C CNN
F 2 "" H 2250 1850 50  0001 C CNN
F 3 "" H 2250 1850 50  0001 C CNN
	1    2250 1850
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 6026FD2A
P 2700 1850
F 0 "#PWR03" H 2700 1600 50  0001 C CNN
F 1 "GND" H 2705 1677 50  0000 C CNN
F 2 "" H 2700 1850 50  0001 C CNN
F 3 "" H 2700 1850 50  0001 C CNN
	1    2700 1850
	1    0    0    -1  
$EndComp
$Comp
L power:PWR_FLAG #FLG01
U 1 1 6026FF84
P 2000 1850
F 0 "#FLG01" H 2000 1925 50  0001 C CNN
F 1 "PWR_FLAG" H 2000 2023 50  0000 C CNN
F 2 "" H 2000 1850 50  0001 C CNN
F 3 "~" H 2000 1850 50  0001 C CNN
	1    2000 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2250 1850 2000 1850
$Comp
L power:PWR_FLAG #FLG02
U 1 1 6027086F
P 2500 1850
F 0 "#FLG02" H 2500 1925 50  0001 C CNN
F 1 "PWR_FLAG" H 2500 2023 50  0000 C CNN
F 2 "" H 2500 1850 50  0001 C CNN
F 3 "~" H 2500 1850 50  0001 C CNN
	1    2500 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2700 1850 2500 1850
$Comp
L power:+5V #PWR07
U 1 1 60270D4B
P 4600 2000
F 0 "#PWR07" H 4600 1850 50  0001 C CNN
F 1 "+5V" H 4615 2173 50  0000 C CNN
F 2 "" H 4600 2000 50  0001 C CNN
F 3 "" H 4600 2000 50  0001 C CNN
	1    4600 2000
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR01
U 1 1 60271566
P 1800 2650
F 0 "#PWR01" H 1800 2500 50  0001 C CNN
F 1 "+5V" H 1815 2823 50  0000 C CNN
F 2 "" H 1800 2650 50  0001 C CNN
F 3 "" H 1800 2650 50  0001 C CNN
	1    1800 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 2650 1950 2650
$Comp
L power:GND #PWR04
U 1 1 60271D3D
P 2850 2650
F 0 "#PWR04" H 2850 2400 50  0001 C CNN
F 1 "GND" H 2855 2477 50  0000 C CNN
F 2 "" H 2850 2650 50  0001 C CNN
F 3 "" H 2850 2650 50  0001 C CNN
	1    2850 2650
	1    0    0    -1  
$EndComp
Wire Wire Line
	2550 2650 2700 2650
Wire Wire Line
	2050 2750 2050 3000
Wire Wire Line
	2050 3000 4100 3000
Wire Wire Line
	2550 2750 2550 2900
Wire Wire Line
	2550 2900 4100 2900
$Comp
L power:+5V #PWR05
U 1 1 60272A27
P 3800 3400
F 0 "#PWR05" H 3800 3250 50  0001 C CNN
F 1 "+5V" H 3815 3573 50  0000 C CNN
F 2 "" H 3800 3400 50  0001 C CNN
F 3 "" H 3800 3400 50  0001 C CNN
	1    3800 3400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 60272EF8
P 3900 3650
F 0 "#PWR06" H 3900 3400 50  0001 C CNN
F 1 "GND" H 3905 3477 50  0000 C CNN
F 2 "" H 3900 3650 50  0001 C CNN
F 3 "" H 3900 3650 50  0001 C CNN
	1    3900 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 3500 4000 3500
Wire Wire Line
	3800 3500 3800 3400
Wire Wire Line
	4100 3600 4000 3600
Wire Wire Line
	4000 3600 4000 3500
Connection ~ 4000 3500
Wire Wire Line
	4000 3500 3800 3500
Wire Wire Line
	4100 3400 3900 3400
Wire Wire Line
	3900 3400 3900 3650
$Comp
L power:GND #PWR08
U 1 1 6027445D
P 4600 3900
F 0 "#PWR08" H 4600 3650 50  0001 C CNN
F 1 "GND" H 4605 3727 50  0000 C CNN
F 2 "" H 4600 3900 50  0001 C CNN
F 3 "" H 4600 3900 50  0001 C CNN
	1    4600 3900
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 3900 4600 3800
$Comp
L Device:C C2
U 1 1 60274E5A
P 4900 2250
F 0 "C2" H 5015 2296 50  0000 L CNN
F 1 "C" H 5015 2205 50  0000 L CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 4938 2100 50  0001 C CNN
F 3 "~" H 4900 2250 50  0001 C CNN
	1    4900 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 2000 4600 2100
$Comp
L power:GND #PWR09
U 1 1 60276A22
P 4900 2500
F 0 "#PWR09" H 4900 2250 50  0001 C CNN
F 1 "GND" H 4905 2327 50  0000 C CNN
F 2 "" H 4900 2500 50  0001 C CNN
F 3 "" H 4900 2500 50  0001 C CNN
	1    4900 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4900 2500 4900 2450
Wire Wire Line
	4900 2100 4600 2100
Connection ~ 4600 2100
Wire Wire Line
	4600 2100 4600 2600
$Comp
L Device:C C1
U 1 1 60277977
P 2300 2250
F 0 "C1" V 2552 2250 50  0000 C CNN
F 1 "C" V 2461 2250 50  0000 C CNN
F 2 "Capacitor_SMD:C_1206_3216Metric" H 2338 2100 50  0001 C CNN
F 3 "~" H 2300 2250 50  0001 C CNN
	1    2300 2250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	1950 2650 1950 2250
Wire Wire Line
	1950 2250 2150 2250
Connection ~ 1950 2650
Wire Wire Line
	1950 2650 2050 2650
Wire Wire Line
	2450 2250 2700 2250
Wire Wire Line
	2700 2250 2700 2650
Connection ~ 2700 2650
Wire Wire Line
	2700 2650 2850 2650
$Comp
L power:GND #PWR0101
U 1 1 6027C8CA
P 5250 3650
F 0 "#PWR0101" H 5250 3400 50  0001 C CNN
F 1 "GND" H 5255 3477 50  0000 C CNN
F 2 "" H 5250 3650 50  0001 C CNN
F 3 "" H 5250 3650 50  0001 C CNN
	1    5250 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 3600 5250 3600
Wire Wire Line
	5250 3600 5250 3650
$Comp
L Connector_Generic:Conn_01x01 J8
U 1 1 60280BEE
P 6950 2800
F 0 "J8" H 7030 2842 50  0000 L CNN
F 1 "SRC_6" H 7030 2751 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 6950 2800 50  0001 C CNN
F 3 "~" H 6950 2800 50  0001 C CNN
	1    6950 2800
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J9
U 1 1 6028100D
P 6950 2900
F 0 "J9" H 7030 2942 50  0000 L CNN
F 1 "SRC_7" H 7030 2851 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 6950 2900 50  0001 C CNN
F 3 "~" H 6950 2900 50  0001 C CNN
	1    6950 2900
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J10
U 1 1 60281154
P 6950 3000
F 0 "J10" H 7030 3042 50  0000 L CNN
F 1 "SRC_8" H 7030 2951 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 6950 3000 50  0001 C CNN
F 3 "~" H 6950 3000 50  0001 C CNN
	1    6950 3000
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J11
U 1 1 6028131A
P 6950 3100
F 0 "J11" H 7030 3142 50  0000 L CNN
F 1 "SRC_9" H 7030 3051 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 6950 3100 50  0001 C CNN
F 3 "~" H 6950 3100 50  0001 C CNN
	1    6950 3100
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J12
U 1 1 602814CB
P 6950 3200
F 0 "J12" H 7030 3242 50  0000 L CNN
F 1 "SRC_10" H 7030 3151 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 6950 3200 50  0001 C CNN
F 3 "~" H 6950 3200 50  0001 C CNN
	1    6950 3200
	1    0    0    -1  
$EndComp
NoConn ~ 6750 2800
NoConn ~ 6750 2900
NoConn ~ 6750 3000
NoConn ~ 6750 3100
NoConn ~ 6750 3200
$Comp
L power:+5V #PWR0102
U 1 1 60283C95
P 3950 2700
F 0 "#PWR0102" H 3950 2550 50  0001 C CNN
F 1 "+5V" H 3965 2873 50  0000 C CNN
F 2 "" H 3950 2700 50  0001 C CNN
F 3 "" H 3950 2700 50  0001 C CNN
	1    3950 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 2800 3950 2800
Wire Wire Line
	3950 2800 3950 2700
$Comp
L Connector_Generic:Conn_01x01 J13
U 1 1 60285333
P 5600 2450
F 0 "J13" H 5680 2492 50  0000 L CNN
F 1 "SRC_GND" H 5680 2401 50  0000 L CNN
F 2 "Connector_PinHeader_1.00mm:PinHeader_1x01_P1.00mm_Vertical" H 5600 2450 50  0001 C CNN
F 3 "~" H 5600 2450 50  0001 C CNN
	1    5600 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	5400 2450 4900 2450
Connection ~ 4900 2450
Wire Wire Line
	4900 2450 4900 2400
Text Notes 2950 3550 0    50   ~ 0
Adres (offset) 3
$EndSCHEMATC
