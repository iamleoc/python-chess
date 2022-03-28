"""
This file handles most of the code relating to the board, such as the visual set up and how the pieces move across it
"""
from constants import LIGHT_SQUARES, RANKS, FILES, SQUARE_SIZE, DARK_SQUARES, BLACK, WHITE, BLUE
from asset_imgs import *
from piece import Piece


class Board:
    black_piece_list = ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"]
    white_piece_list = ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"]

    def __init__(self):
        self.board = []
        self.create_board()
        self.function_mapping = {
            "pawn": self.pawn,
            "rook": self.rook,
            "knight": self.knight,
            "bishop": self.bishop,
            "queen": self.queen,
            "king": self.king,
        }

    def create_board(self):
        """Creates the embedded array from the starting position of a chess game.
        Add pieces where applicable, else adds a 0 for empty squares
        """
        for rank in range(RANKS):
            self.board.append([])
            for file in range(FILES):
                if rank == 0:
                    piece_type = self.black_piece_list[file]
                    self.board[rank].append(Piece(rank, file, BLACK, piece_type))
                elif rank == 1:
                    self.board[rank].append(Piece(rank, file, BLACK, "b_pawn"))
                elif rank == 6:
                    self.board[rank].append(Piece(rank, file, WHITE, "w_pawn"))
                elif rank == 7:
                    piece_type = self.white_piece_list[file]
                    self.board[rank].append(Piece(rank, file, WHITE, piece_type))
                else:
                    self.board[rank].append(0)

    def _draw_squares(self, win, highlight_square):
        """Draws the visual dark and light squares for the board.
        If a square is currently selected by a player, colour it blue.
        """
        win.fill(DARK_SQUARES)
        for rank in range(RANKS):
            for file in range(rank % 2, RANKS, 2):
                pygame.draw.rect(win, LIGHT_SQUARES, (rank * SQUARE_SIZE, file * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        if highlight_square:
            pygame.draw.rect(win, BLUE, [highlight_square.x - (SQUARE_SIZE/2), highlight_square.y - (SQUARE_SIZE/2), SQUARE_SIZE, SQUARE_SIZE])

    def draw_pieces(self, win, highlight_square):
        """Draws or blits the piece images onto the squares of the board."""
        self._draw_squares(win, highlight_square)
        for rank in range(RANKS):
            for file in range(FILES):
                piece = self.board[rank][file]
                if piece != 0:
                    piece.draw(win)

    def move(self, piece, rank, file, last_move):
        """Attempts to move a piece to a new location.
        This will only allow the move to occur if the resulting position won't leave the side that moved in check.
        It saves the original position of the piece and if it will result in check, it moves it back and returns False,
        so that the player may make another choice.
        """
        start_rank = piece.rank
        start_file = piece.file
        self.board[piece.rank][piece.file], self.board[rank][file] = self.board[rank][file], self.board[piece.rank][piece.file]
        if not self.isCheck(WHITE if piece.colour == BLACK else BLACK, last_move):
            piece.move(rank, file)
            return True
        else:
            self.board[start_rank][start_file], self.board[rank][file] = piece, 0
            return False

    def capture_piece(self, piece, rank, file, last_move):
        """If a capture is to occur, this replaces the selected square with the capturing piece."""
        start_rank = piece.rank
        start_file = piece.file
        captured_piece = self.get_piece(rank, file)
        self.board[piece.rank][piece.file], self.board[rank][file] = 0, self.board[piece.rank][piece.file]
        if not self.isCheck(WHITE if piece.colour == BLACK else BLACK, last_move):
            piece.move(rank, file)
            return True
        else:
            self.board[start_rank][start_file], self.board[rank][file] = piece, captured_piece
            return False

    def get_piece(self, rank, file):
        return self.board[rank][file]

    def get_valid_moves(self, piece, last_move):
        """Traverses the possible movement of a selected piece and returns a dict of possible valid moves"""
        moves = {}
        starting_rank = piece.rank
        starting_file = piece.file
        colour = piece.colour
        has_moved = piece.has_moved
        piece_type = piece.piece_type[2:]
        moves.update(self.function_mapping[piece_type](piece_type, colour, has_moved, starting_rank, starting_file, last_move))
        return moves

    # The following code lays out how to determine a piece's valid moves.
    # Specific code written for the pawn and knight, and some extra functions for the king.
    def pawn(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        """Determines a pawns valid moves, including en passant and whether it can move two squares forward"""
        moves = {}

        # check forward moves
        if colour == WHITE:
            if starting_rank - 1 > 0:
                if self.board[starting_rank-1][starting_file] == 0:
                    moves[(starting_rank-1, starting_file)] = 0
                    if not has_moved and self.board[starting_rank-2][starting_file] == 0:
                        moves[(starting_rank - 2, starting_file)] = "pawnTwoSpaces"

        elif colour == BLACK:
            if starting_rank + 1 < 8:
                if self.board[starting_rank + 1][starting_file] == 0:
                    moves[(starting_rank + 1, starting_file)] = 0
                    if not has_moved and self.board[starting_rank + 2][starting_file] == 0:
                        moves[(starting_rank + 2, starting_file)] = "pawnTwoSpaces"

        # check if pawn can make a capture
        if colour == WHITE:
            if starting_file > 0 and starting_rank > 0:
                left_capture = self.get_piece(starting_rank - 1, starting_file - 1)
                if left_capture and left_capture.colour == BLACK:
                    if starting_rank - 1 == 0:
                        moves[(starting_rank-1, starting_file-1)] = "promotion"
                    else:
                        moves[(starting_rank - 1, starting_file - 1)] = 0
            if starting_file < 7 and starting_rank > 0:
                right_capture = self.get_piece(starting_rank - 1, starting_file + 1)
                if right_capture and right_capture.colour == BLACK:
                    if starting_rank - 1 == 0:
                        moves[(starting_rank - 1, starting_file+1)] = "promotion"
                    else:
                        moves[(starting_rank - 1, starting_file + 1)] = 0

        elif colour == BLACK:
            if starting_file > 0 and starting_rank < 7:
                left_capture = self.get_piece(starting_rank + 1, starting_file - 1)
                if left_capture and left_capture.colour == WHITE:
                    if starting_rank + 1 == 7:
                        moves[(starting_rank + 1, starting_file - 1)] = "promotion"
                    else:
                        moves[(starting_rank + 1, starting_file - 1)] = 0
            if starting_file < 7 and starting_rank < 7:
                right_capture = self.get_piece(starting_rank + 1, starting_file + 1)
                if right_capture and right_capture.colour == WHITE:
                    if starting_rank + 1 == 7:
                        moves[(starting_rank + 1, starting_file + 1)] = "promotion"
                    else:
                        moves[(starting_rank + 1, starting_file + 1)] = 0

        # check en passant
        if colour == WHITE:
            if last_move == (starting_rank, starting_file-1):
                moves[(starting_rank-1, starting_file - 1)] = "en passant"
            elif last_move == (starting_rank, starting_file+1):
                moves[(starting_rank-1, starting_file + 1)] = "en passant"
        elif colour == BLACK:
            if last_move == (starting_rank, starting_file-1):
                moves[(starting_rank+1, starting_file - 1)] = "en passant"
            elif last_move == (starting_rank, starting_file+1):
                moves[(starting_rank+1, starting_file + 1)] = "en passant"

        # promotion
        if colour == WHITE:
            if starting_rank - 1 == 0:
                if self.board[starting_rank - 1][starting_file] == 0:
                    moves[(starting_rank - 1, starting_file)] = "promotion"
        else:
            if starting_rank + 1 == 7:
                if self.board[starting_rank + 1][starting_file] == 0:
                    moves[(starting_rank + 1, starting_file)] = "promotion"
        return moves

    def rook(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        moves = {}
        moves.update(self._traverseUp(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDown(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseRight(piece_type, colour, starting_rank, starting_file))
        return moves

    def knight(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        moves = {}
        if starting_rank > 0 and starting_file > 1:
            if self.board[starting_rank-1][starting_file-2] == 0:
                moves[(starting_rank-1, starting_file-2)] = 0
            elif self.get_piece(starting_rank-1, starting_file-2).colour != colour:
                moves[(starting_rank - 1, starting_file - 2)] = self.get_piece(starting_rank-1, starting_file-2)
        if starting_rank > 0 and starting_file < 6:
            if self.board[starting_rank - 1][starting_file + 2] == 0:
                moves[(starting_rank - 1, starting_file + 2)] = 0
            elif self.get_piece(starting_rank - 1, starting_file + 2).colour != colour:
                moves[(starting_rank - 1, starting_file + 2)] = self.get_piece(starting_rank - 1, starting_file + 2)
        if starting_rank > 1 and starting_file > 0:
            if self.board[starting_rank-2][starting_file-1] == 0:
                moves[(starting_rank-2, starting_file-1)] = 0
            elif self.get_piece(starting_rank-2, starting_file-1).colour != colour:
                moves[(starting_rank - 2, starting_file - 1)] = self.get_piece(starting_rank-2, starting_file-1)
        if starting_rank > 1 and starting_file < 7:
            if self.board[starting_rank-2][starting_file+1] == 0:
                moves[(starting_rank-2, starting_file+1)] = 0
            elif self.get_piece(starting_rank-2, starting_file+1).colour != colour:
                moves[(starting_rank - 2, starting_file + 1)] = self.get_piece(starting_rank-2, starting_file+1)
        if starting_rank < 7 and starting_file > 1:
            if self.board[starting_rank+1][starting_file-2] == 0:
                moves[(starting_rank+1, starting_file-2)] = 0
            elif self.get_piece(starting_rank +1, starting_file - 2).colour != colour:
                moves[(starting_rank + 1, starting_file - 2)] = self.get_piece(starting_rank +1, starting_file - 2)
        if starting_rank < 7 and starting_file < 6:
            if self.board[starting_rank+1][starting_file+2] == 0:
                moves[(starting_rank+1, starting_file+2)] = 0
            elif self.get_piece(starting_rank+1, starting_file+2).colour != colour:
                moves[(starting_rank + 1, starting_file + 2)] = self.get_piece(starting_rank+1, starting_file+2)
        if starting_rank < 6 and starting_file > 0:
            if self.board[starting_rank+2][starting_file-1] == 0:
                moves[(starting_rank+2, starting_file-1)] = 0
            elif self.get_piece(starting_rank+2, starting_file-1).colour != colour:
                moves[(starting_rank + 2, starting_file - 1)] = self.get_piece(starting_rank+2, starting_file-1)
        if starting_rank < 6 and starting_file < 7:
            if self.board[starting_rank+2][starting_file+1] == 0:
                moves[(starting_rank+2, starting_file+1)] = 0
            elif self.get_piece(starting_rank+2, starting_file+1).colour != colour:
                moves[(starting_rank+2, starting_file+1)] = self.get_piece(starting_rank+2, starting_file+1)
        return moves

    def bishop(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        moves = {}
        moves.update(self._traverseUpLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseUpRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownRight(piece_type, colour, starting_rank, starting_file))
        return moves

    def queen(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        moves = {}
        moves.update(self._traverseUp(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDown(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseUpLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseUpRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownRight(piece_type, colour, starting_rank, starting_file))
        return moves

    def king(self, piece_type, colour, has_moved, starting_rank, starting_file, last_move):
        moves = {}
        moves.update(self._traverseUp(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDown(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseUpLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownLeft(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseUpRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._traverseDownRight(piece_type, colour, starting_rank, starting_file))
        moves.update(self._castlingRights(piece_type, has_moved, colour, starting_rank, starting_file, last_move))
        return moves

    # The following code traverses in a line and returns possible squares that could be a valid move.
    # If there is a piece occupying the next square, it will stop. If that piece is the opposite colour,
    # then it can be added to the valid moves list as a capture.
    def _traverseUp(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank > 0:
            next_piece = self.get_piece(starting_rank - 1, starting_file)
            if next_piece == 0:
                moves[(starting_rank-1, starting_file)] = next_piece
                if piece_type != "king":
                    moves.update(self._traverseUp(piece_type, colour, starting_rank - 1, starting_file))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank-1, starting_file)] = next_piece
            else:
                return moves
        return moves

    def _traverseDown(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank < 7:
            next_piece = self.get_piece(starting_rank + 1, starting_file)
            if next_piece == 0:
                moves[(starting_rank+1, starting_file)] = 0
                if piece_type != "king":
                    moves.update(self._traverseDown(piece_type, colour, starting_rank + 1, starting_file))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank + 1, starting_file)] = next_piece
            else:
                return moves
        return moves

    def _traverseLeft(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_file > 0:
            next_piece = self.get_piece(starting_rank, starting_file - 1)
            if next_piece == 0:
                moves[(starting_rank, starting_file - 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseLeft(piece_type, colour, starting_rank, starting_file - 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank, starting_file - 1)] = next_piece
            else:
                return moves
        return moves

    def _traverseRight(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_file < 7:
            next_piece = self.get_piece(starting_rank, starting_file + 1)
            if next_piece == 0:
                moves[(starting_rank, starting_file + 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseRight(piece_type, colour, starting_rank, starting_file + 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank, starting_file + 1)] = next_piece
            else:
                return moves
        return moves

    def _traverseUpLeft(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank > 0 and starting_file > 0:
            next_piece = self.get_piece(starting_rank - 1, starting_file - 1)
            if next_piece == 0:
                moves[(starting_rank - 1, starting_file - 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseUpLeft(piece_type, colour, starting_rank - 1, starting_file - 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank - 1, starting_file - 1)] = next_piece
            else:
                return moves
        return moves

    def _traverseUpRight(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank > 0 and starting_file < 7:
            next_piece = self.get_piece(starting_rank - 1, starting_file + 1)
            if next_piece == 0:
                moves[(starting_rank - 1, starting_file + 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseUpRight(piece_type, colour, starting_rank - 1, starting_file + 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank - 1, starting_file + 1)] = next_piece
            else:
                return moves
        return moves

    def _traverseDownLeft(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank < 7 and starting_file > 0:
            next_piece = self.get_piece(starting_rank + 1, starting_file - 1)
            if next_piece == 0:
                moves[(starting_rank + 1, starting_file - 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseDownLeft(piece_type, colour, starting_rank + 1, starting_file - 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank + 1, starting_file - 1)] = next_piece
            else:
                return moves
        return moves

    def _traverseDownRight(self, piece_type, colour, starting_rank, starting_file):
        moves = {}
        if starting_rank < 7 and starting_file < 7:
            next_piece = self.get_piece(starting_rank + 1, starting_file + 1)
            if next_piece == 0:
                moves[(starting_rank + 1, starting_file + 1)] = 0
                if piece_type != "king":
                    moves.update(self._traverseDownRight(piece_type, colour, starting_rank + 1, starting_file + 1))
                else:
                    return moves
            elif next_piece.colour != colour:
                moves[(starting_rank + 1, starting_file + 1)] = next_piece
            else:
                return moves
        return moves

    def _castlingRights(self, piece_type, has_moved, colour, starting_rank, starting_file, last_move):
        """Works out whether a selected king can castle or not."""
        moves = {}
        if not has_moved:
            # short castle
            rook = self.get_piece(starting_rank, starting_file+3)
            if rook != 0 \
                    and rook.piece_type[2:] == "rook" \
                    and not rook.has_moved \
                    and rook.colour == colour \
                    and self.get_piece(starting_rank, starting_file+1) == 0 \
                    and self.get_piece(starting_rank, starting_file+2) == 0:
                # then we can castle
                moves[starting_rank, starting_file+2] = "shortCastle"
            # long castle
            rook = self.get_piece(starting_rank, starting_file-4)
            if rook != 0 \
                    and rook.piece_type[2:] == "rook" \
                    and not rook.has_moved \
                    and rook.colour == colour \
                    and self.get_piece(starting_rank, starting_file - 1) == 0 \
                    and self.get_piece(starting_rank, starting_file - 2) == 0 \
                    and self.get_piece(starting_rank, starting_file - 3) == 0:
                moves[starting_rank, starting_file-2] = "longCastle"
        else:
            pass
        return moves

    # ------------------------------
    # The following code is specific code that is essentially the same as the move function above.
    # The difference here is that the pieces/squares affected are not the same as
    # the pieces/squares selected with the mouse
    def shortCastle(self, king, rank, file, last_move):
        start_rank = king.rank
        start_file = king.file
        rook = self.get_piece(rank, file + 1)
        self.board[king.rank][king.file], self.board[rank][file] = self.board[rank][file], self.board[king.rank][king.file]
        self.board[rank][file - 1], self.board[rook.rank][rook.file] = rook, self.board[rank][file - 1]
        if not self.isCheck(WHITE if king.colour == BLACK else BLACK, last_move):
            king.move(rank, file)
            rook.move(rank, file-1)
            return True
        else:
            # revert to original pos
            self.board[start_rank][start_file], self.board[rank][file] = king, 0
            self.board[rook.rank][rook.file], self.board[rank][file-1] = rook, 0
            return False

    def longCastle(self, king, rank, file, last_move):
        start_rank = king.rank
        start_file = king.file
        rook = self.get_piece(rank, file-2)
        self.board[king.rank][king.file], self.board[rank][file] = self.board[rank][file], self.board[king.rank][king.file]
        self.board[rank][file+1], self.board[rook.rank][rook.file] = rook, self.board[rank][file+1]
        if not self.isCheck(WHITE if king.colour == BLACK else BLACK, last_move):
            king.move(rank, file)
            rook.move(rank, file + 1)
            return True
        else:
            self.board[start_rank][start_file], self.board[rank][file] = king, 0
            self.board[rook.rank][rook.file], self.board[rank][file + 1] = rook, 0
            return False

    def enPassant(self, pawn, rank, file, colour, last_move):
        new_board = self.board[:]
        if colour == WHITE:
            captured_pawn = self.get_piece(rank+1, file)
        else:
            captured_pawn = self.get_piece(rank-1, file)
        if not self.isCheck(WHITE if pawn.colour == BLACK else BLACK, last_move):
            new_board[pawn.rank][pawn.file], new_board[rank][file] = new_board[rank][file], new_board[pawn.rank][pawn.file]
            new_board[captured_pawn.rank][captured_pawn.file] = 0
            pawn.move(rank, file)
            return True
        else:
            return False

    # ---------------------------
    def isCheck(self, colour, last_move):
        """Returns true or false depending on whether it is check or not.
        The colour parameter is the side that you wish to check if it is putting the other side in check.
        """
        # checks whether a side is in check on the copy board
        check_moves = {}
        for rank in range(RANKS):
            for file in range(FILES):
                piece = self.get_piece(rank, file)
                if piece != 0 and piece.colour == colour:
                    check_moves.update(self.get_valid_moves(piece, last_move))
        for (rank, file) in check_moves:
            try:
                self.get_piece(rank, file).piece_type[2:] == "king"
            except AttributeError:
                pass
            else:
                if self.get_piece(rank, file).piece_type[2:] == "king" and self.get_piece(rank, file).colour != colour:
                    return True
        return False

    def short_castle_through_check(self, colour, last_move):
        """Determines if a king is trying to castle through check"""
        check_moves = {}
        for rank in range(RANKS):
            for file in range(FILES):
                piece = self.get_piece(rank, file)
                if piece != 0 and piece.colour != colour:
                    check_moves.update(self.get_valid_moves(piece, last_move))
        if colour == WHITE:
            if (7, 5) in check_moves:
                return True
            else:
                return False
        else:
            if (0, 5) in check_moves:
                return True
            else:
                return False

    def long_castle_through_check(self, colour, last_move):
        """Determines if a king is trying to castle through check"""
        check_moves = {}
        for rank in range(RANKS):
            for file in range(FILES):
                piece = self.get_piece(rank, file)
                if piece != 0 and piece.colour != colour:
                    check_moves.update(self.get_valid_moves(piece, last_move))
        if colour == WHITE:
            if (7, 3) in check_moves:
                return True
            else:
                return False
        else:
            if (0, 3) in check_moves:
                return True
            else:
                return False

    def pawn_promotion(self, piece, rank, file, last_move):
        while True:
            print("Which piece would you like to promote to?")
            new_piece_type = input("N = Knight, B = Bishop, R = Rook, Q = Queen, C = Cancel: ").upper()
            if new_piece_type in ["N", "B", "R", "Q", "C"]:
                break
            else:
                print("Please only enter one of the valid options.\n")
        start_rank = piece.rank
        start_file = piece.file
        captured_piece = self.board[rank][file]
        self.board[piece.rank][piece.file], self.board[rank][file] = 0, self.board[piece.rank][piece.file]
        if not self.isCheck(WHITE if piece.colour == BLACK else BLACK, last_move):
            if new_piece_type == 'N':
                piece.piece_type = piece.piece_type[:2] + "knight"
                piece.piece_image = piece.piece_dict[piece.piece_type]
            elif new_piece_type == "B":
                piece.piece_type = piece.piece_type[:2] + "bishop"
                piece.piece_image = piece.piece_dict[piece.piece_type]
            elif new_piece_type == "R":
                piece.piece_type = piece.piece_type[:2] + "rook"
                piece.piece_image = piece.piece_dict[piece.piece_type]
            elif new_piece_type == "Q":
                piece.piece_type = piece.piece_type[:2] + "queen"
                piece.piece_image = piece.piece_dict[piece.piece_type]
            elif new_piece_type == "C":
                return False
            piece.move(rank, file)
            return True
        else:
            self.board[start_rank][start_file], self.board[rank][file] = piece, captured_piece
            return False
