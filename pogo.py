# benis first python game
import pygame
import random
import sys

print("You can try 5 times and it will count all hits. Good luck.")

scrx=500
scry=500

paddlewidth=100
paddleheight=15
paddlex=100
paddley=400
actualpaddlespeed = 0
maxpaddlespeed = 500

ballx=int(scrx*0.5)
bally=int(scrx*0.5)
ballrad = 5
ballspeedx=200
ballspeedy=-200
maxballspeedy = 200

# lebenspunkte lp
lp=6
hits = 0

STATE_PAUSE = 0
STATE_PLAY = 1
GAMESTATE = STATE_PAUSE

# time processing
deltaTime = 0
ticksLastFrame = 0
def getDeltaTime():
	global deltaTime, ticksLastFrame
	t=pygame.time.get_ticks()
	deltaTime = (t-ticksLastFrame)*0.001
	ticksLastFrame = t

def ballmove():
	global ballx, bally, ballspeedy, ballspeedx, hits
	
	if GAMESTATE != STATE_PLAY:
		return
		
	ballx += ballspeedx*deltaTime
	bally += ballspeedy*deltaTime
	# check if ball has hit the paddle
	if bally>=paddley and bally<=paddley+paddleheight and ballx>=paddlex and ballx<=paddlex+paddlewidth:
		bally=paddley-1
		ballspeedy=-ballspeedy
		hits+=1
		# randomize speed
		if ballx<=paddlex+paddlewidth*0.5:
			ballspeedx -= ballx-paddlex
		else:
			ballspeedx+= ballx-paddlex *0.5
	# pogo
	if ballspeedy != maxballspeedy:
		ballspeedy += 225*deltaTime
	# bounce
	if bally-ballrad <= 0:
		ballspeedy=-ballspeedy
		bally = ballrad+1
	if ballx-ballrad<=0:
		ballspeedx*=-1
		ballx=ballrad+1
	if ballx+ballrad>=scrx:
		ballspeedx*=-1
		ballx=scrx-ballrad-1
	if bally>=scry:
		reset()

def paddlemove():
	global paddlex
	if GAMESTATE != STATE_PLAY:
		return
	paddlex += actualpaddlespeed*deltaTime

def paddleblock():
	# only set globals if you manipulate them (?)
	global paddlex
	if paddlex <= 0:
		paddlex = 0
	if paddlex >= scrx - paddlewidth:
		paddlex = scrx - paddlewidth


def reset():
	global GAMESTATE, deltatime
	global lp, paddlex, paddley, actualpaddlespeed
	global ballx, bally, ballspeedx, ballspeedy

	GAMESTATE = STATE_PAUSE

	paddlex = 200
	paddley = 400
	ballx = int(scrx*0.5)
	bally = int(scry*0.5)

	lp=lp-1
	
	ballspeedx=random.randint(-2,2)
	if ballspeedx == 0:
		ballspeedx = 1
		
	ballspeedx=ballspeedx*100

	ballspeedy=random.randint(-2,2)
	if ballspeedy == 0:
		ballspeedy = 2
		
	ballspeedy=ballspeedy*100

	screen.fill((0,0,55))
	drawball()
	drawpaddle()
	pygame.display.flip()
	# wait in ms
	pygame.time.wait(1000)
	# call getDeltaTime twice to remove time lag.
	getDeltaTime()
	getDeltaTime()
	actualpaddlespeed = 0
	GAMESTATE = STATE_PLAY

def drawball():
	# circle(screen, (colr, colg, colb),(x,y),donotfill) <- 0, 1
	pygame.draw.circle(screen, (255,200,0),(int(ballx), int(bally)), ballrad, 0)

def drawpaddle():
	# rect(screen, (colr, colg, colb),(x,y,width, height), donotfill)
	pygame.draw.rect(screen,(0,200,0),(int(paddlex), int(paddley), paddlewidth, paddleheight), 0)

# game starts here
pygame.init()
screen = pygame.display.set_mode([scrx, scry])
pygame.display.set_caption("Pogo")

reset()

keyleft = 0
keyright = 0
while lp>0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				keyleft = 1
			if event.key==pygame.K_RIGHT:
				keyright = 1
			# exit handler
			if event.key==pygame.K_q:
				print("Done. You exited yourself and have "+str(hits)+" hits.")
				sys.exit()
		if event.type == pygame.KEYUP:
			if event.key==pygame.K_LEFT:
				keyleft=0
			if event.key==pygame.K_RIGHT:
				keyright=0
# keymap processing
	if keyleft==1 and keyright==0:
		actualpaddlespeed = -maxpaddlespeed
	if keyleft==0 and keyright==1:
		actualpaddlespeed = maxpaddlespeed
	if keyleft==0 and keyright ==0:
		actualpaddlespeed = 0

	screen.fill((0,0,55))
	paddlemove()
	paddleblock()
	drawpaddle()
	ballmove()
	drawball()
	pygame.display.flip()
	getDeltaTime()
	
print("Done. You have "+str(hits)+" hits.")
