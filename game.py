import pygame
from constants import BLACK, WHITE, SQUARE_SIZE, BLUE
from board import Board
from constants import RANKS, FILES


class Game:
    def __init__(self, win):
        self.selected = None
        self.board = Board()
        self.valid_moves = {}
        self.win = win
        self.turn = WHITE
        self.is_it_check = False
        self.lastMove = None

    def _init(self):
        self.selected = None
        self.board = Board()
        self.valid_moves = {}

    def right_click(self):
        self.selected = None
        self.valid_moves = {}

    def update(self):
        highlight_square = self.selected
        self.board.draw_pieces(self.win, highlight_square)
        self.board.copyBoard = self.board.board[:]
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, rank, file):
        if self.selected:
            if self.selected.colour == self.turn:
                self.valid_moves = self.board.get_valid_moves(self.selected, self.lastMove)
                result = self._move(rank, file)
                self.selected = None
                if not result:
                    self.selected = None
                    self.valid_moves = {}
                    self.select(rank, file)
        elif self.selected is None:
            piece = self.board.get_piece(rank, file)
            if piece != 0 and piece.colour == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(self.selected, self.lastMove)
            elif piece == 0:
                self.selected = None
        return False

    def _move(self, rank, file):
        new_sq = self.board.get_piece(rank, file)
        if new_sq == 0 and (rank, file) in self.valid_moves:
            if self.valid_moves[(rank, file)] == "shortCastle":
                self.board.shortCastle(self.selected, rank, file)
                self.lastMove = None
                self.change_turn()
            elif self.valid_moves[(rank, file)] == "longCastle":
                self.board.longCastle(self.selected, rank, file)
                self.lastMove = None
                self.change_turn()
            elif self.valid_moves[(rank, file)] == "pawnTwoSpaces":
                result = self.board.move(self.selected, rank, file, self.lastMove)
                if result:
                    self.lastMove = (rank, file)
                    self.change_turn()
                    return True
                else:
                    return False
            elif self.valid_moves[(rank, file)] == "en passant":
                result = self.board.enPassant(self.selected, rank, file, self.selected.colour, self.lastMove)
                if result:
                    self.lastMove = None
                    self.change_turn()
                else:
                    return False
            else:
                result = self.board.move(self.selected, rank, file, self.lastMove, self.is_it_check)
                if result:
                    self.lastMove = None
                    self.change_turn()
                else:
                    return False
        elif new_sq != 0 and (rank, file) in self.valid_moves:
            new_piece = self.board.get_piece(rank, file)
            if new_piece.colour != self.selected.colour:
                self.board.capture_piece(self.selected, rank, file)
                self.lastMove = None
                self.change_turn()
            else:
                return False
        else:
            return False
        return True

    def change_turn(self):
        if self.turn == WHITE:
            self.is_it_check = self.board.isCheck(WHITE, self.lastMove)
            self.turn = BLACK
        else:
            self.is_it_check = self.board.isCheck(BLACK, self.lastMove)
            self.turn = WHITE
        self.valid_moves = {}

    def draw_valid_moves(self, moves):
        for move in moves:
            rank, file = move
            pygame.draw.circle(self.win, BLUE, (file * SQUARE_SIZE + SQUARE_SIZE // 2, rank * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
