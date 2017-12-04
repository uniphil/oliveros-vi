import sys, time
from lib import colours, qlclient, noise, outlets

POWER_SER = '/dev/cu.usbmodem1421'
DMX_SER = '/dev/cu.usbserial-AL03OOPG'
SCREENS = 3

# FAST VERSION
HOUSE_FADE_OUT = 720.
FLASH = 1680.
COLOURS = 3600.
DAYLIGHT = 5820.
DAYLIGHT_FADE_IN = 475.
BLACKOUT = 6300.
END_BLUE = 7100.
END_BLUE_FADE_IN = 10.

t0 = time.time()

print('🌈  OLIVEROS SONIC MEDITATION VI 🌈')
try:
    GREETING = float(sys.argv[1]) if len(sys.argv) == 2 else 10.
except:
    print('USAGE: python app.py <time_to_start>')
    sys.exit(1)
print('   starts in {} seconds.'.format(GREETING))
print()

# lights(DMX_SER) as lamps,\
# with outlets(POWER_SER) as power,\
with qlclient() as lights,\
    colours(t0, GREETING, SCREENS,
            GREETING,
            HOUSE_FADE_OUT,
            FLASH,
            COLOURS,
            DAYLIGHT,
            DAYLIGHT_FADE_IN,
            BLACKOUT,
            END_BLUE,
            END_BLUE_FADE_IN):

    # power(media=True, heat=True)
    lights.house(0.3)
    print()

    print('☛  please arrange the shader windows onto the projectors')
    print('☛  then press <enter>')
    print()
    input('')
    lights.house(1)
    if time.time() > t0 + GREETING:
        print('⚠  you took longer than the start delay.')
        print('⚠  sound will be {:.1f} seconds late.'.format(time.time() - (t0 + GREETING)))
        print()
    else:
        wait = t0 + GREETING - time.time()
        print('☛  starts in {:.1f} seconds'.format(wait))
        print()
        time.sleep(wait)

    with noise():

        while time.time() < t0 + GREETING + HOUSE_FADE_OUT:
            lights.house(1 - (time.time() - (t0 + GREETING)) / HOUSE_FADE_OUT)
            time.sleep(0.01)
        lights.house(0)

        time.sleep(t0 + GREETING + FLASH - time.time())
        lights.flash()

        time.sleep(t0 + GREETING + DAYLIGHT - time.time())

        while time.time() < t0 + GREETING + DAYLIGHT + DAYLIGHT_FADE_IN:
            lights.daylight((time.time() - (t0 + GREETING + DAYLIGHT)) / DAYLIGHT_FADE_IN)
            time.sleep(0.01)
        lights.daylight(1)

        time.sleep(t0 + GREETING + BLACKOUT - time.time())
        lights.blackout()

        time.sleep(t0 + GREETING + END_BLUE - time.time())
        while time.time() < t0 + GREETING + END_BLUE + END_BLUE_FADE_IN:
            lights.end((time.time() - (t0 + GREETING + END_BLUE)) / END_BLUE_FADE_IN)
            time.sleep(0.01)
        lights.end(0.5)

        time.sleep(50000)


        # power(media=True, heat=False)
        # time.sleep(1)
        # lamps.on()
        # from random import random
        # while True:
        #     r, g, b = int(random() * 255), int(random() * 255), int(random() * 255)
        #     lamps.rgb(r, g, b)
        #     time.sleep(0.5)
        # time.sleep(5000)

