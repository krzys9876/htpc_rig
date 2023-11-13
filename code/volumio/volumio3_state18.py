# -*- coding: utf-8 -*-
#I2C

import os
import requests
import time
import RPi.GPIO as GPIO
import unicodedata
import threading
import smbus
import math
import datetime
import io
import socketio
import queue
import argparse
from html.parser import HTMLParser
from xml.etree import ElementTree

import traceback

import OLED_Driver as OLED

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import pygame

COUNTER=[0,0,0,0]
MAX=20

OLEDaddr = 0x3C
KEYSaddr = 0x20

LCD_RST_PIN=23

URL='http://192.168.3.122'
MPC_URL='http://192.168.3.97:13579'
VLC_URL='http://192.168.3.97:8080'
VLC_PASS='vlc'

# debug only
char_print=False

#global bus

# polskie znaki wg UTF8
def strReplace1(string):
    
    string=string.replace(chr(196)+chr(133),'a') #ą
    string=string.replace(chr(196)+chr(135),'c') #ć
    string=string.replace(chr(196)+chr(153),'e') #ę
    string=string.replace(chr(197)+chr(130),'l') #ł
    string=string.replace(chr(197)+chr(132),'n') #ń
    string=string.replace(chr(195)+chr(179),'o') #ó
    string=string.replace(chr(197)+chr(155),'s') #ś
    string=string.replace(chr(197)+chr(186),'z') #ź
    string=string.replace(chr(197)+chr(188),'z') #ż
    string=string.replace(chr(196)+chr(132),'A') #Ą
    string=string.replace(chr(196)+chr(134),'C') #Ć
    string=string.replace(chr(196)+chr(152),'E') #Ę
    string=string.replace(chr(197)+chr(129),'L') #Ł
    string=string.replace(chr(197)+chr(131),'N') #Ń
    string=string.replace(chr(195)+chr(147),'O') #Ó
    string=string.replace(chr(197)+chr(154),'S') #Ś
    string=string.replace(chr(197)+chr(185),'Z') #Ź
    string=string.replace(chr(197)+chr(187),'Z') #Ż
    
    
    
    return string

#inne znaki lub polskie litery w kodowaniu innym, niż UTF8 - zgodnie z tabelą dla wyświetlacza
def strReplace2(string):
    # kolejno: \ _ [ ] CP1250
    transTab={92:0xfb, \
              95:0xc4, \
              91:0xfa, \
              93:0xfc, \
              185:ord('a'), \
              230:ord('c'), \
              234:ord('e'), \
              232:ord('e'), \
              179:ord('l'), \
              241:ord('n'), \
              243:ord('o'), \
              156:ord('s'), \
              159:ord('z'), \
              191:ord('z'), \
              165:ord('A'), \
              198:ord('C'), \
              202:ord('E'), \
              163:ord('L'), \
              209:ord('N'), \
              211:ord('O'), \
              140:ord('S'), \
              143:ord('Z'), \
              175:ord('Z')
        }
    
    string=string.translate(transTab)
    return string

#jeszcze inne znaki, które trzeba zamienić na końcu
def strReplace3(string):
    # kolejno: [ ] mapowane wcześniej z chr 250 i 252
    transTab={91:0xfa, \
              93:0xfc
        }
    
    string=string.translate(transTab)
    return string

def jsonNormalize(js,var,p_print=False):
    # zamiana niektórych znaków i CP1250
            
    txt=strReplace2(getVar(js,var)) if(var in js) else ""
    
    if(p_print):
        for i in range(0,len(txt)):
            print("{}:{}".format(txt[i],ord(txt[i])))
    # normalizacja i zamiana polskich znaków
    txtNorm=unicodedata.normalize('NFKD',txt.translate(VolumioReader.trtab)).encode('ascii','replace')
    txt2=txtNorm.decode('utf-8')
    # ponowna zamiana niektórych znaków
    txt2=strReplace3(txt2)
    return(txt2)


#sprawdzanie, czy atrybut jest na liście
def getVar(p_dict,p_var):
    t=''
    if(p_var in p_dict):
        t=p_dict[p_var]
        if(t is None):
            t=''
    return t

# kody wyświetlacza
volArr=[chr(0x20)+chr(0x20)+chr(0x20)+chr(0x20)+chr(0xDD), \
        chr(0x20)+chr(0x20)+chr(0x20)+chr(0x20)+chr(0xD4), \
        chr(0x20)+chr(0x20)+chr(0x20)+chr(0x20)+chr(0xDA), \
        chr(0x20)+chr(0x20)+chr(0x20)+chr(0xD3)+chr(0xDA), \
        chr(0x20)+chr(0x20)+chr(0x20)+chr(0xD9)+chr(0xDA), \
        chr(0x20)+chr(0x20)+chr(0xD2)+chr(0xD9)+chr(0xDA), \
        chr(0x20)+chr(0x20)+chr(0xD8)+chr(0xD9)+chr(0xDA), \
        chr(0x20)+chr(0xD1)+chr(0xD8)+chr(0xD9)+chr(0xDA), \
        chr(0x20)+chr(0xD7)+chr(0xD8)+chr(0xD9)+chr(0xDA), \
        chr(0xD0)+chr(0xD7)+chr(0xD8)+chr(0xD9)+chr(0xDA), \
        chr(0xD6)+chr(0xD7)+chr(0xD8)+chr(0xD9)+chr(0xDA)]


DELAY = 1.0e-1 # in seconds
DELAY_MSG = 0.2
DELAY_ERR = 0.2
DELAY_RST = 0.2
DELAY_TICK = 0.01
ERR_MINUTES=5

def printTimestamp():
    dateTimeObj = datetime.datetime.now() 
    #timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    #print(timestampStr)
    print(dateTimeObj)

def XMLFind(xml,path):
    val=''
    valEl=xml.find(path)
    if(not (valEl is None)):
        val=valEl.text
    return val    

class MPCParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.var={}
        self.tmpVarId=''
        self.tmpVarData=''
        self.state=0
    
    def handle_starttag(self, tag, attrs):
        if(tag=='p'):
            self.state=1
            #print("Start tag:", tag)
            for attr in attrs:
                (k,v)=attr
                if(k=='id'):
                    self.tmpVarId=v
                    #print('id:'+self.tmpVarId)
                
    def handle_endtag(self, tag):
        if(self.state==1):
            self.state=0
            self.var[self.tmpVarId]=self.tmpVarData
            self.tmpVarId=''
            self.tmpVarData=''
            #print("End tag  :", tag)            

    def handle_data(self, data):
        if(self.state==1):
            self.tmpVarData=data


class Menu:
    def __init__(self,p_list,p_vSize,p_selChar):
        self.list=p_list
        self.vSize=p_vSize
        self.sel=0
        self.vStart=0
        self.selChar=p_selChar

    def clear(self):
        self.list=[]
        self.sel=0
        self.vStart=0

    def up(self):
        if(self.sel>0):
            self.sel-=1
            if(self.sel<self.vStart):
                self.vStart=self.sel
        else:
            self.bottom()
                
    def down(self):
        if(self.sel<len(self.list)-1):
            self.sel+=1
            if(self.sel>=self.vStart+self.vSize):
                self.vStart=self.sel-self.vSize+1
        else:
            self.top()

    def top(self):
        while self.sel>0:
            self.up()

    def bottom(self):
        while self.sel<len(self.list)-1:
            self.down()

    def getItem(self,ind):
        if(ind>=len(self.list)):
            return " "
        else:
            return "{}{}".format(self.selChar if(ind==self.sel) else ' ',self.list[ind])

    def getVItem(self,vInd):
        ind=vInd+self.vStart
        return self.getItem(ind)

    def getSelected(self):
        if(self.isEmpty()):
            return ""
        else:
            return self.list[self.sel]

    def getSelIndex(self):
        return self.sel

    def isEmpty(self):
        return len(self.list)==0

