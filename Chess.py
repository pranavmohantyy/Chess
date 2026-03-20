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
Beige = (245, 245, 220)

pygame.init()

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

    for nr, nc in raw_moves:
        origin = board[row][col]
        target = board[nr][nc]
        board[nr][nc] = origin
        board[row][col] = ""

        if not is_in_check(color):
            legal_moves.append((nr, nc))

        board[row][col] = origin
        board[nr][nc] = target

    return legal_moves


def main():
    global selected_piece, turn
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

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
                        board[row][col] = moving_piece
                        board[old_row][old_col] = ""

                        if moving_piece.lower() == "p" and row in (0, 7):
                            board[row][col] = "Q" if piece_color(moving_piece) == "white" else "q"

                        turn = "black" if turn == "white" else "white"
                        selected_piece = None

                        if is_in_check(turn):
                            print(f"{turn.capitalize()} is in check")

                    else:
                        if board[row][col] != "" and piece_color(board[row][col]) == turn:
                            selected_piece = (row, col)
                        else:
                            selected_piece = None


        screen.fill(Cyan)
        chess_board_drawing()
        draw_pieces()
        pygame.display.update()


main()
pygame.quit()