import time

started = False
lap = False
flash = 0
start_time = time.ticks_ms()
current_time = start_time
stopped_time = current_time
stopwatch = ""
fraction = ""

font = {
   '0' : 0b01110100011001110101110011000101110,
   '1' : 0b00100011000010000100001000010001110,
   '2' : 0b01110100010000100110010001000011111,
   '3' : 0b01110100010000100110000011000101110,
   '4' : 0b00010001100101010010111110001000010,
   '5' : 0b11111100001111000001000011000101110,
   '6' : 0b00110010001000011110100011000101110,
   '7' : 0b11111000010001000100010000100001000,
   '8' : 0b01110100011000101110100011000101110,
   '9' : 0b01110100011000101111000010001001100,
   ':' : 0b00000011000110000000011000110000000,
   '.' : 0b00000000000000000000000000110001100,
   'L' : 0b10000100001000010000100001000011111,
   'a' : 0b00000000000111000001011111000101111,
   'p' : 0b00000000001111010001111101000010000
}


def display_message(message, x, y, size, col):
    for count, letter in enumerate(message):
        char_pixels = font[letter]
        for pixel in range(35):
            if (char_pixels & 2**(34 - pixel)):
                pen(*col)
                fcircle(
                    x + size * (pixel % 5) + count * size * 6,
                    y + size * (pixel // 5),
                    (3 * size) // 8
                )

def draw(tick):
    pen(0, 0, 0)
    clear()
    display_message(stopwatch, 4, 40, 4, (15, 0, 0))
    display_message(fraction, 95, 74, 2, (12,0,0))
    if lap and flash:
        display_message("Lap", 4, 20, 2, (12, 0, 0))

def update(tick):
    global start_time, current_time, started, stopwatch, fraction, lap, stopped_time, flash
    flash = (time.ticks_ms() // 500) % 2
    if started and not lap:
        current_time = time.ticks_ms()
    if pressed(A):
        if not started:
            new_current_time = time.ticks_ms()
            start_time = new_current_time - (current_time - start_time)
            current_time = new_current_time
        if started:
            stopped_time = time.ticks_ms()
        started = not started
    if pressed(B):
        if not started and not lap:
            start_time = time.ticks_ms()
            current_time = start_time
            return
        if not started and lap:
            current_time = stopped_time
        lap = not lap
        
    elapsed = current_time - start_time
    elapsed_seconds = elapsed // 1000
    seconds = ("0" + str(elapsed_seconds % 60))[-2:]
    minutes = ("0" + str(elapsed_seconds // 60))[-2:]
    fraction = "." + str((elapsed // 100) % 10)
    stopwatch = f"{minutes}:{seconds}"

start()