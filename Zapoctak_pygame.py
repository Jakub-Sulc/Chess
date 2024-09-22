import pygame
import chess
import chess.engine
import requests
import random

pygame.init()         #for pygame to be working

#atributes and values
width = 1000
height = 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Game of chess")
timer = pygame.time.Clock()
fps = 60


#chess pieces and their positions 
white_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
white_pieces_position = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
black_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
black_pieces_position = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
captured_white_pieces = []
captured_black_pieces = []
turn_step = 0               # 0 - white is on turn no selected, 1 - white is on turn piece selected, 2 - black is on turn no selected, 3 - black is on turn piece selected
selection = 100

# load ingame pieces, images
black_queen = pygame.image.load("Zapoctak/black_queen.svg.png")
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_king = pygame.image.load("Zapoctak/black_king.svg.png")
black_king = pygame.transform.scale(black_king, (80, 80))
black_rook = pygame.image.load("Zapoctak/black_rook.svg.png")
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_bishop = pygame.image.load("Zapoctak/black_bishop.svg.png")
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_knight = pygame.image.load("Zapoctak/black_knight.svg.png")
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_pawn = pygame.image.load("Zapoctak/black_pawn.svg.png")
black_pawn = pygame.transform.scale(black_pawn, (80, 80))

white_queen = pygame.image.load("Zapoctak/white_queen.svg.png")
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_king = pygame.image.load("Zapoctak/white_king.svg.png")
white_king = pygame.transform.scale(white_king, (80, 80))
white_rook = pygame.image.load("Zapoctak/white_rook.svg.png")
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_bishop = pygame.image.load("Zapoctak/white_bishop.svg.png")
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_knight = pygame.image.load("Zapoctak/white_knight.svg.png")
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_pawn = pygame.image.load("Zapoctak/white_pawn.svg.png")
white_pawn = pygame.transform.scale(white_pawn, (80, 80))

promote_black_queen = black_queen
promote_black_rook = black_rook
promote_black_bishop = black_bishop
promote_black_knight = black_knight

promote_white_queen = white_queen
promote_white_rook = white_rook
promote_white_bishop = white_bishop
promote_white_knight = white_knight

white_images = [white_pawn, white_knight, white_bishop, white_rook, white_king, white_queen]
black_images = [black_pawn, black_knight, black_bishop, black_rook, black_king, black_queen]

#star images
star_filled = pygame.image.load("Zapoctak/star_filled.jpg")
star_filled = pygame.transform.scale(star_filled, (50, 50))
star_empty = pygame.image.load("Zapoctak/Star_empty.png")
star_empty = pygame.transform.scale(star_empty, (55, 55))

piece_list = ["pawn", "knight", "bishop", "rook", "king", "queen"]

# taking chessboard from chess library
board = chess.Board()

def start_screen():
    font1 = pygame.font.SysFont(None, 128)
    font2 = pygame.font.SysFont(None, 56)
    screen.blit(font1.render("Choose Colour", True, "black"), (180, 100))
    black_button = pygame.Surface((150, 150))
    black_button.fill("black")
    white_button = pygame.Surface((150, 150))
    white_button.fill("white")
    screen.blit(black_button, (270, 220))
    screen.blit(white_button, (590, 220))
    screen.blit(font1.render("Choose Opponent", True, "black"), (100, 450))
    noob_button = pygame.Surface((300, 75))
    noob_button.fill("pink")
    noob_button.blit(font2.render("Noob", True, "black"), (90, 20))
    professional_button = pygame.Surface((300, 75))
    professional_button.fill("pink")
    professional_button.blit(font2.render("Professional", True, "black"), (38, 20))
    screen.blit(noob_button, (150, 570))
    screen.blit(professional_button, (550, 570))

