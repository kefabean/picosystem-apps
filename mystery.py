import math

spritesheet()
s = 0

def update(tick):
    global s
    if pressed(RIGHT):
        s += 1 % 256
    if pressed(LEFT):
        s -= 1 % 256
    

def draw(tick):
    pen(0,0,0)
    clear()
    for i in range(-7, 1):
        rx = math.sin(math.radians(tick + (s + i) * 45))
        ry = math.cos(math.radians(tick + (s + i) * 45))
        x = int(rx * 45.0) + 45
        y = int(ry * 20.0) + 45
        scale = int(ry * 8.0) + 24
        if i == 0:
            bounce = int(math.sin(tick/8) * 10.0 - 10.0)
        else:
            bounce = 0
        if (s + i) > -1:
            sprite(
                s + i,
                x, y + bounce,
                1, 1,
                scale, scale
            )
    pen(10,10,10)
    text(f"Sprite: {str(s)}", 38, 104)
    # add scroll bar
    frect(0, 115, 120, 5)
    pen(15, 15, 15)
    frect(int(s * 120.0 / 256.0) - 7, 115, 8, 5)

start()
