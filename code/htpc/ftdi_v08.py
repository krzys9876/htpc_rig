from __future__ import print_function, unicode_literals

import os, sys
import time
import datetime
import locale
import threading
import re

import win32con
import win32api
import win32gui

import wmi
import pythoncom

import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import digitalio
import pyautogui
import queue

import AudioEndpointControl
from AudioEndpointControl import Render, Capture, All
from AudioEndpointControl import Console, Multimedia, Communications
from AudioEndpointControl import (
    DEVICE_STATE_ACTIVE,
    DEVICE_STATE_DISABLED,
    DEVICE_STATE_NOTPRESENT,
    DEVICE_STATE_UNPLUGGED,
    DEVICE_STATEMASK_ALL
    )
from AudioEndpointControl import (
    Device_FriendlyName,
    Device_DeviceDesc,
    DeviceInterface_FriendlyName)

from comtypes import GUID
AppID = GUID('{00000000-0000-0000-0000-000000000001}')

import unicodedata

#########################################

DELAY_ERR=0.5
DELAY_RST=0.2
OLEDaddr=60
MAX=20

TRTAB={ord(u'ą'):u'a',ord(u'Ą'):u'A', \
       ord(u'ć'):u'c',ord(u'Ć'):u'C', \
       ord(u'ę'):u'e',ord(u'Ę'):u'E', \
       ord(u'ł'):u'l',ord(u'Ł'):u'L', \
       ord(u'ń'):u'n',ord(u'Ń'):u'N', \
       ord(u'ó'):u'ó',ord(u'Ó'):u'Ó', \
       ord(u'ś'):u's',ord(u'Ś'):u'S', \
       ord(u'ż'):u'z',ord(u'Ż'):u'Z', \
       ord(u'ź'):u'z',ord(u'Ź'):u'Z'}

def normTxt(txt):
    return unicodedata.normalize('NFKD',txt.translate(TRTAB)).encode('ascii','replace').decode('utf-8')
        

def convertBytes(txt):
    bt=0.0
    try:
        bt=float(txt)/1024
    except:
        pass
    unit='k'
    if(bt>1024):
        bt=bt/1024
        unit='M'
    if(bt>100):
        fmt="{:1.0f}{}"
    else:
        fmt="{:1.1f}{}"
    return fmt.format(bt,unit)

class PerfInfo:
    def __init__(self):
        self.cpuPerc=0.0
        self.cpuTemp=0.0
        self.memTotal=0.0
        self.memAlloc=0.0
        self.memAvail=0.0
        self.netDown="0k"
        self.netUp="0k"
        self.netTotal="0k"
        self.lock=False

    def wait(self):
        while(self.lock):
            pass

    def setLock(self):
        self.wait()
        self.lock=True

    def tryLock(self):
        if(not self.lock):
            self.setLock()
            return True
        else:
            return False

    def setUnlock(self):
        self.lock=False

    def read(self):
        txt='typeperf "\Informacje o procesorze(_Total)\% wykorzystania procesora" ' + \
             '"\Pamięć\Zadeklarowane bajty" "\Pamięć\Dostępne bajty" ' + \
             '"\Interfejs sieciowy(*)\CaŁkowita liczba bajtów/s" "\Interfejs sieciowy(*)\Bajty odebrane/s" '+ \
             '"\Interfejs sieciowy(*)\Bajty wysŁane/s" -sc 1 -si 00:00:01'
        perfStr=os.popen(txt).read()

        cpuPercStr='0'
        #cpuTempStr='273.15'
        memAllocStr='0'
        memAvailStr='0'
        memTotalStr='0'
        netTotalStr='0'
        netDownStr='0'
        netUpStr='0'
        

        try:
            cpuPercStr=extractLine(perfStr,2,1)
            #cpuTempStr=extractLine(perfStr,2,2)
            memAllocStr=extractLine(perfStr,2,2)
            memAvailStr=extractLine(perfStr,2,3)
            netTotalStr=extractLine(perfStr,2,4)
            netDownStr=extractLine(perfStr,2,6)
            netUpStr=extractLine(perfStr,2,8)
        except:
            pass

        self.wait()
        self.setLock()
        
        self.cpuPerc=0.0
        #self.cpuTemp=0.0
        try:
            self.cpuPerc=float(cpuPercStr)
            #self.cpuTemp=float(cpuTempStr)-273.15
        except:
            pass
        
        self.memTotal=0.0
        self.memAvail=0.0
        try:
            self.memAlloc=float(memAllocStr)/1024/1024/1024
            self.memAvail=float(memAvailStr)/1024/1024/1024
            self.memTotal=self.memAlloc+self.memAvail
        except:
            pass

        self.netTotal=convertBytes(netTotalStr)
        self.netDown=convertBytes(netDownStr)
        self.netUp=convertBytes(netUpStr)

        self.setUnlock()

