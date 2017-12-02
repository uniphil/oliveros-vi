import serial, sys, time
from contextlib import contextmanager
from functools import partial

DMX_START_CODE = 0x00

def write_dmx(ser, *levels):
    # ser8N2dtr = 0
    # time.sleep(0.01)
    # ser8N2dtr = 1
    # time.sleep(0.01)

    assert len(levels) <= 512,\
        'this universe is not infinite :( cannot write to more than 512 channels'

    if len(levels) < 24:
        levels = levels + (0,) * (24 - len(levels))

    data = bytes((DMX_START_CODE,) + levels)

    # break & MAB
    ser.baudrate = 57600
    ser.bytesize = serial.SEVENBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.write(bytes((0,)))
    # dmx packets
    ser.baudrate = 250_000
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_TWO
    ser.write(data)

    time.sleep(0.02)


@contextmanager
def dmx(port):
    with serial.Serial(
        port=port,
        baudrate=250000,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO
    ) as ser:
        yield partial(write_dmx, ser)
