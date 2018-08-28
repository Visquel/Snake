#Importamos los demas archivos
import pygame as pg
import Serpiente as snk
import Comida as fd
import sys
from Colores import *

# Constantes del juego
WIDTH      = 40
HEIGHT     = 20
SPEED      = 8
SPEED_TICK = 5
SPEED_INC  = 3
SHORT      = 5
LONG       = 3

#Dar formato a las barreras del mapa
wallblock = pg.Surface((snk.BLOCK_SIZE,snk.BLOCK_SIZE))
wallblock.set_alpha(255)
wallblock.fill(BLACK)
wallblockdark = pg.Surface((snk.BLOCK_SIZE_INNER,snk.BLOCK_SIZE_INNER))
wallblockdark.set_alpha(255)
wallblockdark.fill(WHITE)

#Verificar si la culebra esta dentro de los limites
def inLimits(snake):
	headpos = snake.getHeadPos()
	return not (headpos[0] < 1 or headpos[1] < 1 or headpos[0] >= HEIGHT+1 or headpos[1] >= WIDTH+1)

#Establecer los limites
def drawWalls(surface):

	#Limites derecho e izquierdo
	for y in range(HEIGHT+1):
		surface.blit(wallblock,(0,y*snk.BLOCK_SIZE))
		surface.blit(wallblockdark,(5,y*snk.BLOCK_SIZE+5))
		surface.blit(wallblock,((WIDTH+1)*snk.BLOCK_SIZE,y*snk.BLOCK_SIZE))
		surface.blit(wallblockdark,((WIDTH+1)*snk.BLOCK_SIZE+5,y*snk.BLOCK_SIZE+5))

	#Limites superior e inferior
	for x in range(WIDTH+2):
		surface.blit(wallblock,(x*snk.BLOCK_SIZE,0))
		surface.blit(wallblockdark,(x*snk.BLOCK_SIZE+5,5))
		surface.blit(wallblock,(x*snk.BLOCK_SIZE,(HEIGHT+1)*snk.BLOCK_SIZE,))
		surface.blit(wallblockdark,(x*snk.BLOCK_SIZE+5,(HEIGHT+1)*snk.BLOCK_SIZE+5))


#Iniciamos Pygame
pg.init()

#Se utilizan herramientas de Pygame para la interfaz
pg.mixer.init()
eatsound = pg.mixer.Sound("snakeeat.wav")
crashsound = pg.mixer.Sound("snakecrash.wav")
clock = pg.time.Clock()
screen = pg.display.set_mode(((WIDTH+2)*snk.BLOCK_SIZE,(HEIGHT+2)*snk.BLOCK_SIZE))
pg.display.set_caption("Snake Game")
font = pg.font.SysFont(pg.font.get_default_font(),40)
gameovertext = font.render("GAME OVER",1,BLUE_DARK)
starttext = font.render("PRESIONE ENTER PARA INICIAR EL JUEGO",1,BLUE_DARK)
screen.fill(WHITE)

#Utilizamos los archivos de culebra y comida
snake = snk.snake(screen,WIDTH/2,HEIGHT/2)
food = fd.food(screen,1,HEIGHT+1,1,WIDTH+1)

while food.getPos() in snake.getPosList():
	food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)

eaten = 0
drawWalls(screen)
screen.blit(starttext,((WIDTH-10)*snk.BLOCK_SIZE/2,HEIGHT*snk.BLOCK_SIZE/2))
pg.display.flip()
waiting = True
while waiting:
	event = pg.event.wait()
	if event.type == pg.KEYDOWN:
		waiting = False
screen.fill(WHITE)

def terminate():
    pg.quit()
    sys.exit()


#=========================================================================================================#
#                                          Bloque central del juego                                       #
#=========================================================================================================#
running = True
while running:

	#Se verifica si la culebra ha chocado o esta fuera de los limites
	if not inLimits(snake) or snake.crashed:
		running = False
		crashsound.play()
	else:

		#Se procede a iniciar la interfaz
		food.draw()
		snake.draw()
		drawWalls(screen)
		pg.display.flip()

		#Se verifica que la culebra coma 
		if food.getPos() == snake.getHeadPos():
			eatsound.play()
			snake.grow()
			#La comida no debe aparecer en una posicion ocupada
			food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)
			while food.getPos() in snake.getPosList():
				food.__init__(screen,1,HEIGHT+1,1,WIDTH+1)
			eaten += 1
			#Se aumenta la velocidad
			if eaten % SPEED_INC == 0:
				SPEED += SPEED_TICK

		
		clock.tick(SPEED)
		event = pg.event.poll()
		if event.type == pg.QUIT:
			terminate()
		elif event.type == pg.KEYDOWN:
			actmotdir = snake.getMotionDir()
			if event.key == pg.K_ESCAPE:
				terminate()
			elif event.key == pg.K_UP and actmotdir != snk.DOWN:
				snake.setMotionDir(snk.UP)
			elif event.key == pg.K_DOWN and actmotdir != snk.UP:
				snake.setMotionDir(snk.DOWN)
			elif event.key == pg.K_RIGHT and actmotdir != snk.LEFT:
				snake.setMotionDir(snk.RIGHT)
			elif event.key == pg.K_LEFT and actmotdir != snk.RIGHT:
				snake.setMotionDir(snk.LEFT)

		snake.remove()
		snake.move()





def main():
        clock.tick(LONG)
        snake.draw()
        drawWalls(screen)
        snakeposlist = snake.getPosList()
        blackblock = snake.backblock
        for pos in snakeposlist[1:]:
                screen.blit(blackblock,(pos[1]*snk.BLOCK_SIZE,pos[0]*snk.BLOCK_SIZE))
                pg.display.flip()
                clock.tick(SHORT)

        while True:
                screen.blit(gameovertext,((WIDTH-4)*snk.BLOCK_SIZE/2,HEIGHT*snk.BLOCK_SIZE/2))
                pg.display.flip()
                event = pg.event.wait()
                

main()