class AudioPrefs:
    def __init__(self):
        self.device=None
        self.deviceName=''
        self.vol=0.0
        self.mute=False

    def setDevice(self,p_device):
        self.device=p_device
        devName1='{}'.format(self.device)
        # W nazwie urządzenia mogą pojawić się polskie znaki
        #devName=unicodedata.normalize('NFKD',devName1.translate(TRTAB)).encode('ascii','replace').decode('utf-8')
        devName=normTxt(devName1)
        m=re.search('(Glosniki \()([0-9]* — )*',devName)
        if(not (m is None)):
            devName=devName.replace(m.group(0),'')

            try:
                i=devName.rindex(')')
                devName=devName[:i]
            except:
                pass

        print('{} -> {}'.format(devName1,devName))

        self.deviceName=devName
        self.vol=self.device.volume.Get()
        self.mute=self.device.GetMute()

# global
audioPr=AudioPrefs()

class MMNotificationClient(object):
    def OnDeviceStateChanged(self, AudioDevice, NewState):
        #print('OnDeviceStateChanged: {0}, {1}'.format(AudioDevice, NewState))
        pass

    def OnDeviceRemoved(self, AudioDevice):
        #print('OnDeviceRemoved: {0}'.format(AudioDevice))
        AudioDevice.UnregisterCallback()

    def OnDeviceAdded(self, AudioDevice):
        #print('OnDeviceAdded: {0}'.format(AudioDevice))
        pass

    def OnDefaultDeviceChanged(self, flow, role, AudioDevice):
        #print('OnDefaultDeviceChanged: {0}, {1}, {2}'.format(flow, role, AudioDevice))
        if(flow==Render and role==Multimedia):
            AudioDevice.RegisterCallback(AudioEndpointVolumeCallback())

            global audioPr
            audioPr.setDevice(AudioDevice)
            #print('default changed')

    def OnPropertyValueChanged(self, AudioDevice, key):
        #print('OnPropertyValueChanged: {0}, {1}'.format(AudioDevice, key))
        pass

class AudioEndpointVolumeCallback(object):
    def OnNotify(self, Notify, AudioDevice):
        global audioPr
        if(audioPr.device==AudioDevice):
            audioPr.vol=Notify.MasterVolume
            audioPr.mute=Notify.Muted
        else:
            audioPr.setDevice(AudioDevice)


class ReadThread(threading.Thread):
    def __init__(self,p_pInfo,p_sleep):
        threading.Thread.__init__(self)
        self._stopEvent=threading.Event()
        self.deamon=True
        self.whileLoop=True
        self.pInfo=p_pInfo
        self.sleep=p_sleep

    def run(self):
        pythoncom.CoInitialize()
        while(self.whileLoop):
            self.pInfo.read()
            time.sleep(self.sleep)
        
    def stop(self):
        self.whileLoop=False
        self._stopEvent.set()
        

def getTimestamp():
    dateTimeObj = datetime.datetime.now() 
    #print(dateTimeObj)
    timestampStr = dateTimeObj.strftime("%d.%b.%Y %H:%M:%S")
    return timestampStr
    
    
def extractLine(txt,line,token=0):
    txtSplit=txt.splitlines()
    txtLine=txtSplit[line]
    if(token==0):
        return txtLine
    else:
        txtToken=txtLine.split(',')[token].replace('"','')
        return txtToken


