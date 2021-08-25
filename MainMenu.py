import inspect
import pyautogui
from button import *
import pygame,sys,random
from pygame.locals import *
import pygame as py
vec = pygame.math.Vector2
from abc import ABC, abstractmethod
import threading
import os
from tkinter import *
from pygame.locals import *
import numpy as np
import button
import time
import linecache


mainClock = pygame.time.Clock()

pygame.init()
pygame.mixer.set_num_channels(32)
pygame.mixer.pre_init(44100,-16,2,512)

pygame.display.set_caption("Yvan's Lot") #screen window name
WINDOW_SIZE = (1280,720)
screen = pygame.display.set_mode((1280,720),0,32)
monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

bg_main_menu = pygame.image.load("MainMenuRes/MainMenu.png").convert_alpha()
bg_main_menu = pygame.transform.scale(bg_main_menu, (int(WINDOW_SIZE[0]),(int(WINDOW_SIZE[1]))))

bg_char_sheet = pygame.image.load("MainMenuRes/charsheet.png").convert_alpha()
bg_char_sheet = pygame.transform.scale(bg_char_sheet, (int(WINDOW_SIZE[0]*1.00),(int(WINDOW_SIZE[1]*1))))

normal_icon = pygame.image.load("WorldMap/cursor_final.png").convert_alpha()
normal_icon = pygame.transform.scale(normal_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.06))))

dice_icon = pygame.image.load("MainMenuRes/dice.png").convert_alpha()
dice_icon = pygame.transform.scale(dice_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.06))))

plus_icon = pygame.image.load("MainMenuRes/plus.png").convert_alpha()
plus_icon = pygame.transform.scale(plus_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.06))))

minus_icon = pygame.image.load("MainMenuRes/minus.png").convert_alpha()
minus_icon = pygame.transform.scale(minus_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.06))))

plus_green_icon = pygame.image.load("MainMenuRes/plus_green.png").convert_alpha()
plus_green_icon = pygame.transform.scale(plus_green_icon, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.03))))

bg_infosheet = pygame.image.load("MainMenuRes/scroll.png").convert_alpha()
bg_infosheet = pygame.transform.scale(bg_infosheet, (int(WINDOW_SIZE[0]*0.6),(int(WINDOW_SIZE[1]*0.6))))

#display = pygame.Surface((800,600))
#mouse_position = pygame.mouse.get_pos()
select_sound = pygame.mixer.Sound('MainMenuRes/selection.wav')
scroll_sound = pygame.mixer.Sound('WorldMap/scroll_sound.wav')


