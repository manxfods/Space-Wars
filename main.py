import pygame
import random
import math
from pygame import mixer

# Initialing the modules
pygame.init()

# Defining the window (Widht, Height)
screen = pygame.display.set_mode((800, 800))

# Defining the title and icon
pygame.display.set_caption("Space Wars")
icon = pygame.image.load('img\\icon.png')
pygame.display.set_icon(icon)

# Defining the background
background = pygame.image.load('img\\background.png')

# Defining the background sound
mixer.music.load('sounds/background.mp3')
mixer.music.play(-1)

# Defining the player
playerSkin = pygame.image.load('img\\player.png')
playerX = 350
playerY = 650
playerX_change = 0


def player(x):
    screen.blit(playerSkin, (x, playerY))


# Defining the enemy
enemySkin = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemySkin.append(pygame.image.load('img\\enemy.png'))
    enemyX.append(random.randint(25, 675))
    enemyY.append(50)
    enemyX_change.append(0.5)
    enemyY_change.append(25)


def enemy(x, y, i):
    screen.blit(enemySkin[i], (x, y))


# Defining bullet skin
bulletSkin = pygame.image.load('img\\bullet.png')
bulletX = 0
bulletY = 650
bulletY_change = 1.5
bullet_state = "ready"


def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletSkin, (x + 25, y + 10))


# Making the colision function
def IsColision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                         (math.pow(enemyY-bulletY, 2)))
    if distance <= 32:
        return True
    else:
        return False


# Display score in the screen
score = 0
font = pygame.font.Font('fonts/pcsenior.ttf', 24)
textX = 32
textY = 16


def display_score(x, y):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))


# Starting the loop to open the window
running = True
while running:

    screen.fill((0, 10, 43))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Checking the keys to movement our player
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -0.5
        if event.key == pygame.K_RIGHT:
            playerX_change = 0.5
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('sounds/shoot.wav')
                bullet_sound.play()
                bulletX = playerX
                fire(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0

    # Limiting the player moviment
    playerX += playerX_change
    if playerX <= 25:
        playerX = 25
    elif playerX >= 675:
        playerX = 675

    # Limiting the enemy moviment
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 25:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 675:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Definig the colision function
        colision_enemy_bullet = IsColision(
            enemyX[i], enemyY[i], bulletX, bulletY)
        if colision_enemy_bullet:
            colision_sound = mixer.Sound('sounds/explosion.wav')
            colision_sound.play()
            enemyX[i] = random.randint(50, 650)
            enemyY[i] = random.randint(50, 150)
            bullet_state = "ready"
            bulletY = 650
            score += 1

        # Generating the enemy
        enemy(enemyX[i], enemyY[i], i)

    # Defining bullet rules to moviment
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 650
    if bullet_state == "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling our functions to creat characters
    player(playerX)
    display_score(textX, textY)
    pygame.display.update()
