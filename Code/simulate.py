from RGBLED import COLOURS
from colourSensor import colourSensor

sensor = colourSensor()
with open("log.csv") as file:
    for line in file:
        point = int(line.rstrip())/65535*10
        r = sensor.feed(point)
        #print(sensor,point,r)
        match r:
            case COLOURS.RED:
                print("Red")
            case COLOURS.BLUE:
                print("Blue")
            case COLOURS.WHITE:
                print("White")