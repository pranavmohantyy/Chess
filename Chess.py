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

BOARD_LIGHT = (240, 217, 181)
BOARD_DARK = (181, 136, 99)
BACKGROUND = (35, 35, 35)
ACCENT_BLUE = (70, 130, 180)
ACCENT_GREEN = (34, 139, 34)
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY = (200, 200, 200)
HIGHLIGHT_YELLOW = (255, 215, 0)
SELECT_BLUE = (30, 144, 255)
BORDER_COLOR = (100, 100, 100)

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

previous_board = None
previous_turn = None
previous_white_king_moved = False
previous_black_king_moved = False
previous_white_rooks_moved = [False, False]
previous_black_rooks_moved = [False, False]
previous_white_time = 0.0
previous_black_time = 0.0

in_menu = True
menu_options = ["Start Game", "Reset Game", "Quit"]
selected_option = 0

white_time = 0.0
black_time = 0.0
turn_start_time = None
display_white_time = 0.0
display_black_time = 0.0

def reset_game():
    global board, selected_piece, turn, game_over, last_move, white_king_moved, black_king_moved, white_rooks_moved, black_rooks_moved, white_time, black_time, turn_start_time, previous_board, previous_turn, previous_white_king_moved, previous_black_king_moved, previous_white_rooks_moved, previous_black_rooks_moved, previous_white_time, previous_black_time, display_white_time, display_black_time
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
    display_white_time = 0.0
    display_black_time = 0.0
    previous_board = None
    previous_turn = None
    previous_white_king_moved = False
    previous_black_king_moved = False
    previous_white_rooks_moved = [False, False]
    previous_black_rooks_moved = [False, False]
    previous_white_time = 0.0
    previous_black_time = 0.0

def save_state():
    global previous_board, previous_turn, previous_white_king_moved, previous_black_king_moved, previous_white_rooks_moved, previous_black_rooks_moved, previous_white_time, previous_black_time
    previous_board = [row[:] for row in board]
    previous_turn = turn
    previous_white_king_moved = white_king_moved
    previous_black_king_moved = black_king_moved
    previous_white_rooks_moved = white_rooks_moved[:]
    previous_black_rooks_moved = black_rooks_moved[:]
    previous_white_time = white_time
    previous_black_time = black_time

def undo_move():
    global board, turn, white_king_moved, black_king_moved, white_rooks_moved, black_rooks_moved, white_time, black_time, selected_piece, game_over, last_move
    if previous_board is not None:
        board = [row[:] for row in previous_board]
        turn = previous_turn
        white_king_moved = previous_white_king_moved
        black_king_moved = previous_black_king_moved
        white_rooks_moved = previous_white_rooks_moved[:]
        black_rooks_moved = previous_black_rooks_moved[:]
        white_time = previous_white_time
        black_time = previous_black_time
        selected_piece = None
        game_over = False
        last_move = None

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

pygame.display.set_caption("Chess - Pranav Mohanty")

def chess_board_drawing():
    pygame.draw.rect(screen, BORDER_COLOR, (BOARD_OFFSET-5, BOARD_OFFSET-5, SQUARE_SIZE*8+10, SQUARE_SIZE*8+10), 5)
    pygame.draw.rect(screen, BOARD_DARK, (BOARD_OFFSET-3, BOARD_OFFSET-3, SQUARE_SIZE*8+6, SQUARE_SIZE*8+6))

    for i in range(0, 8):
        for j in range(0, 8):
            x = BOARD_OFFSET + i * SQUARE_SIZE
            y = BOARD_OFFSET + j * SQUARE_SIZE
            color = BOARD_LIGHT if (i + j) % 2 == 0 else BOARD_DARK
            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            pygame.draw.rect(screen, BORDER_COLOR, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

    if selected_piece:
        row, col = selected_piece
        x = BOARD_OFFSET + col * SQUARE_SIZE
        y = BOARD_OFFSET + row * SQUARE_SIZE
        pygame.draw.rect(screen, SELECT_BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE), 4)

        valid_moves = get_valid_moves(row, col)
        for move_row, move_col in valid_moves:
            center_x = BOARD_OFFSET + move_col * SQUARE_SIZE + SQUARE_SIZE // 2
            center_y = BOARD_OFFSET + move_row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, ACCENT_GREEN, (center_x, center_y), 12)
            pygame.draw.circle(screen, TEXT_WHITE, (center_x, center_y), 8)


def draw_pieces():
    font = pygame.font.SysFont("arial", 70, bold=True)

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "":
                color = TEXT_WHITE if piece.isupper() else TEXT_GRAY
                text = font.render(piece, True, color)

                x = BOARD_OFFSET + col * SQUARE_SIZE + (SQUARE_SIZE - text.get_width()) // 2
                y = BOARD_OFFSET + row * SQUARE_SIZE + (SQUARE_SIZE - text.get_height()) // 2
                screen.blit(text, (x, y))

