import pygame.surface
import math
from Objects import *
from menu import *
import options_manager
import time


class Game:
    """
    Base class for all game modes
    Handles Sprites drawing, pause and game over menus
    Handles general operations (e.g., moving the player)
    """
    def __init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen):
        self.name = name
        self.background = background
        self.asteroid_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.goodies_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.asteroid_img = asteroid_img
        self.goodies_img = goodies_img
        self.missile_img = missile_img
        self.height = 600
        self.width = 800
        self.player_size = 64
        self.border_right = self.width - self.player_size
        self.border_left = 0
        self.score = 0
        self.player = player
        self.screen = screen
        self.paused = False

        self.pause_screen = pygame.surface.Surface((self.screen.get_width(), self.screen.get_height()))
        self.pause_screen.fill((117, 117, 117))
        self.pause_screen.set_alpha(5)

        self.over_screen = pygame.surface.Surface((self.screen.get_width(), self.screen.get_height()))
        self.over_screen.fill((252, 3, 3))
        self.over_screen.set_alpha(1)

        self.max_obstacles = 10
        self.over = False

        self.font = pygame.font.Font('assets/font/Pixellari.ttf', 30)
        self.title_font = pygame.font.Font('assets/font/04B_30__.TTF',80)

        self.game_mixer = None
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60)
        self.last_time = time.time()

    def drop_asteroids(self):

        """Creates collidable objects at different positions at the top of the window"""

        delay = random.randint(1,10)

        if len(self.asteroid_group) < self.max_obstacles and delay < 7:
            x_pos = random.randrange(0, self.border_right, 50)
            y_pos = random.randrange(0, 100)
            y_pos = 0 - y_pos * 2
            size = random.randrange(64, 84)
            asteroid = Asteroid(x_pos, y_pos, self.asteroid_img, size, self.asteroid_group)
            self.asteroid_group.add(asteroid)


    def draw_missiles(self):
        """Maps all missiles into the surface"""
        self.missile_group.draw(self.screen)

    def draw_asteroids(self):
        """Maps all collidable objects into the surface"""
        self.asteroid_group.draw(self.screen)

    def check_missile_collision(self):
        """
        Checks for all missiles whether they hit an asteroid
        If it does, it removes them
        """
        for missile in self.missile_group:
            collided = pygame.sprite.spritecollide(missile, self.asteroid_group, True)
            if len(collided) > 0:
                self.missile_group.remove(missile)
                pygame.mixer.Sound('assets/sounds/effects/explosion.wav').play()

    def check_goodie_collision(self):
        """
        Checks if a player collects a goodie
        """
        collided = pygame.sprite.spritecollide(self.player, self.goodies_group, True)
        for goodie in collided:
            self.goodies_group.remove(goodie)
            self.player.ammo += 1
            pygame.mixer.Sound('assets/sounds/effects/pickup.wav').play()

    def drop_goodies(self):
        """Generates ammo perks at the top of the window at a determined probability"""

        prob = random.randrange(1, 160)

        if prob < 2:
            x_pos = random.randrange(0, self.border_right, 50)
            y_pos = 0
            goodie = Goodie(x_pos, y_pos, self.goodies_img, self.goodies_group)
            self.goodies_group.add(goodie)

    def check_player_collision(self):
        """Handles player collisions with obstacles

        It decrements the player life by 1 point

        If it reaches zero, game is over
        """
        collided = pygame.sprite.spritecollide(self.player, self.asteroid_group, False)
        for asteroid in collided:
            radius_combination = self.player.width/2 + asteroid.size/2

            if (self.player.rect.centery+self.player.height/2) > (asteroid.rect.centery-asteroid.size/5)+5:
                distance = get_distance(self.player.rect.centerx, self.player.rect.centery, asteroid.rect.centerx,
                                        asteroid.rect.centery)
                if distance < radius_combination:
                    self.player.hp -= 1
                    pygame.mixer.Sound('assets/sounds/effects/hurt.wav').play()
                    if self.player.hp <= 0:
                        self.over = True

                    asteroid.group.remove(asteroid)

    def toggle_pause(self):
        self.paused = not self.paused

    def end_game(self):
        self.over = True

    def reset(self):
        """Resets the game object values"""
        self.score = 0
        self.asteroid_group = pygame.sprite.Group()
        self.goodies_group = pygame.sprite.Group()
        self.missile_group = pygame.sprite.Group()
        self.over = False
        self.paused = False
        self.player.moving = 0

    def game_over_menu(self):

        """
        Handles game over menu, it returns the player decision regarding the game
        Similar to an interactive while loop
        :return: continue (bool)
        """

        options_manager.save_scores()
        self.game_mixer.stop()
        pygame.mixer.Sound('assets/sounds/effects/gameover.wav').play()
        text = self.title_font.render(options_manager.language_dict.get('gameover'), False, (255, 255, 255))
        y_variation = text.get_height()
        rect = text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - y_variation ))

        # Button instantiation
        restart_button = SquaredButton(self.screen,
                                       coords=(self.screen.get_width() // 2,
                                               100 + self.screen.get_height() // 2 - y_variation),
                                       text=options_manager.language_dict.get('restart'),
                                       font='assets/font/Pixellari.ttf',
                                       size=50, color=(255, 255, 255), bgcolor=(114, 114, 115), bgradius=5,
                                       bdcolor=(255, 255, 255), bdradius=10, hovercolor=(235, 213, 52),
                                       hoverbd=(235, 213, 52),
                                       command=self.reset)

        exit_button = SquaredButton(self.screen,
                                    coords=(self.screen.get_width() // 2,
                                            200 + self.screen.get_height() // 2 - y_variation),
                                    text=options_manager.language_dict.get('quit'),
                                    font='assets/font/Pixellari.ttf',
                                    size=50, color=(255, 255, 255), bgcolor=(114, 114, 115), bgradius=5,
                                    bdcolor=(255, 255, 255), bdradius=10, hovercolor=(235, 213, 52),
                                    hoverbd=(235, 213, 52))

        while self.over is True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.over_screen, (0, 0))
            self.screen.blit(text, rect)
            restart_button.is_inside(mouse_pos)
            restart_button.draw()

            exit_button.is_inside(mouse_pos)
            exit_button.draw()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.over = True
                    if options_manager.settings_dict.get('music') == 'Yes':
                        self.game_mixer.play(-1)
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.is_inside(mouse_pos):
                        if options_manager.settings_dict.get('music') == 'Yes':
                            self.game_mixer.play(-1)
                        return True
                    elif exit_button.is_inside(mouse_pos):
                        if options_manager.settings_dict.get('music') == 'Yes':
                            self.game_mixer.play(-1)
                        return False


            pygame.display.update()
            self.clock.tick(60)

    def paused_menu(self):
        """
        In charge of handling the pause menu
        Contains buttons and text
        """
        self.paused = True
        self.player.moving = 0
        # Button instantiation
        resume_button = SquaredButton(self.screen, coords=(self.screen.get_width()//2, self.screen.get_height()//2),
                                      text=options_manager.language_dict.get('resume'),
                                      font='assets/font/Pixellari.ttf',
                                      size=50, color=(255, 255, 255), bgcolor=(114, 114, 115), bgradius=5,
                                      bdcolor=(255, 255, 255), bdradius=10, hovercolor=(235, 213, 52),
                                      hoverbd=(235, 213, 52),
                                      command=self.toggle_pause)

        restart_button = SquaredButton(self.screen, coords=(self.screen.get_width()//2, 100 +self.screen.get_height()//2),
                                       text=options_manager.language_dict.get('restart'),
                                       font='assets/font/Pixellari.ttf',
                                       size=50, color=(255, 255, 255), bgcolor=(114, 114, 115), bgradius=5,
                                       bdcolor=(255, 255, 255), bdradius=10, hovercolor=(235, 213, 52),
                                       hoverbd=(235, 213, 52),
                                       command=self.reset)

        exit_button = SquaredButton(self.screen, coords=(self.screen.get_width()//2, 200 +self.screen.get_height()//2),
                                    text=options_manager.language_dict.get('quit'),
                                    font='assets/font/Pixellari.ttf',
                                    size=50, color=(255, 255, 255), bgcolor=(114, 114, 115), bgradius=5,
                                    bdcolor=(255, 255, 255), bdradius=10, hovercolor=(235, 213, 52),
                                    hoverbd=(235, 213, 52))

        while self.paused is True:

            mouse_pos = pygame.mouse.get_pos()

            self.screen.blit(self.pause_screen, (0, 0))
            resume_button.is_inside(mouse_pos)
            resume_button.draw()

            restart_button.is_inside(mouse_pos)
            restart_button.draw()

            exit_button.is_inside(mouse_pos)
            exit_button.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or pygame.K_SPACE:
                        self.last_time = time.time()
                        self.paused = False
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.is_inside(mouse_pos) is True:
                        self.last_time = time.time()
                        resume_button.execute()
                    elif restart_button.is_inside(mouse_pos) is True:
                        self.paused = False

                        restart_button.execute()
                        self.last_time = time.time()
                    elif exit_button.is_inside(mouse_pos) is True:
                        self.paused = True
                        self.over = True
                        self.last_time = time.time()
                        return

            pygame.display.update()
            self.clock.tick(60)

##########################################
#                                        #
# CLASSIC GAME MODE                      #
#                                        #
##########################################


class Classic(Game):
    def __init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen):
        Game.__init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen)

    # Game loop
    def game(self):
        """Handles pygame loop: Events and pictures"""

        # Initialize player values depending difficulty
        self.reset()

        distance = 0
        while self.over is False:

            delta = time.time() - self.last_time
            self.last_time = time.time()
            delta *= 60

            # Elements are drawn into the screen
            self.screen.blit(self.background, (0, 0))
            self.drop_asteroids()
            self.check_player_collision()
            self.asteroid_group.update(delta)

            self.draw_asteroids()

            self.missile_group.update(delta)
            self.missile_group.draw(self.screen)
            self.check_missile_collision()

            self.player.update()
            self.drop_goodies()
            self.goodies_group.update(delta)
            self.goodies_group.draw(self.screen)

            self.check_goodie_collision()

            # Event Handling
            for event in pygame.event.get():

                # If player quits return to game mode menu
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:

                    # Control player
                    if event.key == pygame.K_LEFT and (not self.paused):
                        self.player.moving = -2.7
                    if event.key == pygame.K_RIGHT and (not self.paused):
                        self.player.moving = 2.7

                    if event.key == pygame.K_SPACE and (not self.paused):
                        self.player.fire(self.missile_group, self.missile_img)

                    if event.key == pygame.K_ESCAPE:
                        self.paused = True

                if event.type == pygame.KEYUP and (not self.paused):
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.moving = 0

            # Increases distance each 900 iterations
            if self.paused is False:
                if distance == 60:

                    dif = options_manager.settings_dict.get('difficulty').lower()
                    max_score = options_manager.scores_dict.get('classic_' + dif + '_max')

                    self.score += 1
                    if self.score > max_score:
                        options_manager.scores_dict.update([('classic_'+dif+'_max', self.score)])

                    distance = 0
                else:
                    distance += 1

            if self.paused is False:
                self.player.move(delta)


            self.player.draw(self.screen)

            # HUD drawn into screen
            score_string = str(self.score)
            text = self.font.render(options_manager.language_dict.get('distance')+": " + score_string+" km",
                                    False, (255, 255, 255))

            ammo_string = str(self.player.ammo)
            ammo_text = self.font.render(options_manager.language_dict.get('ammo')+": " + ammo_string,
                                         False, (255, 255, 255))
            health_text = self.font.render(options_manager.language_dict.get('hp')+": " + str(self.player.hp),
                                           False, (255, 255, 255))

            dif = options_manager.settings_dict.get('difficulty').lower()
            max_score = options_manager.scores_dict.get('classic_' + dif + '_max')
            record_text = self.font.render('Record: ' + str(max_score), False, (255, 255, 255))

            self.screen.blit(text, (5, 10))
            self.screen.blit(ammo_text, (5, 50))
            self.screen.blit(health_text, (5, 90))
            if self.score < max_score:
                self.screen.blit(record_text, (5, 130))

            if self.paused is True:
                self.paused_menu()

            pygame.display.update()
            self.clock.tick(60)

        # Checks the user decision on whether to keep playing or not
        decision = False
        if self.paused is False:
            decision = self.game_over_menu()

        self.reset()
        if decision is True:
            self.game()

    def reset(self):
        super(Classic, self).reset()
        if options_manager.settings_dict.get('difficulty') == 'Hard':
            self.player.hp = 1
            self.player.ammo = 5
        else:
            self.player.hp = 5
            self.player.ammo = 8
        self.player.x, self.player.y = self.player.orgx, self.player.orgy

##########################################
#                                        #
# ASTRO SAVER GAME MODE                  #
#                                        #
##########################################


class AstroSaver(Game):
    def __init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen, astronaut_img):
        Game.__init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen)
        self.astronaut_group = pygame.sprite.Group()
        self.astronaut_img = astronaut_img

    def check_astronaut_collision(self):
        """Handles player collection of astronaut sprites

        One astronaut collected = 1 point
        """
        collided = pygame.sprite.spritecollide(self.player, self.astronaut_group, False)

        dif = options_manager.settings_dict.get('difficulty').lower()
        max_score = options_manager.scores_dict.get('astrosaver_' + dif + '_max')
        for astronaut in collided:

            self.astronaut_group.remove(astronaut)
            self.score += 1

            pygame.mixer.Sound('assets/sounds/effects/astronaut_pickup.wav').play()
            if self.score > max_score:
                max_score += 1
                options_manager.scores_dict.update([('astrosaver_' + dif + '_max', max_score)])
            break

    def drop_astronauts(self):
        """
        Randomly selects the position and releases an astronaut at the top
        of the screen
        """
        prob = random.randrange(1, 400)

        if prob < 4:
            x_pos = random.randrange(10, self.border_right, 100)
            y_pos = 0
            astronaut = Astronaut(x_pos, y_pos, self.astronaut_img, self.astronaut_group)
            self.astronaut_group.add(astronaut)

    def game(self):
        """Handles pygame loop: Events and pictures"""
        self.reset()

        while self.over is False:

            delta = time.time() - self.last_time
            self.last_time = time.time()
            delta *= 60

            self.screen.blit(self.background, (0, 0))
            self.drop_asteroids()
            self.asteroid_group.update(delta)
            self.draw_asteroids()

            self.missile_group.update(delta)
            self.missile_group.draw(self.screen)
            self.check_missile_collision()

            self.player.update()
            self.drop_goodies()
            self.goodies_group.update(delta)
            self.goodies_group.draw(self.screen)

            self.check_goodie_collision()

            self.drop_astronauts()
            self.astronaut_group.update(delta)
            self.astronaut_group.draw(self.screen)

            self.check_astronaut_collision()
            self.check_player_collision()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.player.moving = -2.7
                    if event.key == pygame.K_RIGHT:
                        self.player.moving = 2.7

                    if event.key == pygame.K_SPACE:
                        self.player.fire(self.missile_group, self.missile_img)

                    if event.key == pygame.K_ESCAPE:
                        self.paused = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.moving = 0

            self.player.move(delta)
            self.player.draw(self.screen)

            # HUD display
            score_string = str(self.score)
            text = self.font.render(options_manager.language_dict.get('score')+': ' + score_string, False, (255, 255, 255))

            ammo_string = str(self.player.ammo)
            ammo_text = self.font.render(options_manager.language_dict.get('ammo')+': '
                                         + ammo_string, False, (255, 255, 255))
            health_text = self.font.render(options_manager.language_dict.get('hp')+': '
                                           + str(self.player.hp), False, (255, 255, 255))

            dif = options_manager.settings_dict.get('difficulty').lower()
            max_score = options_manager.scores_dict.get('astrosaver_' + dif + '_max')
            record_text = self.font.render('Record: ' + str(max_score), False, (255, 255, 255))

            self.screen.blit(text, (5, 10))
            self.screen.blit(ammo_text, (5, 50))
            self.screen.blit(health_text, (5, 90))
            if self.score < max_score:
                self.screen.blit(record_text, (5, 130))

            if self.paused is True:
                self.paused_menu()

            pygame.display.update()
            self.clock.tick(60)

        decision = False
        if self.paused is False:
            decision = self.game_over_menu()

        options_manager.save_scores()
        self.reset()
        if decision is True:
            self.game()

    def reset(self):
        super(AstroSaver, self).reset()
        self.player.x, self.player.y = self.player.orgx, self.player.orgy
        self.astronaut_group = pygame.sprite.Group()

        if options_manager.settings_dict.get('difficulty') == 'Hard':
            self.player.hp = 1
            self.player.ammo = 3
        else:
            self.player.hp = 20
            self.player.ammo = 10

