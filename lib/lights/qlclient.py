import time
from websocket import WebSocket

WS_PATH = 'ws://localhost:9999/qlcplusWS'

def dimmer(level):
    dmx_level = int(level * 255)
    return ('CH|{}|{}'.format(n, dmx_level) for n in range(1, 4))

def led(level, r, g, b):
    return (
        'CH|5|{}'.format(int(level * 255)),
        'CH|7|{}'.format(int(r * 255)),
        'CH|9|{}'.format(int(g * 255)),
        'CH|11|{}'.format(int(b * 255)),
    )


class client():
    def __init__(self):
        self.ws = WebSocket()

    def __enter__(self):
        self.ws.connect(WS_PATH)
        return self

    def __exit__(self, *exc):
        self.ws.close()

    def send(self, commands):
        list(map(self.ws.send, commands))

    def daylight(self, level):
        self.send(dimmer(level))
        self.send(led(level, 1, 0.75, 0.5))

    def house(self, level):
        self.send(dimmer(level * 0.2))
        self.send(led(level * 0.4, 1, 0.25, 0.02))

    def flash(self):
        self.send(dimmer(0))
        self.send(led(1, 1, 1, 1))
        time.sleep(0.1)
        self.send(led(0, 0, 0, 0))

    def end(self, level):
        self.send(dimmer(0))
        self.send(led(level * .5, 0, 0, 1))

    def blackout(self):
        self.send(dimmer(0))
        self.send(led(0, 0, 0, 0))


if __name__ == '__main__':
    with client() as lights:
        lights.house(1)

        # lights.end(1)

        # lights.house(0)
        # time.sleep(2)
        # lights.flash()
        # time.sleep(2)
        # lights.house(1)

        # lights.daylight(1)
