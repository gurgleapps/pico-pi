import board
import digitalio
import time

ledPin = board.GP14
delay = 0.5
led = digitalio.DigitalInOut(ledPin)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(delay)
    led.value = False
    time.sleep(delay)