# GurgleApps.com
#
"""
Code to auto type a message as hid device
Originally a prank https://www.youtube.com/watch?v=kkxXQGj2VRw
Code is organised to explain how it works to beginner coders
hence the simple and extra versions. It's not coded to be optimal.
"""
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

letters_simple = {
    "a":0x04, "b":0x5, "c":0x6, "d":0x7, "e":0x8, "f":0x9,
    "g":0x0A, "h":0xB, "i":0xC, "j":0xD, "k":0xE, "l":0xF,
    "m":0x10, "n":0x11, "o":0x12, "p":0x13, "q":0x14, "r":0x15,
    "s":0x16, "t":0x17, "u":0x18, "v":0x19, "w":0x1A, "x":0x1B, "y":0x1C, "z":0x1D,
    " ":0x2C, "0":0x27, "1":0x1E, "2":0x1F, "3":0x20, "4":0x21, "5":0x22, "6":0x23,
    "7":0x24, "8":0x25, "9":0x26
    }

letters_extra = {
    "!":[0xE1,0x1E],
    "A":[0xE1,0x04], "B":[0xE1,0x5], "C":[0xE1,0x6], "D":[0xE1,0x7], "E":[0xE1,0x8], "F":[0xE1,0x9],
    "G":[0xE1,0x0A], "H":[0xE1,0xB], "I":[0xE1,0xC], "J":[0xE1,0xD], "K":[0xE1,0xE], "L":[0xE1,0xF],
    "M":[0xE1,0x10], "N":[0xE1,0x11], "O":[0xE1,0x12], "P":[0xE1,0x13], "Q":[0xE1,0x14], "R":[0xE1,0x15],
    "S":[0xE1,0x16], "T":[0xE1,0x17], "U":[0xE1,0x18], "V":[0xE1,0x19], "W":[0xE1,0x1A], "X":[0xE1,0x1B], "Y":[0xE1,0x1C], "Z":[0xE1,0x1D],
    }

running = False
# after pressing button to hack starting to type
long_delay = 60 * 1.5
long_delay = 8 # short delay for testing
# delay before we type again
repeat_delay = 5
# message to repeatedly type only needs 1 hex value
message_simple = "you have been hacked "
# more complex multi key chars
message_extra = "You have been Hacked!! 0123456789"


"""
This will type a message with just letters in letters_simple
Just here for learning as it's simpler to follow
"""
def typeStringSimple(text,letterDelay=0):
    global running
    for letter in text:
        if letter in letters_simple:
            keyboard.press(letters_simple[letter])
            keyboard.release(letters_simple[letter])
        time.sleep(letterDelay)
        if stop_btn.value:
            print("stop pressed")
            running = False
            break


def typeString(text,letterDelay=0):
    global running
    for letter in text:
        if letter in letters_simple:
            keyboard.press(letters_simple[letter])
            keyboard.release(letters_simple[letter])
        else:
            if letter in letters_extra:
                for extra_letter in letters_extra[letter]:
                    keyboard.press(extra_letter)
                for extra_letter in letters_extra[letter]:  
                    keyboard.release(extra_letter)
        time.sleep(letterDelay)
        if stop_btn.value:
            print("stop pressed")
            running = False
            break

while True:
    if running:
        typeString(message_extra,0.1)
        time.sleep(repeat_delay)
    else:
        time.sleep(0.1)
        if start_btn.value:
            print("PRESS Start waiting:"+str(long_delay))
            running = True
            time.sleep(long_delay)

