import random
from time import sleep
import constants
import GUI
from ui import play
import pygame

pygame.mixer.init()
# music1 = pygame.mixer.S("assets/sounds/firing.mp3")
# music1.play()


def playEffect(sound):
    sound = pygame.mixer.Sound(sound)
    # pygame.mixer_music.set_volume(100)
    pygame.mixer.Sound.play(sound)
    return sound


funcs = [GUI.inv1.manageInv, GUI.inv2.manageInv,
         GUI.health1.manageInv, GUI.health2.manageInv]


screens = [pygame.transform.scale(pygame.image.load(image), (400, 400)) for image in [
    'assets/images/crackedglass2.png', 'assets/images/crackedglass1.png']]


def displayBrokenScreen():
    GUI.WINDOW.blit(screens[0], (0, 0))


def displayBlood():
    GUI.WINDOW.blit(pygame.transform.scale(pygame.image.load(
        'assets/images/blood.png'), (400, 300)), (0, 0))


def distribute_items(player, count):
    items = []
    for x in range(count):
        items.extend(random.sample(constants.gui['total items'], 1))
    for item in items:
        player.items[item] += 1
    return items


class Player:
    def __init__(self, name, inv, health):
        self.name = name
        self.items = inv.items
        self.health = health
        self.inuse = []


player1 = Player(constants.this_client, GUI.inv1, GUI.health1)
player2 = Player(constants.player2, GUI.inv2, GUI.health2)
shells = [True, True, True, False, False, False, False, False]
# shells = [False for x in range(17)]
fired_count = 0
random.shuffle(shells)


game_state = {
    'd_count': 3,
    'health_total': 4,
    'turn': 2,
    'ended': False,
    'lost': False,
    'level': 1,
    'dead': False
}


