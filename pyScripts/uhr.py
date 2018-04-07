#!/usr/bin/env python3

# import RPi.GPIO as GPIO
import time
import spidev
import numpy as np

spi = spidev.SpiDev()
spi.open(0, 0)
led_values = np.array([0]*24)


def push():
    mask = 0xF
    atoms = [x >> y & mask for x in led_values[::-1] for y in [8, 4, 0]]
    blocks = []
    for it in range(len(atoms) // 2):
        block = (atoms[it * 2] << 4) + atoms[it * 2 + 1]
        blocks = blocks + [int(block)]  # Aendern von np.int in int
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
    clear()
    count = 0
    DELAY = .01

    try:
        while True:
            helligkeit = int(8**count) 
            count = (count + .1)
            if helligkeit > 0xFFF:
                helligkeit = 0
                count = 0
            # code = getArr(count) * helligkeit
            code = [helligkeit] * 20
            led_values[:4] = code[:-5:-1] 
            print(led_values)
            # led_values[0:choice([0, 1, 2, 3, 4, 5])] = 0xFFF
            push()
            time.sleep(DELAY)
    except KeyboardInterrupt:
        clear()
        spi.close()
