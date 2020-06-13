import pygame
import random
import math
from pygame import mixer

# initializing game
pygame.init()

# creating screen
screen = pygame.display.set_mode((600, 800))

# Background

background = pygame.image.load('space.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)
# caption and icon
pygame.display.set_caption("Milkyway Cowboy")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('cow.png')
playerX = 0
playerY = 336
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('fish.png'))
    enemyX.append(random.randrange(430, 530))
    enemyY.append(random.randrange(0, 736))
    enemyX_change.append(40)
    enemyY_change.append(4)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 336
bulletX_change = 5
bulletY_change = 0
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250,350))

def show_score(x, y):
    score = over_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullets(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((10, 10, 10))
    # background
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletY = playerY
                    fire_bullets(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 536:
        playerX = 536
    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemyX[i] < 0:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]
        if enemyY[i] <= 0:
            enemyY_change[i] = 4
            enemyX[i] -= enemyX_change[i]
        elif enemyY[i] >= 736:
            enemyY_change[i] = -4
            enemyX[i] -= enemyX_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion = mixer.Sound('explosion.wav')
            explosion.play()
            bulletX = 0
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randrange(430, 530)
            enemyY[i] = random.randrange(0, 736)

        enemy(enemyX[i], enemyY[i], i)
    # bullet movement
    if bulletX >= 600:
        bulletX = 0
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullets(bulletX, bulletY)
        bulletX += bulletX_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