##########################################
    
class DIR:
    LEFT=1
    RIGHT=2
    NONE=3

class StringTrimmer:
    def __init__(self,p_txt,p_maxlen,p_staticlen,p_starttick,p_endtick,p_loop):
        self.maxlen=p_maxlen
        self.staticlen=p_staticlen
        self.starttick=p_starttick
        self.endtick=p_endtick
        self.loop=p_loop
        self.resetTick()
        self.txt=''
        self.staticTxt=''
        self.printTxt=''
        self.printStaticTxt=''
        self.setText(self.txt,True)
        self.setStaticText(self.staticTxt,True)

    def setText(self,p_txt,force=False):
        if(p_txt!=self.txt or force):
            self.txt=p_txt
            self.txtlen=len(self.txt)
            self.diff=self.txtlen-self.maxlen
            self.resetTick()
            self.printTxt='{: <{:d}}'.format(self.txt,self.maxlen)

    def setStaticText(self,p_stTxt,force=False):
        if(p_stTxt!=self.staticTxt or force):
            self.staticTxt=p_stTxt
            self.printStaticTxt='{: <{:d}}'.format(self.staticTxt,self.staticlen)

    def resetTick(self):
        self.tick=-1
        self.stick=0
        self.etick=0
        
        
    def nextTick(self):
        if(self.diff<=0):
            self.tick=0
            return

        if(self.tick<0):
            self.tick=0
            self.stick=0
            self.estick=0
        elif(self.tick==0):
            if(self.stick<self.starttick-1):
                self.stick+=1
            else:
                self.tick+=1
                self.stick=0
        elif(self.tick==self.diff):
            if(self.etick<0):
                self.etick=0
            elif(self.etick<self.endtick-1):
                self.etick+=1
            else:
                self.tick+=1
                self.etick=0
        else:
            self.tick+=1

        if(self.loop):
            if(self.tick>=self.txtlen+1):
                self.tick=0
        else:
            if(self.tick>=self.diff+1):
                self.tick=0
    
                
    def genPrintText(self):
        ntxt=self.txt

        self.nextTick()

        if(self.diff<0):
            ntxt=self.txt
        else:
            if(self.loop):
                ntxt=(self.txt+chr(0xdd)+self.txt)[self.tick:self.tick+self.maxlen]
            else:
                ntxt=self.txt[self.tick:self.tick+self.maxlen]

        self.printTxt='{: <{:d}}'.format(ntxt,self.maxlen)

    def get(self):
        txt=self.printTxt+self.printStaticTxt
        return txt 

class ScreenLines:
    def __init__(self,p_stick,p_etick,p_loop):
        self.strTrim=[StringTrimmer('',MAX,0,p_stick,p_etick,p_loop), \
                      StringTrimmer('',MAX,0,p_stick,p_etick,p_loop), \
                      StringTrimmer('',MAX,0,p_stick,p_etick,p_loop), \
                      StringTrimmer('',MAX-5,5,p_stick,p_etick,p_loop)]

    def setText(self,txt,index):
        self.strTrim[index].setText(txt)

    def setStaticText(self,txt,index):
        self.strTrim[index].setStaticText(txt)

    def setTexts(self,txt0,txt1,txt2,txt3,stTxt3):
        self.setText(txt0,0)
        self.setText(txt1,1)
        self.setText(txt2,2)
        self.setText(txt3,3)
        self.setStaticText(stTxt3,3)

    def genPrintText(self):
        for i in range(0,4):
            self.strTrim[i].genPrintText()
        
    def get(self,index):
        return self.strTrim[index].get()

