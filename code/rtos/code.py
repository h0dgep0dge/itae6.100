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
    blocker = edgeDetect.risingEdgeDetect(interface.rotaryEncoder)
    count = 0
    yield
    while True:
        yield [blocker]
        count += 1
        if count % 10 == 0:
            self.send(pyRTOS.Message(200,self,"redPusher"))

pyRTOS.add_task(pyRTOS.Task(tick,priority=8))

def interfaceUpdate(self):
    detectors = ["",edgeDetect.risingEdgeDetect(interface.rotaryEncoder)
    edgeDetect.risingEdgeDetect(interface.incomingBarrier)
    edgeDetect.risingEdgeDetect(interface.outgoingBarrier)
    edgeDetect.risingEdgeDetect(interface.armButton)
    edgeDetect.risingEdgeDetect(interface.disarmButton)]
    yield
    while True:
        interface.update()

        yield

pyRTOS.add_task(pyRTOS.Task(interfaceUpdate))

pyRTOS.start()