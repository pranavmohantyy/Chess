import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

Black = (0, 0, 0)
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Cyan  = (0, 255, 255)
Magenta  = (255, 0, 255)
Gray  = (128, 128, 128)
Light_Gray = (200, 200, 200)
Dark_Gray = (50, 50, 50)
Orange = (255, 165, 0)
Purple = (128, 0, 128)
Pink = (255, 192, 203)
Brown = (165, 42, 42)
Light_Green = (144, 238, 144)

pygame.init()
clock = pygame.time.Clock()

SQUARE_SIZE = 100
SCREEN_SIZE = 1000
BOARD_OFFSET = (SCREEN_SIZE - SQUARE_SIZE * 8) // 2

board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"],
]

selected_piece = None
turn = "white"
game_over = False
last_move = None
white_king_moved = False
black_king_moved = False
white_rooks_moved = [False, False]
black_rooks_moved = [False, False]

in_menu = True
menu_options = ["Start Game", "Reset Game", "Quit"]
selected_option = 0

white_time = 0.0
black_time = 0.0
turn_start_time = None

def reset_game():
    global board, selected_piece, turn, game_over, last_move, white_king_moved, black_king_moved, white_rooks_moved, black_rooks_moved, white_time, black_time, turn_start_time
    board = [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        ["","","","","","","",""] ,
        ["","","","","","","",""] ,
        ["","","","","","","",""] ,
        ["","","","","","","",""] ,
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"],
    ]
    selected_piece = None
    turn = "white"
    game_over = False
    last_move = None
    white_king_moved = False
    black_king_moved = False
    white_rooks_moved = [False, False]
    black_rooks_moved = [False, False]
    white_time = 0.0
    black_time = 0.0
    turn_start_time = pygame.time.get_ticks()

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

pygame.display.set_caption("Chess - Pranav Mohanty")

def chess_board_drawing():
    for i in range(0, 8):
        for j in range(0, 8):
            x = BOARD_OFFSET + i * SQUARE_SIZE
            y = BOARD_OFFSET + j * SQUARE_SIZE
            color = White if (i + j) % 2 == 0 else Black
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    if selected_piece:
        row, col = selected_piece
        x = BOARD_OFFSET + col * SQUARE_SIZE
        y = BOARD_OFFSET + row * SQUARE_SIZE
        pygame.draw.rect(screen, Yellow, (x, y, SQUARE_SIZE, SQUARE_SIZE), 5)

        valid_moves = get_valid_moves(row, col)
        for move_row, move_col in valid_moves:
            center_x = BOARD_OFFSET + move_col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = BOARD_OFFSET + move_row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, Light_Green, (center_x, center_y), 15)


def draw_pieces():
    font = pygame.font.SysFont(None, 48)

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "":
                text = font.render(piece, True, Red)
                x = BOARD_OFFSET + col * SQUARE_SIZE + 35
                y = BOARD_OFFSET + row * SQUARE_SIZE + 30
                screen.blit(text, (x, y))

def draw_menu():
    screen.fill(Dark_Gray)
    
    title_font = pygame.font.SysFont(None, 72)
    menu_font = pygame.font.SysFont(None, 48)
    
    title_text = title_font.render("Chess Game", True, White)
    title_x = SCREEN_SIZE // 2 - title_text.get_width() // 2
    title_y = 150
    screen.blit(title_text, (title_x, title_y))
    
    for i, option in enumerate(menu_options):
        color = Yellow if i == selected_option else White
        option_text = menu_font.render(option, True, color)
        option_x = SCREEN_SIZE // 2 - option_text.get_width() // 2
        option_y = 300 + i * 80
        screen.blit(option_text, (option_x, option_y))

def format_time(seconds):
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins}:{secs:02d}"

def draw_timers():
    timer_font = pygame.font.SysFont(None, 36)
    white_text = timer_font.render(f"White: {format_time(white_time)}", True, White)
    black_text = timer_font.render(f"Black: {format_time(black_time)}", True, White)
    screen.blit(white_text, (20, 20))
    screen.blit(black_text, (20, 60))
    
    turn_indicator = timer_font.render(f"Turn: {turn.capitalize()}", True, Yellow if turn == "white" else White)
    screen.blit(turn_indicator, (SCREEN_SIZE - 250, 20))

def in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def piece_color(piece):
    if piece == "":
        return None
    return "white" if piece.isupper() else "black"


def is_enemy(piece, target):
    if piece == "" or target == "":
        return False
    return piece_color(piece) != piece_color(target)


def find_king(color):
    king_symbol = "K" if color == "white" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == king_symbol:
                return (r, c)
    return None


