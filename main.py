import pygame
import random
import math

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

# Defining the player
playerSkin = pygame.image.load('img\\player.png')
playerX = 350
playerY = 650
playerX_change = 0


def player(x):
    screen.blit(playerSkin, (x, playerY))


# Defining the enemy
enemySkin = pygame.image.load('img\\enemy.png')
enemyX = random.randint(25, 675)
enemyY = 50
enemyX_change = 0.3
enemyY_change = 32


def enemy(x, y):
    screen.blit(enemySkin, (x, y))


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
    if distance <= 25:
        return True
    else:
        return False


score = 0
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
            if bullet_state is "ready":
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
    enemyX += enemyX_change
    if enemyX <= 25:
        enemyX_change = 0.3
        enemyY += enemyY_change
    elif enemyX >= 675:
        enemyX_change = -0.3
        enemyY += enemyY_change

    # Definig the colision function
    colision = IsColision(enemyX, enemyY, bulletX, bulletY)
    if colision:
        enemyX = random.randint(50, 650)
        enemyY = random.randint(50, 150)
        bullet_state = "ready"
        bulletY = 650
        score += 1
        print(score)

    # Defining bullet rules to moviment
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 650
    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling our functions to creat characters
    player(playerX)
    enemy(enemyX, enemyY)
    pygame.display.update()
