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

screen = pygame.display.set_mode((1000, 1000))
screen.fill(Cyan)
pygame.display.set_caption("Chess - Pranav Mohanty")

def chess_board():
    for i in range(1, 9):
        for j in range(1, 9):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, White, (i * 100, j * 100, 100, 100))
            else:
                pygame.draw.rect(screen, Black, (i * 100, j * 100, 100, 100))



def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        chess_board()
        pygame.display.update()


main()
pygame.quit()

