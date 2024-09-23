import board
import busio
from digitalio import Direction,Pull
from adafruit_mcp230xx.mcp23008 import MCP23008
from adafruit_debouncer import Debouncer
from RGBLED import *

import iomapping

class Inverter:
    __init__(self,valIn):
        self._valIn = valIn
    
    @property
    def value(self):
        return not self._valIn.value

class conveyorInterface:
    'Class that provides a simple interface to all the inputs and outputs of the conveyor belt'
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
        self._redButton = Debouncer(self.MCPpins[7])
        self._greenButton = Debouncer(self.MCPpins[6])

        self.redButton = Inverter(self._redButton)
        self.greenButton = Inverter(self._greenButton)

        self.armButton = self.redButton
        self.disarmButton = self.greenButton
    
    def initInputs(self):
        'Sets up debouncers on the digital inputs'
        self._incomingBarrier = Debouncer(iomapping.IX2)
        self._outgoingBarrier = Debouncer(iomapping.IX5)
        self._rotaryEncoder = Debouncer(iomapping.IX4)

        self.incomingBarrier = Inverter(self._incomingBarrier)
        self.outgoingBarrier = Inverter(self._outgoingBarrier)
        self.rotaryEncoder = Inverter(self._rotaryEncoder)

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
        # runs update on all the debouncers
        self._incomingBarrier.update()
        self._outgoingBarrier.update()
        self._rotaryEncoder.update()
        self._greenButton.update()
        self._redButton.update()
