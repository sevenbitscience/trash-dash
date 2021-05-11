import pygame
import random


class Trash:
    trashSprites = [pygame.image.load("gfx/appleCore.png"), pygame.image.load("gfx/soda.png"), pygame.image.load(
        "gfx/dino.png"), pygame.image.load("gfx/coin.png")]

    def __init__(self, screenheight):
        self.screenheight = screenheight
        self.size = random.randrange(20, 30)
        self.sprite = self.trashSprites[random.randint(0, len(self.trashSprites)-1)]
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        self.sprite = pygame.transform.rotate(self.sprite, random.randrange(0, 360))
        self.position = pygame.Vector2()
        self.position.xy = random.randrange(370, 1100), random.randrange(-500, -50)
        self.speed = random.randrange(5, 10) / 10

    def fall(self):
        if self.position.y < self.screenheight:
            self.position.y += self.speed
        else:
            self.__init__(self.screenheight)
