class COLOURS:
    OFF     = 0b000
    
    RED     = 0b100
    GREEN   = 0b010
    BLUE    = 0b001
    
    YELLOW  = 0b110
    CYAN    = 0b011
    MAGENTA = 0b101

    WHITE   = 0b111

class LED:
    def __init__(self,red,green,blue):
        self.red = red
        self.green = green
        self.blue = blue
    
    @property
    def value(self):
        return (self.red.value<<2)&(self.green<<1)&(self.blue)
    
    @value.setter
    def value(self,colour):
        self.red.value = colour & COLOURS.RED
        self.green.value = colour & COLOURS.GREEN
        self.blue.value = colour & COLOURS.BLUE
