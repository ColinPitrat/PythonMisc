#!/usr/bin/python2
import pygame, math
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 640, 350
#resolution = largeur, hauteur = 1024, 768

noir = 0
blanc = 255, 255, 255

A = -0.4*hauteur

x0 = largeur/2
y0 = hauteur/2

dq = 60.0
q_step = 2*dq/largeur

#############
# Variables #
#############

quitter = False
show_info = True
police = pygame.font.SysFont("arial", 20);
L = 1.0 / 640
F = -0.3
dy = -1.5
x = 0
q = 0

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)

def f(z):
    global A, L, F
    v = A*math.exp(-L*z*z)*math.cos(F*z)
#    print("f(%s) = %s" % (z, v))
    return v

def redraw():
    global ecran, noir, q, x
    ecran.fill(noir)
    q = 0
    x = 0

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()
redraw()
#####################
# Boucle principale #
#####################
while quitter == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_p:
                dy += 0.1
                redraw()
            if event.key == pygame.K_m:
                dy -= 0.1
                redraw()
            if event.key == pygame.K_w:
                L = L / 2
                redraw()
            if event.key == pygame.K_x:
                L = L * 2
                redraw()
            if event.key == pygame.K_a:
                F = F + 0.1
                redraw()
            if event.key == pygame.K_q:
                F = F - 0.1
                redraw()
            if event.key == pygame.K_i:
                show_info = not show_info

    if q < dq:
        bas = 999999
        sommet = -bas
        s1 = math.sqrt(dq*dq - q*q)
        r = s1
        while r >= -s1:
            c = f(math.sqrt(q*q+r*r))
            s = c - dy*r
            color = (255/A * abs(c)) % 255
            if s >= sommet:
                sommet = s
                pygame.draw.rect(ecran, (255, color, color), (x0 + x, y0 + s, 1, 1), 1)
                pygame.draw.rect(ecran, (255, color, color), (x0 - x, y0 + s, 1, 1), 1)
            if s < bas:
                bas = s
                pygame.draw.rect(ecran, (255, color, color), (x0 + x, y0 + s, 1, 1), 1)
                pygame.draw.rect(ecran, (255, color, color), (x0 - x, y0 + s, 1, 1), 1)
            r = r - 1
        x = x + 1
        q = q + q_step

    if show_info:
        infos = police.render("A=%s - L=%s - F=%s" % (A, L, F), True, blanc)
    ecran.blit(infos, (0, 0))
    pygame.display.flip()

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
