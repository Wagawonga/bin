import board 
import digitalio 
import busio  
import adafruit_tlc5947  
import time
import datetime
import colorsys
from math import *

GBPin = {
    "hour"  :
        [
            (46, 26, 27),
            (48, 47, 45),
            (13, 25, 44),
            (39, 38, 43),
            (41, 40, 42)
        ],
    "min"   :
        [
            (17, 16, 15),
            (19, 18, 14),
            (21, 20, 37),
            (23, 22, 28),
            (33, 34, 29),
            (31, 32, 30)
        ],
    "sec"   :
        [
            (11, 12, 99),
            ( 9, 10, 99),
            ( 7,  8, 99),
            ( 5,  6, 24),
            ( 3,  4, 35),
            ( 1,  2, 36)
        ]
}


# Try to great a Digital input 
pin = digitalio.DigitalInOut(board.D4) 

# Try to create an SPI device 
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
# Initialize TLC5947 
DRIVER_COUNT = 2      # change this to the number of drivers you have chained 
LATCH = digitalio.DigitalInOut(board.CE0) 

#tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH, num_drivers=DRIVER_COUNT)

# You can optionally disable auto_write which allows you to control when
# channel state is written to the chip.  Normally auto_write is true and
# will automatically write out changes as soon as they happen to a channel, but
# if you need more control or atomic updates of multiple channels then disable
# and manually call write as shown below.
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH, num_drivers=DRIVER_COUNT, auto_write=False)

# There are two ways to set channel PWM values. The first is by getting
# a PWMOut object that acts like the built-in PWMOut and can be used anywhere
# it is used in your code.  Change the duty_cycle property to a 16-bit value
# (note this is NOT the 12-bit value supported by the chip natively) and the
# PWM channel will be updated.

def first_last():
    """Cycles the red pin of LED one up, then the other LED; now dims the LEDs
    both down. Repeats with green and blue pins. Then starts all over again.
    Hook up one RGB LED to pins 0 (red), 1 (green), and 2 (blue), AND connect
    another RGB LED to pins 21, 22 and 23 of the last chained driver, respectively.
    """
    redA = tlc5947.create_pwm_out(0)
    greenA = tlc5947.create_pwm_out(1)
    blueA = tlc5947.create_pwm_out(2)
    redZ = tlc5947.create_pwm_out(DRIVER_COUNT*24-3)
    greenZ = tlc5947.create_pwm_out(DRIVER_COUNT*24-2)
    blueZ = tlc5947.create_pwm_out(DRIVER_COUNT*24-1)

    step = 10
    start_pwm = 0
    end_pwm = 32767 # 50% (32767, or half of the maximum 65535):

    while True:
        for (pinA, pinZ) in ((redA, redZ), (greenA, greenZ), (blueA, blueZ)):
            # Brighten:
            print("LED A up")
            for pwm in range(start_pwm, end_pwm, step):
                pinA.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

            print("LED Z up")
            for pwm in range(start_pwm, end_pwm, step):
                pinZ.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

            # Dim:
            print("LED A and LED Z down")
            for pwm in range(end_pwm, start_pwm, 0 - step):
                pinA.duty_cycle = pwm
                pinZ.duty_cycle = pwm
                # tlc5947.write()        # see NOTE below

    # NOTE: if auto_write was disabled you need to call write on the parent to
    # make sure the value is written in each loop (this is not common, if disabling
    # auto_write you probably want to use the direct 12-bit raw access instead,
    # shown next).

#----------
# The other way to read and write channels is directly with each channel 12-bit
# value and an item accessor syntax.  Index into the TLC5947 with the channel
# number (0-max) and get or set its 12-bit value (0-4095).
def test_all_channels(step):
    """Loops over all available channels of all connected driver boards,
    brightening and dimming all LEDs one after the other. With RGB LEDs,
    all each component is cycled. Repeats forever.
    :param step: the PWM increment in each cycle. Higher values makes cycling quicker.
    """

    start_pwm = 0
    end_pwm = 3072 # 75% of the maximum 4095

    while True:
        for pin in range(DRIVER_COUNT*24):
            print(pin)

            # Brighten:
            for pwm in range(start_pwm, end_pwm, step):
                tlc5947[pin] = pwm
                # Again be sure to call write if you disabled auto_write.
                #tlc5947.write()

            # Dim:
            for pwm in range(end_pwm, start_pwm, 0 -step):
                tlc5947[pin] = pwm
                # Again be sure to call write if you disabled auto_write.
                #tlc5947.write()

def test_led_order():
    """ geht alle LEDs durch um zu schauen ob sie richtig zugeordnet wurden"""
    
    for zeile in GBPin:
        for led in GBPin[zeile]:
            for pinColor in led:
                if pinColor != 99:
                   tlc5947[pinColor - 1] = 200
                   time.sleep(0.5)
                   tlc5947[pinColor - 1] = 0

def getBinTime():
    """ Als Rückgabe erhält man 3 Arrays [s, m, h] die Sekunden, Minuten und Stunden
    Binär als Listenwerte gespeichert haben.
    """

    time = datetime.datetime.now().time()

    #6 Leds für die Sekungen s0-s6
    s = [0] * 6
    for i in range(6):
        s[i] = (time.second & (1 << i))
    # 6 Leds für Minuten m0-m6
    m = [0] * 6
    for i in range(6):
        m[i] = (time.minute & (1 << i))
    # 5 Leds für die Stunden h0-h5
    h = [0] * 5
    for i in range(5):
        h[i] = (time.hour & (1 << i))
    return [s, m, h]


