from os import path
from random import random
from subprocess import Popen
from tempfile import NamedTemporaryFile

with open(path.join(path.dirname(__file__), 'fragment-template.frag')) as f:
    FRAG_SRC = f.read()
START = 5
END = 10
PROG_LEN = 2 * 60 * 60  # 2 hours, in seconds

def make_frag(offset):
    src = FRAG_SRC.replace('#define OFFSET 0.', '#define OFFSET {}'.format(offset))
    with NamedTemporaryFile(suffix='.frag', delete=False) as f:
        f.write(src.encode())
    return f.name

class colours():
    def __init__(self, n=3):
        self.n = n

    def __enter__(self):
        for _ in range(self.n):
            offset = random() * PROG_LEN * 10 * self.n;
            frag = make_frag(offset)
            Popen(['glslViewer', frag])  # doesn't block woo

    def __exit__(self, *exc):
        pass


if __name__ == '__main__':
    import time
    with colours():
        time.sleep(100)
