import ssd1306
import utime
import framebuf
import base64
import _thread

print("HC-SR04")
# would have used pin 1 & 2 but they were broken on one of our Pico Boards
triggerPin = 21
echoPin = 18
buttonPin = 15
button2Pin = 14
clockPin = 5
dataPin = 4
bus = 0
i2c = machine.I2C(bus,sda=machine.Pin(dataPin),scl=machine.Pin(clockPin))
print(i2c.scan())
display = ssd1306.SSD1306_I2C(128,64,i2c)
logoSmallB = b'aBn/gP//wH//4D//8B/w/AAf/gAP/wAH/4AD8MAAAeAAAPAAAHgAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAA4AAAAAAAOAAAAAACAOAAAAAAADgAAAAAAgCxAAAAAAHQAB4AMeIAscAAGMAB2AAeBPHiAJHsACmqAbwAGySBIhixLxwhr8H4ABEkgSIt8S+UIS3h+AARJIEiLfktsGE5IVIAFCSBoj2ZrbgoqSGYABckgeIhGe2MOOkgngATPIAiKQFthYBpIZgAEzwBIjgBD70ACSCYAB4AAaAQAQ0YAAEgmAAOAADgAAEMAAAAJpgAAAAAQAAADAAAAACADAAAHgAADwQAB4AAAw+AAP/AAH/gAD/wAB8P+A///Af//gP//wH/D////////////////w'
logoLargeB = b'gB//8A////AP///wD///8A///4AB//+AAf//gAH//4AB//wAAD/8AAA//AAAP/wAAD/gAAAH4AAAB+AAAAfgAAAHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHAAAAAAAAAAMAAAAAAAAAB4AAAAAAAAAHgAAAAAABgAeAAAAAAAAADwAAAAAAAYAFhgAAAAAAAHcAA4AAwZGADYYAAAHHAABwAAfAB8PxgA2HyAADz7AA94AH4CfjMYAMxswABs68AG8ABmMmQzGDiMZvBwYMvsA/QAZjJgMxh4/Gb4+GDP/g/wAMIyYDMYTPxmzNBgzz4B8ADCMmAzGN3sZszAZM8yDxQAwDJgExj5jmbM8GxPMgdwAM4yYB8YwYZ+zHh8fzMHdADPN2AfGMmAfswbMDszB3QARz9gAxjZgGzsmwADMwZ0AGY6ADMYeABg/PIAATMWdAB+AAATCGAAYNzgAAAzBnQAPgAAHwAAAGDAAAAAAxZ0ABwAAA8AAAAAwAAAAAA2cAAAAAAAAAAAAMAAAAAABgDgAAAH4AAAB+BAAAfgAAAH/AAAP/wAAD/8AAA//AAAP//AA///wAP//8AD///AA///+B////gf///4H///+B//'
#
global button_pressed, mode
button_pressed = False
mode = 0
button = machine.Pin(buttonPin, machine.Pin.IN, machine.Pin.PULL_DOWN)
button2 = machine.Pin(button2Pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
#
trigger = machine.Pin(triggerPin, machine.Pin.OUT)
trigger.value(0)
echo = machine.Pin(echoPin, machine.Pin.IN, None)
# for y, row in enumerate(logoLarge):
#     for x, c in enumerate(row):
#         display.pixel(x, y, c)

def button_reader_thread():
    global button_pressed
    while True:
        if (button.value() == 1) != button_pressed:
            print(button.value())
            button_pressed = button.value() == 1
            if button_pressed: press()    

def press():
    print('PRESS')
    echoTime()
    
def echoTime():
    trigger.value(0)
    #sleep 5 microseconds (us microseconds is  a millionth of a second 10-6 seconds)
    utime.sleep_us(5)
    #send a 10us  pulse through trigger
    trigger.value(1)
    utime.sleep_us(10)
    trigger.value(0)
    try:
        echoTime = machine.time_pulse_us(echo, 1, 1000000)
        mm = timeToMM(echoTime)
        updateInfo(echoTime, mm)
        print(str(echoTime)+"us")
        print(str(mm)+"mm")
    except OSError as e:
        print(e)
        
# Calculate distance in milimeters from time in microseconds us
# speed of sound 343.21 m/s in air at 20C
# 343210 mm per second
# 0.34321 mm oer microsecond
def timeToMM(t):
    return (t * 0.34321) * 0.5
    

def customToBuff(data):
    width = data[0]
    height = data[1]
    fbuff = framebuf.FrameBuffer(data[2:],width,height, framebuf.MONO_HLSB)
    return fbuff
    
def updateInfo(time,distance):
    display.fill(0)
    display.blit(logoSmallBuff,20,40)
    display.text("T:"+str(time)+"us",0,0,1)
    #display.text("Second Line:()*&",0,9,1)
    display.text("D:"+str(distance)+ "mm",0,18,1)
    #display.text("4th 1234567890.&",0,27,1)
    display.show()
    
    
def showLargeLogo():
    display.blit(logoLargeBuff, 0, 0)
    display.show()
    
       
        

logoSmallBuff = customToBuff(bytearray(base64.b64decode(logoSmallB)))
logoLargeBuff = customToBuff(bytearray(base64.b64decode(logoLargeB)))
_thread.start_new_thread(button_reader_thread,())

showLargeLogo();

while True:
    pass

