import time

import pygame
from Board.board import ChessBoard


class ChessGUI:
    def __init__(self, width, height, board):
        self.width = width
        self.height = height
        self.square_size = self.width // 8
        self.board = board
        self.selected_piece = None
        self.start_row = None
        self.start_col = None

        # Colors
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click()

            self.draw_board()
            self.highlight_valid_moves()
            pygame.display.flip()
            self.clock.tick(1000)


        pygame.quit()

    def handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // self.square_size
        row = mouse_pos[1] // self.square_size
        print(row,col)
        if self.selected_piece:
            self.board.move_piece((self.start_row, self.start_col), (row, col))
            self.selected_piece = None
        else:
            selected_piece = self.board.get_piece(row, col)
            if selected_piece and selected_piece.color == self.board.turn and \
                    selected_piece.get_valid_moves_with_check(self.board, row, col):
                self.selected_piece = selected_piece
                self.start_row = row
                self.start_col = col

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                square_color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                pygame.draw.rect(self.screen, square_color,
                                 (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

                piece = self.board.get_piece(row, col)
                if piece:
                    # You can customize the piece rendering here
                    piece_image = pygame.image.load(f'images/{piece}.png')
                    piece_image = pygame.transform.scale(piece_image, (self.square_size, self.square_size))
                    self.screen.blit(piece_image, (col * self.square_size, row * self.square_size))

                if self.selected_piece and (row, col) in self.selected_piece.get_valid_moves_with_check(self.board, row, col):
                    pygame.draw.rect(self.screen, (0, 255, 0, 100), (
                    col * self.square_size, row * self.square_size, self.square_size, self.square_size))

    def highlight_valid_moves(self):
        if self.selected_piece:
            piece = self.board.get_piece(self.start_row, self.start_col)
            valid_moves = piece.get_valid_moves_with_check(self.board, self.start_row, self.start_col)
            if not valid_moves:
                return

            shadow_surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            shadow_surface.fill((0, 0, 0, 80))

            for move in valid_moves:
                row, col = move
                square_rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size,
                                          self.square_size)
                self.screen.blit(shadow_surface, square_rect)
    def check_winner(self):
        if self.board.is_check('w'):

        elif self.board.is_check('w'):

