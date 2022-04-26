import random

import pygame
import options_manager


class DemoBox:
    """Widget designed to present a preview of a game mode.
    Includes a snapshot of the game, a description and a title
    """
    def __init__(self, name, screen, image, x, y, text, font):
        self.name = name
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.rectangle = pygame.rect.Rect(x-5, y-5, (self.image.get_width()+10), self.image.get_height()+10)
        self.text = text
        self.font = font
        self.inside = False

    def check_inside(self, pos):
        """
        Detects if the cursor of the mouse is inside the widget
        Depending on coder preference, it will change the button appearance
        :param pos: mouse position (tuple)
        :return: bool
        """
        if pos[0] in range(self.rectangle.left, self.rectangle.right) and pos[1] in range(self.rectangle.top, self.rectangle.bottom):
            self.inside = True
            text_img = self.font.render(self.text, False, (255, 255, 255))
            text_rect = text_img.get_rect(center=(self.screen.get_width()/2, self.screen.get_height()-self.screen.get_height()/5))
            self.screen.blit(text_img, text_rect)
            return True
        else:
            self.inside = False

            return False

    def draw(self):
        """
        Draws the widget into the screen
        Depending on coder preferences, if it is hovered
        its appearance is different
        """
        if self.inside is True:
            pygame.draw.rect(self.screen, (235, 213, 52), self.rectangle)
            text_img = self.font.render(self.name, False, (235, 213, 52))
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), self.rectangle)
            text_img = self.font.render(self.name, False, (255, 255, 255))
        self.screen.blit(self.image, (self.x, self.y))

        text_rect = text_img.get_rect(center=(self.rectangle.left+self.rectangle.width/2, self.rectangle.top-10))
        self.screen.blit(text_img, text_rect)


class Button:
    """
    Widget in charge of receiving user clicks as an option
    Depending on coder choice, it can be an image or a text button
    """
    def __init__(self, screen, text, x, y, font_path=None, font_size=None, command=None, image=None, activeimg=None):
        self.screen = screen
        self.text = text
        self.image = image
        self.activeimg = activeimg
        if font_path is not None and font_size is not None:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font('assets/font/Pixellari.ttf', 10)
        if image is None:
            self.image = self.font.render(text, False, (255, 255, 255))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.rectangle = pygame.rect.Rect(x, y, (self.image.get_width()), self.image.get_height())
        self.rectangle.center = [self.x, self.y]
        self.command = command
        self.inside = False

    def is_inside(self, pos):
        """
        Checks if the mouse cursor is inside the widgets area
        If preferred by the coder, the widget appearance can change when hovered
        :param pos: mouse position (tuple)
        :return: bool
        """
        if pos[0] in range(self.rectangle.left, self.rectangle.right) and pos[1] in range(self.rectangle.top, self.rectangle.bottom):
            if self.text != '':
                self.image = self.font.render(self.text, False, (235, 213, 52))
            self.inside = True
            return True
        else:
            if self.text != '':
                self.image = self.font.render(self.text, False, (255, 255, 255))
            self.inside = False
            return False

    def draw(self):
        """
        Draws the widget into the screen
        """
        if self.text != '':
            self.screen.blit(self.image, self.rectangle)
        else:
            if self.image is not None and self.activeimg is not None:
                if self.inside:
                    self.screen.blit(self.activeimg, self.rectangle)
                else:
                    self.screen.blit(self.image, self.rectangle)

    def execute(self):
        """Execute the command when button is pressed"""
        if self.command is not None:
            self.command()

    def update(self):
        """Updates the widgets position and rectangle area
        Useful when changing position of widget
        """

        self.rectangle.center = [self.x, self.y]