def play_music(type):
    global play_music
    if type == 'Adventure':
        pygame.mixer.music.load('sounds/forest.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
    elif type == 'Battle':
        pygame.mixer.music.load('BattleScreen/battlemusic.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
    elif type == 'Battle1':
        pygame.mixer.music.load('BattleScreen/battlemusic1.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    elif type == 'Map':
        pygame.mixer.music.load('WorldMap/WorldMapOst.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.02)
    elif type == 'MainTheme':
        pygame.mixer.music.load('MainTheme.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    elif type == 'Outro':
        pygame.mixer.music.load('OutroSong.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
    elif type == 'BattleVictory':
        pygame.mixer.music.load('BattleScreen/items/victory.mp3')
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.1)
    elif type == 'BattleDefeat':
        pygame.mixer.music.load('BattleScreen/items/defeat.mp3')
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_volume(0.1)
    else:
        pygame.mixer.music.fadeout(2500)


if __name__=='__main__':
    play_music('MainTheme')
    font = pygame.font.SysFont('Times New Roman', 18)
    fontMenu = pygame.font.Font('WorldMap/ESKARGOT.ttf', 26)
    fontDescription= pygame.font.SysFont('Times New Roman', 22)
    fontMenuLarge = pygame.font.Font('WorldMap/ESKARGOT.ttf', 48)
        #pygame.font.Font('WorldMap/ESKARGOT.ttf', 20)
    player_rect = pygame.Rect((screen.get_width()/2), (screen.get_height()/2), 50, 50)


def draw_bg_main_menu ():
    screen.blit(bg_main_menu,(0,0))

def draw_bg_char_sheet ():
    screen.blit(bg_char_sheet,(0,0))

def draw_infosheet (screen,xcor,ycor):
    screen.blit(bg_infosheet,(xcor,ycor))

def draw_text (text, font, color, surface, x,y):
    textobj = font.render(text, 1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit (textobj, textrect)

def draw_tips(tips, xcor,ycor):
    tips_list = []
    line_spacing_count = 0
    for line in tips.split('\n'):
        tips = fontDescription.render(line,True,'#2c2d47')
        tips_list.append(tips)
        line_spacing_count += 25
        screen.blit(tips,(xcor, ycor + (line_spacing_count*1)))

tips_path = open('MainMenuRes/Tips.txt','r')
tips_path_lore = tips_path.read()
tips_path.close()

def mouse_map_position_align(x,y):
    pyautogui.moveTo(x,y)




menuClick = False

def main_menu():
    global menuClick
    clicked = False

    mouse_position = pygame.mouse.get_pos()
    main_menu_running = True
    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    screen = pygame.display.set_mode((1280,720),0,32)

    fullscreen = button.fullscreen
    #     not bool(linecache.getline('resolution.txt',1))
    # with open('resolution.txt', 'w') as file:
    #     file.write(str(fullscreen))

    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

    button_2 = pygame.Rect(520,220,200,50)
    button_1 = pygame.Rect(520,320,200,50)
        #ToggleButton (screen,520,320, bg_infosheet, 200,50, 0, True, "Tips" )
    button_3 = pygame.Rect(520,420,200,50)

    while main_menu_running:
        screen.fill((0,0,0))
        draw_bg_main_menu()
        draw_text('Yvan\'s Lot: An Epic Hiring Adventure ', fontMenu, (255,225,100),screen, 20,20)

        mx,my = pygame.mouse.get_pos()



        if button_2.collidepoint((mx,my)):
            if menuClick:
               pygame.mixer.Sound(select_sound).play()
               stats()
        if button_3.collidepoint((mx,my)): #quit button
            if menuClick:
                pygame.mixer.Sound(select_sound).play()
                main_menu_running = False

        # pygame.draw.rect(screen, (255,0,0), button_1)
        # pygame.draw.rect(screen, (0,255,0), button_2)
        # pygame.draw.rect(screen, (0,0,255), button_3)

        if button_1.collidepoint(mouse_position):
            draw_text('Tips', fontMenu, (255,255,150),screen, 590,320)
        else:
            draw_text('Tips', fontMenu, (255,225,100),screen, 590,320)

        if button_2.collidepoint(mouse_position):
            draw_text('Character Sheet', fontMenu, (255,255,150),screen, 530,220)
        else:
            draw_text('Character Sheet', fontMenu, (255,225,100),screen, 530,220)

        if button_3.collidepoint(mouse_position):
            draw_text('Quit', fontMenu, (255,255,150),screen, 600,420)
        else:
            draw_text('Quit', fontMenu, (255,225,100),screen, 600,420)


            if button_1.collidepoint((mx,my)) and clicked:
                draw_infosheet(screen,button_1.x-260,button_1.y-200)
                draw_tips(tips_path_lore, button_1.x-210,button_1.y-180)
                if menuClick:
                    pygame.mixer.Sound(scroll_sound).play()
            elif not button_1.collidepoint((mx,my)):
                clicked = False


        menuClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_o:
                    button.fullscreen = not button.fullscreen
                    fullscreen = button.fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

            if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        menuClick = True

                    if event.button == 1 and clicked == False:
                        clicked = True
                    elif event.button == 1 and clicked == True:
                        clicked = False


        screen.blit(normal_icon, player_rect)
        pygame.mouse.set_visible(False)
        mouse_position = pygame.mouse.get_pos()
        player_rect.x, player_rect.y = mouse_position


        pygame.display.update()
        mainClock.tick(60)






















































def stats():
    stats_running = True
    menuClick = False
    clicked = False
    roll_dice = False
    mouse_position = pygame.mouse.get_pos()
    mx,my = pygame.mouse.get_pos()
    stat_distributable = 9
    #screen = pygame.display.set_mode((1280,720),0,32)
    screen = pygame.display.set_mode((1280,720),0,32)
    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    fullscreen = button.fullscreen
        #not bool(linecache.getline('resolution.txt',1))

    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

    randomlist = []
    for i in range(0,9):
        n = random.randint(7,10)
        randomlist.append(n)

    def stats_draw_text (number, font, color, surface, x,y):
        textobj = font.render(number, 1,color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit (textobj, textrect)

#----------------------------RollButton--------------------------------
    roll_button = button.Button(screen, 140, 600, dice_icon, 40,40,0, True,'Roll Dice')
#----------------------------FreeStatsSButton--------------------------------
    bonus_hp = 0
    bonus_arm = 0
    bonus_def = 0
    bonus_atk = 0

    hp_plus_button = button.Button(screen, 350, 550, plus_icon, 20,20,0, True,'Increase')
    hp_minus_button = button.Button(screen, 350, 570, minus_icon, 20,20,0, True,'Decrease')

    armor_plus_button = button.Button(screen, 520, 550, plus_icon, 20,20,0, True,'Increase')
    armor_minus_button = button.Button(screen, 520, 570, minus_icon, 20,20,0, True,'Decrease')

    def_plus_button = button.Button(screen, 920, 550, plus_icon, 20,20,0, True,'Increase')
    def_minus_button = button.Button(screen, 920, 570, minus_icon, 20,20,0, True,'Decrease')

    atk_plus_button = button.Button(screen, 1095, 550, plus_icon, 20,20,0, True,'Increase')
    atk_minus_button = button.Button(screen, 1095, 570, minus_icon, 20,20,0, True,'Decrease')

#----------------------------------------------------------------------
    while stats_running:
        screen.fill((0,0,0))
        draw_bg_char_sheet()
        #draw_text('ESC to return', fontMenu, (0,225,0),screen, 10,0)  #Yvan\'s
        #draw_text('SPACE to continue', fontMenu, (0,225,0),screen, 1060,0)  #Yvan\'s

#-----------------------------SkillTreeButtons+Text-------------------------------
        button_skill_0 = pygame.Rect(310,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_0)
        if button_skill_0.collidepoint(mouse_position):
            stats_draw_text('Native Russian speaker. You were born and raised in Russia.Your knowledge of language and traditions help '
                      ,fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('you to communicate with 260 million people. Blessed with resilience, you gain 40 extra Health Points.'
                      ,fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_1 = pygame.Rect(390,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_1)
        if button_skill_1.collidepoint(mouse_position):
            stats_draw_text('Krass! You have learned some German and became a proud owner of a C1 certificate. With this trait, your',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('starting gold is increased by 100 pieces and you are always accompanied by two landsknechts in your quest.'
                      ,fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_2 = pygame.Rect(470,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_2)
        if button_skill_2.collidepoint(mouse_position):
            stats_draw_text('C2 English speaker. You use it every day, everywhere, and for everything. Your starting gold is increased by'
                      ,fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('100 pieces, and two merry men always watch your back.'
                      ,fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_3 = pygame.Rect(552,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_3)
        if button_skill_3.collidepoint(mouse_position):
            stats_draw_text('You have picked up some French during your travels. Although A2 leaves a lot to be desired, somehow you '
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('managed to convince an unemployed chevalier to join your quest. There are many like him these days.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_4 = pygame.Rect(632,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_4)
        if button_skill_4.collidepoint(mouse_position):
            stats_draw_text('You graduated with a law degree from the Russian State University of Justice. Your Defence and Attack '
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('are increased by 20. Five years of experience added 20 Armor Points to that.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_5 = pygame.Rect(712,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_5)
        if button_skill_5.collidepoint(mouse_position):
            stats_draw_text('You graduated with a LL.M degree from the University of Vienna, thus further improving your Defence '
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('and Attack by 10. Working internationally provided another 20 Armor Points.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_6 = pygame.Rect(795,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_6)
        if button_skill_6.collidepoint(mouse_position):
            stats_draw_text('Python programmer. You have learned Python, SQL, Django, Flask, React, Pandas and some JavaScript. '
            ,fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('You can knock on many doors now as your Attack is increased by 10. Not too shabby for a lawyer.'
            ,fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_7 = pygame.Rect(875,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_7)
        if button_skill_7.collidepoint(mouse_position):
            stats_draw_text('Healthy habits. Smoking, alcohol, drugs and fast food were never your life choices. You gain 20 extra'
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('Health Points, but unable to use any concoctions in battle.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_8 = pygame.Rect(960,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_8)
        if button_skill_8.collidepoint(mouse_position):
            stats_draw_text('Dog person. You have a loyal companion in your quest providing you with extra 10 Defence. Things are'
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('somehow better this way, even though your starting gold is decreased by 50 pieces.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_9 = pygame.Rect(1042,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_9)
        if button_skill_9.collidepoint(mouse_position):
            stats_draw_text('Team spirit. You understand that things get done faster when tackeld by more people than yourself. '
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('Your party members gain 5 Attack and 5 Defence with you around.'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
        button_skill_10 = pygame.Rect(1125,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_10)
        if button_skill_10.collidepoint(mouse_position):
            stats_draw_text('Good eater. You eat well. Maybe a bit too well. Your Health Points are increased by 20.'
                      , fontDescription, '#2c2d47',screen, 300,650)
#--------------------------------------------------------------------------------
        button_skill_11 = pygame.Rect(1202,585,50,50)
        #pygame.draw.rect(screen, (255,0,0), button_skill_11)
        if button_skill_11.collidepoint(mouse_position):
            stats_draw_text('International. You haven\'t seen the half of the world yet, but you did your small part. Different cultures '
                      , fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('and countries fascinate you. You enjoy a diverse company and gain extra 10 Armor and Health Points'
                      , fontDescription, '#2c2d47',screen, 300,675)
#--------------------------------------------------------------------------------
#-----------------------------StatButtons+Text-------------------------------
        # button_stat_0 = pygame.Rect(50,375,70,5)
        # pygame.draw.rect(screen, (255,0,0), button_stat_0)
        # if button_stat_0.collidepoint(mouse_position):
        #     draw_text('Reliability', fontDescription, '#2c2d47',screen, 300,650)#
#----------------------------RollDiceButton---------------------------
        if roll_button.draw():
            roll_dice = True
            randomlist = []
            for i in range(0,9):
                n = random.randint(7,10)
                randomlist.append(n)

        if roll_button.rect.collidepoint(mouse_position):
            stats_draw_text(f'{roll_button.description}', fontMenu, (0,225,0),screen, roll_button.rect.x+50,roll_button.rect.y)
#----------------------------Stats-------------------------------------
        stat1 = str(randomlist[0])
        stat2 = str(randomlist[1])
        stat3 = str(randomlist[2])
        stat4 = str(randomlist[3])
        stat5 = str(randomlist[4])
        stat6 = str(randomlist[5])
        stat7 = str(randomlist[6])
        stat8 = str(randomlist[7])
        stat9 = str(randomlist[8])

        stat_spacing = 0
        stat_list = []
        for i in randomlist:
            stat = fontMenu.render(str(i), True, '#2c2d47')
            stat_list.append(stat)
            stat_spacing += 26
            screen.blit(stat,(218,332 + (stat_spacing*1)))

#-----------------------------------ExpPoints---------------------------------------
        stats_draw_text(str(stat_distributable), fontMenuLarge, '#2c2d47',screen, 745,270)

        exp_points = pygame.Rect(745,270,50,50)
        #pygame.draw.rect(screen, (255,0,0), exp_points)
        if exp_points.collidepoint(mouse_position):
            stats_draw_text('Your hard earned Experience Points',
                      fontDescription, '#2c2d47',screen, 300,650)

#------------------------------------JobDescription--------------------------------
        job_0 = pygame.Rect(380,80,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_0)
        if job_0.collidepoint(mouse_position):
            stats_draw_text('You consult a fashion and IT start-up regarding matters of personal data protection (GDPR/CCPA/COPPA);',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('international corporate and contracts law; compliance with Google Play, AppStore and AppGallery.',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('You negotiate deals with clients and partners, and contribute to competition analytics.',
                      fontDescription, '#2c2d47',screen, 300,694)
#------------------------------------JobDescription--------------------------------
        job_1 = pygame.Rect(320,230,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_1)
        if job_1.collidepoint(mouse_position):
            stats_draw_text('A project in cooperation with European KIC.',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('You fundraised and organized a local competition for Russian start-ups with clean tech ideas.',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('Two Russian teams were selected, trained and sent to the grand finals in the Netherlands in 2019.',
                      fontDescription, '#2c2d47',screen, 300,694)
#------------------------------------JobDescription--------------------------------
        job_2 = pygame.Rect(320,390,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_2)
        if job_2.collidepoint(mouse_position):
            stats_draw_text('Employed as a solo corporate lawyer to support a Russian branch of an international engineering company.',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('Main activities included: corporate, labor, contracts, construction law and logistics (INCOTERMS).',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('Your working languages were Russian, English and German.',
                      fontDescription, '#2c2d47',screen, 300,694)
#------------------------------------JobDescription--------------------------------
        job_3 = pygame.Rect(900,90,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_3)
        if job_3.collidepoint(mouse_position):
            stats_draw_text('You worked as a consultant and business intelligence analyst at a US-based company. ',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('Key responsibilities included: preparation of tender project proposals, draft of reports and research papers',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('on the topic of innovation commercialization and economic development.',
                      fontDescription, '#2c2d47',screen, 300,694)
#------------------------------------JobDescription--------------------------------
        job_4 = pygame.Rect(920,270,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_4)
        if job_4.collidepoint(mouse_position):
            stats_draw_text('Working as an international business specialist at a Russian aerospace company, you provided:',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('translation and interpretation services; hosting of international delegations; managing and drafting of',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('analytical reports, R&D and supply contracts.',
                      fontDescription, '#2c2d47',screen, 300,694)
#------------------------------------JobDescription--------------------------------
        job_5 = pygame.Rect(920,420,250,100)
        #pygame.draw.rect(screen, (255,0,0), job_5)
        if job_5.collidepoint(mouse_position):
            stats_draw_text('You worked at the United Nations (UNECE in Switzerland and ICTY in the Netherlands) providing:',
                      fontDescription, '#2c2d47',screen, 300,650)
            stats_draw_text('translation and interpretation; event management; reserch of housing, land management, and PPPs; support',
                      fontDescription, '#2c2d47',screen, 300,672)
            stats_draw_text('of conferences with high level attendees; and assistance on a case-law involving crimes against humanity.',
                      fontDescription, '#2c2d47',screen, 300,694)


#---------------adventureSubDef----------------------------
        button_adventure = pygame.Rect(1070,10,200,50)
        if button_adventure.collidepoint((mouse_position)) and stat_distributable == 0:
            if menuClick:
                pygame.mixer.Sound(select_sound).play()
                global_map()
        if button_adventure.collidepoint(mouse_position):
            stats_draw_text('Begin Adventure', fontMenu, (0,255,0),screen, 1070,0)
        else:
            stats_draw_text('Begin Adventure', fontMenu, (0,225,0),screen, 1070,0)

        if  stat_distributable >0:
            stats_draw_text('Distribute your points!', fontMenu, (0,225,0),screen, 1000,40)


#---------------adventureSubDef-------------------------------------------
#---------------backToMainMenu--------------------------------------------
        button_back_to_main_menu = pygame.Rect(10,10,200,50)
        if button_back_to_main_menu.collidepoint((mouse_position)):
            if menuClick:
                pygame.mixer.Sound(select_sound).play()
                stats_running = False
        if button_back_to_main_menu.collidepoint(mouse_position):
            stats_draw_text('Back to Menu', fontMenu, (0,255,0),screen, 10,0)
        else:
            stats_draw_text('Back to Menu', fontMenu, (0,225,0),screen, 10,0)
#-------------------------------------------------------------------------
        button_reccruitt = pygame.Rect(45,340,200,20)
        #pygame.draw.rect(screen, (255,0,0), button_reccruitt)
        if button_reccruitt.collidepoint(mouse_position):
            stats_draw_text('A unique system that makes every character really special and still keeps things below 18!', fontDescription, '#2c2d47',screen, 300,650)


        #-------------------------HP/ARM/ATK/DEF----------------------------------
        button_ivan_hp = pygame.Rect(375,550,35,35)
        #pygame.draw.rect(screen, (255,0,0), button_ivan_hp)
        if button_ivan_hp.collidepoint(mouse_position):
            stats_draw_text('Health Points', fontDescription, '#2c2d47',screen, 300,650)
        ivan_hp =  int(60 + bonus_hp + randomlist [0]*2 + randomlist [5]*2 + randomlist [7]*2)
        stats_draw_text(f'{ivan_hp}', fontMenu, (255,255,150),screen, 420,550)

        button_ivan_armor = pygame.Rect(545,555,35,35)
        #pygame.draw.rect(screen, (255,0,0), button_ivan_armor)
        if button_ivan_armor.collidepoint(mouse_position):
            stats_draw_text('Armor Points', fontDescription, '#2c2d47',screen, 300,650)
        ivan_armor = int(50 + bonus_arm + randomlist [4]*2 + randomlist [8]*2 + randomlist [7]+(randomlist [1]+randomlist [3])/2)
        stats_draw_text(f'{ivan_armor}', fontMenu, (255,255,150),screen, 590,550)

        button_ivan_defence = pygame.Rect(945,555,35,35)
        #pygame.draw.rect(screen, (255,0,0), button_ivan_defence)
        if button_ivan_defence.collidepoint(mouse_position):
            stats_draw_text('Defence. Determines efficiency of your armor.', fontDescription, '#2c2d47',screen, 300,650)
        ivan_defence = int(20 + bonus_def + (randomlist [4] + randomlist [8])/2 + randomlist [3]+(randomlist [1]+randomlist [7]/2)+(randomlist [5]+randomlist [6]/2))
        stats_draw_text(f'{ivan_defence}', fontMenu, (255,255,150),screen, 990,550)

        button_ivan_attack = pygame.Rect(1120,555,35,35)
        #pygame.draw.rect(screen, (255,0,0), button_ivan_attack)
        if button_ivan_attack.collidepoint(mouse_position):
            stats_draw_text('Attack Power', fontDescription, '#2c2d47',screen, 300,650)
        ivan_attack = int(20 + bonus_atk + (randomlist [7] + randomlist [8])/2 + (randomlist[6]+randomlist[2]/2)+(randomlist [3]+randomlist [1]/2))
        stats_draw_text(f'{ivan_attack}', fontMenu, (255,255,150),screen, 1165,550)
#----------------------------FreeStatsButton---------------------------

        with open('charstats.txt', 'w') as file:
            file.write(str(ivan_hp))
        with open('charstats.txt', 'a') as file:
            file.write('\n')
            file.write(str(ivan_armor))
            file.write('\n')
            file.write(str(ivan_defence))
            file.write('\n')
            file.write(str(ivan_attack))

#----------------------------HpButton---------------------------
        if hp_plus_button.draw() and stat_distributable !=0:
            bonus_hp += 3
            stat_distributable -= 1
            #pygame.mixer.Sound(select_sound).play()
        if hp_minus_button.draw() and stat_distributable <=8 and bonus_hp >0:
            bonus_hp -= 3
            stat_distributable += 1
            #pygame.mixer.Sound(select_sound).play()
        if bonus_hp > 0:
            screen.blit(plus_green_icon,(347, 549))

#----------------------------ArmButton---------------------------
        if armor_plus_button.draw() and stat_distributable !=0:
            bonus_arm += 3
            stat_distributable -= 1
            #pygame.mixer.Sound(select_sound).play()
        if armor_minus_button.draw() and stat_distributable <=8 and bonus_arm >0:
            bonus_arm -= 3
            stat_distributable += 1
            #pygame.mixer.Sound(select_sound).play()
        if bonus_arm > 0:
            screen.blit(plus_green_icon,(517, 549))
#----------------------------DefButton---------------------------
        if def_plus_button.draw() and stat_distributable !=0:
            bonus_def += 1
            stat_distributable -= 1
            #pygame.mixer.Sound(select_sound).play()
        if def_minus_button.draw() and stat_distributable <=8 and bonus_def >0:
            bonus_def -= 1
            stat_distributable += 1
            #pygame.mixer.Sound(select_sound).play()
        if bonus_def > 0:
            screen.blit(plus_green_icon,(917, 549))
#----------------------------AtkButton---------------------------
        if atk_plus_button.draw() and stat_distributable !=0:
            bonus_atk += 1
            stat_distributable -= 1
            #pygame.mixer.Sound(select_sound).play()
        if atk_minus_button.draw() and stat_distributable <=8 and bonus_atk >0:
            bonus_atk -= 1
            stat_distributable += 1
            #pygame.mixer.Sound(select_sound).play()
        if bonus_atk > 0:
            screen.blit(plus_green_icon,(1092, 549))
#----------------------------------------------------------------

        menuClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    stats_running = False
                if event.key == K_o:
                    #fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    menuClick = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False


        pygame.mouse.set_visible(False)
        mouse_position = pygame.mouse.get_pos()
        player_rect.x, player_rect.y = mouse_position
        screen.blit(normal_icon, player_rect)

        pygame.display.update()
        mainClock.tick(60)





































































#-----------------------------------WorldMap---------------------------------------
clock = pygame.time.Clock()

pygame.init()
pygame.mixer.set_num_channels(32)
pygame.mixer.pre_init(44100,-16,2,512)

#pygame.display.set_caption("Vagrant's Lot: World Map") #screen window name

mouse_position = pygame.mouse.get_pos()

world_map = pygame.image.load("WorldMap/Map.png").convert_alpha()
world_map = pygame.transform.scale(world_map, (int(WINDOW_SIZE[0]),(int(WINDOW_SIZE[1]))))

GM_normal_icon = pygame.image.load("WorldMap/cursor_final.png").convert_alpha()
GM_normal_icon = pygame.transform.scale(GM_normal_icon, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.03))))

GM_select_icon = pygame.image.load("WorldMap/icon_select.png").convert_alpha()
GM_select_icon = pygame.transform.scale(GM_select_icon, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.03))))

bag_of_coins = pygame.image.load("WorldMap/bag.png").convert_alpha()
bag_of_coins = pygame.transform.scale(bag_of_coins, (int(WINDOW_SIZE[0]*0.08),(int(WINDOW_SIZE[1]*0.15))))

gm_quest_icon = pygame.image.load("WorldMap/quest_icon.png").convert_alpha()
gm_quest_icon = pygame.transform.scale(gm_quest_icon, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.04))))
gm_quest_icon_inactive = pygame.image.load("WorldMap/quest_icon_inactive.png").convert_alpha()
gm_quest_icon_inactive = pygame.transform.scale(gm_quest_icon_inactive, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.04))))

gm_new_beginnings = pygame.image.load("WorldMap/quest/new_beginnings.png").convert_alpha()
gm_new_beginnings = pygame.transform.scale(gm_new_beginnings, (int(WINDOW_SIZE[0]*0.2),(int(WINDOW_SIZE[1]*0.44))))

gm_dire_wolves = pygame.image.load("WorldMap/quest/wolves.png").convert_alpha()
gm_dire_wolves = pygame.transform.scale(gm_dire_wolves, (int(WINDOW_SIZE[0]*0.2),(int(WINDOW_SIZE[1]*0.46))))

gm_highwaymen= pygame.image.load("WorldMap/quest/bandits.png").convert_alpha()
gm_highwaymen = pygame.transform.scale(gm_highwaymen, (int(WINDOW_SIZE[0]*0.2),(int(WINDOW_SIZE[1]*0.46))))

gm_dragonhunt = pygame.image.load("WorldMap/quest/dragonhunt.png").convert_alpha()
gm_dragonhunt = pygame.transform.scale(gm_dragonhunt, (int(WINDOW_SIZE[0]*0.2),(int(WINDOW_SIZE[1]*0.46))))

gm_finale = pygame.image.load("WorldMap/quest/finalle.png").convert_alpha()
gm_finale = pygame.transform.scale(gm_finale, (int(WINDOW_SIZE[0]*0.2),(int(WINDOW_SIZE[1]*0.36))))

gm_victory_icon = pygame.image.load("BattleScreen/items/victory.png").convert_alpha()
gm_victory_icon = pygame.transform.scale(gm_victory_icon, (int(WINDOW_SIZE[0]*0.02),(int(WINDOW_SIZE[1]*0.04))))


GM_font_TNR = pygame.font.SysFont('Times New Roman', 18)
GM_font_ESK = pygame.font.Font('WorldMap/ESKARGOT.ttf', 36)
GM_font_Lore = pygame.font.SysFont('Times New Roman', 16)


#-------------------------------------QuestList------------------------------------------


scroll = [0,0]
def global_map ():
    play_music('Map')
    global_map_running = True

    WINDOW_SIZE = (1280,720)
    screen = pygame.display.set_mode((1280,720),0,32)
    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    display = pygame.Surface((800,600))
    fullscreen = button.fullscreen
        #not bool(linecache.getline('resolution.txt',1))

    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

    pyautogui.moveTo(750, 400)
    # moving_right = False
    # moving_left = False
    # moving_up = False
    # moving_down = False
    scroll = [0,0]
    GM_player_rect = pygame.Rect((display.get_width()/2), (display.get_height()/2), 50, 50)
    playSoundScroll = True
    playSoundScroll_counter = 0


    dragonhunt_path = open('WorldMap/quest/dragonhunt.txt','r')
    dragonhunt_lore = dragonhunt_path.read()
    dragonhunt_path.close()

    new_beginnings_path = open('WorldMap/quest/new_beginnings.txt','r')
    new_beginnings_lore = new_beginnings_path.read()
    new_beginnings_path.close()

    dire_wolves_path = open('WorldMap/quest/dire_wolves.txt','r')
    dire_wolves_lore = dire_wolves_path.read()
    dire_wolves_path.close()

    highwaymen_path = open('WorldMap/quest/highwaymen.txt','r')
    highwaymen_lore = highwaymen_path.read()
    highwaymen_path.close()

    finale_path = open('WorldMap/quest/finale.txt','r')
    finale_lore = finale_path.read()
    finale_path.close()


    quest_box = []


    def move (rect, movement):
        rect.x += movement[0]
        rect.y += movement[1]
        return rect
    def gm_draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        display.blit(img,(x,y))
    def gm_draw_bag():
        display.blit(bag_of_coins,((display.get_width()*0)-20,display.get_height()*0.84))
        gm_draw_text(f'{button.wealth}', GM_font_ESK, (255,225,100), bag_of_coins.get_width()-30, display.get_height()*0.92)
    def gm_draw_map ():
        display.blit(world_map,(-100-scroll[0],0-scroll[1]))

    class Quest (pygame.sprite.Sprite):
        def __init__(self,x,y,img, story_image,story_text, status):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.clicked = False
            self.story_text = story_text
            self.story_image = story_image
            self.status = status
            self.reward = int


        def draw_story(self,lore, xmodifier,ymodifier):
            msg_list = []
            line_spacing_count = 0
            if self.rect.collidepoint(mouse_position):
                display.blit(self.story_image, (self.rect.x-120, self.rect.y+10))
                gm_draw_text(self.story_text, GM_font_TNR, (255,225,100), self.rect.x-100, self.rect.y+20)
                for line in lore.split('\n'):
                    msg = GM_font_Lore.render(line,True,'#2c2d47')
                    msg_list.append(msg)
                    line_spacing_count += 20
                    display.blit(msg,(self.rect.x-xmodifier, self.rect.y+ymodifier + (line_spacing_count*1)))


        def hide_quest(self):
            if self.rect.collidepoint(mouse_position) and self.status == 'unlocked':
                for count,i in enumerate(quest_box):
                    if all(i.status) != 'invisible':
                            i.status = 'invisible'
                self.status = 'unlocked'

        def quest_unavailable (self):
            #if self.rect.collidepoint(mouse_position):
            self.image = gm_quest_icon_inactive
            display.blit(self.image, (self.rect.x,self.rect.y))
            #self.status = 'locked'
            #display.blit(gm_quest_icon_inactive, self.rect.center)
                #gm_draw_text(self.story_text, fontDescription, '#2c2d47', self.rect.x, self.rect.y)

        def initiate(self):
            activate = False
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    activate = True
                    self.clicked = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False
                return activate

        # def mouse_position_align(self):
        #     mouse_position = (self.rect.centerx, self.rect.centery)
        #     pos = (self.rect.centerx, self.rect.centery)
        #     return mouse_position

        #def scroll_sound_play (self):
    def restart_game ():
        play_music('MainTheme')
        button.quest_new_beginnings = 'unlocked'
        button.quest_dire_wolves = 'invisible'
        button.quest_highwaymen = 'invisible'
        button.quest_dragonhunt = 'invisible'
        button.quest_finale = 'invisible'
        button.start_wealth = 150
        button.wealth = 0 + button.start_wealth

    while global_map_running:
        #display.fill((170,140,100))
        display.fill('#192740')
        gm_draw_map()
        gm_draw_bag()

        gm_draw_text('Press ESC to Leave', fontDescription, (0,225,0), 10,10)

        scroll[0] += (GM_player_rect.x - scroll[0] -300) /20
        scroll[1] += (GM_player_rect.y - scroll[1] -200) /20

        pygame.mouse.set_visible(False)

        mouse_position = pygame.mouse.get_pos()
        GM_player_rect.x, GM_player_rect.y = mouse_position

#---------------------------SoundCounter---------------------------------------
        playSoundScroll_counter += 1
        if playSoundScroll_counter >= 11:
            playSoundScroll = True
            playSoundScroll_counter = 0


        #---------------------------XMovement---------------------------------
        player_movement = [0,0]
        # if moving_right == True:
        #     player_movement[0] +=1
        # if moving_left == True:
        #     player_movement[0] -=1
        #---------------------------YMovement---------------------------------
        # if moving_up == True:
        #     player_movement[1] -=1
        # if moving_down == True:
        #     player_movement[1] +=1

        if GM_player_rect.x >= 740:
            GM_player_rect.x = 740
        if GM_player_rect.x <= 100:
            GM_player_rect.x = 100

        if GM_player_rect.y >= 460:
            GM_player_rect.y = 460
        if GM_player_rect.y <= 100:
            GM_player_rect.y = 100

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                   screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                #---------------------------------
                if event.key == K_i:
                    pass

                # if event.key == K_d:
                #     moving_right = True
                # if event.key == K_a:
                #     moving_left = True
                # #-------------Sneak---------------
                # if event.key == K_s:
                #     moving_down = True
                # #-------------Jumping-------------
                # if event.key == K_w:
                #     moving_up = True
                #---------------------------------
                if event.key == K_o:
                    #fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen


                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

                if event.key == K_ESCAPE:
                    pygame.mixer.fadeout(2500)
                    restart_game()

                    print(button.start_wealth)
                    print(button.wealth)

                    global_map_running = False

            if event.type == KEYUP:
                # if event.key == K_d:
                #     moving_right = False
                # if event.key == K_a:
                #     moving_left = False
                # if event.key == K_w:
                #     moving_up = False
                # if event.key == K_s:
                #     moving_down = False
                if event.key == K_i:
                    pass

        GM_player_rect = move (GM_player_rect,player_movement)

#------------------------------------WorldMapQuestsList-------------------------------------

        new_beginnings = Quest (745-scroll[0],145-scroll[1], gm_quest_icon, gm_new_beginnings,'New Beginnings', f'{button.quest_new_beginnings}')
        dire_wolves = Quest (720-scroll[0],100-scroll[1], gm_quest_icon, gm_dire_wolves,'Dire Wolves', f'{button.quest_dire_wolves}')
        highwaymen = Quest (755-scroll[0],110-scroll[1], gm_quest_icon, gm_highwaymen,'Highwaymen', f'{button.quest_highwaymen}')
        dragonhunt = Quest (730-scroll[0],190-scroll[1], gm_quest_icon, gm_dragonhunt,'Dragonhunt', f'{button.quest_dragonhunt}')
        finale = Quest (710-scroll[0],140-scroll[1], gm_victory_icon, gm_finale,'', f'{button.quest_finale}')


        quest_box.append(new_beginnings)
        quest_box.extend((dire_wolves,highwaymen,dragonhunt, finale))


        quest_group = pygame.sprite.Group()

    #-------------------------InvisibilityChecks-------------------------
        new_beginnings.hide_quest()
        dire_wolves.hide_quest()
        highwaymen.hide_quest()
        dragonhunt.hide_quest()
        finale.hide_quest()

    #--------------------------------WorldMapQuestsDetails-----------------------------------
#-------------------------NewBeginnings-------------------------
        if new_beginnings.status == 'unlocked':
            quest_group.add(new_beginnings)             #add quests here too
            if new_beginnings.initiate():
                pygame.mixer.music.fadeout(1500)
                new_beginnings_battle()

            new_beginnings.draw_story(new_beginnings_lore, 110,155)

            if new_beginnings.rect.collidepoint(mouse_position):
                if playSoundScroll == True :
                    scroll_sound.play()
                    playSoundScroll = False
                elif playSoundScroll_counter == 10:
                     playSoundScroll_counter = 0

        elif new_beginnings.status == 'locked':
            new_beginnings.quest_unavailable()

#-------------------------DireWolves-------------------------
        if dire_wolves.status == 'unlocked':
            quest_group.add(dire_wolves)
            if dire_wolves.initiate():
                pygame.mixer.music.fadeout(1500)
                dire_wolves_battle()             #battle file load here

            dire_wolves.draw_story(dire_wolves_lore, 110, 152)

            if dire_wolves.rect.collidepoint(mouse_position):
                if playSoundScroll == True :
                    scroll_sound.play()
                    playSoundScroll = False
                elif playSoundScroll_counter == 10:
                    playSoundScroll_counter = 0

        elif dire_wolves.status == 'locked':
            dire_wolves.quest_unavailable()

#-------------------------Highwaymen-------------------------
        if highwaymen.status == 'unlocked':
            quest_group.add(highwaymen)
            if highwaymen.initiate():
                pygame.mixer.music.fadeout(1500)
                highwaymen_battle()             #battle file load here

            highwaymen.draw_story(highwaymen_lore,110,165)

            if highwaymen.rect.collidepoint(mouse_position):
                if playSoundScroll == True :
                    scroll_sound.play()
                    playSoundScroll = False
                elif playSoundScroll_counter == 10:
                    playSoundScroll_counter = 0

        elif highwaymen.status == 'locked':
            highwaymen.quest_unavailable()


#-------------------------Dragonhunt-------------------------
        if dragonhunt.status == 'unlocked':
            quest_group.add(dragonhunt)
            if dragonhunt.initiate():
                pygame.mixer.music.fadeout(1500)
                dragonhunt_battle()             #battle file load here

            dragonhunt.draw_story(dragonhunt_lore,110,133)

            if dragonhunt.rect.collidepoint(mouse_position):
                if playSoundScroll == True :
                    scroll_sound.play()
                    playSoundScroll = False
                elif playSoundScroll_counter == 10:
                    playSoundScroll_counter = 0

        elif dragonhunt.status == 'locked':
            dragonhunt.quest_unavailable()

        #-------------------------Finale-------------------------
        if finale.status == 'unlocked':
            quest_group.add(finale)
            if finale.initiate():
                pygame.mixer.music.fadeout(1500)
                restart_game()
                global_map_running = False

            finale.draw_story(finale_lore,110,0)

            if finale.rect.collidepoint(mouse_position):
                if playSoundScroll == True :
                    scroll_sound.play()
                    playSoundScroll = False
                elif playSoundScroll_counter == 10:
                    playSoundScroll_counter = 0

        elif finale.status == 'locked':
            finale.quest_unavailable()


        #------------------------------------WorldMapQuests------------------------------------
        quest_group.draw(display)
        quest_group.update()

        display.blit(GM_normal_icon, GM_player_rect)


        for i in quest_group:
            if i.rect.collidepoint(mouse_position):
                pygame.mouse.set_visible(False)
                display.blit(GM_select_icon,mouse_position)

    #---------------------------------------------------------------------
        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        #screen.blit(pygame.transform.scale(display,WINDOW_SIZE))

        pygame.display.update()
        clock.tick(60)






























































































































def new_beginnings_battle ():
    new_beginnings_battle_running = True

    clock = pygame.time.Clock()
    pygame.init()

    pygame.mixer.set_num_channels(32)
    pygame.mixer.pre_init(44100,-16,2,512)
    #-----------------------------GameWindowSettings----------------------
    pygame.display.set_caption("New Beginnings")
    WINDOW_SIZE = (1280,720)
    screen = pygame.display.set_mode((1280,720),0,32)
    #display = pygame.Surface((600,400))


    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    fullscreen = button.fullscreen
    #not bool(linecache.getline('resolution.txt',1))
    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)


    #-----------------------------------Battlemap,Interface------------------------
    bg_backscreen = pygame.image.load("BattleScreen/background.png").convert_alpha()
    bg_backscreen = pygame.transform.scale(bg_backscreen, (int(WINDOW_SIZE[0]*1.00),(int(WINDOW_SIZE[1]*0.75))))

    note_map = pygame.image.load("BattleScreen/note_Faroak0.png").convert_alpha()
    note_map = pygame.transform.scale(note_map, (int(WINDOW_SIZE[0]*0.21),(int(WINDOW_SIZE[1]*0.28))))

    bg_map = pygame.image.load("BattleScreen/BattleMap0.png").convert_alpha()
    bg_map = pygame.transform.scale(bg_map, (int(WINDOW_SIZE[0]*0.70),(int(WINDOW_SIZE[1]*0.70))))

    panel = pygame.image.load("BattleScreen/gamepanel0.png").convert_alpha()
    panel = pygame.transform.scale(panel, (int(WINDOW_SIZE[0]*1.10),(int(WINDOW_SIZE[1]*1.40))))

    bag_of_coins = pygame.image.load("BattleScreen/bag.png").convert_alpha()
    bag_of_coins = pygame.transform.scale(bag_of_coins, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    #-----------------------------------Icons-------------------------------------
    attack_icon = pygame.image.load("BattleScreen/icon_fight.png").convert_alpha()
    attack_icon = pygame.transform.scale(attack_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))

    normal_icon = pygame.image.load("BattleScreen/cursor_final.png").convert_alpha()
    normal_icon = pygame.transform.scale(normal_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))


    skip_turn_img = pygame.image.load("BattleScreen/skip_turn.png").convert_alpha()
    skip_turn_img = pygame.transform.scale(skip_turn_img, (int(WINDOW_SIZE[0]*0.06),(int(WINDOW_SIZE[1]*0.05))))

    #-----------------------------------Characters---------------------------------
    # militia_image = pygame.image.load("BattleScreen/militia/idle/0.png").convert_alpha()
    # landsknecht_image = pygame.image.load("BattleScreen/landsknecht/idle/0.png").convert_alpha()

    #------------------------------------------------------------------------------
    #--------------------------------Items----------------------------------------
    inventory_bag = pygame.image.load("BattleScreen/items/inventorybag.png").convert_alpha()
    inventory_bag = pygame.transform.scale(inventory_bag, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    health_potion = pygame.image.load("BattleScreen/items/health_potion.png").convert_alpha()
    health_potion = pygame.transform.scale(health_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    defence_potion = pygame.image.load("BattleScreen/items/reflexes_potion.png").convert_alpha()
    defence_potion = pygame.transform.scale(defence_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    berserk_potion = pygame.image.load("BattleScreen/items/berserk_potion.png").convert_alpha()
    berserk_potion = pygame.transform.scale(berserk_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))


    doors_icon = pygame.image.load("BattleScreen/items/castledoors.png").convert_alpha()
    doors_icon = pygame.transform.scale(doors_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    retry_icon = pygame.image.load("BattleScreen/items/try again.png").convert_alpha()
    retry_icon = pygame.transform.scale(retry_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    victory_icon = pygame.image.load("BattleScreen/items/victory.png").convert_alpha()
    victory_icon = pygame.transform.scale(victory_icon, (int(WINDOW_SIZE[0]*0.15),(int(WINDOW_SIZE[1]*0.15))))

    #------------------------------------------------------------------------------
    screen.fill((242,238,203))

    mouse_position = (0, 0)
    #----------------------------------Music----------------------------------------
    #open_inventory_bag = pygame.mixer.Sound('sounds/OpenInventory.mp3')

    play_music('Battle')

    #------------------------   -------------------------------------------------------
    attack_sound = pygame.mixer.Sound('BattleScreen/items/attack sound.wav')
    arrow_sound = pygame.mixer.Sound('BattleScreen/items/arrow.wav')
    snarl_sound = pygame.mixer.Sound('BattleScreen/items/snarl.wav')
    stone_sound = pygame.mixer.Sound('BattleScreen/items/throwingstone.wav')
    #------------------------------------ActionOrder--------------------------------
    current_fighter = 1

    action_cooldown = 0
    action_waittime = 100
    draw_cursor = False
    battle_status = 0    #0 - nothing, 1 = lost, 2 = won

    play_victory_music = True
    # if battle_status ==0:
    #     play_music('Battle')
    # if battle_status ==2:
    #     play_music('BattleVictory')
    if battle_status ==1:
        play_music('BattleDefeat')


    #------------------------------------BattleInterface (line 315)-------------------
    engage = False
    clicked = False
    skip_turn = False
    #total_fighters = 11
    show_indicators = True

    use_health_potion = False
    health_potion_restores = 50

    use_defence_potion = False
    defence_potion_adds = 100

    use_berserk_potion = False
    berserk_potion_adds = 30


    #----------------------------------ShowStats------------------------------------
    font =pygame.font.SysFont('Times New Roman', 18)
    fontBag = pygame.font.Font('WorldMap/ESKARGOT.ttf', 38)
    fontDMG = pygame.font.Font('WorldMap/ESKARGOT.ttf', 26)
    fontActive = pygame.font.Font('WorldMap/ESKARGOT.ttf', 80)
    fontBattle = pygame.font.SysFont('Times New Roman', 70)
    #pygame.font.Font('WorldMap/ESKARGOT.ttf', 70)


    red = (230,16,35)
    ginger = (245,116,34)
    green = (0,255,0)
    paper =  (255,150,100)
    blue = (0,0,255)
    lightblue = (240,248,255)




    def draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
    #--------------------------------------------------------------------------------

    def draw_bgBackscreen ():
        screen.blit(bg_backscreen,(0,0))

    # def draw_noteMap():
    #     screen.blit(note_map,(998,12))

    def draw_bg():
        screen.blit(bg_map,(210,40))

    def draw_bag():
        screen.blit(bag_of_coins,(0,0))
        draw_text(f'{button.wealth}', fontBag, (255,225,100), 120, 30)

    #------------------------------DrawingIndicators------------------------
    def draw_panel():
        screen.blit(panel,(-50,-35))
        # for count, i in enumerate(army_player):
        #       draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))
        # for count, i in enumerate(army_hostiles):
        #     draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (100,0,0), ((panel.get_width())*0.58), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))

    #-------------------------------------------------------------------------
    yvan_hp = int(linecache.getline('charstats.txt',1))
    yvan_armor = int(linecache.getline('charstats.txt',2))
    yvan_defene = int(linecache.getline('charstats.txt',3))
    yvan_attack = int(linecache.getline('charstats.txt',4))

    #----------------------------------Charaters------------------------------
    class Fighter():
        def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
            self.id=id
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_armor = max_armor
            self.armor = max_armor
            self.defence = defence
            self.start_defence = defence
            self.strength = strength
            self.start_strength = strength
            self.reach = reach
            self.special = special
            self.max_inventory = max_inventory
            self.inventory = max_inventory
            self.start_resistance = resistance
            self.resistance = resistance
            self.start_tricks = tricks
            self.tricks = tricks
            self.alive = True
            self.hostile = True
            self.animation_list = [] #list of lists (action/img)
            self.frame_index = 0
            self.action = 0 #0-idle / 1-attack / 2-hurt / 3-death  updates via self.animation_list = []
            self.update_time = pygame.time.get_ticks()  # how much time has passed

            #-----------------------------Animations--------------------------------------------
            #loading idle action images
            temp_list = []
            for i in range(2):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/idle/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            #loading attack action images
            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/attack/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/hurt/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/dead/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img

            #-----------------------------------------------------------------------------------
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]     # to control action/images
            # two lists (action/frames)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

        #---------------------------------------------------------------------
        def update(self,animation_modifier): #animation
            animation_cooldown = 100
            if self.action == 0:
                animation_cooldown = 1000*animation_modifier
            if self.action == 1:
                animation_cooldown = 150*animation_modifier
            if self.action == 2:
                animation_cooldown = 300*animation_modifier
            if self.action == 3:
                animation_cooldown = 250*animation_modifier

            #animation_cooldown = cooldown
            self.image = self.animation_list[self.action][self.frame_index]  #adding action
            if pygame.time.get_ticks() - self.update_time > animation_cooldown: #if its more than 100 its time to update the animation stage
                self.update_time = pygame.time.get_ticks() #resets timer
                self.frame_index += 1
            # if animation run out, reset
            if self.frame_index >= len(self.animation_list[self.action]):  #adding action

                #after death unit should stay at the last frame of the dead animation sequence
                if self.action == 3:    #dead animation in the list.
                    self.frame_index = len(self.animation_list[self.action])-1  #final frame
                else:
                    self.idle() # sets to idle animation

        #-----------------------------------Idle----------------------------
        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def hurt(self):
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def dead(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def reset(self):
            self.alive = True
            self.inventory = self.max_inventory
            self.hp = self.max_hp
            self.armor = self.max_armor
            self.defence = self.start_defence
            self.strength = self.start_strength
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Attack----------------------------
        def attack(self,target):
            rand = random.randint(-5,5)
            damage = self.strength + rand
            if self.special == 1:
                #target.armor -= 0
                target.hp -= damage
            elif self.special != 1:
                target.armor -= int(damage*(target.defence/100))
                if target.armor > 0:
                    target.hp -= int(damage*(1 - target.defence/100))
                if target.armor <= 0:
                    target.hp -= int((damage*(1 - target.defence/100)-target.armor))
                    target.armor = 0
            # runs hurn animation
            target.hurt()

            if target.hp < 1:
                target.hp = 0
                target.alive = False
                # runs death animation
                target.dead()

            #DamageText
            if self.special != 1:
                if target.armor > 1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage*(1 - target.defence/100))), red)
                if target.armor <=1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
            else:
                damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)

            damage_text_group.add(damage_text)
            #---------------------------------AttackSounds---------------------------------------
            #attack sound # 0-standard blade; 1-arrow; 2-stone
            if self.special == 0:
                pygame.mixer.Sound(attack_sound).play()
            elif self.special == 1:
                pygame.mixer.Sound(arrow_sound).play()
            elif self.special == 2:
                pygame.mixer.Sound(stone_sound).play()
            elif self.special == 3:
                pygame.mixer.Sound(snarl_sound).play()
            #------------------------------------------------------------------------------------


            #animations
            self.action = 1   # set action frames to as 1 as 1 = attack folder animation
            self.frame_index = 0 # frame 0 in the attack folder animation
            self.update_time = pygame.time.get_ticks()

        #----------------------------------------------------------------------
        def draw(self):
            screen.blit(self.image, self.rect)

    #-----------------------------------HealthBar--------------------------
    class healthBar ():
        def __init__(self, x,y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp
        def draw (self, hp):
            self.hp = hp
            # health ration
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen,red,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,green,(self.x, self.y, 50*ratio,5))

    #-----------------------------------ArmorBar--------------------------
    class armorBar ():
        def __init__(self, x,y, armor, max_armor):
            self.x = x
            self.y = y
            self.armor = armor
            self.max_armor = max_armor
        def draw (self, armor):
            self.armor = armor
            # health ration
            ratio = self.armor / self.max_armor
            pygame.draw.rect(screen,lightblue,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,blue,(self.x, self.y, 50*ratio,5))

    #-----------------------------------AttributeChangeBar-----------------
    class DamageText(pygame.sprite.Sprite):   # sprite is updated automatically
        def __init__(self,x,y,damage, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = fontDMG.render(damage, True, color)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.counter = 0

        def update(self):
            #move text
            self.rect.y -=1
            #delete after timer
            self.counter +=1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()    #python list
    #def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
    #-----------------------------------PlayerArmy--------------------------
    # militia = Fighter (435,295, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia_healthbar = healthBar (militia.rect.centerx-25,militia.rect.centery-55,militia.hp, militia.max_hp)
    # militia_armorbar = armorBar (militia.rect.centerx-25,militia.rect.centery-50,militia.armor, militia.max_armor)
    #-----------------------------------------------------------------------
    boy = Fighter (435,305, 'boy',120,60,35,40,1,3,0,True,False,0,0)
    boy_healthbar = healthBar (boy.rect.centerx-25,boy.rect.centery-55,boy.hp, boy.max_hp)
    boy_armorbar = armorBar (boy.rect.centerx-25,boy.rect.centery-50,boy.armor, boy.max_armor)
    #-----------------------------------------------------------------------
    landsknecht = Fighter (530,250,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht_healthbar = healthBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-55,landsknecht.hp, landsknecht.max_hp)
    landsknecht_armorbar = armorBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-50,landsknecht.armor, landsknecht.max_armor)
    #-----------------------------------------------------------------------
    landsknecht1 = Fighter (620,205,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht1_healthbar = healthBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-55,landsknecht1.hp, landsknecht1.max_hp)
    landsknecht1_armorbar = armorBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-50,landsknecht1.armor, landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    chevalier = Fighter (720,135,'chevalier',120,100,65,70,1,0,1,True,False,0,0)
    chevalier_healthbar = healthBar (chevalier.rect.centerx-25,chevalier.rect.centery-65,chevalier.hp, chevalier.max_hp)
    chevalier_armorbar = armorBar (chevalier.rect.centerx-25,chevalier.rect.centery-60,chevalier.armor, chevalier.max_armor)
    #-----------------------------------------------------------------------
    # militia1 = Fighter (700,165, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia1_healthbar = healthBar (militia1.rect.centerx-25,militia1.rect.centery-55,militia1.hp, militia1.max_hp)
    # militia1_armorbar = armorBar (militia1.rect.centerx-25,militia1.rect.centery-50,militia1.armor, militia1.max_armor)
    # #-----------------------------------------------------------------------
    # militia2 = Fighter (790,115, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia2_healthbar = healthBar (militia2.rect.centerx-25,militia2.rect.centery-55,militia2.hp, militia2.max_hp)
    # militia2_armorbar = armorBar (militia2.rect.centerx-25,militia2.rect.centery-50,militia2.armor, militia2.max_armor)
    # #-----------------------------------------------------------------------
    archer = Fighter (530,115, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer_healthbar = healthBar (archer.rect.centerx-25,archer.rect.top-20,archer.hp, archer.max_hp)
    archer_armorbar = armorBar (archer.rect.centerx-25,archer.rect.top-15,archer.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    archer1 = Fighter (440,160, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer1_healthbar = healthBar (archer1.rect.centerx-25,archer1.rect.top-20,archer1.hp, archer.max_hp)
    archer1_armorbar = armorBar (archer1.rect.centerx-25,archer1.rect.top-15,archer1.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    yvan = Fighter (350,210, 'yvan',yvan_hp,yvan_armor,yvan_defene,yvan_attack,2,2,0,True,False,0,0)
    yvan_healthbar = healthBar (yvan.rect.centerx-25,yvan.rect.top-20,yvan.hp, yvan.max_hp)
    yvan_armorbar = armorBar (yvan.rect.centerx-25,yvan.rect.top-15,yvan.armor, yvan.max_armor)
    #max_hp,max_armor, defence, strength,



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_player = []
    #army_player.append(militia)
    army_player.append(boy)
    army_player.append(landsknecht)
    army_player.append(landsknecht1)
    army_player.append(chevalier)
    #army_player.append(militia1)
    #army_player.append(militia2)
    army_player.append(archer)
    army_player.append(archer1)
    army_player.append(yvan)

    army_player_front = army_player[:4]

    #-----------------------------HostileArmy-------------------------------
    # h_militia = Fighter(570,365,'militia',60,30,35,30,1,0,1,True,True,0,0)
    # h_militia_healthbar = healthBar(h_militia.rect.centerx-25,h_militia.rect.centery-55,h_militia.hp, h_militia.max_hp)
    # h_militia_armorbar = armorBar(h_militia.rect.centerx-25,h_militia.rect.centery-50,h_militia.armor, h_militia.max_armor)
    #-----------------------------------------------------------------------
    h_brigand = Fighter(570,365,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    h_brigand_healthbar = healthBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-55,h_brigand.hp, h_brigand.max_hp)
    h_brigand_armorbar = armorBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-50,h_brigand.armor, h_brigand.max_armor)

    #-----------------------------------------------------------------------
    h_brigand1 = Fighter(660,325,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    h_brigand1_healthbar = healthBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-55,h_brigand1.hp, h_brigand1.max_hp)
    h_brigand1_armorbar = armorBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-50,h_brigand1.armor, h_brigand1.max_armor)

    #-----------------------------------------------------------------------
    h_landsknecht = Fighter (750,280,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht_healthbar = healthBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-55,h_landsknecht.hp, h_landsknecht.max_hp)
    h_landsknecht_armorbar = armorBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-50,h_landsknecht.armor, h_landsknecht.max_armor)
    #-----------------------------------------------------------------------
    h_landsknecht1 = Fighter (840,235,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht1_healthbar = healthBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-55,h_landsknecht1.hp, h_landsknecht1.max_hp)
    h_landsknecht1_armorbar = armorBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-50,h_landsknecht1.armor, h_landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    h_brigand2 = Fighter(940,195,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    h_brigand2_healthbar = healthBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-55,h_brigand2.hp, h_brigand2.max_hp)
    h_brigand2_armorbar = armorBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-50,h_brigand2.armor, h_brigand2.max_armor)
    #-----------------------------------------------------------------------
    # h_landsknecht2 = Fighter (790,340,'landsknecht',90,55,40,50,2,0,1,True,True,0,0)
    # h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    # h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    #-----------------------------------------------------------------------
    h_bowman = Fighter (790,350, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman_healthbar = healthBar (h_bowman.rect.centerx-25,h_bowman.rect.top-20,h_bowman.hp, h_bowman.max_hp)
    h_bowman_armorbar = armorBar (h_bowman.rect.centerx-25,h_bowman.rect.top-15,h_bowman.armor, h_bowman.max_armor)
    #-----------------------------------------------------------------------
    h_bowman1 = Fighter (695,400, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman1_healthbar = healthBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-20,h_bowman1.hp, h_bowman1.max_hp)
    h_bowman1_armorbar = armorBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-15,h_bowman1.armor, h_bowman1.max_armor)
    #-----------------------------------------------------------------------
    h_bowman2 = Fighter (880,310, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman2_healthbar = healthBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-20,h_bowman2.hp, h_bowman2.max_hp)
    h_bowman2_armorbar = armorBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-15,h_bowman2.armor, h_bowman2.max_armor)
    #-----------------------------------------------------------------------
    h_bowman3 = Fighter (960,260, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman3_healthbar = healthBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-20,h_bowman3.hp, h_bowman3.max_hp)
    h_bowman3_armorbar = armorBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-15,h_bowman3.armor, h_bowman3.max_armor)



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_hostiles = []
    army_hostiles.append(h_brigand)
    army_hostiles.append(h_brigand1)
    army_hostiles.append(h_landsknecht)
    army_hostiles.append(h_landsknecht1)
    army_hostiles.append(h_brigand2)
    army_hostiles.append(h_bowman)
    army_hostiles.append(h_bowman1)
    army_hostiles.append(h_bowman2)
    army_hostiles.append(h_bowman3)

    army_hostiles_front = army_hostiles[:5]


    #------------------------------TotalUnitNumber----------------------------
    total_hostiles = len(army_hostiles)
    total_allies = len(army_player)
    total_fighters = total_hostiles + total_allies

    #------------------------------ItemsUse(Button)---------------------------
    #inventory_button = button.Button(screen,WINDOW_SIZE[0]*0 + 110, WINDOW_SIZE[1]*0 - 6,inventory_bag,280,120,0, True, 'Inventory')

    inventory_button = button.ToggleButton(screen,-65, 425,inventory_bag,260,120,0, True, 'Inventory')
    #------------------------------ItemsUse(PotionButton)-------------------
    potion_button = button.Button(screen, WINDOW_SIZE[0]*0.01, WINDOW_SIZE[1]*0.90, health_potion, 48,72,30, False,f'Health Potion. Restores {health_potion_restores} HP')
    potion_button1 = button.Button(screen, WINDOW_SIZE[0]*0.06, WINDOW_SIZE[1]*0.90, defence_potion, 48,72,40, False,f'Defence Potion. Gives {defence_potion_adds} DEF/ARM')
    potion_button2 = button.Button(screen, WINDOW_SIZE[0]*0.11, WINDOW_SIZE[1]*0.90, berserk_potion, 48,72,60, False,f'Berserk Potion. Gives {berserk_potion_adds} ATK / Removes {int(berserk_potion_adds*1)} DEF')


    #------------------------------IconToggle(Reset)------------------------
    restart_button = button.Button(screen, 1100, 8, retry_icon, 84,90,25, True,'Try Again')
    skip_turn_button = button.Button(screen, WINDOW_SIZE[0]*0.92, WINDOW_SIZE[1]*0.62, skip_turn_img, 86,82,60, False,f'Skip Turn')
    victory_button = button.Button(screen, 1170, 15, victory_icon, 86,90,25, True,'Back to Map')
    leave_button = button.Button(screen, 1190, 0, doors_icon, 64,90,25, True,'Leave Battlefield')


    #-----------------------------------------------------------------------

    while new_beginnings_battle_running:
        #display.fill((146,244,255))
        draw_bgBackscreen()
        #draw_noteMap()  # location map
        draw_bg()
        draw_panel()
        draw_bag()

        #-----------------------------DrawingUnits/AnimatioSpeedMod------------
        for units in army_player:
            # militia.update(0.9)
            # militia.draw()
            #------------
            landsknecht.update(1)
            landsknecht.draw()
            #------------
            chevalier.update(1.3)
            chevalier.draw()
            #------------
            # militia1.update(0.88)
            # militia1.draw()
            #------------
            boy.update(0.88)
            boy.draw()
            #------------
            landsknecht1.update(1.1)
            landsknecht1.draw()
            #------------
            # militia2.update(0.84)
            # militia2.draw()
            #------------
            archer.update(0.95)
            archer.draw()
            #------------
            archer1.update(0.92)
            archer1.draw()
            #------------
            yvan.update(1.05)
            yvan.draw()

        for hostile in army_hostiles:
            h_brigand.update(0.9)
            h_brigand.draw()
            #------------
            h_brigand2.update(0.85)
            h_brigand2.draw()
            #------------
            h_landsknecht.update(0.95)
            h_landsknecht.draw()
            #------------
            h_landsknecht1.update(0.98)
            h_landsknecht1.draw()
            #------------
            h_brigand1.update(0.9)
            h_brigand1.draw()
            #------------
            h_bowman.update(0.89)
            h_bowman.draw()
            #------------
            h_bowman1.update(0.85)
            h_bowman1.draw()
            #------------
            h_bowman2.update(0.92)
            h_bowman2.draw()
            #------------
            h_bowman3.update(0.90)
            h_bowman3.draw()
        #-----------------------------HealthBar/ArmorBar-----------------------
        #-------------Player------------------------
        if show_indicators == True:
            if chevalier.alive == True:
                chevalier_healthbar.draw(chevalier.hp)
                chevalier_armorbar.draw(chevalier.armor)
            # if militia.alive == True:
            #     militia_healthbar.draw(militia.hp)
            #     militia_armorbar.draw(militia.armor)
            if boy.alive == True:
                boy_healthbar.draw(boy.hp)
                boy_armorbar.draw(boy.armor)
            if landsknecht.alive == True:
                landsknecht_healthbar.draw(landsknecht.hp)
                landsknecht_armorbar.draw(landsknecht.armor)
            # if militia1.alive == True:
            #     militia1_healthbar.draw(militia1.hp)
            #     militia1_armorbar.draw(militia1.armor)
            if landsknecht1.alive == True:
                landsknecht1_healthbar.draw(landsknecht1.hp)
                landsknecht1_armorbar.draw(landsknecht1.armor)
            # if militia2.alive == True:
            #     militia2_healthbar.draw(militia2.hp)
            #     militia2_armorbar.draw(militia2.armor)
            if archer.alive == True:
                archer_healthbar.draw(archer.hp)
                archer_armorbar.draw(archer.armor)
            if archer1.alive == True:
                archer1_healthbar.draw(archer1.hp)
                archer1_armorbar.draw(archer1.armor)
            if yvan.alive == True:
                yvan_healthbar.draw(yvan.hp)
                yvan_armorbar.draw(yvan.armor)

            #------------------Enemy--------------------
            if h_brigand.alive == True:
                h_brigand_healthbar.draw(h_brigand.hp)
                h_brigand_armorbar.draw(h_brigand.armor)
            if h_brigand2.alive == True:
                h_brigand2_healthbar.draw(h_brigand2.hp)
                h_brigand2_armorbar.draw(h_brigand2.armor)
            if h_landsknecht.alive == True:
                h_landsknecht_healthbar.draw(h_landsknecht.hp)
                h_landsknecht_armorbar.draw(h_landsknecht.armor)
            if h_landsknecht1.alive == True:
                h_landsknecht1_healthbar.draw(h_landsknecht1.hp)
                h_landsknecht1_armorbar.draw(h_landsknecht1.armor)
            if h_brigand1.alive == True:
                h_brigand1_healthbar.draw(h_brigand1.hp)
                h_brigand1_armorbar.draw(h_brigand1.armor)
            if h_bowman.alive == True:
                h_bowman_healthbar.draw(h_bowman.hp)
                h_bowman_armorbar.draw(h_bowman.armor)
            if h_bowman1.alive == True:
                h_bowman1_healthbar.draw(h_bowman1.hp)
                h_bowman1_armorbar.draw(h_bowman1.armor)
            if h_bowman2.alive == True:
                h_bowman2_healthbar.draw(h_bowman2.hp)
                h_bowman2_armorbar.draw(h_bowman2.armor)
            if h_bowman3.alive == True:
                h_bowman3_healthbar.draw(h_bowman3.hp)
                h_bowman3_armorbar.draw(h_bowman3.armor)
        #----------------------------------------------------------------------

        #-----------------------------DamageText-----------------------------
        damage_text_group.update()
        damage_text_group.draw(screen)
        #methods update and draw are parts of the sprite.

        #-----------------------------Items/SkipTurn/Inventory-----------------------------
        pos = pygame.mouse.get_pos()
        if skip_turn_button.rect.collidepoint(pos):
            draw_text(f'{skip_turn_button.description}', fontDMG, green, skip_turn_button.rect.x-30,skip_turn_button.rect.y+100)
        if skip_turn_button.draw():
            skip_turn=True
        if battle_status != 2 and leave_button.available == True:
            if leave_button.rect.collidepoint(pos):
                draw_text(f'{leave_button.description}', fontDMG, green, leave_button.rect.x-140,leave_button.rect.y+100)
            if leave_button.draw():
                #pyautogui.moveTo(750, 400)
                play_music('Map')
                button.wealth = button.start_wealth
                new_beginnings_battle_running = False


        if inventory_button.rect.collidepoint(pos):
            draw_text(f'{inventory_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)
        if inventory_button.toggled == True and battle_status ==0:
            potion_button.available = True
            potion_button1.available = True
            potion_button2.available = True


            #---------------------HealthPotion--------------------------------------
            if potion_button.available == True:
                if potion_button.draw():
                    use_health_potion = True
                draw_text(f'{potion_button.price}', fontBag, (255,225,100), potion_button.rect.x+5, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button.rect.collidepoint(pos):
                    draw_text(f'{potion_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

            #-------DefencePotion--------------
            if potion_button1.available == True:
                if potion_button1.draw():
                    use_defence_potion = True
                draw_text(f'{potion_button1.price}', fontBag, (255,225,100), potion_button.rect.x+65, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button1.rect.collidepoint(pos):
                    draw_text(f'{potion_button1.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

                #-------BerserkPotion--------------
            if potion_button2.available == True:
                if potion_button2.draw():
                    use_berserk_potion = True
                draw_text(f'{potion_button2.price}', fontBag, (255,225,100), potion_button.rect.x+130, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button2.rect.collidepoint(pos):
                    draw_text(f'{potion_button2.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)


        #---------------------InventoryStock--------------------------------------
        else:
            potion_button.available = False

        #--------------------------------------------------------------------------
        if battle_status ==0:   #win/loose check


            #-----------------------------PlayerAttacking---------------------------
            for count, ally in enumerate(army_player):
                if current_fighter == 1+count:
                    draw_text('^', fontActive, "#FFA500", ally.rect.centerx-20,ally.rect.y -65)
                    if ally.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:

                            if ally.reach == 2:
                                if engage == True and target != None:
                                    # conditioned upon engage below & def attack above
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif ally.reach == 1:
                                if engage == True and target != None and target.reach == 1:
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            for enemy in army_hostiles_front:
                                if all(enemy.alive == False for enemy in army_hostiles_front):
                                    #enemy.alive == False:
                                    if ally.reach == 1:
                                        if engage == True and target != None and target.reach == 2:
                                            ally.reach = 2
                                            ally.attack(target)
                                            current_fighter += 1
                                            action_cooldown = 0


                            #-----------------------------------------SkipTurn-----------------------------------------
                            if skip_turn == True:
                                current_fighter += 1
                                action_cooldown = 0
                                skip_turn_heal = 10
                                if ally.max_hp - ally.hp > skip_turn_heal:    #50
                                    skip_turn_heal = skip_turn_heal
                                else:
                                    skip_turn_heal = ally.max_hp - ally.hp
                                ally.hp += skip_turn_heal
                                #DamageText
                                damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(skip_turn_heal), green)
                                damage_text_group.add(damage_text)
                            skip_turn = False

                            #------------UsingItem(HealthPotion)---------------------------
                            if use_health_potion == True and button.wealth >= potion_button.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_hp - ally.hp > health_potion_restores:    #50
                                        heal_amount = health_potion_restores
                                    else:
                                        heal_amount = ally.max_hp - ally.hp
                                    ally.hp += heal_amount
                                    ally.inventory -= 1
                                    button.wealth -= potion_button.price
                                    #DamageText
                                    damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(heal_amount), green)
                                    damage_text_group.add(damage_text)

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_health_potion = False

                            #----------------------------------------------------
                            #------------UsingItem(DefencePotion)---------------
                            if use_defence_potion == True and button.wealth >= potion_button1.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_armor - ally.armor > defence_potion_adds:    #50
                                        add_defence_amount = defence_potion_adds
                                    else:
                                        add_defence_amount = ally.max_armor - ally.armor
                                    ally.armor += add_defence_amount
                                    ally.defence = 100
                                    ally.inventory -= 1
                                    button.wealth -= potion_button1.price     #Change price

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_defence_potion = False


                            #------------UsingItem(BerserkPotion)---------------
                            if use_berserk_potion == True and button.wealth >= potion_button2.price:
                                if ally.inventory > 0:
                                    ally.strength += berserk_potion_adds
                                    if ally.defence < int(berserk_potion_adds):
                                        ally.defence = 0
                                    else:
                                        ally.defence -= int(berserk_potion_adds)
                                    ally.inventory -= 1
                                    button.wealth -= potion_button2.price

                                    current_fighter +=1
                                    action_cooldown = 0
                                    #Change price
                                use_berserk_potion = False

                    else:
                        current_fighter +=1   #if dead = skip turn

            #-----------------------------EnemyAttacking----------------------------
            for count, enemy in enumerate(army_hostiles):
                if current_fighter == 1+ total_allies + count:   # "3 + count" - checks with the max_fighter var and number of units in army_player
                    draw_text('^', fontActive, "#FFA500", enemy.rect.centerx-20,enemy.rect.y -65)
                    if enemy.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:
                            #health_check
                            if (enemy.hp / enemy.max_hp) <0.5 and enemy.inventory >0:
                                if enemy.max_hp - enemy.hp > health_potion_restores:
                                    heal_amount = health_potion_restores
                                else:
                                    heal_amount = enemy.max_hp - enemy.hp

                                enemy.hp += heal_amount
                                enemy.inventory -= 1

                                #DamageText
                                damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(heal_amount), green)
                                damage_text_group.add(damage_text)

                                current_fighter +=1
                                action_cooldown = 0

                            elif enemy.reach == 2:
                                if enemy.strength >= ally.hp and ally.alive == True:
                                    enemy.attack(ally)
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif enemy.reach == 1:
                                if all(ally.alive == True for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                elif all(ally.alive == False for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 2]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                            #else:
                            #     enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                            #     # enemy.hp += 10
                            #     current_fighter += 1
                            #     action_cooldown = 0
                            #     # damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(10), green)
                            #     # damage_text_group.add(damage_text)

                    else:
                        current_fighter +=1

            #---------------------------------Turns----------------------------
            # if all have had a turn, reset
            if current_fighter > total_fighters:
                current_fighter = 1

        #-----------------------------DefeatStatus-------------------------
        # checking alive/dead status
        alive_allies = 0
        for ally in army_player:
            if ally.alive == True:
                alive_allies +=1
        if alive_allies ==0:
            battle_status =1

        #---------------------------------VictoryStatus--------------------
        alive_enemies = 0
        for enemy in army_hostiles:
            if enemy.alive == True:
                alive_enemies +=1
        if alive_enemies ==0:
            battle_status =2

        #-------------------Defeat/VictoryStatusDisplay-------------------
        if battle_status !=0:
            if battle_status ==1:
                draw_text(f'Defeat!', fontMenuLarge, (155,0,0), screen.get_width()*0.46,0)
                #-------------------ResetButton-----------------------------------
                if restart_button.available == True:
                    if restart_button.draw():
                        play_music('Battle')
                        for ally in army_player:
                            ally.reset()
                        for enemy in army_hostiles:
                            enemy.reset()
                        button.wealth = button.start_wealth         #restart gold here
                        current_fighter = 1
                        action_cooldown = 0
                        battle_status = 0

                        pos = pygame.mouse.get_pos() # text over the button
                    if restart_button.rect.collidepoint(pos):
                        draw_text(f'{restart_button.description}', fontDMG, green, restart_button.rect.x+30,leave_button.rect.y+100)

            #-------------------Defeat/VictoryStatusDisplay-------------------
            if battle_status ==2:
                button.quest_new_beginnings = 'locked'
                draw_text(f'Victory!', fontMenuLarge, green, screen.get_width()*0.46,0)
                if play_victory_music == True:
                    play_music('BattleVictory')
                play_victory_music = False
                if victory_button.available == True:
                    if victory_button.draw():
                        button.wealth += 200
                        button.start_wealth = button.wealth
                        button.quest_dire_wolves = 'unlocked'
                        print(button.start_wealth)
                        print(button.wealth)
                        play_music('Map')
                        new_beginnings_battle_running = False
                    if victory_button.rect.collidepoint(pos):
                        draw_text(f'{victory_button.description}', fontDMG, green, victory_button.rect.x-75,leave_button.rect.y+100)
        #------------------------------End/Controls------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                if event.key == K_f and show_indicators == True:
                    show_indicators = False
                elif event.key == K_f and show_indicators == False:
                    show_indicators = True

                if event.key == K_o:
                    # fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen

                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

            #---------------------ToggleButton------------------------
            inventory_button.event_handler(event) #ToggleButton
            #---------------------ToggleButton------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        if leave_button.clicked == True or victory_button.clicked == True:
            mouse_map_position_align(750,400)
            #pyautogui.moveTo(750, 400)
        #-----------------------------Action/TargetSearch-------------------
        engage = False
        target = None

        inventory_button.draw(screen) #ToggleButton

        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        screen.blit(normal_icon,pos)

        for count, ally in enumerate(army_player):
            if ally.rect.collidepoint(pos) and ally.alive == True:
                draw_text(f'{ally.id} | HP: {ally.hp} | ARM: {ally.armor} | ATK: {ally.strength} | DEF: {ally.defence} | INV: {ally.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))
        for count, enemy in enumerate(army_hostiles):
            if enemy.rect.collidepoint(pos) and enemy.alive == True:
                pygame.mouse.set_visible(False)
                screen.blit(attack_icon,pos)
                draw_text(f'{enemy.id} | HP: {enemy.hp} | ARM: {enemy.armor} | ATK: {enemy.strength} | DEF: {enemy.defence} | INV: {enemy.inventory}', font, (100,0,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))

                # show attack icon
                #--------------chooseTarget&Attack-------------------------
                if clicked == True and enemy.alive == True:
                    engage = True
                    target = army_hostiles[count]


        #-----------------------------------------------------------------------
        #surf = pygame.transform.scale(display, WINDOW_SIZE)
        #screen.blit(surf, (0,0))

        pygame.display.update()
        clock.tick(60)











































































































def dire_wolves_battle ():
    dire_wolves_battle_running = True

    clock = pygame.time.Clock()
    pygame.init()

    pygame.mixer.set_num_channels(32)
    pygame.mixer.pre_init(44100,-16,2,512)
    #-----------------------------GameWindowSettings----------------------
    pygame.display.set_caption("Dire Wolves")
    WINDOW_SIZE = (1280,720)
    screen = pygame.display.set_mode((1280,720),0,32)
    #display = pygame.Surface((600,400))


    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    fullscreen = button.fullscreen
        #not bool(linecache.getline('resolution.txt',1))
    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)


#-----------------------------------Battlemap,Interface------------------------
    bg_backscreen = pygame.image.load("BattleScreen/background.png").convert_alpha()
    bg_backscreen = pygame.transform.scale(bg_backscreen, (int(WINDOW_SIZE[0]*1.00),(int(WINDOW_SIZE[1]*0.75))))

    note_map = pygame.image.load("BattleScreen/note_Faroak0.png").convert_alpha()
    note_map = pygame.transform.scale(note_map, (int(WINDOW_SIZE[0]*0.21),(int(WINDOW_SIZE[1]*0.28))))

    bg_map = pygame.image.load("BattleScreen/BattleMap0.png").convert_alpha()
    bg_map = pygame.transform.scale(bg_map, (int(WINDOW_SIZE[0]*0.70),(int(WINDOW_SIZE[1]*0.70))))

    panel = pygame.image.load("BattleScreen/gamepanel0.png").convert_alpha()
    panel = pygame.transform.scale(panel, (int(WINDOW_SIZE[0]*1.10),(int(WINDOW_SIZE[1]*1.40))))

    bag_of_coins = pygame.image.load("BattleScreen/bag.png").convert_alpha()
    bag_of_coins = pygame.transform.scale(bag_of_coins, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    #-----------------------------------Icons-------------------------------------
    attack_icon = pygame.image.load("BattleScreen/icon_fight.png").convert_alpha()
    attack_icon = pygame.transform.scale(attack_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))

    normal_icon = pygame.image.load("BattleScreen/cursor_final.png").convert_alpha()
    normal_icon = pygame.transform.scale(normal_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))


    skip_turn_img = pygame.image.load("BattleScreen/skip_turn.png").convert_alpha()
    skip_turn_img = pygame.transform.scale(skip_turn_img, (int(WINDOW_SIZE[0]*0.06),(int(WINDOW_SIZE[1]*0.05))))

    #-----------------------------------Characters---------------------------------
    # militia_image = pygame.image.load("BattleScreen/militia/idle/0.png").convert_alpha()
    # landsknecht_image = pygame.image.load("BattleScreen/landsknecht/idle/0.png").convert_alpha()

    #------------------------------------------------------------------------------
    #--------------------------------Items----------------------------------------
    inventory_bag = pygame.image.load("BattleScreen/items/inventorybag.png").convert_alpha()
    inventory_bag = pygame.transform.scale(inventory_bag, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    health_potion = pygame.image.load("BattleScreen/items/health_potion.png").convert_alpha()
    health_potion = pygame.transform.scale(health_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    defence_potion = pygame.image.load("BattleScreen/items/reflexes_potion.png").convert_alpha()
    defence_potion = pygame.transform.scale(defence_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    berserk_potion = pygame.image.load("BattleScreen/items/berserk_potion.png").convert_alpha()
    berserk_potion = pygame.transform.scale(berserk_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))


    doors_icon = pygame.image.load("BattleScreen/items/castledoors.png").convert_alpha()
    doors_icon = pygame.transform.scale(doors_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    retry_icon = pygame.image.load("BattleScreen/items/try again.png").convert_alpha()
    retry_icon = pygame.transform.scale(retry_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    victory_icon = pygame.image.load("BattleScreen/items/victory.png").convert_alpha()
    victory_icon = pygame.transform.scale(victory_icon, (int(WINDOW_SIZE[0]*0.15),(int(WINDOW_SIZE[1]*0.15))))

    #------------------------------------------------------------------------------
    screen.fill((242,238,203))

    mouse_position = (0, 0)
    #----------------------------------Music----------------------------------------
    #open_inventory_bag = pygame.mixer.Sound('sounds/OpenInventory.mp3')

    play_music('Battle')

    #------------------------   -------------------------------------------------------
    attack_sound = pygame.mixer.Sound('BattleScreen/items/attack sound.wav')
    arrow_sound = pygame.mixer.Sound('BattleScreen/items/arrow.wav')
    snarl_sound = pygame.mixer.Sound('BattleScreen/items/snarl.wav')
    stone_sound = pygame.mixer.Sound('BattleScreen/items/throwingstone.wav')
    #------------------------------------ActionOrder--------------------------------
    current_fighter = 1

    action_cooldown = 0
    action_waittime = 100
    draw_cursor = False
    battle_status = 0    #0 - nothing, 1 = lost, 2 = won

    # if battle_status ==0:
    #     play_music('Battle')
    # if battle_status ==2:
    #     pygame.mixer.music.play(0)
    #     play_music('BattleVictory')
    play_victory_music =  True
    if battle_status ==1:
        play_music('BattleDefeat')

    #------------------------------------BattleInterface (line 315)-------------------
    engage = False
    clicked = False
    skip_turn = False
    #total_fighters = 11
    show_indicators = True

    use_health_potion = False
    health_potion_restores = 50

    use_defence_potion = False
    defence_potion_adds = 100

    use_berserk_potion = False
    berserk_potion_adds = 30


    #----------------------------------ShowStats------------------------------------
    font =pygame.font.SysFont('Times New Roman', 18)
    fontBag = pygame.font.Font('WorldMap/ESKARGOT.ttf', 38)
    fontDMG = pygame.font.Font('WorldMap/ESKARGOT.ttf', 26)
    fontActive = pygame.font.Font('WorldMap/ESKARGOT.ttf', 80)
    fontBattle = pygame.font.SysFont('Times New Roman', 70)
    #pygame.font.Font('WorldMap/ESKARGOT.ttf', 70)


    red = (230,16,35)
    ginger = (245,116,34)
    green = (0,255,0)
    paper =  (255,150,100)
    blue = (0,0,255)
    lightblue = (240,248,255)




    def draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
    #--------------------------------------------------------------------------------

    def draw_bgBackscreen ():
        screen.blit(bg_backscreen,(0,0))

    # def draw_noteMap():
    #     screen.blit(note_map,(998,12))

    def draw_bg():
        screen.blit(bg_map,(210,40))

    def draw_bag():
        screen.blit(bag_of_coins,(0,0))
        draw_text(f'{button.wealth}', fontBag, (255,225,100), 120, 30)

    #------------------------------DrawingIndicators------------------------
    def draw_panel():
        screen.blit(panel,(-50,-35))
        # for count, i in enumerate(army_player):
        #       draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))
        # for count, i in enumerate(army_hostiles):
        #     draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (100,0,0), ((panel.get_width())*0.58), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))

    #-------------------------------------------------------------------------
    yvan_hp = int(linecache.getline('charstats.txt',1))
    yvan_armor = int(linecache.getline('charstats.txt',2))
    yvan_defene = int(linecache.getline('charstats.txt',3))
    yvan_attack = int(linecache.getline('charstats.txt',4))

    #----------------------------------Charaters------------------------------
    class Fighter():
        def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
            self.id=id
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_armor = max_armor
            self.armor = max_armor
            self.defence = defence
            self.start_defence = defence
            self.strength = strength
            self.start_strength = strength
            self.reach = reach
            self.special = special
            self.max_inventory = max_inventory
            self.inventory = max_inventory
            self.start_resistance = resistance
            self.resistance = resistance
            self.start_tricks = tricks
            self.tricks = tricks
            self.alive = True
            self.hostile = True
            self.animation_list = [] #list of lists (action/img)
            self.frame_index = 0
            self.action = 0 #0-idle / 1-attack / 2-hurt / 3-death  updates via self.animation_list = []
            self.update_time = pygame.time.get_ticks()  # how much time has passed

            #-----------------------------Animations--------------------------------------------
            #loading idle action images
            temp_list = []
            for i in range(2):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/idle/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            #loading attack action images
            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/attack/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/hurt/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/dead/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img

            #-----------------------------------------------------------------------------------
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]     # to control action/images
            # two lists (action/frames)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

        #---------------------------------------------------------------------
        def update(self,animation_modifier): #animation
            animation_cooldown = 100
            if self.action == 0:
                animation_cooldown = 1000*animation_modifier
            if self.action == 1:
                animation_cooldown = 150*animation_modifier
            if self.action == 2:
                animation_cooldown = 300*animation_modifier
            if self.action == 3:
                animation_cooldown = 250*animation_modifier

            #animation_cooldown = cooldown
            self.image = self.animation_list[self.action][self.frame_index]  #adding action
            if pygame.time.get_ticks() - self.update_time > animation_cooldown: #if its more than 100 its time to update the animation stage
                self.update_time = pygame.time.get_ticks() #resets timer
                self.frame_index += 1
            # if animation run out, reset
            if self.frame_index >= len(self.animation_list[self.action]):  #adding action

                #after death unit should stay at the last frame of the dead animation sequence
                if self.action == 3:    #dead animation in the list.
                    self.frame_index = len(self.animation_list[self.action])-1  #final frame
                else:
                    self.idle() # sets to idle animation

        #-----------------------------------Idle----------------------------
        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def hurt(self):
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def dead(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def reset(self):
            self.alive = True
            self.inventory = self.max_inventory
            self.hp = self.max_hp
            self.armor = self.max_armor
            self.defence = self.start_defence
            self.strength = self.start_strength
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Attack----------------------------
        def attack(self,target):
            rand = random.randint(-5,5)
            damage = self.strength + rand
            if self.special == 1:
                #target.armor -= 0
                target.hp -= damage
            elif self.special != 1:
                target.armor -= int(damage*(target.defence/100))
                if target.armor > 0:
                    target.hp -= int(damage*(1 - target.defence/100))
                if target.armor <= 0:
                    target.hp -= int((damage*(1 - target.defence/100)-target.armor))
                    target.armor = 0
            # runs hurn animation
            target.hurt()

            if target.hp < 1:
                target.hp = 0
                target.alive = False
                # runs death animation
                target.dead()

            #DamageText
            if self.special != 1:
                if target.armor > 1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage*(1 - target.defence/100))), red)
                if target.armor <=1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
            else:
                damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)

            damage_text_group.add(damage_text)
#---------------------------------AttackSounds---------------------------------------
            #attack sound # 0-standard blade; 1-arrow; 2-stone
            if self.special == 0:
                pygame.mixer.Sound(attack_sound).play()
            elif self.special == 1:
                pygame.mixer.Sound(arrow_sound).play()
            elif self.special == 2:
                pygame.mixer.Sound(stone_sound).play()
            elif self.special == 3:
                pygame.mixer.Sound(snarl_sound).play()
#------------------------------------------------------------------------------------


            #animations
            self.action = 1   # set action frames to as 1 as 1 = attack folder animation
            self.frame_index = 0 # frame 0 in the attack folder animation
            self.update_time = pygame.time.get_ticks()

        #----------------------------------------------------------------------
        def draw(self):
            screen.blit(self.image, self.rect)

    #-----------------------------------HealthBar--------------------------
    class healthBar ():
        def __init__(self, x,y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp
        def draw (self, hp):
            self.hp = hp
            # health ration
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen,red,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,green,(self.x, self.y, 50*ratio,5))

    #-----------------------------------ArmorBar--------------------------
    class armorBar ():
        def __init__(self, x,y, armor, max_armor):
            self.x = x
            self.y = y
            self.armor = armor
            self.max_armor = max_armor
        def draw (self, armor):
            self.armor = armor
            # health ration
            ratio = self.armor / self.max_armor
            pygame.draw.rect(screen,lightblue,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,blue,(self.x, self.y, 50*ratio,5))

    #-----------------------------------AttributeChangeBar-----------------
    class DamageText(pygame.sprite.Sprite):   # sprite is updated automatically
        def __init__(self,x,y,damage, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = fontDMG.render(damage, True, color)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.counter = 0

        def update(self):
            #move text
            self.rect.y -=1
            #delete after timer
            self.counter +=1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()    #python list
    #def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
    #-----------------------------------PlayerArmy--------------------------
    # militia = Fighter (435,295, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia_healthbar = healthBar (militia.rect.centerx-25,militia.rect.centery-55,militia.hp, militia.max_hp)
    # militia_armorbar = armorBar (militia.rect.centerx-25,militia.rect.centery-50,militia.armor, militia.max_armor)
    #-----------------------------------------------------------------------
    boy = Fighter (435,305, 'boy',120,60,35,40,1,3,0,True,False,0,0)
    boy_healthbar = healthBar (boy.rect.centerx-25,boy.rect.centery-55,boy.hp, boy.max_hp)
    boy_armorbar = armorBar (boy.rect.centerx-25,boy.rect.centery-50,boy.armor, boy.max_armor)
    #-----------------------------------------------------------------------
    landsknecht = Fighter (530,250,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht_healthbar = healthBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-55,landsknecht.hp, landsknecht.max_hp)
    landsknecht_armorbar = armorBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-50,landsknecht.armor, landsknecht.max_armor)
    #-----------------------------------------------------------------------
    landsknecht1 = Fighter (620,205,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht1_healthbar = healthBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-55,landsknecht1.hp, landsknecht1.max_hp)
    landsknecht1_armorbar = armorBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-50,landsknecht1.armor, landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    chevalier = Fighter (720,135,'chevalier',120,100,65,70,1,0,1,True,False,0,0)
    chevalier_healthbar = healthBar (chevalier.rect.centerx-25,chevalier.rect.centery-65,chevalier.hp, chevalier.max_hp)
    chevalier_armorbar = armorBar (chevalier.rect.centerx-25,chevalier.rect.centery-60,chevalier.armor, chevalier.max_armor)
    #-----------------------------------------------------------------------
    # militia1 = Fighter (700,165, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia1_healthbar = healthBar (militia1.rect.centerx-25,militia1.rect.centery-55,militia1.hp, militia1.max_hp)
    # militia1_armorbar = armorBar (militia1.rect.centerx-25,militia1.rect.centery-50,militia1.armor, militia1.max_armor)
    # #-----------------------------------------------------------------------
    # militia2 = Fighter (790,115, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia2_healthbar = healthBar (militia2.rect.centerx-25,militia2.rect.centery-55,militia2.hp, militia2.max_hp)
    # militia2_armorbar = armorBar (militia2.rect.centerx-25,militia2.rect.centery-50,militia2.armor, militia2.max_armor)
    # #-----------------------------------------------------------------------
    archer = Fighter (530,115, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer_healthbar = healthBar (archer.rect.centerx-25,archer.rect.top-20,archer.hp, archer.max_hp)
    archer_armorbar = armorBar (archer.rect.centerx-25,archer.rect.top-15,archer.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    archer1 = Fighter (440,160, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer1_healthbar = healthBar (archer1.rect.centerx-25,archer1.rect.top-20,archer1.hp, archer.max_hp)
    archer1_armorbar = armorBar (archer1.rect.centerx-25,archer1.rect.top-15,archer1.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    yvan = Fighter (350,210, 'yvan',yvan_hp,yvan_armor,yvan_defene,yvan_attack,2,2,0,True,False,0,0)
    yvan_healthbar = healthBar (yvan.rect.centerx-25,yvan.rect.top-20,yvan.hp, yvan.max_hp)
    yvan_armorbar = armorBar (yvan.rect.centerx-25,yvan.rect.top-15,yvan.armor, yvan.max_armor)
    #max_hp,max_armor, defence, strength,



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_player = []
    #army_player.append(militia)
    army_player.append(boy)
    army_player.append(landsknecht)
    army_player.append(landsknecht1)
    army_player.append(chevalier)
    #army_player.append(militia1)
    #army_player.append(militia2)
    army_player.append(archer)
    army_player.append(archer1)
    army_player.append(yvan)

    army_player_front = army_player[:4]

    #-----------------------------HostileArmy-------------------------------
    # h_militia = Fighter(570,365,'militia',60,30,35,30,1,0,1,True,True,0,0)
    # h_militia_healthbar = healthBar(h_militia.rect.centerx-25,h_militia.rect.centery-55,h_militia.hp, h_militia.max_hp)
    # h_militia_armorbar = armorBar(h_militia.rect.centerx-25,h_militia.rect.centery-50,h_militia.armor, h_militia.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand = Fighter(570,365,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand_healthbar = healthBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-55,h_brigand.hp, h_brigand.max_hp)
    # h_brigand_armorbar = armorBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-50,h_brigand.armor, h_brigand.max_armor)
    #-----------------------------------------------------------------------
    h_wolf = Fighter(570,370,'wolf',80,1,0,40,1,3,0,True,True,0,0)
    h_wolf_healthbar = healthBar(h_wolf.rect.centerx-25,h_wolf.rect.centery-55,h_wolf.hp, h_wolf.max_hp)
    h_wolf_armorbar = armorBar(h_wolf.rect.centerx-25,h_wolf.rect.centery-50,h_wolf.armor, h_wolf.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand1 = Fighter(660,325,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand1_healthbar = healthBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-55,h_brigand1.hp, h_brigand1.max_hp)
    # h_brigand1_armorbar = armorBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-50,h_brigand1.armor, h_brigand1.max_armor)
    # #-----------------------------------------------------------------------
    h_wolf1 = Fighter(660,330,'wolf',80,1,0,40,1,3,0,True,True,0,0)
    h_wolf1_healthbar = healthBar(h_wolf1.rect.centerx-25,h_wolf1.rect.centery-55,h_wolf1.hp, h_wolf1.max_hp)
    h_wolf1_armorbar = armorBar(h_wolf1.rect.centerx-25,h_wolf1.rect.centery-50,h_wolf1.armor, h_wolf1.max_armor)
    #-----------------------------------------------------------------------
    # h_landsknecht = Fighter (750,280,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht_healthbar = healthBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-55,h_landsknecht.hp, h_landsknecht.max_hp)
    # h_landsknecht_armorbar = armorBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-50,h_landsknecht.armor, h_landsknecht.max_armor)
    #-----------------------------------------------------------------------
    h_wolf2 = Fighter(750,290,'wolf',80,1,0,40,1,3,0,True,True,0,0)
    h_wolf2_healthbar = healthBar(h_wolf2.rect.centerx-25,h_wolf2.rect.centery-55,h_wolf2.hp, h_wolf2.max_hp)
    h_wolf2_armorbar = armorBar(h_wolf2.rect.centerx-25,h_wolf2.rect.centery-50,h_wolf2.armor, h_wolf2.max_armor)
    #-----------------------------------------------------------------------
    # h_landsknecht1 = Fighter (840,235,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht1_healthbar = healthBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-55,h_landsknecht1.hp, h_landsknecht1.max_hp)
    # h_landsknecht1_armorbar = armorBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-50,h_landsknecht1.armor, h_landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    h_blackwolf = Fighter(840,245,'blackwolf',120,1,0,60,1,3,0,True,True,0,0)
    h_blackwolf_healthbar = healthBar(h_blackwolf.rect.centerx-25,h_blackwolf.rect.centery-55,h_blackwolf.hp, h_blackwolf.max_hp)
    h_blackwolf_armorbar = armorBar(h_blackwolf.rect.centerx-25,h_blackwolf.rect.centery-50,h_blackwolf.armor, h_blackwolf.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand2 = Fighter(940,195,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand2_healthbar = healthBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-55,h_brigand2.hp, h_brigand2.max_hp)
    # h_brigand2_armorbar = armorBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-50,h_brigand2.armor, h_brigand2.max_armor)
    # #-----------------------------------------------------------------------
    h_blackwolf1 = Fighter(935,200,'blackwolf',120,1,0,60,1,3,0,True,True,0,0)
    h_blackwolf1_healthbar = healthBar(h_blackwolf1.rect.centerx-25,h_blackwolf1.rect.centery-55,h_blackwolf1.hp, h_blackwolf1.max_hp)
    h_blackwolf1_armorbar = armorBar(h_blackwolf1.rect.centerx-25,h_blackwolf1.rect.centery-50,h_blackwolf1.armor, h_blackwolf1.max_armor)
    #-----------------------------------------------------------------------
    # h_landsknecht2 = Fighter (790,340,'landsknecht',90,55,40,50,2,0,1,True,True,0,0)
    # h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    # h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    #-----------------------------------------------------------------------
    # h_bowman = Fighter (790,350, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman_healthbar = healthBar (h_bowman.rect.centerx-25,h_bowman.rect.top-20,h_bowman.hp, h_bowman.max_hp)
    # h_bowman_armorbar = armorBar (h_bowman.rect.centerx-25,h_bowman.rect.top-15,h_bowman.armor, h_bowman.max_armor)
    # #-----------------------------------------------------------------------
    h_blackwolf2 = Fighter(790,350,'blackwolf',120,1,0,60,1,3,0,True,True,0,0)
    h_blackwolf2_healthbar = healthBar(h_blackwolf2.rect.centerx-25,h_blackwolf2.rect.centery-55,h_blackwolf2.hp, h_blackwolf2.max_hp)
    h_blackwolf2_armorbar = armorBar(h_blackwolf2.rect.centerx-25,h_blackwolf2.rect.centery-50,h_blackwolf2.armor, h_blackwolf2.max_armor)
    #-----------------------------------------------------------------------
    h_blackwolf3 = Fighter(695,405,'blackwolf',120,1,0,60,1,3,0,True,True,0,0)
    h_blackwolf3_healthbar = healthBar(h_blackwolf3.rect.centerx-25,h_blackwolf3.rect.centery-55,h_blackwolf3.hp, h_blackwolf3.max_hp)
    h_blackwolf3_armorbar = armorBar(h_blackwolf3.rect.centerx-25,h_blackwolf3.rect.centery-50,h_blackwolf3.armor, h_blackwolf3.max_armor)
    #-----------------------------------------------------------------------
#-----------------------------------------------------------------------
    # h_bowman1 = Fighter (695,400, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman1_healthbar = healthBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-20,h_bowman1.hp, h_bowman1.max_hp)
    # h_bowman1_armorbar = armorBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-15,h_bowman1.armor, h_bowman1.max_armor)
    # #-----------------------------------------------------------------------
    h_wolf3 = Fighter(880,310,'wolf',80,1,0,40,1,3,0,True,True,0,0)
    h_wolf3_healthbar = healthBar(h_wolf3.rect.centerx-25,h_wolf3.rect.centery-55,h_wolf3.hp, h_wolf3.max_hp)
    h_wolf3_armorbar = armorBar(h_wolf3.rect.centerx-25,h_wolf3.rect.centery-50,h_wolf3.armor, h_wolf3.max_armor)
    #-----------------------------------------------------------------------
    # h_bowman2 = Fighter (880,310, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman2_healthbar = healthBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-20,h_bowman2.hp, h_bowman2.max_hp)
    # h_bowman2_armorbar = armorBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-15,h_bowman2.armor, h_bowman2.max_armor)
    # #-----------------------------------------------------------------------
    # h_bowman3 = Fighter (960,260, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman3_healthbar = healthBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-20,h_bowman3.hp, h_bowman3.max_hp)
    # h_bowman3_armorbar = armorBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-15,h_bowman3.armor, h_bowman3.max_armor)
    # # #-----------------------------------------------------------------------
    h_wolf4 = Fighter(960,270,'wolf',80,1,0,40,1,3,0,True,True,0,0)
    h_wolf4_healthbar = healthBar(h_wolf4.rect.centerx-25,h_wolf4.rect.centery-55,h_wolf4.hp, h_wolf4.max_hp)
    h_wolf4_armorbar = armorBar(h_wolf4.rect.centerx-25,h_wolf4.rect.centery-50,h_wolf4.armor, h_wolf4.max_armor)



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_hostiles = []
    army_hostiles.append(h_wolf)
    army_hostiles.append(h_wolf1)
    army_hostiles.append(h_wolf2)
    army_hostiles.append(h_blackwolf)
    army_hostiles.append(h_blackwolf1)
    army_hostiles.append(h_blackwolf2)
    army_hostiles.append(h_blackwolf3)
    army_hostiles.append(h_wolf3)
    army_hostiles.append(h_wolf4)

    army_hostiles_front = army_hostiles


#------------------------------TotalUnitNumber----------------------------
    total_hostiles = len(army_hostiles)
    total_allies = len(army_player)
    total_fighters = total_hostiles + total_allies

#------------------------------ItemsUse(Button)---------------------------
    #inventory_button = button.Button(screen,WINDOW_SIZE[0]*0 + 110, WINDOW_SIZE[1]*0 - 6,inventory_bag,280,120,0, True, 'Inventory')

    inventory_button = button.ToggleButton(screen,-65, 425,inventory_bag,260,120,0, True, 'Inventory')
    #------------------------------ItemsUse(PotionButton)-------------------
    potion_button = button.Button(screen, WINDOW_SIZE[0]*0.01, WINDOW_SIZE[1]*0.90, health_potion, 48,72,30, False,f'Health Potion. Restores {health_potion_restores} HP')
    potion_button1 = button.Button(screen, WINDOW_SIZE[0]*0.06, WINDOW_SIZE[1]*0.90, defence_potion, 48,72,40, False,f'Defence Potion. Gives {defence_potion_adds} DEF/ARM')
    potion_button2 = button.Button(screen, WINDOW_SIZE[0]*0.11, WINDOW_SIZE[1]*0.90, berserk_potion, 48,72,60, False,f'Berserk Potion. Gives {berserk_potion_adds} ATK / Removes {int(berserk_potion_adds*1)} DEF')


    #------------------------------IconToggle(Reset)------------------------
    restart_button = button.Button(screen, 1100, 8, retry_icon, 84,90,25, True,'Try Again')
    skip_turn_button = button.Button(screen, WINDOW_SIZE[0]*0.92, WINDOW_SIZE[1]*0.62, skip_turn_img, 86,82,60, False,f'Skip Turn')
    victory_button = button.Button(screen, 1170, 15, victory_icon, 86,90,25, True,'Back to Map')
    leave_button = button.Button(screen, 1190, 0, doors_icon, 64,90,25, True,'Leave Battlefield')


#-----------------------------------------------------------------------

    while dire_wolves_battle_running:
        #display.fill((146,244,255))
        draw_bgBackscreen()
        #draw_noteMap()  # location map
        draw_bg()
        draw_panel()
        draw_bag()

        #-----------------------------DrawingUnits/AnimatioSpeedMod------------
        for units in army_player:
            # militia.update(0.9)
            # militia.draw()
            #------------
            landsknecht.update(1)
            landsknecht.draw()
            #------------
            chevalier.update(1.3)
            chevalier.draw()
            #------------
            # militia1.update(0.88)
            # militia1.draw()
            #------------
            boy.update(0.88)
            boy.draw()
            #------------
            landsknecht1.update(1.1)
            landsknecht1.draw()
            #------------
            # militia2.update(0.84)
            # militia2.draw()
            #------------
            archer.update(0.95)
            archer.draw()
            #------------
            archer1.update(0.92)
            archer1.draw()
            #------------
            yvan.update(1.05)
            yvan.draw()

        for hostile in army_hostiles:
            h_wolf.update(0.94)
            h_wolf.draw()
            #------------
            h_wolf1.update(0.92)
            h_wolf1.draw()
            #------------
            h_wolf2.update(0.98)
            h_wolf2.draw()
            #------------
            h_wolf3.update(1.1)
            h_wolf3.draw()
            #------------
            h_wolf4.update(1)
            h_wolf4.draw()
            #------------
            h_blackwolf.update(0.89)
            h_blackwolf.draw()
            #------------
            h_blackwolf1.update(0.92)
            h_blackwolf1.draw()
            #------------
            h_blackwolf2.update(0.86)
            h_blackwolf2.draw()
            #------------
            h_blackwolf3.update(1)
            h_blackwolf3.draw()
            #------------
            # h_brigand.update(0.9)
            # h_brigand.draw()
            # #------------
            # h_brigand2.update(0.85)
            # h_brigand2.draw()
            # #------------
            # h_landsknecht.update(0.95)
            # h_landsknecht.draw()
            # #------------
            # h_landsknecht1.update(0.98)
            # h_landsknecht1.draw()
            # #------------
            # h_brigand1.update(0.9)
            # h_brigand1.draw()
            # #------------
            # h_bowman.update(0.89)
            # h_bowman.draw()
            # #------------
            # h_bowman1.update(0.85)
            # h_bowman1.draw()
            # #------------
            # h_bowman2.update(0.92)
            # h_bowman2.draw()
            # #------------
            # h_bowman3.update(0.90)
            # h_bowman3.draw()
        #-----------------------------HealthBar/ArmorBar-----------------------
        #-------------Player------------------------
        if show_indicators == True:
            if chevalier.alive == True:
                chevalier_healthbar.draw(chevalier.hp)
                chevalier_armorbar.draw(chevalier.armor)
            # if militia.alive == True:
            #     militia_healthbar.draw(militia.hp)
            #     militia_armorbar.draw(militia.armor)
            if boy.alive == True:
                boy_healthbar.draw(boy.hp)
                boy_armorbar.draw(boy.armor)
            if landsknecht.alive == True:
                landsknecht_healthbar.draw(landsknecht.hp)
                landsknecht_armorbar.draw(landsknecht.armor)
            # if militia1.alive == True:
            #     militia1_healthbar.draw(militia1.hp)
            #     militia1_armorbar.draw(militia1.armor)
            if landsknecht1.alive == True:
                landsknecht1_healthbar.draw(landsknecht1.hp)
                landsknecht1_armorbar.draw(landsknecht1.armor)
            # if militia2.alive == True:
            #     militia2_healthbar.draw(militia2.hp)
            #     militia2_armorbar.draw(militia2.armor)
            if archer.alive == True:
                archer_healthbar.draw(archer.hp)
                archer_armorbar.draw(archer.armor)
            if archer1.alive == True:
                archer1_healthbar.draw(archer1.hp)
                archer1_armorbar.draw(archer1.armor)
            if yvan.alive == True:
                yvan_healthbar.draw(yvan.hp)
                yvan_armorbar.draw(yvan.armor)

            #------------------Enemy--------------------
            if h_wolf.alive == True:
                h_wolf_healthbar.draw(h_wolf.hp)
                h_wolf_armorbar.draw(h_wolf.armor)
            if h_wolf1.alive == True:
                h_wolf1_healthbar.draw(h_wolf1.hp)
                h_wolf1_armorbar.draw(h_wolf1.armor)
            if h_wolf2.alive == True:
                h_wolf2_healthbar.draw(h_wolf2.hp)
                h_wolf2_armorbar.draw(h_wolf2.armor)
            if h_wolf3.alive == True:
                h_wolf3_healthbar.draw(h_wolf3.hp)
                h_wolf3_armorbar.draw(h_wolf3.armor)
            if h_wolf4.alive == True:
                h_wolf4_healthbar.draw(h_wolf4.hp)
                h_wolf4_armorbar.draw(h_wolf4.armor)
            if h_blackwolf.alive == True:
                h_blackwolf_healthbar.draw(h_blackwolf.hp)
                h_blackwolf_armorbar.draw(h_blackwolf.armor)
            if h_blackwolf1.alive == True:
                h_blackwolf1_healthbar.draw(h_blackwolf1.hp)
                h_blackwolf1_armorbar.draw(h_blackwolf1.armor)
            if h_blackwolf2.alive == True:
                h_blackwolf2_healthbar.draw(h_blackwolf2.hp)
                h_blackwolf2_armorbar.draw(h_blackwolf2.armor)
            if h_blackwolf3.alive == True:
                h_blackwolf3_healthbar.draw(h_blackwolf3.hp)
                h_blackwolf3_armorbar.draw(h_blackwolf3.armor)
        #----------------------------------------------------------------------

        #-----------------------------DamageText-----------------------------
        damage_text_group.update()
        damage_text_group.draw(screen)
        #methods update and draw are parts of the sprite.

        #-----------------------------Items/SkipTurn/Inventory-----------------------------
        pos = pygame.mouse.get_pos()
        if skip_turn_button.rect.collidepoint(pos):
            draw_text(f'{skip_turn_button.description}', fontDMG, green, skip_turn_button.rect.x-30,skip_turn_button.rect.y+100)
        if skip_turn_button.draw():
            skip_turn=True
        if battle_status != 2 and leave_button.available == True:
            if leave_button.rect.collidepoint(pos):
                draw_text(f'{leave_button.description}', fontDMG, green, leave_button.rect.x-140,leave_button.rect.y+100)
            if leave_button.draw():
                play_music('Map')
                button.wealth = button.start_wealth
                dire_wolves_battle_running = False


        if inventory_button.rect.collidepoint(pos):
            draw_text(f'{inventory_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)
        if inventory_button.toggled == True and battle_status ==0:
            potion_button.available = True
            potion_button1.available = True
            potion_button2.available = True


            #---------------------HealthPotion--------------------------------------
            if potion_button.available == True:
                if potion_button.draw():
                    use_health_potion = True
                draw_text(f'{potion_button.price}', fontBag, (255,225,100), potion_button.rect.x+5, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button.rect.collidepoint(pos):
                    draw_text(f'{potion_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

            #-------DefencePotion--------------
            if potion_button1.available == True:
                if potion_button1.draw():
                    use_defence_potion = True
                draw_text(f'{potion_button1.price}', fontBag, (255,225,100), potion_button.rect.x+65, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button1.rect.collidepoint(pos):
                    draw_text(f'{potion_button1.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

                #-------BerserkPotion--------------
            if potion_button2.available == True:
                if potion_button2.draw():
                    use_berserk_potion = True
                draw_text(f'{potion_button2.price}', fontBag, (255,225,100), potion_button.rect.x+130, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button2.rect.collidepoint(pos):
                    draw_text(f'{potion_button2.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)


        #---------------------InventoryStock--------------------------------------
        else:
            potion_button.available = False

        #--------------------------------------------------------------------------
        if battle_status ==0:   #win/loose check


            #-----------------------------PlayerAttacking---------------------------
            for count, ally in enumerate(army_player):
                if current_fighter == 1+count:
                    draw_text('^', fontActive, "#FFA500", ally.rect.centerx-20,ally.rect.y -65)
                    if ally.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:

                            if ally.reach == 2:
                                if engage == True and target != None:
                                    # conditioned upon engage below & def attack above
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif ally.reach == 1:
                                if engage == True and target != None and target.reach == 1:
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            for enemy in army_hostiles_front:
                                if all(enemy.alive == False for enemy in army_hostiles_front):
                                        #enemy.alive == False:
                                    if ally.reach == 1:
                                     if engage == True and target != None and target.reach == 2:
                                        ally.reach = 2
                                        ally.attack(target)
                                        current_fighter += 1
                                        action_cooldown = 0


#-----------------------------------------SkipTurn-----------------------------------------
                            if skip_turn == True:
                                current_fighter += 1
                                action_cooldown = 0
                                skip_turn_heal = 10
                                if ally.max_hp - ally.hp > skip_turn_heal:    #50
                                    skip_turn_heal = skip_turn_heal
                                else:
                                    skip_turn_heal = ally.max_hp - ally.hp
                                ally.hp += skip_turn_heal
                                #DamageText
                                damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(skip_turn_heal), green)
                                damage_text_group.add(damage_text)
                            skip_turn = False

                            #------------UsingItem(HealthPotion)---------------------------
                            if use_health_potion == True and button.wealth >= potion_button.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_hp - ally.hp > health_potion_restores:    #50
                                        heal_amount = health_potion_restores
                                    else:
                                        heal_amount = ally.max_hp - ally.hp
                                    ally.hp += heal_amount
                                    ally.inventory -= 1
                                    button.wealth -= potion_button.price
                                    #DamageText
                                    damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(heal_amount), green)
                                    damage_text_group.add(damage_text)

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_health_potion = False

                            #----------------------------------------------------
                            #------------UsingItem(DefencePotion)---------------
                            if use_defence_potion == True and button.wealth >= potion_button1.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_armor - ally.armor > defence_potion_adds:    #50
                                        add_defence_amount = defence_potion_adds
                                    else:
                                        add_defence_amount = ally.max_armor - ally.armor
                                    ally.armor += add_defence_amount
                                    ally.defence = 100
                                    ally.inventory -= 1
                                    button.wealth -= potion_button1.price     #Change price

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_defence_potion = False


                            #------------UsingItem(BerserkPotion)---------------
                            if use_berserk_potion == True and button.wealth >= potion_button2.price:
                                if ally.inventory > 0:
                                    ally.strength += berserk_potion_adds
                                    if ally.defence < int(berserk_potion_adds):
                                        ally.defence = 0
                                    else:
                                        ally.defence -= int(berserk_potion_adds)
                                    ally.inventory -= 1
                                    button.wealth -= potion_button2.price

                                    current_fighter +=1
                                    action_cooldown = 0
                                    #Change price
                                use_berserk_potion = False

                    else:
                        current_fighter +=1   #if dead = skip turn

            #-----------------------------EnemyAttacking----------------------------
            for count, enemy in enumerate(army_hostiles):
                if current_fighter == 1+ total_allies + count:   # "3 + count" - checks with the max_fighter var and number of units in army_player
                    draw_text('^', fontActive, "#FFA500", enemy.rect.centerx-20,enemy.rect.y -65)
                    if enemy.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:
                            #health_check
                            if (enemy.hp / enemy.max_hp) <0.5 and enemy.inventory >0:
                                if enemy.max_hp - enemy.hp > health_potion_restores:
                                    heal_amount = health_potion_restores
                                else:
                                    heal_amount = enemy.max_hp - enemy.hp

                                enemy.hp += heal_amount
                                enemy.inventory -= 1

                                #DamageText
                                damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(heal_amount), green)
                                damage_text_group.add(damage_text)

                                current_fighter +=1
                                action_cooldown = 0

                            elif enemy.reach == 2:
                                if enemy.strength >= ally.hp and ally.alive == True:
                                   enemy.attack(ally)
                                   current_fighter += 1
                                   action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif enemy.reach == 1:
                                if all(ally.alive == True for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                elif all(ally.alive == False for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 2]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                            #else:
                            #     enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                            #     # enemy.hp += 10
                            #     current_fighter += 1
                            #     action_cooldown = 0
                            #     # damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(10), green)
                            #     # damage_text_group.add(damage_text)

                    else:
                        current_fighter +=1

            #---------------------------------Turns----------------------------
            # if all have had a turn, reset
            if current_fighter > total_fighters:
                current_fighter = 1

        #-----------------------------DefeatStatus-------------------------
        # checking alive/dead status
        alive_allies = 0
        for ally in army_player:
            if ally.alive == True:
                alive_allies +=1
        if alive_allies ==0:
            battle_status =1

        #---------------------------------VictoryStatus--------------------
        alive_enemies = 0
        for enemy in army_hostiles:
            if enemy.alive == True:
                alive_enemies +=1
        if alive_enemies ==0:
            battle_status =2

        #-------------------Defeat/VictoryStatusDisplay-------------------
        if battle_status !=0:
            if battle_status ==1:
                draw_text(f'Defeat!', fontMenuLarge, (155,0,0), screen.get_width()*0.46,0)
#-------------------ResetButton-----------------------------------
                if restart_button.available == True:
                    if restart_button.draw():
                        play_music('Battle')
                        for ally in army_player:
                            ally.reset()
                        for enemy in army_hostiles:
                            enemy.reset()
                        button.wealth = button.start_wealth         #restart gold here
                        current_fighter = 1
                        action_cooldown = 0
                        battle_status = 0

                        pos = pygame.mouse.get_pos() # text over the button
                    if restart_button.rect.collidepoint(pos):
                        draw_text(f'{restart_button.description}', fontDMG, green, restart_button.rect.x+30,leave_button.rect.y+100)

            #-------------------Defeat/VictoryStatusDisplay-------------------
            if battle_status ==2:
                button.quest_dire_wolves= 'locked'
                draw_text(f'Victory!', fontMenuLarge, green, screen.get_width()*0.46,0)
                if play_victory_music == True:
                      play_music('BattleVictory')
                play_victory_music = False
                if victory_button.available == True:
                    if victory_button.draw():
                        button.wealth += 150
                        button.start_wealth = button.wealth
                        button.quest_highwaymen = 'unlocked'
                        print(button.start_wealth)
                        print(button.wealth)
                        play_music('Map')
                        dire_wolves_battle_running = False
                    if victory_button.rect.collidepoint(pos):
                        draw_text(f'{victory_button.description}', fontDMG, green, victory_button.rect.x-75,leave_button.rect.y+100)
        #------------------------------End/Controls------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)


            if event.type == KEYDOWN:
                if event.key == K_f and show_indicators == True:
                        show_indicators = False
                elif event.key == K_f and show_indicators == False:
                        show_indicators = True

                if event.key == K_o:
                    # fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen

                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

            inventory_button.event_handler(event) #ToggleButton

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        if leave_button.clicked == True or victory_button.clicked == True:
            mouse_map_position_align(750,400)
        #-----------------------------Action/TargetSearch-------------------
        engage = False
        target = None

        inventory_button.draw(screen) #ToggleButton

        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        screen.blit(normal_icon,pos)

        for count, ally in enumerate(army_player):
            if ally.rect.collidepoint(pos) and ally.alive == True:
                draw_text(f'{ally.id} | HP: {ally.hp} | ARM: {ally.armor} | ATK: {ally.strength} | DEF: {ally.defence} | INV: {ally.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))
        for count, enemy in enumerate(army_hostiles):
            if enemy.rect.collidepoint(pos) and enemy.alive == True:
                pygame.mouse.set_visible(False)
                screen.blit(attack_icon,pos)
                draw_text(f'{enemy.id} | HP: {enemy.hp} | ARM: {enemy.armor} | ATK: {enemy.strength} | DEF: {enemy.defence} | INV: {enemy.inventory}', font, (100,0,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))

                # show attack icon
                #--------------chooseTarget&Attack-------------------------
                if clicked == True and enemy.alive == True:
                    engage = True
                    target = army_hostiles[count]


        #-----------------------------------------------------------------------
        #surf = pygame.transform.scale(display, WINDOW_SIZE)
        #screen.blit(surf, (0,0))

        pygame.display.update()
        clock.tick(60)


























































































































def highwaymen_battle ():
    highwaymen_battle_running = True

    clock = pygame.time.Clock()
    pygame.init()

    pygame.mixer.set_num_channels(32)
    pygame.mixer.pre_init(44100,-16,2,512)
    #-----------------------------GameWindowSettings----------------------
    pygame.display.set_caption("Highwaymen")
    WINDOW_SIZE = (1280,720)
    screen = pygame.display.set_mode((1280,720),0,32)
    #display = pygame.Surface((600,400))


    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    fullscreen = button.fullscreen
    #not bool(linecache.getline('resolution.txt',1))
    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)


    #-----------------------------------Battlemap,Interface------------------------
    bg_backscreen = pygame.image.load("BattleScreen/background.png").convert_alpha()
    bg_backscreen = pygame.transform.scale(bg_backscreen, (int(WINDOW_SIZE[0]*1.00),(int(WINDOW_SIZE[1]*0.75))))

    note_map = pygame.image.load("BattleScreen/note_Faroak0.png").convert_alpha()
    note_map = pygame.transform.scale(note_map, (int(WINDOW_SIZE[0]*0.21),(int(WINDOW_SIZE[1]*0.28))))

    bg_map = pygame.image.load("BattleScreen/BattleMap0.png").convert_alpha()
    bg_map = pygame.transform.scale(bg_map, (int(WINDOW_SIZE[0]*0.70),(int(WINDOW_SIZE[1]*0.70))))

    panel = pygame.image.load("BattleScreen/gamepanel0.png").convert_alpha()
    panel = pygame.transform.scale(panel, (int(WINDOW_SIZE[0]*1.10),(int(WINDOW_SIZE[1]*1.40))))

    bag_of_coins = pygame.image.load("BattleScreen/bag.png").convert_alpha()
    bag_of_coins = pygame.transform.scale(bag_of_coins, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    #-----------------------------------Icons-------------------------------------
    attack_icon = pygame.image.load("BattleScreen/icon_fight.png").convert_alpha()
    attack_icon = pygame.transform.scale(attack_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))

    normal_icon = pygame.image.load("BattleScreen/cursor_final.png").convert_alpha()
    normal_icon = pygame.transform.scale(normal_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))


    skip_turn_img = pygame.image.load("BattleScreen/skip_turn.png").convert_alpha()
    skip_turn_img = pygame.transform.scale(skip_turn_img, (int(WINDOW_SIZE[0]*0.06),(int(WINDOW_SIZE[1]*0.05))))

    #-----------------------------------Characters---------------------------------
    # militia_image = pygame.image.load("BattleScreen/militia/idle/0.png").convert_alpha()
    # landsknecht_image = pygame.image.load("BattleScreen/landsknecht/idle/0.png").convert_alpha()

    #------------------------------------------------------------------------------
    #--------------------------------Items----------------------------------------
    inventory_bag = pygame.image.load("BattleScreen/items/inventorybag.png").convert_alpha()
    inventory_bag = pygame.transform.scale(inventory_bag, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    health_potion = pygame.image.load("BattleScreen/items/health_potion.png").convert_alpha()
    health_potion = pygame.transform.scale(health_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    defence_potion = pygame.image.load("BattleScreen/items/reflexes_potion.png").convert_alpha()
    defence_potion = pygame.transform.scale(defence_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    berserk_potion = pygame.image.load("BattleScreen/items/berserk_potion.png").convert_alpha()
    berserk_potion = pygame.transform.scale(berserk_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))


    doors_icon = pygame.image.load("BattleScreen/items/castledoors.png").convert_alpha()
    doors_icon = pygame.transform.scale(doors_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    retry_icon = pygame.image.load("BattleScreen/items/try again.png").convert_alpha()
    retry_icon = pygame.transform.scale(retry_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    victory_icon = pygame.image.load("BattleScreen/items/victory.png").convert_alpha()
    victory_icon = pygame.transform.scale(victory_icon, (int(WINDOW_SIZE[0]*0.15),(int(WINDOW_SIZE[1]*0.15))))

    #------------------------------------------------------------------------------
    screen.fill((242,238,203))

    mouse_position = (0, 0)
    #----------------------------------Music----------------------------------------
    #open_inventory_bag = pygame.mixer.Sound('sounds/OpenInventory.mp3')

    play_music('Battle')

    #------------------------   -------------------------------------------------------
    attack_sound = pygame.mixer.Sound('BattleScreen/items/attack sound.wav')
    arrow_sound = pygame.mixer.Sound('BattleScreen/items/arrow.wav')
    snarl_sound = pygame.mixer.Sound('BattleScreen/items/snarl.wav')
    stone_sound = pygame.mixer.Sound('BattleScreen/items/throwingstone.wav')
    #------------------------------------ActionOrder--------------------------------
    current_fighter = 1

    action_cooldown = 0
    action_waittime = 100
    draw_cursor = False
    battle_status = 0    #0 - nothing, 1 = lost, 2 = won

    # if battle_status ==0:
    #     play_music('Battle')
    # if battle_status ==2:
    #     pygame.mixer.music.play(0)
    #     play_music('BattleVictory')
    play_victory_music = True
    if battle_status ==1:
        play_music('BattleDefeat')

    #------------------------------------BattleInterface (line 315)-------------------
    engage = False
    clicked = False
    skip_turn = False
    #total_fighters = 11
    show_indicators = True

    use_health_potion = False
    health_potion_restores = 50

    use_defence_potion = False
    defence_potion_adds = 100

    use_berserk_potion = False
    berserk_potion_adds = 30


    #----------------------------------ShowStats------------------------------------
    font =pygame.font.SysFont('Times New Roman', 18)
    fontBag = pygame.font.Font('WorldMap/ESKARGOT.ttf', 38)
    fontDMG = pygame.font.Font('WorldMap/ESKARGOT.ttf', 26)
    fontActive = pygame.font.Font('WorldMap/ESKARGOT.ttf', 80)
    fontBattle = pygame.font.SysFont('Times New Roman', 70)
    #pygame.font.Font('WorldMap/ESKARGOT.ttf', 70)


    red = (230,16,35)
    ginger = (245,116,34)
    green = (0,255,0)
    paper =  (255,150,100)
    blue = (0,0,255)
    lightblue = (240,248,255)




    def draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
    #--------------------------------------------------------------------------------

    def draw_bgBackscreen ():
        screen.blit(bg_backscreen,(0,0))

    # def draw_noteMap():
    #     screen.blit(note_map,(998,12))

    def draw_bg():
        screen.blit(bg_map,(210,40))

    def draw_bag():
        screen.blit(bag_of_coins,(0,0))
        draw_text(f'{button.wealth}', fontBag, (255,225,100), 120, 30)

    #------------------------------DrawingIndicators------------------------
    def draw_panel():
        screen.blit(panel,(-50,-35))
        # for count, i in enumerate(army_player):
        #       draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))
        # for count, i in enumerate(army_hostiles):
        #     draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (100,0,0), ((panel.get_width())*0.58), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))

    #-------------------------------------------------------------------------
    yvan_hp = int(linecache.getline('charstats.txt',1))
    yvan_armor = int(linecache.getline('charstats.txt',2))
    yvan_defene = int(linecache.getline('charstats.txt',3))
    yvan_attack = int(linecache.getline('charstats.txt',4))

    #----------------------------------Charaters------------------------------
    class Fighter():
        def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
            self.id=id
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_armor = max_armor
            self.armor = max_armor
            self.defence = defence
            self.start_defence = defence
            self.strength = strength
            self.start_strength = strength
            self.reach = reach
            self.special = special
            self.max_inventory = max_inventory
            self.inventory = max_inventory
            self.start_resistance = resistance
            self.resistance = resistance
            self.start_tricks = tricks
            self.tricks = tricks
            self.alive = True
            self.hostile = True
            self.animation_list = [] #list of lists (action/img)
            self.frame_index = 0
            self.action = 0 #0-idle / 1-attack / 2-hurt / 3-death  updates via self.animation_list = []
            self.update_time = pygame.time.get_ticks()  # how much time has passed

            #-----------------------------Animations--------------------------------------------
            #loading idle action images
            temp_list = []
            for i in range(2):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/idle/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            #loading attack action images
            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/attack/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/hurt/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/dead/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img

            #-----------------------------------------------------------------------------------
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]     # to control action/images
            # two lists (action/frames)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

        #---------------------------------------------------------------------
        def update(self,animation_modifier): #animation
            animation_cooldown = 100
            if self.action == 0:
                animation_cooldown = 1000*animation_modifier
            if self.action == 1:
                animation_cooldown = 150*animation_modifier
            if self.action == 2:
                animation_cooldown = 300*animation_modifier
            if self.action == 3:
                animation_cooldown = 250*animation_modifier

            #animation_cooldown = cooldown
            self.image = self.animation_list[self.action][self.frame_index]  #adding action
            if pygame.time.get_ticks() - self.update_time > animation_cooldown: #if its more than 100 its time to update the animation stage
                self.update_time = pygame.time.get_ticks() #resets timer
                self.frame_index += 1
            # if animation run out, reset
            if self.frame_index >= len(self.animation_list[self.action]):  #adding action

                #after death unit should stay at the last frame of the dead animation sequence
                if self.action == 3:    #dead animation in the list.
                    self.frame_index = len(self.animation_list[self.action])-1  #final frame
                else:
                    self.idle() # sets to idle animation

        #-----------------------------------Idle----------------------------
        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def hurt(self):
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def dead(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def reset(self):
            self.alive = True
            self.inventory = self.max_inventory
            self.hp = self.max_hp
            self.armor = self.max_armor
            self.defence = self.start_defence
            self.strength = self.start_strength
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Attack----------------------------
        def attack(self,target):
            rand = random.randint(-5,5)
            damage = self.strength + rand
            if self.special == 1:
                #target.armor -= 0
                target.hp -= damage
            elif self.special != 1:
                target.armor -= int(damage*(target.defence/100))
                if target.armor > 0:
                    target.hp -= int(damage*(1 - target.defence/100))
                if target.armor <= 0:
                    target.hp -= int((damage*(1 - target.defence/100)-target.armor))
                    target.armor = 0

            # runs hurn animation
            target.hurt()

            if target.hp < 1:
                target.hp = 0
                target.alive = False
                # runs death animation
                target.dead()


            #   if self.special != 1:
            #       damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage-(damage*(target.defence/100)))), red)
            #   else:
            #       damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
            #DamageText
            if self.special != 1:
                if target.armor > 1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage*(1 - target.defence/100))), red)
                if target.armor <=1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
                    #DamageText(target.rect.centerx,target.rect.y-35,str(int((damage*(1 - target.defence/100)))), red)
            else:
                damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)

            damage_text_group.add(damage_text)
            #---------------------------------AttackSounds---------------------------------------
            #attack sound # 0-standard blade; 1-arrow; 2-stone
            if self.special == 0:
                pygame.mixer.Sound(attack_sound).play()
            elif self.special == 1:
                pygame.mixer.Sound(arrow_sound).play()
            elif self.special == 2:
                pygame.mixer.Sound(stone_sound).play()
            elif self.special == 3:
                pygame.mixer.Sound(snarl_sound).play()
            #------------------------------------------------------------------------------------


            #animations
            self.action = 1   # set action frames to as 1 as 1 = attack folder animation
            self.frame_index = 0 # frame 0 in the attack folder animation
            self.update_time = pygame.time.get_ticks()

        #----------------------------------------------------------------------
        def draw(self):
            screen.blit(self.image, self.rect)

    #-----------------------------------HealthBar--------------------------
    class healthBar ():
        def __init__(self, x,y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp
        def draw (self, hp):
            self.hp = hp
            # health ration
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen,red,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,green,(self.x, self.y, 50*ratio,5))

    #-----------------------------------ArmorBar--------------------------
    class armorBar ():
        def __init__(self, x,y, armor, max_armor):
            self.x = x
            self.y = y
            self.armor = armor
            self.max_armor = max_armor
        def draw (self, armor):
            self.armor = armor
            # health ration
            ratio = self.armor / self.max_armor
            pygame.draw.rect(screen,lightblue,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,blue,(self.x, self.y, 50*ratio,5))

    #-----------------------------------AttributeChangeBar-----------------
    class DamageText(pygame.sprite.Sprite):   # sprite is updated automatically
        def __init__(self,x,y,damage, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = fontDMG.render(damage, True, color)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.counter = 0

        def update(self):
            #move text
            self.rect.y -=1
            #delete after timer
            self.counter +=1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()    #python list
    #def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
    #-----------------------------------PlayerArmy--------------------------
    # militia = Fighter (435,295, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia_healthbar = healthBar (militia.rect.centerx-25,militia.rect.centery-55,militia.hp, militia.max_hp)
    # militia_armorbar = armorBar (militia.rect.centerx-25,militia.rect.centery-50,militia.armor, militia.max_armor)
    #-----------------------------------------------------------------------
    boy = Fighter (435,305, 'boy',120,60,35,40,1,3,0,True,False,0,0)
    boy_healthbar = healthBar (boy.rect.centerx-25,boy.rect.centery-55,boy.hp, boy.max_hp)
    boy_armorbar = armorBar (boy.rect.centerx-25,boy.rect.centery-50,boy.armor, boy.max_armor)
    #-----------------------------------------------------------------------
    landsknecht = Fighter (530,250,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht_healthbar = healthBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-55,landsknecht.hp, landsknecht.max_hp)
    landsknecht_armorbar = armorBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-50,landsknecht.armor, landsknecht.max_armor)
    #-----------------------------------------------------------------------
    landsknecht1 = Fighter (620,205,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht1_healthbar = healthBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-55,landsknecht1.hp, landsknecht1.max_hp)
    landsknecht1_armorbar = armorBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-50,landsknecht1.armor, landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    chevalier = Fighter (720,135,'chevalier',120,100,65,70,1,0,1,True,False,0,0)
    chevalier_healthbar = healthBar (chevalier.rect.centerx-25,chevalier.rect.centery-65,chevalier.hp, chevalier.max_hp)
    chevalier_armorbar = armorBar (chevalier.rect.centerx-25,chevalier.rect.centery-60,chevalier.armor, chevalier.max_armor)
    #-----------------------------------------------------------------------
    # militia1 = Fighter (700,165, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia1_healthbar = healthBar (militia1.rect.centerx-25,militia1.rect.centery-55,militia1.hp, militia1.max_hp)
    # militia1_armorbar = armorBar (militia1.rect.centerx-25,militia1.rect.centery-50,militia1.armor, militia1.max_armor)
    # #-----------------------------------------------------------------------
    # militia2 = Fighter (790,115, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    # militia2_healthbar = healthBar (militia2.rect.centerx-25,militia2.rect.centery-55,militia2.hp, militia2.max_hp)
    # militia2_armorbar = armorBar (militia2.rect.centerx-25,militia2.rect.centery-50,militia2.armor, militia2.max_armor)
    # #-----------------------------------------------------------------------
    archer = Fighter (530,115, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer_healthbar = healthBar (archer.rect.centerx-25,archer.rect.top-20,archer.hp, archer.max_hp)
    archer_armorbar = armorBar (archer.rect.centerx-25,archer.rect.top-15,archer.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    archer1 = Fighter (440,160, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer1_healthbar = healthBar (archer1.rect.centerx-25,archer1.rect.top-20,archer1.hp, archer.max_hp)
    archer1_armorbar = armorBar (archer1.rect.centerx-25,archer1.rect.top-15,archer1.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    yvan = Fighter (350,210, 'yvan',yvan_hp,yvan_armor,yvan_defene,yvan_attack,2,2,0,True,False,0,0)
    yvan_healthbar = healthBar (yvan.rect.centerx-25,yvan.rect.top-20,yvan.hp, yvan.max_hp)
    yvan_armorbar = armorBar (yvan.rect.centerx-25,yvan.rect.top-15,yvan.armor, yvan.max_armor)
    #max_hp,max_armor, defence, strength,



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_player = []
    #army_player.append(militia)
    army_player.append(boy)
    army_player.append(landsknecht)
    army_player.append(landsknecht1)
    army_player.append(chevalier)
    #army_player.append(militia1)
    #army_player.append(militia2)
    army_player.append(archer)
    army_player.append(archer1)
    army_player.append(yvan)

    army_player_front = army_player[:4]

    #-----------------------------HostileArmy-------------------------------
    # h_militia = Fighter(570,365,'militia',60,30,35,30,1,0,1,True,True,0,0)
    # h_militia_healthbar = healthBar(h_militia.rect.centerx-25,h_militia.rect.centery-55,h_militia.hp, h_militia.max_hp)
    # h_militia_armorbar = armorBar(h_militia.rect.centerx-25,h_militia.rect.centery-50,h_militia.armor, h_militia.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand = Fighter(570,365,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand_healthbar = healthBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-55,h_brigand.hp, h_brigand.max_hp)
    # h_brigand_armorbar = armorBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-50,h_brigand.armor, h_brigand.max_armor)
    # # #-----------------------------------------------------------------------
    h_landsknecht2 = Fighter (570,365,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand1 = Fighter(660,325,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand1_healthbar = healthBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-55,h_brigand1.hp, h_brigand1.max_hp)
    # h_brigand1_armorbar = armorBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-50,h_brigand1.armor, h_brigand1.max_armor)
    # # # #-----------------------------------------------------------------------
    h_landsknecht3 = Fighter (660,325,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht3_healthbar = healthBar (h_landsknecht3.rect.centerx-25,h_landsknecht3.rect.centery-55,h_landsknecht3.hp, h_landsknecht3.max_hp)
    h_landsknecht3_armorbar = armorBar (h_landsknecht3.rect.centerx-25,h_landsknecht3.rect.centery-50,h_landsknecht3.armor, h_landsknecht3.max_armor)
    #-----------------------------------------------------------------------
    h_landsknecht = Fighter (750,280,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht_healthbar = healthBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-55,h_landsknecht.hp, h_landsknecht.max_hp)
    h_landsknecht_armorbar = armorBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-50,h_landsknecht.armor, h_landsknecht.max_armor)
    #-----------------------------------------------------------------------
    h_landsknecht1 = Fighter (840,235,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    h_landsknecht1_healthbar = healthBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-55,h_landsknecht1.hp, h_landsknecht1.max_hp)
    h_landsknecht1_armorbar = armorBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-50,h_landsknecht1.armor, h_landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    # h_brigand2 = Fighter(940,195,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand2_healthbar = healthBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-55,h_brigand2.hp, h_brigand2.max_hp)
    # h_brigand2_armorbar = armorBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-50,h_brigand2.armor, h_brigand2.max_armor)
    h_chevalier = Fighter (930,150,'chevalier',120,100,60,65,1,0,1,True,True,0,0)
    h_chevalier_healthbar = healthBar (h_chevalier.rect.centerx-25,h_chevalier.rect.centery-65,h_chevalier.hp, h_chevalier.max_hp)
    h_chevalier_armorbar = armorBar (h_chevalier.rect.centerx-25,h_chevalier.rect.centery-60,h_chevalier.armor, h_chevalier.max_armor)
    #-----------------------------------------------------------------------
    # h_landsknecht2 = Fighter (790,340,'landsknecht',90,55,40,50,2,0,1,True,True,0,0)
    # h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    # h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    #-----------------------------------------------------------------------
    h_bowman = Fighter (790,350, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman_healthbar = healthBar (h_bowman.rect.centerx-25,h_bowman.rect.top-20,h_bowman.hp, h_bowman.max_hp)
    h_bowman_armorbar = armorBar (h_bowman.rect.centerx-25,h_bowman.rect.top-15,h_bowman.armor, h_bowman.max_armor)
    #-----------------------------------------------------------------------
    h_bowman1 = Fighter (695,400, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman1_healthbar = healthBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-20,h_bowman1.hp, h_bowman1.max_hp)
    h_bowman1_armorbar = armorBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-15,h_bowman1.armor, h_bowman1.max_armor)
    #-----------------------------------------------------------------------
    h_bowman2 = Fighter (880,310, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman2_healthbar = healthBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-20,h_bowman2.hp, h_bowman2.max_hp)
    h_bowman2_armorbar = armorBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-15,h_bowman2.armor, h_bowman2.max_armor)
    #-----------------------------------------------------------------------
    h_bowman3 = Fighter (960,260, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    h_bowman3_healthbar = healthBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-20,h_bowman3.hp, h_bowman3.max_hp)
    h_bowman3_armorbar = armorBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-15,h_bowman3.armor, h_bowman3.max_armor)



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_hostiles = []
    #army_hostiles.append(h_brigand)
    #army_hostiles.append(h_brigand1)
    army_hostiles.append(h_chevalier)
    army_hostiles.append(h_landsknecht)
    army_hostiles.append(h_landsknecht1)
    army_hostiles.append(h_landsknecht2)
    army_hostiles.append(h_landsknecht3)
    #army_hostiles.append(h_brigand2)
    army_hostiles.append(h_bowman)
    army_hostiles.append(h_bowman1)
    army_hostiles.append(h_bowman2)
    army_hostiles.append(h_bowman3)

    army_hostiles_front = army_hostiles[:5]


    #------------------------------TotalUnitNumber----------------------------
    total_hostiles = len(army_hostiles)
    total_allies = len(army_player)
    total_fighters = total_hostiles + total_allies

    #------------------------------ItemsUse(Button)---------------------------
    #inventory_button = button.Button(screen,WINDOW_SIZE[0]*0 + 110, WINDOW_SIZE[1]*0 - 6,inventory_bag,280,120,0, True, 'Inventory')

    inventory_button = button.ToggleButton(screen,-65, 425,inventory_bag,260,120,0, True, 'Inventory')
    #------------------------------ItemsUse(PotionButton)-------------------
    potion_button = button.Button(screen, WINDOW_SIZE[0]*0.01, WINDOW_SIZE[1]*0.90, health_potion, 48,72,30, False,f'Health Potion. Restores {health_potion_restores} HP')
    potion_button1 = button.Button(screen, WINDOW_SIZE[0]*0.06, WINDOW_SIZE[1]*0.90, defence_potion, 48,72,40, False,f'Defence Potion. Gives {defence_potion_adds} DEF/ARM')
    potion_button2 = button.Button(screen, WINDOW_SIZE[0]*0.11, WINDOW_SIZE[1]*0.90, berserk_potion, 48,72,60, False,f'Berserk Potion. Gives {berserk_potion_adds} ATK / Removes {int(berserk_potion_adds*1)} DEF')


    #------------------------------IconToggle(Reset)------------------------
    restart_button = button.Button(screen, 1100, 8, retry_icon, 84,90,25, True,'Try Again')
    skip_turn_button = button.Button(screen, WINDOW_SIZE[0]*0.92, WINDOW_SIZE[1]*0.62, skip_turn_img, 86,82,60, False,f'Skip Turn')
    victory_button = button.Button(screen, 1170, 15, victory_icon, 86,90,25, True,'Back to Map')
    leave_button = button.Button(screen, 1190, 0, doors_icon, 64,90,25, True,'Leave Battlefield')


    #-----------------------------------------------------------------------

    while highwaymen_battle_running:
        #display.fill((146,244,255))
        draw_bgBackscreen()
        #draw_noteMap()  # location map
        draw_bg()
        draw_panel()
        draw_bag()

        #-----------------------------DrawingUnits/AnimatioSpeedMod------------
        for units in army_player:
            # militia.update(0.9)
            # militia.draw()
            #------------
            landsknecht.update(1)
            landsknecht.draw()
            #------------
            chevalier.update(1.3)
            chevalier.draw()
            #------------
            # militia1.update(0.88)
            # militia1.draw()
            #------------
            boy.update(0.88)
            boy.draw()
            #------------
            landsknecht1.update(1.1)
            landsknecht1.draw()
            #------------
            # militia2.update(0.84)
            # militia2.draw()
            #------------
            archer.update(0.95)
            archer.draw()
            #------------
            archer1.update(0.92)
            archer1.draw()
            #------------
            yvan.update(1.05)
            yvan.draw()

        for hostile in army_hostiles:
            # h_brigand.update(0.9)
            # h_brigand.draw()
            # #------------
            # h_brigand2.update(0.85)
            # h_brigand2.draw()
            #------------
            h_landsknecht.update(0.95)
            h_landsknecht.draw()
            #------------
            h_landsknecht1.update(0.98)
            h_landsknecht1.draw()
            #------------
            h_landsknecht2.update(0.94)
            h_landsknecht2.draw()
            #------------
            h_landsknecht3.update(0.92)
            h_landsknecht3.draw()
            #------------
            h_chevalier.update(1.25)
            h_chevalier.draw()
            #------------
            # h_brigand1.update(0.9)
            # h_brigand1.draw()
            #------------
            h_bowman.update(0.89)
            h_bowman.draw()
            #------------
            h_bowman1.update(0.85)
            h_bowman1.draw()
            #------------
            h_bowman2.update(0.92)
            h_bowman2.draw()
            #------------
            h_bowman3.update(0.90)
            h_bowman3.draw()
        #-----------------------------HealthBar/ArmorBar-----------------------
        #-------------Player------------------------
        if show_indicators == True:
            if chevalier.alive == True:
                chevalier_healthbar.draw(chevalier.hp)
                chevalier_armorbar.draw(chevalier.armor)
            # if militia.alive == True:
            #     militia_healthbar.draw(militia.hp)
            #     militia_armorbar.draw(militia.armor)
            if boy.alive == True:
                boy_healthbar.draw(boy.hp)
                boy_armorbar.draw(boy.armor)
            if landsknecht.alive == True:
                landsknecht_healthbar.draw(landsknecht.hp)
                landsknecht_armorbar.draw(landsknecht.armor)
            # if militia1.alive == True:
            #     militia1_healthbar.draw(militia1.hp)
            #     militia1_armorbar.draw(militia1.armor)
            if landsknecht1.alive == True:
                landsknecht1_healthbar.draw(landsknecht1.hp)
                landsknecht1_armorbar.draw(landsknecht1.armor)
            # if militia2.alive == True:
            #     militia2_healthbar.draw(militia2.hp)
            #     militia2_armorbar.draw(militia2.armor)
            if archer.alive == True:
                archer_healthbar.draw(archer.hp)
                archer_armorbar.draw(archer.armor)
            if archer1.alive == True:
                archer1_healthbar.draw(archer1.hp)
                archer1_armorbar.draw(archer1.armor)
            if yvan.alive == True:
                yvan_healthbar.draw(yvan.hp)
                yvan_armorbar.draw(yvan.armor)

            #------------------Enemy--------------------
            if h_chevalier.alive == True:
                h_chevalier_healthbar.draw(h_chevalier.hp)
                h_chevalier_armorbar.draw(h_chevalier.armor)
            # if h_brigand.alive == True:
            #     h_brigand_healthbar.draw(h_brigand.hp)
            #     h_brigand_armorbar.draw(h_brigand.armor)
            # if h_brigand2.alive == True:
            #     h_brigand2_healthbar.draw(h_brigand2.hp)
            #     h_brigand2_armorbar.draw(h_brigand2.armor)
            if h_landsknecht.alive == True:
                h_landsknecht_healthbar.draw(h_landsknecht.hp)
                h_landsknecht_armorbar.draw(h_landsknecht.armor)
            if h_landsknecht1.alive == True:
                h_landsknecht1_healthbar.draw(h_landsknecht1.hp)
                h_landsknecht1_armorbar.draw(h_landsknecht1.armor)
            if h_landsknecht2.alive == True:
                h_landsknecht2_healthbar.draw(h_landsknecht2.hp)
                h_landsknecht2_armorbar.draw(h_landsknecht2.armor)
            if h_landsknecht3.alive == True:
                h_landsknecht3_healthbar.draw(h_landsknecht3.hp)
                h_landsknecht3_armorbar.draw(h_landsknecht3.armor)
            # if h_brigand1.alive == True:
            #     h_brigand1_healthbar.draw(h_brigand1.hp)
            #     h_brigand1_armorbar.draw(h_brigand1.armor)
            if h_bowman.alive == True:
                h_bowman_healthbar.draw(h_bowman.hp)
                h_bowman_armorbar.draw(h_bowman.armor)
            if h_bowman1.alive == True:
                h_bowman1_healthbar.draw(h_bowman1.hp)
                h_bowman1_armorbar.draw(h_bowman1.armor)
            if h_bowman2.alive == True:
                h_bowman2_healthbar.draw(h_bowman2.hp)
                h_bowman2_armorbar.draw(h_bowman2.armor)
            if h_bowman3.alive == True:
                h_bowman3_healthbar.draw(h_bowman3.hp)
                h_bowman3_armorbar.draw(h_bowman3.armor)
        #----------------------------------------------------------------------

        #-----------------------------DamageText-----------------------------
        damage_text_group.update()
        damage_text_group.draw(screen)
        #methods update and draw are parts of the sprite.

        #-----------------------------Items/SkipTurn/Inventory-----------------------------
        pos = pygame.mouse.get_pos()
        if skip_turn_button.rect.collidepoint(pos):
            draw_text(f'{skip_turn_button.description}', fontDMG, green, skip_turn_button.rect.x-30,skip_turn_button.rect.y+100)
        if skip_turn_button.draw():
            skip_turn=True
        if battle_status != 2 and leave_button.available == True:
            if leave_button.rect.collidepoint(pos):
                draw_text(f'{leave_button.description}', fontDMG, green, leave_button.rect.x-140,leave_button.rect.y+100)
            if leave_button.draw():
                play_music('Map')
                button.wealth = button.start_wealth
                highwaymen_battle_running = False


        if inventory_button.rect.collidepoint(pos):
            draw_text(f'{inventory_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)
        if inventory_button.toggled == True and battle_status ==0:
            potion_button.available = True
            potion_button1.available = True
            potion_button2.available = True


            #---------------------HealthPotion--------------------------------------
            if potion_button.available == True:
                if potion_button.draw():
                    use_health_potion = True
                draw_text(f'{potion_button.price}', fontBag, (255,225,100), potion_button.rect.x+5, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button.rect.collidepoint(pos):
                    draw_text(f'{potion_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

            #-------DefencePotion--------------
            if potion_button1.available == True:
                if potion_button1.draw():
                    use_defence_potion = True
                draw_text(f'{potion_button1.price}', fontBag, (255,225,100), potion_button.rect.x+65, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button1.rect.collidepoint(pos):
                    draw_text(f'{potion_button1.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

                #-------BerserkPotion--------------
            if potion_button2.available == True:
                if potion_button2.draw():
                    use_berserk_potion = True
                draw_text(f'{potion_button2.price}', fontBag, (255,225,100), potion_button.rect.x+130, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button2.rect.collidepoint(pos):
                    draw_text(f'{potion_button2.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)


        #---------------------InventoryStock--------------------------------------
        else:
            potion_button.available = False

        #--------------------------------------------------------------------------
        if battle_status ==0:   #win/loose check


            #-----------------------------PlayerAttacking---------------------------
            for count, ally in enumerate(army_player):
                if current_fighter == 1+count:
                    draw_text('^', fontActive, "#FFA500", ally.rect.centerx-20,ally.rect.y -65)
                    if ally.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:

                            if ally.reach == 2:
                                if engage == True and target != None:
                                    # conditioned upon engage below & def attack above
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif ally.reach == 1:
                                if engage == True and target != None and target.reach == 1:
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            for enemy in army_hostiles_front:
                                if all(enemy.alive == False for enemy in army_hostiles_front):
                                    #enemy.alive == False:
                                    if ally.reach == 1:
                                        if engage == True and target != None and target.reach == 2:
                                            ally.reach = 2
                                            ally.attack(target)
                                            current_fighter += 1
                                            action_cooldown = 0


                            #-----------------------------------------SkipTurn-----------------------------------------
                            if skip_turn == True:
                                current_fighter += 1
                                action_cooldown = 0
                                skip_turn_heal = 10
                                if ally.max_hp - ally.hp > skip_turn_heal:    #50
                                    skip_turn_heal = skip_turn_heal
                                else:
                                    skip_turn_heal = ally.max_hp - ally.hp
                                ally.hp += skip_turn_heal
                                #DamageText
                                damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(skip_turn_heal), green)
                                damage_text_group.add(damage_text)
                            skip_turn = False

                            #------------UsingItem(HealthPotion)---------------------------
                            if use_health_potion == True and button.wealth >= potion_button.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_hp - ally.hp > health_potion_restores:    #50
                                        heal_amount = health_potion_restores
                                    else:
                                        heal_amount = ally.max_hp - ally.hp
                                    ally.hp += heal_amount
                                    ally.inventory -= 1
                                    button.wealth -= potion_button.price
                                    #DamageText
                                    damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(heal_amount), green)
                                    damage_text_group.add(damage_text)

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_health_potion = False

                            #----------------------------------------------------
                            #------------UsingItem(DefencePotion)---------------
                            if use_defence_potion == True and button.wealth >= potion_button1.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_armor - ally.armor > defence_potion_adds:    #50
                                        add_defence_amount = defence_potion_adds
                                    else:
                                        add_defence_amount = ally.max_armor - ally.armor
                                    ally.armor += add_defence_amount
                                    ally.defence = 100
                                    ally.inventory -= 1
                                    button.wealth -= potion_button1.price     #Change price

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_defence_potion = False


                            #------------UsingItem(BerserkPotion)---------------
                            if use_berserk_potion == True and button.wealth >= potion_button2.price:
                                if ally.inventory > 0:
                                    ally.strength += berserk_potion_adds
                                    if ally.defence < int(berserk_potion_adds):
                                        ally.defence = 0
                                    else:
                                        ally.defence -= int(berserk_potion_adds)
                                    ally.inventory -= 1
                                    button.wealth -= potion_button2.price

                                    current_fighter +=1
                                    action_cooldown = 0
                                    #Change price
                                use_berserk_potion = False

                    else:
                        current_fighter +=1   #if dead = skip turn

            #-----------------------------EnemyAttacking----------------------------
            for count, enemy in enumerate(army_hostiles):
                if current_fighter == 1+ total_allies + count:   # "3 + count" - checks with the max_fighter var and number of units in army_player
                    draw_text('^', fontActive, "#FFA500", enemy.rect.centerx-20,enemy.rect.y -65)
                    if enemy.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:
                            #------------------------------EnemyDefencePotion------------------
                            if (enemy.armor / enemy.max_armor) <0.2 and enemy.armor < defence_potion_adds and enemy.max_armor > health_potion_restores and enemy.inventory >0:
                                if enemy.max_armor - enemy.armor > defence_potion_adds:
                                    add_defence_amount = defence_potion_adds
                                else:
                                    add_defence_amount = enemy.max_armor - enemy.armor
                                enemy.armor += add_defence_amount
                                enemy.defence = 100
                                enemy.inventory -= 1
                                current_fighter +=1
                                action_cooldown = 0


                            #------------------------------EnemyHealthPotion------------------
                            elif (enemy.hp / enemy.max_hp) <0.5 and enemy.inventory >0:
                                if enemy.max_hp - enemy.hp > health_potion_restores:
                                    heal_amount = health_potion_restores
                                else:
                                    heal_amount = enemy.max_hp - enemy.hp

                                enemy.hp += heal_amount
                                enemy.inventory -= 1

                                #DamageText
                                damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(heal_amount), green)
                                damage_text_group.add(damage_text)

                                current_fighter +=1
                                action_cooldown = 0

                            #-------------------------------------------------------------------
                            elif enemy.reach == 2:
                                if enemy.strength >= ally.hp and ally.alive == True:
                                    enemy.attack(ally)
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif enemy.reach == 1:
                                if all(ally.alive == True for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                elif all(ally.alive == False for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 2]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                            #else:
                            #     enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                            #     # enemy.hp += 10
                            #     current_fighter += 1
                            #     action_cooldown = 0
                            #     # damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(10), green)
                            #     # damage_text_group.add(damage_text)

                    else:
                        current_fighter +=1

            #---------------------------------Turns----------------------------
            # if all have had a turn, reset
            if current_fighter > total_fighters:
                current_fighter = 1

        #-----------------------------DefeatStatus-------------------------
        # checking alive/dead status
        alive_allies = 0
        for ally in army_player:
            if ally.alive == True:
                alive_allies +=1
        if alive_allies ==0:
            battle_status =1

        #---------------------------------VictoryStatus--------------------
        alive_enemies = 0
        for enemy in army_hostiles:
            if enemy.alive == True:
                alive_enemies +=1
        if alive_enemies ==0:
            battle_status =2

        #-------------------Defeat/VictoryStatusDisplay-------------------
        if battle_status !=0:
            if battle_status ==1:
                draw_text(f'Defeat!', fontMenuLarge, (155,0,0), screen.get_width()*0.46,0)
                #-------------------ResetButton-----------------------------------
                if restart_button.available == True:
                    if restart_button.draw():
                        play_music('Battle')
                        for ally in army_player:
                            ally.reset()
                        for enemy in army_hostiles:
                            enemy.reset()
                        button.wealth = button.start_wealth         #restart gold here
                        current_fighter = 1
                        action_cooldown = 0
                        battle_status = 0

                        pos = pygame.mouse.get_pos() # text over the button
                    if restart_button.rect.collidepoint(pos):
                        draw_text(f'{restart_button.description}', fontDMG, green, restart_button.rect.x+30,leave_button.rect.y+100)

            #-------------------Defeat/VictoryStatusDisplay-------------------
            if battle_status ==2:
                button.quest_highwaymen = 'locked'
                draw_text(f'Victory!', fontMenuLarge, green, screen.get_width()*0.46,0)
                if play_victory_music == True:
                   play_music('BattleVictory')
                play_victory_music = False
                if victory_button.available == True:
                    if victory_button.draw():
                        button.wealth += 400
                        button.start_wealth = button.wealth
                        button.quest_dragonhunt = 'unlocked'
                        print(button.start_wealth)
                        print(button.wealth)
                        play_music('Map')
                        highwaymen_battle_running = False
                    if victory_button.rect.collidepoint(pos):
                        draw_text(f'{victory_button.description}', fontDMG, green, victory_button.rect.x-75,leave_button.rect.y+100)
        #------------------------------End/Controls------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                if event.key == K_f and show_indicators == True:
                    show_indicators = False
                elif event.key == K_f and show_indicators == False:
                    show_indicators = True

                if event.key == K_o:
                    # fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen

                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

            #---------------------ToggleButton------------------------
            inventory_button.event_handler(event) #ToggleButton
            #---------------------ToggleButton------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        if leave_button.clicked == True or victory_button.clicked == True:
            mouse_map_position_align(750,400)
        #-----------------------------Action/TargetSearch-------------------
        engage = False
        target = None

        inventory_button.draw(screen) #ToggleButton

        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        screen.blit(normal_icon,pos)

        for count, ally in enumerate(army_player):
            if ally.rect.collidepoint(pos) and ally.alive == True:
                draw_text(f'{ally.id} | HP: {ally.hp} | ARM: {ally.armor} | ATK: {ally.strength} | DEF: {ally.defence} | INV: {ally.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))
        for count, enemy in enumerate(army_hostiles):
            if enemy.rect.collidepoint(pos) and enemy.alive == True:
                pygame.mouse.set_visible(False)
                screen.blit(attack_icon,pos)
                draw_text(f'{enemy.id} | HP: {enemy.hp} | ARM: {enemy.armor} | ATK: {enemy.strength} | DEF: {enemy.defence} | INV: {enemy.inventory}', font, (100,0,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))

                # show attack icon
                #--------------chooseTarget&Attack-------------------------
                if clicked == True and enemy.alive == True:
                    engage = True
                    target = army_hostiles[count]


        #-----------------------------------------------------------------------
        #surf = pygame.transform.scale(display, WINDOW_SIZE)
        #screen.blit(surf, (0,0))

        pygame.display.update()
        clock.tick(60)













































































































































def dragonhunt_battle ():
    dragonhunt_battle_running = True

    clock = pygame.time.Clock()
    pygame.init()

    pygame.mixer.set_num_channels(32)
    pygame.mixer.pre_init(44100,-16,2,512)
    #-----------------------------GameWindowSettings----------------------
    pygame.display.set_caption("Dragonhunt")
    WINDOW_SIZE = (1280,720)
    screen = pygame.display.set_mode((1280,720),0,32)
    #display = pygame.Surface((600,400))


    monitor_size =[pygame.display.Info().current_w, pygame.display.Info().current_h]

    fullscreen = button.fullscreen
    #not bool(linecache.getline('resolution.txt',1))
    if fullscreen:
        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
    else:
        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)


    #-----------------------------------Battlemap,Interface------------------------
    bg_backscreen = pygame.image.load("BattleScreen/background.png").convert_alpha()
    bg_backscreen = pygame.transform.scale(bg_backscreen, (int(WINDOW_SIZE[0]*1.00),(int(WINDOW_SIZE[1]*0.75))))

    # note_map = pygame.image.load("BattleScreen/note_Faroak0.png").convert_alpha()
    # note_map = pygame.transform.scale(note_map, (int(WINDOW_SIZE[0]*0.21),(int(WINDOW_SIZE[1]*0.28))))

    bg_map = pygame.image.load("BattleScreen/BigBattleMap.png").convert_alpha()
    bg_map = pygame.transform.scale(bg_map, (int(WINDOW_SIZE[0]*0.70),(int(WINDOW_SIZE[1]*0.70))))

    panel = pygame.image.load("BattleScreen/gamepanel0.png").convert_alpha()
    panel = pygame.transform.scale(panel, (int(WINDOW_SIZE[0]*1.10),(int(WINDOW_SIZE[1]*1.40))))

    bag_of_coins = pygame.image.load("BattleScreen/bag.png").convert_alpha()
    bag_of_coins = pygame.transform.scale(bag_of_coins, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    #-----------------------------------Icons-------------------------------------
    attack_icon = pygame.image.load("BattleScreen/icon_fight.png").convert_alpha()
    attack_icon = pygame.transform.scale(attack_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))

    normal_icon = pygame.image.load("BattleScreen/cursor_final.png").convert_alpha()
    normal_icon = pygame.transform.scale(normal_icon, (int(WINDOW_SIZE[0]*0.04),(int(WINDOW_SIZE[1]*0.05))))


    skip_turn_img = pygame.image.load("BattleScreen/skip_turn.png").convert_alpha()
    skip_turn_img = pygame.transform.scale(skip_turn_img, (int(WINDOW_SIZE[0]*0.06),(int(WINDOW_SIZE[1]*0.05))))

    #-----------------------------------Characters---------------------------------
    # militia_image = pygame.image.load("BattleScreen/militia/idle/0.png").convert_alpha()
    # landsknecht_image = pygame.image.load("BattleScreen/landsknecht/idle/0.png").convert_alpha()

    #------------------------------------------------------------------------------
    #--------------------------------Items----------------------------------------
    inventory_bag = pygame.image.load("BattleScreen/items/inventorybag.png").convert_alpha()
    inventory_bag = pygame.transform.scale(inventory_bag, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    health_potion = pygame.image.load("BattleScreen/items/health_potion.png").convert_alpha()
    health_potion = pygame.transform.scale(health_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    defence_potion = pygame.image.load("BattleScreen/items/reflexes_potion.png").convert_alpha()
    defence_potion = pygame.transform.scale(defence_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    berserk_potion = pygame.image.load("BattleScreen/items/berserk_potion.png").convert_alpha()
    berserk_potion = pygame.transform.scale(berserk_potion, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))


    doors_icon = pygame.image.load("BattleScreen/items/castledoors.png").convert_alpha()
    doors_icon = pygame.transform.scale(doors_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    retry_icon = pygame.image.load("BattleScreen/items/try again.png").convert_alpha()
    retry_icon = pygame.transform.scale(retry_icon, (int(WINDOW_SIZE[0]*0.10),(int(WINDOW_SIZE[1]*0.15))))

    victory_icon = pygame.image.load("BattleScreen/items/victory.png").convert_alpha()
    victory_icon = pygame.transform.scale(victory_icon, (int(WINDOW_SIZE[0]*0.15),(int(WINDOW_SIZE[1]*0.15))))

    #------------------------------------------------------------------------------
    screen.fill((242,238,203))

    mouse_position = (0, 0)
    #----------------------------------Music----------------------------------------
    #open_inventory_bag = pygame.mixer.Sound('sounds/OpenInventory.mp3')

    play_music('Battle1')

    #------------------------   -------------------------------------------------------
    attack_sound = pygame.mixer.Sound('BattleScreen/items/attack sound.wav')
    arrow_sound = pygame.mixer.Sound('BattleScreen/items/arrow.wav')
    snarl_sound = pygame.mixer.Sound('BattleScreen/items/snarl.wav')
    stone_sound = pygame.mixer.Sound('BattleScreen/items/throwingstone.wav')
    flame_sound = pygame.mixer.Sound('BattleScreen/items/flame.wav')
    #------------------------------------ActionOrder--------------------------------
    current_fighter = 1

    action_cooldown = 0
    action_waittime = 100
    draw_cursor = False
    battle_status = 0    #0 - nothing, 1 = lost, 2 = won

    # if battle_status ==0:
    #     play_music('Battle')
    # if battle_status ==2:
    #     pygame.mixer.music.play(0)
    #     play_music('BattleVictory')
    play_victory_music = True
    if battle_status ==1:
        play_music('BattleDefeat')

    #------------------------------------BattleInterface (line 315)-------------------
    engage = False
    clicked = False
    skip_turn = False
    #total_fighters = 11
    show_indicators = True

    use_health_potion = False
    health_potion_restores = 50

    use_defence_potion = False
    defence_potion_adds = 100

    use_berserk_potion = False
    berserk_potion_adds = 30


    #----------------------------------ShowStats------------------------------------
    font =pygame.font.SysFont('Times New Roman', 18)
    fontBag = pygame.font.Font('WorldMap/ESKARGOT.ttf', 38)
    fontDMG = pygame.font.Font('WorldMap/ESKARGOT.ttf', 26)
    fontActive = pygame.font.Font('WorldMap/ESKARGOT.ttf', 80)
    fontBattle = pygame.font.SysFont('Times New Roman', 70)
    #pygame.font.Font('WorldMap/ESKARGOT.ttf', 70)


    red = (230,16,35)
    ginger = (245,116,34)
    green = (0,255,0)
    paper =  (255,150,100)
    blue = (0,0,255)
    lightblue = (240,248,255)




    def draw_text(text,font,text_col,x,y):
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
    #--------------------------------------------------------------------------------

    def draw_bgBackscreen ():
        screen.blit(bg_backscreen,(0,0))

    # def draw_noteMap():
    #     screen.blit(note_map,(998,12))

    def draw_bg():
        screen.blit(bg_map,(210,40))

    def draw_bag():
        screen.blit(bag_of_coins,(0,0))
        draw_text(f'{button.wealth}', fontBag, (255,225,100), 120, 30)

    #------------------------------DrawingIndicators------------------------
    def draw_panel():
        screen.blit(panel,(-50,-35))
        # for count, i in enumerate(army_player):
        #       draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))
        # for count, i in enumerate(army_hostiles):
        #     draw_text(f'{i.id} | HP: {i.hp} | ARM: {i.armor} | ATK: {i.strength} | DEF: {i.defence} | INV: {i.inventory}', font, (100,0,0), ((panel.get_width())*0.58), (((screen.get_height() + bg_map.get_height())/2.24)+(count*16)))

    def countX(lst, x):
        return lst.count(x)

    #-------------------------------------------------------------------------
    yvan_hp = int(linecache.getline('charstats.txt',1))
    yvan_armor = int(linecache.getline('charstats.txt',2))
    yvan_defene = int(linecache.getline('charstats.txt',3))
    yvan_attack = int(linecache.getline('charstats.txt',4))

    #----------------------------------Charaters------------------------------
    class Fighter():
        def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
            self.id=id
            self.max_hp = max_hp
            self.hp = max_hp
            self.max_armor = max_armor
            self.armor = max_armor
            self.defence = defence
            self.start_defence = defence
            self.strength = strength
            self.start_strength = strength
            self.reach = reach
            self.special = special
            self.max_inventory = max_inventory
            self.inventory = max_inventory
            self.start_resistance = resistance
            self.resistance = resistance
            self.start_tricks = tricks
            self.tricks = tricks
            self.alive = True
            self.hostile = True
            self.animation_list = [] #list of lists (action/img)
            self.frame_index = 0
            self.action = 0 #0-idle / 1-attack / 2-hurt / 3-death  updates via self.animation_list = []
            self.update_time = pygame.time.get_ticks()  # how much time has passed

            #-----------------------------Animations--------------------------------------------
            #loading idle action images
            temp_list = []
            for i in range(2):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/idle/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                if self.id == 'caerbannog':
                    img = pygame.transform.scale(img,(img.get_width(), img.get_height()))
                else:
                    img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            #loading attack action images
            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/attack/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                if self.id == 'caerbannog':
                    img = pygame.transform.scale(img,(img.get_width(), img.get_height()))
                else:
                    img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(1):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/hurt/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                if self.id == 'caerbannog':
                    img = pygame.transform.scale(img,(img.get_width(), img.get_height()))
                else:
                    img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)

            temp_list = []
            for i in range(3):
                img = pygame.image.load(f'BattleScreen/units/{self.id}/dead/{i}.png')
                img = pygame.transform.flip(img, hostile, False)
                if self.id == 'caerbannog':
                    img = pygame.transform.scale(img,(img.get_width(), img.get_height()))
                else:
                    img = pygame.transform.scale(img,(img.get_width()*2, img.get_height()*2))
                temp_list.append(img) #appends temp list to store img
            self.animation_list.append(temp_list)
            #-----------------------------------------------------------------------------------

            self.image = self.animation_list[self.action][self.frame_index]     # to control action/images
            # two lists (action/frames)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)

        #---------------------------------------------------------------------
        def update(self,animation_modifier): #animation
            animation_cooldown = 100
            if self.action == 0:
                animation_cooldown = 1000*animation_modifier
            if self.action == 1:
                animation_cooldown = 150*animation_modifier
            if self.action == 2:
                animation_cooldown = 300*animation_modifier
            if self.action == 3:
                animation_cooldown = 250*animation_modifier

            #animation_cooldown = cooldown
            self.image = self.animation_list[self.action][self.frame_index]  #adding action
            if pygame.time.get_ticks() - self.update_time > animation_cooldown: #if its more than 100 its time to update the animation stage
                self.update_time = pygame.time.get_ticks() #resets timer
                self.frame_index += 1
            # if animation run out, reset
            if self.frame_index >= len(self.animation_list[self.action]):  #adding action

                #after death unit should stay at the last frame of the dead animation sequence
                if self.action == 3:    #dead animation in the list.
                    self.frame_index = len(self.animation_list[self.action])-1  #final frame
                else:
                    self.idle() # sets to idle animation

        #-----------------------------------Idle----------------------------
        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def hurt(self):
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def dead(self):
            self.action = 3
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Hurt----------------------------
        def reset(self):
            self.alive = True
            self.inventory = self.max_inventory
            self.hp = self.max_hp
            self.armor = self.max_armor
            self.defence = self.start_defence
            self.strength = self.start_strength
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()

        #-----------------------------------Attack----------------------------
        def attack(self,target):
            rand = random.randint(-5,5)
            damage = self.strength + rand
            if self.special == 1:
                #target.armor -= 0
                target.hp -= damage
            elif self.special != 1:
                target.armor -= int(damage*(target.defence/100))
                if target.armor > 0:
                    target.hp -= int(damage*(1 - target.defence/100))
                if target.armor <= 0:
                    target.hp -= int((damage*(1 - target.defence/100)-target.armor))
                    target.armor = 0
            # runs hurn animation
            target.hurt()

            if target.hp < 1:
                target.hp = 0
                target.alive = False
                # runs death animation
                target.dead()


            #   if self.special != 1:
            #       damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage-(damage*(target.defence/100)))), red)
            #   else:
            #       damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
            #DamageText
            if self.special != 1:
                if target.armor > 1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(int(damage*(1 - target.defence/100))), red)
                if target.armor <=1:
                    damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)
                    #DamageText(target.rect.centerx,target.rect.y-35,str(int((damage*(1 - target.defence/100)))), red)
            else:
                damage_text = DamageText(target.rect.centerx,target.rect.y-35,str(damage), red)

            damage_text_group.add(damage_text)
            #---------------------------------AttackSounds---------------------------------------
            #attack sound # 0-standard blade; 1-arrow; 2-stone
            if self.special == 0:
                pygame.mixer.Sound(attack_sound).play()
            elif self.special == 1:
                pygame.mixer.Sound(arrow_sound).play()
            elif self.special == 2:
                pygame.mixer.Sound(stone_sound).play()
            elif self.special == 3:
                pygame.mixer.Sound(snarl_sound).play()
            elif self.special == 4:
                pygame.mixer.Sound(flame_sound).play()
            #------------------------------------------------------------------------------------


            #animations
            self.action = 1   # set action frames to as 1 as 1 = attack folder animation
            self.frame_index = 0 # frame 0 in the attack folder animation
            self.update_time = pygame.time.get_ticks()

        #----------------------------------------------------------------------
        def draw(self):
            screen.blit(self.image, self.rect)

    #-----------------------------------HealthBar--------------------------
    class healthBar ():
        def __init__(self, x,y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp
        def draw (self, hp):
            self.hp = hp
            # health ration
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen,red,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,green,(self.x, self.y, 50*ratio,5))

    #-----------------------------------ArmorBar--------------------------
    class armorBar ():
        def __init__(self, x,y, armor, max_armor):
            self.x = x
            self.y = y
            self.armor = armor
            self.max_armor = max_armor
        def draw (self, armor):
            self.armor = armor
            # health ration
            ratio = self.armor / self.max_armor
            pygame.draw.rect(screen,lightblue,(self.x, self.y, 50,5))
            pygame.draw.rect(screen,blue,(self.x, self.y, 50*ratio,5))

    #-----------------------------------AttributeChangeBar-----------------
    class DamageText(pygame.sprite.Sprite):   # sprite is updated automatically
        def __init__(self,x,y,damage, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = fontDMG.render(damage, True, color)
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.counter = 0

        def update(self):
            #move text
            self.rect.y -=1
            #delete after timer
            self.counter +=1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()    #python list
    #def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
    #-----------------------------------PlayerArmy--------------------------
    militia = Fighter (350,300, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    militia_healthbar = healthBar (militia.rect.centerx-25,militia.rect.centery-55,militia.hp, militia.max_hp)
    militia_armorbar = armorBar (militia.rect.centerx-25,militia.rect.centery-50,militia.armor, militia.max_armor)
    #-----------------------------------------------------------------------
    boy = Fighter (435,270, 'boy',120,60,35,40,1,3,0,True,False,0,0)
    boy_healthbar = healthBar (boy.rect.centerx-25,boy.rect.centery-55,boy.hp, boy.max_hp)
    boy_armorbar = armorBar (boy.rect.centerx-25,boy.rect.centery-50,boy.armor, boy.max_armor)
    #-----------------------------------------------------------------------
    landsknecht = Fighter (540,210,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht_healthbar = healthBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-55,landsknecht.hp, landsknecht.max_hp)
    landsknecht_armorbar = armorBar (landsknecht.rect.centerx-25,landsknecht.rect.centery-50,landsknecht.armor, landsknecht.max_armor)
    #-----------------------------------------------------------------------
    landsknecht1 = Fighter (620,170,'landsknecht',90,55,45,55,1,0,1,True,False,0,0)
    landsknecht1_healthbar = healthBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-55,landsknecht1.hp, landsknecht1.max_hp)
    landsknecht1_armorbar = armorBar (landsknecht1.rect.centerx-25,landsknecht1.rect.centery-50,landsknecht1.armor, landsknecht1.max_armor)
    #-----------------------------------------------------------------------
    chevalier = Fighter (720,100,'chevalier',120,100,65,70,1,0,1,True,False,0,0)
    chevalier_healthbar = healthBar (chevalier.rect.centerx-25,chevalier.rect.centery-65,chevalier.hp, chevalier.max_hp)
    chevalier_armorbar = armorBar (chevalier.rect.centerx-25,chevalier.rect.centery-60,chevalier.armor, chevalier.max_armor)
    #-----------------------------------------------------------------------
    militia1 = Fighter (440,350, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    militia1_healthbar = healthBar (militia1.rect.centerx-25,militia1.rect.centery-55,militia1.hp, militia1.max_hp)
    militia1_armorbar = armorBar (militia1.rect.centerx-25,militia1.rect.centery-50,militia1.armor, militia1.max_armor)
    #-----------------------------------------------------------------------
    militia2 = Fighter (840,110, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    militia2_healthbar = healthBar (militia2.rect.centerx-25,militia2.rect.centery-55,militia2.hp, militia2.max_hp)
    militia2_armorbar = armorBar (militia2.rect.centerx-25,militia2.rect.centery-50,militia2.armor, militia2.max_armor)
    #-----------------------------------------------------------------------
    militia3 = Fighter (930,110, 'militia',60,30,35,30,1,0,1,True,False,0,0)
    militia3_healthbar = healthBar (militia3.rect.centerx-25,militia3.rect.centery-55,militia3.hp, militia3.max_hp)
    militia3_armorbar = armorBar (militia3.rect.centerx-25,militia3.rect.centery-50,militia3.armor, militia3.max_armor)
    #-----------------------------------------------------------------------
    archer = Fighter (530,115, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer_healthbar = healthBar (archer.rect.centerx-25,archer.rect.top-20,archer.hp, archer.max_hp)
    archer_armorbar = armorBar (archer.rect.centerx-25,archer.rect.top-15,archer.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    archer1 = Fighter (440,160, 'archer',65,30,40,32,2,1,1,True,False,0,0)
    archer1_healthbar = healthBar (archer1.rect.centerx-25,archer1.rect.top-20,archer1.hp, archer.max_hp)
    archer1_armorbar = armorBar (archer1.rect.centerx-25,archer1.rect.top-15,archer1.armor, archer.max_armor)
    #-----------------------------------------------------------------------
    yvan = Fighter (350,210, 'yvan',yvan_hp,yvan_armor,yvan_defene,yvan_attack,2,2,0,True,False,0,0)
    yvan_healthbar = healthBar (yvan.rect.centerx-25,yvan.rect.top-20,yvan.hp, yvan.max_hp)
    yvan_armorbar = armorBar (yvan.rect.centerx-25,yvan.rect.top-15,yvan.armor, yvan.max_armor)
    #max_hp,max_armor, defence, strength,



    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_player = []
    army_player.append(boy)
    army_player.append(landsknecht)
    army_player.append(landsknecht1)
    army_player.append(chevalier)
    army_player.append(archer)
    army_player.append(archer1)
    army_player.append(yvan)

    army_player.append(militia)
    army_player.append(militia1)
    army_player.append(militia2)
    army_player.append(militia3)

    army_player_front = army_player[:8]

    #def __init__(self, x,y,id,max_hp,max_armor, defence, strength, reach, special, max_inventory,alive,hostile,resistance,tricks):
    #-----------------------------HostileArmy-------------------------------
    h_dragohare = Fighter (760,230,'dragohare',400,300,85,40,3,4,0,True,True,0,0)
    h_dragohare_healthbar = healthBar (h_dragohare.rect.centerx+90,h_dragohare.rect.centery+70,h_dragohare.hp, h_dragohare.max_hp)
    h_dragohare_armorbar = armorBar (h_dragohare.rect.centerx+90,h_dragohare.rect.centery+75,h_dragohare.armor, h_dragohare.max_armor)
    #-----------------------------HostileArmy-------------------------------
    h_caerbannog = Fighter (850,280,'caerbannog',800,400,85,60,3,4,0,True,True,0,0)
    h_caerbannog_healthbar = healthBar (h_caerbannog.rect.centerx+20,h_caerbannog.rect.centery-105,h_caerbannog.hp, h_caerbannog.max_hp)
    h_caerbannog_armorbar = armorBar (h_caerbannog.rect.centerx+20,h_caerbannog.rect.centery-100,h_caerbannog.armor, h_caerbannog.max_armor)

    # h_militia = Fighter(570,365,'militia',60,30,35,30,1,0,1,True,True,0,0)
    # h_militia_healthbar = healthBar(h_militia.rect.centerx-25,h_militia.rect.centery-55,h_militia.hp, h_militia.max_hp)
    # h_militia_armorbar = armorBar(h_militia.rect.centerx-25,h_militia.rect.centery-50,h_militia.armor, h_militia.max_armor)
    #-----------------------------------------------------------------------
    # h_brigand = Fighter(570,365,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # h_brigand_healthbar = healthBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-55,h_brigand.hp, h_brigand.max_hp)
    # h_brigand_armorbar = armorBar(h_brigand.rect.centerx-25,h_brigand.rect.centery-50,h_brigand.armor, h_brigand.max_armor)
    # # #-----------------------------------------------------------------------
    # h_landsknecht2 = Fighter (570,365,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    # h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    # # #-----------------------------------------------------------------------
    # # h_brigand1 = Fighter(660,325,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # # h_brigand1_healthbar = healthBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-55,h_brigand1.hp, h_brigand1.max_hp)
    # # h_brigand1_armorbar = armorBar(h_brigand1.rect.centerx-25,h_brigand1.rect.centery-50,h_brigand1.armor, h_brigand1.max_armor)
    # # # # #-----------------------------------------------------------------------
    # h_landsknecht3 = Fighter (660,325,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht3_healthbar = healthBar (h_landsknecht3.rect.centerx-25,h_landsknecht3.rect.centery-55,h_landsknecht3.hp, h_landsknecht3.max_hp)
    # h_landsknecht3_armorbar = armorBar (h_landsknecht3.rect.centerx-25,h_landsknecht3.rect.centery-50,h_landsknecht3.armor, h_landsknecht3.max_armor)
    # #-----------------------------------------------------------------------
    # h_landsknecht = Fighter (750,280,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht_healthbar = healthBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-55,h_landsknecht.hp, h_landsknecht.max_hp)
    # h_landsknecht_armorbar = armorBar (h_landsknecht.rect.centerx-25,h_landsknecht.rect.centery-50,h_landsknecht.armor, h_landsknecht.max_armor)
    # #-----------------------------------------------------------------------
    # h_landsknecht1 = Fighter (840,235,'landsknecht',90,55,40,50,1,0,1,True,True,0,0)
    # h_landsknecht1_healthbar = healthBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-55,h_landsknecht1.hp, h_landsknecht1.max_hp)
    # h_landsknecht1_armorbar = armorBar (h_landsknecht1.rect.centerx-25,h_landsknecht1.rect.centery-50,h_landsknecht1.armor, h_landsknecht1.max_armor)
    # #-----------------------------------------------------------------------
    # #-----------------------------------------------------------------------
    # # h_brigand2 = Fighter(940,195,'brigand',50,25,30,30,1,0,1,True,True,0,0)
    # # h_brigand2_healthbar = healthBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-55,h_brigand2.hp, h_brigand2.max_hp)
    # # h_brigand2_armorbar = armorBar(h_brigand2.rect.centerx-25,h_brigand2.rect.centery-50,h_brigand2.armor, h_brigand2.max_armor)
    # h_chevalier = Fighter (930,150,'chevalier',120,100,60,65,1,0,1,True,True,0,0)
    # h_chevalier_healthbar = healthBar (h_chevalier.rect.centerx-25,h_chevalier.rect.centery-65,h_chevalier.hp, h_chevalier.max_hp)
    # h_chevalier_armorbar = armorBar (h_chevalier.rect.centerx-25,h_chevalier.rect.centery-60,h_chevalier.armor, h_chevalier.max_armor)
    # #-----------------------------------------------------------------------
    # # h_landsknecht2 = Fighter (790,340,'landsknecht',90,55,40,50,2,0,1,True,True,0,0)
    # # h_landsknecht2_healthbar = healthBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-55,h_landsknecht2.hp, h_landsknecht2.max_hp)
    # # h_landsknecht2_armorbar = armorBar (h_landsknecht2.rect.centerx-25,h_landsknecht2.rect.centery-50,h_landsknecht2.armor, h_landsknecht2.max_armor)
    # #-----------------------------------------------------------------------
    # h_bowman = Fighter (790,350, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman_healthbar = healthBar (h_bowman.rect.centerx-25,h_bowman.rect.top-20,h_bowman.hp, h_bowman.max_hp)
    # h_bowman_armorbar = armorBar (h_bowman.rect.centerx-25,h_bowman.rect.top-15,h_bowman.armor, h_bowman.max_armor)
    # #-----------------------------------------------------------------------
    # h_bowman1 = Fighter (695,400, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman1_healthbar = healthBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-20,h_bowman1.hp, h_bowman1.max_hp)
    # h_bowman1_armorbar = armorBar (h_bowman1.rect.centerx-25,h_bowman1.rect.top-15,h_bowman1.armor, h_bowman1.max_armor)
    # #-----------------------------------------------------------------------
    # h_bowman2 = Fighter (880,310, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman2_healthbar = healthBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-20,h_bowman2.hp, h_bowman2.max_hp)
    # h_bowman2_armorbar = armorBar (h_bowman2.rect.centerx-25,h_bowman2.rect.top-15,h_bowman2.armor, h_bowman2.max_armor)
    # #-----------------------------------------------------------------------
    # h_bowman3 = Fighter (960,260, 'bowman',45,20,30,25,2,1,1,True,True,0,0)
    # h_bowman3_healthbar = healthBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-20,h_bowman3.hp, h_bowman3.max_hp)
    # h_bowman3_armorbar = armorBar (h_bowman3.rect.centerx-25,h_bowman3.rect.top-15,h_bowman3.armor, h_bowman3.max_armor)
    #


    # +125 HealthBar / -45  amd +5 Armor
    #x: +90-100; y: -45
    #-----------------------------------------------------------------------
    army_hostiles = []
    army_hostiles.append(h_dragohare)
    #army_hostiles.append(h_brigand)
    #army_hostiles.append(h_brigand1)
    # army_hostiles.append(h_chevalier)
    # army_hostiles.append(h_landsknecht)
    # army_hostiles.append(h_landsknecht1)
    # army_hostiles.append(h_landsknecht2)
    # army_hostiles.append(h_landsknecht3)
    # #army_hostiles.append(h_brigand2)
    # army_hostiles.append(h_bowman)
    # army_hostiles.append(h_bowman1)
    # army_hostiles.append(h_bowman2)
    # army_hostiles.append(h_bowman3)

    army_hostiles_front = army_hostiles

    enemy_reserves = True
    army_hostiles_reserves = []
    army_hostiles_reserves.append(h_caerbannog)

    #------------------------------TotalUnitNumber----------------------------
    total_hostiles = len(army_hostiles)
    total_allies = len(army_player)
    total_fighters = total_hostiles + total_allies

    #------------------------------ItemsUse(Button)---------------------------
    #inventory_button = button.Button(screen,WINDOW_SIZE[0]*0 + 110, WINDOW_SIZE[1]*0 - 6,inventory_bag,280,120,0, True, 'Inventory')

    inventory_button = button.ToggleButton(screen,-65, 425,inventory_bag,260,120,0, True, 'Inventory')
    #------------------------------ItemsUse(PotionButton)-------------------
    potion_button = button.Button(screen, WINDOW_SIZE[0]*0.01, WINDOW_SIZE[1]*0.90, health_potion, 48,72,30, False,f'Health Potion. Restores {health_potion_restores} HP')
    potion_button1 = button.Button(screen, WINDOW_SIZE[0]*0.06, WINDOW_SIZE[1]*0.90, defence_potion, 48,72,40, False,f'Defence Potion. Gives {defence_potion_adds} DEF/ARM')
    potion_button2 = button.Button(screen, WINDOW_SIZE[0]*0.11, WINDOW_SIZE[1]*0.90, berserk_potion, 48,72,60, False,f'Berserk Potion. Gives {berserk_potion_adds} ATK / Removes {int(berserk_potion_adds*1)} DEF')


    #------------------------------IconToggle(Reset)------------------------
    restart_button = button.Button(screen, 1100, 8, retry_icon, 84,90,25, False,'Try Again')
    skip_turn_button = button.Button(screen, WINDOW_SIZE[0]*0.92, WINDOW_SIZE[1]*0.62, skip_turn_img, 86,82,60, False,f'Skip Turn')
    victory_button = button.Button(screen, 1170, 15, victory_icon, 86,90,25, True,'Back to Map')
    leave_button = button.Button(screen, 1190, 0, doors_icon, 64,90,25, True,'Leave Battlefield')

    #-----------------------------------EnemyReservesMangement----------------------



    #-----------------------------------------------------------------------

    while dragonhunt_battle_running:
        #display.fill((146,244,255))
        draw_bgBackscreen()
        #draw_noteMap()  # location map
        draw_bg()
        draw_panel()
        draw_bag()

        #-----------------------------DrawingUnits/AnimatioSpeedMod------------
        for units in army_player:
            militia.update(0.9)
            militia.draw()
            #------------
            militia1.update(0.88)
            militia1.draw()
            #------------
            militia2.update(0.84)
            militia2.draw()
            #------------
            militia3.update(0.84)
            militia3.draw()
            #------------
            landsknecht.update(1)
            landsknecht.draw()
            #------------
            chevalier.update(1.3)
            chevalier.draw()
            #------------
            boy.update(0.88)
            boy.draw()
            #------------
            landsknecht1.update(1.1)
            landsknecht1.draw()
            #------------
            archer.update(0.95)
            archer.draw()
            #------------
            archer1.update(0.92)
            archer1.draw()
            #------------
            yvan.update(1.05)
            yvan.draw()

#----------------------------EnemyUnitsDraw---------------------------
        for hostile in army_hostiles:
            h_dragohare.update(1.2)
            h_dragohare.draw()
            #------------
            # h_brigand.update(0.9)
            # h_brigand.draw()
            # #------------
            # h_brigand2.update(0.85)
            # h_brigand2.draw()
            #------------
            #h_landsknecht.update(0.95)
            # h_landsknecht.draw()
            # #------------
            # h_landsknecht1.update(0.98)
            # h_landsknecht1.draw()
            # #------------
            # h_landsknecht2.update(0.94)
            # h_landsknecht2.draw()
            # #------------
            # h_landsknecht3.update(0.92)
            # h_landsknecht3.draw()
            # #------------
            # h_chevalier.update(1.25)
            # h_chevalier.draw()
            # #------------
            # # h_brigand1.update(0.9)
            # # h_brigand1.draw()
            # #------------
            # h_bowman.update(0.89)
            # h_bowman.draw()
            # #------------
            # h_bowman1.update(0.85)
            # h_bowman1.draw()
            # #------------
            # h_bowman2.update(0.92)
            # h_bowman2.draw()
            # #------------
            # h_bowman3.update(0.90)
            # h_bowman3.draw()
        #-----------------------------HealthBar/ArmorBar-----------------------
        #-------------Player------------------------
        if show_indicators == True:
            if chevalier.alive == True:
               chevalier_healthbar.draw(chevalier.hp)
               chevalier_armorbar.draw(chevalier.armor)
            if militia.alive == True:
               militia_healthbar.draw(militia.hp)
               militia_armorbar.draw(militia.armor)
            if militia1.alive == True:
               militia1_healthbar.draw(militia1.hp)
               militia1_armorbar.draw(militia1.armor)
            if militia2.alive == True:
               militia2_healthbar.draw(militia2.hp)
               militia2_armorbar.draw(militia2.armor)
            if militia3.alive == True:
               militia3_healthbar.draw(militia3.hp)
               militia3_armorbar.draw(militia3.armor)
            if boy.alive == True:
               boy_healthbar.draw(boy.hp)
               boy_armorbar.draw(boy.armor)
            if landsknecht.alive == True:
               landsknecht_healthbar.draw(landsknecht.hp)
               landsknecht_armorbar.draw(landsknecht.armor)
            if landsknecht1.alive == True:
               landsknecht1_healthbar.draw(landsknecht1.hp)
               landsknecht1_armorbar.draw(landsknecht1.armor)
            if archer.alive == True:
               archer_healthbar.draw(archer.hp)
               archer_armorbar.draw(archer.armor)
            if archer1.alive == True:
               archer1_healthbar.draw(archer1.hp)
               archer1_armorbar.draw(archer1.armor)
            if yvan.alive == True:
               yvan_healthbar.draw(yvan.hp)
               yvan_armorbar.draw(yvan.armor)

            #------------------Enemy--------------------
            if h_dragohare.alive == True:
               h_dragohare_healthbar.draw(h_dragohare.hp)
               h_dragohare_armorbar.draw(h_dragohare.armor)
            # if h_chevalier.alive == True:
            #     h_chevalier_healthbar.draw(h_chevalier.hp)
            #     h_chevalier_armorbar.draw(h_chevalier.armor)
            # # if h_brigand.alive == True:
            # #     h_brigand_healthbar.draw(h_brigand.hp)
            # #     h_brigand_armorbar.draw(h_brigand.armor)
            # # if h_brigand2.alive == True:
            # #     h_brigand2_healthbar.draw(h_brigand2.hp)
            # #     h_brigand2_armorbar.draw(h_brigand2.armor)
            # if h_landsknecht.alive == True:
            #     h_landsknecht_healthbar.draw(h_landsknecht.hp)
            #     h_landsknecht_armorbar.draw(h_landsknecht.armor)
            # if h_landsknecht1.alive == True:
            #     h_landsknecht1_healthbar.draw(h_landsknecht1.hp)
            #     h_landsknecht1_armorbar.draw(h_landsknecht1.armor)
            # if h_landsknecht2.alive == True:
            #     h_landsknecht2_healthbar.draw(h_landsknecht2.hp)
            #     h_landsknecht2_armorbar.draw(h_landsknecht2.armor)
            # if h_landsknecht3.alive == True:
            #     h_landsknecht3_healthbar.draw(h_landsknecht3.hp)
            #     h_landsknecht3_armorbar.draw(h_landsknecht3.armor)
            # # if h_brigand1.alive == True:
            # #     h_brigand1_healthbar.draw(h_brigand1.hp)
            # #     h_brigand1_armorbar.draw(h_brigand1.armor)
            # if h_bowman.alive == True:
            #     h_bowman_healthbar.draw(h_bowman.hp)
            #     h_bowman_armorbar.draw(h_bowman.armor)
            # if h_bowman1.alive == True:
            #     h_bowman1_healthbar.draw(h_bowman1.hp)
            #     h_bowman1_armorbar.draw(h_bowman1.armor)
            # if h_bowman2.alive == True:
            #     h_bowman2_healthbar.draw(h_bowman2.hp)
            #     h_bowman2_armorbar.draw(h_bowman2.armor)
            # if h_bowman3.alive == True:
            #     h_bowman3_healthbar.draw(h_bowman3.hp)
            #     h_bowman3_armorbar.draw(h_bowman3.armor)
    #----------------------------------------------------------------------
#------------------------------------EnemyReserves-------------------------------------
        if h_dragohare.alive == False:
            h_caerbannog.update(1.3)
            h_caerbannog.draw()
            if enemy_reserves == True:
               army_hostiles.append(h_caerbannog)
               army_hostiles = army_hostiles_reserves
               enemy_reserves = False
            if h_caerbannog.alive == True:
               h_caerbannog_healthbar.draw(h_caerbannog.hp)
               h_caerbannog_armorbar.draw(h_caerbannog.armor)


        #-----------------------------DamageText-----------------------------
        damage_text_group.update()
        damage_text_group.draw(screen)
        #methods update and draw are parts of the sprite.

        #-----------------------------Items/SkipTurn/Inventory-----------------------------
        pos = pygame.mouse.get_pos()
        if skip_turn_button.rect.collidepoint(pos):
            draw_text(f'{skip_turn_button.description}', fontDMG, green, skip_turn_button.rect.x-30,skip_turn_button.rect.y+100)
        if skip_turn_button.draw():
            skip_turn=True
        if battle_status != 2 and leave_button.available == True:
            if leave_button.rect.collidepoint(pos):
                draw_text(f'{leave_button.description}', fontDMG, green, leave_button.rect.x-140,leave_button.rect.y+100)
            if leave_button.draw():
                play_music('Map')
                button.wealth = button.start_wealth
                dragonhunt_battle_running= False


        if inventory_button.rect.collidepoint(pos):
            draw_text(f'{inventory_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)
        if inventory_button.toggled == True and battle_status ==0:
            potion_button.available = True
            potion_button1.available = True
            potion_button2.available = True

            #---------------------HealthPotion--------------------------------------
            if potion_button.available == True:
                if potion_button.draw():
                    use_health_potion = True
                draw_text(f'{potion_button.price}', fontBag, (255,225,100), potion_button.rect.x+5, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button.rect.collidepoint(pos):
                    draw_text(f'{potion_button.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

            #-------DefencePotion--------------
            if potion_button1.available == True:
                if potion_button1.draw():
                    use_defence_potion = True
                draw_text(f'{potion_button1.price}', fontBag, (255,225,100), potion_button.rect.x+65, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button1.rect.collidepoint(pos):
                    draw_text(f'{potion_button1.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

                #-------BerserkPotion--------------
            if potion_button2.available == True:
                if potion_button2.draw():
                    use_berserk_potion = True
                draw_text(f'{potion_button2.price}', fontBag, (255,225,100), potion_button.rect.x+130, potion_button.rect.y-60)
                pos = pygame.mouse.get_pos()
                if potion_button2.rect.collidepoint(pos):
                    draw_text(f'{potion_button2.description}', fontDMG, green, potion_button.rect.x,potion_button.rect.y-100)

        #---------------------InventoryStock--------------------------------------
        else:
            potion_button.available = False

        #--------------------------------------------------------------------------
        if battle_status ==0:   #win/loose check

            #-----------------------------PlayerAttacking---------------------------
            for count, ally in enumerate(army_player):
                if current_fighter == 1+count:
                    draw_text('^', fontActive, "#FFA500", ally.rect.centerx-20,ally.rect.y -65)
                    if ally.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:

                            if ally.reach == 2:
                                if engage == True and target != None:
                                    # conditioned upon engage below & def attack above
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif ally.reach == 1:
                                if engage == True and target != None and target.reach != 2:
                                    ally.attack(target)
                                    current_fighter += 1
                                    action_cooldown = 0

                            for enemy in army_hostiles_front:
                                if all(enemy.alive == False for enemy in army_hostiles_front):
                                    #enemy.alive == False:
                                    if ally.reach == 1:
                                        if engage == True and target != None and target.reach == 2:
                                            ally.reach = 2
                                            ally.attack(target)
                                            current_fighter += 1
                                            action_cooldown = 0


                            #-----------------------------------------SkipTurn-----------------------------------------
                            if skip_turn == True:
                                current_fighter += 1
                                action_cooldown = 0
                                skip_turn_heal = 10
                                if ally.max_hp - ally.hp > skip_turn_heal:    #50
                                    skip_turn_heal = skip_turn_heal
                                else:
                                    skip_turn_heal = ally.max_hp - ally.hp
                                ally.hp += skip_turn_heal
                                #DamageText
                                damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(skip_turn_heal), green)
                                damage_text_group.add(damage_text)
                            skip_turn = False

                            #------------UsingItem(HealthPotion)---------------------------
                            if use_health_potion == True and button.wealth >= potion_button.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_hp - ally.hp > health_potion_restores:    #50
                                        heal_amount = health_potion_restores
                                    else:
                                        heal_amount = ally.max_hp - ally.hp
                                    ally.hp += heal_amount
                                    ally.inventory -= 1
                                    button.wealth -= potion_button.price
                                    #DamageText
                                    damage_text = DamageText(ally.rect.centerx,ally.rect.y-35,str(heal_amount), green)
                                    damage_text_group.add(damage_text)

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_health_potion = False

                            #----------------------------------------------------
                            #------------UsingItem(DefencePotion)---------------
                            if use_defence_potion == True and button.wealth >= potion_button1.price:
                                if ally.inventory > 0:
                                    # not healing beyond max_hp
                                    if ally.max_armor - ally.armor > defence_potion_adds:    #50
                                        add_defence_amount = defence_potion_adds
                                    else:
                                        add_defence_amount = ally.max_armor - ally.armor
                                    ally.armor += add_defence_amount
                                    ally.defence = 100
                                    ally.inventory -= 1
                                    button.wealth -= potion_button1.price     #Change price

                                    current_fighter +=1
                                    action_cooldown = 0
                                use_defence_potion = False


                            #------------UsingItem(BerserkPotion)---------------
                            if use_berserk_potion == True and button.wealth >= potion_button2.price:
                                if ally.inventory > 0:
                                    ally.strength += berserk_potion_adds
                                    if ally.defence < int(berserk_potion_adds):
                                        ally.defence = 0
                                    else:
                                        ally.defence -= int(berserk_potion_adds)
                                    ally.inventory -= 1
                                    button.wealth -= potion_button2.price

                                    current_fighter +=1
                                    action_cooldown = 0
                                    #Change price
                                use_berserk_potion = False

                    else:
                        current_fighter +=1   #if dead = skip turn



        #-----------------------------EnemyAttacking----------------------------
            for count, enemy in enumerate(army_hostiles ):
                if current_fighter == 1+ total_allies + count:   # "3 + count" - checks with the max_fighter var and number of units in army_player
                    draw_text('^', fontActive, "#FFA500", enemy.rect.centerx-20,enemy.rect.y -65)
                    if enemy.alive == True:
                        action_cooldown +=1
                        if action_cooldown >= action_waittime:
                            #------------------------------EnemyDefencePotion------------------
                            if (enemy.armor / enemy.max_armor) <0.2 and enemy.armor < defence_potion_adds and enemy.max_armor > health_potion_restores and enemy.inventory >0:
                                if enemy.max_armor - enemy.armor > defence_potion_adds:
                                    add_defence_amount = defence_potion_adds
                                else:
                                    add_defence_amount = enemy.max_armor - enemy.armor
                                enemy.armor += add_defence_amount
                                enemy.defence = 100
                                enemy.inventory -= 1
                                current_fighter +=1
                                action_cooldown = 0


                            #------------------------------EnemyHealthPotion------------------
                            elif (enemy.hp / enemy.max_hp) <0.5 and enemy.inventory >0:
                                if enemy.max_hp - enemy.hp > health_potion_restores:
                                    heal_amount = health_potion_restores
                                else:
                                    heal_amount = enemy.max_hp - enemy.hp

                                enemy.hp += heal_amount
                                enemy.inventory -= 1

                                #DamageText
                                damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(heal_amount), green)
                                damage_text_group.add(damage_text)

                                current_fighter +=1
                                action_cooldown = 0

                            #-------------------------------------------------------------------
                            elif enemy.reach == 2:
                                if enemy.strength >= ally.hp and ally.alive == True:
                                    enemy.attack(ally)
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif enemy.reach == 1:
                                if all(ally.alive == True for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                elif all(ally.alive == False for ally in army_player_front):
                                    enemy.attack (random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 2]))
                                    current_fighter += 1
                                    action_cooldown = 0
                                else:
                                    enemy.attack(random.choice([ally for ally in army_player if ally.alive == True and ally.reach == 1]))
                                    current_fighter += 1
                                    action_cooldown = 0

                            elif enemy.reach == 3 and enemy.id == 'dragohare':
                                alive_targets = sum(ally.alive == True for ally in army_player)
                                if alive_targets >= 6:
                                    for i in range(6):
                                        enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                elif alive_targets < 6:
                                    for j in range (alive_targets):
                                        enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                enemy.armor = enemy.max_armor
                                current_fighter += 1
                                action_cooldown = 0

                            elif enemy.reach == 3 and enemy.id == 'caerbannog':
                                alive_targets = sum(ally.alive == True for ally in army_player)
                                if alive_targets >= 6:
                                    for i in range(6):
                                        enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                elif alive_targets < 6:
                                    for j in range (alive_targets):
                                        enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                                current_fighter += 1
                                action_cooldown = 0

                            else:
                                 current_fighter +=1

                    #     enemy.attack(random.choice([ally for ally in army_player if ally.alive == True]))
                    #     # enemy.hp += 10
                    #     current_fighter += 1
                    #     action_cooldown = 0
                    #     # damage_text = DamageText(enemy.rect.centerx,enemy.rect.y-35,str(10), green)
                    #     # damage_text_group.add(damage_text)

                    else:
                        current_fighter +=1

            #---------------------------------Turns----------------------------
            # if all have had a turn, reset
            if current_fighter > total_fighters:
                current_fighter = 1

        #-----------------------------DefeatStatus-------------------------
        # checking alive/dead status
        alive_allies = 0
        for ally in army_player:
            if ally.alive == True:
                alive_allies +=1
        if alive_allies ==0:
            battle_status =1

        #---------------------------------VictoryStatus--------------------
        alive_enemies = 0
        for enemy in army_hostiles:
            if enemy.alive == True:
                alive_enemies +=1
        if alive_enemies ==0 and all(enemy.alive == False for enemy in army_hostiles_reserves):
            battle_status =2

        #-------------------Defeat/VictoryStatusDisplay-------------------
        if battle_status !=0:
            if battle_status ==1:
                draw_text(f'Defeat!', fontMenuLarge, (155,0,0), screen.get_width()*0.46,0)

                #-------------------ResetButton-----------------------------------
                if restart_button.available == True:
                    if restart_button.draw():
                        play_music('Battle1')
                        for ally in army_player:
                            ally.reset()
                        for enemy in army_hostiles:
                            enemy.reset()


                        button.wealth = button.start_wealth         #restart gold here
                        current_fighter = 1
                        action_cooldown = 0
                        battle_status = 0

                        pos = pygame.mouse.get_pos() # text over the button
                    if restart_button.rect.collidepoint(pos):
                        draw_text(f'{restart_button.description}', fontDMG, green, restart_button.rect.x+30,leave_button.rect.y+100)

            #-------------------Defeat/VictoryStatusDisplay-------------------
            if battle_status ==2:
                button.quest_dragonhunt = 'locked'
                draw_text(f'Victory!', fontMenuLarge, green, screen.get_width()*0.46,0)
                if play_victory_music == True:
                   play_music('BattleVictory')
                play_victory_music = False
                if victory_button.available == True:
                    if victory_button.draw():
                        button.wealth += 1000
                        button.start_wealth = button.wealth
                        button.quest_finale= 'unlocked'
                        print(button.start_wealth)
                        print(button.wealth)
                        pyautogui.moveTo(750, 400)
                        play_music('Outro')
                        dragonhunt_battle_running = False
                    if victory_button.rect.collidepoint(pos):
                        draw_text(f'{victory_button.description}', fontDMG, green, victory_button.rect.x-75,leave_button.rect.y+100)
        #------------------------------End/Controls------------------------
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w,event.h),0,32)

            if event.type == KEYDOWN:
                if event.key == K_f and show_indicators == True:
                    show_indicators = False
                elif event.key == K_f and show_indicators == False:
                    show_indicators = True

                if event.key == K_o:
                    # fullscreen = not fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    button.fullscreen = not button.fullscreen
                    # with open('resolution.txt', 'w') as file:
                    #     file.write(str(fullscreen))
                    fullscreen = button.fullscreen

                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size,FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(),screen.get_height()),0,32)

            #---------------------ToggleButton------------------------
            inventory_button.event_handler(event) #ToggleButton
            #---------------------ToggleButton------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        if leave_button.clicked == True or victory_button.clicked == True:
            mouse_map_position_align(750,400)
        #-----------------------------Action/TargetSearch-------------------
        engage = False
        target = None

        inventory_button.draw(screen) #ToggleButton

        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        screen.blit(normal_icon,pos)

        for count, ally in enumerate(army_player):
            if ally.rect.collidepoint(pos) and ally.alive == True:
                draw_text(f'{ally.id} | HP: {ally.hp} | ARM: {ally.armor} | ATK: {ally.strength} | DEF: {ally.defence} | INV: {ally.inventory}', font, (0,100,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))
        for count, enemy in enumerate(army_hostiles):
            if enemy.rect.collidepoint(pos) and enemy.alive == True:
                pygame.mouse.set_visible(False)
                screen.blit(attack_icon,pos)
                draw_text(f'{enemy.id} | HP: {enemy.hp} | ARM: {enemy.armor} | ATK: {enemy.strength} | DEF: {enemy.defence} | INV: {enemy.inventory}', font, (100,0,0), ((panel.get_width())*0.01), (((screen.get_height() + bg_map.get_height())/2.24)))

                # show attack icon
                #--------------chooseTarget&Attack-------------------------
                if clicked == True and enemy.alive == True:
                    engage = True
                    target = army_hostiles[count]


        #-----------------------------------------------------------------------
        #surf = pygame.transform.scale(display, WINDOW_SIZE)
        #screen.blit(surf, (0,0))

        pygame.display.update()
        clock.tick(60)

























































































































#
#
# def adventure():
#     adventure_running = True
#     while adventure_running:
#         screen.fill((0,0,0))
#         draw_text('Adventure Begins', fontMenu, (255,225,100),screen, 20,20)
#         draw_text('Press ESC to return', fontMenu, (255,225,100),screen, 20,60)  #Yvan\'s
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     MainMusic.play_music()
#                     adventure_running = False
#
#         pygame.mouse.set_visible(False)
#         mouse_position = pygame.mouse.get_pos()
#         player_rect.x, player_rect.y = mouse_position
#         screen.blit(normal_icon, player_rect)
#
#         pygame.display.update()
#         mainClock.tick(60)



def leave():
    running = True
    while running:
        screen.fill((0,0,0))
        draw_text('Quit', fontMenu, (255,225,100),screen, 20,20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


if __name__ == '__main__':
    main_menu()

