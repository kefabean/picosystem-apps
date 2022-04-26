import math

spritesheet()
s = 0
carousel = True
button_tick = 0

def update(tick):
    global s, carousel, button_tick
    delay = tick > (button_tick + 3)
    if button(RIGHT) and delay:
        s = (s + 1) % 256
        button_tick = tick
    if button(LEFT) and delay:
        s = (s - 1) % 256
        button_tick = tick
    if pressed(A):
        carousel = not carousel
    

def draw(tick):
    pen(0,0,0)
    clear()
    bounce = int(math.sin(tick/8) * 10.0 - 10.0)
    if carousel:
        for i in range(-7, 1):
            rx = math.sin(math.radians(tick + (s + i) * 45))
            ry = math.cos(math.radians(tick + (s + i) * 45))
            x = int(rx * 45.0) + 45
            y = int(ry * 20.0) + 45
            scale = int(ry * 8.0) + 24
            if i == 0:
                b = bounce
            else:
                b = 0
            if (s + i) > -1:
                sprite(
                    s + i,
                    x, y + b,
                    1, 1,
                    scale, scale
                )
    else:
        sprite(s, 20, 20 + bounce, 1, 1, 80, 80)
    pen(10,10,10)
    text(f"Sprite: {str(s)}", 38, 104)
    # add scroll bar
    frect(0, 115, 120, 5)
    pen(15, 15, 15)
    frect(int(s * 120.0 / 256.0) - 7, 115, 8, 5)

start()