def draw_menu():
    screen.fill(BACKGROUND)

    for i in range(0, SCREEN_SIZE, 50):
        for j in range(0, SCREEN_SIZE, 50):
            if (i + j) % 100 == 0:
                pygame.draw.rect(screen, (45, 45, 45), (i, j, 50, 50))

    title_font = pygame.font.SysFont("arial", 80, bold=True)
    shadow_font = pygame.font.SysFont("arial", 80, bold=True)

    title_text = title_font.render("Chess Master", True, TEXT_WHITE)
    shadow_text = shadow_font.render("Chess Master", True, (20, 20, 20))

    title_x = SCREEN_SIZE // 2 - title_text.get_width() // 2
    title_y = 120

    screen.blit(shadow_text, (title_x + 3, title_y + 3))
    screen.blit(title_text, (title_x, title_y))

    subtitle_font = pygame.font.SysFont("arial", 24)
    subtitle_text = subtitle_font.render("A Complete Chess Experience", True, TEXT_GRAY)
    subtitle_x = SCREEN_SIZE // 2 - subtitle_text.get_width() // 2
    subtitle_y = title_y + 90
    screen.blit(subtitle_text, (subtitle_x, subtitle_y))

    menu_font = pygame.font.SysFont("arial", 36, bold=True)

    for i, option in enumerate(menu_options):
        option_width = 300
        option_height = 60
        option_x = SCREEN_SIZE // 2 - option_width // 2
        option_y = 280 + i * 80

        if i == selected_option:
            pygame.draw.rect(screen, ACCENT_BLUE, (option_x, option_y, option_width, option_height), border_radius=10)
            pygame.draw.rect(screen, HIGHLIGHT_YELLOW, (option_x, option_y, option_width, option_height), 3, border_radius=10)
            color = TEXT_WHITE
        else:
            pygame.draw.rect(screen, (60, 60, 60), (option_x, option_y, option_width, option_height), border_radius=10)
            pygame.draw.rect(screen, BORDER_COLOR, (option_x, option_y, option_width, option_height), 2, border_radius=10)
            color = TEXT_GRAY

        option_text = menu_font.render(option, True, color)
        text_x = option_x + (option_width - option_text.get_width()) // 2
        text_y = option_y + (option_height - option_text.get_height()) // 2
        screen.blit(option_text, (text_x, text_y))

    footer_font = pygame.font.SysFont("arial", 18)
    footer_text = footer_font.render("Use arrow keys to navigate • Enter to select • Mouse click supported", True, TEXT_GRAY)
    footer_x = SCREEN_SIZE // 2 - footer_text.get_width() // 2
    footer_y = SCREEN_SIZE - 50
    screen.blit(footer_text, (footer_x, footer_y))

def format_time(seconds):
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins}:{secs:02d}"

def draw_timers():
    panel_width = 200
    panel_height = 120
    panel_x = 20
    panel_y = 20

    pygame.draw.rect(screen, (40, 40, 40), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
    pygame.draw.rect(screen, BORDER_COLOR, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=10)

    timer_font = pygame.font.SysFont("arial", 24, bold=True)
    small_font = pygame.font.SysFont("arial", 16)

    white_label = small_font.render("White", True, TEXT_WHITE)
    white_time_text = timer_font.render(format_time(display_white_time), True, TEXT_WHITE)
    screen.blit(white_label, (panel_x + 15, panel_y + 15))
    screen.blit(white_time_text, (panel_x + 15, panel_y + 35))

    black_label = small_font.render("Black", True, TEXT_GRAY)
    black_time_text = timer_font.render(format_time(display_black_time), True, TEXT_GRAY)
    screen.blit(black_label, (panel_x + 15, panel_y + 75))
    screen.blit(black_time_text, (panel_x + 15, panel_y + 95))

    turn_panel_width = 180
    turn_panel_height = 50
    turn_panel_x = SCREEN_SIZE - turn_panel_width - 20
    turn_panel_y = 20

    pygame.draw.rect(screen, (40, 40, 40), (turn_panel_x, turn_panel_y, turn_panel_width, turn_panel_height), border_radius=8)
    pygame.draw.rect(screen, ACCENT_BLUE if turn == "white" else ACCENT_GREEN,
                     (turn_panel_x, turn_panel_y, turn_panel_width, turn_panel_height), 3, border_radius=8)

    turn_text = timer_font.render(f"{turn.capitalize()}'s Turn", True, HIGHLIGHT_YELLOW)
    turn_text_x = turn_panel_x + (turn_panel_width - turn_text.get_width()) // 2
    turn_text_y = turn_panel_y + (turn_panel_height - turn_text.get_height()) // 2
    screen.blit(turn_text, (turn_text_x, turn_text_y))

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
                        option_width = 300
                        option_height = 60
                        option_x = SCREEN_SIZE // 2 - option_width // 2
                        option_y = 280 + i * 80
                        if option_x <= x <= option_x + option_width and option_y <= y <= option_y + option_height:
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        continue
                    elif event.key == pygame.K_u:
                        undo_move()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        in_menu = True
                        selected_option = 0
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
                            save_state()
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

            screen.fill(BACKGROUND)
            chess_board_drawing()
            draw_pieces()
            draw_timers()

            if game_over:
                status_font = pygame.font.SysFont("arial", 48, bold=True)
                status_text = status_font.render("Game Over!", True, HIGHLIGHT_YELLOW)
                status_x = SCREEN_SIZE // 2 - status_text.get_width() // 2
                status_y = SCREEN_SIZE // 2 - status_text.get_height() // 2
                screen.blit(status_text, (status_x, status_y))

                restart_font = pygame.font.SysFont("arial", 24)
                restart_text = restart_font.render("Press R to restart or ESC for menu", True, TEXT_GRAY)
                restart_x = SCREEN_SIZE // 2 - restart_text.get_width() // 2
                restart_y = status_y + 60
                screen.blit(restart_text, (restart_x, restart_y))
        pygame.display.update()
        clock.tick(60)


main()
pygame.quit()