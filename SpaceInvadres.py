import pygame
from pygame import mixer
import os.path
import random
import math
#inicijalizacija pygame-a
pygame.init()

screen = pygame.display.set_mode((800,500))#x i y osa
myfont = pygame.font.SysFont("Arial", 60,)
label = myfont.render("hello world" ,1, (255,255,0))#rgb
clock = pygame.time.Clock()
FPS = 30
backround = pygame.image.load('2599.jpg')

pygame.display.set_caption("space invader")
image = pygame.image.load('transportation (2).png')
pygame.display.set_icon(image)

mixer.music.load('background.wav')
mixer.music.play(-1)

score = 0

playerImg = pygame.image.load('game.png')
playerX = 370
playerY = 380
playerX_Change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numEnemies = 9

for i in range (numEnemies):
    enemyImg.append(pygame.image.load('signs.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(5) 
    enemyY_change.append(64)

buleltImg = pygame.image.load('miscellaneous.png')
bulletX = 0 
bulletY = 380
bulletX_change = 0  
bulletY_change = 15
bulletState = "ready"

scoreValue = 0
font = pygame.font.Font('freesansbold.ttf',32)
testX = 10
testY = 10

oveerFont = pygame.font.Font('freesansbold.ttf',32)

def gameOver():
    oveerFont = font.render("GAME OVER",True,(255,255,255))
    screen.blit(oveerFont,(200,250))



def showScore(x,y):
    score = font.render("Score :" + str(scoreValue),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def bulletFire(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(buleltImg,(x+16,y+10))

def isCollsion(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False

line = pygame.font.Font('freesansbold.ttf',5)
line = font.render("---------------------------------------------------------------------------------------------",1,(255,0,0))
running = True

while running:
    screen.fill((0,0,0))
    screen.blit(backround,(0,0))
    screen.blit(line,(0,364))
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #keyboard
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -6
            if event.key == pygame.K_RIGHT:
                playerX_Change = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                playerX_Change = -6
            elif event.key == pygame.K_LEFT:
                playerX_Change = 6
            elif event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX 
                    bulletFire(bulletX,bulletY)
            elif event.key == pygame.K_p:
                playerX_Change = 0

             



    playerX += playerX_Change 
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range (numEnemies):
        if enemyY[i] > 300:
            for j in range(numEnemies):
                enemyY[j] = 2000
            gameOver()
            break 


        enemyX[i] += enemyX_change[i] 
        if enemyX[i] <= 0:  
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        collision = isCollsion(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            ExplosionSound = mixer.Sound('explosion.wav')
            ExplosionSound.play()
            bulletY = 380
            bulletState = "ready"
            scoreValue += 1
            #print(score)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150) 
        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 380
        bulletState = "ready"

    if bulletState is "fire":
        bulletFire(bulletX,bulletY)
        bulletY -= bulletY_change
    


    player(playerX,playerY)
    showScore(testX,testY)
    #screen.blit(label,(100,100))
    pygame.display.update()
    clock.tick(FPS)