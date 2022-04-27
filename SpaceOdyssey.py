
import sys

import pygame.time

from gamemodes import *
from Objects import Player
from menu import DemoBox, Button
import options_manager


def settings_menu():

    # Options widget for game language
    left_button = Button(screen, '<', 30, 50, 'assets/font/04B_30__.TTF', 50)
    right_button = Button(screen, '>', 30, 50, 'assets/font/04B_30__.TTF', 50)

    lang_options = CircularOptions(screen, screen.get_width() // 2, screen.get_height() // 4, width=100,
                                   height=50,
                                   bleft=left_button, bright=right_button, font='assets/font/Pixellari.ttf',
                                   size=30, bdradius=150, title=options_manager.language_dict.get('language'))
    lang_options.options.extend(['English', 'Spanish', 'German'])
    lang_options.init_option(options_manager.settings_dict.get('language'))

    left_button_mus = Button(screen, '<', 30, 50, 'assets/font/04B_30__.TTF', 50)
    right_button_mus = Button(screen, '>', 30, 50, 'assets/font/04B_30__.TTF', 50)

    music_options = CircularOptions(screen, screen.get_width() // 2, screen.get_height() // 2, width=100,
                                   height=50,
                                   bleft=left_button_mus, bright=right_button_mus, font='assets/font/Pixellari.ttf',
                                   size=30, bdradius=150, title=options_manager.language_dict.get('music'))
    music_options.options.extend(['Yes', 'No'])
    music_options.init_option(options_manager.settings_dict.get('music'))

    left_button_dif = Button(screen, '<', 30, 50, 'assets/font/04B_30__.TTF', 50)
    right_button_dif = Button(screen, '>', 30, 50, 'assets/font/04B_30__.TTF', 50)

    difficulty_options = CircularOptions(screen, screen.get_width()//2, int(screen.get_width()*0.6),
                                         width=100, height=50, bleft=left_button_dif, bright=right_button_dif,
                                         font='assets/font/Pixellari.ttf', size=30, bdradius=150,
                                         title=options_manager.language_dict.get('difficulty'))
    difficulty_options.options.extend(['Normal', 'Hard'])
    difficulty_options.init_option(options_manager.settings_dict.get('difficulty'))

    # Menu loop
    while True:

        # Read from lang
        lang_options.title = options_manager.language_dict.get('language')
        music_options.title = options_manager.language_dict.get('music')
        difficulty_options.title = options_manager.language_dict.get('difficulty')

        pos = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))

        title = title_font.render(options_manager.language_dict.get('settings'), False, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width()//2, title.get_height()))
        screen.blit(title, title_rect)
        back_button = Button(screen, '<', 30, 50, 'assets/font/04B_30__.TTF', 50, main_menu)

        difficulty_options.draw()
        music_options.draw()
        lang_options.draw()

        back_button.is_inside(pos)
        back_button.draw()

        lang_options.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                options_manager.save_settings()
                options_manager.save_scores()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_inside(pos):
                    main_menu()
                elif lang_options.check_buttons(pos):

                    options_manager.settings_dict['language'] = str(lang_options.current_option)
                    options_manager.parse_language()

                elif music_options.check_buttons(pos):
                    options_manager.settings_dict['music'] = str(music_options.current_option)
                    if options_manager.settings_dict.get('music') == 'Yes':
                        mixer.play(-1)
                    else:
                        mixer.stop()
                else:
                    difficulty_options.check_buttons(pos)
                    options_manager.settings_dict['difficulty'] = str(difficulty_options.current_option)
        pygame.display.update()


def gamemode_menu():

    # Menu loop
    while True:

        screen.blit(background, (0, 0))
        title = title_font.render(options_manager.language_dict.get('gamemode'), False, (255, 255, 255)).convert_alpha()
        title_rect = title.get_rect(center=(screen.get_width()//2, title.get_height()))
        screen.blit(title, title_rect)

        classic_demobox = DemoBox('Classic', screen, classic_demo, width / 6 - saver_demo.get_width() / 2, height/2-50,
                                  options_manager.language_dict.get('classic_desc'), font)

        shooter_demobox = DemoBox('Shooter', screen, shooter_demo, width/2-shooter_demo.get_width()/2, height/2-50,
                                  options_manager.language_dict.get('shooter_desc'), font)

        saver_demobox = DemoBox('Astrosaver', screen, saver_demo, width - width/6 - saver_demo.get_width() / 2, height/2-50,
                                options_manager.language_dict.get('saver_desc'), font)

        back_button = Button(screen, '<', 30, 50, 'assets/font/04B_30__.TTF', 50, main_menu)
        pos = pygame.mouse.get_pos()

        if classic_demobox.check_inside(pos) is not True:
            if shooter_demobox.check_inside(pos) is not True:
                if saver_demobox.check_inside(pos) is not True:
                    back_button.is_inside(pos)

        back_button.draw()
        classic_demobox.draw()

        shooter_demobox.draw()

        saver_demobox.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                options_manager.save_settings()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if classic_demobox.check_inside(pos) is True:
                    classic_game.game()
                    gamemode_menu()
                elif shooter_demobox.check_inside(pos) is True:
                    shooting_game.game()
                    gamemode_menu()
                elif saver_demobox.check_inside(pos) is True:
                    saver_game.game()
                    gamemode_menu()
                elif back_button.is_inside(pos) is True:
                    back_button.execute()

        clock.tick(32)
        pygame.display.update()


def main_menu():

    # Display elements config
    count = 0
    press = font.render(options_manager.language_dict.get('presstoplay'), False, (255, 255, 255))
    press_rect = press.get_rect(center=(screen.get_width()//2, 400))
    space_rect = space.get_rect(center=(screen.get_width()//2, 190))
    odyssey_rect = odyssey.get_rect(center=(screen.get_width()//2, space_rect.bottom+30))

    # Menu loop
    while True:
        mouse_pos = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))
        screen.blit(space, space_rect)
        screen.blit(odyssey, odyssey_rect)
        if count <= 600:
            screen.blit(press, press_rect)
        count += 15

        if count == 1200:
            count = 0

        settings_button = Button(screen, '', width-50, 50, image=settings_symbol, activeimg=settings_active)

        settings_button.is_inside(mouse_pos)

        settings_button.draw()
        settings_button.command = settings_menu

        ship_player.draw(screen)
        ship_player.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options_manager.save_settings()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                gamemode_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_button.is_inside(mouse_pos):
                    settings_menu()

        pygame.display.update()
        clock.tick(60)
# Main code
# If played with .py file, remove this line
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

width = 800
height = 600

player_size = 64


clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('Space Odyssey')

options_manager.parse_settings()
options_manager.parse_language()
options_manager.parse_scores()

# Images initialization
background = pygame.image.load('assets/retro.jpeg').convert()
background = pygame.transform.scale(background, (width, height)).convert_alpha()

shooter_bg = pygame.image.load('assets/black_hole.png').convert_alpha()
shooter_bg = pygame.transform.scale(shooter_bg, (width, height)).convert_alpha()

classic_bg = pygame.image.load('assets/mars.png').convert_alpha()
classic_bg = pygame.transform.scale(classic_bg, (width, height)).convert_alpha()

classic_demo = pygame.image.load('assets/menu/demo_classic.png').convert_alpha()
classic_demo = pygame.transform.scale(classic_demo, (200, 120)).convert_alpha()

shooter_demo = pygame.image.load('assets/menu/demo_shooter.png').convert_alpha()
shooter_demo = pygame.transform.scale(shooter_demo, (200, 120)).convert_alpha()

saver_demo = pygame.image.load('assets/menu/demo_saver.png').convert_alpha()
saver_demo = pygame.transform.scale(saver_demo, (200, 120)).convert_alpha()

space = pygame.image.load('assets/space.png').convert_alpha()


odyssey = pygame.image.load('assets/odyssey.png').convert_alpha()


settings_symbol = pygame.image.load('assets/menu/settings.png').convert_alpha()
settings_symbol = pygame.transform.scale(settings_symbol, (50, 50)).convert_alpha()

settings_active = pygame.image.load('assets/menu/settings_active.png').convert_alpha()
settings_active = pygame.transform.scale(settings_active, (50, 50)).convert_alpha()

ship1 = pygame.image.load('assets/player/ship1.png')
ship1 = pygame.transform.scale(ship1, (64, 80)).convert_alpha()
ship2 = pygame.image.load('assets/player/ship2.png')
ship2 = pygame.transform.scale(ship2, (64, 80)).convert_alpha()
ship3 = pygame.image.load('assets/player/ship3.png')
ship3 = pygame.transform.scale(ship3, (64, 80)).convert_alpha()
pygame.display.set_icon(ship1)

# player center positions
ship_posx = 370
ship_posy = 480


asteroid_img = pygame.image.load('assets/sprites/asteroid.png').convert_alpha()

projectile_img = pygame.image.load('assets/sprites/laser.png').convert_alpha()
projectile_img = pygame.transform.scale(projectile_img, (10, 30))

goodie_img = pygame.image.load('assets/sprites/ammo.png').convert_alpha()
goodie_img = pygame.transform.scale(goodie_img, (38, 40))

astronaut_img = pygame.image.load('assets/sprites/astronaut.png').convert_alpha()
astronaut_img = pygame.transform.scale(astronaut_img, (50, 45))

satellite_img = pygame.image.load('assets/sprites/satellite.png').convert_alpha()
satellite_img = pygame.transform.scale(satellite_img, (64, 64))

border_right = width-player_size
border_left = 0


font = pygame.font.Font('assets/font/Pixellari.ttf', 25)
title_font = pygame.font.Font('assets/font/04B_30__.TTF', 50)


mixer = pygame.mixer.Sound('assets/sounds/effects/bg_music.wav')
mixer.set_volume(0.05)
if options_manager.settings_dict.get('music') == 'Yes':
    mixer.play(-1)

ship_player = Player(ship_posx, ship_posy, ship1, ship2, ship3)

# Game mode objects initialized
classic_game = Classic('Classic', classic_bg, asteroid_img, goodie_img, projectile_img, ship_player, screen)
saver_game = AstroSaver('Astronaut Saver', background, satellite_img, goodie_img, projectile_img, ship_player, screen,
                        astronaut_img)
shooting_game = Shooter('Classic', shooter_bg, asteroid_img, goodie_img, projectile_img, ship_player, screen)
# Add main mixer to games
classic_game.game_mixer = mixer
saver_game.game_mixer = mixer
shooting_game.game_mixer = mixer

# launch game
main_menu()







