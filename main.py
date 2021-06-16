import pygame
from pygame import mixer
import random
import math

# Initializing PyGame
pygame.init()

# Creating game screen (game window/surface)
screen = pygame.display.set_mode((800, 600))  # width: 800px, height: 600px

# Changing default game window title:
pygame.display.set_caption("Space Invaders 2")

# Setting background image:
# Image attribution: www.wallpaperscraft.com
background = pygame.image.load('background.jpg')

# Setting background music:
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 causes it to loop the music infinitely


# Logging game levels:
level_value = 1
level_font = pygame.font.Font('freesansbold.ttf', 32)
levelX = 600
levelY = 10

def show_level(x, y):
    level_text = level_font.render("LEVEL: " + str(level_value), True, (255, 255, 255))
    screen.blit(level_text, (x, y))


# Creating player:
# Image attribution: Icon made by Freepik (https://www.freepik.com) from Flaticon (www.flaticon.com)
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0

def player (x, y):
    screen.blit(playerImg, (x, y))


# Creating enemies:
# Image attribution: Icon made by Freepik (https://www.freepik.com) from Flaticon (www.flaticon.com)
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    # Spawning enemies at random locations:
    enemyX.append(random.randint(0, 736-1))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Creating bullet:
# Image attribution: Icon made by Icongeek26 (https://www.flaticon.com/authors/icongeek26) from Flaticon (www.flaticon.com)
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # Will adjust value based on playerX when firing bullet
bulletY = 480 - 32
bulletY_change = -10
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state  # Accessing bullet_state variable defined outside the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y))


# Detecting collisions:
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(bulletX - enemyX, 2) + math.pow(bulletY - enemyY, 2))
    if distance <= 27:
        return True
    return False


# Logging player score:
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = 10
scoreY = 10

def show_score(x, y):
    score_text = score_font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (x, y))


# Displaying 'Game Over' screen:
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Creating game loop:
running = True
while running:
    # Constantly display background image:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Check if user quits the game:
        if event.type == pygame.QUIT:
            running = False

        #Check if key pressed:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -(2 + (level_value * 0.5))
            elif event.key == pygame.K_RIGHT:
                playerX_change = (2 + (level_value * 0.5))
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
                bullet_Sound = mixer.Sound('laser.wav')  # Bullet firing sound
                bullet_Sound.play()
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT and playerX_change == -3) or (event.key == pygame.K_RIGHT and playerX_change == 3):
                playerX_change = 0

    # Updating player position:
    playerX += playerX_change

    # Setting boundaries for player movement:
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Calling player() to draw the player spaceship:
    player(playerX, playerY)


    # Controlling enemy movement:
    for i in range(num_of_enemies):
        # Checking if the game is over:
        if enemyY[i] >= 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Off-screen
            game_over_text()
            break

        # Updating enemy position:
        enemyX[i] += enemyX_change[i]

        # Move down and change direction when hitting boundaries:
        if enemyX[i] <= 0:
            enemyX_change[i] *= (-1)
            enemyX[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] *= (-1)
            enemyX[i] = 735
            enemyY[i] += enemyY_change[i]

        # Checking for collisions:
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Explosion sound:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

            bullet_state = "ready"
            bulletY = 480 - 32
            score_value += 1
            # Reset enemy coordinates to random values (random respawn location):
            enemyX[i] = random.randint(0, 736 - 1)
            enemyY[i] = random.randint(50, 150)

        # Calling enemy() to draw the enemy:
        enemy(enemyX[i], enemyY[i], i)


    # Controlling bullet movement:
    if bulletY <= 0:
        bulletY = 480 - 32
        bullet_state = "ready"
    if bullet_state == "fire":
        bulletY += bulletY_change
        fire_bullet(bulletX, bulletY)


    # Displaying the score:
    show_score(scoreX, scoreY)


    # Controlling game level:
    if score_value > 10 * level_value:
        level_value += 1
        for i in range(num_of_enemies):
            if enemyX_change[i] > 0:
                enemyX_change[i] += 0.5
            else:
                enemyX_change[i] -= 0.5
        num_of_enemies += 1
        enemyImg.append(pygame.image.load('enemy.png'))
        # Spawning enemies at random locations:
        enemyX.append(random.randint(0, 736 - 1))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(enemyX_change[num_of_enemies - 2])
        enemyY_change.append(40)


    # Displaying the level:
    show_level(levelX, levelY)


    # Update display screen:
    pygame.display.update()