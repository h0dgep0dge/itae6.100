import time
import board
from analogio import AnalogIn
from colourSensor import colourSensor
from conveyor import conveyor

def downUp(sensor,start,low,end):
    for i in range(start*10,low*10,-1):
        v = sensor.feed(i/10)
        if v != None:
            print(v)
            c.colourLED = v
        time.sleep(0.1)
    for i in range(low*10,end*10,1):
        v = sensor.feed(i/10)
        if v != None:
            print(v)
            c.colourLED = v
        time.sleep(0.1)

c = conveyor()
sense = colourSensor()
#analog_in = AnalogIn(board.A0)

while True:
    a = c.colour.value/65535*10;
    v = sense.feed(a)
    #print(sense)
    if v:
        c.colourLED = v
    if c.stop.value == False:
        c.colourLED = 0