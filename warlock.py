import io
import math
import time
import random
import json


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


class ActionButton(Button):

    def draw(self, is_selected):
        pen(10, 10, 15)
        if is_selected:
            frect(self.x, self.y, 38, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, 38, 12)
        text(self.message, self.x + 2, self.y + 2)

    def update(self):
        if pressed(A):
            blip.play(500, 120, 100)
            self.func()


class NumberButton(Button):        
        
    def draw(self, is_selected):
        pen(15, 10, 15)
        rect(self.x, self.y + 11, 38, 15)
        text(str(self.func()), self.x + 2, self.y + 15)
        if is_selected:
            frect(self.x, self.y, 38, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, 38, 12)
        text(self.message, self.x + 2, self.y + 2)

    def update(self):
        if pressed(DOWN):
            blip.play(200, 18, 100)
            self.func(-1)
        if pressed(UP):
            blip.play(800, 18, 50)
            self.func(1)


class LetterButton(Button):
        
    def draw(self, is_selected):
        pen(5, 5, 10)
        if is_selected:
            frect(self.x, self.y, 10, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, 10, 12)
        text(self.message, self.x + 2, self.y + 2)
        
    def update(self):
        if pressed(A):
            self.func(self.message)


class Player:

    def __init__(self, data):
        if data is None:
            self.reset()
        else:
            self._skill   = data['_skill']
            self._stamina = data['_stamina']
            self._luck    = data['_luck']
            self._gold    = data['_gold']
            self._hero    = data['_hero']
            self._note    = data['_note']

    def skill(self, delta = 0):
        self._skill = max(min(12, self._skill + delta), 0)
        return self._skill
        
    def stamina(self, delta = 0):
        self._stamina = max(min(24, self._stamina + delta), 0)
        return self._stamina

    def luck(self, delta = 0):
        self._luck = max(min(24, self._luck + delta), 0)
        return self._luck

    def gold(self, delta = 0):
        self._gold = max(self._gold + delta, 0)
        return self._gold

    def hero(self, delta = 0):
        self._hero = max(self._hero + delta, 0)
        return self._hero

    def backspace(self, char):
        self._note = self._note[:-1]
        
    def add_char(self, char):
        self._note += char
    
    def reset(self):
            self._skill   = random.randint(1, 6) + 6
            self._stamina = random.randint(1, 6) + random.randint(1, 6) + 12
            self._luck    = random.randint(1, 6) + 6
            self._gold    = 0
            self._hero    = 0
            self._note    = ""


class Scene:
    
    def __init__(self, game):
        self.button_index = 0
        self.moved = False
        self.game = game
        self.init()

    def navigate(self):
        if pressed(LEFT):
            if self.button_index > 0:
                self.button_index -= 1
                self.moved = True
            else:
                self.moved = False
        if pressed(RIGHT):
            if self.button_index < (len(self.buttons) - 1):
                self.button_index += 1
                self.moved = True
            else:
                self.moved = False

    def draw(self, tick):
        pass

    def update(self):
        pass


