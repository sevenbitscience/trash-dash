import pygame
from player import Player
from trash import Trash


def check_collision(a_x, a_y, a_width, a_height, b_x, b_y, b_width, b_height):
    return (a_x + a_width > b_x) and (a_x < b_x + b_width) and (a_y + a_height > b_y) and (a_y < b_y + b_height)


def check_collision_list(a, b):
    return (a[0] + a[2] > b[0]) and (a[0] < b[0] + b[2]) and (a[1] + a[3] > b[1]) and (a[1] < b[1] + b[3])


def main():
    # start pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 640))
    pygame.display.set_caption("Trash dash")

    # Load assets for outside
    house = pygame.image.load("gfx/house.png")
    house = pygame.transform.scale(house, (1280, 640))
    atm = pygame.image.load("gfx/atm.png")
    atm = pygame.transform.scale(atm, (1280, 640))
    hud_icon_size = 60
    trash_pile = pygame.image.load("gfx/soda.png")
    trash_pile = pygame.transform.scale(trash_pile, (hud_icon_size, hud_icon_size))
    coin = pygame.image.load("gfx/coin.png")
    coin = pygame.transform.scale(coin, (hud_icon_size, hud_icon_size))
    timer_icon = pygame.image.load("gfx/hourglass-icon.png")
    timer_icon = pygame.transform.scale(timer_icon, (hud_icon_size, hud_icon_size))
    backpack_icon = pygame.image.load("gfx/backpack-icon.png")
    backpack_icon = pygame.transform.scale(backpack_icon, (hud_icon_size, hud_icon_size))

    score_font = pygame.font.Font("Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 50)
    score_color = (191, 69, 69)
    trash_text = score_font.render(str(0), True, score_color)
    score_text = score_font.render(str(0), True, score_color)
    backpack_text = score_font.render(str(10), True, score_color)
    score_holder = pygame.Rect(10, 550, 560, 80)
    barriers = [(0, 0, 320, 200), (100, 200, 70, 130)]
    shop_hitbox = (100, 230, 70, 70)

    # Load assets for the atm
    sell_font = pygame.font.Font("Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 40)
    sell_text = sell_font.render("Sell", True, (235, 235, 235))
    sell_button_color = (71, 145, 64)
    sell_button = (383, 445, 542, 80)
    sell_rect = pygame.Rect(sell_button)

    # Load assets for inside
    upgrades_font = pygame.font.Font("Fonts/Press_Start_2P/PressStart2P-Regular.ttf", 20)
    upgrade_text_color = (36, 36, 36)
    start_button = (985, 435, 205, 90)
    start_text = upgrades_font.render("Next day", True, upgrade_text_color)
    quit_button = (985, 320, 205, 90)
    quit_text = upgrades_font.render("Quit", True, (181, 23, 2))
    inside = pygame.image.load("gfx/inside.png")
    inside = pygame.transform.scale(inside, (1280, 640))

    # Load sound effects
    collect_sound = pygame.mixer.Sound("sfx/pickup.wav")
    miss_sound = pygame.mixer.Sound("sfx/miss.wav")
    select_sound = pygame.mixer.Sound("sfx/select.wav")
    coin_sound = pygame.mixer.Sound("sfx/coin.wav")
    full_sound = pygame.mixer.Sound("sfx/full.wav")
    master_volume = 0.5

    # Setup vars for in game stuff
    trash_collected = 0
    prev_trash = 0
    balance = 0
    trash_price = 5
    backpack = 10

    sell_time = 5
    sell_frames = 120

    # Setup timer
    start_ticks = pygame.time.get_ticks()
    last_seconds = -1
    total_time = 40
    time_left = total_time
    timer_width = 490
    timer_step = timer_width / time_left
    timer_rect = [610, 562, timer_width, 55]
    timer_color = [0, 255, 0]

    # start the player
    dino = Player()
    left = False

    last_time = start_ticks
    animation_fps = 100

    # create trash pieces
    trash_pieces = []

    for i in range(20):
        trash_pieces.append(Trash(screen.get_height()))

    # bools for what menu to be in
    shop_open = False
    running = False

    # main loop
    while True:
        while running:
            collect_sound.set_volume(master_volume)
            miss_sound.set_volume(master_volume/1.5)
            select_sound.set_volume(master_volume)
            full_sound.set_volume(master_volume/1.5)
            touching_trash = False
            current_ticks = pygame.time.get_ticks()
            seconds = int(((current_ticks - start_ticks) / 1000))
            if last_seconds != seconds:
                time_left -= seconds - last_seconds
                print(time_left)
                last_seconds = seconds
                timer_rect[2] = timer_width - (timer_step * (total_time - time_left))

            if time_left >= 30:
                timer_color = [103, 219, 53]
            elif 15 < time_left < 30:
                timer_color = [245, 197, 39]
            elif 0 < time_left < 15:
                timer_color = [184, 44, 22]
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
                    left = True
                if pressed[pygame.K_d]:
                    dino.velocity.x = dino.speed
                    dino.currentSprite = dino.rightSprite
                    left = False
                if pressed[pygame.K_w]:
                    dino.velocity.y = -dino.speed
                if pressed[pygame.K_s]:
                    dino.velocity.y = dino.speed

                next_x = ((dino.position.x + 54) + dino.velocity.x, (dino.position.x + 6) + dino.velocity.x)
                next_y = ((dino.position.y + 58) + dino.velocity.y, (dino.position.y + 4) + dino.velocity.y)

                if abs(dino.velocity.x) + abs(dino.velocity.y) > dino.speed:
                    dino.velocity.x /= 1.3
                    dino.velocity.y /= 1.3

                if abs(dino.velocity.x) + abs(dino.velocity.y) > 0.5:
                    if current_ticks - last_time > animation_fps:
                        dino.animate()
                        last_time = current_ticks
                else:
                    dino.reset()
                if left:
                    dino.currentSprite = dino.leftSprite
                else:
                    dino.currentSprite = dino.rightSprite

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
                        trash.__init__(screen.get_height())
                    touching_trash = True
                screen.blit(trash.sprite, (trash.position.x, trash.position.y))
                trash.fall()

            if not shop_open:
                if interact:
                    if touching_trash and trash_collected < backpack:
                        collect_sound.play((trash_collected-prev_trash)-1)
                    elif touching_trash and trash_collected >= backpack:
                        full_sound.play()
                    elif not touching_trash:
                        miss_sound.play()
                screen.blit(dino.currentSprite, (dino.position.x, dino.position.y))

                pygame.draw.rect(screen, (38, 24, 24), score_holder, 0, 10)
                screen.blit(trash_pile, (20, 560))
                screen.blit(trash_text, (80, 567))
                screen.blit(coin, (200, 560))
                screen.blit(score_text, (270, 567))
                screen.blit(backpack_icon, (400, 560))
                screen.blit(backpack_text, (460, 567))

                pygame.draw.rect(screen, (38, 24, 24), (600, 550, 560, 80), 0, 10)
                screen.blit(timer_icon, (1090, 560))
                pygame.draw.rect(screen, timer_color, timer_rect, 0, 10)

                prev_trash = trash_collected

            if shop_open:
                sell_frame_delay = sell_time * 1000 / sell_frames
                if trash_collected > 0:
                    coin_delay = (sell_frames - 5)/trash_collected
                    last_coin_frame = 0
                else:
                    coin_delay = sell_frames + 1
                    last_coin_frame = sell_frames + 1
                screen.blit(atm, (0, 0))
                pygame.draw.rect(screen, sell_button_color, sell_rect, 0, 10)
                screen.blit(sell_text, (570, 465))
                if check_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3, sell_button[0],
                                   sell_button[1], sell_button[2], sell_button[3]) and select:
                    select_sound.play()
                    for i in range(sell_frames):
                        sell_width = sell_button[2]-i*sell_button[2]/sell_frames
                        screen.blit(atm, (0, 0))
                        pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                        pygame.draw.rect(screen, sell_button_color, (sell_button[0], sell_button[1], int(sell_width),
                                                                     sell_button[3]), 0, 10)
                        screen.blit(sell_text, (570, 465))
                        if int(last_coin_frame + coin_delay) == i:
                            coin_sound.play()
                            last_coin_frame = i
                        pygame.display.update()
                        pygame.time.delay(int(sell_frame_delay))

                    screen.blit(atm, (0, 0))
                    pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                    screen.blit(sell_text, (570, 465))
                    pygame.display.update()
                    pygame.time.delay(500)
                    balance += trash_collected * trash_price
                    trash_collected = 0
                    score_text = score_font.render(str(balance), True, score_color)
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                    shop_open = False
            pygame.display.update()
        if trash_collected > 0:
            sell_frame_delay = sell_time * 1000 / sell_frames
            coin_delay = (sell_frames - 5) / trash_collected
            last_coin_frame = 0
            for i in range(sell_frames):
                sell_width = sell_button[2] - i * sell_button[2] / sell_frames
                screen.blit(atm, (0, 0))
                pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
                pygame.draw.rect(screen, sell_button_color, (sell_button[0], sell_button[1], int(sell_width),
                                                             sell_button[3]), 0, 10)
                screen.blit(sell_text, (570, 465))
                if int(last_coin_frame + coin_delay) == i:
                    coin_sound.play()
                    last_coin_frame = i
                pygame.display.update()
                pygame.time.delay(int(sell_frame_delay))

            screen.blit(atm, (0, 0))
            pygame.draw.rect(screen, (50, 50, 50), sell_rect, 0, 10)
            screen.blit(sell_text, (570, 465))
            pygame.display.update()
            pygame.time.delay(500)
            balance += trash_collected * trash_price
            trash_collected = 0
            score_text = score_font.render(str(balance), True, score_color)
            trash_text = score_font.render(str(trash_collected), True, score_color)

        while not running:
            select_sound.set_volume(master_volume)
            select = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    select = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    select_sound.play()
                    running = True
                    start_ticks = pygame.time.get_ticks()
                    last_seconds = -1
                    total_time = 40
                    time_left = total_time
                    timer_width = 490
                    timer_step = timer_width / time_left
                    timer_rect = [610, 562, timer_width, 55]
                    trash_collected = 0
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                    for trash in trash_pieces:
                        trash.__init__(screen.get_height())

            if select:
                mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 3, 3)
                if check_collision_list(mouse_pos, start_button):
                    select_sound.play()
                    running = True
                    start_ticks = pygame.time.get_ticks()
                    last_seconds = -1
                    total_time = 40
                    time_left = total_time
                    timer_width = 490
                    timer_step = timer_width / time_left
                    timer_rect = [610, 562, timer_width, 55]
                    trash_collected = 0
                    last_time = start_ticks
                    dino.position.xy = 100, 400
                    trash_text = score_font.render(str(trash_collected), True, score_color)
                    for trash in trash_pieces:
                        trash.__init__(screen.get_height())
                elif check_collision_list(mouse_pos, quit_button):
                    select_sound.play()
                    pygame.time.wait(int(select_sound.get_length()*1000))
                    return

            screen.blit(inside, (0, 0))
            # pygame.draw.rect(screen, (13, 219, 67), start_button, 0, 20)
            screen.blit(quit_text, (1050, 363))
            screen.blit(start_text, (1010, 474))
            pygame.display.update()


if __name__ == "__main__":
    main()
