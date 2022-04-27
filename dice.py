import io
import math
import time
import random


selected = 0
blip = Voice(10, 10, 10, 10, 40, 2)
lose = Voice(10, 10, 10, 40, -2, 10, 100, 100)
win  = Voice(10, 10, 30, 40, 20, 10, 0, 0)


class Button:

    def __init__(self, message, x, y, func):
        self.x = x
        self.y = y
        self.message = message
        self.func = func
        self.hidden = False


class ActionButton(Button):

    def draw(self, tick, is_selected):
        if not self.hidden:
            pen(10, 10, 15)
            if is_selected:
                frect(self.x, self.y, 38, 12)
                pen(0, 0, 0)
            else:
                rect(self.x, self.y, 38, 12)
            text(self.message, self.x + 2, self.y + 2)

    def update(self, tick):
        if pressed(A):
            blip.play(500, 120, 100)
            self.func()


class NumberButton(Button):        
        
    def draw(self, tick, is_selected):
        if not self.hidden:
            pen(15, 10, 15)
            rect(self.x, self.y + 11, 38, 15)
            text(str(self.func()), self.x + 2, self.y + 15)
            if is_selected:
                frect(self.x, self.y, 38, 12)
                pen(0, 0, 0)
            else:
                rect(self.x, self.y, 38, 12)
            text(self.message, self.x + 2, self.y + 2)

    def update(self, tick):
        if pressed(DOWN):
            blip.play(200, 18, 100)
            self.func(-1)
        if pressed(UP):
            blip.play(800, 18, 50)
            self.func(1)


class Game:

    def __init__(self):
        self.button_index = 0
        self.buttons = [
            NumberButton("Dice", 2,  1, self.dice_number),
            ActionButton("Roll", 80, 1, self.roll)
        ]
        self._dice_number = 1
        self.dice_rolls = []
        self.patterns = {
         1: [0, 0, 0, 0, 1, 0, 0, 0, 0],
         2: [1, 0, 0, 0, 0, 0, 0, 0, 2],
         3: [1, 0, 0, 0, 1, 0, 0, 0, 1],
         4: [1, 0, 1, 0, 0, 0, 1, 0, 1],
         5: [1, 0, 1, 0, 1, 0, 1, 0, 1],
         6: [1, 0, 1, 1, 0, 1, 1, 0, 1]
        }
    
    def dice_number(self, delta = 0):
        self._dice_number = max(min(12, self._dice_number + delta), 1)
        return self._dice_number

    def roll(self):
        self.dice_rolls = [ random.randint(1, 6) for r in range(self._dice_number) ]

    def draw_dice(self, x, y, num):
        size = 6
        pattern = self.patterns[num]
        rect(x - size + 1, y - size + 1, 4 * size, 4 * size)
        for count, dot in enumerate(pattern):
            if dot:
                fcircle(x + (count % 3) * size, y + (count // 3) * size, 2)

    def draw(self, tick):
        pen(0, 0, 0)
        clear()
        for count, b in enumerate(self.buttons):
            b.draw(tick, self.button_index == count)
        pen(0, 15, 0)
        for count, roll in enumerate(self.dice_rolls):
            self.draw_dice(7 + (count % 4) * 30, 36 + (count // 4) * 30, roll)

    def update(self, tick):
        for b in self.buttons:
            b.update(tick)
        if pressed(LEFT):
            if self.button_index > 0:
                self.button_index -= 1
        if pressed(RIGHT):
            if self.button_index < (len(self.buttons) - 1):
                self.button_index += 1


def update(tick):
    global g
    g.update(tick)
        

def draw(tick):
    global g
    g.draw(tick)


g = Game()
start()