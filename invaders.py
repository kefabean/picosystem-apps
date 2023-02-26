import random
import time
from _leaderboard import Leaderboard

def draw_sprite(n, x, y):
    global tiles
    blit(tiles, 0, n * 16, 16, 16, x, y)


class Ship():
    def __init__(self):
        self.n = 4
        self.dx = 0
        self.x = 56
        self.y = 102
        self.tick = 0
        self.dead = False

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
        if pressed(X):
            pass
            # if missile.y <= -16:
            #     missile.move(self.x, self.y)
            #     # sound.play(pew_sound)
            # elif missile1.y <= 16:
            #     missile1.move(self.x, self.y)
            #     # sound.play(pew_sound)
            # elif missile2.y <= 16:
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


# class Missile():
#     def __init__(self, power):
#         super().__init__(tiles, 12, 0, -32)
#         self.n
#         self.x = 0
#         self.y = -32
#         self.boom = 0
#         self.power = power

#     def update(self):
#         super().update()
#         if self.boom:
#             if self.boom == 1:
#                 pass # sound.play(boom_sound)
#             self.set_frame(12 + self.boom)
#             self.boom += 1
#             if self.boom > 4:
#                 self.boom = 0
#                 self.kill()
#                 aliens.tile(self.ax, self.ay, 0)
#                 aliens.dirty = True
#             return

#         if self.y <= -32:
#             return
#         self.move(self.x, self.y - 8)
#         self.set_frame(12 - self.power, 0 if self.y % 16 == 6 else 4)
#         self.ax = (self.x + 8 - aliens.x) // 16
#         self.ay = (self.y + 4 - aliens.y) // 16
#         if aliens.tile(self.ax, self.ay) and (self.x + 10 - aliens.x) % 16 > 4:
#             aliens.tile(self.ax, self.ay, 7)
#             self.move(self.x, self.y - 4)
#             self.boom = 1

#     def kill(self):
#         self.move(self.x, -32)
#         self.set_frame(12 - self.power)


class Aliens():
    def __init__(self):
        # super().__init__(tiles, 7, 3)
        self.grid = [ [ 8 for x in range(7)] for y in range(3) ]
        #for y in range(3):
        #    for x in range(7):
        #        self.tile(x, y, 8)
        # self.tick = 0
        self.left = self.right = self.descend = 0
        self.dx = 2
        self.dirty = False
        self.x = 0
        self.y = 0

    def draw(self):
        for y_index, row in enumerate(self.grid):
            for x_index, sprite in enumerate(row):
                if sprite:
                    draw_sprite(
                        sprite,
                        x_index * 16 + self.x,
                        y_index * 16 + self.y
                    )

    def update(self, tick):
        # self.tick = (self.tick + 1) % 4
        # self.layer.frame(0, 0 if self.tick >= 2 else 4)
        if tick % 4 == 0:
            if self.x >= (14 + self.right) or self.x <= (2 - self.left):
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
        for x in range(7):
            for y in range(3):
                if self.tile(x, y):
                    self.left = min(16 * x, self.left)
                    self.right = min(96 - 16 * x, self.right)
        self.dirty = False


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

def draw(tick):
    global sprites
    pen(0,0,0)
    clear()
    for sprite in sprites:
        sprite.draw() 
    # game.render_sprites(sprites)
    # game.render_block(aliens.x + aliens.left - 1, aliens.y - 1,
    #     aliens.x + 113 - aliens.right, aliens.y + 48)
    # if ship.dead or aliens.y >= 80:
    #     pause("Game Over")
    # else:
    #     pause("You won!")

def update(tick):
    # global aliens, sprites, game
    global sprites, state, ship
    if state == 0:
        # space  = _stage.Grid(tiles)
        aliens = Aliens()
        # game   = _stage.Stage(.display, 12)
        # for y in range(8):
        #     for x in range(8):
        #         space.tile(x, y, 1)
        # for i in range(8):
        #     space.tile(random.randint(0, 7), random.randint(0, 7),
        #                random.randint(2, 3))
        # aliens.move(8, 17)
        # saucer   = Saucer()
        # bomb     = Bomb()
        ship     = Ship()
        # missile  = Missile(0)
        # missile1 = Missile(1)
        # missile2 = Missile(2)
        # text = stage.Text(9, 1)
        # text.move(28, 60)
        # sprites = [saucer, bomb, ship, missile, missile1, missile2]
        sprites = [ship, aliens]
        # game.layers = [text] + sprites + [aliens, space]
        # game.render_block()
        # # pew_sound = open("invaders_pew.wav", 'rb')
        # boom_sound = open("invaders_boom.wav", 'rb')
        # sound = .audio
        # sound.mute(False)
        state = 1
    elif state == 1:
        # if aliens.left + aliens.right < 112 and aliens.y < 80 and not ship.dead:
            for sprite in sprites:
                sprite.update(tick)
            # aliens.update()


# tiles = _stage.Bank.from_bmp16("invaders_tiles.bmp")
tiles = Buffer(16, 256)
open("invaders_tiles.16bpp", "rb").readinto(tiles)
ship = None
state = 0
sprites = []
start()