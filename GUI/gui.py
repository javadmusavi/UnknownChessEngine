import threading
import time
import pygame
import sys
from Board import board


class GUI:
    def __init__(self, board: board.ChessBoard):
        self.running = False
        self.update_thread = None
        self.board = board
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.selected_piece = None
        self.valid_moves = []

    def draw_board(self):
        square_size = self.width // 8
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = pygame.Color('white')
                else:
                    color = pygame.Color('gray')
                pygame.draw.rect(self.screen, color, (col * square_size, row * square_size, square_size, square_size))

    def draw_pieces(self):
        square_size = self.width // 8
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece is not None:
                    piece_image = pygame.image.load(f"images/{piece.color}_{type(piece).__name__}.png")
                    piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                    if (row, col) == self.selected_piece:
                        self.screen.blit(pygame.Surface((square_size, square_size), pygame.SRCALPHA),
                                         (col * square_size, row * square_size))
                    self.screen.blit(piece_image, (col * square_size, row * square_size))

    def draw(self):
        self.draw_board()
        self.draw_pieces()
        pygame.display.flip()

    def handle_click(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected_piece is None:
            if piece is not None:
                self.selected_piece = (row, col)
                self.valid_moves = piece.get_valid_moves(self.board, row, col)
        else:
            if (row, col) in self.valid_moves:
                print(self.selected_piece[0], self.selected_piece[1])
                self.board.move_piece(self.selected_piece[0] * 10 + self.selected_piece[1], row * 10 + col)
                self.selected_piece = None
                self.valid_moves = []
            else:
                self.selected_piece = None
                self.valid_moves = []
        self.draw()

    def run(self):
        self.running = True
        self.update_thread = threading.Thread(target=self.update_board, args=(self.board,), daemon=True)
        self.update_thread.start()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    row = event.pos[1] // (self.height // 8)
                    col = event.pos[0] // (self.width // 8)
                    self.handle_click(row, col)
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def update_board(self, board):
        while self.running:
            self.board = board
            time.sleep(0.1)

    def update(self, board):
        self.board = board
