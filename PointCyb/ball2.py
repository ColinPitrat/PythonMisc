#!/usr/bin/python2
import sys, pygame, time
pygame.init()

size = width, height = 1366, 768
speed = [1, 1]
black = 0, 0, 0
white = 255, 255, 255
angle = 0
anglespeed = 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ressources/ball.gif")
ballcenter = pygame.Rect(ball.get_width() / 2, ball.get_height() / 2, ball.get_width(), ball.get_height())
ballcorner = pygame.Rect(0, 0, ball.get_width(), ball.get_height())
blitrect = ball.get_rect()

def increase_speed(delta):
    for direction in [0, 1]:
        if speed[direction] != 0 or delta > 0:
            if speed[direction] >= 0:
                speed[direction] = speed[direction] + delta
            else:
                speed[direction] = speed[direction] - delta
  
count=0
zoom=1
begin = pygame.time.get_ticks();
while 1:
    begin_loop = pygame.time.get_ticks();
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE: sys.exit()
            if event.key == pygame.K_q: sys.exit()
            if event.key == pygame.K_b: 
                zoom = zoom * 1.1
            if event.key == pygame.K_n: 
                zoom = zoom / 1.1
            if event.key == pygame.K_f: 
                increase_speed(1)
            if event.key == pygame.K_s: 
                increase_speed(-1)
            if event.key == pygame.K_r: 
                anglespeed += 0.1
            if event.key == pygame.K_u: 
                anglespeed -= 0.1

    oldrect = blitrect
    # Do movements
#    ballcorner = ballcorner.move(speed)
    ballcenter = ballcenter.move(speed)
    angle += anglespeed
    rball = pygame.transform.scale(ball, (int(ball.get_width() * zoom), int(ball.get_height() * zoom)))
    rball2 = pygame.transform.rotate(rball, angle)
    rball2 = rball2.subsurface(rball.get_rect().move([(rball2.get_rect().width - rball.get_rect().width)/2, (rball2.get_rect().height - rball.get_rect().height)/2]))
#ballcorner = ballcenter.move([-rball.get_width() / 2, -rball.get_height() / 2])
    ballcorner = ballcenter.move([-rball2.get_width() / 2, -rball2.get_height() / 2])

    # Bounce
    if ballcorner.left < 0 or ballcorner.left > width - rball2.get_width():
        speed[0] = -speed[0]
    if ballcorner.top < 0 or ballcorner.top > height - rball2.get_height():
        speed[1] = -speed[1]

    # Draw
#    screen.fill(black, oldrect)
    screen.fill(black, oldrect)
    blitrect = screen.blit(rball2, ballcorner)
#    pygame.draw.circle(screen, (255, 0, 0), (ballcorner.left, ballcorner.top), 5)
#    pygame.draw.circle(screen, (0, 255, 0), (ballcorner.left + rball.get_width(), ballcorner.top + rball.get_height()), 5)
#    pygame.display.flip()
    pygame.display.update([oldrect, blitrect])
    count += 1

    while pygame.time.get_ticks() - begin_loop < 5:
        time.sleep(0.001)

    if pygame.time.get_ticks() - begin > 1000:
        print("%s FPS" % ((1000 * count) / (pygame.time.get_ticks() - begin)));
        begin = pygame.time.get_ticks()
        count = 0
