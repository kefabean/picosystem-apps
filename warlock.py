import io
import math
import time
import random
import json


selected = 0
blip = Voice(10, 10, 10, 10, 40, 2)
lose = Voice(10, 10, 10, 40, -2, 10, 100, 100)
win  = Voice(10, 10, 30, 40, 20, 10, 0, 0)


class Dice:
    def __init__(self):
        self.step = 0
        self.player_attack  = 0
        self.monster_attack = 0
    
    def roll(self):
        global buttons
        if self.step == 0:
            self.dice = [ random.randint(1, 6) for r in range(4) ]
            self.player_attack  = sum(self.dice[0:2]) + buttons[0].val
            self.monster_attack = sum(self.dice[2:4]) + buttons[3].val
        self.step += 1
        if self.step == 5:
            if self.player_attack > self.monster_attack:
                buttons[4].val = max(0, buttons[4].val - 1) 
                win.play(1200, 180, 100)
            if self.player_attack < self.monster_attack:
                buttons[1].val = max(0, buttons[1].val - 1)
                lose.play(1200, 180, 100)
        self.step %= 5
        
    def draw(self):
        global buttons
        if buttons[1].val == 0:
            pen(15, 0, 0)
            text("Player dead!", 1, 39)
            return
        if buttons[4].val == 0:
            pen(15, 0, 0)
            text("Monster killed!", 1, 98)
            return
        if self.step > 0:
            pen(10, 10, 10)
            frect(1, 33, 20, 20)
            pen(0, 0, 0)
            text(str(self.dice[0]), 8, 39)
        if self.step > 1:
            pen(10, 10, 10)
            frect(28, 33, 20, 20)
            pen(0, 0, 0)
            text(str(self.dice[1]), 36, 39)
            pen(10, 10, 10)
            text("Attack = " + str(self.player_attack), 53, 39)
        if self.step > 2:
            pen(10, 10, 10)
            frect(1, 92, 20, 20)
            pen(0, 0, 0)
            text(str(self.dice[2]), 8, 98)
        if self.step > 3:
            pen(10, 10, 10)
            frect(28, 92, 20, 20)
            pen(0, 0, 0)
            text(str(self.dice[3]), 36, 98)
            pen(10, 10, 10)
            text("Attack = " + str(self.monster_attack), 53, 98)


class Button:
    def __init__(self, message, x, y):
        self.x = x
        self.y = y
        self.message = message
        self.col = (10, 10, 15)
        
    def draw(self, is_selected):
        pen(*self.col)
        if is_selected:
            frect(self.x, self.y, 38, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, 38, 12)
        text(self.message, self.x + 2, self.y + 2)
        
    def press_a(self):
        global dice
        blip.play(500, 120, 100)
        dice.roll()   
    
    def press_down(self):
        pass
    
    def press_up(self):
        pass


class NumberButton(Button):
    def __init__(self, message, x, y, max_val, val):
        self.x = x
        self.y = y
        self.message = message
        self.val = val
        self.max_val = max_val
        self.col = (15, 10, 15)
        
    def draw(self, is_selected):
        pen(*self.col)
        rect(self.x, self.y + 11, 38, 15)
        text(str(self.val), self.x + 2, self.y + 15)
        pen(*self.col)
        super().draw(is_selected)
        
    def press_a(self):
        pass
    
    def press_down(self):
        blip.play(200, 18, 100)
        self.val -= 1
        self.val = max(self.val, 0)
    
    def press_up(self):
        blip.play(800, 18, 50)
        self.val += 1
        self.val = min(self.val, self.max_val)

 
def update(tick):
    global selected, buttons
    if pressed(LEFT):
        blip.play(1600, 30, 100)
        selected -= 1
    if pressed(RIGHT):
        blip.play(1800, 30, 100)
        selected += 1
    if pressed(A):
        buttons[selected].press_a()
    if pressed(UP):
        buttons[selected].press_up()
    if pressed(DOWN):
        buttons[selected].press_down()
    selected %= len(buttons)
    if buttons[4].val == 0:
        selected = 4
        if len(buttons) == 6:
            buttons.pop(5)
    elif buttons[1].val == 0:
        selected = 1
        if len(buttons) == 6:
            buttons.pop(5)
    else:
        if len(buttons) == 5:
            buttons.append(Button("Roll", 81, 60))
        

def draw(tick):
    global buttons, dice
    pen(0, 0, 0)
    clear()
    for count, m in enumerate(buttons):
        m.draw(selected == count)
    dice.draw()

buttons = [
    NumberButton("Skill", 1, 1, 12, 11),
    NumberButton("Stam", 41, 1, 24, 18),
    NumberButton("Luck", 81, 1, 12, 10),
    NumberButton("Skill", 1, 60, 12, 8),
    NumberButton("Stam", 41, 60, 25, 4),
    Button("Roll", 81, 60)
]

dice = Dice()

start()