##########################################
#                                        #
# SHOOTER GAME MODE                      #
#                                        #
##########################################


class Shooter(Game):
    def __init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen):
        Game.__init__(self, name, background, asteroid_img, goodies_img, missile_img, player, screen)
        self.max_obstacles = 10

    def check_missile_collision(self):
        """Overridden missile collision handler.
        Each obstacle reached by a missile = 1 point
        """
        dif = options_manager.settings_dict.get('difficulty').lower()
        max_score = options_manager.scores_dict.get('shooter_'+dif+'_max')

        for missile in self.missile_group:
            collided = pygame.sprite.spritecollide(missile, self.asteroid_group, True)
            if len(collided) > 0:
                self.missile_group.remove(missile)
                self.score += 1
                if self.score > max_score:
                    max_score += 1
                    options_manager.scores_dict.update([('shooter_'+dif+'_max', max_score)])
                pygame.mixer.Sound('assets/sounds/effects/explosion.wav').play()

    def game(self):
        """Handles pygame loop: Events and pictures"""

        if options_manager.settings_dict.get('difficulty') == 'Hard':
            self.player.hp = 1
            self.player.ammo = 50
        else:
            self.player.hp = 2
            self.player.ammo = 150

        distance = 0
        while self.over is False:

            delta = time.time() - self.last_time
            self.last_time = time.time()
            delta *= 60

            self.screen.blit(self.background, (0, 0))
            self.drop_asteroids()
            self.check_player_collision()
            self.asteroid_group.update(delta)

            self.draw_asteroids()

            self.missile_group.update(delta)
            self.missile_group.draw(self.screen)
            self.check_missile_collision()

            self.player.update()
            self.drop_goodies()
            self.goodies_group.update(delta)
            self.goodies_group.draw(self.screen)

            self.check_goodie_collision()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset()
                    return

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.player.moving = -2.7
                    if event.key == pygame.K_RIGHT:
                        self.player.moving = 2.7

                    if event.key == pygame.K_SPACE:
                        self.player.fire(self.missile_group, self.missile_img)

                    if event.key == pygame.K_ESCAPE:
                        self.paused = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.moving = 0

            self.player.move(delta)
            self.player.draw(self.screen)

            # HUD display
            score_string = str(self.score)
            text = self.font.render(options_manager.language_dict.get('score')+': ' + score_string,
                                    False, (255, 255, 255)).convert_alpha()

            ammo_string = str(self.player.ammo)
            ammo_text = self.font.render(options_manager.language_dict.get('ammo')+': '+ammo_string,
                                         False, (255, 255, 255)).convert_alpha()
            health_text = self.font.render(options_manager.language_dict.get('hp')+': '+str(self.player.hp),
                                           False, (255, 255, 255)).convert_alpha()

            dif = options_manager.settings_dict.get('difficulty').lower()
            max_score = options_manager.scores_dict.get('shooter_'+dif+'_max')
            record_text = self.font.render('Record: '+str(max_score), False, (255, 255, 255)).convert_alpha()

            self.screen.blit(text, (5, 10))
            self.screen.blit(ammo_text, (5, 50))
            self.screen.blit(health_text, (5, 90))
            if self.score < max_score:
                self.screen.blit(record_text, (5, 130))
            if self.paused is True:
                self.paused_menu()





            pygame.display.update()
            self.clock.tick(60)
            if delta >= 2:
                print(delta)

        decision = False
        if self.paused is False:
            decision = self.game_over_menu()

        self.reset()
        if decision is True:
            self.game()

    def reset(self):
        super(Shooter, self).reset()
        if options_manager.settings_dict.get('difficulty') == 'Hard':
            self.player.hp = 1
            self.player.ammo = 50
        else:
            self.player.hp = 2
            self.player.ammo = 150
        self.player.x, self.player.y = self.player.orgx, self.player.orgy


def get_distance(px, py, ox, oy):
    """Gets distance between two coordinates"""
    return math.sqrt((px-ox)**2 + (py-oy)**2)
