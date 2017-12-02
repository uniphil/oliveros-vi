from os import path
from subprocess import Popen

SHORT = path.join(path.dirname(__file__), 'white noise_short_w_automation.mp3')
LONG = path.join(path.dirname(__file__), 'White Noise_full_w_automation.mp3')

class noise():
    def __init__(self, short_version=False):
        self.short = short_version

    def __enter__(self):
        path = SHORT if self.short else LONG
        print('▶  afplay', path)
        self.p = Popen(['afplay', path])

    def __exit__(self, *exc):
        print('×  afplay')
        self.p.terminate()


if __name__ == '__main__':
    import time
    with noise():
        time.sleep(60)
