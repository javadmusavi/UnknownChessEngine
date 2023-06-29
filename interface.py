from Board.board import ChessBoard
from GUI.gui2 import ChessGUI

board = ChessBoard()
# board.move_piece((6,4), (4,4))
# board.move_piece((1,4), (3,4))
# board.move_piece((6,3), (4,3))
# board.move_piece((1,3), (3,3))
# board.move_piece((7,5), (3,1))

# board.move_piece('c8', 'f5')


# board.move_piece('e2', 'e4')
# board.move_piece('e7', 'e5')
# board.move_piece('f1', 'b5')
# # board.move_piece('d2', 'd4')

ChessGUI(800,800,board).run()

print(board)
