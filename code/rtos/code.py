from conveyor import conveyorInterface
from colourSensor import colourSensor
import pyRTOS
import edgeDetect
import iomapping
from RGBLED import COLOURS

#import digitalio
#import board
import time

ENCODER_TICK = 500
INCOMING_BARRIER = 501
OUTGOING_BARRIER = 502
ARM = 503
DISARM = 504
NEW_COLOUR = 505
OUTGOING_COLOUR = 506
PUSH = 507

interface = conveyorInterface()

class pushMe:
    def __init__(self,colour):
        self.ticks = 0
        self.colour = colour
    
    def incr(self):
        self.ticks += 1
    
    def __str__(self):
        return "pushme object " + str(self.ticks) + " " + str(self.colour)
    
    def __repr__(self):
        return self.__str__()

def pusher(self):
    args = self.recv()[0]
    pin = args["pin"]
    dwell = args["dwell"]
    pushed = False
    yield
    while True:
        if pushed:
            yield [pyRTOS.wait_for_message(self),pyRTOS.timeout(dwell)]
        else:
            yield [pyRTOS.wait_for_message(self)]
        m = self.recv()
        if len(m) > 0:
            pushed = True
            pin.value = True
        else:
            pushed = False
            pin.value = False

redPusher = pyRTOS.Task(pusher,name="redPusher",mailbox=True,priority=8)
redPusher.deliver({"pin":interface.redPusher,"dwell":0.2})
pyRTOS.add_task(redPusher)

whitePusher = pyRTOS.Task(pusher,name="whitePusher",mailbox=True,priority=8)
whitePusher.deliver({"pin":interface.whitePusher,"dwell":0.2})
pyRTOS.add_task(whitePusher)

bluePusher = pyRTOS.Task(pusher,name="bluePusher",mailbox=True,priority=8)
bluePusher.deliver({"pin":interface.bluePusher,"dwell":0.2})
pyRTOS.add_task(bluePusher)

def pushManager(self):
    whitePushTicks = 3
    redPushTicks = 8
    bluePushTicks = 13
    pushQueue = []
    yield
    while True:
        yield [pyRTOS.wait_for_message(self)]
        messages = self.recv()
        for m in messages:
            if m.type == OUTGOING_COLOUR:
                pushQueue.append(pushMe(m.message))
            elif m.type == ENCODER_TICK:
                deleteList = []
                for i, push in enumerate(pushQueue):
                    push.incr()
                    if push.colour == COLOURS.RED and push.ticks >= redPushTicks:
                        self.send(pyRTOS.Message(PUSH,self,"redPusher"))
                        deleteList.append(i)
                    elif push.colour == COLOURS.WHITE and push.ticks >= whitePushTicks:
                        self.send(pyRTOS.Message(PUSH,self,"whitePusher"))
                        deleteList.append(i)
                    elif push.colour == COLOURS.BLUE and push.ticks >= bluePushTicks:
                        self.send(pyRTOS.Message(PUSH,self,"bluePusher"))
                        deleteList.append(i)
                    deleteList.sort(reverse=True)
                    for i in deleteList: del pushQueue[i]
                    
            print(pushQueue)

pyRTOS.add_task(pyRTOS.Task(pushManager,name="pushManager",mailbox=True,priority=8))

def startRunStop(self):
    armed = False
    running = False
    runTime = 60
    runUntil = 0
    
    interface.statusLED = COLOURS.GREEN
    interface.motor.value = False
    interface.pump.value = False
    yield
    while True:
        if running:
            yield [pyRTOS.wait_for_message(self),pyRTOS.timeout(runUntil-time.monotonic())]
        else: yield [pyRTOS.wait_for_message(self)]
        messages = self.recv()
        if len(messages) == 0:
            running = False
        
        for m in messages:
            print(m.type)
            if m.type == ARM: armed = False
            elif m.type == DISARM: armed = True
            elif m.type == INCOMING_BARRIER and armed:
                runUntil = time.monotonic()+runTime
                running = True
        
        if armed:
            interface.statusLED = COLOURS.RED
        else:
            interface.statusLED = COLOURS.GREEN
            running = False
        
        if running:
            interface.motor.value = True
            interface.pump.value = True
        else:
            interface.motor.value = False
            interface.pump.value = False
        
            

SRSTask = pyRTOS.Task(startRunStop,name="startRunStop",mailbox=True,priority=8)
pyRTOS.add_task(SRSTask)

def colourManager(self):
    colourQueue = []
    yield
    while True:
        yield [pyRTOS.wait_for_message(self)]
        messages = self.recv()
        for m in messages:
            if m.type == NEW_COLOUR:
                colourQueue.append(m.message)
                print("new colour",colourQueue)
            elif m.type == OUTGOING_BARRIER:
                if len(colourQueue) > 0:
                    print(colourQueue[0],"at outgoing barrier")
                    self.send(pyRTOS.Message(OUTGOING_COLOUR,self,"pushManager",colourQueue[0]))
                    del colourQueue[0]
                else:
                    print("something at the outgoing barrier but don't know the colour! fuck!")
        if len(colourQueue) > 0: interface.colourLED = colourQueue[-1]
        else: interface.colourLED = COLOURS.OFF

pyRTOS.add_task(pyRTOS.Task(colourManager,name="colourManager",mailbox=True,priority=8))

def interfaceUpdate(self):
    detectors = [("pushManager",   edgeDetect.risingEdgeDetect(interface.rotaryEncoder),   ENCODER_TICK),
                 ("startRunStop",  edgeDetect.risingEdgeDetect(interface.incomingBarrier), INCOMING_BARRIER),
                 ("colourManager", edgeDetect.risingEdgeDetect(interface.outgoingBarrier), OUTGOING_BARRIER)]
    arm = edgeDetect.risingEdgeDetect(interface.armButton)
    disarm = edgeDetect.risingEdgeDetect(interface.disarmButton)
    sensor = colourSensor()
    yield
    while True:
        interface.update()
        if next(disarm):
            self.send(pyRTOS.Message(ARM,self,"startRunStop"))
        elif next(arm):
            self.send(pyRTOS.Message(DISARM,self,"startRunStop"))
        
        for detector in map(lambda d : (d[0],next(d[1]),d[2]),detectors):
            if detector[1]:
                self.send(pyRTOS.Message(detector[2],self,detector[0]))
                
        c = sensor.feed(interface.colourSensor.value/65535*9)
        if c:
            self.send(pyRTOS.Message(NEW_COLOUR,self,"colourManager",c))
        yield

pyRTOS.add_task(pyRTOS.Task(interfaceUpdate))

pyRTOS.start()