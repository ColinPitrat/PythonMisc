#!/usr/bin/python2

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

points = []

black = (0, 0, 0)
white = (255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 1 est le bouton de gauche
            if event.button == 4:
                points.append(event.pos)
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[2]:
                points.append(event.pos)
   
    screen.fill(white)
        
    for point in points:
        pygame.draw.circle(screen, black, point, 5)
        
    pygame.display.update()
    
