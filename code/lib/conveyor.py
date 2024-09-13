import board
import busio
from digitalio import Direction,Pull
from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_debouncer import Debouncer
from RGBLED import *

import iomapping

class conveyorInterface():
    # Output Mappings
    pump = iomapping.QX0
    motor = iomapping.QX1
    
    whitePusher = iomapping.QX2
    redPusher = iomapping.QX3
    bluePusher = iomapping.QX4

    # Analog Input Mapping
    colourSensor = iomapping.IW0

    def __init__(self):
        self.initMCP()
        self.initInputs()
    
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
        for pin in [6,7]]:
            self.MCPpins[pin].direction = Direction.INPUT
            self.MCPpins[pin].pull = Pull.UP
        self.redButton = Debouncer(self.MCPpins[7])
        self.greenButton = Debouncer(self.MCPpins[6])

        self.armButton = self.redButton
        self.disarmButton = self.greenButton
    
    def initInputs(self):
        # Digital Input Mapping
        self.incomingBarrier = Debouncer(iomapping.IX2)
        self.outgoingBarrier = Debouncer(iomapping.IX5)
        self.rotaryEncoder = Debouncer(iomapping.IX4)

    @property
    def armButton(self):
        return not self.redButton.value # Needs a not because these are active low
    
    @property
    def disarmButton(self):
        return not self.greenButton.value # Needs a not because these are active low

    @property
    def colourLED(self):
        return self._colourLED.value
    
    @colourLED.setter
    def colourLED(self,value):
        self._colourLED.value = value

    @property
    def statusLED(self):
        return self._statusLED.value
    
    @colourLED.setter
    def statusLED(self,value):
        self._statusLED.value = value

    def update(self):
        self.incomingBarrier.update()
        self.outgoingBarrier.update()
        self.rotaryEncoder.update()
        self.greenButton.update()
        self.redButton.update()