class VolumioMenu:
    def __init__(self,p_caption='',p_vSize=3):
        self.menu=Menu([],p_vSize,chr(0x10))
        self.caption=p_caption

    def getItem(self,visIndex):
        return self.menu.getVItem(visIndex)

    def up(self):
        self.menu.up()

    def down(self):
        self.menu.down()

    def top(self):
        self.menu.top()

    def bottom(self):
        self.menu.bottom()

    def getSelected(self):
        return self.menu.getSelected()

    def getSelIndex(self):
        return self.menu.getSelIndex()

    def getCaption(self):
        return self.caption
    

class VolumioPlaylists(VolumioMenu):

    NONE=0
    READY=1

    def __init__(self):
        VolumioMenu.__init__(self,'PLAYLIST:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.clear()

    def clear(self):
        self.state=VolumioPlaylists.NONE
        self.js=None
        self.menu.clear()

    def read(self,p_js):
        self.js=p_js
        self.state=VolumioPlaylists.READY

        for i in range(0,len(self.js)):
            self.menu.list.append(self.js[i])

        #print(self.menu.list)

class VolumioWebRadios(VolumioMenu):

    NONE=0
    READY=1

    def __init__(self):
        VolumioMenu.__init__(self,'CD/RADIO:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.clear()

    def clear(self):
        self.state=VolumioWebRadios.NONE
        self.js=None
        self.menu.clear()

    def read(self,p_js):
        # Helpful info:
        # http://volumio.local/api/v1/browse
        self.state=VolumioWebRadios.READY        
        if('navigation' in p_js):
            nav=p_js['navigation']
            if('lists' in nav):
                ls=nav['lists'][0]
                if('items' in ls):
                    self.js=ls['items']
                    # add CD Audio as first item
                    self.js.insert(0,{'service': 'cd_controller', 'uri': 'audiocd', 'title': 'CD'})
                    for i in range(0,len(self.js)):
                        item=jsonNormalize(self.js[i],'title',char_print)
                        self.menu.list.append(item)
                        print(self.js[i])

        #print(self.menu.list)

    def getSelected(self):
        return self.js[self.getSelIndex()]['uri']



class VolumioPlaylistsAction(VolumioMenu):

    def __init__(self):
        VolumioMenu.__init__(self,'PLAYLIST:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.menu.list=['Clear and play','Add to queue']

class VolumioPlayOptions(VolumioMenu):

    def __init__(self,p_vState):
        VolumioMenu.__init__(self,'OPTIONS:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.menu.list=['Repeat all','Repeat single','Random']
        self.vState=p_vState

    def getItem(self,visIndex):
        item=VolumioMenu.getItem(self,visIndex)
        if(visIndex==0):
            item=item+(' ON' if(self.vState.repeatAll) else ' OFF')
        elif(visIndex==1):
            item=item+(' ON' if(self.vState.repeatSingle) else ' OFF')
        elif(visIndex==2):
            item=item+(' ON' if(self.vState.random) else ' OFF')
        return item

class VolumioNaviMenu(VolumioMenu):

    def __init__(self,p_vState):
        VolumioMenu.__init__(self,'SKIP:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.menu.list=['Next album','Skip +10s','Skip -10s']
        self.vState=p_vState    
        
class VolumioRemoteMenu(VolumioMenu):
    def __init__(self,p_vState):
        VolumioMenu.__init__(self,'REMOTE:'+chr(0x10)+'sel '+chr(0x11)+'back')
        self.menu.list=['Media Player Classic','VLC']
        self.vState=p_vState    

class VolumioMenuControl:
    NONE=0
    PLAYLIST=1
    PLAYLIST_ACTION=2
    OPTIONS=3
    NAVI=4
    REMOTE=5
    RADIOS=6

    def __init__(self,p_vState):
        self.vState=p_vState
        self.state=VolumioMenuControl.NONE
        self.playlists=VolumioPlaylists()
        self.radios=VolumioWebRadios()
        self.playlistsAction=VolumioPlaylistsAction()
        self.options=VolumioPlayOptions(self.vState)
        self.navi=VolumioNaviMenu(self.vState)
        self.remote=VolumioRemoteMenu(self.vState)
        self.setState(VolumioMenuControl.NONE)
        

    def readPlaylists(self,p_js):
        self.playlists.read(p_js)

    def readRadios(self,p_js):
        self.radios.read(p_js)

    def setState(self,p_state):
        self.currentMenu=None
        self.state=p_state
        if(self.state==VolumioMenuControl.PLAYLIST):
            self.currentMenu=self.playlists
        elif(self.state==VolumioMenuControl.PLAYLIST_ACTION):
            self.currentMenu=self.playlistsAction
        elif(self.state==VolumioMenuControl.OPTIONS):
            self.currentMenu=self.options
        elif(self.state==VolumioMenuControl.NAVI):
            self.currentMenu=self.navi
        elif(self.state==VolumioMenuControl.REMOTE):
            self.currentMenu=self.remote
        elif(self.state==VolumioMenuControl.RADIOS):
            self.currentMenu=self.radios

    def enter(self):
        self.setState(VolumioMenuControl.PLAYLIST)
        self.playlistsAction.top()
        self.options.top()
        
    def enter2(self):
        self.setState(VolumioMenuControl.NAVI)
        self.navi.top()

    def exit(self):
        self.playlists.clear()
        self.setState(VolumioMenuControl.NONE)
        

    def getItem(self,visIndex):
        if(self.state==VolumioMenuControl.NONE):
            return ''
        elif(self.currentMenu is not None):
            return self.currentMenu.getItem(visIndex)

    def process(self,key):
        if(key==1):
            if(self.state==VolumioMenuControl.PLAYLIST):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.PLAYLIST_ACTION):
                self.setState(VolumioMenuControl.PLAYLIST)
            elif(self.state==VolumioMenuControl.RADIOS):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.OPTIONS):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.NAVI):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.REMOTE):
                return {'name' : 'exit'}
        elif(key==2):                
            if(self.state==VolumioMenuControl.PLAYLIST):
                self.setState(VolumioMenuControl.PLAYLIST_ACTION)
            elif(self.state==VolumioMenuControl.PLAYLIST_ACTION):
                if(self.playlistsAction.getSelIndex()==0):
                    return {'name':'playlist', 'param1':self.playlists.getSelected(), 'param2':'play'}
                elif(self.playlistsAction.getSelIndex()==1):
                    return {'name':'playlist', 'param1':self.playlists.getSelected(), 'param2':'add'}
            elif(self.state==VolumioMenuControl.RADIOS):
                return {'name':'playradio', 'param1':self.radios.getSelected()}
            elif(self.state==VolumioMenuControl.OPTIONS):
##              if(self.options.getSelIndex()==0):
##                  return {'name':'nextalbum'}
                if(self.options.getSelIndex()==0):
                    return {'name':'repeatAll'}
##                if(self.options.getSelIndex()==1):
##                    return {'name':'repeatSingle'}
                if(self.options.getSelIndex()==2):
                    return {'name':'random'}
            elif(self.state==VolumioMenuControl.NAVI):
                if(self.navi.getSelIndex()==0):
                    return {'name':'nextalbum'}
                if(self.navi.getSelIndex()==1):
                    return {'name':'skip+'}
                if(self.navi.getSelIndex()==2):
                    return {'name':'skip-'}
            elif(self.state==VolumioMenuControl.REMOTE):
                if(self.remote.getSelIndex()==0):
                    return {'name':'MPC'}
                if(self.remote.getSelIndex()==1):
                    return {'name':'VLC'}
        elif(key==3):                
            if(self.currentMenu is not None):
                self.currentMenu.up()
        elif(key==4):                
            if(self.currentMenu is not None):
                self.currentMenu.down()
        elif(key==5):
            if(self.state==VolumioMenuControl.PLAYLIST):
                self.setState(VolumioMenuControl.RADIOS)
            elif(self.state==VolumioMenuControl.RADIOS):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.NAVI):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.OPTIONS):
                return {'name' : 'exit'}
        elif(key==6):
            if(self.state==VolumioMenuControl.PLAYLIST):
                return {'name' : 'exit'}
            elif(self.state==VolumioMenuControl.NAVI):
                self.setState(VolumioMenuControl.OPTIONS)
            elif(self.state==VolumioMenuControl.OPTIONS):
                self.setState(VolumioMenuControl.REMOTE)
            elif(self.state==VolumioMenuControl.REMOTE):
                return {'name' : 'exit'}

        return {'name' : 'none'}

    def getCaption(self):
        if(self.currentMenu is not None):
            return self.currentMenu.getCaption()
        else:
            return ''
        


