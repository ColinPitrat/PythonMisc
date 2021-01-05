#!/usr/bin/python2
import sys, pygame, random, time, pygame.gfxdraw
pygame.init()

size = width, height = 1600, 1000
black = 0, 0, 0
blue = 0, 0, 255
white = 255, 255, 255

speed = 5
nb_etoiles = 1000
delay_between_shoots = 20
size_laser = 20
speed_laser = 10
min_proba_asteroide = 50
max_proba_asteroide = 900
total_proba_asteroide = 1000
speed_increase_proba = 100
asteroide_min_x_speed = 1
asteroide_max_x_speed = 10
asteroide_min_y_speed = -1
asteroide_max_y_speed = 1
asteroide_points = 1
max_energie = 10

screen = pygame.display.set_mode(size)
pygame.display.set_caption("StarWars")

score = 0
energie = max_energie
vaisseau = pygame.image.load("ressources/z95.png")
vaisseau_rect = vaisseau.get_rect()
vaisseau_rect.top = (height - vaisseau_rect.height) / 2
aster = []
for i in range(1,10):
    aster.append(pygame.image.load("ressources/ovni1/ovni%s.png" % i))
aster_rect = aster[0].get_rect()
explode = []
for i in range(1,8):
    explode.append(pygame.image.load("ressources/explosion1/explode%s.png" % i))
explode_rect = explode[0].get_rect()

son_explosion = pygame.mixer.Sound("ressources/explode.wav")
son_laser = pygame.mixer.Sound("ressources/laser.wav")

can_shoot = 0
increase_proba = 0
proba_asteroide = min_proba_asteroide
lasers = []
etoiles = []
asteroides = []
explosions = []
for i in range(0, nb_etoiles):
    color =  random.randint(0, 255)
    etoiles.append([random.randint(0, width), (random.randint(0, height)), (color, color, color)])
loops = 0

fps_begin = pygame.time.get_ticks()
fps_count = 0
while 1:
    begin_loop = pygame.time.get_ticks()
    old_rect = vaisseau_rect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        if vaisseau_rect.left > 0:
            vaisseau_rect.left -= speed
    if pressed_keys[pygame.K_RIGHT]:
        if vaisseau_rect.right < width:
            vaisseau_rect.left += speed
    if pressed_keys[pygame.K_UP]:
        if vaisseau_rect.top > 0:
            vaisseau_rect.top -= speed
    if pressed_keys[pygame.K_DOWN]:
        if vaisseau_rect.bottom < height:
            vaisseau_rect.top += speed
    if pressed_keys[pygame.K_SPACE]:
        if can_shoot == 0 and energie > 0:
            lasers.append([vaisseau_rect.left + 50, vaisseau_rect.top + 22])
            son_laser.play()
            can_shoot = delay_between_shoots

    if can_shoot > 0:
        can_shoot -= 1

    if increase_proba > speed_increase_proba and energie > 0:
        proba_asteroide += 1;
        increase_proba = 0

    if random.randint(0, total_proba_asteroide) < proba_asteroide:
        x = width
        y = random.randint(0, height)
        dx = random.randint(asteroide_min_x_speed, asteroide_max_x_speed)
        #dy = random.randint(asteroide_min_y_speed, asteroide_max_y_speed)
        dy = random.randint(-dx/10, dx/10)
        asteroides.append([x, y, dx, dy, 0])

    screen.fill(black)
    for etoile in etoiles:
        pygame.gfxdraw.pixel(screen, etoile[0], etoile[1], etoile[2])
        etoile[0] -= 1
        if etoile[0] <= 0:
            color =  random.randint(0, 255)
            etoile[0] = width
            etoile[1] = random.randint(0, height)
            etoile[2] = (color, color, color)

    for asteroide in asteroides:
        aster_rect.left = asteroide[0]
        aster_rect.top = asteroide[1]
        screen.blit(aster[asteroide[4]], aster_rect)
        asteroide[0] -= asteroide[2]
        asteroide[1] -= asteroide[3]
        if loops % 3 == 0:
            asteroide[4] = (asteroide[4] + 1) % len(aster)
        if vaisseau_rect.colliderect(aster_rect) and energie > 0:
            energie -= asteroide_points
            asteroides.remove(asteroide)
            explosions.append([asteroide[0], asteroide[1], 0])
            son_explosion.play()
            explosions.append([vaisseau_rect.left, vaisseau_rect.top, 0])
            son_explosion.play()
        elif asteroide[0] + aster_rect.width <= 0 or asteroide[1] + aster_rect.height <= 0 or asteroide[1] >= height:
                asteroides.remove(asteroide)
        else:
            for laser in lasers:
                if aster_rect.collidepoint(laser[0] + size_laser, laser[1]):
                    asteroides.remove(asteroide)
                    score += asteroide_points
                    explosions.append([asteroide[0], asteroide[1], 0])
                    son_explosion.play()
                    lasers.remove(laser)

    for explosion in explosions:
        explode_rect.left = explosion[0]
        explode_rect.top = explosion[1]
        screen.blit(explode[explosion[2]], explode_rect)
        if loops % 3 == 0:
            explosion[2] = explosion[2] + 1
        if explosion[2] >= len(explode):
            explosions.remove(explosion)

    if energie > 0:
        screen.blit(vaisseau, vaisseau_rect)
    else:
        font = pygame.font.SysFont("arial", 80);
        game_over = font.render("Game over !", True, (255, 0, 0))
        screen.blit(game_over, ((width - game_over.get_width()) / 2, (height - game_over.get_height()) / 2))

    font = pygame.font.SysFont("arial", 20);
    level = (proba_asteroide - min_proba_asteroide) // 10 + 1
    information = font.render("Level: %s - Energie: %s - Score: %s" % (level, energie * 100 / max_energie, score), True, (255, 0, 0))
    screen.blit(information, (width - information.get_width(), 0))


    for laser in lasers:
        pygame.gfxdraw.hline(screen, laser[0], laser[0] + size_laser, laser[1], blue)
        pygame.gfxdraw.hline(screen, laser[0], laser[0] + size_laser, laser[1]+1, black)
        laser[0] += speed_laser
        if laser[0] > width:
            lasers.remove(laser)

    pygame.display.flip()
    loops += 1
    increase_proba += 1
    fps_count += 1

    while pygame.time.get_ticks() - begin_loop < 15:
        time.sleep(0.001)

    if pygame.time.get_ticks() - fps_begin > 1000:
        print("%s FPS" % ((1000 * fps_count) / (pygame.time.get_ticks() - fps_begin)));
        fps_begin = pygame.time.get_ticks()
        fps_count = 0
