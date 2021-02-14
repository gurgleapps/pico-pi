import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
keyboard = Keyboard(usb_hid.devices)

start_btn_pin = board.GP16
stop_btn_pin = board.GP17

start_btn = digitalio.DigitalInOut(start_btn_pin)
start_btn.direction = digitalio.Direction.INPUT
start_btn.pull = digitalio.Pull.DOWN

stop_btn = digitalio.DigitalInOut(stop_btn_pin)
stop_btn.direction = digitalio.Direction.INPUT
stop_btn.pull = digitalio.Pull.DOWN

letters = {
    "a":0x04, "b":0x5, "c":0x6, "d":0x7, "e":0x8, "f":0x9,
    "g":0x0A, "h":0xB, "i":0xC, "j":0xD, "k":0xE, "l":0xF,
    "m":0x10, "n":0x11, "o":0x12, "p":0x13, "q":0x14, "r":0x15,
    "s":0x16, "t":0x17, "u":0x18, "v":0x19, "w":0x1A, "x":0x1B, "y":0x1C, "z":0x1D,
    " ":0x2C
    }

running = False
# after pressing button to hack starting to type
longDelay = 60 * 1.5
# delay before we type again
repeatDelay = 5
# message to repeatedly type
message = "you have been hacked "

def typeString(text,letterDelay=0):
    global running
    for letter in text:
        keyboard.press(letters[letter])
        keyboard.release(letters[letter])
        time.sleep(letterDelay)
        if stop_btn.value:
            print("stop pressed")
            running = False
            break

while True:
    if running:
        typeString(message,0.1)
        time.sleep(repeatDelay)
    else:
        time.sleep(0.1)
        if start_btn.value:
            print("PRESS Start waiting:"+str(longDelay))
            running = True
            time.sleep(longDelay)

