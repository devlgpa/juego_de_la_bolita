import sys #para usar exit()
import time #para usar sleep()
import pygame

ANCHO = 640 #ancho de la pantalla
ALTO = 480 #alto de la pantalla
color_azul = (0, 0, 64) #color
color_blanco = (255, 255, 255) #color blanco, para textos 

pygame.init()

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar Imagen
        self.image = pygame.image.load('./bolita.png')
        #Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        #Posicion Inicial centrada en pantall
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        #establecer velocidad incial
        self.speed = [4,4]
    def update(self):
        #Evitar que salga por arriba
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        #evitar que salga por derecha
        elif self.rect.right >= ANCHO or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        #Mover en base a posiscion actual y velocidad.
        self.rect.move_ip(self.speed)

class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cargar Imagen
        self.image = pygame.image.load('./paleta.png')
        #Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        #Posicion Inicial centrada en pantalla en x
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        #establecer velocidad incial
        self.speed = [0,0]
    def update(self, evento):
        #buscar si se presiono flecha izquierda
        if evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-10, 0]
        #si presiono la flecha derecha
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [10, 0]
        else:
            self.speed = [0, 0]
        #Mover en base a posiscion actual y velocidad.
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        #Cargar Imagen
        self.image = pygame.image.load('./ladrillo.png')
        #Obtener rectangulo de la imagen
        self.rect = self.image.get_rect()
        #Posicion inicial, provista externamente
        self.rect.topleft = posicion  

class Muro(pygame.sprite.Group):
    def __init__(self, cantidadLadrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadLadrillos):
            ladrillo = Ladrillo((pos_x, pos_y))
            self.add(ladrillo)

            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height

#funcion llamada tras dejar ir la bolita.
def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 72)
    texto = fuente.render('Juego terminado :(', True, (color_blanco))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    #pausar por 3 segundos
    time.sleep(3)
    #salir
    sys.exit()

def mostrar_puntuacon():
    fuente = pygame.font.SysFont('Consolas', 20)
    texto = fuente.render(str(puntuacion).zfill(5), True, (color_blanco))
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0, 0]
    pantalla.blit(texto, texto_rect)

def mostrar_vidas():
    fuente = pygame.font.SysFont('Consolas', 20)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, (color_blanco))
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO, 0]
    pantalla.blit(texto, texto_rect)


#inicializando pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#configurar titulo
pygame.display.set_caption('Juego de Ladrillos')
#crear el reloj
reloj = pygame.time.Clock()
#ajustar repeticion de evento de tecla presionada
pygame.key.set_repeat(30)

bolita = Bolita()
jugador = Paleta()
muro = Muro(50)
puntuacion = 0
vidas = 3
esperando_saque = True

while True:
    #Establecer FPS
    reloj.tick(60)
    #revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            #cerrar el videojuego
            sys.exit()
        #buscar eventos por teclado
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)
            if esperando_saque == True and evento.key == pygame.K_SPACE:
                esperando_saque = False
                if bolita.rect.centerx < ANCHO / 2:
                    bolita.speed = [4, -4]
                else:
                    bolita.speed = [-4, -4]
    #actualizar posicion de la bolita
    if esperando_saque == False:
        bolita.update()
    else:
        bolita.rect.midbottom = jugador.rect.midtop
    #colicion entre bolita y jugador
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]

    #colision de la bolita con el muro
    lista = pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)
        puntuacion += 10
    #Revisar si la bolita sale de la pantalla
    if bolita.rect.top >ALTO:
        vidas -= 1
        esperando_saque = True

    #rellenar pantalla
    pantalla.fill(color_azul)
    #Mostrar puntuacion
    mostrar_puntuacon()
    #mostrar vidas
    mostrar_vidas()
    #Dibujar bolita en pantalla
    pantalla.blit(bolita.image, bolita.rect)
    #Dibujar jugador en pantalla
    pantalla.blit(jugador.image, jugador.rect)
    #Dibujar ladrillos
    muro.draw(pantalla)
    #Actualizar los Elementos en pantalla
    pygame.display.flip()

    if vidas <= 0:
        juego_terminado()