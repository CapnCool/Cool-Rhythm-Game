import os
import pygame
from random import randint
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cool Rhythm Game')
pygame.display.set_icon(pygame.image.load(os.path.join('Sprites', 'icon.png')))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ARROW_EMPTY_IMG = pygame.image.load(os.path.join('Sprites', 'Arrow_empty.png'))
ARROW_EMPTY_IMG = pygame.transform.scale(ARROW_EMPTY_IMG, (64, 64))

header_font = pygame.font.Font(os.path.join('Fonts', '8-bit_wonder.ttf'), 40)
button_font = pygame.font.Font(os.path.join('Fonts', '8-bit_wonder.ttf'), 25)
score_font = pygame.font.Font(os.path.join('Fonts', 'arcadeclassic.ttf'), 20)

score = 0
id_0, id_1, id_2, id_3 = 0, 0, 0, 0
id_0_list, id_1_list, id_2_list, id_3_list = [], [], [], []

note_time = []


# creating sprites
class Arrow(pygame.sprite.Sprite):
    def __init__(self, color: int, angle: int):
        pygame.sprite.Sprite.__init__(self)
        position = [-50, -150, 50, 150]
        global id_0, id_1, id_2, id_3

        arrow_img = pygame.image.load(os.path.join('Sprites', f'Arrow_{color}.png'))
        arrow_img = pygame.transform.scale(arrow_img, (64, 64))

        self.frames = []
        self.frames.append(pygame.transform.rotate(arrow_img, 90 * angle))
        self.frames.append((pygame.image.load(os.path.join('Sprites', 'Animations', f'boom_f1_{color}.png'))))
        self.frames.append((pygame.image.load(os.path.join('Sprites', 'Animations', f'boom_f2_{color}.png'))))
        self.frames.append((pygame.image.load(os.path.join('Sprites', 'Animations', f'boom_f3_{color}.png'))))

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()

        self.rect.centerx = WIDTH // 2 + position[angle]
        self.rect.centery = -10

        self.x_pos_2 = self.rect.centerx - 80
        self.y_pos_2 = 0

        self.text_x = self.rect.centerx + 32
        self.text_y = 540 - 64

        self.type = angle
        self.speed = 7.5

        self.animate = False

        if angle == 0:
            self.id = id_0
            id_0_list.append(self.id)
            id_0 += 1
        elif angle == 1:
            self.id = id_1
            id_1_list.append(self.id)
            id_1 += 1
        elif angle == 2:
            self.id = id_2
            id_2_list.append(self.id)
            id_2 += 1
        elif angle == 3:
            self.id = id_3
            id_3_list.append(self.id)
            id_3 += 1

    def update(self):
        global score
        global keypress_w, keypress_a, keypress_s, keypress_d
        position = [-50, -150, 50, 150]

        if self.animate:
            if self.current_frame < len(self.frames) - 1:
                self.current_frame += .25

            else:
                self.kill()

            self.image = self.frames[int(self.current_frame)]
            self.rect.centerx = self.x_pos_2
            self.rect.centery = self.y_pos_2

        else:
            self.rect.centery += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            if self.type == 0:
                id_0_list.remove(self.id)
            elif self.type == 1:
                id_1_list.remove(self.id)
            elif self.type == 2:
                id_2_list.remove(self.id)
            elif self.type == 3:
                id_3_list.remove(self.id)

        if self.type == 0:
            if id_0_list and self.id == min(id_0_list):
                if keypress_w:
                    keypress_w = False
                    id_0_list.remove(self.id)
                    if pygame.sprite.spritecollide(self, empty_sprites, False):
                        score += 1
                        self.animate = True
                        self.current_frame += 1
                        self.y_pos_2 = self.rect.centery - 64
                    else:
                        self.kill()

        if self.type == 1:
            if id_1_list and self.id == min(id_1_list):
                if keypress_a:
                    keypress_a = False
                    id_1_list.remove(self.id)
                    if pygame.sprite.spritecollide(self, empty_sprites, False):
                        score += 1
                        self.animate = True
                        self.current_frame += 1
                        self.y_pos_2 = self.rect.centery - 64
                    else:
                        self.kill()

        if self.type == 2:
            if id_2_list and self.id == min(id_2_list):
                if keypress_s:
                    keypress_s = False
                    id_2_list.remove(self.id)
                    if pygame.sprite.spritecollide(self, empty_sprites, False):
                        score += 1
                        self.animate = True
                        self.current_frame += 1
                        self.y_pos_2 = self.rect.centery - 64
                    else:
                        self.kill()

        if self.type == 3:
            if id_3_list and self.id == min(id_3_list):
                if keypress_d:
                    keypress_d = False
                    id_3_list.remove(self.id)
                    if pygame.sprite.spritecollide(self, empty_sprites, False):
                        score += 1
                        self.animate = True
                        self.current_frame += 1
                        self.y_pos_2 = self.rect.centery - 64
                    else:
                        self.kill()


