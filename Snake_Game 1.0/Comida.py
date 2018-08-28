import pygame as pg
import random as rnd
from Colores import *


BLOCK_SIZE       = 30
BLOCK_SIZE_INNER = 20

class food:

	#Se determina donde puede aparecer el bloque "comida"
	def __init__(self,surface,minx,maxx,miny,maxy):
		self.surface = surface
		self.posx    = rnd.randint(minx,maxx-1)
		self.posy    = rnd.randint(miny,maxy-1)

		#Se crea le da forma al bloque "Comida"
		self.foodblock = pg.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.foodblock.set_alpha(255)
		self.foodblock.fill(RED)
		self.foodblockdark = pg.Surface((BLOCK_SIZE_INNER,BLOCK_SIZE_INNER))
		self.foodblockdark.set_alpha(255)
		self.foodblockdark.fill(RED_DARK)

	def getPos(self):
		return (self.posx,self.posy)

	#Se presenta el bloque "comida" de forma aleatoria
	def draw(self):
		fb = self.foodblock
		fbd = self.foodblockdark
		sf = self.surface

		foodpos = self.getPos()
		sf.blit(fb,(foodpos[1]*BLOCK_SIZE,foodpos[0]*BLOCK_SIZE))
		sf.blit(fbd,(foodpos[1]*BLOCK_SIZE+5,foodpos[0]*BLOCK_SIZE+5))
