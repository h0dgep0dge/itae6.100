from conveyor import conveyorInterface
from colourSensor import colourSensor
from RGBLED import COLOURS

class conveyorController:
    runTime = 20 # The amount of time to keep running after the last sensor input

    def __init__(self):
        self.interface = conveyorInterface()

        # Set state to initial values
        self.armed = False
        self.running = False
        self.encoderLatched = False
        self.OBarrierLatched = False

        # Initialize sensor object
        self.sensor = colourSensor()

        # Set outputs to initial values
        self.interface.motor.value = False
        self.interface.pump.value = False
        self.interface.whitePusher.value = False
        self.interface.redPusher.value = False
        self.interface.bluePusher.value = False
        self.interface.statusLED = COLOURS.GREEN
        self.interface.colourLED = COLOURS.OFF

    def disarm(self):
        self.armed = False
        self.interface.motor.value = False
        self.interface.pump.value = False
        self.interface.whitePusher.value = False
        self.interface.redPusher.value = False
        self.interface.bluePusher.value = False
        self.interface.statusLED = COLOURS.GREEN
        self.interface.colourLED = COLOURS.OFF

    def arm(self):
        self.armed = True
        self.interface.status = COLOURS.RED

    def refreshRunUntil(self):
        self.runUntil = time.monotonic() + self.runTime # I assume time.monotonic returns a number of seconds? docs doesn't say

    def run(self):
        self.motor.value = True
        self.pump.value = True
    
    def stop(self):
        self.motor.value = False
        self.pump.value = False

    def feedSensor(self):
        c = self.sensor.feed(self.interface.colourSensor.value)
        if c:
            print("Recieved colour",c)

    def tick(self):
        print("Recieved encoder tick")

    def outgoing(self):
        print("Something at outgoing barrier")

    def update(self):
        self.interface.update()

        if self.interface.armButton:
            self.arm()

        if not self.armed:
            return

        self.feedSensor()

        if not self.running:
            if self.interface.incomingBarrier.value:
                self.refreshRunUntil()
                self.run()
            else:
                return
        
        if self.runUntil < time.monotonic():
            self.stop()
            return
        
        if self.interface.rotaryEncoder.value:
            if not self.encoderLatched:
                self.tick()
                self.encoderLatched = True
        else
            self.encoderLatched = False
        
        if self.interface.outgoingBarrier.value:
            if not self.OBarrierLatched:
                self.outgoing()
                self.OBarrierLatched = True
        else
            self.OBarrierLatched = False
        

        

        
        


        
