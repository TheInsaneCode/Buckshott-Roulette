import pygame
import sys
import random
import constants
from pygame.locals import *
from time import sleep

''' 
level:   1 
health:  4
rewards: 3
1shells: 3f 3b
2shelss: 3f 4b
3shelss: 3f 4b
'''
# 
pygame.init()
pygame.font.init()


BACKGROUND = (255, 255, 255)
FONT = lambda size, bold=False: pygame.font.SysFont('arial', size, bold)


fpsClock = pygame.time.Clock()

WINDOW = pygame.display.set_mode(
    (constants.screen['width'], constants.screen['height']))
pygame.display.set_caption(constants.screen['name'])


class Methods:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = constants.gui['size of box']
        self.height = constants.gui['size of box']
        self.padding = constants.gui['padding']
        self.items = {item: 0 for item in constants.gui['total items']}
        self.boxes = 4
        self.extra = 0
        self.end = False
        self.positions = []
        self.required = []

    def increment(self, name):
        self.items[name] += 1

    def decrement(self, name):
        if self.items[name] != 0:
            self.items[name] -= 1

    def plus(self, total_level_health):
        if self.boxes >= total_level_health:
            return
        elif self.boxes < total_level_health:
            self.boxes += 1

    def minus(self):
        self.boxes -= 1
        if self.boxes == 0:
            self.end = True

    def __add(self): ...


class ItemGroup(Methods):
    def __init__(self, coords, vertical, menu):
        super().__init__()
        self.x = coords[0]
        self.y = coords[1]
        self.veritcal = vertical
        self.menu = menu
        self.color1 = constants.gui['empty box']
        self.color2 = constants.gui['non empty box']
        if self.menu:
            del self.boxes, self.extra, self.end
        else:
            del self.items
            
    def vUse(self):
        # if not self.permission:
        #     return
        
        state = pygame.mouse.get_pressed()[0]
        x,y = pygame.mouse.get_pos()
        
        if x>(self.x+self.padding) and x<(self.x+self.width+self.padding):
            sleep(0.02)
            if (y>self.y) and (y<(self.required[2-1])):
                # print(y, self.y, self.required[2-1], 'health')
                if list(self.items.values())[0] != 0: 
                    if state:return 1
                    else: return ["Increase your health", "Bandage"]
            elif (y>self.required[2-1]) and (y<(self.required[3-1])):
                # print(y, self.required[2-1], self.required[3-1], 'glass')
                if list(self.items.values())[1] != 0: 
                    if state:return 2
                    else: return ["Shows the current shot", "Eye Glass"]
            elif (y>self.required[3-1]) and (y<(self.required[4-1])):
                # print(y, self.required[3-1], self.required[4-1], 'rpg')
                
                if list(self.items.values())[2] != 0: 
                    if state:return 3
                    else: return ["Double the damage", "Rpg"]
            elif (y>self.required[4-1]) and (y<(self.required[5-1])):
                # print(y, self.required[4-1], self.required[5-1], 'clock')
                if list(self.items.values())[3] != 0: 
                    if state:return 4
                    else: return ["Skip opponent's turn", "Clock"]
            elif (y>self.required[5-1]) and (y<(self.required[5-1]+self.height)):
                # print(y, self.required[5-1], self.required[5-1]+self.height, 'magnet')
                if list(self.items.values())[4] != 0: 
                    if state:return 5
                    else: return ["Relases current shot", "Magnet"]
        

            
        

    def addItem(self, name):
        self.items[name] += 1
        return self

    def rezie(self, percent):
        self.width = self.height = (self.width*percent)/100

    def badging(self, rect_values, index):
        (x, y) = rect_values
        image = pygame.image.load(
            constants.images[constants.gui['total items'][index]])
    #    image = pygame.transform.scale(image, (20, 20))

        (x, y) = (x+constants.gui['padding']*2, y)
        WINDOW.blit(
            image, (x+(constants.gui['padding']*2), y+(constants.gui['padding'])*3))
        font = FONT(10)
        text = font.render(
            str(self.items[list(self.items.keys())[index]]), True, (0, 0, 0))
        WINDOW.blit(text, (x, y))


    def __draw__(self):
        if self.veritcal:
            if self.menu:
                (x, y, w, h) = (self.x, self.y, self.width+(constants.gui['padding']*2), (self.height*len(
                    self.items))+(len(self.items)*constants.gui['padding'])+constants.gui['padding'])
                v = len(self.items)
            else:
                (x, y, w, h) = (self.x, self.y, self.width+(constants.gui['padding']*2), (self.height*self.boxes)+(
                    self.boxes*constants.gui['padding'])+constants.gui['padding'])
                v = self.boxes
            pygame.draw.rect(WINDOW, (0, 0, 0), (x, y, w, h))
            for i in range(v):
                Y = (y+constants.gui['padding']) + \
                    (i*self.height)+(constants.gui['padding']*i)
                color = self.color1
                if int(list(self.items.values())[i]) > 0:
                    color = self.color2
                pygame.draw.rect(
                    WINDOW, color, (x+constants.gui['padding'], Y, self.width, self.height))
                self.positions.append([x+constants.gui['padding'], Y])
                if len(self.required) <= 5:
                    self.required.append(Y)
                if self.menu:
                    self.badging((x, Y), i)
        else:
            if self.menu:
                (x, y, w, h) = (self.x, self.y, (self.width*len(self.items))+(len(self.items) *
                                                                              constants.gui['padding'])+constants.gui['padding'], self.height+(constants.gui['padding']*2),)
                v = len(self.items)
            else:
                (x, y, w, h) = (self.x, self.y, (self.width*self.boxes)+(self.boxes *
                                                                         constants.gui['padding'])+constants.gui['padding'], self.height+(constants.gui['padding']*2),)
                v = self.boxes
            pygame.draw.rect(WINDOW, (0, 0, 0), (x, y, w, h))
            for i in range(v):
                X = (x+constants.gui['padding']) + \
                    (i*self.width)+(constants.gui['padding']*i)
                # if self.items[i] > 0:
                #     color = self.color1
                # else:
                #     color = self.color2
                pygame.draw.rect(
                    WINDOW, constants.gui['non empty box'], (X, y+constants.gui['padding'], self.width, self.height))
                self.positions.append([X, y+constants.gui['padding']])
                if len(self.required) <= 5:
                    self.required.append(X)
                if self.menu:
                    self.badging((X, y), i)


    def manageInv(self):
        self.__draw__()
        return self.vUse()
        
        
        
