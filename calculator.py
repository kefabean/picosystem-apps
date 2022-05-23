import math
from _font import big_text

KEYS_ACROSS = 4
H_SIZE = 24
V_SIZE = 16
KEYPAD = [
   'C', '±', '√', 'π',
   '7', '8', '9', '*',
   '4', '5', '6', '/',
   '1', '2', '3', '-',
   '0', '.', '=', '+'
]

cursor = 0
current = ''
register = ''
operator = ''


def draw_button(x, y, key):
   if KEYPAD[key] in 'C±√π':
       button_col = (11,11,11)
       text_col = (0,0,0)
   elif KEYPAD[key] in '+-*/':
       if KEYPAD[key] == operator:
           button_col = (12,12,12)
           text_col = (8,4,0)
       else:
           button_col = (11,9,0)
           text_col = (14,14,14)
   else:
       button_col = (2,2,2)
       text_col = (13,13,13)
   pen(*button_col)
   frect(x, y, H_SIZE, V_SIZE)
   if cursor == key:
      pen(15, 5, 5, 8)
      frect(x, y, H_SIZE, V_SIZE)
   pen(*text_col)
   big_text(KEYPAD[key], x + H_SIZE // 2 - 4 , y + 1, V_SIZE // 8)

def draw_keypad():
   for key in range(len(KEYPAD)):
      draw_button(
         15 + int((key %  KEYS_ACROSS) * (H_SIZE + 2)),
         30 + int((key // KEYS_ACROSS) * (V_SIZE + 2)),
         key
      )
      
def draw_result():
    pen(13,13,13)
    if register != '' and current == '':
        text = register
    else:
        text = current
    if len(text) > 12:
        text = "{:E}".format(eval(text))
    elif text == '':
        text = '0.'
    elif '.' not in text:
        text += '.'
    big_text(text, 120, 10, V_SIZE // 16, right_align = True)

def draw(tick):
    pen(0,0,0)
    clear()
    draw_keypad()
    draw_result()

def update(tick):
   global cursor, current, register, operator
   if pressed(UP):
      if cursor > (KEYS_ACROSS - 1):
         cursor = cursor - KEYS_ACROSS
   if pressed(DOWN):
      if cursor < (len(KEYPAD) - KEYS_ACROSS):
         cursor = cursor + KEYS_ACROSS
   if pressed(RIGHT):
      if ((cursor + 1) % KEYS_ACROSS) > (cursor % KEYS_ACROSS):
         cursor += 1
   if pressed(LEFT):
      if ((cursor - 1) % KEYS_ACROSS) < (cursor % KEYS_ACROSS):
         cursor -= 1
   if pressed(A):
       button = KEYPAD[cursor]
       if button in '0123456789' and len(current) < 12:
           current += button
       if button == 'C':
           current = ''
           register = ''
           operator = ''
       if button == '.' and button not in current:
           current += button
       if button == '±':
           current = str(eval("-"+current))
       if button == 'π':
           if register == '':
             register = str(math.pi)
           else:
             current = str(math.pi)
       if button == '√':
           current = str(math.sqrt(eval(current)))
       if button in '+*/-':
           if button == operator:
               operator = ''
           else:
               operator = button
           if register == '':
               register = current
               current = ''
       if button == '=':
           if register != '' and operator != '' and current != '':
              register = str(eval(register + operator + current))
              operator = ''
              current = ''

start()