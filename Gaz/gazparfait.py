#!/usr/bin/python2
# -*- coding: utf8 -*-"

import pygame, random, math, time

resolution = width, height = 800, 800

noir = 0, 0, 0
rouge = 255, 0, 0
vert = 0, 255, 0
bleu = 0, 0, 255
NB_MOLECULES = 100

molecules = []

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

class Molecule:
    MAX_X = width
    MAX_Y = height
    MAX_V = 10
    R = 10
    D = 2*R
    M = 1

    def __init__(self):
        self.x = random.randint(0, self.MAX_X)
        self.y = random.randint(0, self.MAX_Y)
        #self.x = self.MAX_X/2
        #self.y = self.MAX_Y/2
        v = random.random()*self.MAX_V
        #v = self.MAX_V/2
        theta = random.random()*2*math.pi
        #theta = random.random()*math.pi/8-9*math.pi/16
        self.vx = v*math.cos(theta)
        self.vy = v*math.sin(theta)
        self.couleur = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        #self.couleur = (self.x%255, self.y%255, int(255*v)%255)
        #self.couleur = (self.x%255, self.y%255, int(theta/2/math.pi*255))
        self.rayon = self.R
        self.masse = self.M

    def move(self):
        self.x += self.vx
        if self.x + self.rayon >= width and self.vx > 0:
            self.vx = -self.vx
            self.x += self.vx
        if self.x - self.rayon  <= 0 and self.vx < 0:
            self.vx = -self.vx
            self.x += self.vx
        self.y += self.vy
        if self.y + self.rayon >= height and self.vy > 0:
            self.vy = -self.vy
            self.y += self.vy
        if self.y - self.rayon <= 0 and self.vy < 0:
            self.vy = -self.vy
            self.y += self.vy
        #self.v = math.sqrt(self.vx**2+self.vy**2)

    def trigo(self, dx, dy):
        phi = math.atan(dy/dx)
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        return phi, cos_phi, sin_phi

    def collide(self, m):
        dmin = self.rayon + m.rayon
        if abs(self.y - m.y) < dmin and abs(self.x - m.x) < dmin:
            d = distance(self.x, self.y, m.x, m.y)
            if d < dmin and distance(self.x + self.vx, self.y + self.vy, m.x + m.vx, m.y + m.vy) < d:
                # Vecteur normale à la tangente
                dx = m.x - self.x
                dy = m.y - self.y
                #print("dx, dy = %s, %s" % (dx, dy))
                #pygame.draw.circle(ecran, rouge,  (int(m.x), int(m.y)), 20)
                #pygame.draw.line(ecran, vert,  (self.x, self.y), (m.x, m.y))
                #pygame.draw.line(ecran, vert,  (width/2, height/2), (width/2+100*dx, height/2+100*dy))
                phi = math.atan(dy/dx)
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)
                v1x = self.vx*math.cos(phi) + self.vy*math.sin(phi)
                v1y = -self.vx*math.sin(phi) + self.vy*math.cos(phi)
                v2x = m.vx*math.cos(phi) + m.vy*math.sin(phi)
                v2y = -m.vx*math.sin(phi) + m.vy*math.cos(phi)
                v1x2 = (v1x*(self.masse-m.masse)+2*m.masse*v2x)/(self.masse+m.masse)
                v2x2 = (v2x*(m.masse-self.masse)+2*self.masse*v1x)/(self.masse+m.masse)
                self.vx = v1x2*math.cos(phi)-v1y*math.sin(phi)
                self.vy = v1x2*math.sin(phi)+v1y*math.cos(phi)
                m.vx = v2x2*math.cos(phi)-v2y*math.sin(phi)
                m.vy = v2x2*math.sin(phi)+v2y*math.cos(phi)

    def project(self, m, cos_phi, sin_phi):
        v1x = self.vx*cos_phi + self.vy*sin_phi
        v1y = -self.vx*sin_phi + self.vy*cos_phi
        v2x = m.vx*cos_phi + m.vy*sin_phi
        v2y = -m.vx*sin_phi + m.vy*cos_phi
        return v1x, v1y, v2x, v2y

    def unproject(self, m, v1x, v1y, v2x, v2y, cos_phi, sin_phi):
        self.vx = v2x*cos_phi-v1y*sin_phi
        self.vy = v2x*sin_phi+v1y*cos_phi
        m.vx = v1x*cos_phi-v2y*sin_phi
        m.vy = v1x*sin_phi+v2y*cos_phi

    def collide_optim(self, m):
        d = distance(self.x, self.y, m.x, m.y)
        if d < self.D and distance(self.x + self.vx, self.y + self.vy, m.x + m.vx, m.y + m.vy) < d:
            # Vecteur normale à la tangente
            dx = m.x - self.x
            dy = m.y - self.y

            phi, cos_phi, sin_phi = self.trigo(dx, dy)
            v1x, v1y, v2x, v2y = self.project(m, cos_phi, sin_phi)

            self.unproject(m, v1x, v1y, v2x, v2y, cos_phi, sin_phi)

    def collide_all(self, molecules, i):
        xmin, xmax = self.x - self.D, self.x + self.D
        ymin, ymax = self.y - self.D, self.y + self.D
        for j in range(0, i):
            n = molecules[j]
            #self.collide(n)
            if n.x > xmin and n.x < xmax and n.y > ymin and n.y < ymax:
                self.collide_optim(n)

def reset_molecules():
    global molecules
    molecules = []
    for i in range(0, NB_MOLECULES):
        molecules.append(Molecule())

def handle_molecules(molecules, ecran):
    for i in range(0, NB_MOLECULES):
        m = molecules[i]
        m.move()
        pygame.draw.circle(ecran, m.couleur,  (int(m.x), int(m.y)), m.rayon)
        # Vecteur vitesse
        #pygame.draw.line(ecran, bleu,  (int(m.x), int(m.y)), (int(m.x+m.rayon*m.vx), int(m.y+m.rayon*m.vy)))
        m.collide_all(molecules, i)

##################
# Initialisation #
##################
pygame.init()
pygame.display.set_caption("Gaz parfait")
ecran = pygame.display.set_mode(resolution)

reset_molecules()

# Profiling
import cProfile, pstats, StringIO
pr = cProfile.Profile()
pr.enable()

quitter = False
while quitter != True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitter = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitter = True
            if event.key == pygame.K_r:
                reset_molecules()
            if event.key == pygame.K_p:
                NB_MOLECULES *= 2
                while len(molecules) < NB_MOLECULES:
                    molecules.append(Molecule())
            if event.key == pygame.K_m:
                if NB_MOLECULES > 2:
                    NB_MOLECULES /= 2

    ecran.fill(noir)
    handle_molecules(molecules, ecran)
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
