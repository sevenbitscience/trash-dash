import pygame


class Player:
    position = pygame.Vector2(100, 400)
    velocity = pygame.Vector2(0, 0)
    speed = 2
    # drag = 0.1
    frame = 0
    costume = 0
    walk = [pygame.image.load("assets/gfx/walking/Dino R1.png"), pygame.image.load("assets/gfx/walking/Dino R2.png"),
            pygame.image.load("assets/gfx/walking/Dino R3.png"), pygame.image.load("assets/gfx/walking/Dino R4.png"),
            pygame.image.load("assets/gfx/walking/Dino R5.png"), pygame.image.load("assets/gfx/walking/Dino R6.png")]
    idle = pygame.image.load("assets/gfx/dino.png")
    duck_walk = [pygame.image.load("assets/gfx/DuckDino/Duck R1.png"), pygame.image.load(
        "assets/gfx/DuckDino/Duck R2.png"),
                 pygame.image.load("assets/gfx/DuckDino/Duck R3.png"), pygame.image.load(
            "assets/gfx/DuckDino/Duck R4.png"),
                 pygame.image.load("assets/gfx/DuckDino/Duck R5.png"), pygame.image.load(
            "assets/gfx/DuckDino/Duck R6.png")]
    duck_idle = pygame.image.load("assets/gfx/DuckDino/Duck Idle.png")
    robo_walk = [pygame.image.load("assets/gfx/RoboDino/ROBO R1.png"), pygame.image.load(
        "assets/gfx/RoboDino/ROBO R2.png"),
                 pygame.image.load("assets/gfx/RoboDino/ROBO R3.png"), pygame.image.load(
            "assets/gfx/RoboDino/ROBO R4.png"),
                 pygame.image.load("assets/gfx/RoboDino/ROBO R5.png"), pygame.image.load(
            "assets/gfx/RoboDino/ROBO R6.png")]
    robo_idle = pygame.image.load("assets/gfx/RoboDino/Dino Bot Idle.png")
    rightSprite = idle
    rightSprite = pygame.transform.scale(rightSprite, (60, 60))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite

    def animate(self):
        if self.frame >= len(self.walk):
            self.frame = 0

        if self.costume == 0:
            self.rightSprite = self.walk[self.frame]
        if self.costume == 1:
            self.rightSprite = self.robo_walk[self.frame]
        elif self.costume == 2:
            self.rightSprite = self.duck_walk[self.frame]

        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
        self.frame += 1

    def reset(self):
        if self.costume == 0:
            self.rightSprite = self.idle
        if self.costume == 1:
            self.rightSprite = self.robo_idle
        elif self.costume == 2:
            self.rightSprite = self.duck_idle

        self.rightSprite = pygame.transform.scale(self.rightSprite, (60, 60))
        self.leftSprite = pygame.transform.flip(self.rightSprite, True, False)
