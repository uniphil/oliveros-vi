from lib import colours, noise, outlets


if __name__ == '__main__':
    import sys, time
    with outlets(sys.argv[1]) as power, colours(1, 10, 1), noise():
        power(True)
        time.sleep(5)
        power(False)
        time.sleep(50)
