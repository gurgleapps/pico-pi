import machine
import time
import rgbled

print("GurgleApps.com RGB Driver Test")
delay = 0.03
delay2 = 1.5
fadeDelay = 0.004
onboardLED = rgbled.RGBLED(18, 19, 20)
#breadboardLED1 = rgbled.RGBLED(0, 1, 2)
#breadboardLED2 = rgbled.RGBLED(3, 4, 5, False)

#leds = [onboardLED, breadboardLED1, breadboardLED2]
leds = [onboardLED]

def primaryColours(delay):
    for led in leds:
        led.setColor(0xFF0000)
    time.sleep(delay)
    for led in leds:
        led.setColor(0x00FF00)
    time.sleep(delay)
    for led in leds:
        led.setColor(0xFF)
    time.sleep(delay)


def rainbowCycle(delay):
    for pos in range(255):
        rgb = rgbled.RGBLED.spectrum(pos)
        for led in leds:
            led.setColor(rgb, True)
            # breadboardLED.rainbow(rgb)
        time.sleep(delay)


def fadeIn(rgb, delay):
    step = 1 / 255
    for val in range(255):
        for led in leds:
            led.setColor(rgb, True, step * val)
        time.sleep(delay)


def fadeOut(rgb, delay):
    step = 1 / 255
    for val in range(255, 0, -1):
        for led in leds:
            led.setColor(rgb, True, step * val)
        time.sleep(delay)


while True:
    primaryColours(delay2)
    fadeIn(0xFF0000, fadeDelay)
    fadeOut(0xFF0000, fadeDelay)
    fadeIn(0xFF00, fadeDelay)
    fadeOut(0xFF00, fadeDelay)
    fadeIn(0xFF, fadeDelay)
    fadeOut(0xFF, fadeDelay)
    for _ in range(3):
        rainbowCycle(delay)
