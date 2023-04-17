import time, _thread
import json
from microdot import Microdot
from picolux import PicoLux


p = None
breathe = False
animation = 0

def start(config):
    global p
    print("starting picolux server")
    p = PicoLux(config)
    app = Microdot()
    default_lightstate = {"r": 0, "g": 0, "b": 0, "w": -1, "brightness": -1}

    @app.before_request
    def start_timer(request):
        request.g.start_time = time.time()

    @app.after_request
    def end_timer(request, response):
        duration = time.time() - request.g.start_time
        print(f"request took {duration:0.2f} seconds\n")

    @app.route("/")
    def index(request):
        print("HTTP GET : /")
        return "pico light server"

    @app.route("/api/v1/info")
    def info(request):
        print("HTTP GET : /api/v1/info")
        return "info coming soon"

    @app.route("/api/v1/led", methods=["GET", "POST"])
    def lights_config(request):
        global p
        payload = {}
        if request.method == "GET":
            for i, x in enumerate(p.pxl):
                payload[i] = x
            print("HTTP GET : /api/v1/led")
            return json.dumps(payload), 200
        elif request.method == "POST":
            # should change status for led chain
            """
            payload:
            {'r': int, 'g': int, 'b': int, 'w'=0: int, 'brightness'=-1: int}
            """
            payload.update(default_lightstate)
            print(request.body)
            try:
                request_data = json.loads(request.body)
            # microdot args are a little sus so we are doing this manually
            # rather than relying on dict.update().  Also all values are
            # assumed to be strings, it seems.  :(
            except:
                print("Error parsing request body printed above")
                return {"error": "could not parse request body"}, 400
            print(f"parsed body: {request_data}")
            payload.update(request_data)
            p.sfill(payload)
            print("HTTP POST: /api/v1/led")
            return payload

    @app.route("/api/v1/led/<int:idx>", methods=["GET", "POST"])
    def light_config(request, idx):
        global p
        if request.method == "GET":
            payload = {idx: p.pxl[idx]}
            print(f"HTTP GET : /api/v1/led/{id}")
            return json.dumps(payload), 200
        elif request.method == "POST":
            # should set status for one led
            """
            payload:
            {'r': int, 'g': int, 'b': int, 'w'=0: int, 'brightness'=-1: int}
            """
            payload.update(default_lightstate)
            print(request.body)
            try:
                request_data = json.loads(request.body)
            # microdot args are a little sus so we are doing this manually
            # rather than relying on dict.update().  Also all values are
            # assumed to be strings, it seems.  :(
            except:
                print("Error parsing request body printed above")
                return {"error": "could not parse request body"}, 400
            print(f"parsed body: {request_data}")
            payload.update(request_data)
            p.sset(idx, payload)
            print(f"HTTP POST: /api/v1/led/{idx}")
            payload["i"] = idx
            return payload

    def do_light_cycle():
        global p
        global breathe
        brightness = 50
        min_brightness = 75
        while breathe:
            for i in range(brightness):
                val = min_brightness + i
                p.fill(val, val, val)
                time.sleep(0.001)
            for i in range(brightness):
                val = min_brightness + brightness - i
                p.fill(val, val, val)
                time.sleep(0.001)

    def five_round_burst(idx, color, rev=False):
        global p
        for x in range(5):
            try:
                if rev:
                    p.sset(idx + x, color, write=False)
                else:
                    p.sset(idx - x, color, write=False)
            except:
                pass
        p.pxl.write()

    def do_knight_rider():
        global breathe
        color = {"r": 200, "g": 0, "b": 0, "w": 0}
        bckgnd = {"r": 30, "g": 30, "b": 30, "w": 0}
        while breathe:
            print("increasing")
            for i in range(3, p._count):
                try:
                    five_round_burst(i - 7, bckgnd)
                except:
                    pass
                five_round_burst(i, color)
                p.pxl.write()
                time.sleep(0.0025)
            print("decreasing")
            for i in range(p._count, 0, -1):
                try:
                    five_round_burst(i + 4, bckgnd, True)
                except:
                    pass
                five_round_burst(i, color)
                p.pxl.write()
                time.sleep(0.0025)
        exit()

    @app.route("/api/v1/anim/test", methods=["GET", "DELETE"])
    def light_cycle(request):
        global animation
        global breathe

        if request.method == "GET":
            if not animation:
                breathe = True
                _thread.start_new_thread(do_knight_rider, ())
                animation = 1
                return "running in new thread"
            else:
                breathe = False
                _thread.start_new_thread(do_knight_rider, ())
        elif request.method == "DELETE":
            breathe = False
            animation = 0
            return "stopping animation"

    print("starting up microdot server")
    app.run()
