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
            self.player_attack  = sum(self.dice[0:2]) + buttons[0].score
            self.monster_attack = sum(self.dice[2:4]) + buttons[3].score
        self.step += 1
        if self.step == 5:
            if self.player_attack > self.monster_attack:
                buttons[4].score = max(0, buttons[4].score - 1) 
                win.play(1200, 180, 100)
            if self.player_attack < self.monster_attack:
                buttons[1].score = max(0, buttons[1].score - 1)
                lose.play(1200, 180, 100)
        self.step %= 5
        
    def draw(self):
        global buttons
        if buttons[1].score == 0:
            pen(15, 0, 0)
            text("Player dead!", 1, 39)
            return
        if buttons[4].score == 0:
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

class NumberButton:
    def __init__(self, message, x, y, max_score, score):
        self.x = x
        self.y = y
        self.message = message
        self.score = score
        self.max_score = max_score
        
    def draw(self, is_selected):
        pen(15, 15, 15)
        rect(self.x, self.y + 11, 38, 15)
        text(str(self.score), self.x + 2, self.y + 15)
        pen(15, 10, 15)
        if is_selected:
            frect(self.x, self.y, 38, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, 38, 12)
        text(self.message, self.x + 2, self.y + 2)
        
    def press_a(self):
        pass
    
    def press_down(self):
        blip.play(200, 18, 100)
        self.score -= 1
        self.score = max(self.score, 0)
    
    def press_up(self):
        blip.play(800, 18, 50)
        self.score += 1
        self.score = min(self.score, self.max_score)
        
        
class Button:
    def __init__(self, message, x, y):
        self.x = x
        self.y = y
        self.message = message
        
    def draw(self, is_selected):
        pen(10, 10, 15)
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
    if buttons[4].score == 0:
        selected = 4
        if len(buttons) == 6:
            buttons.pop(5)
    elif buttons[1].score == 0:
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


    
        


# def update(tick):
#     global view
# 
#     if(pressed(RIGHT)):
#         view += 1
# 
#     if(pressed(LEFT)):
#         view -= 1
# 
#     view %= view_count
# 
# 
# def title(t):
#     pen(15, 15, 15)
#     frect(0, 0, 120, 11)
#     pen(0, 0, 0)
# 
#     text(f"{t} ({view + 1}/{view_count})", 2, 2)
# 
# 
# def view0_word_wrap(tick):
#     title("Word wrap")
#     wrap = int(math.sin(time.ticks_ms() / 500.0) * 36.0) + 80
# 
#     message = """\
# \\penAAAFWe are just an advanced breed of \\penFFFFmonkeys\\penAAAF on a minor \
# planet of a \\penFFFFvery average star\\penAAAF. But we can understand the \
# Universe. That makes us something very special.\
# \n\
# \n\t\\penFFFF- Stephen Hawking"""
# 
#     # measure how large the text will be and draw boundary on screen
#     w, h = measure(message, wrap)
#     pen(4, 4, 4, 4)
#     frect(0, 28, w + 4, h + 4)
# 
#     # draw wrapped text
#     pen(8, 8, 8)
#     text(message, 2, 30, wrap)
# 
#     # draw wrap width marker
#     pen(15, 15, 15)
#     text("Wrap here ", wrap - 54, 15)
#     vline(wrap + 2, 15, 8)
#     line(wrap + 2, 23, wrap + 2 - 2, 21)
#     line(wrap + 2, 23, wrap + 2 + 2, 21)
#     pen(0, 8, 0)
#     vline(wrap + 2, 27, 92)
# 
# 
# def view1_colour_codes(tick):
#     title("Colour codes")
# 
#     pen(15, 15, 15)
#     message = """\
# \\penffff~680nm is \\penf00fred\\penffff\
# \n~480nm is \\pen00ffblue\\penffff\
# \nYou're on my wavelength\
# \nAnd I quite like your hue\
# \n\
# \n\\pen0fff- Tanya Ha (@Ha_Tanya)"""
# 
#     pen(8, 8, 8)
#     text(message, 2, 32)
# 
# 
# def view2_scroll_and_clip(tick):
#     message = """\
# \"The fact that we live at the bottom of a deep gravity well, on the surface of \
# a gas covered planet going around a nuclear fireball 90 million miles away and \
# think this to be normal is obviously some indication of how skewed our \
# perspective tends to be.\""""
# 
#     # box width and height
#     bx = 30
#     by = 0
#     bw = 90
#     bh = 120
#     p = 20
# 
#     w, h = measure(message, bw - 10)
#     h += p * 2
#     overflow = h - bh
#     scroll = int((math.sin(time.ticks_ms() / 2000.0) * overflow / 2.0) + (overflow / 2.0))
#     scroll -= p
# 
#     alpha(4)
#     blit(douglas, 0, 0, 32, 45, -10, 20 - int(scroll / 3), 32 * 3, 45 * 3)
# 
#     alpha()
#     pen(12, 12, 12)
#     clip(bx, by, bw, bh)
#     text(message, bx + 5, by + 5 - scroll, bw - 10)
#     clip()
# 
#     title("Scroll and clip")



#    [view0_word_wrap, view1_colour_codes, view2_scroll_and_clip][view](tick)