# drawing a chessboard
def draw_board():
    for i in range(32):
        column = i%4
        row = i//4
        if row % 2 == 0:
            pygame.draw.rect(screen, "light gray", [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, "light gray", [700 - (column * 200), row * 100, 100, 100])

# drawing chess pieces    
def draw_pieces():
    for i in range(len(white_pieces)):
        j = piece_list.index(white_pieces[i])
        screen.blit(white_images[j], (white_pieces_position[i][0]*100 + 10, white_pieces_position[i][1]*100 + 10))


    for i in range(len(black_pieces)):
        j = piece_list.index(black_pieces[i])   
        screen.blit(black_images[j], (black_pieces_position[i][0]*100 + 10, black_pieces_position[i][1]*100 + 10))

def resign_button():
    resign_surface = pygame.Surface((150, 100))
    resign_surface.fill("red")
    font1 = pygame.font.SysFont(None, 56)
    resign_surface.blit(font1.render("Resign", True, "black"), (12, 30))
    screen.blit(resign_surface, (825, 350))
    pygame.draw.rect(screen, "dark red", [825, 350, 150, 100], 5)

def evaluation_button():
    evaluation_surface = pygame.Surface((150, 100))
    evaluation_surface.fill("green")
    font2 = pygame.font.SysFont(None, 36)
    evaluation_surface.blit(font2.render("Evaluation", True, "black"), (12, 37))
    screen.blit(evaluation_surface, (825, 200))
    pygame.draw.rect(screen, "dark green", [825, 200, 150, 100], 5)

    evaluation_number_surface = pygame.Surface((150, 100))
    evaluation_number_surface.fill("gray")
    screen.blit(evaluation_number_surface, (825, 50))
    pygame.draw.rect(screen, "pink", [825, 50, 150, 100], 5)

def best_move_button():
    evaluation_surface = pygame.Surface((150, 100))
    evaluation_surface.fill("green")
    font2 = pygame.font.SysFont(None, 36)
    evaluation_surface.blit(font2.render("Best Move", True, "black"), (12, 37))
    screen.blit(evaluation_surface, (825, 500))
    pygame.draw.rect(screen, "dark green", [825, 500, 150, 100], 5)

    evaluation_number_surface = pygame.Surface((150, 100))
    evaluation_number_surface.fill("gray")
    screen.blit(evaluation_number_surface, (825, 650))
    pygame.draw.rect(screen, "pink", [825, 650, 150, 100], 5)

def write_eval(eval):
    if eval is not None:
        if isinstance(eval, str):
            font1 = pygame.font.SysFont(None, 40)
            screen.blit(font1.render(eval, True, "black"), (842, 90))
        else:
            font1 = pygame.font.SysFont(None, 56)
            pawn_score = eval / 100
            screen.blit(font1.render(str(pawn_score), True, "black"), (862, 80))

def write_best_move(best_move):
    font1 = pygame.font.SysFont(None, 56)
    screen.blit(font1.render(str(best_move), True, "black"), (860, 680))

def draw_promotion_menu(black_turn):
    menu_surface = pygame.Surface((400, 100))
    menu_surface.fill((200, 200, 200))

    if black_turn:
        piece_images = [promote_white_queen, promote_white_rook, promote_white_bishop, promote_white_knight]
    else:
        piece_images = [promote_black_queen, promote_black_rook, promote_black_bishop, promote_black_knight]

    piece_types = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    piece_buttons = []
    
    for i, image in enumerate(piece_images):
        menu_surface.blit(image, (i * 100 + 10, 10))
        piece_buttons.append(pygame.Rect(i * 100, 0, 100, 100))

    for i in range(1, 4):
        pygame.draw.line(menu_surface, (0, 0, 0), (i * 100, 0), (i * 100, 100), 5)

    screen.blit(menu_surface, (300, 350))
    pygame.display.update()

    return piece_buttons, piece_types

def handle_promotion_choice(piece_buttons, piece_types):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, rect in enumerate(piece_buttons):
                    if rect.collidepoint(x - 300, y - 350):
                        return piece_types[i]
        pygame.display.update()

# transfering coordinates from our board to the one form chess library
def position_to_square(a, b):
    file = a
    rank = 7 - b
    return chess.square(file, rank)

def square_to_position(square):
    file = chess.square_file(square)
    rank = 7 - chess.square_rank(square)
    return file*100, rank*100

def square_to_coordinates(square):
    file = square % 8
    rank = square // 8
    return file, 7 - rank

def highlight_valid_moves(valid_moves):
    for j in valid_moves:
        x, y = square_to_position(j.to_square)
        pygame.draw.circle(screen, "green", (x + 50, y + 50), 15)

def update_piece_position(start_square, end_square, black_turn):            #we ask about black_turn, because white has already made the move, but we have move the image of the piece
    start_position = square_to_coordinates(start_square)
    end_position = square_to_coordinates(end_square)
    captured_piece = board.piece_at(end_square)
       
    if captured_piece:
        if black_turn:
            for i, position in enumerate(white_pieces_position):
                if position == end_position:
                    white_pieces_position[i] = (9,9)
                    break

        else:
            for i, position in enumerate(black_pieces_position):
                if position == end_position:
                    black_pieces_position[i] = (9,9)
                    break
    
    if black_turn:
        if start_position == (4, 0) and end_position == (6, 0) and start_position == black_pieces_position[4]:
            black_pieces_position[4] = end_position
            black_pieces_position[7] = (5, 0)
        elif start_position == (4, 0) and end_position == (2, 0) and start_position == black_pieces_position[4]:
            black_pieces_position[4] = end_position
            black_pieces_position[0] = (3, 0)
        else:
            for i, position in enumerate(black_pieces_position):
                if position == start_position:
                    black_pieces_position[i] = end_position
                    break
    else:
        if start_position == (4, 7) and end_position == (6, 7) and start_position == white_pieces_position[4]:
            white_pieces_position[4] = end_position
            white_pieces_position[7] = (5, 7)
        elif start_position == (4, 7) and end_position == (2, 7) and start_position == white_pieces_position[4]:
            white_pieces_position[4] = end_position
            white_pieces_position[0] = (3, 7)
        else:
            for i, position in enumerate(white_pieces_position):
                if position == start_position:
                    white_pieces_position[i] = end_position
                    break

def update_pieces_en_passant(start_square, end_square, black_turn):
    start_position = square_to_coordinates(start_square)
    end_position = square_to_coordinates(end_square)

    if black_turn:
        for i, position in enumerate(white_pieces_position):
            if position == (end_position[0], end_position[1] - 1):
                white_pieces_position[i] = (9,9)
                break
        for i, position in enumerate(black_pieces_position):
            if position == start_position:
                black_pieces_position[i] = end_position
                break            
    
    else:
        for i, position in enumerate(black_pieces_position):
            if position == (end_position[0], end_position[1] + 1):
                black_pieces_position[i] = (9,9)
                break
        for i, position in enumerate(white_pieces_position):
            if position == start_position:
                white_pieces_position[i] = end_position
                break

def check_promotion(start_square, end_square, white_turn):
    start_position = square_to_coordinates(start_square)
    end_position = square_to_coordinates(end_square)
    piece = board.piece_at(start_square)
    if piece.piece_type == chess.PAWN:
        if white_turn and end_position[1] == 0 and start_position[1] == 1:
            for position in black_pieces_position:
                if start_position[0] == end_position[0] and end_position not in black_pieces_position:
                    return True
                elif start_position[0] == end_position[0] - 1 and position == end_position:
                    return True
                elif start_position[0] == end_position[0] + 1 and position == end_position:
                    return True
        elif not white_turn and end_position[1] == 7 and start_position[1] == 6:
            for i, position in enumerate(white_pieces_position):
                if start_position[0] == end_position[0] and end_position not in white_pieces_position:
                    return True
                elif start_position[0] == end_position[0] - 1 and position == end_position:
                    return True
                elif start_position[0] == end_position[0] + 1 and position == end_position:
                    return True              
       
def update_pieces_promotion(start_square, end_square, black_turn, promotion_piece):
    start_position = square_to_coordinates(start_square)
    end_position = square_to_coordinates(end_square)
    captured_piece = board.piece_at(end_square)

    if captured_piece:
        if black_turn:
            for i, position in enumerate(white_pieces_position):
                if position == end_position:
                    white_pieces_position[i] = (9,9)
                    break

        else:
            for i, position in enumerate(black_pieces_position):
                if position == end_position:
                    black_pieces_position[i] = (9,9)
                    break
    if black_turn:
        for i, position in enumerate(black_pieces_position):
            if position == start_position:
                black_pieces_position[i] = end_position
                if promotion_piece == chess.QUEEN:
                    black_pieces[i] = "queen"
                elif promotion_piece == chess.ROOK:
                    black_pieces[i] = "rook"
                elif promotion_piece == chess.BISHOP:
                    black_pieces[i] = "bishop"
                elif promotion_piece == chess.KNIGHT:
                    black_pieces[i] = "knight"    
                break
        
    else:        
        
        for i, position in enumerate(white_pieces_position):
            if position == start_position:
                white_pieces_position[i] = end_position
                if promotion_piece == chess.QUEEN:
                   white_pieces[i] = "queen"
                elif promotion_piece == chess.ROOK:
                   white_pieces[i] = "rook"
                elif promotion_piece == chess.BISHOP:
                   white_pieces[i] = "bishop"
                elif promotion_piece == chess.KNIGHT:
                   white_pieces[i] = "knight"    
                break

"""
def check_promotion_stockfish(end_square, moving_piece):
    #piece = board.piece_at(end_square)
    #if moving_piece == 1 or moving_piece == 2 or moving_piece == 3 or moving_piece == 4 or moving_piece == 5:
        #if moving_piece != piece:
    True
"""

def win(black_turn):
    global end
    if board.is_checkmate() and player_colour != black_turn:
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        screen.blit(font1.render("You Won", True, "black"), (315, 425))
        if points == 0:
            screen.blit(star_filled, (315, 350))
            screen.blit(star_filled, (375, 320))
            screen.blit(star_filled, (435, 350))
            pygame.draw.rect(screen, "green", (300, 530, 200, 70))
            pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
            font2 = pygame.font.SysFont(None, 45)
            screen.blit(font2.render("Play Again", True, "black"), (322, 550))
            end = 1

        elif points < 4:
            screen.blit(star_empty, (315, 350))
            screen.blit(star_filled, (375, 320))
            screen.blit(star_filled, (435, 350))
            pygame.draw.rect(screen, "green", (300, 530, 200, 70))
            pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
            font2 = pygame.font.SysFont(None, 45)
            screen.blit(font2.render("Play Again", True, "black"), (322, 550))
            end = 1

        else:
            screen.blit(star_empty, (315, 350))
            screen.blit(star_empty, (375, 320))
            screen.blit(star_filled, (435, 350))
            pygame.draw.rect(screen, "green", (300, 530, 200, 70))
            pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
            font2 = pygame.font.SysFont(None, 45)
            screen.blit(font2.render("Play Again", True, "black"), (322, 550))
            end = 1

    

def draw():
    global end
    if board.is_stalemate():
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("Draw", True, "black"), (355, 425))
        screen.blit(font2.render("by Stalemate", True, "black"), (330, 350))
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1

    elif board.is_insufficient_material():
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("Draw", True, "black"), (355, 425))
        screen.blit(font2.render("by Insufficient", True, "black"), (315, 330))
        screen.blit(font2.render("material", True, "black"), (355, 370))
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1

    elif board.is_repetition():
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("Draw", True, "black"), (355, 425))
        screen.blit(font2.render("by Threefold", True, "black"), (325, 330))
        screen.blit(font2.render("repetition", True, "black"), (340, 370))
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1 

    elif board.is_fifty_moves():
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("Draw", True, "black"), (355, 425))
        screen.blit(font2.render("by Fifty moves", True, "black"), (315, 330))
        screen.blit(font2.render("rule", True, "black"), (375, 370))
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1


