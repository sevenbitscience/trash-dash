import pygame
import random


class Trash:
    trashSprites = [pygame.image.load("gfx/appleCore.png"), pygame.image.load("gfx/soda.png"), pygame.image.load(
        "gfx/dino.png"), pygame.image.load("gfx/coin.png")]

    def __init__(self):
        self.size = random.randrange(20, 30)
        self.sprite = self.trashSprites[random.randint(0, len(self.trashSprites)-1)]
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        self.sprite = pygame.transform.rotate(self.sprite, random.randrange(0, 360))
        self.position = pygame.Vector2()
        self.position.xy = random.randrange(370, 1100), random.randrange(-700, -50)
        self.speed = random.randrange(5, 10) / 10

    def fall(self, screenheight):
        if self.position.y < screenheight:
            self.position.y += self.speed
        else:
            self.__init__()
