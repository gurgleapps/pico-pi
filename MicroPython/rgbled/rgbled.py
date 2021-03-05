import machine
import time
"""
GurgleApps.com RGB LED Micropython code
"""


class RGBLED():
    """
    Class for regular RGB LED not LED strips

    Example:

    led = RGBLED(0,2,3)
    led.setColor(0xFF00FF)
    """
    gamma = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 13, 13, 14, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30, 31, 31, 32, 33, 33, 34, 35, 36, 36, 37, 38, 39, 40, 40, 41, 42, 43, 44, 45, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
             70, 71, 72, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 86, 87, 88, 89, 91, 92, 93, 95, 96, 97, 99, 100, 101, 103, 104, 105, 107, 108, 110, 111, 113, 114, 115, 117, 118, 120, 121, 123, 125, 126, 128, 129, 131, 132, 134, 136, 137, 139, 140, 142, 144, 145, 147, 149, 151, 152, 154, 156, 158, 159, 161, 163, 165, 166, 168, 170, 172, 174, 176, 178, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 220, 222, 224, 226, 228, 230, 232, 235, 237, 239, 241, 244, 246, 248, 250, 253, 255]

    def __init__(self, red_pin, green_pin, blue_pin, common_anode=True):
        self.freq = 4000
        self.full = 65535  # all of cycle
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.red = machine.PWM(machine.Pin(self.red_pin))
        self.red.freq(self.freq)
        self.green = machine.PWM(machine.Pin(self.green_pin))
        self.green.freq(self.freq)
        self.blue = machine.PWM(machine.Pin(self.blue_pin))
        self.blue.freq(self.freq)
        self.common_anode = common_anode

    def cleanup(self):
        self.off()
        self.red.deinit()
        self.green.deinit()
        self.blue.deinit()

    def __exit__(self, exception_type, exception_value, traceback):
        self.cleanup()

    def off(self):
        offDuty = 0
        if self.common_anode:
            offDuty = 65535
        self.red.duty_u16(offDuty)
        self.green.duty_u16(offDuty)
        self.blue.duty_u16(offDuty)

    @staticmethod
    def color(r, g, b):
        return RGBLED.colour(r, g, b)

    @staticmethod
    def colour(r, g, b):
        return (r << 16) | (g << 8) | b

    def setColor(self, c, gammaCorrect=False, intensity=1):
        r = (c >> 16)
        g = (c >> 8) & 0xFF
        b = c & 0xFF
        if intensity < 1:
            r = int(r * intensity)
            g = int(g * intensity)
            b = int(b * intensity)
        # Quick and dirty imperfect Gamma Correct
        if gammaCorrect:
            r = self.gamma[r]
            g = self.gamma[g]
            b = self.gamma[b]
        step = self.full / 255
        if self.common_anode:
            self.red.duty_u16(self.full - int(step * r))
            self.green.duty_u16(self.full - int(step * g))
            self.blue.duty_u16(self.full - int(step * b))
        else:
            self.red.duty_u16(int(step * r))
            self.green.duty_u16(int(step * g))
            self.blue.duty_u16(int(step * b))

    def setColour(self, c, gammaCorrect=False):
        self.setColor(c, gammaCorrect)

    @staticmethod
    def spectrum(pos):
        if pos < 85:
            return RGBLED.color(255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return RGBLED.color(0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return RGBLED.color(pos * 3, 0, 255 - pos * 3)

    def rainbow(self, pos):
        """
        Not really needed, just with some boards we had better results with this code
        when driving multiple LEDs
        You can just use spectrum() and setColor()
        """
        none = self.full  # for common anode
        step = none / 85
        if not self.common_anode:
            none = 0
        if pos < 0 or pos > 255:
            pass
        elif pos < 86:
            if self.common_anode:
                x = none - int(step * pos)  # starts max and tends to 0
            else:
                x = int(step * pos)  # starts 0 tends to max
            self.red.duty_u16(self.full - x)  # start full red and go to 0
            self.green.duty_u16(x)  # start no green and go to full
            self.blue.duty_u16(none)  # no blue
        elif pos < 171:
            pos -= 85
            if self.common_anode:
                x = none - int(step * pos)
            else:
                x = int(step * pos)
            self.red.duty_u16(none)
            self.green.duty_u16(self.full - x)
            self.blue.duty_u16(x)
        else:
            pos -= 170
            if self.common_anode:
                x = none - int(step * pos)
            else:
                x = int(step * pos)
            self.red.duty_u16(x)
            self.green.duty_u16(none)
            self.blue.duty_u16(self.full - x)
