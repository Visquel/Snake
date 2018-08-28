import random
import pygame
import sys
from pygame.locals import *

velocidad_serpiente = 9
ancho_pantalla = 800
altura_pantalla = 500
tamano_celda = 25
assert ((ancho_pantalla % tamano_celda) == 0), "El ancho de la pantalla debe ser multiplo al tamano de celda"
assert ((altura_pantalla % tamano_celda) == 0), "La altura de la pantalla deber multiplo del tamano de celda"
an_celda = int(ancho_pantalla / tamano_celda) #Ancho de la celda
al_celda = int (altura_pantalla / tamano_celda) #altura de la celda

#Definiendo los colores para los elementos del programa
negro = (0,0,0)
blanco = (255,255,255)
amarillo = (255,255,0)
azul = (0,0,255)
azul_oscuro = (0,0,150)
rojo = (255,0,0)
rojo_oscuro = (150,0,0)
verde = (0,255,0)
verde_oscuro = (0,155,0)
gris_oscuro = (40,40,40)

color_fondo = gris_oscuro #color del fondo de la pantalla

#Definiendo las teclas del teclado
UP = "arriba"
DOWN = "abajo"
LEFT = "izquierda"
RIGHT = "derecha"

cabeza = 0 #indice de la cabeza de la serpiente

def main():
    global reloj_velocidad, mostrar_pantalla, tipo_letra, sonido_comida, sonido_choque

    pygame.init()
    pygame.mixer.init()
    sonido_comida = pygame.mixer.Sound("snakeeat.wav")
    sonido_choque = pygame.mixer.Sound("snakecrash.wav")
    reloj_velocidad = pygame.time.Clock()
    mostrar_pantalla = pygame.display.set_mode((ancho_pantalla, altura_pantalla))
    tipo_letra = pygame.font.Font("freesansbold.ttf", 18)
    pygame.display.set_caption("Snake Game")

    mostrar_pantallaInicio() 
    while True:
        correr_juego()
        pantalla_perdiste() #Mostrar la pantalla de perder

def correr_juego():
    #Estableciendo un punto de inicio aleatorio
    iniciar_x = random.randint(5, an_celda - 6)
    iniciar_y = random.randint(5, al_celda - 6)
    coords_serp = [{"x": iniciar_x,     "y": iniciar_y},
                       {"x": iniciar_x - 1, "y": iniciar_y},
                       {"x": iniciar_x - 2, "y": iniciar_y}]
    direccion = RIGHT

    #Iniciar la manzana en un lugar aleatorio
    manzana = getRandomLocation()

    while True: #ciclo principal del juego
        for event in pygame.event.get(): #ciclo de manejo de eventos
            if (event.type == QUIT):
                finalizar()
            elif (event.type == KEYDOWN):
                if ((event.key == K_LEFT) and (direccion != RIGHT)):
                    direccion = LEFT
                elif ((event.key == K_RIGHT) and (direccion != LEFT)):
                    direccion = RIGHT
                elif ((event.key == K_UP) and (direccion != DOWN)):
                    direccion = UP
                elif ((event.key == K_DOWN) and (direccion != UP)):
                    direccion = DOWN
                elif (event.key == K_ESCAPE):
                    finalizar()

        #Evaluar si la serpiente ha chocado con ella misma o con los bordes
        if ((coords_serp[cabeza]["x"] == -1) or (coords_serp[cabeza]["x"] == an_celda) or (coords_serp[cabeza]["y"] == -1) or (coords_serp[cabeza]["y"] == al_celda)):
           sonido_choque.play()
           return #perdiste
        for cuerpo_serp in coords_serp[1:]:
            if (cuerpo_serp ["x"] == coords_serp[cabeza]["x"]) and (cuerpo_serp["y"] == coords_serp[cabeza]["y"]):
                sonido_choque.play()
                return #perdiste

        #verificar que la posicion de la manzana no choque con la serpiente
        for cuerpo_serp in coords_serp[1:]:
            if (cuerpo_serp ["x"] == coords_serp[cabeza]["x"]) and (cuerpo_serp["y"] == coords_serp[cabeza]["y"]) and ((coords_serp[cabeza]["x"] == manzana["x"]) and (coords_serp[cabeza]["y"] == manzana["y"])):
                manzana = getRandomLocation() #Establecer una nueva manzana en alguna parte excepto en la serpiente


        #Evaluar si la serpiente ha comido y aplicar
        if ((coords_serp[cabeza]["x"] == manzana["x"]) and (coords_serp[cabeza]["y"] == manzana["y"])):
            sonido_comida.play()
            #No eliminar el segmento de la cola de la serpiente
            manzana = getRandomLocation() #Establecer una nueva manzana en alguna parte
        else:
            del coords_serp[-1] #Eliminar un segmento de la cola de la serpiente

        #Mover la serpiente agregando un segmento en la direccion en que se esta moviendo            
        if (direccion == UP):
            nueva_cabeza = {"x": coords_serp[cabeza]["x"], "y": coords_serp[cabeza]["y"] - 1}
        elif (direccion == DOWN):
            nueva_cabeza = {"x": coords_serp[cabeza]["x"], "y": coords_serp[cabeza]["y"] + 1}
        elif (direccion == LEFT):
            nueva_cabeza = {"x": coords_serp[cabeza]["x"] - 1, "y": coords_serp[cabeza]["y"]}
        elif (direccion == RIGHT):
            nueva_cabeza = {"x": coords_serp[cabeza]["x"] + 1, "y": coords_serp[cabeza]["y"]}

        coords_serp.insert(0, nueva_cabeza)
        mostrar_pantalla.fill(color_fondo)
        dibujar_serp(coords_serp)
        dibujar_manzana(manzana)
        fijar_puntaje(len(coords_serp) - 3)
        pygame.display.update()
        reloj_velocidad.tick(velocidad_serpiente)

