#!/usr/bin/python2
import pygame, numpy, numexpr
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 700, 700

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
couleur = None
incrementsCouleur = [ 0x100, -1, 0x10000, -0x100, 1, -0x10000 ]
limitesCouleur = [ 0x44FFFF, 0x44FF44, 0xFFFF44, 0xFF4444, 0xFF44FF, 0x4444FF ]
etapeCouleur = 0
vitesseCouleur = 50
# 0 = Mandelbrot, 1 = Julia
typeFractale=0
cJulia = complex(0, 1)
coefs = [ 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
currentCoef = 0

expr = None
ix = None
iy = None
c = None
img = None
z = None

def initExpr():
    global expr
    expr = 'c'
    for k in range(1, 13):
        expr = '%s + %s*z**%s' % (expr, coefs[k-1], k)
    print 'Expression used:', expr

def init():
    global ix, iy, x, y, c, img, z, i, couleur, etapeCouleur
    i = 0
    couleur = 0x4444FF
    etapeCouleur = 0
    ix, iy = numpy.mgrid[0:largeur, 0:hauteur]
    x = numpy.linspace(minX, maxX, largeur)[ix]
    y = numpy.linspace(maxY, minY, hauteur)[iy]
    z = x+complex(0,1)*y
    img = numpy.zeros(z.shape, dtype=int)
    if typeFractale == 0:
        c = numpy.copy(z)
    else:
        c = cJulia*numpy.ones(z.shape)
    ix.shape = largeur*hauteur
    iy.shape = largeur*hauteur
    c.shape = largeur*hauteur
    z.shape = largeur*hauteur

def trf():
    global expr, ix, iy, c, img, z, couleur, incrementsCouleur, limitesCouleur, etapeCouleur, vitesseCouleur
    for v in range(1, vitesseCouleur):
        if couleur == limitesCouleur[etapeCouleur]:
            etapeCouleur += 1
            if etapeCouleur >= len(incrementsCouleur):
                etapeCouleur -= len(incrementsCouleur)
        couleur += incrementsCouleur[etapeCouleur]
    if not len(z): return img
    z = numexpr.evaluate(expr)
    rem = abs(z)>2.0
    try:
        img[ix[rem], iy[rem]] = couleur
    except OverflowError:
        print("Overflow pour la couleur %s, etape %s, increment %s, limite %s" % (couleur, etapeCouleur, incrementCouleur[etapeCouleur], limitesCouleur[etapeCouleur]))
    rem = -rem
    z = z[rem]
    ix, iy = ix[rem], iy[rem]
    c = c[rem]
    return img

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Ensembles de Mandelbrot, de Julia et autres")
initExpr()
init()

quitter = False
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
            if event.key == pygame.K_j:
                typeFractale = 1
                init()
            if event.key == pygame.K_m:
                typeFractale = 0
                init()
#           Ne fonctionne pas a cause de numexpr qui a besoin d'ordonner les coefficients !!
#           (ce qui n'est pas possible si ils sont complexes)
#            if event.key == pygame.K_UP:
#                coefs[currentCoef] += complex(0,0.1)
#                initExpr()
#                init()
#            if event.key == pygame.K_DOWN:
#                coefs[currentCoef] -= complex(0,0.1)
#                initExpr()
#                init()
            if event.key == pygame.K_PAGEUP:
                coefs[currentCoef] += 0.1
                initExpr()
                init()
            if event.key == pygame.K_PAGEDOWN:
                coefs[currentCoef] -= 0.1
                initExpr()
                init()
            if event.key == pygame.K_F1:
                currentCoef = 0
            if event.key == pygame.K_F2:
                currentCoef = 1
            if event.key == pygame.K_F3:
                currentCoef = 2
            if event.key == pygame.K_F4:
                currentCoef = 3
            if event.key == pygame.K_F5:
                currentCoef = 4
            if event.key == pygame.K_F6:
                currentCoef = 5
            if event.key == pygame.K_F7:
                currentCoef = 6
            if event.key == pygame.K_F8:
                currentCoef = 7
            if event.key == pygame.K_F9:
                currentCoef = 8
            if event.key == pygame.K_F10:
                currentCoef = 9
            if event.key == pygame.K_F11:
                currentCoef = 10
            if event.key == pygame.K_F12:
                currentCoef = 11
            # Touches a et b: augmentent ou diminuent les parties reelles et imaginaires de C pour un ensemble de Julia
            if event.key == pygame.K_a and typeFractale == 1:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    cJulia += 0.01
                else:
                    cJulia -= 0.01
                init()
            if event.key == pygame.K_b and typeFractale == 1:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    cJulia += complex(0,0.01)
                else:
                    cJulia -= complex(0,0.01)
                init()
            # Touche v: augmente ou diminue la vitesse de changement de couleurs
            if event.key == pygame.K_v:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    vitesseCouleur += 1
                else:
                    vitesseCouleur -= 1
                init()
            # Touche i: augmente ou diminue le nombre d'iterations
            if event.key == pygame.K_i:
                if event.mod == pygame.KMOD_SHIFT or event.mod == pygame.KMOD_LSHIFT or event.mod == pygame.KMOD_RSHIFT:
                    maxIterations *= 2
                else:
                    maxIterations /= 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            centerX = minX + 1.0*event.pos[0]/largeur*(maxX-minX)
            centerY = minY + 1.0*(maxY-minY)*(hauteur-event.pos[1])/hauteur
            if pygame.mouse.get_pressed()[0]:
                print("Clic en (%s, %s) dans (%s, %s) -> (%s, %s)" % (event.pos[0], event.pos[1], minX, minY, maxX, maxY))
                newLargeur = (maxX - minX) / zoomFactor
                newHauteur = (maxY - minY) / zoomFactor
                zoom *= zoomFactor
                print("Zoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
            elif pygame.mouse.get_pressed()[2]:
                newLargeur = (maxX - minX) * zoomFactor
                newHauteur = (maxY - minY) * zoomFactor
                zoom /= zoomFactor
                print("Dezoom (%s, %s) => (%s, %s) (%s, %s)" % (centerX, centerY, minX, minY, maxX, maxY))
            else:
                continue
            minX = centerX - newLargeur/2.0
            maxX = centerX + newLargeur/2.0
            minY = centerY - newHauteur/2.0
            maxY = centerY + newHauteur/2.0
            init()

    dessine = False

    if i < maxIterations:
        i += 1
        ecran.fill(noir)
        pygame.surfarray.blit_array(ecran, trf())
        if typeFractale == 0:
            infos = police.render("Iter=%s/%s - Zoom=%s - VCol=%s" % (i, maxIterations, zoom, vitesseCouleur), True, rouge)
        else:
            infos = police.render("Iter=%s/%s - Zoom=%s - VCol=%s - C=%s" % (i, maxIterations, zoom, vitesseCouleur, cJulia), True, rouge)
        ecran.blit(infos, (0, 0))
        pygame.display.flip()
    # Activer (en mettant 'and True') pour le profiling
    if i >= maxIterations and False:
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
