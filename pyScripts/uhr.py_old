#!/usr/bin/env python3

# import RPi.GPIO as GPIO
import time
import spidev
import numpy as np

import adafruit_tlc5947 

spi = spidev.SpiDev()
spi.open(0, 0)
led_values = np.array([0]*24)

tlc5947 = adafruit_tlc5947.TLC5947(spi)

def push():
    mask = 0xF
    atoms = [x >> y & mask for x in led_values[::-1] for y in [8, 4, 0]]
    blocks = []
    for it in range(len(atoms) // 2):
        block = (atoms[it * 2] << 4) + atoms[it * 2 + 1]
        blocks = blocks + [int(block)]  # Aendern von np.int in int
    print(blocks)
    spi.xfer(blocks)


def set(led_nr, value):
    '''Setzen einer LED. Gültige Value Werte: 0 - 0xFFFD
    eingacher ist es die LED direkt über das Numpy Array zu setzen'''
    led_values[led_nr - 1] = value


def clear():
    global led_values
    led_values[::] = 0
    spi.xfer([0x00]*36)


def getArr(num):
    b = bin(num)[2:]
    l = [0]*20 + [int(x) for x in b]
    return np.array(l)


def mulHell(mult):
    '''Berechent den Multiplikator für den Reiz
    in Abhängigkeit von dem gewünschten Multi-
    plikator der Empfindugsstärke (mult)'''
    return 8**(mult-1)


if __name__ == "__main__":
    print()
    print('Script startet:')
    print()
    DELAY = 3
    count = 0
    intCount = 10
    try:
        while True:
            intCount = intCount + 1
            helligkeit = 0
            count = 0
            set(2, helligkeit)
            push()
            time.sleep(DELAY)
            helligkeit = int(0xFFFD)
            set(2, helligkeit)
            push()
            time.sleep(DELAY)
    except KeyboardInterrupt:
        clear()
        spi.close()
