import pygame
import random


class Trash:
    trashSprites = [pygame.image.load("assets/gfx/appleCore.png"), pygame.image.load("assets/gfx/soda.png")]

    def __init__(self, screenheight):
        self.screenheight = screenheight
        self.size = random.randrange(20, 30)
        self.sprite = self.trashSprites[random.randint(0, len(self.trashSprites)-1)]
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        self.sprite = pygame.transform.rotate(self.sprite, random.randrange(0, 360))
        self.position = pygame.Vector2(random.randrange(370, 1100), random.randrange(-500, -50))
        self.speed = random.randrange(5, 10) / 10

    def fall(self):
        if self.position.y < self.screenheight:
            self.position.y += self.speed
        else:
            self.__init__(self.screenheight)
