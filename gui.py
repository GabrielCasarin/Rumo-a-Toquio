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

SCREEN      = pygame.display.set_mode((800,600))

IMG_NAMES   = [
                "Blue-battleaxehide",      "Blue-swordhide",         "Red-spearhide",
                "Blue-battleaxehideused",  "Blue-swordhideused",     "Red-spearhideused",
                "Blue-battleaxe",          "Blue-sword",             "Red-spear",
                "Blue-battleaxeused",      "Blue-swordused",         "Red-spearused",
                "Blue-spearhide",          "Red-battleaxehide",      "Red-swordhide",
                "Blue-spearhideused",      "Red-battleaxehideused",  "Red-swordhideused",
                "Blue-spear",              "Red-battleaxe",          "Red-sword",
                "Blue-spearused",          "Red-battleaxeused",      "Red-swordused"
              ]
IMAGES      = {
                name: pygame.image.load("SamurAI-Images/{}.png".format(name)).convert_alpha()
                for name in IMG_NAMES
              }


class Samurai(pygame.sprite.Sprite):
    def __init__(self, img_name, center):
        super(Samurai, self).__init__()
        self.image = IMAGES[img_name]
        self.rect = self.image.get_rect(center=center)
        print(self.image.get_size())

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)


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

    def draw(self, surface):
        for casa in self.casas.values():
            pygame.draw.rect(surface, casa["cor"], casa["rect"])
            pygame.draw.rect(surface, (0,0,0), casa["rect"].copy(), 2)

class Cliente:
    def __init__(self):
        
        self.board = Board(15)

        self.screen = SCREEN
        self.screen.fill((255,255,255))

        # tabuleiro = self.request_turn()
        # for i in range(len(tabuleiro)):
        #     tabuleiro[i] = tabuleiro[i].split()
        #     for j in range(len(tabuleiro[i])):
        #         self.board.casas[(i,j)]['cor'] = cores[tabuleiro[i][j]]

        self.samurais = {
                "blue_1": Samurai("Blue-battleaxe", self.board.casas[(7,14)]["rect"].center),
                "blue_2": Samurai("Blue-spear", self.board.casas[(14,14)]["rect"].center),
                "blue_3": Samurai("Blue-sword", self.board.casas[(14,7)]["rect"].center),
                "red_1": Samurai("Red-battleaxe", self.board.casas[(7,0)]["rect"].center),
                "red_2": Samurai("Red-spear", self.board.casas[(0,0)]["rect"].center),
                "red_3": Samurai("Red-sword", self.board.casas[(0,7)]["rect"].center),
        }

    def run(self):
        self.board.draw(self.screen)
        for samurai in self.samurais:
            self.samurais[samurai].draw(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            pygame.display.update()

    def request_turn(self):
        texto = open('info.txt').read().split('\\n')
        tabuleiro = texto[7:]
        return tabuleiro

Cliente().run()