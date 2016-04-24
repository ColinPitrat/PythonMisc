#!/usr/bin/python2
import sys, pygame, random
pygame.init()

size = width, height = 800, 600
black = 0, 0, 0
nb_balls = 3
minspeed = 1
maxspeed = 10

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Balle rebondissante")

ball = pygame.image.load("ressources/ball.gif")
ballsrects = []

def add_ball():
    ballsrects.append([ball.get_rect(), [random.randint(minspeed, maxspeed), random.randint(minspeed, maxspeed)]])
    ballsrects[-1][0].left = random.randint(0, width - ball.get_rect().width)
    ballsrects[-1][0].top = random.randint(0, height - ball.get_rect().height)

def remove_ball():
    if len(ballsrects) > 0:
        ballsrects.pop()

for i in range(1, nb_balls):
    add_ball()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_a:
                add_ball()
            if event.key == pygame.K_r:
                remove_ball()

    screen.fill(black)

    for i in range(0, len(ballsrects)):
        ballsrects[i][0] = ballsrects[i][0].move(ballsrects[i][1])
        if ballsrects[i][0].left < 0 or ballsrects[i][0].right > width:
            ballsrects[i][1][0] = -ballsrects[i][1][0]
        if ballsrects[i][0].top < 0 or ballsrects[i][0].bottom > height:
            ballsrects[i][1][1] = -ballsrects[i][1][1]
        screen.blit(ball, ballsrects[i][0])
#    for br in ballsrects:
#        br = br[0].move(br[1])
#        if br.left < 0 or br.right > width:
#            speed[0] = -speed[0]
#        if br.top < 0 or br.bottom > height:
#            speed[1] = -speed[1]
#        screen.blit(ball, br)

    pygame.display.flip()
