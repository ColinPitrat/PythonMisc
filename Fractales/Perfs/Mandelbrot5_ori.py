#!/usr/bin/python2
import pygame, numpy, numexpr
pygame.init()

##############
# Constantes #
##############
resolution = largeur, hauteur = 900, 600

noir = 0, 0, 0
rouge = 255, 0, 0
blanc = 255, 255, 255

#############
# Variables #
#############
police = pygame.font.SysFont("arial", 15);
minX = -2
maxX = 1
minY = -1
maxY = 1
maxIterations = 256
zoom = 1.0
zoomFactor = 2.0

def mandel(n, m, itermax, xmin, xmax, ymin, ymax, depth=1):
    expr = 'z**2+c'
    for _ in xrange(depth-1):
        expr = '({expr})**2+c'.format(expr=expr)
    itermax = itermax/depth
    print 'Expression used:', expr
    ix, iy = numpy.mgrid[0:n, 0:m]
    x = numpy.linspace(xmin, xmax, n)[ix]
    y = numpy.linspace(ymin, ymax, m)[iy]
    c = x+complex(0,1)*y
    del x, y # save a bit of memory, we only need z
    img = numpy.zeros(c.shape, dtype=int)
    ix.shape = n*m
    iy.shape = n*m
    c.shape = n*m
    z = numpy.copy(c)
    for i in xrange(itermax):
        if not len(z): break # all points have escaped
        z = numexpr.evaluate(expr)
        rem = abs(z)>2.0
        img[ix[rem], iy[rem]] = depth*i+1
        rem = -rem
        z = z[rem]
        ix, iy = ix[rem], iy[rem]
        c = c[rem]
    img[img==0] = 0
    return img

##################
# Initialisation #
##################
ecran = pygame.display.set_mode(resolution)
pygame.display.set_caption("Ensemble de Mandelbrot")

quitter = False
i = 0
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
                i = 0
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
            i = 0
            minX = centerX - newLargeur/2.0
            maxX = centerX + newLargeur/2.0
            minY = centerY - newHauteur/2.0
            maxY = centerY + newHauteur/2.0

    dessine = False

    if i == 0:
        i += 1
        ecran.fill(noir)
        pygame.surfarray.blit_array(ecran, mandel(largeur, hauteur, maxIterations, minX, maxX, maxY, minY, 6))
        infos = police.render("Iter=%s - Zoom=%s" % (maxIterations, zoom), True, rouge)
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
