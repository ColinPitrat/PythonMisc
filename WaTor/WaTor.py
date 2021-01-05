#!/usr/bin/python
# -*- coding: utf8 -*-"

import pygame
import pygame.gfxdraw
import random
import numpy

def powerOf2(n):
    """Returns whether n is a power of 2"""
    return (n > 0) and ((n & (n-1)) == 0)

def powerOf2exponent(n):
    """Returns the base 2 logarithm of n. If n is not a power of 2, this is rounded down."""
    r = 0
    while (n > 1):
        r += 1
        n >>= 1
    return r

def make_fastrandom():
    while True:
        l = numpy.random.randint(4, size=1000000)
        for e in l:
            yield e

class WaTor(object):

    maskFish = 0x8000
    maskShark = 0x4000
    maskChronon = 0x3FFF
    maskEnergy = 0x7FFF0000
    maskMove = 0x80000000
    energyUnit = 0x00010000
    shiftEnergy = 16
    # TODO: make these parameters
    fishReproduce = 10
    sharkReproduce = 20
    sharkEnergy = 20 << shiftEnergy

    def __init__(self, w, h):
        if not powerOf2(w) or not powerOf2(h):
            raise Exception("WaTor width & height must be powers of 2")
        self.__width = w
        self.__widthMask = w-1
        self.__widthShift = powerOf2exponent(w)
        self.__height = h
        self.__heightMask = (h-1)
        self.__heightMaskInIdx = (self.__heightMask << self.__widthShift)
        self.__maskCurrentMove = self.maskMove
        self.__fastrandom = make_fastrandom()
        self.__r04 = range(0,4)
        self.reseau = [0] * (self.__width*self.__height)
        self.__directions = [-self.__width, self.__width, -1, 1]
        self.__mask_idx = self.__width * self.__height - 1

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def idx(self, x, y):
        #return ((y%self.__height) * self.__width) + (x % self.__width)
        return ((y & self.__heightMask) << self.__widthShift) + (x & self.__widthMask)

    def x_from_idx(self, idx):
        return (idx & self.__widthMask)

    def y_from_idx(self, idx):
        return ((idx & self.__heightMaskInIdx) >> self.__widthShift)

    def add_fish(self, x, y):
        self.reseau[self.idx(x,y)] = self.__maskCurrentMove | self.maskFish | self.fishReproduce

    def add_shark(self, x, y):
        self.reseau[self.idx(x,y)] = self.__maskCurrentMove | self.maskShark | self.sharkReproduce | self.sharkEnergy

    def is_empty(self, x, y):
        return self.reseau[self.idx(x,y)] == 0

    def is_fish(self, x, y):
        return (self.reseau[self.idx(x,y)] & self.maskFish) != 0

    def is_shark(self, x, y):
        return (self.reseau[self.idx(x,y)] & self.maskShark) != 0

    def display(self, ecran):
        for idx, val in enumerate(self.reseau):
            if val != 0:
                couleur = vert
                if (val & self.maskShark):
                    couleur = bleu
                x = self.x_from_idx(idx)
                y = self.y_from_idx(idx)
                pygame.gfxdraw.box(ecran, (x, y, 2, 2), couleur)

    def shark_hunt(self, idx, c, maskNextMove):
        # TODO: deduplicate with move_common
        i = self.__fastrandom.next()
        for j in self.__r04:
            k = i+j
            nidx = (idx + self.__directions[k&3]) & self.__mask_idx
            if self.reseau[nidx] & self.maskFish:
                if c == 0:
                    val = maskNextMove | self.maskShark | self.sharkReproduce | self.sharkEnergy
                    self.reseau[idx] = val
                    self.reseau[nidx] = val
                else:
                    self.reseau[idx] = 0
                    self.reseau[nidx] = maskNextMove | self.maskShark | c | self.sharkEnergy
                return True
        return False

    def move_common(self, idx, c, val, reproduce, maskNextMove):
        # Les poissons et les requins qui ne chassent pas bougent aleatoirement vers un emplacement voisin libre si possible
        i = self.__fastrandom.next()
        for j in self.__r04:
            k = i+j
            nidx = (idx + self.__directions[k&3]) & self.__mask_idx
            if self.reseau[nidx] == 0:
                if c == 0:
                    val = maskNextMove | val | reproduce
                    self.reseau[idx] = val
                    self.reseau[nidx] = val
                else:
                    self.reseau[idx] = 0
                    self.reseau[nidx] = maskNextMove | val | c
                return

    def move_shark(self, idx, c, maskNextMove, e):
        e -= self.energyUnit
        # Les requins meurent si ils n'ont plus d'energie
        if e <= 0:
            self.reseau[idx] = 0
            return
        # Sinon ils privilegient la chasse
        if self.shark_hunt(idx, c, maskNextMove):
            return
        self.move_common(idx, c, self.maskShark | e, self.sharkReproduce, maskNextMove)

    def move_fish(self, idx, c, maskNextMove):
        self.move_common(idx, c, self.maskFish, self.fishReproduce, maskNextMove)

    def move(self):
        maskNextMove = self.__maskCurrentMove ^ self.maskMove
        for idx, val in enumerate(self.reseau):
            if (val & self.maskMove == self.__maskCurrentMove) and val:
                c = val & self.maskChronon
                if c > 0:
                    c -= 1

                shark = (val & self.maskShark)
                if shark:
                    self.move_shark(idx, c, maskNextMove, val & self.maskEnergy)
                else:
                    self.move_fish(idx, c, maskNextMove)

        self.__maskCurrentMove = maskNextMove


if __name__ == '__main__':
    # Profiling
    import cProfile, pstats, StringIO
    pr = cProfile.Profile()
    pr.enable()

    pygame.init()

    ##############
    # Constantes #
    ##############
    resolution = largeur, hauteur = 256, 256

    noir = 0, 0, 0
    rouge = 255, 0, 0
    vert = 0, 255, 0
    bleu = 0, 0, 255
    cyan = 0, 255, 255
    magenta = 255, 0, 255
    jaune = 255, 255, 0
    blanc = 255, 255, 255

    #####################
    # Boucle principale #
    #####################
    quitter = False
    wator = WaTor(largeur, hauteur)
    ecran = pygame.display.set_mode(resolution)
    i = 0
    wator.add_fish(128, 128)
    while quitter != True:
        # Boucle d'evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitter = True
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
                x = event.pos[0]
                y = event.pos[1]
                if x < largeur and y < hauteur:
                  if pygame.mouse.get_pressed()[0]:
                    wator.add_shark(x, y)
                  if pygame.mouse.get_pressed()[2]:
                    wator.add_fish(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitter = True
                elif event.key == pygame.K_r:
                    wator = Wator(largeur, hauteur)

        # Calcul de la generation suivante
        wator.move()

        # Affiche le resultat
        ecran.fill(noir)
        wator.display(ecran)
        pygame.display.flip()
        i += 1
        if i == 50:
            wator.add_shark(128, 128)
        if i == 1000:
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