class SquaredButton:
    """
    Special text button with optional background and border
    """
    def __init__(self, screen, coords, text, font=None, size=None
                 , color=(255, 255, 255), bgcolor=None, bgradius=0, bdcolor=None, bdradius=0
                 , hovercolor=None, hoverbg=None, hoverbd=None, command=None):
        self.screen = screen
        self.x = coords[0]
        self.y = coords[1]
        self.text = text
        if font is not None and size is not None:
            self.font = pygame.font.Font(font, size)
        else:
            self.font = pygame.font.Font('assets/font/Pixellari.ttf', 10)
        self.color = color
        self.bgcolor = bgcolor
        self.bgradius = bgradius
        self.border_color = bdcolor
        self.border_radius = bdradius

        self.hovercolor= hovercolor
        if hovercolor is None:
            self.hovercolor= color

        self.hoverbg = hoverbg
        if hoverbg is None:
            self.hoverbg = self.bgcolor

        self.hoverbd = hoverbd
        if hoverbd is None:
            self.hoverbd = self.border_color

        self.text_image = self.font.render(self.text, False, self.color)
        self.button_area = pygame.rect.Rect(self.x + (self.border_radius+self.bgradius)//2,
                                            self.y + (self.border_radius+self.bgradius)//2,
                                            self.text_image.get_width() + self.border_radius + self.bgradius,
                                            self.text_image.get_height() + self.border_radius + self.bgradius)

        self.button_region = pygame.rect.Rect(0, 0, self.button_area.width, self.button_area.height)
        self.button_region.center = [self.x, self.y]
        self.inside = False
        self.command = command

    def is_inside(self, pos):
        """
        Checks if the mouse cursor is inside the widgets area
        If preferred by the coder, the widget appearance can change when hovered
        :param pos: mouse position (tuple)
        :return: bool
        """
        if pos[0] in range(self.button_region.left, self.button_region.right) and pos[1] in range(self.button_region.top,self.button_region.bottom):
            self.text_image = self.font.render(self.text, False, self.hovercolor)
            self.inside = True
            return True
        else:
            self.text_image = self.font.render(self.text, False, self.color)
            self.inside = False
            return False

    def draw(self):
        """
        Draws the widget into the screen.
        If specified by coder, the widget appearance changes if hovered or clicked
        """
        rect = pygame.surface.Surface((self.button_area.width, self.button_area.height))
        if self.border_color is not None:
            if self.inside is False:
                rect.fill(self.border_color)
            else:
                rect.fill(self.hoverbd)
        else:
            rect.fill((0, 0, 0))
            rect.set_alpha(0)       # If color is omitted, make it transparent

        bg_rect = pygame.surface.Surface((self.button_area.width-self.border_radius,
                                             self.button_area.height-self.border_radius))
        rec = bg_rect.get_rect(center=(rect.get_width()-rect.get_width()//2, rect.get_height()-rect.get_height()//2))

        if self.bgcolor is not None:
            if self.inside is False:
                bg_rect.fill(self.bgcolor)
            else:
                bg_rect.fill(self.hoverbg)

        if self.bgcolor is None:
            if self.border_color is not None:
                random_color = get_random_color(self.border_color)
                bg_rect.fill(random_color)
                rect.blit(bg_rect, rec)
                rect.set_colorkey(random_color)
        else:
            rect.blit(bg_rect, rec)

        self.screen.blit(rect, self.button_region)

        text_rect = self.text_image.get_rect(center=(self.button_region.left+self.button_region.width//2,
                                                     self.button_region.top+self.button_region.height//2))

        self.screen.blit(self.text_image, text_rect)

    def execute(self):
        """Execute the command when button is pressed"""
        if self.command is not None:
            self.command()


class Label:
    def __init__(self, screen, text, x=0, y=0, value=None, color=(255, 255, 255), image=None, font_path=None, font_size=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.text = text
        self.value = value
        self.image = image
        self.color = color
        if font_path is not None and font_size is not None:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.Font('assets/font/Pixellari.ttf', 10)
        if self.image is None:
            self.image = self.font.render(self.text, False, color)


class CircularOptions:
    """Widget designed to hold a group of options
    It works similar to a circular buffer

    It can handle both text and images

    Uses two buttons to navigate options
    """
    def __init__(self, screen, x, y, width, height, title=None, bdradius=10, bleft=None, bright=None, font=None, size=10,
                 title_distance = 10):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = []
        self.current_index = 0
        self.current_option = None
        self.rect_area = pygame.rect.Rect(0, 0, width, height)
        self.rect_area.center = [x, y]
        self.title = title
        if font is None:
            self.font = pygame.font.Font('assets/font/Pixellari.ttf', size)
        else:
            self.font = pygame.font.Font(font, size)
        self.size = size

        self.button_left = bleft
        self.button_right = bright
        self.bd_radius = min(bdradius, self.width)
        self.title_distance = title_distance

        # Scaling buttons to widget's size
        if self.button_left is not None:
            self.button_left.command = self.go_left
            self.button_left.width = self.width*self.button_left.width//self.button_left.screen.get_width()
            self.button_left.height = self.height*self.button_left.height//self.button_left.screen.get_height()
            self.button_left.screen = self.screen

        if self.button_right is not None:
            self.button_right.command = self.go_right
            self.button_right.width = self.width*self.button_right.width//self.button_right.screen.get_width()
            self.button_right.height = self.height*self.button_right.height//self.button_right.screen.get_height()
            self.button_right.screen = self.screen

        self.button_left.x = self.x-bdradius-self.button_left.width//2
        self.button_left.y = self.y

        self.button_right.x = self.x+bdradius+self.button_right.width//2
        self.button_right.y = self.y

    def go_left(self):
        """Go to the left option"""
        if len(self.options) > 0:
            if self.current_index == 0:
                self.current_index = len(self.options)-1
            else:
                self.current_index -= 1
            self.current_option = self.options[self.current_index]

    def go_right(self):
        """Go to the right option"""
        if len(self.options) > 0:
            if self.current_index == (len(self.options)-1):
                self.current_index = 0
            else:
                self.current_index += 1
            self.current_option = self.options[self.current_index]

    def check_buttons(self, pos):
        """Checks if one of the two navigation buttons are being hovered
        :return: bool
        """
        if self.button_right is not None:
            if self.button_right.is_inside(pos):
                self.button_right.execute()
                return True

        if self.button_left is not None:
            if self.button_left.is_inside(pos):
                self.button_left.execute()
                return True
        return False

    def draw(self):
        """
        Draws the widget into the screen
        """

        if self.current_option is None:
            return

        self.button_left.draw()

        current_option = self.current_option
        if type(current_option) is str:
            translation = options_manager.language_dict.get(current_option.lower())

            if translation is not None:
                current_option = self.font.render(translation, False, (255, 255, 255))
            else:
                current_option = self.font.render(current_option, False, (255, 255, 255))

        current_option_rect = current_option.get_rect(center=(self.x, self.y))
        self.screen.blit(current_option, current_option_rect)

        if self.title is not None:
            title_img = self.font.render(self.title, False, (255, 255, 255))
            title_rect = title_img.get_rect(center=(self.x, self.rect_area.top-title_img.get_height()//2
                                                    - self.title_distance))
            self.screen.blit(title_img, title_rect)

        self.button_right.draw()

    def init_option(self, option):
        """
        Initializes the option specified by input.
        :param option: option (string or image)
        :return:
        """
        index = self.options.index(option)
        self.current_option = option
        self.current_index = index
        self.button_left.update()
        self.button_right.update()


def get_random_color(compare=None):
    """Generates a random RGB color. If compare color is provided, it will search a color that is different to input"""
    v1, v2, v3 = random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)
    color = (v1, v2, v3)
    if compare is not None:
        if color == compare:
            return get_random_color(compare)
        else:
            return color
    else:
        return color
