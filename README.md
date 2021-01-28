# pico-pi




- [pico-pi](#pico-pi)
  - [About](#about)
- [Coding Environment](#coding-environment)
  - [MicroPython](#micropython)
    - [Get MicroPython on the Pico](#get-micropython-on-the-pico)
    - [Start Coding Using MicroPython](#start-coding-using-micropython)
    - [Copy Files To Pico Using MicroPython](#copy-files-to-pico-using-micropython)
  - [CircuitPython](#circuitpython)
    - [Get CircuitPython on the Pico](#get-circuitpython-on-the-pico)
    - [Start Coding Using CircuitPython](#start-coding-using-circuitpython)
  - [C and C++](#c-and-c)
    - [Overview](#overview)
    - [Project Setup](#project-setup)





## About
A handy guide to getting started with the Raspberry Pi Pico

[![Alt text](https://img.youtube.com/vi/xpPPmEJIvhw/0.jpg)](https://youtu.be/xpPPmEJIvhw)

# Coding Environment

Pressing the BOOTSEL button on the pico board and plugging it in via USB will mount the pico as a mass storage device. You simply copy over a .uf2 file to change the firmware on your pico.

A good place to get started is micro python, or circuit python. You can also build your own firmware in C/C++ using the SDK.

## MicroPython

### Get MicroPython on the Pico

Grab yourself the latest version of Micro Python in the form of a .uf2 file. You should be able to find it at https://www.raspberrypi.org/ then copy it onto the device that appeared when you plugged the pico in with the BOOTSEL button pressed.

The device will be unmounted and you now have the Micro Python firmware on your Pico.

### Start Coding Using MicroPython

Unlike CircuitPython you can't just drag python files over to it like a mass storage device. The quickest way to get started is using Thonny https://thonny.org/. This will let you run python line by line in REPL or run the code from the editor.

It will also allow you to save files onto the Pico as you can't just drag and drop or treat the Pico as a UB drive with MicroPython. If you dave a file named main.py this file will be run whenever the Pico is powered on. 

Another option to attach to the Pico is via the USB connection using minicom. You Pico should be /dev/ttyACM0 or similar. If unsure then list the files in /dev and see which one is removed when you unplug your pico.

```bash
sudo apt install minicom
minicom -o -D /dev/ttyACM0
```

Now you should be able to type python code and ctrl-d to reboot the Pico
```
>>> print("hello world")
hello world
>>> 
MPY: soft reboot
MicroPython v1.13-290-g556ae7914 on 2021-01-21; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
```

ctrl-a then x to quit

### Copy Files To Pico Using MicroPython

If you don't want to be tied to Thonny you can use rshell

```bash
sudo apt install python3-pip
sudo pip3 install rshell
rshell -p /dev/ttyACM0
```

Type boards to list dev boards, repl boardname to enter REPL ctrl-x to exit REPL.

```
> boards
pyboard @ /dev/ttyACM0 connected Epoch: 1970 Dirs: /main.py /ssd1306.oy /ssd1306.py /pyboard/main.py /pyboard/ssd1306.oy /pyboard/ssd1306.py
> ls /pyboard
main.py    ssd1306.py ssd1306.oy
> 
```

Now you can copy files etc using cp mv mkdir rm etc.


## CircuitPython

### Get CircuitPython on the Pico

Grab yourself the latest version of Circuit Python in the form of a .uf2 file. You should be able to find it at https://circuitpython.org/downloads then copy it onto the device that appeared when you plugged the pico in with the BOOTSEL button pressed.

The device will be unmounted and you now have the Micro Python firmware on your Pico.

### Start Coding Using CircuitPython

You should see your pico mounted as a mass storage device. It will look like you just plugged in USB drive named **'CIRCUITPY'** (You can rename this if you like or just leave it).

You can drag over a file called code.py and it will run the code in that file whenver that file is created, changed, or when the pico is powered on.

You will likely want to benefit from the many libraries available for CircuitPython. You can download these from https://circuitpython.org/libraries and add any you want to use in the /lib folder on your pico.

The MU code editor is tooled up to work with CircuitPython https://codewith.mu/ 

## C and C++

### Overview

You can build your own .uf2 firmware using C/C++. You need to use the SDK.

### Project Setup

On linux you need to make sure you have the correct tools
```bash
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi
```

CD to your project folder where your code is. In our example our code is flash-led.c
```c
#include "pico/stdlib.h"

int main() {
    const uint LED_PIN = 14;
    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);
    while (true) {
        gpio_put(LED_PIN, 1);
        sleep_ms(250);
        gpio_put(LED_PIN, 0);
        sleep_ms(250);
    }
}
```

Next in your project folder clone the Pico SDK repo

```bash
git clone https://github.com/raspberrypi/pico-sdk.git
```

Copy this file to your project folder
```bash
cp pico-sdk/external/pico_sdk_import.cmake ./
```

Create CMakeLists.txt
```
touch CMakeLists.txt
```

Then edit the contents of CMakeLists.txt in this example our C code is in flash-led.c in the project folder


```
cmake_minimum_required(VERSION 3.12)
include(pico_sdk_import.cmake)
project(flash_led_project)
pico_sdk_init()

add_executable(flash_led
    flash-led.c
)

target_link_libraries(flash_led pico_stdlib)
pico_add_extra_outputs(flash_led)
```

```bash
cd build
make ..
make flash_led
```

You should find flash_led.uf2 in your build folder. Congratulations you just buult firmware you can copy to your Raspberry Pi Pico.