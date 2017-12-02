from functools import partial
from contextlib import contextmanager
from serial import Serial

@contextmanager
def outlets(port):
    def set(ser, media, heat):
        print('⏻  media', 'on' if media else 'off')
        print('⏻  heat', 'on' if heat else 'off')
        ser.write(b'1' if media else b'0')

    with Serial(port=port, baudrate=9600) as ser:
        print('🔌  serial', port)
        yield partial(set, ser)
        print('×  serial', port)


if __name__ == '__main__':
    import sys, time
    port = sys.argv[1]
    with outlets(port) as set:
        while True:
            set(True)
            time.sleep(1)
            set(False)
            time.sleep(1)
