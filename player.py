import pygame


class Player:
    position = pygame.Vector2()
    position.xy = 100, 400
    velocity = pygame.Vector2()
    velocity.xy = 0, 0
    speed = 2
    # drag = 0.1
    frame = 0
    walk = [pygame.image.load("gfx/walking/Dino R1.png"), pygame.image.load("gfx/walking/Dino R2.png"),
            pygame.image.load("gfx/walking/Dino R3.png"), pygame.image.load("gfx/walking/Dino R4.png"),
            pygame.image.load("gfx/walking/Dino R5.png"), pygame.image.load("gfx/walking/Dino R6.png")]
    rightSprite = pygame.image.load("gfx/dino.png")
    rightSprite = pygame.transform.scale(rightSprite, (60, 60))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite

    def animate(self):
        if self.frame >= len(self.walk):
            self.frame = 0
        self.rightSprite = self.walk[self.frame]
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
        self.frame += 1

    def reset(self):
        self.rightSprite = pygame.image.load("gfx/dino.png")
        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
