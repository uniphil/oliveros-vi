from os import path
from random import random
from subprocess import Popen
from tempfile import NamedTemporaryFile

with open(path.join(path.dirname(__file__), 'fragment-template.frag')) as f:
    FRAG_SRC = f.read()

def make_frag(config, offset):
    src = FRAG_SRC\
        .replace('#define OFFSET 0.', '#define OFFSET {}'.format(offset))\
        .replace('#define GREETING 60.', '#define GREETING {}'.format(config.GREETING))\
        .replace('#define HOUSE_FADE_OUT 35.', '#define HOUSE_FADE_OUT {}'.format(config.HOUSE_FADE_OUT))\
        .replace('#define FLASH (GREETING + 150.)', '#define FLASH (GREETING + {})'.format(config.FLASH))\
        .replace('#define COLOURS (GREETING + 300.)', '#define COLOURS (GREETING + {})'.format(config.COLOURS))\
        .replace('#define DAYLIGHT (GREETING + 340.)', '#define DAYLIGHT (GREETING + {})'.format(config.DAYLIGHT))\
        .replace('#define DAYLIGHT_FADE_IN 35.', '#define DAYLIGHT_FADE_IN {}'.format(config.DAYLIGHT_FADE_IN))\
        .replace('#define BLACKOUT (GREETING + 409.77)', '#define BLACKOUT (GREETING + {})'.format(config.BLACKOUT))\
        .replace('#define END_BLUE (GREETING + 480.)', '#define END_BLUE (GREETING + {})'.format(config.END_BLUE))\
        .replace('#define END_BLUE_FADE_IN 15.', '#define END_BLUE_FADE_IN {}'.format(config.END_BLUE_FADE_IN))
    with NamedTemporaryFile(suffix='.frag', delete=False) as f:
        f.write(src.encode())
    return f.name

class colours():
    def __init__(self, t0, delay, n,
                GREETING,
                HOUSE_FADE_OUT,
                FLASH,
                COLOURS,
                DAYLIGHT,
                DAYLIGHT_FADE_IN,
                BLACKOUT,
                END_BLUE,
                END_BLUE_FADE_IN):
        self.t0 = t0
        self.delay = delay
        self.n = n
        self.GREETING = GREETING
        self.HOUSE_FADE_OUT = HOUSE_FADE_OUT
        self.FLASH = FLASH
        self.COLOURS = COLOURS
        self.DAYLIGHT = DAYLIGHT
        self.DAYLIGHT_FADE_IN = DAYLIGHT_FADE_IN
        self.BLACKOUT = BLACKOUT
        self.END_BLUE = END_BLUE
        self.END_BLUE_FADE_IN = END_BLUE_FADE_IN

        self.ps = []

    def __enter__(self):
        for _ in range(self.n):
            offset = random() * 80000 * self.n;
            frag = make_frag(self, offset)
            print('⚙  glslViewer', frag)
            proc = Popen([
                'glslViewer', frag, '-l',
                '-x', '0', '-y', '0',
                '-w', '640', '-h', '360',
            ])  # doesn't block woo
            self.ps.append(proc)

    def __exit__(self, *exc):
        for proc in self.ps:
            print('× ', ' '.join(proc.args[:2]))
            proc.terminate()


if __name__ == '__main__':
    import time
    with colours(1,15,1):
        time.sleep(100)
