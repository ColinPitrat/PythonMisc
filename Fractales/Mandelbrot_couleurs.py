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
iterDepth = 1
couleur = 255
incrementsCouleur = [ 0x100, -1, 0x10000, -0x100, 1, -0x10000 ]
limitesCouleur = [ 0xFFFF, 0xFF00, 0xFFFF00, 0xFF0000, 0xFF00FF, 0xFF ]
etapeCouleur = 0
vitesseCouleur = 5

expr = None
ix = None
iy = None
c = None
img = None
z = None

def exprinit():
    global iterDepth, expr
    depth = iterDepth
    expr = 'z**2+c'
    for _ in xrange(depth-1):
        expr = '({expr})**2+c'.format(expr=expr)
    print 'Expression used:', expr

def init():
    global ix, iy, c, img, z, couleur, etapeCouleur, i
    i = 0
    couleur = 255
    etapeCouleur = 0
    ix, iy = numpy.mgrid[0:largeur, 0:hauteur]
    x = numpy.linspace(minX, maxX, largeur)[ix]
    y = numpy.linspace(maxY, minY, hauteur)[iy]
    c = x+complex(0,1)*y
    img = numpy.zeros(c.shape, dtype=int)
    ix.shape = largeur*hauteur
    iy.shape = largeur*hauteur
    c.shape = largeur*hauteur
    z = numpy.copy(c)

def trf():
    global expr, ix, iy, c, img, z, couleur, incrementsCouleur, limitesCouleur, etapeCouleur, iterDepth, vitesseCouleur
    for v in range(1, vitesseCouleur*iterDepth):
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
pygame.display.set_caption("Ensemble de Mandelbrot")
exprinit()
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
            if event.key == pygame.K_r:
                init()
            if event.key == pygame.K_f:
                vitesseCouleur += 1
                init()
            if event.key == pygame.K_s:
                vitesseCouleur -= 1
                init()
            if event.key == pygame.K_p:
                maxIterations *= 2
            if event.key == pygame.K_m:
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
        i += iterDepth
        ecran.fill(noir)
        pygame.surfarray.blit_array(ecran, trf())
        infos = police.render("Iter=%s/%s - Zoom=%s - VCol=%s" % (i, maxIterations, zoom, vitesseCouleur), True, rouge)
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
