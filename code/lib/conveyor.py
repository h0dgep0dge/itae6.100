import board
import busio
from digitalio import Direction,Pull
from adafruit_mcp230xx.mcp23008 import MCP23008
from RGBLED import *

import iomapping

class conveyor():
    # Pin mapping

    # Outputs
    pump = iomapping.QX0
    motor = iomapping.QX1

    whitePusher = iomapping.QX2
    redPusher = iomapping.QX3
    bluePusher = iomapping.QX4

    # Inputs
    incomingBarrier = iomapping.IX2
    outgoingBarrier = iomapping.IX5
    rotaryEncoder = iomapping.IX4

    colour = iomapping.IW0

    def __init__(self):
        self.initMCP()
    
    def initMCP(self):
        self.mcp = MCP23008(iomapping.I2C)
        self.MCPpins = []
        for i in range(0,8):
            self.MCPpins.append(self.mcp.get_pin(i))
        self.initLEDs()
        self.initButtons()
    
    def initLEDs(self):
        for pin in range(0,6):
            self.MCPpins[pin].direction = Direction.OUTPUT
            self.MCPpins[pin].value = False
        self._colourLED = LED(self.MCPpins[0],self.MCPpins[2],self.MCPpins[1])
        self._statusLED = LED(self.MCPpins[3],self.MCPpins[5],self.MCPpins[4])
    
    def initButtons(self):
        for pin in range(6,8):
            self.MCPpins[pin].direction = Direction.INPUT
            self.MCPpins[pin].pull = Pull.UP
        self.start = self.MCPpins[7]
        self.stop = self.MCPpins[6]
    
    @property
    def colourLED(self):
        return self._colourLED.value
    
    @colourLED.setter
    def colourLED(self,value):
        self._colourLED.value = value
        
            