class DeviceGPIO:
    def __init__(self,p_gpio,p_dir):
        self.gpio=p_gpio
        self.dir=p_dir

    def init(self):
        for i in range(0,len(self.gpio)):
            self.gpio[i].direction=self.dir[i]
        # Podświetlenie na stałe
        self.gpio[5].value=True

    def exit(self):
        # Podświetlenie na stałe
        self.gpio[5].value=False
        self.gpio[5].direction=digitalio.Direction.INPUT


    # rotary - A
    def getA(self):
        return self.gpio[3]

    # rotary - B
    def getB(self):
        return self.gpio[2]
        
    # play/pause
    def getPP(self):
        return self.gpio[0]

    # mute
    def getM(self):
        return self.gpio[1]
    
    # OLED reset
    def getRst(self):
        return self.gpio[4]

    def getState(self):
        return (self.getPP().value,self.getM().value,self.getB().value,self.getA().value)

    

class DeviceOLED:
    def __init__(self,p_device,p_rstPin):
        self.device=p_device
        self.rstPin=p_rstPin

    def initLCD(self):
        # RESET
        self.rstPin.value=False
        time.sleep(DELAY_RST)
        self.rstPin.value=True
        time.sleep(DELAY_RST)
    
        try:        
            self.writeB(0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0	
            self.writeB(0x80,0x09) # 4-line mode	
            self.writeB(0x80,0x05) # view 0
            self.writeB(0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0
            
            self.writeB(0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0 
            self.writeB(0x80,0x72) # ROM selection
            self.writeB(0x40,0x00) # ROM jako dane A=0x00 B=0x04 C=0x0C
            self.writeB(0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0

            self.writeB(0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0
            self.writeB(0x80,0x79) # SD=1
            self.writeB(0x80,0x81) # contrast set
            self.writeB(0x80,0x00) # wartosc jako komenda, nie dane (00-min FF-max)
            self.writeB(0x80,0x78) # SD=0   
            self.writeB(0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0
            
            self.writeB(0x80,0x0D) # ??? (bez tego czasem nie dziala)
            self.writeB(0x80,0x01) # clear display
            self.writeB(0x80,0x80) #Set DDRAM Address to 0x80 (line 1 start)
            time.sleep (DELAY_RST) # na wszelki wypadek
            self.writeB(0x80,0x0C) # turn on
        except IOError as e:
            printTimestamp()
            #time.sleep(DELAY_ERR)
            raise

    def writeB(self,b1,b2):
        b=bytearray(2)
        b[0]=b1
        b[1]=b2
        try:
            self.device.write(b)
        except Error as e:
            print(e)
            

    def writeS(self,arr):
        #print('refresh')
        #print(arr)

        b=bytearray(4*MAX+1)
        b[0]=0x40
        for i in range(0,4):
            for j in range(0,MAX):
                #print(i,j,arr[i][j],ord(arr[i][j]))
                b[1+i*MAX+j]=ord(arr[i][j])

        # adres początkowy
        self.writeB(0x80,0x80)
        self.device.write(b)

    def printTxt(self,lines):
        # w pierwszej linii mogą pojawić się polskie znaki
        #line0=devName=unicodedata.normalize('NFKD',lines.get(0).translate(TRTAB)).encode('ascii','replace').decode('utf-8')
        line0=normTxt(lines.get(0))
        arr=[line0,lines.get(1),lines.get(2),lines.get(3)]
        #for i in range(0,4):
        #    arr[i]='{: <{:d}}'.format(arr[i],MAX)

        self.writeS(arr)

class ActionQueue(queue.Queue):
    def __init__(self):
        queue.Queue.__init__(self,3)

    def clear(self):
        while(not self.empty()):
            x=self.get()

    def addKey(self,key):
        if(not self.full()):
            self.put(key)


class ButtonThread(threading.Thread):
    def __init__(self,p_gpio,p_sleep,p_queue):
        threading.Thread.__init__(self)
        self._stopEvent=threading.Event()
        self.deamon=True
        self.gpio=p_gpio
        self.queue=p_queue
        self.sleep=p_sleep
        self.whileLoop=True

    def addToQueue(self,val,p_idle=False):
        self.queue.addKey(val)
        #print(val)
        
        
    def run(self):
        val=(False,False,False,False)
        firstFlag=True
        rotaryFlag=DIR.NONE
        rotaryTimer=time.time()
        
        while(self.whileLoop):
            valn=self.gpio.getState()
            if(not firstFlag):
                interval=time.time()-rotaryTimer
                if(valn[0]!=val[0] and not valn[0]):
                    self.addToQueue('playpause')                    
                    
                if(valn[1]!=val[1] and not valn[1]):
                    self.addToQueue('volumemute')                    

                if(valn[3]!=val[3]):
                    if(valn[2]!=valn[3]):
                        if(rotaryFlag!=DIR.LEFT or (interval>0.2)):
                            self.addToQueue('volumeup')
                            rotaryFlag=DIR.RIGHT
                            rotaryTimer=time.time()
                    else:
                        if(rotaryFlag!=DIR.RIGHT or (interval>0.2)):
                            self.addToQueue('volumedown')
                            rotaryFlag=DIR.LEFT
                            rotaryTimer=time.time()

            val=valn
            firstFlag=False
            time.sleep(self.sleep)
        
    def stop(self):
        self.whileLoop=False
        self._stopEvent.set()

class TemperatureReader:
    def get():
        openHwInfo=wmi.WMI(namespace="root\OpenHardwareMonitor").Sensor()
        temp=next((s for s in openHwInfo if s.Name[:14]=="Temperature #1"),None)
        return temp.Value if (temp is not None) else 0.0

locale.setlocale(locale.LC_ALL,'pl_PL.UTF-8')


if __name__=="__main__":

    f = open("c:\\data\\test.log", "a")
    f.write("Start" + "\n")
    f.close()
    

    state=ScreenLines(6,3,True)

    # wybór urządzenia I2C przed inicjalizacją pinów GPIO
    i2c=busio.I2C(board.SCL,board.SDA)
    device=I2CDevice(i2c,OLEDaddr)

    # 0 - PP, 1 - SW, 2 - DT, 3 - CLK, 4 - RST, 5 - PP_LED
    pinArr=[digitalio.DigitalInOut(board.C6), \
            digitalio.DigitalInOut(board.C1), \
            digitalio.DigitalInOut(board.C2), \
            digitalio.DigitalInOut(board.C3), \
            digitalio.DigitalInOut(board.C0),
            digitalio.DigitalInOut(board.C7)]
    dirArr=[digitalio.Direction.INPUT, \
            digitalio.Direction.INPUT, \
            digitalio.Direction.INPUT, \
            digitalio.Direction.INPUT, \
            digitalio.Direction.OUTPUT,
            digitalio.Direction.OUTPUT]

    gpio=DeviceGPIO(pinArr,dirArr)
    gpio.init()

    oled=DeviceOLED(device,gpio.getRst())
    oled.initLCD()
    oled.printTxt(state)

    actQueue=ActionQueue()

    buttonTh=ButtonThread(gpio,0.0005,actQueue)
    buttonTh.start()
    
    pInfo=PerfInfo()
    readTh=ReadThread(pInfo,0.1)
    readTh.start()

    AudioDevices = AudioEndpointControl.AudioEndpoints(DEVICE_STATE=DEVICE_STATE_ACTIVE, PKEY_Device=Device_FriendlyName, EventContext=AppID)


    try:

        def wndProc(hWnd, msg, wparam, lparam):
            if (msg == win32con.WM_DESTROY) or \
               (msg==win32con.WM_QUIT) or \
               (msg==win32con.WM_NCDESTROY) or \
               (msg==win32con.WM_QUERYENDSESSION) or \
               (msg==win32con.WM_ENDSESSION):

                # czyszczenie wyświetlacza
                state.setTexts('','       '+chr(0x96)+'off'+chr(0x97),'','','')
                oled.printTxt(state)
                
                if(msg==win32con.WM_QUERYENDSESSION) or (msg==win32con.WM_ENDSESSION):
                    return True
                
                win32gui.PostQuitMessage(0)
                exit(0)
                return 0
            else:
                win32gui.DefWindowProc(hWnd, msg, wparam, lparam)


        hInstance = win32api.GetModuleHandle()
        wndClass                = win32gui.WNDCLASS()
        wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        #wndClass.style          = win32con.CS_HIDE
        wndClass.lpfnWndProc    = wndProc
        wndClass.hInstance      = hInstance
        wndClass.hIcon          = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        wndClass.hCursor        = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = 'testClass'

        wndClassAtom = win32gui.RegisterClass(wndClass)

        hWindow = win32gui.CreateWindow(
            wndClassAtom,                   #it seems message dispatching only works with the atom, not the class name
            'Python Win32 Window',
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hInstance,
            None)

        win32gui.ShowWindow(hWindow, win32con.SW_SHOWMINIMIZED)
        win32gui.UpdateWindow(hWindow)

        cnt=0
        c=0.0
        mt=0.0
        ma=0.0
        nt="0k"
        nd="0k"
        nu="0k"
        dispTxt=''
        lockCnt=0

        tick=0

        AudioDevices.RegisterCallback(MMNotificationClient())
        for AudioDevice in AudioDevices:
            if AudioDevice.isDefault():
                AudioDevice.RegisterCallback(AudioEndpointVolumeCallback())
                audioPr.setDevice(AudioDevice)

        while(True):
            while(not actQueue.empty()):
                key=actQueue.get()
                if(key=='playpause'):
                    pyautogui.press('playpause')                
                elif(key=='volumemute'):
                    pyautogui.press('volumemute')                
                elif(key=='volumeup'):
                    pyautogui.press('volumeup')                
                elif(key=='volumedown'):
                    pyautogui.press('volumedown')                


            if(pInfo.tryLock()):
                c=pInfo.cpuPerc
                #ct=pInfo.cpuTemp
                mt=pInfo.memTotal
                ma=pInfo.memAlloc
                nt=pInfo.netTotal
                nd=pInfo.netDown
                nu=pInfo.netUp
                pInfo.setUnlock()
                lockCnt=0
            else:
                lockCnt+=1

            # w Windows 11 temperatura nie odczytuje się przez typeperf, obejście:
            ct=TemperatureReader.get()

            newTxt='{} CPU{:3.0f}%/{:2.0f} RAM {:1.1f}/{:1.0f}GB (locks:{:d}) Device: {} Volume: {:2.0f} Mute:{}'.format( \
                getTimestamp(),c,ct,mt-ma,mt,lockCnt,audioPr.deviceName,audioPr.vol*100,'off' if not audioPr.mute else 'on')

            state0=getTimestamp()
            state1='Pr{:3.0f}%/{:2.0f}{} M {:1.1f}/{:1.0f}GB'.format(c,ct,chr(0x80),ma,mt)
            state2='Net {}{}  {}{}'.format(chr(0xE0),nd,chr(0xDE),nu)
            state3=audioPr.deviceName
            state3s='{}{}{:3.0f}'.format(chr(0xFE),chr(0x90) if not audioPr.mute else 'x',audioPr.vol*100)
            state.setTexts(state0,state1,state2,state3,state3s)

            win32gui.PumpWaitingMessages()
            #win32gui.PumpMessages()

            if(tick % 8 ==0):
                state.genPrintText()
                

            if(tick % 8 ==0 or newTxt!=dispTxt):
                oled.printTxt(state)
            
            #if(newTxt!=dispTxt):
                dispTxt=newTxt
                #print('{:d}:{}'.format(cnt,dispTxt))
                #oled.printTxt(state)

            cnt+=1

            if(cnt>100):
                cnt=0
                readTh.stop()
                readTh=ReadThread(pInfo,0.1)
                readTh.start()                
                                    
            time.sleep(0.1)

            tick+=1

            #if(refresh):
            #    oled.printTxt(state)
                
    finally:
        buttonTh.stop()
        readTh.stop()
        state.setTexts('','       '+chr(0x96)+'off'+chr(0x97),'','','')
        oled.printTxt(state)
        gpio.exit()

        for AudioDevice in AudioDevices:
            try:
                AudioDevice.UnregisterCallback()
            except:
                print('Error: {}'.format(AudioDevice))
                pass
        AudioDevices.UnregisterCallback()
        
        print('Koniec')
        
    

main()
