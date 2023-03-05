import random
import time
from _leaderboard import Leaderboard

TILES = Buffer(16, 256, "invaders_tiles.16bpp")

def draw_sprite(n, x, y):
    blit(TILES, 0, n * 16, 16, 16, x, y, )


class Ship():
    def __init__(self, game):
        self.n = 4
        self.dx = 0
        self.x = 56
        self.y = 102
        self.tick = 0
        self.dead = False
        self.game = game

    def draw(self):
        draw_sprite(self.n, self.x, self.y)

    def update(self, tick):
        # keys = _ugame.buttons.get_pressed()
        # self.set_frame(4, 0 if self.tick else 4)
        # if keys & _ugame.K_RIGHT:
        if button(RIGHT):
            self.dx = 1 # min(self.dx + 1, 4)
            # self.set_frame(5, 0)
        # elif keys & _ugame.K_LEFT:
        elif button(LEFT):
            self.dx = -1 # max(self.dx - 1, -4)
            # self.set_frame(5, 4)
        else:
            self.dx = 0 # self.dx // 2
        # if keys & _ugame.K_X:
        if pressed(A):
            if self.game.missile.y <= -16:
                self.game.missile.x = self.x
                self.game.missile.y = self.y
            #     missile.move(self.x, self.y)
            #     # sound.play(pew_sound)
            elif self.game.missile1.y <= 16:
                self.game.missile1.x = self.x
                self.game.missile1.y = self.y
            #     missile1.move(self.x, self.y)
            #     # sound.play(pew_sound)
            elif self.game.missile2.y <= 16:
                self.game.missile2.x = self.x
                self.game.missile2.y = self.y
            #     missile2.move(self.x, self.y)
            #     # sound.play(pew_sound)
        # if keys & _ugame.K_O:
        # if pressed(A):
        #     pause(" Pause...")
        self.x = max(min(self.x + self.dx, 104), 0)
        # self.move(self.x, self.y)


# class Saucer():
#     def __init__(self):
#         self.x = 0
#         self.y = 0
#         self.n = 9
#         self.tick = 0
#         self.dx = 4

#     def update(self):
#         super().update()
#         self.tick = (self.tick + 1) % 6
#         self.layer.frame(9, 0 if self.tick >= 3 else 4)
#         if self.x >= 128 or self.x <= -16:
#             self.dx = -self.dx
#         self.move(self.x + self.dx, self.y)
#         if abs(self.x - ship.x) < 4 and bomb.y >= 128:
#             bomb.move(self.x, self.y)


# class Bomb():
#     def __init__(self):
#         self.n = 6
#         self.x = 0
#         self.y = 128
#         self.boom = 0

#     def update(self):
#         super().update()
#         if self.y >= 128:
#             return
#         if self.boom:
#             if self.boom == 1:
#                 sound.play(boom_sound)
#             self.set_frame(12 + self.boom, 0)
#             self.boom += 1
#             if self.boom > 4:
#                 self.boom = 0
#                 ship.dead = True
#                 self.move(self.x, 128)
#             return
#         self.move(self.x, self.y + 8)
#         self.set_frame(6, 0 if self.y % 16 else 4)
#         if _stage.collide(self.x + 4, self.y + 4, self.x + 12, self.y + 12,
#                          ship.x + 4, ship.y + 4, ship.x + 12, ship.y + 12):
#             self.boom = 1

