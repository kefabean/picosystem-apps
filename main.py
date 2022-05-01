backlight(0)

import os
import math
import time
import gc

battery_level = 100
battery_text = ""
battery_offset = 0
battery_colour = (10, 10, 10)
last_note = 0
note_duration = 0
note_idx = 0
intro_melody = True
spritesheet()
machine_id = machine.unique_id()
if machine_id == b'\xe4`$\xc7C\x0e3*':
    owner = "Thomas"
elif machine_id == b'\xe4`$\xc7C!B*':
    owner = "Josie"
else:
    owner = "Unknown"

notes = [
    (None, 50), ("G6", 5), ("E6", 15), ("A6", 5), ("G6", 15), (None, 25), ("B7", 1), ("C7", 1)
]
intro = Voice()
intro.envelope(attack=50, decay=10, sustain=70, release=2000)


files = [
    file for file in os.listdir() if file.endswith(".py") and
    file not in ("main.py", "launcher.py", "sprites.py", "spritesheets.py") and
    not file.startswith("_")
]

if "shapes.py" not in files:
    files.append("shapes")

if "colour.py" not in files:
    files.append("colour")

if "music.py" not in files:
    files.append("music")

if "audio.py" not in files:
    files.append("audio")

if "text.py" not in files:
    files.append("text")

# HACK to add a quick menu item
files.append("__quit__")

filecount = len(files)

target_angle = 0
current_angle = 0
selected = 0
blip = Voice(10, 10, 10, 10, 40, 2)
ding = Voice(5, 5, 100, 500, 0, 0)
ding.effects(reverb=50)
ding.bend(500, 500)


def get_item_angle(index):
    return 360.0 / filecount * index


def update_melody(tick):
    global last_note, note_idx, note_duration, intro_melody
    
    if tick - last_note > note_duration:
        last_note = tick
        note, note_duration = notes[note_idx]
        if note:
            intro.play(note, note_duration * 8)
        note_idx += 1
    if note_idx >= len(notes):
        intro_melody = False


def update(tick):
    global selected, target_angle, battery_level, battery_colour, battery_text, battery_offset
    
    if tick % 1000 == 0:
        battery_level = battery()
        if battery_level < 20:
            battery_colour = (15, 0, 0)
        else:
            battery_colour = (10, 10, 10)
        battery_text = str(battery_level) + "%"
        width, _ = measure(battery_text)
        battery_offset = 26 - width

    if intro_melody:
        update_melody(tick)
    else:
        if pressed(LEFT):
            selected -= 1
            blip.play(1600, 30, 100)

        if pressed(RIGHT):
            selected += 1
            blip.play(1800, 30, 100)

        if pressed(A):
            ding.play(880, 30, 100)
            quit()

        #selected %= filecount
        target_angle = -get_item_angle(selected)

    if tick <= 75:
        backlight(tick)


def draw(tick):
    global current_angle, intro_melody

    pen(0, 0, 0)
    clear()

    if intro_melody:
        pen(15, 15, 15)
        _logo()
        label = "".join(["", "Pi", "co", "Sys", "tem"][0:min(note_idx, 5)])
        label_width, _ = measure(label)
        text(label, int(60 - (label_width / 2)), 90)
        return

    pen(11, 11, 8)
    text("Run file", 40, 15)
    
    # display owner and battery level
    pen(5, 5, 5)
    text(owner, 0,0)
    rect(70 + battery_offset, 0, 20, 8)
    rect(90 + battery_offset, 2, 2, 4)
    text(battery_text, 94 + battery_offset, 1)
    pen(*battery_colour)
    frect(72 + battery_offset, 2, int(16 * battery_level / 100), 4)

    current_angle += (target_angle - current_angle) / 10.0

    for i in range(filecount):
        item_angle = get_item_angle(i) + current_angle

        # add a bounce to the selected sprite
        bounce = 0
        if i == selected%filecount:
            bounce = math.sin(math.radians(item_angle + (time.ticks_ms() / 2.0))) * 10.0 - 10.0

        rx = math.sin(math.radians(item_angle))
        ry = math.cos(math.radians(item_angle))
        x = rx * 45.0
        y = ry * 20.0
        scale = ((ry + 1.0) * 8.0) + 7.0

        sprite(
            #ord(files[i][0]) -97, # sprite number
            i,
            int(60 + x - (scale / 2)),           # x position
            int(55 + y - (scale / 2) + bounce),  # y position
            1, 1,                                # not clear what this does?
            int(scale), int(scale)               # size
        )

    # centre name of file at bottom of screen
    label = files[selected % filecount]
    if label == "__quit__":
        label = "quit"
    label_width, _ = measure(label)
    pen(11, 11, 8)
    frect(int(60 - label_width / 2 - 3), 102 - 3, label_width + 6, 13)
    pen(0, 0, 0)
    text(label, int(60 - (label_width / 2)), 102)


start()  # Will unblock when "quit" is called


__launch_file__ = files[selected % filecount]
for k in locals().keys():
    if k not in ("gc", "__launch_file__"):
        del locals()[k]

gc.collect()
if __launch_file__ != "__quit__":
    __import__(__launch_file__)
