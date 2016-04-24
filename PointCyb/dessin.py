#!/usr/bin/env python

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

points = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
#            if event.buttons[0]:
            if pygame.mouse.get_pressed()[0]:
                points.append([event.pos, (0, 0, 255)])
            if pygame.mouse.get_pressed()[1]:
                points.append([event.pos, (0, 255, 0)])
            if pygame.mouse.get_pressed()[2]:
                points.append([event.pos, (255, 0, 0)])
    
    screen.fill((255,255,255))
        
#    if len(points) >= 3:
#        pygame.draw.polygon(screen, (0,255,0), points)
    for point in points:
        pygame.draw.circle(screen, point[1], point[0], 5)
        
    pygame.display.update()
    
