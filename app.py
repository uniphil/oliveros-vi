import sys, time
from lib import colours, lights, noise, outlets

POWER_SER = '/dev/cu.usbmodem1421'
DMX_SER = '/dev/cu.usbserial-AL03OOPG'
SCREENS = 1
COLOURS_START = 5
COLOURS_END = 3600
t0 = time.time()

print('🌈  OLIVEROS SONIC MEDITATION VI 🌈')
try:
    delay = int(sys.argv[1])
except:
    print('USAGE: python app.py <time_to_start>')
    sys.exit(1)
print('   starts in {} seconds.'.format(delay))
print()

# lights(DMX_SER) as lamps,\
with outlets(POWER_SER) as power,\
    colours(delay + COLOURS_START, delay + COLOURS_END, SCREENS):

    power(media=True, heat=True)
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

    with noise():
        power(media=True, heat=False)
        time.sleep(1)
        # lamps.on()
        from random import random
        # while True:
        #     r, g, b = int(random() * 255), int(random() * 255), int(random() * 255)
        #     lamps.rgb(r, g, b)
        #     time.sleep(0.5)
        time.sleep(5000)

