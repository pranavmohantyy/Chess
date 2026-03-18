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

ROWS, COLS = 8, 8
SQUARE_SIZE = 100

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

screen = pygame.display.set_mode((1000, 1000))
screen.fill(Cyan)
pygame.display.set_caption("Chess - Pranav Mohanty")

def chess_board_drawing():
    for i in range(0, 8):
        for j in range(0, 8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, White, (i * 100, j * 100, 100, 100))
            else:
                pygame.draw.rect(screen, Black, (i * 100, j * 100, 100, 100))

def draw_pieces():
    font = pygame.font.SysFont(None, 48)

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "":
                text = font.render(piece, True, Red)
                screen.blit(text, (col * 100 + 35, row * 100 + 30))



def main():
    global selected_piece
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                if selected_piece is None:
                    if board[row][col] != "":
                        selected_piece = (row, col)
                else:
                    old_row, old_col = selected_piece
                    board[row][col] = board[old_row][old_col]
                    board[old_row][old_col] = ""
                    selected_piece = None

        chess_board_drawing()
        draw_pieces()
        pygame.display.update()


main()
pygame.quit()

