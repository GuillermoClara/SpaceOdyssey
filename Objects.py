import pygame
import random


class Asteroid(pygame.sprite.Sprite):
    """
    Sprite used as the obstacles
    Has an update method to update
    its position as time passes
    """
    def __init__(self, x, y, image, size, group):
        super().__init__()
        self.size = size
        self.image = pygame.transform.scale(image, (size, size))

        angle = random.randrange(0, 180)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.height = int(self.image.get_height())
        self.width = int(self.image.get_width())
        self.image = pygame.transform.rotate(self.image, angle)
        new_size = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.size = size*size/new_size
        self.x = x
        self.y = y

        self.group = group

    def update(self, dt=1):
        """
        Updates the y coordinate position.
        If it reaches the bottom of the screen
        it removes the Sprite
        """
        self.y += 5.5*dt
        self.rect.center = [self.x+self.width/2, self.y+self.height/2]
        if self.y >= 600:
            self.group.remove(self)


class Missile(pygame.sprite.Sprite):
    """
    Sprite used as a projectile to destroy obstacles
    Includes an update method to update its position
    """
    def __init__(self, x, y, image, group):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.group = group

    def update(self, dt=1):
        """
        Updates the y coordinate position
        If the y coordinate reaches the top of the screen
        it removes the Sprite
        """
        self.y -= 4*dt
        self.rect.center = [self.x, self.y]
        if self.y <= 0:
            self.group.remove(self)


class Goodie(pygame.sprite.Sprite):
    """
    Sprite used as ammo boxes for the player
    Includes an update method to update its
    position as time passes
    """
    def __init__(self, x, y, image, group):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()
        self.group = group

    def update(self, dt=1):
        """Updates object's position in y positive direction
        If the position is greater than the screen height, it
        removes the sprite
        """
        self.y += 2*dt
        self.rect.center = [self.x, self.y]
        if self.y >= 600:
            self.group.remove(self)


class Astronaut(pygame.sprite.Sprite):
    """
    Collectible Sprite. Similar to Goodies but
    they add to score instead of ammo
    """
    def __init__(self, x, y, image, group):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image
        angle = random.randrange(0, 180)
        self.image = pygame.transform.rotate(self.image, angle)
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.group = group

    def update(self, dt=1):
        """
        Updates the sprite y coordinate and its image center
        If the y coordinate becomes greater than the height of the screen
        the sprite is removed
        """
        self.y += 2*dt
        self.rect.center = [self.x+self.width/2, self.y+self.height/2]
        if self.y >= 600:
            self.group.remove(self)


class Player(pygame.sprite.Sprite):
    """
    Sprite controlled by the player
    Contains actions such as move and fire
    """
    def __init__(self, posx, posy, img1, img2, img3):
        super().__init__()

        self.ammo = 3
        self.lives = 3

        self.size = 64

        self.moving = 0

        self.images = []
        self.images.append(img1)
        self.images.append(img2)
        self.images.append(img3)
        self.index = 0
        self.image = self.images[self.index]
        self.count = 0

        self.rect = self.image.get_rect()
        self.height = int(self.image.get_height())
        self.width = int(self.image.get_width())
        self.hp = 100

        self.orgx = posx
        self.orgy = posy

        self.x = posx
        self.y = posy

    def update(self):
        """
        Updates the Sprite center coordinates.
        Also manages the different sprite animations
        """
        self.rect.center = [self.x+self.width/2, self.y+self.height/2]

        self.count += 1

        if self.count >= 10:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.count = 0
            self.image = self.images[self.index]

    def move(self, dt=1):
        """
        Handles player movement
        """
        self.x += self.moving*dt
        if self.moving > 0:
            if self.x >= 740:
                self.x = 740
        else:
            if self.x <= 0:
                self.x = 0

    def draw(self, screen):
        """
        Draws the sprite into the screen
        using current x and y coordinates
        :param screen: screen
        """
        screen.blit(self.image, (self.x, self.y))

    def fire(self, group, projectile_img):
        """
        Fires a missile from the player position.
        It is then added to the missile Sprite group
        :param group: missiles group
        :param projectile_img: image
        """
        if self.ammo > 0:
            missile = Missile(self.x+self.size/2 + 5, self.y, projectile_img, group)
            group.add(missile)
            pygame.mixer.Sound('assets/sounds/effects/shoot.wav').play()
            self.ammo -= 1
