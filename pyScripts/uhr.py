#!/usr/bin/env python3

# import RPi.GPIO as GPIO
import time
import spidev

print()
print('Script startet:')
print()


DELAY = 1

spi = spidev.SpiDev()
spi.open(0, 0)
led_values = [0]*24


def push():
    mask = 0xF
    # Bitreihenfolge umdehren
    # rev = [int('{:012b}'.format(x)[::-1], 2) for x in led_values]
    # rev = rev[::-1]  # Slicing um array zu Invertieren!
    print(led_values)
    atoms = [x >> y & mask for x in led_values[::-1] for y in [8, 4, 0]]
    blocks = []
    for it in range(len(atoms) // 2):
        block = (atoms[it * 2] << 4) + atoms[it * 2 + 1]
        blocks = blocks + [block]
    print(blocks)
    spi.xfer(blocks)


def set(led_nr, value):
    '''Setzen einer LED. Gültige Value Werte: 0 - 0xFFF '''
    led_values[led_nr - 1] = value


def clear():
    global led_values
    led_values = [0]*24
    spi.xfer([0x00]*36)


clear()
count = 0
try:
    while True:
        count = (count + 1) % 0xFFF
        # spi.xfer([count] + [0x0]*5)
        set(1, count)
        set(2, count)
        set(3, count)
        set(4, count)
        push()
        time.sleep(DELAY)
except KeyboardInterrupt:
    clear()
    spi.close()
