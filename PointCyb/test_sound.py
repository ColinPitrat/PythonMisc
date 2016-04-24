#!/usr/bin/python2
import pygame, time

pygame.init()
#pygame.mixer.init()
print("Mixer settings", pygame.mixer.get_init())
print("Mixer channels", pygame.mixer.get_num_channels())

pygame.mixer.music.load('ressources/Demo.mp3')
pygame.mixer.music.set_volume(1.0)
print("Play")

pygame.mixer.music.play(1, 0)
while pygame.mixer.music.get_busy():
    print("Playing", pygame.mixer.music.get_pos())
    time.sleep(1)

pygame.mixer.music.stop()
print("Stoping music")

#pygame.mixer.quit()
pygame.quit()
print("Done")
