#!/usr/bin/python2
import pygame
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 200, 200

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

#############
# Variables #
#############
police = pygame.font.SysFont("arial", 15);
minX = -5.0/2
maxX = 3.0/4
minY = -3.0/2
maxY = 3.0/2
maxIterations = 256
zoom = 1.0
zoomFactor = 2.0

def converge(x, y):
    a = x
    b = y
    for i in range(0, maxIterations):
        tmp = a*a - b*b + x
        b = 2*a*b + y
        a = tmp
        if a*a + b*b > 4:
            return (int(i*255.0/maxIterations), 0, 255)
    return (0, 0, 0)
        
##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Ensemble de Mandelbrot")

quitter = False
y = 0
# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
#####################
# Boucle principale #
#####################
while quitter != True:
    # Boucle d'evenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_c:
                y = 1
            if event.key == pygame.K_p:
                maxIterations *= 2
            if event.key == pygame.K_m:
                maxIterations /= 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            centerX = minX + 1.0*event.pos[0]/largeur*(maxX-minX)
            centerY = -(minY + 1.0*event.pos[1]/hauteur*(maxY-minY))
            if pygame.mouse.get_pressed()[0]:
                print("Clic en (%s, %s) dans (%s, %s) -> (%s, %s)" % (event.pos[0], event.pos[1], minX, minY, maxX, maxY))
                newLargeur = (maxX - minX) / zoomFactor
                newHauteur = (maxY - minY) / zoomFactor
                zoom *= zoomFactor
                print("Zoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
            if pygame.mouse.get_pressed()[2]:
                newLargeur = (maxX - minX) * zoomFactor
                newHauteur = (maxY - minY) * zoomFactor
                zoom /= zoomFactor
                print("Dezoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
            y = 0
            minX = centerX - newLargeur/2.0
            maxX = centerX + newLargeur/2.0
            minY = centerY - newHauteur/2.0
            maxY = centerY + newHauteur/2.0

    if y < hauteur:
        if y == 0:
            ecran.fill(noir)
        for x in range(0, largeur):
                X = minX + 1.0*x/largeur*(maxX-minX)
                Y = -(minY + 1.0*y/hauteur*(maxY-minY))
                couleur = converge(X, Y)
                if couleur:
                    pygame.draw.line(ecran, couleur, (x, y), (x, y))
        infos = police.render("Iter=%s - Zoom=%s" % (maxIterations, zoom), True, rouge)
        ecran.blit(infos, (0, 0))
        pygame.display.flip()
        y += 1
    else:
        quitter = True

###############
# Terminaison #
###############
pygame.quit()

# Profiling
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