def lose(black_turn):
    global end
    if resign == 1:
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("You Lost", True, "black"), (320, 425))
        screen.blit(font2.render("by Resignation", True, "black"), (312, 350))
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1

    elif board.is_checkmate() and player_colour == black_turn:
        pygame.draw.rect(screen, "white", (300, 300, 200, 200))
        pygame.draw.rect(screen, "dark green", [300, 300, 200, 200], 5)
        font1 = pygame.font.SysFont(None, 56)
        font2 = pygame.font.SysFont(None, 36)
        screen.blit(font1.render("You Lost", True, "black"), (320, 425))
        screen.blit(font2.render("by Checkmate", True, "black"), (318, 350))  
        pygame.draw.rect(screen, "green", (300, 530, 200, 70))
        pygame.draw.rect(screen, "dark green", [300, 530, 200, 70], 5)
        font2 = pygame.font.SysFont(None, 45)
        screen.blit(font2.render("Play Again", True, "black"), (322, 550))
        end = 1

"""   
def evaluation_engine(fen):
    url = "https://lichess.org/api/cloud-eval"
    params = {
        'fen': fen,
        'multiPv': 1,  # Number of lines to analyze
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            
            if "pvs" in data:
                evaluation = data['pvs'][0]
                
                if 'cp' in evaluation:  
                    return evaluation['cp']  
                elif 'mate' in evaluation:  
                    return f"mate {evaluation['mate']}"  
                else:
                    return None  
            else:
                return None
        except ValueError:
            return None
    else:
        return None
    
def best_move_engine(fen):
    url = "https://lichess.org/api/cloud-eval"
    params = {
        'fen': fen,
        'multiPv': 1,  # Number of lines to analyze
    }
    response = requests.get(url, params=params)

    
    if response.status_code == 200:
        try:
            data = response.json()
            
            if "pvs" in data:
                best_move = data['pvs'][0]['moves'].split()[0]
                return best_move
            else:
                return None
        except ValueError:
            return None
    else:
        return None
"""    