def getRGB4Point(x, y, v, compl):
    ''' gegeben wird ein Punkt im R2. dieser wid in den Einheitskreis Transformiert
    und über das HSV-Modell ein Farbwert bestimmt. Die ausgabe ist der RGB-Farbwert
    als HEX-String '''
    
    #überführen in Polare Koordinaten:
    s = sqrt(x**2 + y**2)
    if (x + s) == 0:
        h = pi
    else:
        h = 2 * atan(y / (s + x))
    
    # h soll zwischen 0,2*pi
    if h < 0:
        h = h + 2 * pi

    if compl:
        # s = 1
        h = (h + pi) % (2 * pi)
    
    #Sicherstellen, dass man sich im Einheitskreis befindet:
    #Idee dabei: r soll am Einheitskreis reflektiert werden.
    if s % 2 == 0:
        s = s % 2
        h = (h + pi) % (2 * pi)
    if s > 1:
        s = 2 - (s % 2)

    [r, g, b] = colorsys.hsv_to_rgb(h/(2 * pi), s, v) # Farbdarstellung im Intervall [0, 1]
    # print("x,y,v:", x, y, v, "s, h, h_norm:", s, h, h/(2 * pi),"r,g,b", r, g, b)
    return '#%02x%02x%02x' % (int(abs(r)*255), int(abs(g)*255), int(abs(b)*255)) # abs, da nahe 0 Werte negativ sein können

punkt = [0, 0]
v = [-0.1, -0.1] # Geschw.
v_max = .2
winkel = 0
omega = 0 # Winkelgesch.
omage_max = 0.1
steckung = 0
i = 0 # Steckgeschw.
i_max = 0.1

def modSpeeds():
    ''' Erstellt eine zufällige Tranformationsmatrix basierend auf der vorigen
    transition'''

    def modSpeed(speed, max_speed):
        res = speed + 0.25 * ((random.random() - 0.5) * max_speed)
        if res > max_speed:
            res = 2 * max_speed - res
        if res < -max_speed:
            res = -2 * max_speed - res
        return res

    # Transition
    global v
    v[0] = modSpeed(v[0], v_max)
    if (abs(punkt[0]) > 1) and (v[0] * punkt[0] > 0):
        v[0] = 0
    v[1] = modSpeed(v[1], v_max)
    if (abs(punkt[1]) > 1 ) and (v[1] * punkt[1] > 0):
        v[1] = 0
    punkt[0] = punkt[0] + v[0]
    punkt[1] = punkt[1] + v[1]

    # Drehung
    #global w
    #w = modSpeed(w, w_max)
    #winkel = winkel + w

    # Streckung
    #global i
    #i = modSpeed(i, i_max)
    #streckung = streckung + 1 + 

def modPoint(x, y):
    x_res = x + punkt[0] + v[0]
    y_res = y + punkt[1] + v[1]
    return [x_res, y_res]

def getBinTime():
    """ Als Rückgabe erhält man 3 Arrays [s, m, h] die Sekunden, Minuten und Stunden
    Binär als Listenwerte gespeichert haben.
    """
    time = datetime.datetime.now().time()

    #6 Leds für die Sekungen s0-s6
    s = [0] * 6
    for i in range(6):
        s[i] = (time.second & (1 << i))
    # 6 Leds für Minuten m0-m6
    m = [0] * 6
    for i in range(6):
        m[i] = (time.minute & (1 << i))
    # 5 Leds für die Stunden h0-h5
    h = [0] * 5
    for i in range(5):
        h[i] = (time.hour & (1 << i))
    return [s, m, h]


def setColorLed(pos, color):
    liste = GBPin["h"] + GBPin["m"] + GBPin["s"]
    addr = liste[pos]
    tlc5947[addr[0]] = color[0]
    tlc5947[addr[1]] = color[1]
    tlc5947[addr[2]] = color[2]


def paint():
    global w
    modSpeeds()
    times = getBinTime()
    times = [times[2], times[1], times[0]]
    t = [x for y in times for x in y]
    t = [0] + t
    count = 0
    pos = 0
    for y0 in range(50, 300, 100):
        for x0 in range(550, 0, -100):
            [x, y] = modPoint(x0 / 500, y0 / 500) # Anpassen so das x0 und y0 im einheitskreis liegen
            helligkeit = 0.5
            compl = False
            if (count < len(t)) and t[count] > 0:
                helligkeit = 1
                compl = True
            color = getRGB4Point(x, y, helligkeit, compl)
            count = count + 1
            setColorLed(pos, color)
            pos = pos + 1


def mainloop():
    """ Eine Iteration der Hauptfunktion der Uhr.
    """
    paint()
    tlc5947.write()
    time.sleep(0.1)

#----------
# Choose here which function to try:
if __name__ == "__main__":
    DELAY = 0.1
    try:
        while True:
            print("Iteration Start")
            time.sleep(DELAY)
            mainloop()

    except KeyboardInterrupt:
        print("ende")
        #clear()
