import adafruit_sdcard
import busio
import digitalio
import board
import storage
import analogio
import time

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.GP18, board.GP19, board.GP16)
cs = digitalio.DigitalInOut(board.GP20)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

apin = analogio.AnalogIn(board.GP26)

# Use the filesystem as normal.
start = time.monotonic()
with open("/sd/test.txt", "a") as f:
    for b in range(0,1000):
        f.write(str(apin.value)+"\n")
print(1/(time.monotonic()-start) * 1000)
'''
1000 lines with individual opens
34.3 samples per second

1000 lines with 100 opens
294.6 samples per second

1000 lines with a single open
1530.6 samples per second
'''