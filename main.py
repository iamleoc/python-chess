"""
Author: Leo Clough
Program: A playable game of chess that follows all the rules of the game.
Date Finished: 15/03/2022
"""
import pygame
from constants import HEIGHT, WIDTH, SQUARE_SIZE
from game import Game

# --------------- SET UP ---------------
# A few basic parts of setting up the game
FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
LEFT = 1
RIGHT = 3
pygame.display.set_caption("Chess")


# --------------- FUNCTIONS ---------------
def get_rank_file_from_mouse(pos):
    x, y = pos
    rank = y // SQUARE_SIZE
    file = x // SQUARE_SIZE
    return rank, file


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                rank, file = get_rank_file_from_mouse(pos)
                game.select(rank, file)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:  # Allows user to reset choice
                game.right_click()

        game.update()
        pygame.display.update()

    pygame.quit()


# --------------- MAIN ---------------
main()