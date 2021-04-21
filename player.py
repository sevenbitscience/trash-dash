import pygame


def animate(tick):
    print("lol")


class Player:
    position = pygame.Vector2()
    position.xy = 100, 400
    velocity = pygame.Vector2()
    velocity.xy = 0, 0
    speed = 2
    # drag = 0.1
    rightSprite = pygame.image.load("gfx/dino.png")
    rightSprite = pygame.transform.scale(rightSprite, (60, 60))
    leftSprite = pygame.transform.flip(rightSprite, True, False)
    currentSprite = rightSprite
