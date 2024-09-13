class COLOURS:
    OFF     = 0b000
    
    RED     = 0b100
    GREEN   = 0b010
    BLUE    = 0b001
    
    YELLOW  = 0b110
    CYAN    = 0b011
    MAGENTA = 0b101

    WHITE   = 0b111


class colourSensor:
    WAITING = 0
    BLUE = 1
    RED = 2
    WHITE = 3
    RESETTING = 4
    
    BLUETHRESH  = 6.9
    REDTHRESH   = 6
    WHITETHRESH = 4
    RESETTHRESH = 7
    MARGIN      = 0.2
    
    def __init__(self):
        self.state = self.WAITING
    
    def feed(self,value):
        #print("feeding",value)
        if self.state == self.WAITING:
            return self.feedWaiting(value)
        if self.state == self.BLUE:
            return self.feedBlue(value)
        if self.state == self.RED:
            return self.feedRed(value)
        if self.state == self.WHITE:
            return self.feedWhite(value)
        if self.state == self.RESETTING:
            return self.feedResetting(value)
        return None
    
    def feedWaiting(self,value):
        if value <= self.BLUETHRESH:
            self.state = self.BLUE
            return self.feedBlue(value)
        return None
    
    def feedBlue(self,value):
        if value <= self.REDTHRESH:
            self.state = self.RED
            return self.feedRed(value)
        if value >= self.BLUETHRESH+self.MARGIN:
            self.state = self.RESETTING
            return COLOURS.BLUE
        return None
    
    def feedRed(self,value):
        if value <= self.WHITETHRESH:
            self.state = self.WHITE
            return self.feedWhite(value)
        if value >= self.REDTHRESH+self.MARGIN:
            self.state = self.RESETTING
            return COLOURS.RED
        return None
    
    def feedWhite(self,value):
        if value >= self.WHITETHRESH+self.MARGIN:
            self.state = self.RESETTING
            return COLOURS.WHITE
        return None
    
    def feedResetting(self,value):
        if value >= self.BLUETHRESH + self.MARGIN:
            self.state = self.WAITING
            return self.feedWaiting(value)
        return None
    
    def __str__(self):
        if self.state == self.WAITING:
            return "colourSensor WAITING"
        if self.state == self.BLUE:
            return "colourSensor BLUE"
        if self.state == self.RED:
            return "colourSensor RED"
        if self.state == self.WHITE:
            return "colourSensor WHITE"
        if self.state == self.RESETTING:
            return "colourSensor RESETTING"
        return "colourSensor BROKEN"

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