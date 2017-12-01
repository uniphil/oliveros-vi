from os import path
from random import random
from subprocess import Popen
from tempfile import NamedTemporaryFile

with open(path.join(path.dirname(__file__), 'fragment-template.frag')) as f:
    FRAG_SRC = f.read()

def make_frag(start, end, offset):
    print('{}, {}, {}'.format(start, end, offset))
    src = FRAG_SRC\
        .replace('#define OFFSET 0.', '#define OFFSET {}'.format(offset))\
        .replace('#define START 1.', '#define START {}'.format(start))\
        .replace('#define END 1000.', '#define END {}'.format(end))
    with NamedTemporaryFile(suffix='.frag', delete=False) as f:
        f.write(src.encode())
    return f.name

class colours():
    def __init__(self, start=1, end=5, n=3):
        self.start = float(start)
        self.end = float(end)
        self.n = n

    def __enter__(self):
        for _ in range(self.n):
            offset = random() * self.end * 10 * self.n;
            frag = make_frag(self.start, self.end, offset)
            Popen([
                'glslViewer', frag, '-l',
                '-x', '0', '-y', '0',
                '-w', '1280', '-h', '720',
            ])  # doesn't block woo

    def __exit__(self, *exc):
        pass


if __name__ == '__main__':
    import time
    with colours(1,2,1):
        time.sleep(100)
