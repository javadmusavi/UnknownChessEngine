from . import Rook, Knight, Pawn, Queen, Bishop, King
from tabulate import tabulate


class ChessBoard:
    def __init__(self):
        self.board = {
            0: Rook('b'), 1: Knight('b'), 2: Bishop("b"), 3: Queen('b'),
            4: King('b'), 5: Bishop('b'), 6: Knight("b"), 7: Rook("b"),
            8: Pawn("b"), 9: Pawn("b"), 10: Pawn("b"), 11: Pawn("b"),
            12: Pawn("b"), 13: Pawn("b"), 14: Pawn("b"), 15: Pawn("b"),

            48: Pawn("w"), 49: Pawn("w"), 50: Pawn("w"), 51: Pawn("w"),
            52: Pawn("w"), 53: Pawn("w"), 54: Pawn("w"), 55: Pawn("w"),
            56: Rook("w"), 57: Knight("w"), 58: Bishop("w"), 59: Queen("w"),
            60: King("w"), 61: Bishop("w"), 62: Knight("w"), 63: Rook("w"),
        }
        self.white_pieces = 0xFFFF000000000000
        self.black_pieces = 0x000000000000FFFF
        self.piece_counts = {'K': 2, 'Q': 2, 'R': 4, 'B': 4, 'N': 4, 'P': 16}
        self.turn = 'w'
        self.history = []

    def __str__(self):
        board_str = ''
        for i in range(8):
            for j in range(8):
                square = i * 8 + j
                if square in self.board:
                    if self.board[square] is None:
                        board_str += '.'
                    else:
                        board_str += str(self.board[square])

                else:
                    board_str += '. '
                board_str += ' '
            board_str += '\n'

        rows = board_str.split("\n")
        data = [row.split() for row in rows]

        table = tabulate(data)
        return table
    def move_piece(self, start_square, end_square):
        if type(start_square) == str:
            start_file, start_rank = start_square[0], start_square[1]
            end_file, end_rank = end_square[0], end_square[1]
            start_file_idx, start_rank_idx = ord(start_file) - 97, 8 - int(start_rank)
            end_file_idx, end_rank_idx = ord(end_file) - 97, 8 - int(end_rank)
        elif type(start_square) == int:
            start_file_idx, start_rank_idx = start_square / 10, start_square % 10
            end_file_idx, end_rank_idx = end_square / 10, end_square % 10
        elif type(start_square) == tuple:
            start_rank_idx, start_file_idx = start_square[0], start_square[1]
            end_rank_idx, end_file_idx = end_square[0], end_square[1]

        piece = self.get_piece(start_rank_idx, start_file_idx)
        if piece is None:
            return False

        if self.turn != piece.color:
            return False


        valid_moves = piece.get_valid_moves_with_check(self, start_rank_idx, start_file_idx)


        if (end_rank_idx, end_file_idx) not in valid_moves:
            return False

        captured_piece = self.get_piece(end_rank_idx, end_file_idx)
        self.set_piece(piece, end_rank_idx, end_file_idx)

        del self.board[start_rank_idx * 8 + start_file_idx]

        self.history.append({
            'piece': piece,
            'start_square': start_square,
            'end_square': end_square,
            'captured_piece': captured_piece
        })

        self.turn = 'b' if self.turn == 'w' else 'w'
        return True

    def simulate_move_piece(self, start_square, end_square):
        if type(start_square) == str:
            start_file, start_rank = start_square[0], start_square[1]
            end_file, end_rank = end_square[0], end_square[1]
            start_file_idx, start_rank_idx = ord(start_file) - 97, 8 - int(start_rank)
            end_file_idx, end_rank_idx = ord(end_file) - 97, 8 - int(end_rank)
        elif type(start_square) == int:
            start_file_idx, start_rank_idx = start_square / 10, start_square % 10
            end_file_idx, end_rank_idx = end_square / 10, end_square % 10
        elif type(start_square) == tuple:
            start_rank_idx, start_file_idx = start_square[0], start_square[1]
            end_rank_idx, end_file_idx = end_square[0], end_square[1]

        piece = self.get_piece(start_rank_idx, start_file_idx)
        if piece is None:
            return False

        valid_moves = piece.get_valid_moves(self, start_rank_idx, start_file_idx)

        if (end_rank_idx, end_file_idx) not in valid_moves:
            return False

        captured_piece = self.get_piece(end_rank_idx, end_file_idx)
        self.set_piece(piece, end_rank_idx, end_file_idx)

        del self.board[start_rank_idx * 8 + start_file_idx]

        self.history.append({
            'piece': piece,
            'start_square': start_square,
            'end_square': end_square,
            'captured_piece': captured_piece
        })

        return True

    def get_piece(self, rank_idx, file_idx):
        return self.board.get(rank_idx * 8 + file_idx)

    def set_piece(self, piece, rank_idx, file_idx):
        self.board[rank_idx * 8 + file_idx] = piece

    def find_king(self, color):
        for position, piece in self.board.items():
            if type(piece) == King and piece.color == color:
                return position
        return False

    def is_check(self, color):
        # Find the king's position
        king_position = self.find_king(color)

        # Iterate through all opponent's pieces
        king_rank_file = self.convert_position_to_rank_file(king_position)
        for position, piece in self.board.items():
            if piece.color != color:
                rank, file = self.convert_position_to_rank_file(position)

                valid_moves = piece.get_valid_moves(self, rank, file)
                if king_rank_file in valid_moves:
                    return True
        return False

    def undo_move(self):
        if type(self.history[-1]['start_square']) == str:

            start_rank, start_file = self.convert_geometric_to_rank_file_index(self.history[-1]['start_square'])
            self.set_piece(self.history[-1]['piece'], start_rank, start_file)

            if self.history[-1]['captured_piece']:
                self.board[self.convert_geometric_to_position(self.history[-1]['end_square'])] = self.history[-1][
                    'captured_piece']
            else:
                try:
                    del self.board[self.convert_geometric_to_position(self.history[-1]['end_square'])]
                except KeyError:
                    pass
        elif type(self.history[-1]['start_square']) == tuple:
            self.set_piece(self.history[-1]['piece'], self.history[-1]['start_square'][0],
                           self.history[-1]['start_square'][1])

            if self.history[-1]['captured_piece']:
                self.board[self.convert_rank_file_to_position(self.history[-1]['end_square'][0],
                                                              self.history[-1]['end_square'][1])] = self.history[-1][
                    'captured_piece']
            else:
                try:
                    del self.board[
                        self.convert_rank_file_to_position(self.history[-1]['end_square'][0], self.history[-1]['end_square'][1])]
                except KeyError:
                    pass
        elif type(self.history[-1]['start_square']) == int:
            rank, file = self.convert_position_to_rank_file(self.history[-1]['start_square'])
            self.set_piece(self.history[-1]['piece'], rank, file)

            if self.history[-1]['captured_piece']:
                self.board[self.history[-1]['end_square']] = self.history[-1]['captured_piece']
            else:
                try:
                    del self.board[self.history[-1]['end_square']]
                except KeyError:
                    pass

    def check_winner(self, color):
        pass
    @staticmethod
    def convert_position_to_rank_file(position):
        return position // 8, position % 8

    @staticmethod
    def convert_geometric_to_rank_file_index(rank_file):
        file_label = rank_file[0]  # Extract the file label
        rank_label = int(rank_file[1])  # Extract the rank label as integer
        file_idx = ord(file_label) - ord('a')  # Convert file label to index
        rank_idx = 8 - rank_label  # Convert rank label to index
        return rank_idx, file_idx

    @staticmethod
    def convert_geometric_to_position(rank_file):
        start_file_idx, start_rank_idx = ord(rank_file[0]) - 97, 8 - int(rank_file[1])
        return start_rank_idx * 8 + start_file_idx

    @staticmethod
    def convert_rank_file_to_position(rank, file):
        return rank * 8 + file
