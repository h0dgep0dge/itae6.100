from controller import conveyorController
import pyRTOS

def task(self):
    controller = conveyorController()
    yield
    while True:
        controller.update()
        yield


pyRTOS.add_task(pyRTOS.Task(task))
pyRTOS.start()