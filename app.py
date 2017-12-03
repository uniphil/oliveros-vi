import sys, time
from lib import colours, qlclient, noise, outlets

POWER_SER = '/dev/cu.usbmodem1421'
DMX_SER = '/dev/cu.usbserial-AL03OOPG'
SCREENS = 1
GREETING = 5
HOUSE_FADE_OUT = 3
FLASH = 10
COLOURS = 13
DAYLIGHT = 18
DAYLIGHT_FADE_IN = 3
BLACKOUT = 25
END_BLUE = 30
END_BLUE_FADE_IN = 3

t0 = time.time()

print('🌈  OLIVEROS SONIC MEDITATION VI 🌈')
try:
    delay = int(sys.argv[1]) if len(sys.argv) == 2 else 10.
except:
    print('USAGE: python app.py <time_to_start>')
    sys.exit(1)
print('   starts in {} seconds.'.format(delay))
print()

# lights(DMX_SER) as lamps,\
# with outlets(POWER_SER) as power,\
with qlclient() as lights,\
    colours(t0, delay, SCREENS,
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
    lights.house(1)
    print()

    print('☛  please arrange the shader windows onto the projectors')
    print('☛  then press <enter>')
    print()
    input('')
    if time.time() > t0 + delay:
        print('⚠  you took longer than the start delay.')
        print('⚠  sound will be {:.1f} seconds late.'.format(time.time() - (t0 + delay)))
        print()
    else:
        wait = t0 + delay - time.time()
        print('☛  starts in {:.1f} seconds'.format(wait))
        print()
        time.sleep(wait)

    with noise(True):

        while time.time() < t0 + delay + HOUSE_FADE_OUT:
            lights.house(1 - (time.time() - (t0 + delay)) / HOUSE_FADE_OUT)
            time.sleep(0.01)
        lights.house(0)

        time.sleep(t0 + delay + FLASH - time.time())
        lights.flash()

        time.sleep(t0 + delay + DAYLIGHT - time.time())

        while time.time() < t0 + delay + DAYLIGHT + DAYLIGHT_FADE_IN:
            lights.daylight((time.time() - (t0 + delay + DAYLIGHT)) / DAYLIGHT_FADE_IN)
            time.sleep(0.01)
        lights.daylight(1)

        time.sleep(t0 + delay + BLACKOUT - time.time())
        lights.blackout()

        time.sleep(t0 + delay + END_BLUE - time.time())
        while time.time() < t0 + delay + END_BLUE + END_BLUE_FADE_IN:
            lights.end((time.time() - (t0 + delay + END_BLUE)) / END_BLUE_FADE_IN)
            time.sleep(0.01)
        lights.end(1)


        # power(media=True, heat=False)
        # time.sleep(1)
        # lamps.on()
        # from random import random
        # while True:
        #     r, g, b = int(random() * 255), int(random() * 255), int(random() * 255)
        #     lamps.rgb(r, g, b)
        #     time.sleep(0.5)
        # time.sleep(5000)

