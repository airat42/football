import pygame, sys
from squares import *
from pygame.locals import *
from items import *


WIDTH = 1600
HEIGHT = 900
FPS = 60
POWERUP_TIME = 5000

field_img = pygame.image.load('field.png')
selected_field = pygame.image.load('field_selected.png')
variable_field = pygame.image.load('variable.png')

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def update_footballers_img(footballer):
    screen.blit(footballer.image, (footballer.position.coord.left, footballer.position.coord.top))

def update_field_img(field):
    if field.selected:
        screen.blit(selected_field, field.coord)
    elif field.footballer_exist:
        screen.blit(variable_field, field.coord)

def main_menu():
    done = False
    coord_to_step = None
    pass_button = ImageButton(300, 700, 'Пас', 'button.png', 'button_hovered.png', 'pass')
    run_button = ImageButton(500, 700, 'Переместиться', 'button.png', 'button_hovered.png', 'run')
    shot_button = ImageButton(700, 700, 'Удар', 'button.png', 'button_hovered.png', 'shot')
    long_button = ImageButton(900, 700, 'Навес', 'button.png', 'button_hovered.png', 'long')
    dribling_button = ImageButton(1100, 700, 'Дриблинг', 'button.png', 'button_hovered.png', 'dribling')
    buttons = [pass_button, run_button, shot_button, long_button, dribling_button]
    while not done:
        screen.fill((100, 100, 100))
        screen.blit(field_img, (SCREEN_DIV, 0))
        screen.blit(ball.image, (ball.position.coord.centerx, ball.position.coord.centery))
        for field in fields:
            update_field_img(field)
        for btn in buttons:
            btn.check_hovered(pygame.mouse.get_pos())
            btn.draw(screen)
        for footballer in footballers:
            update_footballers_img(footballer)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == MOUSEBUTTONDOWN:
                for footballer in footballers:
                    if footballer.selected:
                        if coord_to_step:
                            break
                        for field in fields:
                            if field.footballer_exist:
                                screen.blit(variable_field, field.coord)
                            coord_to_step = field.select_field()
                            if coord_to_step:
                                field_to_step = field
                                break
                    else:
                        footballer.select()
            if coord_to_step:
                if event.type == pygame.USEREVENT and event.button == run_button:
                    for footballer in footballers:
                        if footballer.selected:
                            footballer.update(coord_to_step.centerx, coord_to_step.centery)
                            footballer.selected = False
                            footballer.image = footballer.regular_image
                            coord_to_step = None
                            update_footballers_img(footballer)
                            field_to_step.selected = False
                            break

                for btn in buttons:
                    btn.handle_event(event, coord_to_step)

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()