import machine
import time

ledPin = 14
delay = 0.5
led = machine.Pin(ledPin, machine.Pin.OUT)

while True:
    led.value(1)
    time.sleep(delay)
    led.value(0)
    time.sleep(delay)