class Missile():
    def __init__(self, game):
        self.n = 12
        self.x = 0
        self.y = -32
        self.boom = 0
        self.power = 0
        self.game = game
        
    def draw(self):
        draw_sprite(self.n, self.x, self.y)

    def update(self, tick):
        if self.boom:
            if self.boom == 1:
                self.game.score += 1
                pass # sound.play(boom_sound)
            self.n = 12 + self.boom
            self.boom += 1
            if self.boom > 4:
                self.boom = 0
                self.kill()
                self.game.aliens.grid[self.ay][self.ax] = 0
                self.game.aliens.dirty = True
            return
        if self.y <= -32:
            return
        self.y -= 4
        self.n = 12 - self.power
        self.ax = (self.x + 8 - self.game.aliens.x) // 16
        self.ay = (self.y + 4 - self.game.aliens.y) // 16
        try:
            if self.game.aliens.grid[self.ay][self.ax] and (self.x + 8 - self.game.aliens.x) % 16 > 2:
                self.game.aliens.grid[self.ay][self.ax] = 7
                self.y -= 4
                self.boom = 1
        except IndexError:
            pass

    def kill(self):
#         self.move(self.x, -32)
        self.y = -32
#         self.set_frame(12 - self.power)
        self.n = 12 - self.power

class Aliens():
    def __init__(self, game):
        self.grid = [ [ 8 for x in range(7)] for y in range(3) ]
        # self.tick = 0
        self.left = self.descend = self.right = self.bottom = 0
        self.dx = game.level
        self.num_left = 7 * 3
        self.dirty = False
        self.x = 4
        self.y = 0
        self.i = 0
        self.game = game

    def draw(self):
        for y_index, row in enumerate(self.grid):
            for x_index, sprite in enumerate(row):
                if sprite:
                    draw_sprite(
                        sprite - self.i,
                        x_index * 16 + self.x,
                        y_index * 16 + self.y
                    )

    def update(self, tick):
        # self.tick = (self.tick + 1) % 4
        # self.layer.frame(0, 0 if self.tick >= 2 else 4)
        # print(f"x: {self.x}, l: {self.left}, r:{self.right}")
        if tick % 8 == 0:
            self.i = 1 - self.i
        if tick % 8 == 0:
            if self.x >= (8 + self.right) or self.x <= (0 - self.left):
                self.y += 1
                self.descend += 1
                if self.descend >= 4:
                    self.descend = 0
                    self.dx = -self.dx
                    self.x += self.dx
            else:
                self.x += self.dx

    def reform(self):
        self.left = 16 * 6
        self.right = 16 * 6
        self.bottom = 16 * 2
        self.num_left = 0
        for x in range(7):
            for y in range(3):
                if self.grid[y][x]:
                    self.num_left += 1
                    self.bottom = min(32 - 16 * y, self.bottom)
                    self.left   = min(16 * x, self.left)
                    self.right  = min(96 - 16 * x, self.right)
        self.dirty = False
        print(self.num_left)


# def pause(info):
#     while pressed(A):
#         time.sleep(0.25)
#     text.cursor(0, 0)
#     text.text(info)
#     game.render_block()
#     while not pressed(A):
#         time.sleep(0.25)
#     text.clear()
#     game.render_block()
#     while pressed(A):
#         time.sleep(0.25)


# tiles = stage.Bank.from_bmp16("invaders_tiles.bmp")
# while True:
#     space = stage.Grid(tiles)
#     aliens = Aliens()
#     game = stage.Stage(ugame.display, 12)
#     for y in range(8):
#         for x in range(8):
#             space.tile(x, y, 1)
#     for i in range(8):
#         space.tile(random.randint(0, 7), random.randint(0, 7),
#                    random.randint(2, 3))
#     aliens.move(8, 17)
#     saucer = Saucer()
#     bomb = Bomb()
#     ship = Ship()
#     missile = Missile(0)
#     missile1 = Missile(1)
#     missile2 = Missile(2)
#     text = stage.Text(9, 1)
#     text.move(28, 60)
#     sprites = [saucer, bomb, ship, missile, missile1, missile2]
#     game.layers = [text] + sprites + [aliens, space]
#     game.render_block()
#     pew_sound = open("invaders_pew.wav", 'rb')
#     boom_sound = open("invaders_boom.wav", 'rb')
#     sound = ugame.audio
#     sound.mute(False)