def best_move_stockfish(fen):
    engine = chess.engine.SimpleEngine.popen_uci("Zapoctak/stockfish/stockfish-windows-x86-64-avx2.exe")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=0.7))
    best_move = info['pv'][0]
    engine.quit()
    return best_move

def evaluation_stockfish(fen):
    engine = chess.engine.SimpleEngine.popen_uci("Zapoctak/stockfish/stockfish-windows-x86-64-avx2.exe")
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time=0.7))
    eval = info['score'].relative
    engine.quit()
    if eval.is_mate():
        if board.turn == chess.BLACK:
            eval_result = f"Mate in -{eval.mate()}"
        else:
            eval_result = f"Mate in {eval.mate()}"
    else:
        eval_result = eval.score()
        if board.turn == chess.BLACK:
            eval_result = -eval_result
    return eval_result
    
def noob_evaluation(fen):
    score = 0
    pieces_on_board = fen.split()[0]
    for i in pieces_on_board:
        if i == "P":
            score += 1
        elif i == "N":
            score += 3
        elif i == "B":
            score += 3
        elif i == "R":
            score += 5
        elif i == "Q":
            score += 10
        elif i == "p":
            score -= 1
        elif i == "n":
            score -= 3
        elif i == "b":
            score -= 3
        elif i == "r":
            score -= 5
        elif i == "q":
            score -= 10
    return score

