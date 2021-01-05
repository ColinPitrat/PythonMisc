import pygame
import random
import os
import sys
from pygame.locals import *

pygame.init()

width, height = 1280, 1024
screen = pygame.display.set_mode((width, height))

current_path = os.path.dirname(__file__) # Where your .py file is located
resource_path = os.path.join(current_path, 'resources') # The resource folder path
image_path = os.path.join(resource_path, 'images') # The image folder path

demons = pygame.image.load(os.path.join(image_path, 'horse.png')).convert_alpha()
actions = [
    ('idle', 4),
    ('walk', 7),
    ('attack1', 4),
    ('die', 8),
]
demons = pygame.image.load(os.path.join(image_path, 'horse2.png')).convert_alpha()
actions = [
    ('idle', 4),
    ('walk', 7),
    ('attack1', 5),
    ('die', 8),
]

orientations=8

demon = []
for j in range(orientations):
  demon.append([])
  idx = 0
  for i, (name, frames) in enumerate(actions):
    demon[j].append([])
    for k in range(frames):
        demon[j][i].append([])
        demon[j][i][k] = pygame.Surface((128, 128), flags=HWSURFACE | SRCALPHA)
        demon[j][i][k].blit(demons, (0, 0), area=(128*idx, 128*j, 128, 128))
        idx += 1

NB_FRAMES=100

exit = False
orient = 2
action = 0
# Sprite 1 is the "rest" one. Adding NB_FRAMES-1 ensures the sprite is animated
# when moving no matter how small the movement is.
frame = 0
pos = [100, 100]
while not exit:
    screen.fill((100, 200, 100))

    for o in range(orientations):
        screen.blit(demon[o][action][(frame // NB_FRAMES) % len(demon[o][action])], (pos[0] + o*128, pos[1]))

    pygame.display.flip()
    frame += 1

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit = True
        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit = True
            if event.key == pygame.K_UP:
                orient = 2
            if event.key == pygame.K_DOWN:
                orient = 6
            if event.key == pygame.K_LEFT:
                orient = 0
            if event.key == pygame.K_RIGHT:
                orient = 4
            if event.key == pygame.K_n:
                action = (action + 1) % len(actions)
                print("Action: %s" % actions[action][0])
            if event.key == pygame.K_p:
                action = (action - 1) % len(actions)
                print("Action: %s" % actions[action][0])

pygame.quit()
