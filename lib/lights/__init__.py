import time
from threading import Thread
from queue import Empty, Queue
from .dmx import dmx

class lights():
    def __init__(self, port):
        self.port = port
        self.queue = Queue()
        self.thread = Thread(target=self.worker)
        self.state = (0,)

    def __enter__(self):
        print('💡  serial', self.port)
        self.thread.start()
        return self

    def __exit__(self, *exc):
        print('×  serial', self.port)
        self.queue.put('death')
        self.thread.join(timeout=0.1)

    def on(self):
        print('💡  on')
        self.state = (255,)

    def off(self):
        print('💡  off')
        self.state = (0,)

    def rgb(self, r, g, b):
        print('💡  rgb {} {} {}'.format(r, g, b))
        self.state = (255, 0, 0, 255, r, g, b)

    def worker(self):
        with dmx(self.port) as write:
            while True:
                try:
                    task = self.queue.get_nowait()
                except Empty:
                    write(*self.state)
                    continue
                if task == 'death':
                    print('   byeeeeee from dmx thread')
                    self.queue.task_done()
                    break
                else:
                    print('wat', task)
                    continue

