import pygame, sys, random
from assets import constants
from pygame.locals import *
pygame.init()



BACKGROUND = (255, 255, 255)

fpsClock = pygame.time.Clock()
 
WINDOW = pygame.display.set_mode((constants.screen['width'], constants.screen['height']))
pygame.display.set_caption(constants.screen['name'])
 


def main():
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()


    WINDOW.fill(BACKGROUND)
    pygame.display.update()
    fpsClock.tick(constants.screen['FPS'])
 
y = random.sample([x for x in range(10)], 10)
y.sort()
print(y)

looping = True
while looping :
    main()
    exit()