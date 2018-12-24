import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()

# display
display_width = 900
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TANKS')
theme = pygame.image.load('image.jpg')

# colours
white = (255, 255, 225)
black = (0, 0, 0)
grey = (25, 25, 25)
red = (255, 0, 0)
orange = (255, 100, 0)
blue = (0, 100, 255)
rand_colour = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256))

# font types
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

# tank data
tank_hight = 20
tank_width = 40
wheel_radius = 4
turret_width = 4

# obstacles
wall_thickness = display_width * 0.05
wall_hight = display_height * 0.4


def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(display_width / 2), int(display_height / 2) + y_displace)
    gameDisplay.blit(textSurf, textRect)


def pause():
    gamePaused = True

    while gamePaused:
        gameDisplay.blit(theme, (0, 0))
        message_to_screen("GAME PAUSED", orange, -100, "large")
        message_to_screen("Press C to continue or Q to quit", black, 100, "small")
        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_c:
                    gamePaused = False

                if event.key == pygame.K_b:
                    game_intro()

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def tank1(x, y):
    pygame.draw.circle(gameDisplay, black, (x, y), int(tank_hight / 2))
    pygame.draw.rect(gameDisplay, black, (int(x - (tank_width / 2)), y, tank_width, tank_hight))
    for i in range(1, int(tank_width / (2 * wheel_radius))):
        pygame.draw.circle(gameDisplay, black,
                           (int((x - (tank_width / 2)) + 2 * wheel_radius * i), y + tank_hight),
                           wheel_radius)

    pygame.display.update()


def tank2(x, y):
    pygame.draw.circle(gameDisplay, black, (x, y), int(tank_hight / 2))
    pygame.draw.rect(gameDisplay, black, (int(x - (tank_width / 2)), y, tank_width, tank_hight))
    for i in range(1, int(tank_width / (2 * wheel_radius))):
        pygame.draw.circle(gameDisplay, black,
                           (int((x - (tank_width / 2)) + 2 * wheel_radius * i), y + tank_hight),
                           wheel_radius)

    pygame.display.update()


def turret_position(x, y, beta):
    alfa = (beta / 180) * math.pi
    L = 25
    Lx = L * math.cos(alfa)
    Ly = L * math.sin(alfa)
    x1 = Lx + x
    y1 = y - Ly

    pygame.draw.line(gameDisplay, black, (x, y), (x1, y1), 5)
    pygame.display.update()

    return x1, y1, beta


def fire(x, y, z, beta, gamma):
    x1, y1, beta = turret_position(x, y, beta)
    t = 0

    alfa = (beta / 180) * math.pi
    V = 100
    Vx = V * math.cos(alfa)
    Vy = V * math.sin(alfa)
    a = 10

    fireShot = True

    while fireShot:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        x2 = int(x1 + Vx * t)
        y2 = int(y1 - Vy * t + ((a * (t ** 2)) / 2))
        t += (0.2)

        if x2 > display_width or x2 < 0:
            fireShot = False
        if y2 >= int(y + tank_hight + (wheel_radius / 2)):
            fireShot = False

        gameDisplay.blit(theme, (0, 0))
        pygame.draw.circle(gameDisplay, blue, (x2, y2), 5)
        obstacles(y)
        tank1(x, y)
        turret_position(x, y, beta)
        tank2(z, y)
        turret_position(z, y, gamma)
        pygame.display.update()


def obstacles(y):
    pygame.draw.rect(gameDisplay, grey, (0, int(y + tank_hight + (wheel_radius / 2)), display_width,
                                         int(display_height - (y + tank_hight + (wheel_radius / 2)))))
    pygame.draw.rect(gameDisplay, grey, (int((display_width / 2) - (wall_thickness / 2)), int(
        display_height - wall_hight - (display_height - y - tank_hight - (wheel_radius / 2))), wall_thickness,
                                         wall_hight))


def game_intro():
    gameDisplay.blit(theme, (0, 0))
    message_to_screen("Welcome to TANKS!", black, -100, 'large')
    message_to_screen("Press S to start, P to pause or Q to quit", white, 100)
    pygame.display.update()

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    intro = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def game_loop():
    tank1_x = int(display_width * 0.1)
    tank_y = int(display_height * 0.9)
    tank2_x = int(display_width * 0.9)

    TurrPos1 = 60
    TurrPos2 = 120
    tank_move = 0
    currTurrPos = 0
    turn = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q:
                    gameExit = True

                elif event.key == pygame.K_LEFT:
                    tank_move = -5

                elif event.key == pygame.K_RIGHT:
                    tank_move = 5

                elif event.key == pygame.K_UP:
                    currTurrPos = 1

                elif event.key == pygame.K_DOWN:
                    currTurrPos = -1

                elif event.key == pygame.K_p:
                    pause()

                elif event.key == pygame.K_SPACE:
                    if turn % 2 == 0:
                        fire(tank1_x, tank_y, tank2_x, TurrPos1, TurrPos2)
                    else:
                        fire(tank2_x, tank_y, tank1_x, TurrPos2, TurrPos1)
                    turn += 1


            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    currTurrPos = 0

        if TurrPos1 >= 180:
            TurrPos1 = 180
        elif TurrPos1 <= 0:
            TurrPos1 = 0
        if tank1_x >= int(display_width / 2 - wall_thickness / 2 - tank_width / 2):
            tank1_x = int(display_width / 2 - wall_thickness / 2 - tank_width / 2)
        elif tank1_x <= int(0 + (tank_width / 2)):
            tank1_x = int(0 + (tank_width / 2))

        if TurrPos2 >= 180:
            TurrPos2 = 180
        elif TurrPos2 <= 0:
            TurrPos2 = 0
        if tank2_x <= int(display_width / 2 + wall_thickness / 2 + tank_width / 2):
            tank2_x = int(display_width / 2 + wall_thickness / 2 + tank_width / 2)
        elif tank2_x >= int(display_width - (tank_width / 2)):
            tank2_x = int(display_width - (tank_width / 2))

        if turn % 2 == 0:
            tank1_x += tank_move
            TurrPos1 += currTurrPos

        else:
            tank2_x += tank_move
            TurrPos2 -= currTurrPos

        gameDisplay.blit(theme, (0, 0))
        obstacles(tank_y)
        tank1(tank1_x, tank_y)
        turret_position(tank1_x, tank_y, TurrPos1)
        tank2(tank2_x, tank_y)
        turret_position(tank2_x, tank_y, TurrPos2)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()


game_intro()
game_loop()
