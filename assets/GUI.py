import pygame, sys, random
import constants
import ui
from pygame.locals import *
pygame.init()



BACKGROUND = (200, 200, 150)
fpsClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((constants.screen['width'], constants.screen['height']))
pygame.display.set_caption(constants.screen['name'])
 

"""CUSTOM FUNCTION"""

    

def chest_opening(obj, funcs, index, delay=0, special_indexes_delay=None):
    if pygame.mouse.get_pressed()[0] and index != -1:
        ui.play(obj, funcs, delay, special_indexes_delay)
        return True
    obj.default(index)
    
def fire(obj, funcs, turn, bullet, coords=(10, 10+constants.gui['size of box'])):
  x,y = pygame.mouse.get_pos()
  
  if pygame.mouse.get_pressed()[0] and turn and bullet and x>coords[1]:
    ui.play(obj, funcs, 0.1, (1,2))
    return True
  if not bullet and turn and pygame.mouse.get_pressed()[0] and x>coords[1]:
    ui.play(obj, funcs, images_index=[0, 3, 4])
    return True
    
  obj.default(0)
    

"""---------------"""

def main():
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()


    fpsClock.tick(constants.screen['FPS'])
    pygame.display.update()
 

FilledShots = ui.DisplayScreen((290, 10))
EmptyShots = ui.DisplayScreen((290, 30))
Playerinfo = ui.DisplayScreen((10, 10))
Levelinfo = ui.DisplayScreen((10, 30))
Header = ui.DisplayScreen((230, 330))
tooltip = ui.DisplayScreen((230, 350))
info = ui.DisplayScreen((160, 70))



looping = True
X1, Y = 10, ui.Y_center_group(5)
X2 = constants.screen['width']-constants.gui['size of box']-(constants.gui['padding']*2)-X1
inv1 = ui.ItemGroup((X1, Y), True, True)
inv2 = ui.ItemGroup((X2, ui.Y_center_group(5)), True, True)

Y1 = 320
health1 = ui.ItemGroup((X1, Y1), False, False)
health2 = ui.ItemGroup((X1, Y1+30), False, False)
health1.rezie(50)
health2.rezie(50)

gun = ui.Animation((190, 190), 0, *constants.sprites_gun.values())
chest = ui.Animation((130, 170), 150, *constants.sprites_chest.values())
played = None
fired = False
index = 0
# inv1.manageInv()

choice_screen = ui.DisplayScreen((120, 100))
choice = None

if __name__ == '__main__':
  while looping :
      main()
      WINDOW.fill(BACKGROUND) 
      if choice is None:
        choice = choice_screen.choice()
        print(choice)
        
        
      EmptyShots.show("Empty shots: 3", 15)
      FilledShots.show("Filled shots:   4", 15)
      inv1.manageInv()
      inv2.manageInv()
      health1.manageInv()
      health2.manageInv()
        
      # if pygame.mouse.get_pressed()[0]:
      #    ui.play(chest, [inv1.manageInv,
      # inv2.manageInv,
      # health1.manageInv,
      # health2.manageInv])
      #    index = -1
      # else:
      #   chest.default(index)
      played = chest_opening(chest, [inv1.manageInv,inv2.manageInv, health1.manageInv, health2.manageInv], index)
      if played:
        index = -1