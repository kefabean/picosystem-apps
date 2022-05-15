import json


blip = Voice(10, 10, 10, 10, 40, 2)
lose = Voice(10, 10, 10, 40, -2, 10, 100, 100)


class Button:

    def __init__(self, message, x, y, func, size = 10, col = (5, 5, 10)):
        self.x = x
        self.y = y
        self.message = message
        self.func = func
        self.col = col
        self.size = size
        
    def draw(self, is_selected):
        pen(*self.col)
        if is_selected:
            frect(self.x, self.y, self.size, 12)
            pen(0, 0, 0)
        else:
            rect(self.x, self.y, self.size, 12)
        text(self.message, self.x + 2, self.y + 2)
            
    def update(self):
        if pressed(A):
            blip.play(500, 120, 100)
            self.func(self.message)


class Leaderboard:

    letters = '1234567890-abcedfghihjklmnopqrstuvwxyz,.:? '
    titles  = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']

    def __init__(self, game, game_name):
        self.game = game
        self.game_name = game_name
        try:
            with open(f"{game_name}_leaderboard.json",'r') as fh:
               scores = json.load(fh)
        except:
            scores = [
                {'name':'hermione', 'score':500},
                {'name':'harry', 'score':200},
                {'name':'ron', 'score':100},
                {'name':'dumbledore', 'score':50},
                {'name':'malfoy', 'score':20},
                {'name':'hagrid', 'score':10},
                {'name':'snape', 'score':5},
                {'name':'dobby', 'score':2}
            ]
        self.scores = scores
        self.button_index = 0
        self.buttons = [
            Button(
                char,
                11 * (count % 11),
                55 + 13 * (count // 11),
                self.add_char
            ) for count, char in enumerate(self.letters)
        ]
        self.buttons.append(
            Button("<", 11 * 10,  55 + 13 * 3, self.backspace)
        )
        self.buttons.append(
            Button("OK", 82, 108, self.add_score, size = 38, col = (0,12,5))
        )
        self.name = ""

    def backspace(self, char):
        self.name = self.name[:-1]
        
    def add_char(self, char):
        if len(self.name) > 13:
            lose.play(1200, 180, 100)
        else:
            self.name += char

    def add_score(self, char):
        scores = self.scores
        scores.append({'name':self.name, 'score': self.game.score})
        scores.sort(key = lambda item:item['score'], reverse = True)
        self.scores = scores[0:len(self.titles)]
        with open(f"{self.game_name}_leaderboard.json",'w') as fh:
           json.dump(self.scores, fh)
        self.game.state = "leaderboard"

    def draw_leaderboard(self, tick):
        pen(0,15,0)
        text("Hall of fame", 30, 10)
        for count, s in enumerate(self.scores):
            score = str(self.scores[count]['score'])
            align, _ = measure(score)
            pen(15, 15, 15)
            text(Leaderboard.titles[count], 0, count * 10 + 24)
            text(self.scores[count]['name'], 30, count * 10 + 24)
            text(str(self.scores[count]['score']), 120 - align, count * 10 + 24)
        text("Press Y to play", 25, 110)

    def draw_name_entry(self, tick):
        for count, b in enumerate(self.buttons):
            b.draw(count == self.button_index)
        pen(0, 15, 0)
        text("New high score", 23, 0)
        pen(5, 5, 10)
        text("Enter your name:", 0, 15)
        pen(5, 15, 5)
        if tick // 10 % 2 == 0:
            cursor = "|"
        else:
            cursor = " "
        text(self.name + cursor, 1, 34, 120)
        
    def draw(self, tick):
        alpha(8)
        pen(0,0,0)
        clear()
        alpha()
        if self.game.state == "gameover":
            pen(15, 0, 0)
            text("GAME OVER!", 35, 40)
            pen(10,10,10)
            text("Press Y to continue", 15, 60)
        if self.game.state == "nameentry":
            self.draw_name_entry(tick)
        if self.game.state == "leaderboard":
            self.draw_leaderboard(tick)

    def update(self, game):
        self.game = game
        if game.state == "leaderboard":
            if pressed(Y):
                game.__init__()
            if pressed(X):
                machine.reset()
        if game.state == "gameover":
            if pressed(Y):
                if game.score > self.scores[-1]['score']:
                    game.state = "nameentry"
                else:
                    game.state = "leaderboard"
        if game.state == "nameentry":
            self.buttons[self.button_index].update()
            if pressed(LEFT):
                if self.button_index > 0:
                    self.button_index -= 1
                    blip.play(1600, 30, 100)
            if pressed(RIGHT):
                if self.button_index < (len(self.buttons) - 1):
                    self.button_index += 1
                    blip.play(1800, 30, 100)
            if pressed(UP):
                if self.button_index > 10:
                    self.button_index -= 11
                    blip.play(1600, 30, 100)
            if pressed(DOWN):
                if (len(self.buttons) - self.button_index) > 11:
                    blip.play(1800, 30, 100)
                    self.button_index += 11
                else:
                    self.button_index = len(self.buttons) - 1
