#!/usr/bin/python2
import sys, pygame, time, random, string
pygame.init()

size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Deminage")

explosion = pygame.mixer.Sound("ressources/bombe.wav")
victoire = pygame.mixer.Sound("ressources/clairon.wav")

explosion_surfaces = []
for i in range(1, 17):
    explosion_surfaces.append(pygame.image.load("ressources/explosion/explosion_%02d.png" % i))

background = pygame.image.load("ressources/bombe.png")

def init_game():
    global proposition, status, status2, toGuess, seconds, duration, begintime, endtime, playing, exploding
    proposition = ''
    status = 'Entrez le code pour desamorcer'
    status2 = ''
    toGuess = random.randint(0, 99999)
    seconds = duration = 90
    playing = False
    exploding = False

init_game()

e_offset=0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_r:
                init_game()
            if event.key == pygame.K_RETURN and len(proposition) > 0:
                if int(proposition) > toGuess:
                    status = "Trop grand !"
                elif int(proposition) < toGuess:
                    status = "Trop petit !"
                else:
                    status = "Bombe desamorcee."
                    status2 = "Pressez R pour reccommencer."
                    victoire.play()
                    playing = False
                proposition = ''
            if event.key == pygame.K_BACKSPACE:
                proposition = proposition[:-1]
            if event.unicode in string.digits and len(proposition) < 5:
                if not playing:
                    playing = True
                    begintime = time.clock()
                proposition = proposition + event.unicode

    if playing:
        seconds = duration - (time.clock() - begintime)
        if seconds <= 0:
            seconds = 0
            explosion.play()
            playing = False
            exploding = True
            endtime = time.clock()

    screen.blit(background, (0, 0))
    if exploding:
        screen.blit(explosion_surfaces[e_offset], (0, 0))
        e_offset = int(time.clock()*10 - endtime*10)
        if e_offset > len(explosion_surfaces)-1:
            exploding = False
            e_offset = 0
            init_game()
    else:
        font = pygame.font.SysFont("arial", 80);
        compte_a_rebours = '%02d:%02d' % (int(seconds / 60), seconds % 60)
        compte_a_rebours_surface = font.render(compte_a_rebours, True, (255, 0, 0))
        proposition_surface = font.render(proposition, True, (255, 0, 0))
        font2 = pygame.font.SysFont("arial", 14);
        status_surface = font2.render(status, True, (255, 0, 0))
        status2_surface = font2.render(status2, True, (255, 0, 0))

        # Max size of surface is 219x90, position of upper left corner are resp. 165x240 and 165x360
        screen.blit(compte_a_rebours_surface, (165+219 - compte_a_rebours_surface.get_width(), 230))
        screen.blit(proposition_surface, (165+219 - proposition_surface.get_width(), 350))
        screen.blit(status_surface, (165+219 - status_surface.get_width(), 317))
        screen.blit(status2_surface, (165+219 - status2_surface.get_width(), 437))

    pygame.display.flip()
