#!/usr/bin/env python3

# import RPi.GPIO as GPIO
import time
import spidev
import numpy as np
from random import choice

spi = spidev.SpiDev()
spi.open(0, 0)
led_values = np.array([0]*24)


def push():
    mask = 0xF
    atoms = [x >> y & mask for x in led_values[::-1] for y in [8, 4, 0]]
    print(atoms)
    blocks = []
    for it in range(len(atoms) // 2):
        block = (atoms[it * 2] << 4) + atoms[it * 2 + 1]
        blocks = blocks + [int(block)] #  Aendern von np.int in int
    print(blocks)
    spi.xfer(blocks)


def set(led_nr, value):
    '''Setzen einer LED. Gültige Value Werte: 0 - 0xFFF '''
    led_values[led_nr - 1] = value


def clear():
    global led_values
    led_values[::] = 0
    spi.xfer([0x00]*36)


if __name__ == "__main__":
    DELAY = 1
    print()
    print('Script startet:')
    print()
    clear()
    count = 0
    try:
        while True:
            count = (count + 1) % 0xFFF
            led_values[0:5] = 1 
            push()
            time.sleep(DELAY)
    except KeyboardInterrupt:
        clear()
        spi.close()