def noob_best_move(black_turn, half_moves, noob_move, list_of_best_moves = None, evaluation_of_best_moves = None):
    if list_of_best_moves is None:
        list_of_best_moves = []
    if evaluation_of_best_moves is None:
        evaluation_of_best_moves = []
    half_moves += 1
    best_evaluation = None
    best_move = None
    checkmate_move = None
    number_of_tried_moves = 0
    legal_moves = list(board.legal_moves)
    total_moves = len(legal_moves)
    if half_moves == 1:
        for move in board.legal_moves:
            number_of_tried_moves += 1
            board.push(move)
            noob_move = move
            if board.is_game_over():
                checkmate_move = move
                board.pop()
                break
            else:
                noob_best_move(black_turn, half_moves, noob_move, list_of_best_moves, evaluation_of_best_moves)
            board.pop()
    elif half_moves == 2:
        for opponent_move in board.legal_moves:
            board.push(opponent_move)
            fen = board.fen()
            evaluation = noob_evaluation(fen)
            if best_evaluation == None:
                best_evaluation = evaluation
                best_move = noob_move
            elif black_turn:
                if evaluation < best_evaluation:
                    best_move = noob_move
                    best_evaluation = evaluation
            else:
                if evaluation > best_evaluation:
                    best_move = noob_move
                    best_evaluation = evaluation
            board.pop()
    if half_moves == 2:
        list_of_best_moves.append(best_move)
        evaluation_of_best_moves.append(best_evaluation)
    if half_moves == 1:
        if checkmate_move is not None:
            return checkmate_move
        elif number_of_tried_moves == total_moves:
            if black_turn:
                greatest_eval = max(evaluation_of_best_moves)
            else:
                greatest_eval = min(evaluation_of_best_moves)
            best_noob_moves = [m for i, m in enumerate(list_of_best_moves) if evaluation_of_best_moves[i] == greatest_eval]
            chosen_move = random.choice(best_noob_moves)
            return chosen_move
            

        

    
