import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()

# display
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('TANKS')

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
wall_thickness = 140
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


def fading_display():
    dy = int((display_height)/255)
    for i in range(130):
        colour = (i, i, i)
        pygame.draw.rect(gameDisplay, colour, (0, int((i*dy)), display_width, display_height - i*dy))


def pause():
    gamePaused = True

    while gamePaused:
        gameDisplay.fill(white)
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


def tank(x, y):
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

    pygame.draw.line(gameDisplay, black, (x, y-5), (x1, y1), 5)
    pygame.display.update()

    return x1, y1, beta


def fire(x, y, beta):
    x1, y1, beta = turret_position(x, y, beta)
    t = 0

    alfa = (beta / 180) * math.pi
    V = 40
    Vx = V * math.cos(alfa)
    Vy = V * math.sin(alfa)
    a = 2

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

        t += (1 / 2)
        x2 = int(x1 + Vx * t)
        y2 = int(y1 - Vy * t + ((a * (t ** 2)) / 2))

        pygame.draw.circle(gameDisplay, blue, (x2, y2), 5)
        pygame.display.update()
        if x2 > display_width or x2 < 0:
            fireShot = False
        if y2 >= int(y + tank_hight + (wheel_radius / 2)):
            pygame.time.delay(0)
            fireShot = False

        gameDisplay.fill(black)
        fading_display()
        obstacles(y)
        tank(x, y)
        turret_position(x, y, beta)


def obstacles(y):
    pygame.draw.rect(gameDisplay, grey, (0, int(y + tank_hight + (wheel_radius / 2)), display_width,
                                          int(display_height - (y + tank_hight + (wheel_radius / 2)))))
    pygame.draw.rect(gameDisplay, grey, (int((display_width / 2) - (wall_thickness / 2)), int(
        display_height - wall_hight - (display_height - y - tank_hight - (wheel_radius / 2))), wall_thickness,
                                          wall_hight))


def game_intro():
    gameDisplay.fill(black)
    fading_display()
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
    tank_x = int(display_width * 0.1)
    tank_y = int(display_height * 0.9)
    tank_move = 0
    TurrPos = 60
    currTurrPos = 0

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
                    fire(tank_x, tank_y, TurrPos)
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tank_move = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    currTurrPos = 0

        gameDisplay.fill(black)
        fading_display()
        obstacles(tank_y)
        tank_x += tank_move
        TurrPos += currTurrPos

        if TurrPos >= 180:
            TurrPos = 180
        elif TurrPos <= 0:
            TurrPos = 0
        if tank_x >= int(display_width / 2 - wall_thickness / 2 - tank_width / 2):
            tank_x = int(display_width / 2 - wall_thickness / 2 - tank_width / 2)
        elif tank_x <= int(0 + (tank_width / 2)):
            tank_x = int(0 + (tank_width / 2))

        tank(tank_x, tank_y)
        turret_position(tank_x, tank_y, TurrPos)
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()


game_intro()
game_loop()
