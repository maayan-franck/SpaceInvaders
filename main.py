import pygame
import random
import math
from pygame import mixer


# Initialize pygame methods
pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('background.png')
# background sound
mixer.music.load('jdog_music_2.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# player data
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# enemy data
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 4

for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2.5)
    enemy_y_change.append(40)

# bullet data
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 6
bullet_state = "ready"  # ready - bullet not on screen.   fire - bullet moving on screen

# score
score_value = 0
score_font = pygame.font.Font("ARCADE.TTF", 50)  # check dafont.com for more fonts
text_x, text_y = 10, 10

# final score
final_score_font = pygame.font.Font("ARCADE.TTF", 64)

# game over text
game_over_font = pygame.font.Font("ARCADE.TTF", 100)

# play again text
play_again_font = pygame.font.Font("ARCADE.TTF", 50)


def display_score(x, y):
    score = score_font.render(f"Score: {str(score_value)}", True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (x, y))


def play_again_text():
    text = play_again_font.render("RE-RUN PROGRAMME TO PLAY AGAIN", True, (0, 250, 0))
    screen.blit(text, (15, 250))


def final_score():
    text = final_score_font.render(f"FINAL SCORE: {str(score_value)}", True, (255, 255, 255))
    screen.blit(text, (180, 300))


def player(x, y):  # player driver function
    screen.blit(player_img, (x, y))


def enemy(x, y, i):  # enemy driver function
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):  # fire bullet driver function --> accessing bullet state and position
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(en_x, en_y, bul_x, bul_y):  # compute distance between bullet and enemy, identify as collision if true
    distance = math.sqrt((en_x-bul_x)**2 + (en_y-bul_y)**2)
    if distance < 30:
        return True
    return False


# creating game loop
running = True
while running:
    # RGB = red, green, blue --> 0-255, check 'color to rgb' for different color codes
    screen.fill((0, 0, 0))  # --> black
    # set background image
    screen.blit(background, (0, 0))
    # check if "QUIT" button has been pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke pressed check - left or right, set player change of position
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:  # running bullet driver func and changing bullet state if space key is hit
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser_bullet_sound.wav")  # playing laser bullet sound
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        # stopping player movement when left or right arrows are released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # applying movement to player according to left\right arrows
    player_x += player_x_change

    # setting player borders
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # bullet movement and state
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # setting enemy movement and borders, and game over
    for i in range(number_of_enemies):
        # game over
        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over_text(185, 150)
            play_again_text()
            final_score()
            break
        # enemy movement
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 6
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -6
            enemy_y[i] += enemy_y_change[i]

        # applying collision implications
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)  # checking for a hit
        if collision:
            # playing explosion sound
            explosion_sound = mixer.Sound("explosion_sound.wav")
            explosion_sound.play()
            # reset bullet position and state, incrementing score, re-spawning enemy
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # calling player and enemy driver functions and updating game loop display
    player(player_x, player_y)
    display_score(text_x, text_y)
    pygame.display.update()


