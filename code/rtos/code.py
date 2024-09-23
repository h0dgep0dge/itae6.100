from conveyor import conveyorInterface
import pyRTOS
import edgeDetect
import iomapping


import digitalio
import board

INPUTS = 256
RISING = 0
FALLING = 1
CHANGING = 2

interface = conveyorInterface()

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
redPusher.deliver({"pin":interface.redPusher,"dwell":0.5})
pyRTOS.add_task(redPusher)

redPusher = pyRTOS.Task(pusher,name="whitePusher",mailbox=True,priority=8)
redPusher.deliver({"pin":interface.whitePusher,"dwell":0.5})
pyRTOS.add_task(redPusher)

redPusher = pyRTOS.Task(pusher,name="bluePusher",mailbox=True,priority=8)
redPusher.deliver({"pin":interface.bluePusher,"dwell":0.5})
pyRTOS.add_task(redPusher)

def tick(self):
    count = 0
    yield
    while True:
        yield [pyRTOS.wait_for_message(self)]
        m = self.recv()
        count += 1
        if count % 10 == 0:
            self.send(pyRTOS.Message(200,self,"redPusher"))

pyRTOS.add_task(pyRTOS.Task(tick,name="tick",priority=8))

def outgoing(self):
    count = 0
    yield
    while True:
        yield [pyRTOS.wait_for_message(self)]
        m = self.recv()
        count += 1
        if count % 10 == 0:
            self.send(pyRTOS.Message(200,self,"bluePusher"))

pyRTOS.add_task(pyRTOS.Task(tick,name="outgoing",priority=8))

def incoming(self):
    count = 0
    yield
    while True:
        yield [pyRTOS.wait_for_message(self)]
        m = self.recv()
        count += 1
        if count % 10 == 0:
            self.send(pyRTOS.Message(200,self,"whitePusher"))

pyRTOS.add_task(pyRTOS.Task(tick,name="incoming",priority=8))

def interfaceUpdate(self):
    detectors = [("tick",     edgeDetect.risingEdgeDetect(interface.rotaryEncoder)),
                 ("incoming", edgeDetect.risingEdgeDetect(interface.incomingBarrier)),
                 ("outgoing", edgeDetect.risingEdgeDetect(interface.outgoingBarrier))]
    arm = edgeDetect.risingEdgeDetect(interface.armButton)
    disarm = edgeDetect.risingEdgeDetect(interface.disarmButton)
    yield
    while True:
        interface.update()
        for detector in map(lambda d : (d[0],next(d[1])),detectors):
            if detector[1]:
                self.send(pyRTOS.Message(200,self,detector[0]))
        if next(disarm):
            self.send(pyRTOS.Message(200,self,"control"))
        elif next(arm):
            self.send(pyRTOS.Message(201,self,"control"))
        yield

pyRTOS.add_task(pyRTOS.Task(interfaceUpdate))

pyRTOS.start()