def msj_para_jugar():
    mensaje_jugar = tipo_letra.render("Presione una tecla para jugar", True, blanco)
    obtener_tecla = mensaje_jugar.get_rect()
    obtener_tecla.topleft = (ancho_pantalla - 500, altura_pantalla - 50)
    mostrar_pantalla.blit(mensaje_jugar, obtener_tecla)

def evaluar_teclas():
    if len(pygame.event.get(QUIT)) > 0:
        finalizar()
    evento_t_arriba = pygame.event.get(KEYUP)
    if len(evento_t_arriba) == 0:
        return None
    if (evento_t_arriba[0].key == K_ESCAPE):
        finalizar()
    return evento_t_arriba[0].key

def mostrar_pantallaInicio():
    fuente_titulo = pygame.font.Font('freesansbold.ttf', 60)
    titulo_principal = fuente_titulo.render("SNAKE GAME", True, blanco, azul_oscuro)
    grado1 = 0
    grado2 = 0

    while True:
        mostrar_pantalla.fill(color_fondo)
        rotar_titulo = pygame.transform.rotate(titulo_principal, grado1)
        rotar_rectangulo = rotar_titulo.get_rect()
        rotar_rectangulo.center = (ancho_pantalla / 2, altura_pantalla / 2)
        mostrar_pantalla.blit(rotar_titulo, rotar_rectangulo)
                
        msj_para_jugar()

        if evaluar_teclas():
            pygame.event.get() #limpiar la cola de eventos, para iniciar el juego
            return

        pygame.display.update()
        reloj_velocidad.tick(velocidad_serpiente)
        grado1 += 3 #Girar por 3 grados cada marco
        grado2 += 7 #Girar por 7 grados cada marco

def finalizar():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {"x": random.randint(0, an_celda - 1), "y": random.randint(0, al_celda - 1)}
    
def pantalla_perdiste():
    fuente_perdiste = pygame.font.Font('freesansbold.ttf', 100)
    pantalla_game = fuente_perdiste.render("GAME", True, blanco)
    pantalla_over = fuente_perdiste.render("OVER", True, blanco)
    locacion_game = pantalla_game.get_rect()
    locacion_over = pantalla_over.get_rect()
    locacion_game.midtop = ((ancho_pantalla / 2, 10))
    locacion_over.midtop = (ancho_pantalla / 2, locacion_game.height + 10 + 25)

    mostrar_pantalla.blit(pantalla_game, locacion_game)
    mostrar_pantalla.blit(pantalla_over, locacion_over)
    msj_para_jugar()
    pygame.display.update()
    pygame.time.wait(500)
    evaluar_teclas() #limpiar cualquier tecla presionada en el evento

    while True:
        if evaluar_teclas():
            pygame.event.get() #quitar evento en la fila
            return

def fijar_puntaje(puntaje):
    puntaje_pantalla = tipo_letra.render("Puntaje: %s" % (puntaje), True, blanco)
    locacion_puntaje = puntaje_pantalla.get_rect()
    locacion_puntaje_ariz = (ancho_pantalla - 120, 10)
    mostrar_pantalla.blit(puntaje_pantalla, locacion_puntaje)

def dibujar_serp(coords_serp):
    for coordenadas in coords_serp:
        x = coordenadas["x"] * tamano_celda
        y = coordenadas["y"] * tamano_celda
        segmento_serp = pygame.Rect(x, y, tamano_celda, tamano_celda)
        pygame.draw.rect (mostrar_pantalla, verde, segmento_serp)
        segmento_serp_interior = pygame.Rect(x + 4, y + 4, tamano_celda - 8, tamano_celda - 8)
        pygame.draw.rect(mostrar_pantalla, verde_oscuro, segmento_serp_interior)

def dibujar_manzana(coordenadas):
    x = coordenadas['x'] * tamano_celda
    y = coordenadas['y'] * tamano_celda
    dib_manzana = pygame.Rect(x, y, tamano_celda, tamano_celda)
    pygame.draw.rect(mostrar_pantalla, rojo, dib_manzana)
    segmento_serp_interior = pygame.Rect(x + 4, y + 4, tamano_celda - 8, tamano_celda - 8)
    pygame.draw.rect(mostrar_pantalla, rojo_oscuro, segmento_serp_interior)


main()




    
        
            
            

    

        
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
        
        
        
        
            
               
    

    
    
    