list_of_best_moves = []
evaluation_of_best_moves = []
player_colour = None
opponent = None
selected_square = None
run = True
valid_moves = []
points = 0
resign = 0
end = 0
eval = None
best_move = None
player_has_moved = False
while run:
    timer.tick(fps)
    screen.fill("dark grey")


    if player_colour is not None and opponent is not None:
        if end == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 300 <= x <= 500 and 530 <= y <= 600:
                        player_colour = None
                        opponent = None
                        selected_square = None
                        valid_moves = []
                        points = 0
                        resign = 0
                        end = 0
                        eval = None
                        best_move = None
                        player_has_moved = False
                        board = chess.Board()
                        white_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
                        white_pieces_position = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                        black_pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]
                        black_pieces_position = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                        start_screen()

        if player_colour == chess.BLACK:
            player_has_moved = True    
        draw_board()
        draw_pieces()
        resign_button()
        evaluation_button()
        best_move_button()
        win(board.turn)
        draw()
        lose(board.turn)

        

        

        if not board.is_game_over():    
            if player_has_moved and board.turn != player_colour:
                if opponent == "professional":
                    fen = board.fen()
                    professional_move = best_move_stockfish(fen)
                    moving_piece = board.piece_at(professional_move.from_square).piece_type
                    en_passant_square = board.ep_square #idk zdali dobře
                    board.push(professional_move)
                    
                    if moving_piece == 1 and en_passant_square == board.peek().to_square:
                        update_pieces_en_passant(board.peek().from_square, board.peek().to_square, board.turn) #tady musím překopat pro stockfishe
                    elif moving_piece == 1 and board.piece_at(board.peek().to_square).piece_type != moving_piece: 
                        promotion_piece = board.piece_at(board.peek().to_square).piece_type
                        if promotion_piece == 2:
                            promotion_piece = chess.KNIGHT
                        elif promotion_piece == 3:
                            promotion_piece = chess.BISHOP
                        elif promotion_piece == 4:
                            promotion_piece = chess.ROOK
                        elif promotion_piece == 5:
                            promotion_piece = chess.QUEEN
                        update_pieces_promotion(board.peek().from_square, board.peek().to_square, board.turn, promotion_piece)
                    
                    else:
                        update_piece_position(board.peek().from_square, board.peek().to_square, board.turn)
                    
                    player_has_moved = False

                
                elif opponent == "noob":
                    noob_move = noob_best_move(board.turn, 0, None, None, None)
                    moving_piece = board.piece_at(noob_move.from_square).piece_type
                    en_passant_square = board.ep_square
                    board.push(noob_move)
                    if moving_piece == 1 and en_passant_square == board.peek().to_square:
                        update_pieces_en_passant(board.peek().from_square, board.peek().to_square, board.turn) #tady musím překopat pro stockfishe
                    elif moving_piece == 1 and board.piece_at(board.peek().to_square).piece_type != moving_piece: 
                        promotion_piece = board.piece_at(board.peek().to_square).piece_type
                        if promotion_piece == 2:
                            promotion_piece = chess.KNIGHT
                        elif promotion_piece == 3:
                            promotion_piece = chess.BISHOP
                        elif promotion_piece == 4:
                            promotion_piece = chess.ROOK
                        elif promotion_piece == 5:
                            promotion_piece = chess.QUEEN
                        update_pieces_promotion(board.peek().from_square, board.peek().to_square, board.turn, promotion_piece)
                    
                    else:
                        update_piece_position(board.peek().from_square, board.peek().to_square, board.turn)
                    
                    player_has_moved = False
                    noob_move = None
                    print(end)

            else:
            #event handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.MOUSEBUTTONDOWN and board.turn == player_colour:
                        x, y = pygame.mouse.get_pos()
                        if 825 <= x <= 975 and 200 <= y <= 300:
                            fen = board.fen()
                            points += 1
                            if eval != None: 
                                pygame.draw.rect(screen, "gray", [825, 50, 150, 100])
                                pygame.draw.rect(screen, "pink", [825, 50, 150, 100], 5)
                            eval = evaluation_stockfish(fen)
                            write_eval(eval)
                        elif 825 <= x <= 975 and 350 <= y <= 450:
                            resign = 1
                        elif 825 <= x <= 975 and 500 <= y <= 600:
                            fen = board.fen()
                            points += 2
                            if best_move != None: 
                                pygame.draw.rect(screen, "gray", [825, 650, 150, 100])
                                pygame.draw.rect(screen, "pink", [825, 650, 150, 100], 5)
                            best_move = board.san(best_move_stockfish(fen)) 
                            write_best_move(best_move)

                        else:
                            file = x//100
                            rank = y//100
                            clicked_square = position_to_square(file, rank) 

                            if selected_square == None:
                                piece = board.piece_at(clicked_square)
                                if piece:
                                    selected_square = clicked_square
                                    valid_moves = [move for move in board.legal_moves if move.from_square == selected_square]
                            else:
                                move = chess.Move(selected_square, clicked_square)
                                if check_promotion(selected_square, clicked_square, board.turn):
                                        piece_buttons, piece_types = draw_promotion_menu(board.turn)
                                        promotion_piece = handle_promotion_choice(piece_buttons, piece_types)
                                        move.promotion = promotion_piece
                                if move in valid_moves:
                                    if board.piece_at(selected_square).piece_type == chess.PAWN and board.ep_square and board.ep_square == clicked_square:
                                        board.push(move)
                                        update_pieces_en_passant(selected_square, clicked_square, board.turn)

                                    elif check_promotion(selected_square, clicked_square, board.turn):
                                        board.push(move)
                                        update_pieces_promotion(selected_square, clicked_square, board.turn, promotion_piece)

                                    else:    
                                        board.push(move)
                                        update_piece_position(selected_square, clicked_square, board.turn)
                                selected_square = None
                                valid_moves = []
                                player_has_moved = True
                                print(end)
                if eval is not None:
                    write_eval(eval)
                if best_move is not None:
                    write_best_move(best_move)    
                highlight_valid_moves(valid_moves)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    else:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 270 <= x <= 420 and 220 <= y <= 370:
                    player_colour = chess.BLACK
                elif 590 <= x <= 740 and 220 <= y <= 370:
                    player_colour = chess.WHITE
                if 150 <= x <= 450 and 570 <= y <= 645:
                    opponent = "noob"
                elif 550 <= x <= 850 and 570 <= y <= 645:
                    opponent = "professional"
    pygame.display.flip()
pygame.quit()