if __name__ == '__main__':
    counter =  0
    counter2 =  0
    counter3 =  0
    counter4 =  0
    timer = 30
    
    effect = []
    choice = None
    played = False
    allowed = False
    fired = False
    
    _3clicked = False
    _4clicked = False

    while GUI.looping:
        # GUI.tooltip.show("Fr", 15)
        if counter2 > 0:
            counter2 -= 1
            GUI.WINDOW.fill((200, 200, 150))
            displayBrokenScreen()
            pygame.display.update()
            continue
        if counter4 > 0:
            counter4 -= 1
            try:
                GUI.info.show(
                    str("Bullet found" if shells[0] else "Not found"), 15)
            except:
                GUI.info.show(str("Out of shots"))
        if game_state['level'] == 3:
            GUI.WINDOW.fill((200, 200, 150))
            GUI.Levelinfo.show('Game Finished', 25)
            pygame.display.update()
            sleep(5)
            exit()
        if GUI.health1.boxes == 0 or GUI.health2.boxes == 0 and not dead:
            counter = 30
            dead = True

        if counter > 0:
            # GUI.WINDOW.fill((200, 200, 150))
            counter -= 1
            displayBlood()
            # pygame.display.update()
            # WINDOW.fill()

            if counter == 27:
                playEffect('assets/sounds/blood.mp3')
        if counter == 1:
            game_state['lost'] = True
        elif len(shells) == 0:
            game_state['ended'] = True
        if game_state['lost']:
            # do something
            del player1, GUI.inv1, GUI.inv2, GUI.health1, GUI.health2, player2
            GUI.looping = False
            exit()

        if game_state['ended']:
            screens.pop(0)
            # counter = 0
            game_state['level'] += 1
            game_state['d_count'] = 5
            game_state['health_total'] = 8
            played = False
            allowed = False
            fired = False
            game_state['turn'] = 2
            choice = None
            game_state['timer'] = 30
            effect = []
            game_state['ended'] = False
            GUI.played = False
            GUI.index = 0
            shells = [True, True, True, False, False, False,
                      False, False, False, False, True, True]
            random.shuffle(shells)
            random.shuffle(shells)
            random.shuffle(shells)
            random.shuffle(shells)
            for x in range(4):
                GUI.health1.plus(game_state['health_total'])
                GUI.health2.plus(game_state['health_total'])

        GUI.main()
        GUI.WINDOW.fill((200, 200, 150))
        for func in funcs:
            if not game_state['dead']:
                func()
        GUI.EmptyShots.show("Empty shots: "+str(shells.count(False)), 15)
        GUI.Playerinfo.show("Player: " + player1.name, 15)
        GUI.FilledShots.show("Filled shots:   "+str(shells.count(True)), 15)
        GUI.Levelinfo.show("level: "+str(game_state['level']), 15)
        if type(text := GUI.inv1.manageInv()) is list:
            GUI.Header.show(text[1], 15, True)
            GUI.tooltip.show(text[0], 15)
        if pygame.mouse.get_pressed()[0]:
            Effect = GUI.inv1.manageInv()
            if Effect is not None:
                effect.append(Effect)
                print("effect used: ", effect[0])
        for func in funcs:
            func()
        if 1 in effect:
            GUI.health1.plus(game_state['health_total'])
            GUI.inv1.decrement('sunnyplast')
            effect.remove(1)
            sleep(0.02)
        if 2 in effect:
            GUI.inv1.decrement('magnifying_glass')
            effect.remove(2)
            sleep(0.02)
            counter4 = 20
        # print(counter4, counter4>0)
        if 5 in effect:
            print(shells[0])
            GUI.inv1.decrement('magnet')
            effect.remove(5)
            del shells[0]
        if 3 in effect:
            if not _3clicked:
                sleep(0.02)
                GUI.inv1.decrement('rpg')
                _3clicked = True
        if 4 in effect:
            if not _4clicked:
                sleep(0.02)
                GUI.inv1.decrement('clock')
                _4clicked = True
        
        if not played or timer > 0:
            GUI.played = GUI.chest_opening(GUI.chest, funcs, GUI.index)
        elif not fired and not allowed:
            # print(choice)
            if choice is None:
                choice = GUI.choice_screen.choice()
                GUI.gun.default(0)
                continue
            else:
                if len(shells) > 0:
                    GUI.fired = GUI.fire(GUI.gun, funcs, True, shells[0])

                else:
                    GUI.fired = GUI.fire(GUI.gun, funcs, False, False)

            if GUI.fired:

            
                if shells[0]:
                    if 4 in effect:
                        _4clicked = False
                        effect.remove(4)
                    else:
                        game_state['turn'] = 1
                    # counter3 = 0
                    if choice == constants.this_client:
                        player1.health.minus()
                        displayBrokenScreen()
                        counter2 = 20
                    elif choice == constants.player2:
                        player2.health.minus()
                    playEffect('assets/sounds/firing.mp3')

                    if 3 in effect:
                        _3clicked = False
                        if choice == constants.this_client:
                            player1.health.minus()
                            playEffect('assets/sounds/firing.mp3')
                        elif choice == constants.player2:
                            player2.health.minus()
                        effect.remove(3)
                else:
                    game_state['turn'] = 1
                    if 3 in effect:
                        _3clicked = False
                        effect.remove(3)
                    if choice == constants.this_client and counter3 == 0:
                        # if 4 not in effect:
                        game_state['turn'] = 2
                        counter3 += 1
                        # print("IM here")
                    elif counter3 == 1:
                        if 4 in effect: 
                            _4clicked = False
                            effect.remove(4)
                            game_state['turn'] = 2
                        else:
                            game_state['turn'] = 1
                            counter3 += 1
                            
                        # counter3 += 1
                    if counter3 > 1:
                        counter3 = 0
                        
                    if 4 in effect:
                        _4clicked = False
                        effect.remove(4)
                        game_state['turn'] = 2
                    else:
                        if counter3 != 1:
                            game_state['turn'] = 1
                        
                        

                    playEffect('assets/sounds/missed.mp3')
                print('I fired and bullets remaning', len(shells)) if shells[0] else print("I fired and missed and bullet remaining", len(shells))
            
                del shells[0]
                choice = None

        if GUI.played:
            GUI.index = -1
            GUI.played = None
            played = True
            allowed = True
            distribute_items(player1, game_state['d_count'])
            # distribute_items(player2, game_state['d_count'])
            # GUI.inv1.addItem('clock').addItem('clock').addItem('clock')
            playEffect("assets\sounds\chest.mp3")
        if allowed and timer != 0:
            timer -= 1
        if timer == 0:
            allowed = False
            timer = 0

        if not (game_state['turn']==2) and len(shells) > 0:
            print('computer fired and bullets remaning', len(shells)) if shells[0] else print("Computer fired and missed and bullet remaining", len(shells))
            game_state['turn'] = 2
            if shells[0]:
                player1.health.minus()
                counter2 = 120
                playEffect('assets/sounds/glass.mp3')
            del shells[0]
        sleep(0.01)
    else:
        exit("Hi")
