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
    
    def sfill(self, led_state):
        '''
        led_state:
                {'r': int, 'g': int, 'b': int, 'w'=0: int, 'brightness'=-1: int}
        '''
        if led_state['brightness'] >= 0:
            # brightness is 0-100 multiplier of the rgb values
            # if it's not -1, then use it as a percentage of the
            # actual rgb value specified.  A value of zero is
            # effectively turned off
            pass
        self.fill(led_state['r'], led_state['g'], led_state['b'], led_state['w'])
        return True
    
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
