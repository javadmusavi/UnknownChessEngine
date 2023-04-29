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

    def __str__(self):
        board_str = ''
        for i in range(8):
            for j in range(8):
                square = i * 8 + j
                if square in self.board:
                    board_str += self.board[square].symbol
                else:
                    board_str += '.'
                board_str += ' '
            board_str += '\n'
        return board_str

    def move_piece(self, start_sq, end_sq):
        piece = self.board[start_sq]
        del self.board[start_sq]
        self.board[end_sq] = piece

        if piece.color == 'w':
            self.white_pieces &= ~(1 << start_sq)
            self.white_pieces |= (1 << end_sq)
        else:
            self.black_pieces &= ~(1 << start_sq)
            self.black_pieces |= (1 << end_sq)

        self.piece_counts[piece.symbol] -= 1
