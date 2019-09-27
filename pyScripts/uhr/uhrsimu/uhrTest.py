from tkinter import *
import colorsys
import random
import time
import datetime
from math import *

master = Tk()

w = Canvas(master, width=650, height=350)
w.pack()

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

def paint():
    global w
    modSpeeds()
    times = getBinTime()
    times = [times[2], times[1], times[0]]
    t = [x for y in times for x in y]
    t = [0] + t
    count = 0
    for y0 in range(50, 300, 100):
        for x0 in range(550, 0, -100):
            [x, y] = modPoint(x0 / 500, y0 / 500) # Anpassen so das x0 und y0 im einheitskreis liegen
            helligkeit = 0.5
            compl = False
            if (count < len(t)) and t[count] > 0:
                helligkeit = 1
                compl = True
            color = getRGB4Point(x, y, helligkeit, compl)
            w.create_rectangle(x0, y0, x0+50, y0+50, fill=color)
            count = count + 1
    w.create_rectangle(50, 50, 100, 100, fill="white")
    w.after(10, paint)

paint()
mainloop()
