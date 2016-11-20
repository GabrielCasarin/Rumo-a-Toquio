import pygame


class Samurai(pygame.sprite.Sprite):
    def __init__(self):
        super(Samurai, self).__init__()

    def update(self):
        pass


class Board(pygame.sprite.Sprite):
    def __init__(self):
        super(Board, self).__init__()

    def update(self):
        pass


class Game(object):
    def __init__(self, size, dimension):
        super(Game, self).__init__()
        self._setup()
        self.size = size
        self.dimension = dimension
        # instancia uma tela
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((255,255,255))
        for x in range(0, self.size[0], self.size[0]/self.dimension):
            for y in range(0, self.size[1], self.size[1]/self.dimension):
                pygame.draw.rect(self.screen, (0,0,0) , (x,y,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
        pygame.display.update()

        # [coluna, linha]
        self.quadrado_atual = [0, 0]


    def _setup(self):
        pygame.init()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # sys.exit()

                elif event.type == pygame.KEYDOWN:
                    # pra cima = diminuir linha
                    if event.key == pygame.K_UP:
                        pygame.draw.rect(self.screen, (0,0,0) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        if self.quadrado_atual[1] > 0:
                            self.quadrado_atual[1] -= 1
                        pygame.draw.rect(self.screen, (0,0,255) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        pygame.display.update()
                        print("subir:", self.quadrado_atual)
                    # pra baixo = aumentar linha
                    elif event.key == pygame.K_DOWN:
                        pygame.draw.rect(self.screen, (0,0,0) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        if self.quadrado_atual[1] < self.dimension:
                            self.quadrado_atual[1] += 1
                        pygame.draw.rect(self.screen, (0,0,255) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        pygame.display.update()                            
                        print("descer:", self.quadrado_atual)
                    # pra esquerda = diminuir coluna
                    elif event.key == pygame.K_LEFT:
                        pygame.draw.rect(self.screen, (0,0,0) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        if self.quadrado_atual[0] > 0:
                            self.quadrado_atual[0] -= 1
                        pygame.draw.rect(self.screen, (0,0,255) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        pygame.display.update()
                        print("esquerda:", self.quadrado_atual)
                    # pra direita = aumentar coluna
                    elif event.key == pygame.K_RIGHT:
                        pygame.draw.rect(self.screen, (0,0,0) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        if self.quadrado_atual[0] < self.dimension:
                            self.quadrado_atual[0] += 1
                        pygame.draw.rect(self.screen, (0,0,255) , (self.quadrado_atual[0]*self.size[0]/self.dimension,self.quadrado_atual[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        pygame.display.update()
                        print("descer:", self.quadrado_atual)
                    elif (event.key == pygame.K_RETURN
                          or event.key == pygame.K_KP_ENTER):
                        self.quadrado_selecionado = list(self.quadrado_atual)
                        pygame.draw.rect(self.screen, (255,0,0) , (self.quadrado_selecionado[0]*self.size[0]/self.dimension,self.quadrado_selecionado[1]*self.size[1]/self.dimension,self.size[0]/self.dimension,self.size[1]/self.dimension), 2)
                        pygame.display.update()
                        print("quadrado selecionado:", self.quadrado_selecionado)

g = Game((526,526), 15)
g.run()
