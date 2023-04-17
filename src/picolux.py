import gc
import machine
import time
import neopixel

from picolux_default_config import PicoluxConfig as Defaults


class PicoLux:
    _off_color = (0, 0, 0, 0)
    pxl = None

    def __init__(self, config: Defaults = None) -> None:
        self.config(config)
        gc.collect()
        
    def config(self, config: Defaults = None) -> None:
        if not config:
            print("PicoLux: using default config")
            self.config = Defaults
        else:
            print("PicoLux: using provided config")
            self.config = config
        self._bpp = self.config.BPP
        self._pin = self.config.PIN
        self._count = self.config.LED_COUNT
        self.pxl = neopixel.NeoPixel(machine.Pin(self._pin), self._count, self._bpp)
        
    def sfill(self, led_state):
        """
        led_state:
                {'r': int, 'g': int, 'b': int, 'w'=0: int, 'brightness'=-1: int}
        """
        if led_state["brightness"] >= 0:
            # brightness is 0-100 multiplier of the rgb values
            # if it's not -1, then use it as a percentage of the
            # actual rgb value specified.  A value of zero is
            # effectively turned off
            pass
        self.fill(led_state["r"], led_state["g"], led_state["b"], led_state["w"])


    def fill(self, red, green, blue, white=0):
        if self._bpp == 4:
            self.pxl.fill((red, green, blue, white))
        else:
            self.pxl.fill((red, green, blue))
        self.pxl.write()

    def set(self, idx, red, green, blue, white=0, write=False):
        if self._bpp == 4:
            self.pxl[idx] = (red, green, blue, white)
        else:
            self.pxl[idx] = (red, green, blue)

    def sset(self, idx, led_state, write=False):
        r = led_state.get("r", 0)
        g = led_state.get("g", 0)
        b = led_state.get("b", 0)
        w = led_state.get("w", 0)
        # TODO: should process the rest of teh state here
        self.set(idx, r, g, b, w, write)
        self.set()

    def write(self):
        self.pxl.write()

    def testCycle(self):
        for i in range(100):
            self.fill(i, i, i)
            time.sleep(0.25)
