import pygame
import math
import random
from pygame import mixer

pygame.init()

screen=pygame.display.set_mode((800,600))

pygame.display.set_caption('sampath')

pic=pygame.image.load('candle.png')
pygame.display.set_icon(pic)
enemyimg=pygame.image.load('enemy.png')
playerimg=pygame.image.load('player.png')
#background img
backgroundimg=pygame.image.load('back.png')
#bg music
mixer.music.load('bgms.wav')
mixer.music.play()

bulletimg=pygame.image.load('bullet.png')


playerx=370
playery=480
playerx_mov=0##here observe clearly if u change value to some 0.2 the movement is changes it moves fastes
playery_mov=0
#enemy part how it is working
#below process is to get more enemies
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_mov=[]
enemyy_mov=[]
num=5
for i in range(num):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0, 736)) ##becz of below line think it y we took 736
    enemyy.append(random.randint(50, 150))
    enemyx_mov.append(2)
    enemyy_mov.append(10)


#bullet movement and its working
bulletx=0
bullety=480
bullety_mov=5
bullet_state='ready'
##inserting player into console we use blit function to insert any thing on to console
def player(x,y):
    screen.blit(playerimg,(x,y))
#inserting enemy on to console
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletimg,(x+16,y+6))
def iscollision(enemyx,enemyy,bulletx,bullety):
    dis=math.sqrt((math.pow(enemyx-bulletx,2))+(math.pow(enemyy-bullety,2)))
    if dis<25:
        return True
    else:
        return False
score_val=0
font=pygame.font.Font('freesansbold.ttf',32)
fontx=10
fonty=10
def show_score(x,y):
    score=font.render("score:"+ str(score_val),True,(0,255,0))
    screen.blit(score,(x,y))
text_over=pygame.font.Font('freesansbold.ttf',60)
def game_over():
    text=text_over.render('GAMEOVER',True,(100,0,0))
    screen.blit(text,(200,250))
run=True
while run:
    ## (R,G,B)
    screen.fill((0, 0, 0))
    screen.blit(backgroundimg,(0,0))
    #the below condition checks all keys in key board and their functions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        #how keyboard keys are controlled as follows
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_mov=-5
            if event.key==pygame.K_RIGHT:
                playerx_mov=5
            if event.key==pygame.K_UP:
                playery_mov=-5
            if event.key==pygame.K_DOWN:
                playery_mov=5
            if event.key==pygame.K_SPACE:
                ##so here if u not give ready syatement ,whwn u move and shoot it will get some errors to fix
                if bullet_state is 'ready':
                    bullet_sound=mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx=playerx # to fix player x coodinate to bullet after shooting bullet
                    fire_bullet(bulletx,bullety)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerx_mov=0
            if event.key==pygame.K_RIGHT:
                playerx_mov=0
            if event.key==pygame.K_UP:
                playery_mov=0
            if event.key==pygame.K_DOWN:
                playery_mov=0




    #u should call function after filling color,,if u call,the fig is under color itself
    playerx+=playerx_mov
    playery+=playery_mov
    if playerx<0:
        playerx=0
    elif playerx>=736:##becoz we took 64 pixels of spaceship so we need to subtract 800-64
        playerx=736
    elif playery<=0:
        playery=0
    elif playery>=536:##here 600-64
        playery=536
    #enemy movement in this when u speify a+=b it occurs repeatedly
    for i in range(num):
        if enemyy[i]>440:
            for j in range(num):
                enemyy[j]=2000
            game_over()
            break

        enemyx[i] += enemyx_mov[i]
        if enemyx[i] >= 736:  ###here observe v need to give on above enemy boundries as 736 not 800 ..
            enemyy[i] += enemyy_mov[i]
            enemyx_mov[i] = -2  # here u can add directly it goes as loop ,,but for understanding we r taking variable
        elif enemyx[i] <= 0:
            enemyy[i] += enemyy_mov[i]
            enemyx_mov[i]= 2
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_sound=mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullety = 480
            bullet_state = 'ready'
            score_val += 1
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i], enemyy[i],i)

    if bullety<=0:
        bullety=480
        bullet_state='ready'
    if bullet_state is 'fire':
        fire_bullet(bulletx,bullety)
        bullety-=bullety_mov
    show_score(fontx,fonty)
    player(playerx,playery)
    pygame.display.update()


