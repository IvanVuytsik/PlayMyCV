import pyautogui
import pygame
import self as self


# def start_wealth():
#     global start_wealth
#     start_wealth = 150
# start_wealth()

start_wealth = 150

def wealth():
    global wealth
    wealth = 0
    wealth += start_wealth
wealth()

# start_wealth = 150
# wealth = 0
# wealth += start_wealth





#unlocked_quests = []
quest_new_beginnings = 'unlocked'
quest_dire_wolves = 'invisible'
quest_highwaymen = 'invisible'
quest_dragonhunt = 'invisible'
quest_finale = 'invisible'

# unlocked_quests.append(quest_new_beginnings)
# unlocked_quests.append(quest_dire_wolves)



def fullscreen():
    global fullscreen
    fullscreen = False
fullscreen()


def mouse_map_align ():
    pyautogui.moveTo(750, 400)





class Button():
    def __init__(self, surface, x, y, image, size_x, size_y, price, available, description):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface
        self.price = price
        self.available = available
        self.description = description

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        return action


class ToggleButton():
    def __init__(self, surface, x, y, image, size_x, size_y, price, available, description):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.toggled = False
        self.surface = surface
        self.price = price
        self.available = True
        self.description = description

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.toggled == False:
                if self.rect.collidepoint(event.pos):
                    self.toggled = True
                    #print('Open')
            elif event.button == 1 and self.toggled == True:
                if self.rect.collidepoint(event.pos):
                    self.toggled = False
                    #print('Close')

