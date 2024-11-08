import board
import busio
from digitalio import Direction,Pull
from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_debouncer import Debouncer
from RGBLED import *

import iomapping

class conveyorInterface():
    'Class that provides a simple interface to all the inputs and outputs of the conveyor belt'
    relayActiveLow = False
    # Output Mappings
    _pump = iomapping.QX0
    _motor = iomapping.QX1
    
    _whitePusher = iomapping.QX2
    _redPusher = iomapping.QX3
    _bluePusher = iomapping.QX4

    # Analog Input Mapping
    colourSensor = iomapping.IW0

    def __init__(self):
        self.initMCP()
        self.initInputs()
    
    def initMCP(self):
        'Sets up the MCP object and provides all the pins'
        
        self.mcp = MCP23008(iomapping.I2C)
        self.MCPpins = []
        for i in range(0,8):
            self.MCPpins.append(self.mcp.get_pin(i))
        self.initLEDs() # setup LEDs attached to the MCP
        self.initButtons() # setup buttons attached to the MCP
    
    def initLEDs(self):
        'Sets up the status and colour LEDs attached to the MCP'
        for pin in range(0,6):
            self.MCPpins[pin].direction = Direction.OUTPUT
            self.MCPpins[pin].value = False
        self._colourLED = LED(self.MCPpins[0],self.MCPpins[2],self.MCPpins[1])
        self._statusLED = LED(self.MCPpins[3],self.MCPpins[5],self.MCPpins[4])
    
    def initButtons(self):
        'Sets up the buttons attached to the MCP, with debouncers'
        for pin in [6,7]:
            self.MCPpins[pin].direction = Direction.INPUT
            self.MCPpins[pin].pull = Pull.UP
        self.redButton = Debouncer(self.MCPpins[7])
        self.greenButton = Debouncer(self.MCPpins[6])
    
    def initInputs(self):
        'Sets up debouncers on the digital inputs'
        self._incomingBarrier = Debouncer(iomapping.IX2)
        self._outgoingBarrier = Debouncer(iomapping.IX5)
        self._rotaryEncoder = Debouncer(iomapping.IX4)

    @property
    def armButton(self):
        return not self.redButton.value # Needs a not because these are active low
    
    @property
    def disarmButton(self):
        return not self.greenButton.value # Needs a not because these are active low
    
    @property
    def incomingBarrier(self):
        return not self._incomingBarrier.value
    
    @property
    def outgoingBarrier(self):
        return not self._outgoingBarrier.value
    
    @property
    def rotaryEncoder(self):
        return not self._rotaryEncoder.value
    
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
    
    @property
    def pump(self):
        return self.relayActiveLow ^ self._pump.value
    
    @pump.setter
    def pump(self,value):
        self._pump.value = self.relayActiveLow ^ value
    
    @property
    def motor(self):
        return self.relayActiveLow ^ self._motor.value
    
    @motor.setter
    def motor(self,value):
        self._motor.value = self.relayActiveLow ^ value
    
    @property
    def whitePusher(self):
        return self.relayActiveLow ^ self._whitePusher.value
    
    @whitePusher.setter
    def whitePusher(self,value):
        self._whitePusher.value = self.relayActiveLow ^ value
    
    @property
    def redPusher(self):
        return self.relayActiveLow ^ self._redPusher.value
    
    @redPusher.setter
    def redPusher(self,value):
        self._redPusher.value = self.relayActiveLow ^ value
    
    @property
    def bluePusher(self):
        return self.relayActiveLow ^ self._bluePusher.value
    
    @bluePusher.setter
    def bluePusher(self,value):
        self._bluePusher.value = self.relayActiveLow ^ value
    
    def update(self):
        # runs update on all the debouncers
        self._incomingBarrier.update()
        self._outgoingBarrier.update()
        self._rotaryEncoder.update()
        self.greenButton.update()
        self.redButton.update()
