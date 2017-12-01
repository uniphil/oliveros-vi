from contextlib import contextmanager
from serial import Serial

@contextmanager
def outlets(port):
    with Serial(port=port, baudrate=9600) as ser:
        yield lambda state: ser.write(b'1' if state else b'0')


if __name__ == '__main__':
    import sys, time
    port = sys.argv[1]
    with outlets(port) as set:
        while True:
            set(True)
            time.sleep(1)
            set(False)
            time.sleep(1)