class ArrowEmpty(pygame.sprite.Sprite):
    def __init__(self, angle: int, position: int):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.rotate(ARROW_EMPTY_IMG, 90 * angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2 + position
        self.rect.bottom = 540

    def update(self):
        pass

def play_song(file_name: str):
    global note_times
    note_times = []
    with open(os.path.join('Audio', f'{file_name}.txt'), 'r') as file:
        for line in file:
            line_list = (line.strip()).split()
            note_times.append(int(line_list[0]) * 60 * 1000 + int(line_list[1]) * 1000 + int(line_list[2]))

    pygame.mixer.music.load(os.path.join('Audio', f'{file_name}.mp3'))
    pygame.mixer.music.play()


FPS = 60

empty_sprites = pygame.sprite.Group(ArrowEmpty(1, -150), ArrowEmpty(0, -50), ArrowEmpty(2, 50), ArrowEmpty(3, 150))
moving_sprites = pygame.sprite.Group()


def game_loop(level: int):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True
    songs = ['moonlight_sonata', 'solitude', 'demons_on_the_beach']

    play_song(songs[level - 1])
    while run:
        global keypress_w, keypress_a, keypress_s, keypress_d
        keypress_w = False
        keypress_a = False
        keypress_s = False
        keypress_d = False
        elapsed_time = pygame.time.get_ticks() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    keypress_w = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    keypress_s = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    keypress_a = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    keypress_d = True
        WINDOW.blit(pygame.image.load(os.path.join('Sprites', 'backgrounds', f'background_{level}.png')), (0, 0))
        if note_times:
            if elapsed_time + 16 > note_times[0] > elapsed_time - 16:
                moving_sprites.add(Arrow(level, randint(0, 3)))
                note_times.pop(0)
        else:
            if not pygame.mixer.music.get_busy():
                run = False


        # updates
        empty_sprites.update()
        moving_sprites.update()

        # draws
        empty_sprites.draw(WINDOW)
        moving_sprites.draw(WINDOW)

        WINDOW.blit(score_font.render('score {}'.format(score), True, WHITE), (0, 0))

        # update display
        pygame.display.update()

        clock.tick(FPS)


def main_menu():
    menu = True
    while menu:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        WINDOW.fill(BLACK)
        WINDOW.blit(header_font.render('COOL RHYTHM GAME', True, (0, 255, 0)), (WIDTH // 2 - 300, 100))

        mx, my = pygame.mouse.get_pos()


        start_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        credits_button = pygame.Rect(WIDTH // 2 - 100, 375, 200, 50)

        if start_button.collidepoint((mx, my)):
            if click:
                levels()
        if credits_button.collidepoint((mx, my)):
            if click:
                credits()


        pygame.draw.rect(WINDOW, (0, 0, 0), start_button)
        pygame.draw.rect(WINDOW, (0, 0, 0), credits_button)

        WINDOW.blit(button_font.render('PLAY', True, (0, 255, 0)), (WIDTH // 2 - 75, 300))
        WINDOW.blit(button_font.render('CREDITS', True, (0, 255, 0)), (WIDTH // 2 - 100, 375))

        pygame.display.update()

def levels():
    levels = True
    while levels:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                levels = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        WINDOW.fill(BLACK)

        mx, my = pygame.mouse.get_pos()

        one_button = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        two_button = pygame.Rect(WIDTH // 2 - 100, 375, 200, 50)
        three_button = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)

        if one_button.collidepoint((mx, my)):
            if click:
                game_loop(1)
                score = 0
        if two_button.collidepoint((mx, my)):
            if click:
                game_loop(2)
                score = 0
        if three_button.collidepoint((mx, my)):
            if click:
                game_loop(3)
                score = 0

        WINDOW.blit(header_font.render('LEVELS', True, (0, 255, 0)), (WIDTH // 2 - 115, 100))

        pygame.draw.rect(WINDOW, (0, 0, 0), one_button)
        pygame.draw.rect(WINDOW, (0, 0, 0), two_button)
        pygame.draw.rect(WINDOW, (0, 0, 0), three_button)

        WINDOW.blit(button_font.render('LEVEL 1', True, (0, 255, 0)), (WIDTH // 2 - 75, 300))
        WINDOW.blit(button_font.render('LEVEL 2', True, (0, 255, 0)), (WIDTH // 2 - 75, 375))
        WINDOW.blit(button_font.render('LEVEL 3', True, (0, 255, 0)), (WIDTH // 2 - 75, 450))

        pygame.display.update()

def credits():
    credits = True
    while credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                credits = False

        WINDOW.fill(BLACK)
        WINDOW.blit(button_font.render('MUSIC', True, (WHITE)), (10, 100))
        WINDOW.blit(score_font.render('Primal Light - http://primallightmusic.bandcamp.com/releases', True, (WHITE)), (10, 175))
        pygame.display.update()



if __name__ == '__main__':
    main_menu()

pygame.quit()