#     while aliens.left + aliens.right < 112 and aliens.y < 80 and not ship.dead:
#         for sprite in sprites:
#             sprite.update()
#         aliens.update()
#         game.render_sprites(sprites)
#         game.render_block(aliens.x + aliens.left - 1, aliens.y - 1,
#                           aliens.x + 113 - aliens.right, aliens.y + 48)
#         if aliens.dirty:
#             aliens.reform()
#         game.tick()

#     if ship.dead or aliens.y >= 80:
#         pause("Game Over")
#     else:
#         pause("You won!")

# def draw_old(tick):
#     global sprites, score, state
#     pen(0,0,0)
#     clear()
#     for sprite in sprites:
#         sprite.draw()
#     pen(5, 5, 8)
#     text("Score: " + str(score), 0, 0)
#     if state == 3:
#         pen(10,10,10)
#         text("Game over!", 10, 60)
# 
# def update_old(tick):
#     # global aliens, sprites, game
#     global sprites, state, ship, aliens, missile, missile1, missile2, score, level
#     if state == 0:
#         score = 0
#         state = 1
#         ship = Ship()
#     elif state == 1:
#         # space  = _stage.Grid(tiles)
#         aliens = Aliens()
#         # game   = _stage.Stage(.display, 12)
#         # for y in range(8):
#         #     for x in range(8):
#         #         space.tile(x, y, 1)
#         # for i in range(8):
#         #     space.tile(random.randint(0, 7), random.randint(0, 7),
#         #                random.randint(2, 3))
#         # aliens.move(8, 17)
#         # saucer   = Saucer()
#         # bomb     = Bomb()
#         
#         missile  = Missile(0)
#         missile1 = Missile(1)
#         missile2 = Missile(2)
#         # text = stage.Text(9, 1)
#         # text.move(28, 60)
#         # sprites = [saucer, bomb, ship, missile, missile1, missile2]
#         sprites = [ship, aliens, missile, missile1, missile2]
#         # game.layers = [text] + sprites + [aliens, space]
#         # game.render_block()
#         # # pew_sound = open("invaders_pew.wav", 'rb')
#         # boom_sound = open("invaders_boom.wav", 'rb')
#         # sound = .audio
#         # sound.mute(False)
#         state = 2
#     elif state == 2:
#         # if aliens.left + aliens.right < 112 and aliens.y < 80 and not ship.dead:
#         for sprite in sprites:
#             sprite.update(tick)
#         if aliens.dirty:
#             aliens.reform()
#             # aliens.update()
#         if ship.dead or (aliens.y - aliens.bottom) >= 72:
#             state = 3
#         if aliens.num_left == 0:
#             level += 1
#             state = 1
#     elif state == 3:
#         pass
        
class Invaders():
    
    def __init__(self):
        self.score = 0
        self.level = 0
        self.new_level()
        
    def new_level(self):
        self.level += 1
        self.state = 1
        self.aliens = Aliens(self)
        self.ship = Ship(self)
        self.missile = Missile(self)
        self.missile1 = Missile(self)
        self.missile2 = Missile(self)
        self.sprites = [
            self.ship,
            self.aliens,
            self.missile,
            self.missile1,
            self.missile2
        ]
        
        
def draw(tick):
    global game
    pen(0,0,0)
    clear()
    for sprite in game.sprites:
        sprite.draw()
    pen(5, 5, 8)
    text("Score: " + str(game.score), 0, 0)
    if game.state == 2:
        pen(10,10,10)
        text("Game over!", 10, 60)


def update(tick):
    global game
    if game.state == 0:
        game = Invaders()
    elif game.state == 1:
        for sprite in game.sprites:
            sprite.update(tick)
        if game.aliens.dirty:
            game.aliens.reform()
        if game.ship.dead or (game.aliens.y - game.aliens.bottom) >= 72:
            game.state = 2
        if game.aliens.num_left == 0:
            game.new_level()
    elif game.state == 2:
        pass
        

game = Invaders()
start()