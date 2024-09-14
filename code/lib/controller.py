from conveyor import conveyorInterface
from colourSensor import colourSensor
from RGBLED import COLOURS

class pushMe:
    def __init__(self,colour):
        self.ticks = 0
        self.colour = colour

class conveyorController:
    runTime = 20 # The amount of time to keep running after the last sensor input

    whitePushTicks = 10
    redPushTicks = 20
    bluePushTicks = 30
    pusherDwell = 3

    def __init__(self):
        self.interface = conveyorInterface()

        # Set state to initial values
        self.armed = False
        self.running = False
        self.encoderLatched = False
        self.OBarrierLatched = False
        self.colourQueue = []
        self.pushQueue = []

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
        self.runUntil = time.monotonic() + self.runTime # I assume time.monotonic returns a number of seconds? docs don't say

    def start(self):
        self.running = True
        self.motor.value = True
        self.pump.value = True
    
    def stop(self):
        self.running = False
        self.motor.value = False
        self.pump.value = False

    def feedSensor(self):
        c = self.sensor.feed(self.interface.colourSensor.value)
        if c:
            print("Recieved colour",c)
            self.colourQueue.append(c)

    def tick(self):
        print("Recieved encoder tick")
        for i in range(0,len(self.pushQueue)):
            push = self.pushQueue[i]
            push.ticks += 1
            if push.colour == COLOURS.WHITE:
                if push.ticks > self.whitePushTicks+self.pusherDwell:
                    self.interface.whitePusher = False
                    self.pushQueue.pop(i)
                elif push.ticks >= self.whitePushTicks:
                    self.interface.whitePusher = True
            elif push.colour == COLOURS.RED:
                if push.ticks > self.redPushTicks+self.pusherDwell:
                    self.interface.redPusher = False
                    self.pushQueue.pop(i)
                elif push.ticks >= self.redPushTicks:
                    self.interface.redPusher = True
            elif push.colour == COLOURS.BLUE:
                if push.ticks > self.bluePushTicks+self.pusherDwell:
                    self.interface.bluePusher = False
                    self.pushQueue.pop(i)
                elif push.ticks >= self.bluePushTicks:
                    self.interface.bluePusher = True

    def outgoing(self):
        self.refreshRunUntil()
        if len(self.colourQueue) > 0:
            print(self.colourQueue[0],"at outgoing barrier")
            self.pushQueue.append(pushMe(colourQueue.pop(0)))
        else
            print("Something at outgoing barrier, don't know what colour! fuck!")

    def update(self):
        self.interface.update()

        if not self.armed:
            if self.interface.armButton:
                self.arm()
            else
                return

        if self.interface.disarmButton:
            self.disarm()
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
