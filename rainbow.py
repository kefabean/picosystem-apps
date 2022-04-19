import io
import time
import random
import math


selected = 0
blip = Voice(10, 10, 10, 10, 40, 2)
lose = Voice(10, 10, 10, 40, -2, 10, 100, 100)
win  = Voice(10, 10, 30, 40, 20, 10, 0, 0)


def update(tick):
    pass
        

def draw(tick):
    
    #text("Daddy is the worst at tidying up", 0, 60, 120)
    #text("lara is the very, very, very, very, very, very, very BEST",0,15+tick%15,120
    pen(15, 15, 15)
    clear()
    y = 40 + int(20 * math.sin((tick) / 16))
    for i in range(1, 20):
        hue = ((tick + i) % 100) / 100
        colour = hsv(hue, 1, 1)
        pen(colour)
        #rect(0, 0, 120, 120)
        frect(0, y - (20 - i), 120, 2 * (20- i))
    pen(0,0,0)
    text("     I love rainbow bear", 0, y - 4, 120)


start()