import pygame
import threading
import time
import random

pygame.init()
pygame.mixer.init()

try:
    pygame.mixer.music.load("musicaFondo.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
except pygame.error as e:
    print(f"Error al cargar música: {e}")

imagen_fondo = pygame.image.load("espacio.png")
imagen_fondo = pygame.transform.scale(imagen_fondo, (800, 600))

ancho_ventana = 800
alto_ventana = 600
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))

try:
    icono_aplicacion = pygame.image.load("conejo.ico")
    pygame.display.set_icon(icono_aplicacion)
except pygame.error as e:
    print(f"Error al cargar el ícono: {e}")

pygame.display.set_caption("Brain Scape")

try:
    imagen_jugador = pygame.image.load("conejoastronauta.png")
    imagen_jugador = pygame.transform.scale(imagen_jugador, (50, 50))
    rectangulo_jugador = imagen_jugador.get_rect(center=(ancho_ventana // 2, alto_ventana - 50))
except pygame.error as e:
    print(f"Error al cargar la imagen del jugador: {e}")

try:
    imagen_obstaculo = pygame.image.load('asteroide.png')
    imagen_obstaculo = pygame.transform.scale(imagen_obstaculo, (50, 50))
except pygame.error as e:
    print(f"Error al cargar la imagen del obstáculo: {e}")

obstaculos = []
cantidad_obstaculos = 5

class Obstaculo:
    def __init__(self, posicion, direccion):
        self.imagen = imagen_obstaculo
        self.rectangulo = self.imagen.get_rect(center=posicion)
        self.direccion = direccion

    def mover(self):
        self.rectangulo.x += velocidad_movimiento * self.direccion
        if self.rectangulo.right >= ancho_ventana or self.rectangulo.left <= 0:
            self.direccion *= -1

obstaculos = [
    Obstaculo((400, alto_ventana // 2), random.choice([1, -1])),
    Obstaculo((100, alto_ventana // 2), random.choice([1, -1])),
    Obstaculo((700, alto_ventana // 2), random.choice([1, -1])),
    Obstaculo((300, alto_ventana // 2), random.choice([1, -1])),

    Obstaculo((700, 60), random.choice([1, -1])),
    Obstaculo((300, 60), random.choice([1, -1])),
    Obstaculo((400, 60), random.choice([1, -1])),
    Obstaculo((100, 60), random.choice([1, -1])),

    Obstaculo((100, 180), random.choice([1, -1])),
    Obstaculo((300, 180), random.choice([1, -1])),
    Obstaculo((700, 180), random.choice([1, -1])),
    Obstaculo((400, 180), random.choice([1, -1])),

    Obstaculo((100, 400), random.choice([1, -1])),
    Obstaculo((300, 400), random.choice([1, -1])),
    Obstaculo((700, 400), random.choice([1, -1])),
    Obstaculo((400, 400), random.choice([1, -1])),

    Obstaculo((100, 480), random.choice([1, -1])),
    Obstaculo((300, 480), random.choice([1, -1])),
    Obstaculo((700, 480), random.choice([1, -1])),
    Obstaculo((400, 480), random.choice([1, -1])),
]

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

velocidad_movimiento = 5
esta_pausado = False

def mover_obstaculos():
    global esta_pausado
    while True:
        if not esta_pausado:
            for obstaculo in obstaculos:
                obstaculo.mover()
        time.sleep(0.02)

hilo_movimiento = threading.Thread(target=mover_obstaculos)
hilo_movimiento.daemon = True
hilo_movimiento.start()

ejecutando = True
juego_terminado = False
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            if evento.key == pygame.K_p:
                esta_pausado = not esta_pausado
                pygame.mixer.music.set_volume(0.1 if esta_pausado else 0.3)

    if not juego_terminado:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            rectangulo_jugador.x -= velocidad_movimiento
        if teclas[pygame.K_RIGHT]:
            rectangulo_jugador.x += velocidad_movimiento
        if teclas[pygame.K_UP]:
            rectangulo_jugador.y -= velocidad_movimiento
        if teclas[pygame.K_DOWN]:
            rectangulo_jugador.y += velocidad_movimiento

        rectangulo_jugador.clamp_ip(ventana.get_rect())

        for obstaculo in obstaculos:
            if rectangulo_jugador.colliderect(obstaculo.rectangulo):
                juego_terminado = True

    if juego_terminado:
        ventana.fill(ROJO)
        fuente = pygame.font.Font(None, 74)
        texto_game_over = fuente.render("GAME OVER", True, (255, 255, 255))
        rectangulo_texto = texto_game_over.get_rect(center=(ancho_ventana // 2, alto_ventana // 2))
        ventana.blit(texto_game_over, rectangulo_texto)
    else:
        for x in range(0, ancho_ventana, imagen_fondo.get_width()):
            for y in range(0, alto_ventana, imagen_fondo.get_height()):
                ventana.blit(imagen_fondo, (x, y))
        
        for obstaculo in obstaculos:
            ventana.blit(obstaculo.imagen, obstaculo.rectangulo)
        ventana.blit(imagen_jugador, rectangulo_jugador)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
