#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import _chess_engine as chess_engine
#import pygame as py

import _chess_ai_engine as ai_engine
from _chess_enums import Player

"""Variables"""
WIDTH = HEIGHT = 120  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
#MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [(14,14,14), (5, 5,5)]
human_player = 'w'
row = 0
col = 0
valid_moves = []
running = True
square_selected = ()  # keeps track of the last selected square
player_clicks = []  # keeps track of player clicks (two tuples)
game_over = False

# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    # Load images for the chess pieces
    global images
    for p in Player.PIECES:
        buffer = Buffer(32, 32)
        open("images/" + p + ".16bpp", "rb").readinto(buffer)
        IMAGES[p] = buffer
        #IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(game_state, valid_moves, square_selected):
    # Draw the complete chess board with pieces
    draw_squares()
    highlight_square(game_state, valid_moves, square_selected)
    draw_pieces(game_state)


def draw_squares():
    # Draw the chess board with the alternating two colors
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pen(*color)
            frect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)


def draw_pieces(game_state):
    # Draw the chess pieces onto the board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                blit(
                    IMAGES[piece.get_player() + "_" + piece.get_name()],
                    0, 0, 32, 32, c * SQ_SIZE, r * SQ_SIZE, 16, 16
                )


def highlight_square(game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]
        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            #s = py.Surface((SQ_SIZE, SQ_SIZE))
            #s.set_alpha(100)
            #s.fill(py.Color("blue"))
            pen(0, 0, 15, 7)
            frect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            #screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

            # highlight move squares
            #s.fill(py.Color("green"))
            pen(0, 15, 0, 7)
            for move in valid_moves:
                #blit(s, (move[1] * SQ_SIZE, move[0] * SQ_SIZE))
                frect(move[1] * SQ_SIZE, move[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE)


# def main():
#     # Check for the number of players and the color of the AI
#     human_player = ""
#     while True:
#         try:
#             number_of_players = input("How many players (1 or 2)?\n")
#             if int(number_of_players) == 1:
#                 number_of_players = 1
#                 while True:
#                     human_player = input("What color do you want to play (w or b)?\n")
#                     if human_player is "w" or human_player is "b":
#                         break
#                     else:
#                         print("Enter w or b.\n")
#                 break
#             elif int(number_of_players) == 2:
#                 number_of_players = 2
#                 break
#             else:
#                 print("Enter 1 or 2.\n")
#         except ValueError:
#             print("Enter 1 or 2.")

def update(tick):
    global human_player, row, col, ai, game_state, valid_moves, square_selected, player_clicks, running, game_over
    #py.init()
    #screen = py.display.set_mode((WIDTH, HEIGHT))
    #clock = py.time.Clock()
    #game_state = chess_engine.game_state()
    if human_player is 'b':
        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
        game_state.move_piece(ai_move[0], ai_move[1], True)

    if pressed(DOWN):
        if row < DIMENSION:
            row += 1
    if pressed(UP):
        if row > 0:
         row -= 1
    if pressed(LEFT):
        if col > 0:
            col -= 1
    if pressed(RIGHT):
        if col < DIMENSION:
            col += 1
    if pressed(A):
        if square_selected == (row, col):
            square_selected = ()
            player_clicks = []
        else:
            square_selected = (row, col)
            player_clicks.append(square_selected)
    #while running:
    #    for e in py.event.get():
    #        if e.type == py.QUIT:
    #            running = False
    #        elif e.type == py.MOUSEBUTTONDOWN:
    #            if not game_over:
    #                location = py.mouse.get_pos()
    #                col = location[0] // SQ_SIZE
    #                row = location[1] // SQ_SIZE
    #                if square_selected == (row, col):
    #                    square_selected = ()
    #                    player_clicks = []
    #                else:
    #                    square_selected = (row, col)
    #                    player_clicks.append(square_selected)
            if len(player_clicks) == 2:
                # this if is useless right now
                if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []
                else:
                    game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                          (player_clicks[1][0], player_clicks[1][1]), False)
                    square_selected = ()
                    player_clicks = []
                    valid_moves = []

                    if human_player is 'w':
                        ai_move = ai.minimax_white(game_state, 3, -100000, 100000, True, Player.PLAYER_2)
                        game_state.move_piece(ai_move[0], ai_move[1], True)
                    elif human_player is 'b':
                        ai_move = ai.minimax_black(game_state, 3, -100000, 100000, True, Player.PLAYER_1)
                        game_state.move_piece(ai_move[0], ai_move[1], True)
            else:
                valid_moves = game_state.get_valid_moves((row, col))
                if valid_moves is None:
                    valid_moves = []
    if pressed(X):
        game_over = False
        game_state = chess_engine.game_state()
        valid_moves = []
        square_selected = ()
        player_clicks = []
        valid_moves = []
    if pressed(B):
        game_state.undo_move()
        print(len(game_state.move_log))


def draw(tick):

        draw_game_state(game_state, valid_moves, square_selected)

        endgame = game_state.checkmate_stalemate_checker()
        if endgame == 0:
            game_over = True
            text("Black wins.", 0, 0)
        elif endgame == 1:
            game_over = True
            text("White wins.", 0, 0)
        elif endgame == 2:
            game_over = True
            text("Stalemate.", 0, 0)

 #       clock.tick(MAX_FPS)
 #       py.display.flip()



#def draw_text(screen, text):
#    font = py.font.SysFont("Helvitca", 32, True, False)
#    text_object = font.render(text, False, py.Color("Black"))
#    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
#                                                      HEIGHT / 2 - text_object.get_height() / 2)
#    screen.blit(text_object, text_location)


#if __name__ == "__main__":
#    main()
load_images()
ai = ai_engine.chess_ai()
game_state = chess_engine.game_state()
start()