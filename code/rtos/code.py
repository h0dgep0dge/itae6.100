from conveyor import conveyorInterface
import pyRTOS
import edgeDetect
import iomapping


import digitalio
import board

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

redPusher = pyRTOS.Task(pusher,name="redPusher",mailbox=True)
redPusher.deliver({"pin":interface.redPusher,"dwell":0.1})
pyRTOS.add_task(redPusher)

def tick(self):
    blocker = edgeDetect.risingEdgeDetect(interface.rotary_encoder)
    yield

pyRTOS.add_task(pyRTOS.Task(tick))

def interfaceUpdate(self):
    # initiate
    yield
    while True:
        interface.update()
        yield

pyRTOS.add_task(pyRTOS.Task(runner))

pyRTOS.start()