class ButtonGroup:
    def __init__(self, orientation):
        self.orientation = orientation
        self.width = constants.gui['size of button']
        self.height = constants.gui['size of button']

    def newButton(self, name): ...
    def update(self, new_number): ...


class DisplayScreen:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.width = constants.screen['ds width']
        self.height = constants.screen['ds height']-281
        self.font = FONT(20)
        self.factor = 100
        self.you = constants.this_client
        self.opposite = constants.player2
        self.c1 = (0, 0, 0)
        self.c2 = (0, 0, 0)
        self.b1 = (200, 200, 150)
        self.b2 = (200, 200, 150)

    def choice(self):
      you = self.font.render(str(self.you), True, self.c1, self.b1)
      opp = self.font.render(str(self.opposite), True, self.c2, self.b2)
      reply = self.detectResponce((you, opp))
    #   pygame.draw.rect(WINDOW, (0, 0, 0), [self.x, self.y, self.width, self.height])
      if reply is None:
        WINDOW.blit(you, (self.x, self.y))
        WINDOW.blit(opp, (self.x+self.factor, self.y))
      else:
          return reply
      
    def detectResponce(self, text_obj):
        x, y = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]: 
            if x > self.x and x < self.x+text_obj[0].get_width() and y > self.y and y < self.y+self.height:
                self.c1 = (200, 200, 150)
                self.b1 = (0, 0, 0)
            else:
                self.c1 = (0, 0, 0)
                self.b1 = (200, 200, 150)
            if x > self.x+self.factor and x < self.x+text_obj[1].get_width()+self.factor and y > self.y and y < self.y+self.height:
                self.c2 = (200, 200, 150)
                self.b2 = (0, 0, 0)
            else:
                self.c2 = (0, 0, 0)
                self.b2 = (200, 200, 150)
            return
        if x > self.x and x < self.x+text_obj[0].get_width() and y > self.y and y < self.y+self.height:
            # print(self.x, self.width, self.x+text_obj[0].get_width())
            return self.you
        elif x > self.x+self.factor and x < self.x+text_obj[1].get_width()+self.factor and y > self.y and y < self.y+self.height:
            return self.opposite
        # return
        
    def show(self, text, size=20, bold=False):
        self.font = FONT(size, bold)
        text = self.font.render(text, True, (0, 0, 0))
        WINDOW.blit(text, (self.x, self.y))

    # def rewards(self, ):
      



class Animation:
   def __init__(self,coords:tuple, resize:int, *names):
      self.x = coords[0]
      self.y = coords[1]
      self.names = list(names)
      self.images = [pygame.image.load(image) for image in self.names]
      self.resize_factor = resize
      if self.resize_factor != 0:
         self.__resize__()         
   
   def __resize__(self):
      self.images = [pygame.transform.scale(image, (self.resize_factor, self.resize_factor)) for image in self.images]
      
      
   def default(self, index):
      WINDOW.blit(self.images[index], (self.x, self.y))
    #   WINDOW.blit(pygame.image.load("assets/images/chest1.png"), (0, 0))
    
   def subAnimation(self, indexes):
        self.sub_animation = []
        for index in range(indexes):
            self.sub_animation.append(self.images[index])
      


Y_center_group = lambda x: (constants.screen['height']//2)-(constants.gui['size of box']*x/2)
X_center_group = lambda x: (constants.screen['width']//2)-(constants.gui['size of box']*x/2)


X_center = lambda size: (constants.screen['width']//2)-(size.get_width()/2)
Y_center = lambda size: (constants.screen['height']//2)-(size.get_height()/2)

def play(obj, funcs, delay=0, special_indexes_delay=None, images_index=[]):
    for ind, sprite in enumerate(obj.images):
        if ind not in images_index and images_index != []:
            continue
        WINDOW.fill(BACKGROUND)
        WINDOW.blit(sprite, (obj.x, obj.y))
        if special_indexes_delay != None: 
            if ind in special_indexes_delay:
                sleep(delay)
        else:
           
            sleep(delay)
            ...
        for func in funcs:
            func()
        pygame.display.update()
        
        


# NOTE x or y is the number of bonus items in the game

if __name__ == '__main__':
    looping = True
    x = 0
    inv1 = ItemGroup((X_center_group(5), 100), False, True)
    screens = DisplayScreen((20, 350))
    chest_animation = Animation((0, 0), 100,*constants.sprites_chest.values())
    gun_animation = Animation((200, 200), 0, *constants.sprites_gun.values())
    index = 0
   
    while looping:
        WINDOW.fill(BACKGROUND)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        inv1.manageInv()
        _0 = screens.choice()
        if _0 is not None:
            print(_0)
        x+=1
        
        if x%100 == 0:
            # play(gun_animation, [inv1.manageInv], 0.1, [2,3])
         
            # index = -1
            ...
        else:
            gun_animation.default(index)
            
           
        #    print("else")
        fpsClock.tick(constants.screen['FPS'])
        pygame.display.update()