import adafruit_sdcard
import busio
import digitalio
import board
import storage
import analogio
import time
import os

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
cs = digitalio.DigitalInOut(board.GP20)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

apin = analogio.AnalogIn(board.GP26)

vcc = digitalio.DigitalInOut(board.GP22)
vcc.direction = digitalio.Direction.OUTPUT
vcc.value = True

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Use the filesystem as normal.
start = time.monotonic()

flushes = 0
samples = 0

i = 0
filename = None
while True:
    filename = "/sd/log"+str(i)+".csv"
    try:
        os.stat(filename)
    except:
        break
    i += 1

with open(filename, "w") as f:
    while True:
        t = time.monotonic()
        led.value = int(t*6)%2
        if t > start+(samples*1/50):
            f.write(str(apin.value)+","+str(t)+"\n")
            samples += 1
        if t > start+(flushes*5):
            f.flush()
            flushes += 1
        #if t-start > 60:
            #break
#print(samples,"samples and",flushes,"flushes in",time.monotonic()-start,"seconds")
'''
1000 lines with individual opens
34.3 samples per second

1000 lines with 100 opens
294.6 samples per second

1000 lines with a single open
1530.6 samples per second

1000 lines with a single open + flush per line
46 samples per second
'''