class ChessBoard:
    def __init__(self):
        self.board = {
            0: Piece('R', 'b'), 1: Piece('N', 'b'), 2: Piece('B', 'b'), 3: Piece('Q', 'b'),
            4: Piece('K', 'b'), 5: Piece('B', 'b'), 6: Piece('N', 'b'), 7: Piece('R', 'b'),
            8: Piece('P', 'b'), 9: Piece('P', 'b'), 10: Piece('P', 'b'), 11: Piece('P', 'b'),
            12: Piece('P', 'b'), 13: Piece('P', 'b'), 14: Piece('P', 'b'), 15: Piece('P', 'b'),

            48: Piece('P', 'w'), 49: Piece('P', 'w'), 50: Piece('P', 'w'), 51: Piece('P', 'w'),
            52: Piece('P', 'w'), 53: Piece('P', 'w'), 54: Piece('P', 'w'), 55: Piece('P', 'w'),
            56: Piece('R', 'w'), 57: Piece('N', 'w'), 58: Piece('B', 'w'), 59: Piece('Q', 'w'),
            60: Piece('K', 'w'), 61: Piece('B', 'w'), 62: Piece('N', 'w'), 63: Piece('R', 'w'),
        }
        self.white_pieces = 0xFFFF000000000000
        self.black_pieces = 0x000000000000FFFF
        self.piece_counts = {'K': 2, 'Q': 2, 'R': 4, 'B': 4, 'N': 4, 'P': 16}
        self.turn = 'w'

    def __str__(self):
        board_str = ''
        for i in range(8):
            for j in range(8):
                square = i * 8 + j
                if square in self.board:
                    board_str += str(self.board[square])
                else:
                    board_str += '. '
                board_str += ' '
            board_str += '\n'
        return board_str

    def move_piece(self, start_square, end_square):
        start_file, start_rank = start_square[0], start_square[1]
        end_file, end_rank = end_square[0], end_square[1]
        start_file_idx, start_rank_idx = ord(start_file) - 97, int(start_rank) - 1
        end_file_idx, end_rank_idx = ord(end_file) - 97, int(end_rank) - 1
        print(start_rank_idx, start_file_idx)
        piece = self.board.get((7-start_rank_idx)*8 +start_file_idx)
        if piece is None:
            return False

        if self.turn != piece.color:
            return False

        valid_moves = piece.get_valid_moves(self, start_rank_idx, start_file_idx)
        if (end_rank_idx, end_file_idx) not in valid_moves:
            return False

        captured_piece = self.board[end_rank_idx][end_file_idx]
        self.board[end_rank_idx][end_file_idx] = self.board[start_rank_idx][start_file_idx]
        self.board[start_rank_idx][start_file_idx] = '.'

        self.history.append({
            'piece': piece,
            'start_square': start_square,
            'end_square': end_square,
            'captured_piece': captured_piece
        })

        self.turn = 'black' if self.turn == 'white' else 'white'

        return True


class Piece:
    """Class representing a chess piece."""

    def __init__(self, piece_type, color):
        self.piece_type = piece_type  # 'K', 'Q', 'R', 'B', 'N', or 'P'
        self.color = color  # 'w' for white, 'b' for black
        self.has_moved = False  # Whether the piece has moved yet in the game

    def __str__(self):
        """Return the string representation of the piece."""
        return self.color + self.piece_type

    def generate_moves(self, board, x, y):
        """Generate all possible moves for the piece at position (x, y) on the board."""
        # TODO: Implement this function


board = ChessBoard()
print(board)
board.move_piece('e2','e4')