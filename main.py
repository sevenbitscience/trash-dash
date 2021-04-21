import pygame
from player import Player
from trash import Trash


def check_collision(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)


def main():
    pygame.init()

    playing = True

    screen = pygame.display.set_mode((1280, 640))
    pygame.display.set_caption("Trash dash")
    house = pygame.image.load("gfx/house.png")
    house = pygame.transform.scale(house, (1280, 640))
    atm = pygame.image.load("gfx/atm.png")
    atm = pygame.transform.scale(atm, (1280, 640))
    trash_pile = pygame.image.load("gfx/soda.png")
    hud_icon_size = 60
    trash_pile = pygame.transform.scale(trash_pile, (hud_icon_size, hud_icon_size))
    coin = pygame.image.load("gfx/coin.png")
    coin = pygame.transform.scale(coin, (hud_icon_size, hud_icon_size))
    score_font = pygame.font.Font("Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 50)
    score_color = (191, 69, 69)
    trash_text = score_font.render(str(0), True, score_color)
    score_text = score_font.render(str(0), True, score_color)
    score_holder = pygame.Rect(10, 550, 500, 80)

    collect_sound = pygame.mixer.Sound("sfx/pickup.wav")
    miss_sound = pygame.mixer.Sound("sfx/miss.wav")
    select_sound = pygame.mixer.Sound("sfx/select.wav")
    coin_sound = pygame.mixer.Sound("sfx/coin.wav")
    full_sound = pygame.mixer.Sound("sfx/full.wav")

    master_volume = 0.5

    sell_button = (383, 445, 542, 80)
    sell_rect = pygame.Rect(sell_button)

    barriers = [(0, 0, 320, 200), (100, 200, 70, 130)]
    shop_hitbox = (100, 230, 70, 70)

    trash_collected = 0
    prev_trash = 0
    balance = 0
    trash_price = 5
    backpack = 10

    start_ticks = pygame.time.get_ticks()
    last_seconds = -1
    total_time = 60
    time_left = total_time
    timer_width = 490
    timer_step = timer_width / time_left
    timer_rect = [540, 562, timer_width, 55]
    timer_color = [0, 255, 0]

    dino = Player()

    trash_pieces = []
    for i in range(20):
        trash_pieces.append(Trash())

    for trash in trash_pieces:
        trash.fall(screen.get_height())

    shop_open = False
    running = True

    # main loop
    while True:
        while running:
            collect_sound.set_volume(master_volume)
            miss_sound.set_volume(master_volume/1.5)
            select_sound.set_volume(master_volume)
            full_sound.set_volume(master_volume/2)
            touching_trash = False
            seconds = int(((pygame.time.get_ticks() - start_ticks) / 1000))
            if last_seconds != seconds:
                time_left -= seconds - last_seconds
                print(time_left)
                last_seconds = seconds
                timer_rect[2] = timer_width - (timer_step * (total_time - time_left))

            if time_left >= 30:
                timer_color = [0, 255, 0]
            elif 15 < time_left < 30:
                timer_color = [255, 255, 0]
            elif 0 < time_left < 15:
                timer_color = [255, 0, 0]
            elif time_left <= 0:
                running = False

            dino.velocity.xy = 0, 0
            interact = False
            select = False

            pressed = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    interact = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    select = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    trash_collected = 0
                    time_left = 60
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    shop_open = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = False

            if not shop_open:
                if pressed[pygame.K_a]:
                    dino.velocity.x = -dino.speed
                    dino.currentSprite = dino.leftSprite
                if pressed[pygame.K_d]:
                    dino.velocity.x = dino.speed
                    dino.currentSprite = dino.rightSprite
                if pressed[pygame.K_w]:
                    dino.velocity.y = -dino.speed
                if pressed[pygame.K_s]:
                    dino.velocity.y = dino.speed

                next_x = ((dino.position.x + 54) + dino.velocity.x, (dino.position.x + 6) + dino.velocity.x)
                next_y = ((dino.position.y + 58) + dino.velocity.y, (dino.position.y + 4) + dino.velocity.y)

                if abs(dino.velocity.x) + abs(dino.velocity.y) > dino.speed:
                    dino.velocity.x /= 1.3
                    dino.velocity.y /= 1.3

                for i in range(len(barriers)):
                    if barriers[i][0] < next_x[0] < barriers[i][0] + barriers[i][2] and barriers[i][1] + \
                            barriers[i][3] > next_y[0] > barriers[i][1]:
                        dino.velocity.x = 0

                    if next_y[0] < barriers[i][1] + barriers[i][3] and barriers[i][0] + barriers[i][2] > next_x[0] \
                            > barriers[i][0]:
                        dino.velocity.y = 0

                if not screen.get_width() >= next_x[0] or not next_x[1] >= 0:
                    dino.velocity.x = 0

                if not 540 >= next_y[0] or not next_y[1] >= 0:
                    dino.velocity.y = 0

                dino.position.x += dino.velocity.x
                dino.position.y += dino.velocity.y
            if check_collision(dino.position.x, dino.position.y, 50, 50,
                               shop_hitbox[0], shop_hitbox[1], shop_hitbox[2], shop_hitbox[3]) and interact:
                shop_open = True

            screen.blit(house, (0, 0))
            for trash in trash_pieces:
                if check_collision(dino.position.x, dino.position.y, 50, 50, trash.position.x,
                                   trash.position.y, 20, 20) and interact:
                    if trash_collected < backpack:
                        trash_collected += 1
                        trash_text = score_font.render(str(trash_collected), True, score_color)
                        trash.__init__()
                    touching_trash = True
                screen.blit(trash.sprite, (trash.position.x, trash.position.y))
                trash.fall(screen.get_height())

            if not shop_open:
                if interact:
                    if touching_trash and trash_collected < backpack:
                        collect_sound.play((trash_collected-prev_trash)-1)
                    elif touching_trash and trash_collected >= backpack-1:
                        full_sound.play()
                    elif not touching_trash:
                        miss_sound.play()

                screen.blit(dino.currentSprite, (dino.position.x, dino.position.y))

                pygame.draw.rect(screen, (38, 24, 24), score_holder, 0, 10)
                screen.blit(trash_pile, (20, 558))
                screen.blit(trash_text, (80, 565))
                screen.blit(coin, (200, 558))
                screen.blit(score_text, (280, 565))

                pygame.draw.rect(screen, (38, 24, 24), (530, 550, 500, 80), 0, 10)
                pygame.draw.rect(screen, timer_color, timer_rect, 0, 10)

                prev_trash = trash_collected

            if shop_open:
                sell_time = 5
                sell_frames = 120
                sell_frame_delay = sell_time * 1000 / sell_frames
                if trash_collected > 0:
                    coin_delay = sell_frames/trash_collected
                    last_coin_frame = 0
                    print(coin_delay)
                else:
                    coin_delay = sell_frames + 1
                    last_coin_frame = sell_frames + 1
                screen.blit(atm, (0, 0))
                pygame.draw.rect(screen, (0, 255, 0), sell_rect, 0, 10)
                if check_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3, sell_button[0],
                                   sell_button[1], sell_button[2], sell_button[3]) and select:
                    select_sound.play()
                    for i in range(sell_frames):
                        sell_width = sell_button[2]-i*sell_button[2]/sell_frames
                        screen.blit(atm, (0, 0))
                        pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                        pygame.draw.rect(screen, (0, 255, 0), (sell_button[0], sell_button[1], int(sell_width),
                                                               sell_button[3]), 0, 10)
                        if int(last_coin_frame + coin_delay) == i:
                            coin_sound.play()
                            last_coin_frame = i
                        pygame.display.update()
                        pygame.time.delay(int(sell_frame_delay))

                    if trash_collected > 0 and trash_collected != 7:
                        coin_sound.play()

                    screen.blit(atm, (0, 0))
                    pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                    pygame.display.update()
                    pygame.time.delay(500)
                    balance += trash_collected * trash_price
                    trash_collected = 0
                    score_text = score_font.render(str(balance), True, score_color)
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                    shop_open = False

            pygame.display.update()
        balance += trash_collected * trash_price
        score_text = score_font.render(str(balance), True, score_color)
        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    running = True
                    start_ticks = pygame.time.get_ticks()
                    last_seconds = -1
                    time_left = total_time
                    timer_width = 300
                    timer_step = timer_width / time_left
                    timer_rect = [540, 562, timer_width, 55]
                    timer_color = [0, 255, 0]
                    trash_collected = 0
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                    for trash in trash_pieces:
                        trash.__init__()
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), screen.get_height()))
            pygame.display.update()


if __name__ == "__main__":
    main()
