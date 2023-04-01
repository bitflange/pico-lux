import time, _thread
from microdot import Microdot
from pico_lux import PicoLux

p = PicoLux(19, 131)
breathe = False
animation = 0

def start():
    app = Microdot()
    
    @app.before_request
    def start_timer(request):
        request.g.start_time = time.time()
    
    @app.after_request
    def end_timer(request, response):
        duration = time.time() - request.g.start_time
        print(f'request took {duration:0.2f} seconds\n')
    
    @app.route('/')
    def index(request):
        print("HTTP GET : /")
        return "pico light server"
    
    @app.route('/api/v1/info')
    def info(request):
        print("HTTP GET : /api/v1/info")
        return "info coming soon"
    
    @app.route('/api/v1/led', methods=['GET', 'POST'])
    def lights_config(request):
        if request.method == 'GET':
            # should return status for led chain
            print("HTTP GET : /api/v1/led")
            pass
        elif request.method == 'POST':
            # should change status for led chain
            print("HTTP POST: /api/v1/led")
            pass

    @app.route('/api/v1/led/<int:id>', methods=['GET', 'POST'])
    def light_config(request, id):
        if request.method == 'GET':
            # should return status for one led
            print(f"HTTP GET : /api/v1/led/{id}")
            pass
        elif request.method == 'POST':
            # should set status for one led
            print(f"HTTP POST: /api/v1/led/{id}")
            pass50
    
    
    def do_light_cycle():
        global breathe
        brightness = 50
        min_brightness = 75
        while breathe:
            for i in range(brightness):
                val = min_brightness + i
                p.fill(val, val, val)
                time.sleep(.0050)
            for i in range(brightness):
                val = min_brightness + brightness - i
                p.fill(val, val ,val)
                time.sleep(.0050)
                
    def do_knight_rider():
        global breathe
        color = (150, 0, 0)
        bckgnd = (120, 120, 120)
        while breathe:
            print("increasing")
            for i in range(p._count):
                p.fill(120, 120, 120)
                print(i-1)
                p.pxl[i-1] = color
                try:
                    p.pxl[i-2] = color
                except:
                    pass
                try:
                    p.pxl[i] = color
                except:
                    pass
                p.pxl.write()
                time.sleep(.1)
            print("decreasing")
            for i in range(p._count):
                p.fill(120, 120, 120)
                val = p._count - (i + 1)
                print(val)
                p.pxl[val] = color
                p.pxl.write()
                time.sleep(.05)
    
    @app.route('/api/v1/anim/test', methods=['GET'])
    def light_cycle(request):
        global animation  
        global breathe  
        if not animation:
            breathe = True
            _thread.start_new_thread(do_knight_rider, ())
            animation = 1
        return "running in new thread"

    
    print("starting up microdot server")
    app.run()