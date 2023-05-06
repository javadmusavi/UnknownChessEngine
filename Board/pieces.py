class Piece:
    """Class representing a chess piece."""

    def __init__(self, color):
        self.color = color  # 'w' for white, 'b' for black
        self.has_moved = False  # Whether the piece has moved yet in the game

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        """
        Returns a list of valid moves for the piece at the given position on the board.
        """
        raise NotImplementedError("Subclasses should implement this method")


class King(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []
        # Check all 8 neighboring squares
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0:
                    continue
                end_rank_idx = start_rank_idx + dr
                end_file_idx = start_file_idx + df
                if end_rank_idx < 0 or end_rank_idx >= 8 or end_file_idx < 0 or end_file_idx >= 8:
                    continue  # End square is off the board
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None or end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
        return valid_moves

    def __str__(self):
        return f'{self.color}K'


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []
        # Check if pawn can move one or two squares up
        if self.color == 'w':
            print('here')
            if start_rank_idx == 6:
                if board.get_piece(start_rank_idx - 1, start_file_idx) is None and board.get_piece(start_rank_idx - 2,
                                                                                                   start_file_idx) is None:
                    valid_moves.extend([(start_rank_idx-1, start_file_idx), (start_rank_idx - 2, start_file_idx)])
            elif start_rank_idx > 0 and board.get_piece(start_rank_idx - 1, start_file_idx) is None:
                valid_moves.append((start_rank_idx - 1, start_file_idx))

            # Check if pawn can capture diagonally
            for dr, df in [(-1, 1), (-1, -1)]:
                end_rank_idx = start_rank_idx + dr
                end_file_idx = start_file_idx + df
                print()
                if end_rank_idx < 0 or end_rank_idx >= 8 or end_file_idx < 0 or end_file_idx >= 8:
                    print('here')
                    continue  # End square is off the board
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                print(end_rank_idx, end_file_idx)
                if end_piece is not None and end_piece.color != self.color:
                    print('here')
                    valid_moves.append((end_rank_idx, end_file_idx))

        elif self.color == 'b':
            if start_rank_idx == 1:
                if board.get_piece(start_rank_idx + 1, start_file_idx) is None and board.get_piece(start_rank_idx + 2,
                                                                                                   start_file_idx) is None:
                    valid_moves.extend([(start_rank_idx+1, start_file_idx), (start_rank_idx + 2, start_file_idx)])
            if start_rank_idx < 7 and board.get_piece(start_rank_idx + 1, start_file_idx) is None:
                valid_moves.append((start_rank_idx + 1, start_file_idx))\

            # Check if pawn can capture diagonally
            for dr, df in [(1, 1), (1, -1)]:
                end_rank_idx = start_rank_idx + dr
                end_file_idx = start_file_idx + df
                if end_rank_idx < 0 or end_rank_idx >= 8 or end_file_idx < 0 or end_file_idx >= 8:

                    continue  # End square is off the board
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is not None and end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))

        return valid_moves

    def __str__(self):
        return f'{self.color}P'


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []
        # Check horizontal squares
        for df in [-1, 1]:
            end_rank_idx = start_rank_idx
            end_file_idx = start_file_idx + df
            while end_file_idx >= 0 and end_file_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_file_idx += df

        # Check vertical squares
        for dr in [-1, 1]:
            end_rank_idx = start_rank_idx + dr
            end_file_idx = start_file_idx
            while end_rank_idx >= 0 and end_rank_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_rank_idx += dr

        return valid_moves

    def __str__(self):
        return f'{self.color}R'


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []

        # Check diagonal squares
        for dr, df in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            end_rank_idx = start_rank_idx + dr
            end_file_idx = start_file_idx + df
            while end_rank_idx >= 0 and end_rank_idx <= 7 and end_file_idx >= 0 and end_file_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_rank_idx += dr
                end_file_idx += df

        return valid_moves

    def __str__(self):
        return f'{self.color}B'


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []

        # Check horizontal squares
        for df in [-1, 1]:
            end_rank_idx = start_rank_idx
            end_file_idx = start_file_idx + df
            while end_file_idx >= 0 and end_file_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_file_idx += df

        # Check vertical squares
        for dr in [-1, 1]:
            end_rank_idx = start_rank_idx + dr
            end_file_idx = start_file_idx
            while end_rank_idx >= 0 and end_rank_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_rank_idx += dr

        # Check diagonal squares
        for dr, df in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            end_rank_idx = start_rank_idx + dr
            end_file_idx = start_file_idx + df
            while end_rank_idx >= 0 and end_rank_idx <= 7 and end_file_idx >= 0 and end_file_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None:
                    valid_moves.append((end_rank_idx, end_file_idx))
                elif end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))
                    break
                else:
                    break
                end_rank_idx += dr
                end_file_idx += df

        return valid_moves

    def __str__(self):
        return f'{self.color}Q'


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def get_valid_moves(self, board, start_rank_idx, start_file_idx):
        valid_moves = []

        # Check all possible knight moves
        for dr, df in [(1, 2), (2, 1), (-1, 2), (2, -1), (-2, 1), (1, -2), (-1, -2), (-2, -1)]:
            end_rank_idx = start_rank_idx + dr
            end_file_idx = start_file_idx + df
            if end_rank_idx >= 0 and end_rank_idx <= 7 and end_file_idx >= 0 and end_file_idx <= 7:
                end_piece = board.get_piece(end_rank_idx, end_file_idx)
                if end_piece is None or end_piece.color != self.color:
                    valid_moves.append((end_rank_idx, end_file_idx))

        return valid_moves

    def __str__(self):
        return f'{self.color}N'
