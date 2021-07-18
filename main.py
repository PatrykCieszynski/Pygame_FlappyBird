import pygame
from sys import exit
from random import randint


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_fly_1 = pygame.image.load('sprites/yellowbird-midflap.png').convert_alpha()
        bird_fly_1 = pygame.transform.rotozoom(bird_fly_1, 0, 1.5)
        bird_fly_2 = pygame.image.load('sprites/yellowbird-downflap.png').convert_alpha()
        bird_fly_2 = pygame.transform.rotozoom(bird_fly_2, 0, 1.5)
        bird_fly_3 = pygame.image.load('sprites/yellowbird-upflap.png').convert_alpha()
        bird_fly_3 = pygame.transform.rotozoom(bird_fly_3, 0, 1.5)
        self.bird_fly = [bird_fly_1, bird_fly_2, bird_fly_1, bird_fly_3]
        self.bird_index = 0
        self.image = self.bird_fly[self.bird_index]
        self.rect = self.image.get_rect(center=(80, 300))
        self.rect = pygame.Rect.inflate(self.rect, -5, -5)
        self.gravity = 0
        self.rotation = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.MOUSEBUTTONDOWN]) and self.gravity > -3:
            self.gravity = -10
            wing_sound.play()
            wing_sound.set_volume(0.10)

    def apply_gravity(self):
        if self.gravity < 20:
            self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.y >= 680:
            self.rect.y = 680

    def animation(self):
        if game_active == 1:
            self.bird_index += 0.1
            if self.bird_index >= len(self.bird_fly): self.bird_index = 0
            self.image = self.bird_fly[int(self.bird_index)]
        else:
            self.image = self.bird_fly[0]

    def rotate(self):
        if self.gravity <= 0:
            if self.rotation < 30:
                self.rotation += 4
        elif self.gravity >= 0:
            if self.rotation > -90:
                self.rotation -= 3
        self.image = pygame.transform.rotozoom(self.image, self.rotation, 1)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()
        self.rotate()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y_pos, enemy_type):
        super().__init__()
        self.image = pygame.image.load('sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.8)
        if enemy_type == "normal":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center=(500, y_pos))
        else:
            self.rect = self.image.get_rect(center=(500, y_pos))

    def move(self):
        self.rect.x -= 4

    def update(self):
        self.move()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class ScoreHitbox(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites/test.png').convert_alpha()
        self.rect = self.image.get_rect(center=(80, 0))


def collision():
    if bird.sprite.rect.y >= 670:
        collision_sound.play()
        collision_sound.set_volume(0.10)
        return False
    elif pygame.sprite.spritecollide(bird.sprite, pipe_group, False):
        collision_sound.play()
        collision_sound.set_volume(0.10)
        die_sound.play()
        die_sound.set_volume(0.15)
        return False
    else:
        return True


def draw_score(gamestate):
    game_font = pygame.font.SysFont('Arial', 40)
    if gamestate == 1:
        score_surf = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(216, 80))
        screen.blit(score_surf, score_rect)
    if gamestate == 0 or gamestate == -1:
        score_surf = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(216, 80))
        screen.blit(score_surf, score_rect)
        highscore_surf = game_font.render(F' High score: {int(highscore)}', True, (255, 255, 255))
        highscore_rect = highscore_surf.get_rect(center=(216, 600))
        screen.blit(highscore_surf, highscore_rect)


def update_score(score, highscore):
    if score > highscore:
        highscore = score
    return highscore


pygame.init()

# Variables
DEFAULT_WIDTH = 432
DEFAULT_HEIGHT = 768
DEFAULT_FPS = 60
score = 0
highscore = 0
screen = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT))
clock = pygame.time.Clock()
game_active = -1
flag = False
time = 0

# Music
collision_sound = pygame.mixer.Sound('audio/hit.ogg')
die_sound = pygame.mixer.Sound('audio/die.ogg')
point_sound = pygame.mixer.Sound('audio/point.ogg')
swoosh_sound = pygame.mixer.Sound('audio/swoosh.ogg')
wing_sound = pygame.mixer.Sound('audio/wing.ogg')

pygame.display.set_caption('FlappyBird')

# Backgrounds
sky_surf = pygame.image.load('sprites/background-day.png').convert()
sky_surf = pygame.transform.rotozoom(sky_surf, 0, 1.5)
ground_surf = pygame.image.load('sprites/base-extended.png').convert()
ground_rect = ground_surf.get_rect(topleft=(0, 700))
banner_surf = pygame.image.load('sprites/message.png').convert_alpha()
banner_surf = pygame.transform.rotozoom(banner_surf, 0, 1.5)

# Group
bird = pygame.sprite.GroupSingle(Bird())
pipe_group = pygame.sprite.Group()
score_hitbox = pygame.sprite.GroupSingle(ScoreHitbox())

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active == -1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.rect.y = 300
                score = 0
                pipe_group.empty()
                game_active = 1
        if game_active == 0:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.sprite.rect.y = 300
                score = 0
                pipe_group.empty()
                game_active = -1
        if game_active == 1:
            if event.type == obstacle_timer:
                pos = randint(-260, 260)
                pipe_group.add(Obstacle(pos, 'normal'))
                pipe_group.add(Obstacle(pos + 730, 'reverse'))

    # Backgrounds
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, ground_rect)

    if game_active == -1:
        draw_score(game_active)
        ground_rect.x -= 4
        if ground_rect.x < 0 - ground_surf.get_width() / 3:
            ground_rect.x = 0
        screen.blit(banner_surf, (DEFAULT_WIDTH/6, DEFAULT_HEIGHT/5))

    if game_active == 1:
        ground_rect.x -= 4
        if ground_rect.x < 0 - ground_surf.get_width() / 3:
            ground_rect.x = 0

        # Obstacle
        pipe_group.draw(screen)
        pipe_group.update()

        # Bird
        bird.draw(screen)
        game_active = collision()
        bird.update()

        # Score
        draw_score(game_active)
        score_hitbox.draw(screen)
        if pygame.sprite.spritecollide(score_hitbox.sprite, pipe_group, False) and flag is False:
            score += 1
            flag = True
            time = pygame.time.get_ticks()
        if flag is True and pygame.time.get_ticks() - time >= 2000:
            flag = False

    elif game_active == 0:
        pipe_group.draw(screen)
        bird.draw(screen)
        bird.update()
        draw_score(game_active)
        highscore = update_score(score, highscore)
        pygame.time.delay(-1)

    pygame.display.update()
    clock.tick(DEFAULT_FPS)