def is_square_attacked(row, col, by_color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "" and piece_color(piece) == by_color:
                for attack in get_raw_moves_for_piece(r, c):
                    if attack == (row, col):
                        return True
    return False


def is_in_check(color):
    king_pos = find_king(color)
    if king_pos is None:
        return True
    opponent = "black" if color == "white" else "white"
    return is_square_attacked(king_pos[0], king_pos[1], opponent)


def is_checkmate(color):
    if not is_in_check(color):
        return False
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "" and piece_color(piece) == color:
                if get_valid_moves(r, c):
                    return False
    return True


def get_raw_moves_for_piece(row, col):
    piece = board[row][col]
    if piece == "":
        return []
    moves = []
    color = piece_color(piece)

    if piece.lower() == "p":
        direction = -1 if color == "white" else 1
        start_row = 6 if color == "white" else 1

        next_row = row + direction
        if in_bounds(next_row, col) and board[next_row][col] == "":
            moves.append((next_row, col))
            two_row = row + 2 * direction
            if row == start_row and in_bounds(two_row, col) and board[two_row][col] == "":
                moves.append((two_row, col))

        for dc in [-1, 1]:
            target_row = row + direction
            target_col = col + dc
            if in_bounds(target_row, target_col):
                target = board[target_row][target_col]
                if target != "" and piece_color(target) != color:
                    moves.append((target_row, target_col))
        
        if last_move:
            last_from, last_to = last_move
            last_from_row, last_from_col = last_from
            last_to_row, last_to_col = last_to
            last_piece = board[last_to_row][last_to_col]
            if (last_piece.lower() == "p" and piece_color(last_piece) != color and 
                last_to_row == row and abs(last_from_row - last_to_row) == 2):
                if last_to_col == col - 1 or last_to_col == col + 1:
                    en_passant_row = row + direction
                    en_passant_col = last_to_col
                    if in_bounds(en_passant_row, en_passant_col):
                        moves.append((en_passant_row, en_passant_col))

    elif piece.lower() == "n":
        knight_deltas = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for dr, dc in knight_deltas:
            nr, nc = row + dr, col + dc
            if in_bounds(nr, nc) and (board[nr][nc] == "" or is_enemy(piece, board[nr][nc])):
                moves.append((nr, nc))

    elif piece.lower() in ["r", "b", "q"]:
        directions = []
        if piece.lower() in ["r", "q"]:
            directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if piece.lower() in ["b", "q"]:
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            while in_bounds(nr, nc):
                if board[nr][nc] == "":
                    moves.append((nr, nc))
                else:
                    if piece_color(board[nr][nc]) != color:
                        moves.append((nr, nc))
                    break
                nr += dr
                nc += dc

    elif piece.lower() == "k":
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in king_moves:
            nr, nc = row + dr, col + dc
            if in_bounds(nr, nc) and (board[nr][nc] == "" or is_enemy(piece, board[nr][nc])):
                moves.append((nr, nc))
        
        if color == "white" and not white_king_moved:
            if not white_rooks_moved[0] and board[7][0] == "R" and board[7][1] == "" and board[7][2] == "" and board[7][3] == "":
                moves.append((7, 2))
            if not white_rooks_moved[1] and board[7][7] == "R" and board[7][5] == "" and board[7][6] == "":
                moves.append((7, 6))
        elif color == "black" and not black_king_moved:
            if not black_rooks_moved[0] and board[0][0] == "r" and board[0][1] == "" and board[0][2] == "" and board[0][3] == "":
                moves.append((0, 2))
            if not black_rooks_moved[1] and board[0][7] == "r" and board[0][5] == "" and board[0][6] == "":
                moves.append((0, 6))

    return moves


def get_valid_moves(row, col):
    piece = board[row][col]
    if piece == "":
        return []
    color = piece_color(piece)
    if color != turn:
        return []

    raw_moves = get_raw_moves_for_piece(row, col)
    legal_moves = []
    
    is_castling_move = piece.lower() == "k"

    for nr, nc in raw_moves:
        origin = board[row][col]
        target = board[nr][nc]
        
        is_castling = (piece.lower() == "k" and abs(col - nc) == 2)
        
        if is_castling:
            opponent = "black" if color == "white" else "white"
            if is_in_check(color):
                continue
            intermediate_col = (col + nc) // 2
            if is_square_attacked(row, intermediate_col, opponent):
                continue
        
        board[nr][nc] = origin
        board[row][col] = ""

        if not is_in_check(color):
            legal_moves.append((nr, nc))

        board[row][col] = origin
        board[nr][nc] = target

    return legal_moves


def main():
    global selected_piece, turn, game_over, last_move, white_king_moved, black_king_moved, white_rooks_moved, black_rooks_moved, in_menu, selected_option, white_time, black_time, turn_start_time
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if in_menu:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            in_menu = False
                            turn_start_time = pygame.time.get_ticks()
                        elif selected_option == 1:
                            reset_game()
                            in_menu = False
                        elif selected_option == 2:
                            running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for i, option in enumerate(menu_options):
                        option_text = pygame.font.SysFont(None, 48).render(option, True, White)
                        option_x = SCREEN_SIZE // 2 - option_text.get_width() // 2
                        option_y = 300 + i * 80
                        if option_x <= x <= option_x + option_text.get_width() and option_y <= y <= option_y + option_text.get_height():
                            if i == 0:
                                in_menu = False
                                turn_start_time = pygame.time.get_ticks()
                            elif i == 1:
                                reset_game()
                                in_menu = False
                            elif i == 2:
                                running = False
                            break
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game()
                    continue

                if turn_start_time is not None:
                    elapsed = (pygame.time.get_ticks() - turn_start_time) / 1000.0
                    if turn == "white":
                        white_time += elapsed
                    else:
                        black_time += elapsed
                    turn_start_time = pygame.time.get_ticks()
                
                if game_over:
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = (x - BOARD_OFFSET) // SQUARE_SIZE
                    row = (y - BOARD_OFFSET) // SQUARE_SIZE

                    if not in_bounds(row, col):
                        continue

                    if selected_piece is None:
                        if board[row][col] != "" and piece_color(board[row][col]) == turn:
                            selected_piece = (row, col)
                    else:
                        old_row, old_col = selected_piece
                        valid_moves = get_valid_moves(old_row, old_col)

                        if (row, col) in valid_moves:
                            moving_piece = board[old_row][old_col]
                            
                            is_en_passant = (moving_piece.lower() == "p" and old_col != col and 
                                            board[row][col] == "")
                            
                            is_castling = (moving_piece.lower() == "k" and abs(old_col - col) == 2)
                            
                            board[row][col] = moving_piece
                            board[old_row][old_col] = ""
                            
                            if is_en_passant:
                                board[old_row][col] = ""
                            
                            if is_castling:
                                if col > old_col:
                                    board[row][col-1] = board[row][7]
                                    board[row][7] = ""
                                else:
                                    board[row][col+1] = board[row][0]
                                    board[row][0] = ""

                            if moving_piece.lower() == "k":
                                if piece_color(moving_piece) == "white":
                                    white_king_moved = True
                                else:
                                    black_king_moved = True
                            
                            if moving_piece.lower() == "r":
                                if piece_color(moving_piece) == "white":
                                    if old_col == 0:
                                        white_rooks_moved[0] = True
                                    elif old_col == 7:
                                        white_rooks_moved[1] = True
                                else:
                                    if old_col == 0:
                                        black_rooks_moved[0] = True
                                    elif old_col == 7:
                                        black_rooks_moved[1] = True

                            if moving_piece.lower() == "p" and row in (0, 7):
                                board[row][col] = "Q" if piece_color(moving_piece) == "white" else "q"

                            last_move = ((old_row, old_col), (row, col))
                            turn = "black" if turn == "white" else "white"
                            turn_start_time = pygame.time.get_ticks()
                            selected_piece = None

                            if is_checkmate(turn):
                                winner = "White" if turn == "black" else "Black"
                                print(f"Checkmate! {winner} wins")
                                game_over = True
                            elif is_in_check(turn):
                                print(f"{turn.capitalize()} is in check")

                        else:
                            if board[row][col] != "" and piece_color(board[row][col]) == turn:
                                selected_piece = (row, col)
                            else:
                                selected_piece = None

        if in_menu:
            draw_menu()
        else:
            if turn_start_time is not None:
                elapsed = (pygame.time.get_ticks() - turn_start_time) / 1000.0
                if turn == "white":
                    display_white_time = white_time + elapsed
                    display_black_time = black_time
                else:
                    display_white_time = white_time
                    display_black_time = black_time + elapsed
            else:
                display_white_time = white_time
                display_black_time = black_time
            
            screen.fill(Cyan)
            chess_board_drawing()
            draw_pieces()
            
            timer_font = pygame.font.SysFont(None, 36)
            white_text = timer_font.render(f"White: {format_time(display_white_time)}", True, White)
            black_text = timer_font.render(f"Black: {format_time(display_black_time)}", True, White)
            screen.blit(white_text, (20, 20))
            screen.blit(black_text, (20, 60))
            turn_indicator = timer_font.render(f"Turn: {turn.capitalize()}", True, Yellow if turn == "white" else Yellow)
            screen.blit(turn_indicator, (SCREEN_SIZE - 250, 20))
        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()