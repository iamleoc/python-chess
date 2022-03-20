import pygame
from constants import SQUARE_SIZE, BLUE
from asset_imgs import *


class Piece:
    RADIUS = 20
    piece_dict = {
        "b_pawn": B_PAWN,
        "b_rook": B_ROOK,
        "b_knight": B_KNIGHT,
        "b_bishop": B_BISHOP,
        "b_queen": B_QUEEN,
        "b_king": B_KING,
        "w_pawn": W_PAWN,
        "w_rook": W_ROOK,
        "w_knight": W_KNIGHT,
        "w_bishop": W_BISHOP,
        "w_queen": W_QUEEN,
        "w_king": W_KING
    }

    def __init__(self, rank, file, colour, piece_type):
        self.rank = rank
        self.file = file
        self.colour = colour
        self.piece_image = self.piece_dict[piece_type]
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.piece_type = piece_type
        self.has_moved = False
        self.is_selected = False

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.file + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.rank + SQUARE_SIZE // 2

    def draw(self, win):
        win.blit(self.piece_image, (self.x - (self.piece_image.get_width() // 2), self.y - (self.piece_image.get_height() // 2)))

    def move(self, rank, file):
        self.rank = rank
        self.file = file
        self.calc_pos()
        self.has_moved = True
