import pygame
import random
import time
import math
import sys
from pygame import mixer

#initialize the pygame
pygame.init()

#creating a surface and window for game to run
screen = pygame.display.set_mode((800, 600))

#Title and icon
pygame.display.set_caption("Tennis")
icon = pygame.image.load('images/ping-pong.png')
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
pygame.display.set_icon(icon)

#Player 1
playerImg = pygame.image.load('images/paddle.png')
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
playerOneRect = playerImg.get_rect()
playerOneX = 0
playerOneY = 270
playerOneChange = 0

#Player 2
playerTwoX = 735
playerTwoY = 270
playerTwoChange = 0
playerTwoRect = playerImg.get_rect()

#Ball
ballImg = pygame.image.load('images/ball.png')
#<div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
ballRect = ballImg.get_rect()
ballX = 375
ballY = 270
ballXChange = 0
ballYChange = 0
collision = False

#Star
starImg = pygame.image.load('images/star.png')
#<div>Icons made by <a href="https://www.flaticon.com/authors/pixel-perfect" title="Pixel perfect">Pixel perfect</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
starRect = starImg.get_rect()
starX = random.randint(250, 550)
starY = random.randint(150, 450)
transparent = (0, 0, 0, 0)

#SCORES
score1_value = 0
score2_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text1X = 10
textY = 10
text2X = 650

#game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


#functions
def star(x, y):
    screen.blit(starImg, (x, y))


def game_over_text(player):
    over_text = over_font.render("PLAYER" + player + " WINS", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score(x1, x2, y):
    score1 = font.render("Score: " + str(score1_value), True, (255, 255, 255))
    score2 = font.render("Score: " + str(score2_value), True, (255, 255, 255))
    screen.blit(score1, (x1, y))
    screen.blit(score2, (x2, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def ball(x, y):
    screen.blit(ballImg, (x, y))


def collision(ball, p1, p2):
    if ballRect.colliderect(playerOneRect):
        return True
    elif ballRect.colliderect(playerTwoRect):
        return True
    else:
        return False

clock = pygame.time.Clock()
#game loop
running = True
while running:
	screen.fill((0, 0, 0))
	clock.tick(40)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				playerTwoChange = -1
			if event.key == pygame.K_DOWN:
				playerTwoChange = 1
			if event.key == pygame.K_w:
				playerOneChange = -1
			if event.key == pygame.K_s:
				playerOneChange = 1

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
				playerOneChange = 0
				playerTwoChange = 0
	playerOneY += playerOneChange
	playerTwoY += playerTwoChange
	playerOneRect.topleft = (playerOneX - 15, playerOneY - 32)
	playerTwoRect.topleft = (playerTwoX, playerTwoY - 32)
	ballRect.topleft = (ballX, ballY)
	starRect.topleft = (starX, starY)

	win_sound = mixer.Sound('win.wav')
	if score1_value == 10:
		win_sound.play()
		game_over_text("1")
		running = False
	elif score2_value == 10:
		win_sound.play()
		game_over_text("2")
		running = False

	power_sound = mixer.Sound('power.mp3')
	if score1_value >= 5 or score2_value >= 5:
		star(starX, starY)
		if ballRect.colliderect(starRect) and ballXChange < 0:
			power_sound.play()
			ballXChange = -1
			if ballYChange > 0:
				ballYChange = -1
			elif ballYChange < 0:
				ballYChange = 1
			starX = random.randint(250, 550)
			starY = random.randint(150, 450)
		elif ballRect.colliderect(starRect) and ballXChange > 0:
			power_sound.play()
			ballXChange = 1
			if ballYChange > 0:
				ballYChange = -1
			elif ballYChange < 0:
				ballYChange = 1
			starX = random.randint(250, 550)
			starY = random.randint(150, 450)
	if playerOneY <= 0:
		playerOneY = 0
	elif playerOneY >= 575:
		playerOneY = 575

	if playerTwoY <= 0:
		playerTwoY = 0
	elif playerTwoY >= 575:
		playerTwoY = 575

	ballX += ballXChange
	ballY += ballYChange

	if (ballX == 375 and ballY == 270 and ballXChange == 0 and ballYChange == 0):
		ballXChange = .2
		ballYChange = .2

	if (ballX == playerOneX and ballY == playerOneY):
		if (ballY > 250):
			ballXChange = .5
			ballYChange = .5
		elif (ballY <= 250):
			ballXChange = .5
			ballYChange = -.5

    #hit_sound = mixer.Sound('click.wav')
	if collision:
		if ballRect.colliderect(playerOneRect):  #changes directions the same way everytime... i need to fix this
            #hit_sound.play()
			if (ballY > 250):
				ballXChange = .5
				if ballY > playerOneY:
					ballYChange = -.2
				elif ballY < playerOneY:
					ballYChange = .5
				else:
					ballYChange = .1
			elif (ballY <= 250):
				ballXChange = .5
				if ballY > playerOneY:
					ballYChange = -.7
				elif ballY < playerOneY:
					ballYChange = .5
				else:
					ballYChange = .1
		elif ballRect.colliderect(playerTwoRect):
            #hit_sound.play()
			if (ballY > 250):
				ballXChange = -.5
				if ballY > playerTwoY:
					ballYChange = -.2
				elif ballY < playerTwoY:
					ballYChange = .5
				else:
					ballYChange = .1
			elif (ballY <= 250):
				ballXChange = -.5
				if ballY > playerTwoY:
					ballYChange = -.7
				elif ballY < playerTwoY:
					ballYChange = .5
				else:
					ballYChange = .1
	if (ballY >= 600):
		ballYChange = -.5
	elif (ballY <= 0):
		ballYChange = .5
	if (ballX < 0 or ballX > 800):
		time.sleep(.1)
        #beep_sound = mixer.Sound('beep.aiff')
        #beep_sound.play()
		if ballX < 0:
			score2_value += 1
		elif ballX > 800:
			score1_value += 1
		ballX = 375
		ballY = 270
		ballXChange = 0
		ballYChange = 0

	ballX += ballXChange
	ballY += ballYChange
	ball(ballX, ballY)
	player(playerOneX, playerOneY)
	player(playerTwoX, playerTwoY)
	show_score(text1X, text2X, textY)
	pygame.display.update()
	
