import pygame
pygame.init()

cores = {
    '0': (255,0,0),
    '1': (255,100,0),
    '2': (255,0,100),
    '3': (0,0,255),
    '4': (100,0,255),
    '5': (0,100,255),
    '8': (200,200,200),
    '9': (20,20,20),
}

class Samurai(pygame.sprite.Sprite):
    def __init__(self):
        super(Samurai, self).__init__()

    def update(self):
        pass

class Board(pygame.sprite.Sprite):
    def __init__(self, n):
        super(Board, self).__init__()
        delta_x = 20
        delta_y = 20
        self.casas = {
            (i, j): {
                "rect": pygame.Rect(30*i + delta_x, 30*j + delta_y, 30, 30),
                "cor": (255,255,255)
            } for i in range(n) for j in range(n)
        }

    def update(self):
        pass


class Cliente:
    def __init__(self):
        super(Cliente, self).__init__()
        
        t = Board(15)
        screen = pygame.display.set_mode((800,600))
        screen.fill((255,255,255))

        tabuleiro = self.request_turn()
        for i in range(len(tabuleiro)):
            tabuleiro[i] = tabuleiro[i].split()
            for j in range(len(tabuleiro[i])):
                t.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]

    def run(self):
        while True:
            for casa in t.casas.values():
                pygame.draw.rect(screen, casa["cor"], casa["rect"])
                pygame.draw.rect(screen, (0,0,0), casa["rect"].copy(), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()

    def request_turn(self):
        texto = open('info.txt').read().split('\\n')
        tabuleiro = texto[7:]
        return tabuleiro
