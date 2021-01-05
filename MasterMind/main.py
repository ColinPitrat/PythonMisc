#!/usr/bin/python
# -*- coding: utf8 -*-"

import pygame, random, math, time, sys

#############
# Constants #
#############
resolution = width, height = 700, 800

colors = [
  (255,   0,   0), # Red
  (  0, 255,   0), # Light green
  (  0,   0, 255), # Blue
  (  0, 255, 255), # Cyan
  (255,   0, 255), # Magenta
  (255, 255,   0), # Yellow
  (127, 255,   0), # Orange
  (  0, 127,   0), # Dark green
  (255, 255, 255), # White
]

black = (  0,   0,   0)
brown = ( 44,  21,   3)

nb_lines = 10
nb_slots = 4
slot_radius = 20
slot_margin = 10
score_margin = 2
score_radius = (slot_radius // 2) - score_margin

board_x_margin = 30
board_y_margin = 20
board_height = 2 * board_y_margin + 2 * (nb_lines + 2) * (slot_radius + slot_margin)
board_width = 2*board_x_margin + 2 * (nb_slots + 1) * (slot_radius + slot_margin)
board_x = (width - board_width) // 2
board_y = (height - board_height) // 2


def display_board(screen, board):
    pygame.draw.rect(screen, brown, (board_x, board_y, board_width, board_height))
    for i in range(nb_lines+2):
        # Margin between the "to guess" and the trials
        if i == 1: continue
        for j in range(nb_slots):
            if i == 0:
                pygame.draw.circle(screen, black, (board_x + board_x_margin + (2*j+1)*(slot_radius+slot_margin), board_y + board_y_margin + (2*i+1)*(slot_radius+slot_margin)), slot_radius)
            else:
                pygame.draw.circle(screen, black, (board_x + board_x_margin + (2*j+1)*(slot_radius+slot_margin), board_y + board_y_margin + (2*i+1)*(slot_radius+slot_margin)), slot_radius)
        # No score for the "to guess"
        if i == 0: continue
        for dx in range(2):
            for dy in range(2):
                pygame.draw.circle(screen, black, (board_x + board_x_margin + (2*nb_slots+1)*(slot_radius+slot_margin) + (2*dx+1)*(score_radius+score_margin), board_y + board_y_margin + (2*i)*(slot_radius+slot_margin) + slot_margin + (2*dy+1)*(score_radius+score_margin)), score_radius)


def game_loop():
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Mastermind")

    quit = False
    while quit != True:
        # Boucle d'evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit = True

        # Affichage
        screen.fill(black)
        display_board(screen, None)
        pygame.display.flip()


def main():
    pygame.init()
    game_loop()
    pygame.quit()

if __name__ == '__main__':
    main()
