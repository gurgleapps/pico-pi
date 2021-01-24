# pico-pi




- [pico-pi](#pico-pi)
  - [About](#about)
- [Coding Environment](#coding-environment)
  - [MicroPython](#micropython)
  - [CircuitPython](#circuitpython)
  - [C and C++](#c-and-c)
    - [Overview](#overview)
    - [Project Setup](#project-setup)





## About
A handy guide to getting started with the Raspberry Pi Pico


# Coding Environment

Pressing the BOOTSEL button on the pico board and plugging it in via USB will mount the pico as a mass storage device. You simply copy over a .uf2 file to change the firmware on your pico.

A good place to get started is micro python, or circuit python. You can also build your own firmware using the SDK.

## MicroPython

Grab yourself the latest version of Micro Python in the form of a .uf2 file. You should be able to find it at https://www.raspberrypi.org/ then copy it onto the device that appeared when you plugged the pico in with the BOOTSEL button pressed.

The device will be unmounted and you now have the Micro Python firmware on your Pico.


## CircuitPython

## C and C++

### Overview

You can build your own .uf2 firmware using C/C++. You need to use the SDK.

### Project Setup

On linux you need to make sure you have the correct tools
```bash
sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi
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