class VolumioState:
    VOL_STEP=5
    
    def __init__(self):
        self.state=''
        self.albumArt=''
        self.albumArtRefresh=False
        self.artist=''
        self.album=''
        self.title=''
        self.timer=''
        self.repeatAll=False
        self.repeatSingle=False
        self.random=False
        self.n=1
        self.remoteScreenRefresh=False
        self.remoteTimeouts=0
        self.volume=0

    def setRefreshFlags(self,p_art,p_remote):
        self.albumArtRefresh=p_art
        self.remoteScreenRefresh=p_remote

class StringTrimmer:
    def __init__(self,p_txt,p_maxlen,p_starttick,p_endtick,p_loop):
        self.maxlen=p_maxlen
        self.starttick=p_starttick
        self.endtick=p_endtick
        self.loop=p_loop
        self.resetTick()
        self.txt=''
        self.printTxt=''
        self.setText(p_txt,True)

    def setText(self,p_txt,force=False):
        if(p_txt!=self.txt or force):
            self.txt=p_txt
            self.txtlen=len(self.txt)
            self.diff=self.txtlen-self.maxlen
            self.resetTick()
            self.printTxt='{: <{:d}}'.format(self.txt,self.maxlen)

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
        return self.printTxt

class ScreenLines:
    def __init__(self,p_max,p_stick,p_etick,p_loop):
        self.strTrim=[StringTrimmer('',p_max,p_stick,p_etick,p_loop), \
                      StringTrimmer('',p_max,p_stick,p_etick,p_loop), \
                      StringTrimmer('',p_max,p_stick,p_etick,p_loop), \
                      StringTrimmer('',p_max,p_stick,p_etick,p_loop)]

    def setText(self,txt,index):
        self.strTrim[index].setText(txt)

    def setTexts(self,txt0,txt1,txt2,txt3):
        self.setText(txt0,0)
        self.setText(txt1,1)
        self.setText(txt2,2)
        self.setText(txt3,3)

    def genPrintText(self):
        for i in range(0,4):
            self.strTrim[i].genPrintText()
        
    def get(self,index):
        return self.strTrim[index].get()
        
class VolumioReader:

    IDLE=0
    PROCESSING=1
    MENU=2
    SHUTDOWN=3
    REMOTE_MPC=4
    REMOTE_VLC=5
    ENDED=6

    SIO_DISCONNECTED=0
    SIO_CONNECTING=1
    SIO_CONNECTED=2

    SIO_REQ_IDLE=0
    SIO_REQ_PROCESSING=1

    trtab={ord(u'ą'):u'a',ord(u'Ą'):u'A', \
           ord(u'ć'):u'c',ord(u'Ć'):u'C', \
           ord(u'ę'):u'e',ord(u'Ę'):u'E', \
           ord(u'ł'):u'l',ord(u'Ł'):u'L', \
           ord(u'ń'):u'n',ord(u'Ń'):u'N', \
           ord(u'ó'):u'ó',ord(u'Ó'):u'Ó', \
           ord(u'ś'):u's',ord(u'Ś'):u'S', \
           ord(u'ż'):u'z',ord(u'Ż'):u'Z', \
           ord(u'ź'):u'z',ord(u'Ź'):u'Z',
           250:u'[',252:u']'}
    

    def __init__(self,p_tick,p_tickRefresh,p_tickKeys):
        # 4 linie wyświetlacza
