class Filter:
    def __init__(self,span):
        self.vals = []
        self.index = 0
        for i in range(0,span):
            self.vals.append(0)
    
    def feed(self,val):
        self.vals[self.index] = val
        self.index = (self.index+1)%len(self.vals)
    
    def avg(self):
        s = 0
        for v in self.vals:
            s = s+v
        return s/len(self.vals)
