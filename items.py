import pygame
from squares import *

ball_img = pygame.image.load('ball.png')
footballer_img = pygame.image.load('footballer.png')
selected_footballer_img = pygame.image.load('footballer_selected.png')

class Field:
    def __init__(self, coord, footballer_exist, ball_exist):
        self.coord = coord
        self.footballer_exist = footballer_exist
        self.ball_exist = ball_exist
        self.selected = False

    def user_click(self, x, y):
        if x >= self.coord.left and x <= self.coord.right and y <= self.coord.bottom and y >= self.coord.top:
            return True

    def select_field(self):
        x, y = pygame.mouse.get_pos()
        if self.user_click(x, y):

            if self.selected:
                self.selected = False
            else:
                self.selected = True
                return self.coord

    def __str__(self):
        return str(self.coord) + 'footbaler' + str(self.footballer_exist) + 'ball' + str(self.ball_exist) + 'selected:' + str(self.selected)

fields = [Field(i[0], i[1], i[2]) for i in SQUARE_MATRIX]

class Ball(pygame.sprite.Sprite):
    def __init__(self, start_pos, image):
        pygame.sprite.Sprite.__init__(self)
        self.position = start_pos
        self.image = image
        start_pos.ball_exist = True

    def update(self, pos, pre_pos):
        pre_pos.ball_exist = False
        self.position = pos
        pos.ball_exist = True

ball = Ball(fields[34], ball_img)

class Footbaler(pygame.sprite.Sprite):
    def __init__(self, start_pos, regular_image, selected_image):
        pygame.sprite.Sprite.__init__(self)
        self.prev_position = start_pos
        self.position = start_pos
        self.selected = False
        self.regular_image = regular_image
        self.selected_image = selected_image
        self.image = self.regular_image
        self.rect = self.image.get_rect()
        start_pos.footballer_exist = True

    def user_click(self, x, y):
        if x >= self.position.coord.left and x <= self.position.coord.right and y <= self.position.coord.bottom and y >= self.position.coord.top:
            return True

    def select(self):
        x, y = pygame.mouse.get_pos()
        if self.user_click(x, y):
            if self.selected:
                self.selected = False
                self.image = self.regular_image
            else:
                self.selected = True
                self.image = self.selected_image

    def update(self, x, y):
        for new_pos in fields:
            if x >= new_pos.coord.left and x <= new_pos.coord.right and y <= new_pos.coord.bottom and y >= new_pos.coord.top:
                if new_pos.footballer_exist is False:
                    self.prev_position = self.position
                    self.position = new_pos
                    for field in fields:
                        if self.prev_position == field:
                            field.footballer_exist = False
                            if field.ball_exist:
                                print(field)
                                print('fffff')
                                ball.update(new_pos, field)
                        if self.position == field:
                            field.footballer_exist = True
                else:
                    self.selected = False
                    self.image = self.regular_image
                    self.select()

footballer_1 = Footbaler(fields[4], footballer_img, selected_footballer_img)
footballer_2 = Footbaler(fields[15], footballer_img, selected_footballer_img)
footballer_3 = Footbaler(fields[36], footballer_img, selected_footballer_img)

footballers = [footballer_1, footballer_2, footballer_3]

class ImageButton:
    def __init__(self, x, y, text, image, hover_image, func):
        self.x = x
        self.y = y
        self.text = text
        self.image = pygame.image.load(image)
        self.hover_image = pygame.image.load(hover_image)
        self.is_hovered = False
        self.rect = self.image.get_rect(topleft=(x, y))
        self.func = func

    def draw(self, screen):
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (55, 55, 55))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hovered(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event, coord):
        for footballer in footballers:
            if footballer.selected:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
                    if self.func == 'run':
                        footballer.update(coord.centerx, coord.centery)