class NoteScene(Scene):

    def init(self):
        letters = '1234567890-abcedfghihjklmnopqrstuvwxyz,.:? '
        self.buttons  = [
            LetterButton(
                char,
                11 * (count % 11),
                65 + 13 * (count // 11),
                self.game.player.add_char
            ) for count, char in enumerate(letters)
        ]
        self.buttons.append(
            LetterButton("<", 11 * 10,  65 + 13 * 3, self.game.player.backspace)
        )

    def draw(self, tick):
        pen(5, 5, 10)
        text("Notes:", 1, 1)
        pen(5, 15, 5)
        if tick // 10 % 2 == 0:
            cursor = "|"
        else:
            cursor = " "
        text(self.game.player._note + cursor, 1, 14, 120)

    def update(self):
        if pressed(UP):
            if self.button_index > 10:
                self.button_index -= 11
                blip.play(1600, 30, 100)
        if pressed(DOWN):
            if (len(self.buttons) - self.button_index) > 11:
                blip.play(1800, 30, 100)
                self.button_index += 11


class ResetScene(Scene):

    def init(self):
        self.buttons  = [
            ActionButton("Reset?", 1,  1, self.game.player.reset)
        ]
        
        
class AttrScene(Scene):

    def init(self):
        self.buttons  = [
            NumberButton("Gold", 1,  1, self.game.player.gold),
            NumberButton("Hero", 41, 1, self.game.player.hero)
        ]


class DiceScene(Scene):

    def init(self):
        self.step     = 0
        self.dice     = []
        self.buttons  = [
            NumberButton("Skill", 1,  1, self.game.player.skill),
            NumberButton("Stam", 41,  1, self.game.player.stamina),
            NumberButton("Luck", 81,  1, self.game.player.luck),
            NumberButton("Skill", 1, 60, self.game.monster.skill),
            NumberButton("Stam", 41, 60, self.game.monster.stamina),
            ActionButton("Roll", 81, 60, self.roll)
        ]
    
    def roll(self):
        if self.step == 0:
            self.dice = [ random.randint(1, 6) for r in range(4) ]
            self.player_attack  = sum(self.dice[0:2]) + self.game.player.skill()
            self.monster_attack = sum(self.dice[2:4]) + self.game.monster.skill()
        self.step += 1
        if self.step == 5:
            if self.player_attack > self.monster_attack:
                self.monster.stamina(-1) 
                win.play(1200, 180, 100)
            if self.player_attack < self.monster_attack:
                self.player.stamina(-1)
                lose.play(1200, 180, 100)
        self.step %= 5

    def draw_dice(self, x, y, val):
        pen(10, 10, 10)
        frect(x, y, 20, 20)
        pen(0, 0, 0)
        text(str(val), x + 7, y +7)
        
    def draw(self, tick):
        if self.game.player.stamina() == 0:
            pen(15, 0, 0)
            text("Player dead!", 1, 39)
            return
        if self.game.monster.stamina() == 0:
            pen(15, 0, 0)
            text("Monster killed!", 1, 98)
            return
        if self.step > 0:
            self.draw_dice(1, 33, self.dice[0])
        if self.step > 1:
            self.draw_dice(28, 33, self.dice[1])
            pen(15, 0, 0)
            text("Attack = " + str(self.player_attack), 53, 39)
        if self.step > 2:
            self.draw_dice(1, 92, self.dice[2])
        if self.step > 3:
            self.draw_dice(28, 92, self.dice[3])
            pen(15, 0, 0)
            text("Attack = " + str(self.monster_attack), 53, 98)


class Game:

    def __init__(self):
        self.scene_index = 1
        data = self.load()
        self.player  = Player(data["player"])
        self.monster = Player(data["monster"])
        self.scenes  = [
            ResetScene(self),
            DiceScene(self),
            AttrScene(self),
            NoteScene(self)
        ]

    def draw(self, tick):
        pen(0, 0, 0)
        clear()
        scene = self.scenes[self.scene_index]
        for count, b in enumerate(scene.buttons):
            b.draw(scene.button_index == count)
        scene.draw(tick)
        
    def load(self):
        try:
            with open("warlock_data.json",'r') as fh:
               load_data = json.load(fh)
        except:
            load_data = {
                "monster": None,
                "player": None,
                "note": ""
            }
        return load_data
        
    def save(self):
        save_data = {
            "player": self.player.__dict__,
            "monster": self.monster.__dict__
        }
        with open("warlock_data.json",'w') as fh:
           json.dump(save_data, fh)

    def update(self, tick):
        scene = self.scenes[self.scene_index]
        scene.navigate()
        if pressed(LEFT):
            blip.play(1600, 30, 100)
            if not scene.moved and self.scene_index > 0:
                self.scene_index -= 1
        if pressed(RIGHT):
            blip.play(1800, 30, 100)
            if not scene.moved and self.scene_index < (len(self.scenes) - 1):
                self.scene_index += 1
        scene.update()
        scene.buttons[scene.button_index].update()
        if pressed(A) or pressed(UP) or pressed(DOWN):
            self.save()


def update(tick):
    global g
    g.update(tick)
        

def draw(tick):
    global g
    g.draw(tick)


g = Game()
g.load()
start()