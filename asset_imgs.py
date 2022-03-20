import pygame

WIDTH = 60
HEIGHT = 60

B_PAWN = pygame.transform.scale(pygame.image.load('assets/b_pawn_2x_ns.png'), (WIDTH, HEIGHT))
B_ROOK = pygame.transform.scale(pygame.image.load('assets/b_rook_2x_ns.png'), (WIDTH, HEIGHT))
B_KNIGHT = pygame.transform.scale(pygame.image.load('assets/b_knight_2x_ns.png'), (WIDTH, HEIGHT))
B_BISHOP = pygame.transform.scale(pygame.image.load('assets/b_bishop_2x_ns.png'), (WIDTH, HEIGHT))
B_QUEEN = pygame.transform.scale(pygame.image.load('assets/b_queen_2x_ns.png'), (WIDTH, HEIGHT))
B_KING = pygame.transform.scale(pygame.image.load('assets/b_king_2x_ns.png'), (WIDTH, HEIGHT))

W_PAWN = pygame.transform.scale(pygame.image.load('assets/w_pawn_2x_ns.png'), (WIDTH, HEIGHT))
W_ROOK = pygame.transform.scale(pygame.image.load('assets/w_rook_2x_ns.png'), (WIDTH, HEIGHT))
W_KNIGHT = pygame.transform.scale(pygame.image.load('assets/w_knight_2x_ns.png'), (WIDTH, HEIGHT))
W_BISHOP = pygame.transform.scale(pygame.image.load('assets/w_bishop_2x_ns.png'), (WIDTH, HEIGHT))
W_QUEEN = pygame.transform.scale(pygame.image.load('assets/w_queen_2x_ns.png'), (WIDTH, HEIGHT))
W_KING = pygame.transform.scale(pygame.image.load('assets/w_king_2x_ns.png'), (WIDTH, HEIGHT))