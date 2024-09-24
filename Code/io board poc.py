# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
# SPDX-License-Identifier: MIT
"""CircuitPython Blink Example - the CircuitPython 'Hello, World!'"""
import time
import board
import digitalio
import busio
from adafruit_mcp230xx.mcp23008 import MCP23008
from analogio import AnalogIn
from RGBLED import *

i2c = busio.I2C(board.GP1, board.GP0)
mcp = MCP23008(i2c)

pins = []

for i in range(0,6):
    p = mcp.get_pin(i)
    p.direction = digitalio.Direction.OUTPUT
    p.value = False
    pins.append(p)

start = mcp.get_pin(7)
start.direction = digitalio.Direction.INPUT
start.pull = digitalio.Pull.UP

stop = mcp.get_pin(6)
stop.direction = digitalio.Direction.INPUT
stop.pull = digitalio.Pull.UP

colour = AnalogIn(board.A0)

statusLed = LED(pins[0],pins[2],pins[1])
colourLed = LED(pins[3],pins[5],pins[4])

def statusRed():
    statusLed.value = COLOURS.RED

def statusGreen():
    statusLed.value = COLOURS.GREEN

def colourRed():
    colourLed.value = COLOURS.RED

def colourWhite():
    colourLed.value = COLOURS.WHITE

def colourBlue():
    colourLed.value = COLOURS.BLUE

def colourOff():
    colourLed.value = COLOURS.OFF

running = False

statusGreen()

while True:
    if start.value == False and running == False:
        running = True
        statusRed()
    elif stop.value == False and running == True:
        running = False
        statusGreen()
    
    if running:
        a = colour.value
        if a < 16383:
            colourWhite()
        elif a < 32767:
            colourRed()
        elif a < 49151:
            colourBlue()
        else:
            colourOff()
    else:
        colourOff()
    
    
    
    
    
    
    
    
    
    
    
    
    
    