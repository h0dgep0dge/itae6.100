import board
import analogio
import digitalio
import time
import busio

pot = analogio.AnalogIn(board.GP26)
uart = busio.UART(board.GP0, board.GP1, baudrate=9600, timeout=0)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

for i in range(0,4):
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)

for i in range(0,8):
    led.value = True
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)

for i in range(0,16):
    led.value = True
    time.sleep(0.125)
    led.value = False
    time.sleep(0.125)

led.value = True

while True:
    a = pot.value
    uart.write(bytearray([a>>8,a&255]))
    time.sleep(1/50)
    
