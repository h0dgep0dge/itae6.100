'''
Some generators to use as blockers with pyRTOS
For detecting rising (false-true) and falling (true-false) edges on board pins
but it should work with other things with a value property that return a bool
'''
import digitalio
from adafruit_debouncer import Debouncer

def risingEdgeDetect(pin):
    latched = pin.value
    while True:
        if pin.value and not latched:
            latched = True
            yield True
        elif pin.value and latched:
            yield False
        else:
            latched = False
            yield False

def fallingEdgeDetect(pin):
    latched = not pin.value
    while True:
        if not pin.value and not latched:
            latched = True
            yield True
        elif not pin.value and latched:
            yield False
        else:
            latched = False
            yield False


def DBrisingEdgeDetect(pin):
    debounced = Debouncer(pin)
    detector = risingEdgeDetect(debounced)
    while True:
        debounced.update()
        yield detector.__next__()

def DBfallingEdgeDetect(pin):
    debounced = Debouncer(pin)
    detector = fallingEdgeDetect(debounced)
    while True:
        debounced.update()
        yield detector.__next__()

def changingEdgeDetect(pin):
    rising = risingEdgeDetect(pin)
    falling = fallingEdgeDetect(pin)
    while True:
        yield rising.__next__() or falling.__next__()

def DBchangingEdgeDetect(pin):
    debounced = Debouncer(pin)
    detector = changingEdgeDetect(debounced)
    while True:
        debounced.update()
        yield detector.__next__()









