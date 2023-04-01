import machine
import time
import neopixel

class PicoLux:
    _off_color = (0, 0, 0, 0)
    _bpp = 3
    pxl = None
    
    def __init__(self, pin, count, rgbw=False):
        if rgbw:
            self._bpp = 4
        self.pxl = neopixel.NeoPixel(machine.Pin(pin), count, self._bpp)
        self._count = count
        
    def fill(self, red, green, blue, white=0):
        if white:
            self.pxl.fill((red, green, blue, white))
        else:
            self.pxl.fill((red, green, blue))
        self.pxl.write()
 
    def testCycle(self):
        for i in range(100):
            self.fill(i, i, i)
            time.sleep(.25)