##        self.state=['{: <{:d}}'.format('',MAX), \
##                    '{: <{:d}}'.format('',MAX), \
##                    '{: <{:d}}'.format('',MAX), \
##                    '{: <{:d}}'.format('',MAX)]

        self.lines=ScreenLines(MAX,6,3,True)
            
        self.function=''
        self.functionId=0
        self.errArr=[]
        self.vState=VolumioState()
        self.IOErrCnt=0
        self.menuState=VolumioReader.IDLE
        self.tick=p_tick
        self.tickRefresh=p_tickRefresh
        self.tickKeys=p_tickKeys
        self.tickCount=0

        # semafor dla zapytań do serwera
        self.reqLock=False
        #semafor dla I2C
        self.i2cLock=False
        #semafor dla odświeżania ekranu
        self.dispLock=False

        self.keyQueue=queue.Queue(0)
        self.keysReader=None

        self.menuControl=VolumioMenuControl(self.vState)
        
        # zegar dla funkcji shutdown - tworzony po naciśnięciu
        self.shutdownTh=None

        #Zestawienie połączenia z WebSocket

        self.sioConn=VolumioReader.SIO_DISCONNECTED
        self.sioWait=VolumioReader.SIO_REQ_IDLE
        self.sioData=None

        self.sio=socketio.Client()
        self.sio.on('connect',self.on_connect)
        self.sio.on('pushState',self.on_pushState)
        self.sio.on('disconnect',self.on_disconnect)
        self.sio.on('pushListPlaylist',self.on_pushListPlaylists)
        self.sio.on('pushBrowseLibrary',self.on_pushBrowseLibrary)
        self.sio.on('pushState',self.on_pushState)        
        self.sio.on('pushQueue',self.on_pushQueue)
        self.setConnMessage()
     
        if(GUI):
            self.screen = pygame.display.set_mode((512, 128),0,24)
            self.updateScreen()

    def setKeysReader(self, p_keys):
        self.keysReader=p_keys

    def mainLoop(self):
        while(True):
            time.sleep(self.tick)
            self.tickCount+=1
            
            if(self.tickCount % self.tickKeys==0):
                if( not self.keyQueue.empty()):
                    key=self.keyQueue.get()
                    self.process(key)

                if(self.keysReader!=None):
                    self.keysReader.readKeys()
                
                    
            if(self.tickCount % self.tickRefresh==0):
                self.update()

            if(self.tickCount % 200==0):
                self.updateDebug()

            if(self.tickCount % 20==0):
                self.stateOnScreen()

            if(GUI):
                events=pygame.event.get()
                for event in events:
                    if(event.type==pygame.KEYDOWN):
                        if(event.key==pygame.K_ESCAPE):
                            raise KeyboardInterrupt
                        elif(event.key==pygame.K_0):
                            self.addKey(0)
                        elif(event.key==pygame.K_1):
                            self.addKey(1)
                        elif(event.key==pygame.K_2):
                            self.addKey(2)
                        elif(event.key==pygame.K_3):
                            self.addKey(3)
                        elif(event.key==pygame.K_4):
                            self.addKey(4)
                        elif(event.key==pygame.K_5):
                            self.addKey(5)
                        elif(event.key==pygame.K_6):
                            self.addKey(6)
                        elif(event.key==pygame.K_7):
                            self.addKey(7)
                

    def addKey(self,p_key):
        self.keyQueue.put(p_key)
            

    def connect(self):
        print('Connecting...')
        try:
            self.sioConn=VolumioReader.SIO_CONNECTING
            self.sioWait=VolumioReader.SIO_REQ_IDLE
            self.sio.connect(URL)
        except socketio.exceptions.ConnectionError as e:
            print(e)
            self.sioConn=VolumioReader.SIO_DISCONNECTED

    def on_pushState(self,data):
        self.sioData=data
        self.sioWait=VolumioReader.SIO_REQ_IDLE

    def on_pushListPlaylists(self,data):
        self.sioData=data
        self.sioWait=VolumioReader.SIO_REQ_IDLE

    def on_pushBrowseLibrary(self,data):
        self.sioData=data
        self.sioWait=VolumioReader.SIO_REQ_IDLE

    def on_pushQueue(self,data):
        self.sioData=data
        self.sioWait=VolumioReader.SIO_REQ_IDLE

    def sioWaitForIdle(self):
        while(self.sioWait==VolumioReader.SIO_REQ_PROCESSING and self.sioConn==VolumioReader.SIO_CONNECTED):
            time.sleep(DELAY_TICK)

    def on_connect(self):
        self.sioConn=VolumioReader.SIO_CONNECTED
        self.sioWait=VolumioReader.SIO_REQ_IDLE
        print('SocketIO sid is', self.sio.sid)

    def on_disconnect(self):
        self.sioConn=VolumioReader.SIO_DISCONNECTED
        self.sioWait=VolumioReader.SIO_REQ_IDLE
        print('disconnected')


    def checkErr(self):
        for i in range(0,len(self.errArr)):
            #wyszukanie pierwszego błędu starszego, niż ERR_MINUTES
            if(self.errArr[i]<datetime.datetime.now().timestamp()-ERR_MINUTES*60):
                #skrócenie tablicy
                self.errArr=self.errArr[:i]
                break

        self.IOErrCnt=len(self.errArr)

    def addErr(self):
        # dodanie timestamp do listy błędów
        self.errArr.insert(0,datetime.datetime.now().timestamp())
        self.updateDebug()
        print('Errors last {:d} minutes: {:d}'.format(ERR_MINUTES,self.IOErrCnt))        

    def updateScreen(self):
        if(GUI):
            pygame.display.flip()

    def printOnScreen(self,txt,x,y):
        if(GUI):
            font = pygame.font.SysFont("comicsansms", 16)
            text = font.render(txt, True, (255, 255, 255))
            self.screen.blit(text,(x,y))

    def update(self):
        # tu sprawdzić, czy reader nie jest w trakcie obsługi menu

        while(self.dispLock):
            time.sleep(DELAY_TICK)

        try:
            self.dispLock=True
            
            if(self.menuState==VolumioReader.IDLE):
                self.readVolumioState()                
            elif(self.menuState==VolumioReader.SHUTDOWN):
                self.readShutdownState()
            elif(self.menuState==VolumioReader.MENU):
                self.readMenuState()
            elif(self.menuState==VolumioReader.REMOTE_MPC):
                self.readRemoteMPCState()
            elif(self.menuState==VolumioReader.REMOTE_VLC):
                self.readRemoteVLCState()
            elif(self.menuState==VolumioReader.ENDED): #
                self.message(['','','',''])

            # tekst na wyświetlacz
            self.printState()
            
            if(self.vState.albumArtRefresh and self.menuState==VolumioReader.IDLE):
                self.printAlbumArt()
                self.vState.albumArtRefresh=False
            elif(self.vState.remoteScreenRefresh):
                if(self.menuState==VolumioReader.REMOTE_MPC):
                    self.printGraphics('/home/pi/python/MPC.png')
                elif(self.menuState==VolumioReader.REMOTE_VLC):
                    self.printGraphics('/home/pi/python/VLC.jpg')
        finally:
            self.dispLock=False

    def printState(self):

        for i in range(0,4):
            printArr=[]
            txt=self.lines.get(i)

            for j in range(0,MAX):
                printArr.append(ord(txt[j]))

            errflag=0
            while(errflag<5):            
                try:
                    # początkowa pozycja kursora wyświetlacza w kolejnej linii (32 bajty na linię)
                    while(self.i2cLock):
                        time.sleep(DELAY_TICK)
                    self.i2cLock=True
                    bus.write_byte_data(OLEDaddr,0x80,0x80+i*32) #Set DDRAM Address to 0x80 (line 1 start)
                    self.i2cLock=False
                except IOError as e:
                    printTimestamp()
                    print("[1]I/O error({0}): {1}".format(e.errno, e.strerror))
                    time.sleep(DELAY_ERR)
                    #print '{:02d}|{:02d}|{:02d}[{:s}]'.format(len(txt),COUNTER[i],pos,printTxt)
                finally:
                    self.i2cLock=False

                self.i2cLock=False
                try:
                    #wypisanie jednej linii (widoczne 20 znaków)
                    while(self.i2cLock):
                        time.sleep(DELAY_TICK)
                    self.i2cLock=True
                    bus.write_i2c_block_data(OLEDaddr,0x40,printArr)
                    self.i2cLock=False
                    errflag=99
                except IOError as e:
                    printTimestamp()
                    print("[2:{0}]I/O error({1}): {2}".format(errflag,e.errno, e.strerror))
                    self.addErr()
                    errflag+=1
                    time.sleep(DELAY_ERR)
                finally:
                    self.i2cLock=False
        
    def setAlbumArt(self,p_albumart,p_uri):
        if(self.isCD(p_uri)):
            p_albumart='/home/pi/python/cd.jpg'

        
        if(self.vState.albumArt!=p_albumart):
            print(p_albumart)
            self.vState.albumArt=p_albumart
            self.vState.albumArtRefresh=True
            OLED.Clear_Screen()

    def printGraphics(self,img):
        scx=128
        scy=128

        if(GUI):
            try:
                pyimage_orig=pygame.image.load(img)
                if pyimage_orig.get_bitsize()<24:
                    pyimage=pyimage_orig.convert()
                else:
                    pyimage=pyimage_orig

                pyimage2=pygame.transform.smoothscale(pyimage,(scx,scy))
                self.screen.blit(pyimage2, (0, 0))
                self.updateScreen()
                    
                pxarray = pygame.surfarray.array2d(pyimage2) 
                displayImageArr(pxarray)
            except ValueError as e:
                printTimestamp()
                print("[2:]Image display error(): {0}".format(str(e)))
        else:                
            pimage=Image.open(img).rotate(180,expand=True)
            pimage2=pimage.resize((scx,scy),resample=Image.LANCZOS)
            OLED.Display_Image(pimage2)

        

    def printAlbumArt(self):
        if('/home/pi/' in self.vState.albumArt):
            self.printGraphics(self.vState.albumArt)
            return
        
        url = URL+self.vState.albumArt \
              if (len(self.vState.albumArt)>0 and self.vState.albumArt[0:1]=='/') \
              else self.vState.albumArt

        (r,s) = self.request(url)
        if not s:
            return
        
        try:
            img = io.BytesIO(r.content)
            self.printGraphics(img)
        except pygame.error as e:
            # tylko wypisanie błędu
            print(e)


    def updateDebug(self):
        self.checkErr()
        self.debugOnScreen()

    def setOptions(self,p_repeatAll,p_repeatSingle,p_random):
        self.vState.repeatAll=p_repeatAll
        self.vState.repeatSingle=p_repeatSingle
        self.vState.random=p_random


    def isCD(self,p_uri):
        return 'cdda:///' in p_uri

    def setTitle(self,p_artist,p_album,p_title,p_uri,p_print=False):
        # supress incorrect info for CD Audio (this is often the previous disk's info)
        if(self.isCD(p_uri)):
            p_title="Track "+p_uri[8:]
            p_artist="CD Audio"
            p_album=""
        
        if(self.vState.artist!=p_artist or \
           self.vState.album!=p_album or \
           self.vState.title!=p_title):
            self.vState.artist=p_artist
            self.vState.album=p_album
            self.vState.title=p_title

            if(GUI):
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(128, 0, (512-128), 2*16))
                self.printOnScreen(self.vState.artist+'/'+self.vState.album,128,0)
                self.printOnScreen(self.vState.title,128,16)            
                self.updateScreen()

            if(p_print):
                print("Artist")
                for i in range(0,len(self.vState.artist)):
                    print("{}:{}".format(self.vState.artist[i],ord(self.vState.artist[i])))
                print("Album")
                for i in range(0,len(self.vState.album)):
                    print("{}:{}".format(self.vState.album[i],ord(self.vState.album[i])))
                print("Title")
                for i in range(0,len(self.vState.title)):
                    print("{}:{}".format(self.vState.title[i],ord(self.vState.title[i])))

    def setVState(self,p_state):
        if(self.vState.state!=p_state):
            self.vState.state=p_state

            if(GUI):
                pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(128, 32, (512-128), 16))
                self.printOnScreen(self.vState.state,128,32)
                self.updateScreen()


    def debugOnScreen(self):
        #%Y-%m-%d %H:%M:%S"
        txt='['+datetime.datetime.now().strftime('%H:%M:%S')+']'+ \
                 'IO err({:d}min):{:d}'.format(ERR_MINUTES,self.IOErrCnt)
        
        if(GUI):
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(128, 48, (512-128), 16))
            self.printOnScreen(txt,128,48)
            self.updateScreen()

    def timerOnScreen(self):
        #%Y-%m-%d %H:%M:%S"
        txt=self.vState.state+'/'+self.vState.timer
        if(GUI):
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(128, 32, (512-128), 16))
            self.printOnScreen(txt,128,32)
            self.updateScreen()

    def stateOnScreen(self):
        if(GUI):
            pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(128, 64, (512-128), 4*16))
            for i in range(0,4):
                self.printOnScreen('['+self.lines.get(i)+']',128,64+i*16)
                self.updateScreen()
                
        

    def readMenuState(self):        
        self.lines.setTexts(self.menuControl.getCaption(), \
                            self.menuControl.getItem(0), \
                            self.menuControl.getItem(1), \
                            self.menuControl.getItem(2))

        if(self.menuControl.playlists.state==VolumioPlaylists.NONE and \
           self.menuControl.state==VolumioMenuControl.PLAYLIST):
            self.readPlaylists()
        elif(self.menuControl.radios.state==VolumioWebRadios.NONE and \
           self.menuControl.state==VolumioMenuControl.RADIOS):
            self.readRadios()


    def readRemoteMPCState(self):        
        (resp,s)=self.request(MPC_URL+'/variables.html',0.25)

        if(not s):
            # wyjście do głównego menu (mozna dorobić licznik timeoutów)
            self.vState.remoteTimeouts+=1
            print('Timeouts:{:d}'.format(self.vState.remoteTimeouts))

            state2=' waiting {:d}...'.format(self.vState.remoteTimeouts)

            self.lines.setTexts('MPC Remote Control', '', state2, '')

            if(self.vState.remoteTimeouts>20):
                self.menuState=VolumioReader.IDLE
                self.vState.setRefreshFlags(True,False)
                self.vState.remoteTimeouts=0
                self.message(['MPC Remote Control','','   timeout :(',''],1)
            return

        self.vState.remoteTimeouts=0
        
        parser = MPCParser()
        parser.feed(resp.text)

        fileTxt=strReplace1(parser.var['file']) if('file' in parser.var) else ""
        fileTxt=unicodedata.normalize('NFKD',fileTxt.translate(VolumioReader.trtab)).encode('ascii','replace').decode('utf-8')
        fileTxt=strReplace2(fileTxt)        

        pathTxt=strReplace1(parser.var['filedir']) if('filedir' in parser.var) else ""
        pathTxt=unicodedata.normalize('NFKD',pathTxt.translate(VolumioReader.trtab)).encode('ascii','replace').decode('utf-8')
        pathTxt=strReplace2(pathTxt)        
        
        stateStr=parser.var['state'] if('state' in parser.var) else "1"
        
        state0=chr(0x10) if(stateStr=='2') else chr(0xD0)

        posStr=parser.var['positionstring'] if('positionstring' in parser.var) else "00:00:00"
        posStr1=parser.var['position'] if('position' in parser.var) else "0"
        durStr=parser.var['durationstring'] if('durationstring' in parser.var) else "00:00:00"
        durStr1=parser.var['duration'] if('duration' in parser.var) else "0"

        state0=state0+' '+posStr+'/'+durStr
        volStr=parser.var['volumelevel'] if('volumelevel' in parser.var) else "0"
        volTxt=volStr
        try:
            volTxt=volArr[int(int(volStr)/10)]
        except:
            pass

        #state0=state0+' '+volTxt
        pos=0
        try:
            pos=int(100*int(posStr1)/int(durStr1))
        except:
            pass

        #sizeTxt=parser.var['size']
        posTxt='  ({:02d}%)'.format(pos)
        state1='{: <{:d}}'.format(posTxt,MAX-1-len(volTxt))
        state1=state1+' '+volTxt      

        self.lines.setTexts(state0,state1,fileTxt,pathTxt)
        self.lines.genPrintText()
        
    def readRemoteVLCState(self):        
        (resp,s)=self.request(VLC_URL+'/requests/status.xml',0.25,VLC_PASS)

        if(not s):
            # wyjście do głównego menu (mozna dorobić licznik timeoutów)
            self.vState.remoteTimeouts+=1
            print('Timeouts:{:d}'.format(self.vState.remoteTimeouts))

            state2=' waiting {:d}...'.format(self.vState.remoteTimeouts)

            self.lines.setTexts('VLC Remote Control', '', state2, '')

            if(self.vState.remoteTimeouts>20):
                self.menuState=VolumioReader.IDLE
                self.vState.setRefreshFlags(True,False)
                self.vState.remoteTimeouts=0
                self.message(['VLC Remote Control','','   timeout :(',''],1)
            return

        self.vState.remoteTimeouts=0

        root=ElementTree.fromstring(resp.text)    
        
        fileTxt=strReplace1(XMLFind(root,'./information/category/[@name="meta"]/info/[@name="filename"]'))
        fileTxt=unicodedata.normalize('NFKD',fileTxt.translate(VolumioReader.trtab)).encode('ascii','replace').decode('utf-8')
        fileTxt=strReplace2(fileTxt)        
        
        stateStr=XMLFind(root,'./state')        
        state0=chr(0x10) if(stateStr=='playing') else chr(0xD0)

        posStr=XMLFind(root,'./time')
        posNum=0
        try:
            posNum=int(posStr)
            posStr='{:02d}:{:02d}:{:02d}'.format(posNum//3600,posNum//60,posNum%60)
        except:
            pass
        
        durStr=XMLFind(root,'./length')
        durNum=1
        try:
            durNum=int(durStr)
            durStr='{:02d}:{:02d}:{:02d}'.format(durNum//3600,durNum//60,durNum%60)
        except:
            pass

        state0=state0+' '+posStr+'/'+durStr
        volStr=XMLFind(root,'./volume')
        volTxt=volStr
        volNum=0
        try:
            volNum=int(volStr)
            volPrefix=''
            if(volNum>256):
                volPrefix='+'
                volNum=256
            volTxt=volPrefix+volArr[int(volNum/256*10)]
        except:
            pass

        pos=int(100*int(posNum)/int(durNum)) if durNum>0 else 0

        posTxt='  ({:02d}%)'.format(pos)
        state1='{: <{:d}}'.format(posTxt,MAX-1-len(volTxt))
        state1=state1+' '+volTxt      

        self.lines.setTexts(state0,state1,fileTxt,'')
        self.lines.genPrintText()        
        

    def readShutdownState(self):
        if(self.shutdownTh==None):
            self.lines.setTexts('SHUTDOWN','','Invalid timer','')
        else:
            self.lines.setTexts('SHUTDOWN','','Press Shutdown','   in {} sec.'.format(self.shutdownTh.timeSec))
  
    def readPlaylists(self):
        if(self.sioConn!=VolumioReader.SIO_CONNECTED):
            return

        if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
            return
            
        self.sioWait=VolumioReader.SIO_REQ_PROCESSING
        self.sio.emit('listPlaylist', '')
        self.sioWaitForIdle()

        js=self.sioData

        #print(js)
        print('Playlists: {}'.format(len(js)))
        self.menuControl.readPlaylists(js)

    def readRadios(self):
        if(self.sioConn!=VolumioReader.SIO_CONNECTED):
            return

        if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
            return
            
        self.sioWait=VolumioReader.SIO_REQ_PROCESSING
        self.sio.emit('browseLibrary', {'uri':'radio/favourites'})
        self.sioWaitForIdle()

        js=self.sioData

        #print(js)
        #print('Radios: {}'.format(len(js)))
        self.menuControl.readRadios(js)

    def getCDTracks(self):
        if(self.sioConn!=VolumioReader.SIO_CONNECTED):
            return

        if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
            return
            
        self.sioWait=VolumioReader.SIO_REQ_PROCESSING
        self.sio.emit('browseLibrary', {'uri':'audiocd'})
        self.sioWaitForIdle()

        js=self.sioData
        if('navigation' in js):
            nav=js['navigation']
            if('lists' in nav):
                ls=nav['lists'][0]
                if('items' in ls):                    
                    return len(ls['items'])            

        return 0

    def getCurrentTracks(self):
        if(self.sioConn!=VolumioReader.SIO_CONNECTED):
            return

        if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
            return
            
        self.sioWait=VolumioReader.SIO_REQ_PROCESSING
        self.sio.emit('getQueue', {})
        self.sioWaitForIdle()

        js=self.sioData
        return len(js)


    def message(self,txt,delay=0):
        self.lines.setTexts(txt[0],txt[1],txt[2],txt[3])
        self.printState()
        if(delay>0):
            time.sleep(delay)

    def nextAlbum(self):
        if(self.sioConn!=VolumioReader.SIO_CONNECTED):
            return

        if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
            return

        self.message(['','   Ommmmmmmmm','     ...',''])
            
        self.sioWait=VolumioReader.SIO_REQ_PROCESSING
        self.sio.emit('getQueue', '')
        self.sioWaitForIdle()

        js=self.sioData
        curr=self.vState.n

        #for i in range(0,len(js)):
        #    j=js[i]
        #    print('{}.{}/{}'.format(i,j['name'],j['album']))
        
        
        print('current track {:d}'.format(curr))

        pos=-1
        for i in range(curr+1,len(js)):
            if(self.vState.album!=jsonNormalize(js[i],'album',char_print)):
                pos=i
                break

        if(pos==-1):
            for i in range(0,curr):
                if(self.vState.album!=jsonNormalize(js[i],'album',char_print)):
                    pos=i
                    break
                
        if(pos==-1):
            print('next album not found')
            return

        print('play position:{:d}'.format(pos))

        url = URL+'/api/v1/commands/?cmd=play&N={:d}'.format(pos)
        (r,s) = self.request(url)



    def readVolumioState(self):
        try:
            if(self.sioConn==VolumioReader.SIO_DISCONNECTED):
                self.connect()
                raise IOError('Not connected')
            elif(self.sioConn==VolumioReader.SIO_CONNECTING):
                print('sioConn=1')
                return

            if(self.sioWait==VolumioReader.SIO_REQ_PROCESSING):
                return
            self.sioWait=VolumioReader.SIO_REQ_PROCESSING
            self.sio.emit('getState', '')
            self.sioWaitForIdle()

            js=self.sioData
            
            try:
                self.setVState(getVar(js,'status'))
            except TypeError as e:
                # czasem zdarza się chwilowy błąd przy przełączaniu list
                print(e)
                return

            art=jsonNormalize(js,'artist',char_print) #.decode('utf-8')
            alb=jsonNormalize(js,'album',char_print) #.decode('utf-8')
            tit=jsonNormalize(js,'title',char_print) #.decode('utf-8')
            uri=jsonNormalize(js,'uri') #.decode('utf-8')
            
            self.setTitle(art,alb,tit,uri,char_print)
            self.setAlbumArt(getVar(js,'albumart'),uri)
            self.setOptions(getVar(js,'repeat'),getVar(js,'repeatSingle'),getVar(js,'random'))
            self.vState.n=getVar(js,'position')            
                          
            state0=chr(0x10) if(getVar(js,'status')=='play') else chr(0xD0)

            seek=0
            try:
                if(isinstance(getVar(js,'seek'),int)):
                    seek=int(getVar(js,'seek')) // 1000
            except:
                seek=0
            
            seekTxt='{:02d}:{:02d}'.format(seek //60,seek % 60)
            dur=0
            try:
                if(isinstance(getVar(js,'seek'),int)):
                    dur=int(getVar(js,'duration'))
            except:
                dur=0

            durTxt='{:02d}:{:02d}'.format(dur //60,dur % 60)
            timerTxt=seekTxt+'/'+durTxt
            self.vState.timer=timerTxt
            self.timerOnScreen()

            if(len(timerTxt)<=12):
                state0=state0+' '
            state0=state0+timerTxt
            if(len(timerTxt)<=11):
                state0=state0+' '
            
            # czasem volume to tekst, czasem liczba
            volTxt='0'
            if(getVar(js,'mute')):                
                volTxt=volArr[0]
            else:
                v=getVar(js,'volume')
                
                if(isinstance(v,int) or \
                   (isinstance(v,str) and v.isdigit())):
                    volTxt=volArr[int(int(v)/10)]
                    # potrzebne do ustalania głośności - 2020-05-21 przestało dziłać +/-
                    self.vState.volume=int(getVar(js,'volume'))

            #print ord(volTxt[0])            
            state0=state0+volTxt
            #repeatChr=chr(0x1c) if(js['repeat'] or js['repeatSingle']) else ' '
            #state0=state0+repeatChr
            state0='{: <{:d}}'.format(state0,MAX)

            self.lines.setTexts(state0,self.vState.artist,self.vState.album,self.vState.title)

        except IOError as e:
            self.setConnMessage()
            printTimestamp()
            print("[0]I/O error({0}): {1}".format(e.errno, e.strerror))
            print(e)
            time.sleep(DELAY_ERR)

        self.lines.genPrintText()


    def setConnMessage(self):
        self.lines.setTexts('Connecting','  to','  Volumio player...','')
            

    def printShutdown(self):
        self.message(['','','',''])

    def shutdown(self):
        print("SHUTDOWN")
        self.menuState=VolumioReader.ENDED
        self.printShutdown()
        if(self.sioConn==VolumioReader.SIO_CONNECTED):
            self.sio.emit('shutdown', '')
        OLED.Clear_Screen()
        os.system("sudo shutdown -h now")

    def idle(self):
        print("IDLE")
        # na wszelki wypadek odświeżenie albumArt
        self.vState.setRefreshFlags(True,False)
        self.menuState=VolumioReader.IDLE

    def process(self,key):
        if(key<0 or key>7):
            return

        while(self.menuState==VolumioReader.PROCESSING):
            time.sleep(DELAY_TICK)

        # przechowanie stanu
        tmpState=self.menuState
        # zmiana stanu - blokada
        self.menuState=VolumioReader.PROCESSING
        print('reader-process:{:d}'.format(key))
        self.function='{:01d}'.format(key)

        # play/stop
        if(key==0):
            if(tmpState==VolumioReader.IDLE):
                self.sio.emit('toggle', '')
            elif(tmpState==VolumioReader.REMOTE_MPC):
                (r,s)=self.request(MPC_URL+'/command.html?wm_command=889',0.25)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                (r,s)=self.request(VLC_URL+'/requests/status.xml?command=pl_pause',0.25,VLC_PASS)
        # left
        elif(key==1):
            if(tmpState==VolumioReader.IDLE):
                self.sio.emit('prev', '')
            # jump back (medium)
            elif(tmpState==VolumioReader.REMOTE_MPC):
                (r,s)=self.request(MPC_URL+'/command.html?wm_command=903',0.25)
            # seek (-30s)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                (r,s)=self.request(VLC_URL+'/requests/status.xml?command=seek&val=-30s',0.25,VLC_PASS)
            elif(tmpState==VolumioReader.MENU):
                action=self.menuControl.process(key)
                #wyjście z menu
                if(action['name']=='exit'):
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
        # right
        elif(key==2):
            if(tmpState==VolumioReader.IDLE):
                self.sio.emit('next', '')
            # jump forward (medium)
            elif(tmpState==VolumioReader.REMOTE_MPC):
                (r,s)=self.request(MPC_URL+'/command.html?wm_command=904',0.25)
            # seek (+30s)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                (r,s)=self.request(VLC_URL+'/requests/status.xml?command=seek&val=%2B30s',0.25,VLC_PASS)
            elif(tmpState==VolumioReader.MENU):
                action=self.menuControl.process(key)
                #wybór playlisty
                if(action['name']=='playlist'):
                    playlist=action['param1']
                    action2=action['param2']
                    print(playlist)
                    self.message(['','   Ommmmmmmmm','     ...',''],DELAY_MSG)
                    if(playlist!=''):
                        if(action2=='play'):
                            self.sio.emit('playPlaylist',{'name':playlist})                            
                        elif(action2=='add'):
                            self.sio.emit('enqueue',{'name':playlist})
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
                elif(action['name']=='playradio'):
                    print('radio: '+action['param1'])
                    self.message(['','   Ommmmmmmmm','     ...',''],DELAY_MSG)
                    if(action['param1'])=="audiocd":
                        cd_tracks = self.getCDTracks()
                        print(cd_tracks)
                        if(cd_tracks>0):
                            #curr_tracks = self.getCurrentTracks()
                            #print(curr_tracks)
                            #for i in range(0,curr_tracks):
                            #    print("removing "+str(i))
                            #    self.sio.emit('removeFromQueue',{"value":0})
                            #self.sioWaitForIdle()
                            #for i in range(0,cd_tracks):
                            #    print("adding "+"track"+str(i))
                            #    self.sio.emit('addToQueue',{"uri":"cdda:///"+str(i)})
                            #self.sioWaitForIdle()                            
                            self.sio.emit('replaceAndPlay',{"name":"Audio CD","service": "cd_controller","uri":action['param1']})
                            #self.sioWaitForIdle()
                        else:
                            self.message(['','   No disc','    or','   not ready'],DELAY_MSG)                           
                    else:
                        self.sio.emit('replaceAndPlay',{"name":"Radio","service": "webradio","uri":action['param1']})
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
                elif(action['name']=='nextalbum'):
                    print('next album')
                    self.nextAlbum()
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
                elif(action['name']=='repeatAll'):
                    print('repeat all')
                    print(self.vState.repeatAll)
                    self.sio.emit('setRepeat',{'value':not self.vState.repeatAll})
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
##                elif(action['name']=='repeatSingle'):
##                    print('repeat single')
##                    print(self.vState.repeatSingle)
##                    self.sio.emit('setRepeat','') # {'value':not self.vState.repeatSingle})
##                    self.menuControl.exit()
##                    tmpState=VolumioReader.IDLE
                elif(action['name']=='random'):
                    print('random')
                    self.sio.emit('setRandom',{'value':not self.vState.random})
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
                elif(action['name']=='skip+'):
                    print('skip+')
                    url = URL+'/api/v1/commands/?cmd=seek&position=plus'
                    (r,s) = self.request(url)
                    #self.menuControl.exit()
                    #tmpState=VolumioReader.IDLE
                elif(action['name']=='skip-'):
                    print('skip-')
                    url = URL+'/api/v1/commands/?cmd=seek&position=minus'
                    (r,s) = self.request(url)
                    #self.menuControl.exit()
                    #tmpState=VolumioReader.IDLE
                elif(action['name']=='MPC'):
                    print('MPC')
                    self.message(['','     MPC Remote','',''],1)
                    self.menuControl.exit()                    
                    tmpState=VolumioReader.REMOTE_MPC
                    self.vState.setRefreshFlags(False,True)
                elif(action['name']=='VLC'):
                    print('VLC')
                    self.message(['','     VLC Remote','',''],1)
                    self.menuControl.exit()
                    tmpState=VolumioReader.REMOTE_VLC
                    self.vState.setRefreshFlags(False,True)
                
        # up
        elif(key==3):
            if(tmpState==VolumioReader.IDLE):
                self.sio.emit('volume', self.vState.volume+VolumioState.VOL_STEP)
            # vol up
            elif(tmpState==VolumioReader.REMOTE_MPC):
                (r,s)=self.request(MPC_URL+'/command.html?wm_command=907',0.25)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                # %2B to +
                (r,s)=self.request(VLC_URL+'/requests/status.xml?command=volume&val=%2B16',0.25,VLC_PASS)
            elif(tmpState==VolumioReader.MENU):                
                self.menuControl.process(key)
        # down
        elif(key==4):
            if(tmpState==VolumioReader.IDLE):
                self.sio.emit('volume', self.vState.volume-VolumioState.VOL_STEP)
            # vol down
            elif(tmpState==VolumioReader.REMOTE_MPC):
                (r,s)=self.request(MPC_URL+'/command.html?wm_command=908',0.25)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                (r,s)=self.request(VLC_URL+'/requests/status.xml?command=volume&val=-16',0.25,VLC_PASS)
            elif(tmpState==VolumioReader.MENU):
                self.menuControl.process(key)
        #menu
        elif(key==5):
            if(tmpState==VolumioReader.IDLE):
                #wejście do menu
                tmpState=VolumioReader.MENU
                self.menuControl.enter()
            elif(tmpState==VolumioReader.MENU):
                action=self.menuControl.process(key)
                #wyjście z menu
                if(action['name']=='exit'):
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
            elif(tmpState==VolumioReader.REMOTE_MPC):
                tmpState=VolumioReader.IDLE
                self.vState.setRefreshFlags(True,False)
            elif(tmpState==VolumioReader.REMOTE_VLC):
                tmpState=VolumioReader.IDLE
                self.vState.setRefreshFlags(True,False)
                
        #menu2
        elif(key==6):
            if(tmpState==VolumioReader.IDLE):
                #wejście do menu
                tmpState=VolumioReader.MENU
                self.menuControl.enter2()
            elif(tmpState==VolumioReader.MENU):
                action=self.menuControl.process(key)
                #wyjście z menu
                if(action['name']=='exit'):
                    self.menuControl.exit()
                    tmpState=VolumioReader.IDLE
            elif(tmpState==VolumioReader.REMOTE_MPC):
                tmpState=VolumioReader.IDLE
                self.vState.albumArtRefresh=True
            elif(tmpState==VolumioReader.REMOTE_VLC):
                tmpState=VolumioReader.IDLE
                self.vState.albumArtRefresh=True

        elif(key==7):
            if(tmpState!=VolumioReader.SHUTDOWN):
                self.shutdownTh=DelayThread(5,0.1,self.idle,False) 
                self.shutdownTh.start()
                tmpState=VolumioReader.SHUTDOWN
            elif(tmpState==VolumioReader.SHUTDOWN):
                self.shutdownTh.stop()
                self.shutdownTh.join()
                self.shutdown()

        #odtworzenie stanu
        if(self.menuState!=VolumioReader.ENDED):
            self.menuState=tmpState

        print('reader-end-process:{:d}'.format(key))

    def wait_for_file(self,file,seconds=10):
        sec=0
        while sec<seconds:
            if os.path.exists(file):
                return
            sec+=1
            time.sleep(1)
        
    
    def request(self,url,p_tout=10,p_pass=''):
        if(url==''):
            return ('',False)

        resp=None
        respStatus=False
        self.reqLock=True
        try:
            s = requests.Session()
            if(p_pass==''):
                resp=s.get(url,timeout=p_tout,verify=False)
            else:
                resp=s.get(url,timeout=p_tout,auth=('',p_pass))
            respStatus=True
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, \
                requests.exceptions.ConnectionError,requests.exceptions.MissingSchema) as e:
            print('GET:'+type(e).__module__+'/'+type(e).__qualname__+'/'+type(e).__name__)
            #traceback.print_exc()
        finally:
            self.reqLock=False

        return (resp,respStatus)
        
        

    def quit(self):
        self.sio.disconnect()


def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LCD_RST_PIN, GPIO.OUT)
    
    
    
def initLCD():
    GPIO.output(LCD_RST_PIN,GPIO.LOW)
    time.sleep(DELAY_RST)
    GPIO.output(LCD_RST_PIN,GPIO.HIGH)
    time.sleep(DELAY_RST)
    
    try:
        
        bus.write_byte_data(OLEDaddr,0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0	
        bus.write_byte_data(OLEDaddr,0x80,0x09) # 4-line mode	
        bus.write_byte_data(OLEDaddr,0x80,0x05) # view 0
        bus.write_byte_data(OLEDaddr,0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0
        
        bus.write_byte_data(OLEDaddr,0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0 
        bus.write_byte_data(OLEDaddr,0x80,0x72) # ROM selection
        bus.write_byte_data(OLEDaddr,0x40,0x00) # ROM jako dane A=0x00 B=0x04 C=0x0C
        bus.write_byte_data(OLEDaddr,0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0

        bus.write_byte_data(OLEDaddr,0x80,0x3A) # function set: N=1 BE=0 RE=1 IS=0
        bus.write_byte_data(OLEDaddr,0x80,0x79) # SD=1
        bus.write_byte_data(OLEDaddr,0x80,0x81) # contrast set
        bus.write_byte_data(OLEDaddr,0x80,0x00) # wartosc jako komenda, nie dane
        bus.write_byte_data(OLEDaddr,0x80,0x78) # SD=0   
        bus.write_byte_data(OLEDaddr,0x80,0x38) # function set: N=1 BE=0 RE=0 IS=0
        
        bus.write_byte_data(OLEDaddr,0x80,0x0D) # ??? (bez tego czasem nie dziala)
        bus.write_byte_data(OLEDaddr,0x80,0x01) # clear display
        bus.write_byte_data(OLEDaddr,0x80,0x80) #Set DDRAM Address to 0x80 (line 1 start)
        time.sleep (DELAY) # na wszelki wypadek
        bus.write_byte_data(OLEDaddr,0x80,0x0C) # turn on
    except IOError as e:
        printTimestamp()
        print("[5]I/O error({0}): {1}".format(e.errno, e.strerror))
        time.sleep(DELAY_ERR)
        raise


class I2CKeys:
    IDLE=0
    PROCESSING=1
    PROCESSED=2
    
    def __init__(self,p_bus,p_reader):
        self.bus=p_bus
        self.keys=255
        self.key=-1
        self.state=I2CKeys.IDLE
        self.reader=p_reader

    def i2cread(self):
        val=255
        try:
            while(self.reader.i2cLock):
                time.sleep(DELAY_TICK)
            self.reader.i2cLock=True
            val=bus.read_byte(KEYSaddr)
            if(val!=255):
                print(val)
            self.reader.i2cLock=False
        except IOError as e:
            printTimestamp()
            print("[3]I/O error({0}): {1}".format(e.errno, e.strerror))
            val=255
            time.sleep(DELAY_ERR)
        finally:
            self.reader.i2cLock=False

        return val
        

    def readKeys(self):
        if(self.state==I2CKeys.IDLE):
            k=self.i2cread()
            if(k!=255):
                print('read:{:d}'.format(k))
                self.setKeys(k)
                if(self.key!=-1):
                    self.state=I2CKeys.PROCESSING
        elif(self.state==I2CKeys.PROCESSING):
            self.process()
            self.state=I2CKeys.PROCESSED
        elif(self.state==I2CKeys.PROCESSED):
            k=self.i2cread()
            if(k==255):
                self.setKeys(k)
                self.state=I2CKeys.IDLE
                
    def setKeys(self,k):
        self.keys=k
        self.key=self.decode(k)

    def decode(self,k):
        i=0
        kinv=255-k
        while(i<8):
            # wykrywany jest tylko pierwszy klawisz
            if((kinv & (1<<i))>>i):
                return i
            i+=1
        return -1
    
    def process(self):
        print('keys-process:{:d}'.format(self.key))
        #self.reader.process(self.key)
        #time.sleep(0.3)
        self.reader.addKey(self.key)
        dummy=0

class DelayThread(threading.Thread):
    def __init__(self,p_delay,p_tick,p_func,p_inf):
        threading.Thread.__init__(self)
        self._stopEvent=threading.Event()
        self.deamon=True
        self.delay=p_delay
        self.tick=p_tick
        self.func=p_func
        self.timeSec=0
        self.inf=p_inf

    def run(self):
        startTS=datetime.datetime.now().timestamp()
        while(True):
            if(self._stopEvent.is_set()):
                return
            currTS=datetime.datetime.now().timestamp()
            diffTS=currTS-startTS
            self.timeSec=self.delay-int(diffTS)
            if(self.timeSec)<0:
                self.func()
                if(self.inf):
                    startTS=datetime.datetime.now().timestamp()
                else:
                    break
            time.sleep(self.tick)
        

    def stop(self):
        self._stopEvent.set()

def dummyFunc():
    print("dummy")


def Test_Pattern():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    
    draw.line([(0,8), (127,8)],   fill = "RED",    width = 16)
    draw.line([(0,24),(127,24)],  fill = "YELLOW", width = 16)
    draw.line([(0,40),(127,40)],  fill = "GREEN",  width = 16)
    draw.line([(0,56),(127,56)],  fill = "CYAN",   width = 16)
    draw.line([(0,72),(127,72)],  fill = "BLUE",   width = 16)
    draw.line([(0,88),(127,88)],  fill = "MAGENTA",width = 16)
    draw.line([(0,104),(127,104)],fill = "BLACK",  width = 16)
    draw.line([(0,120),(127,120)],fill = "WHITE",  width = 16)
    
    OLED.Display_Image(image)


def displayImageArr(imgArr):
    #kopia Display_Image

    OLED.Set_Coordinate(0,0)
    for y1 in range(0, OLED.SSD1351_HEIGHT):
        #odbicie w pionie
        y=OLED.SSD1351_HEIGHT-y1-1            
        for x1 in range(0, OLED.SSD1351_WIDTH): #RGB 8-8-8 (3 bytes) --> 5-6-5 (2 bytes): RRRRRrrr, GGGGGGgg, BBBBBbbb --> RRRRRGGG GGGBBBBB
            x=OLED.SSD1351_WIDTH-x1-1
            b=int((imgArr[x,y] & 0xFF0000) >> 16)
            g=int((imgArr[x,y] & 0x00FF00) >> 8)
            r=int((imgArr[x,y] & 0x0000FF))
            OLED.color_fill_byte[x1*2] = ((r & 0xF8)|(g >> 5))
            OLED.color_fill_byte[x1*2+1] = (((g << 3) & 0xE0)|(b >> 3))
        OLED.Write_Datas(OLED.color_fill_byte)


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gui', type=str, choices=['Y', 'N'], default='Y',help='Y for GUI, N for console only')

    return parser.parse_args()


def main():
    global GUI
    flags = vars(read_args())
    print('GUI={}'.format(flags['gui']))
    GUI=flags['gui']=='Y'

    if(GUI):
        print('GUI')
        global pygame
        import pygame
    else:
        print('HEADLESS')

    print(os.environ.get("USERNAME"))
    print(os.popen("type python3").read())

    global bus
    bus=smbus.SMBus(1)
    if(GUI):
        pygame.init()

    initGPIO()
    initLCD()
    OLED.Device_Init()

    Test_Pattern()

    vReader=VolumioReader(0.05,6,2)
    keys=I2CKeys(bus,vReader)
    vReader.setKeysReader(keys)

    try:
        vReader.mainLoop()

    finally:

        OLED.Clear_Screen()
        GPIO.cleanup()

        vReader.quit()
        if(GUI):
            pygame.quit()
        print("KONIEC")

main()    

