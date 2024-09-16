from conveyor import conveyorInterface
from colourSensor import colourSensor
from RGBLED import COLOURS
import time

class pushMe:
    def __init__(self,colour):
        self.ticks = 0
        self.pushed = False
        self.colour = colour
    
    def __str__(self):
        return "pushme object " + str(self.ticks) + " " + str(self.pushed) + " " + str(self.colour)
    
    def __repr__(self):
        return self.__str__()

class conveyorController:
    'The almighty conveyor controller object. Make an isntance and call update() frequently, let the class do the rest'
    runTime = 60 # The amount of time to keep running after the last sensor input

    # ticks are how long to wait between the outgoing barrier and the respective pusher
    # dwell is how long to leave the pusher activated
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
        'Set the armed flag to off, and set all outputs to safe values'
        self.armed = False
        self.interface.motor.value = False
        self.interface.pump.value = False
        self.interface.whitePusher.value = False
        self.interface.redPusher.value = False
        self.interface.bluePusher.value = False
        self.interface.statusLED = COLOURS.GREEN
        self.interface.colourLED = COLOURS.OFF
        self.runUntil = 0
        print("disarming")

    def arm(self):
        'Set the arm flag, and switch the status led to red for armed'
        self.armed = True
        self.interface.statusLED = COLOURS.RED
        print("arming")

    def refreshRunUntil(self):
        'Updates the runUntil to let the machine run another runTime seconds'
        self.runUntil = time.monotonic() + self.runTime # I assume time.monotonic returns a number of seconds? docs don't say

    def start(self):
        'Set the running flag and start the motor and pump'
        self.running = True
        self.interface.motor.value = True
        self.interface.pump.value = True
    
    def stop(self):
        'Set the running flag and drop running the motor and pump'
        self.running = False
        self.interface.motor.value = False
        self.interface.pump.value = False

    def feedSensor(self):
        'Grab the analog reading from the colour sensor, sticks it up the sensor object, then adds anything returned to the colour queue'
        c = self.sensor.feed(self.interface.colourSensor.value/65535*9)
        if c: # If c has a value other than None, something has just passed under the sensor
            print("Recieved colour",c)
            self.colourQueue.append(c) # record the colour of the passing object
            self.interface.colourLED = c

    def tick(self):
        'Called every time the encoder ticks over, takes care of timing the pushers'
        print("Recieved encoder tick",self.colourQueue,self.pushQueue)
        i = 0
        while i < len(self.pushQueue):
            push = self.pushQueue[i]
            push.ticks += 1
            if push.colour == COLOURS.WHITE:
                if push.ticks > self.whitePushTicks+self.pusherDwell:
                    self.interface.whitePusher.value = False
                    self.pushQueue[i].pushed = True
                elif push.ticks >= self.whitePushTicks:
                    self.interface.whitePusher.value = True
            elif push.colour == COLOURS.RED:
                if push.ticks > self.redPushTicks+self.pusherDwell:
                    self.interface.redPusher.value = False
                    self.pushQueue[i].pushed = True
                elif push.ticks >= self.redPushTicks:
                    self.interface.redPusher.value = True
            elif push.colour == COLOURS.BLUE:
                if push.ticks > self.bluePushTicks+self.pusherDwell:
                    self.interface.bluePusher.value = False
                    self.pushQueue[i].pushed = True
                elif push.ticks >= self.bluePushTicks:
                    self.interface.bluePusher.value = True
            if self.pushQueue[i].pushed:
                del self.pushQueue[i]
            else:
                i += 1
        if len(self.colourQueue) > 0:
            self.interface.colourLED = self.colourQueue[0]
        else:
            self.interface.colourLED = COLOURS.OFF

    def outgoing(self):
        'Called when the outgoing barrier breaks, grabs the oldest colour from the colour queue and puts it into the pushing queue'
        self.refreshRunUntil()
        if len(self.colourQueue) > 0:
            print(self.colourQueue[0],"at outgoing barrier")
            self.pushQueue.append(pushMe(self.colourQueue.pop(0)))
        else:
            print("Something at outgoing barrier, don't know what colour! fuck!")

    def update(self):
        'Called frequently, to check all the inputs, control the outputs, and update the state of the controller'
        self.interface.update() # calls the "call frequently" function of the interface class

        if not self.armed:
            if self.interface.armButton: # if the machine isn't armed, but the arm button is pressed
                self.arm()
            else:
                return # if the machine isn't armed and shouldn't be armed, do nothing further and return back

        if self.interface.disarmButton: # the machine is armed, but the disarm button is pressed, disarm and do nothing else
            self.disarm()
            return

        self.feedSensor()

        if not self.running: # the machine is armed, but nothing is running until an object is placed on the machine
            if self.interface.incomingBarrier.value: # an object has been placed on the machine
                self.refreshRunUntil() # give the machine runTime seconds to run
                self.start()           # and start it running
            else:
                return # the machine isn't running and there's nothing placed on the belt, don't need to do anything
        elif self.interface.incomingBarrier.value: # the machine is already running, but something just got placed on the belt
            self.refreshRunUntil() # so keep it running

        
        if self.runUntil < time.monotonic(): # the runUntil time has passed, so the machine should stop
            self.stop()
            return
        
        if self.interface.rotaryEncoder.value: # the encoder is pressed
            if not self.encoderLatched: # if encoderLatched isn't true, the encoder has only just ticked
                self.tick() # run the tick() logic
                self.encoderLatched = True # set the latched variable so tick() is only called once per tick
        else: # unlatch the encoder when the encoder isn't pressed
            self.encoderLatched = False
        
        if self.interface.outgoingBarrier.value: # something has tripped the outgoing barrier
            self.refreshRunUntil() # since there's something moving on the conveyor, keep the runUntil topped up
            if not self.OBarrierLatched: # this is the rising edge of the barrier signal
                self.outgoing() # run the logic for an object waiting at the outgoing barrier
                self.OBarrierLatched = True # latch so the logic function only runs once per pulse
        else: # reset the latch when the barrier clears again
            self.OBarrierLatched = False
