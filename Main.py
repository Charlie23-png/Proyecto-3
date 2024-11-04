import pygame  
import threading
import time
import random

pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Brain Scape")

# Carga la imagen del título
titulo = pygame.image.load("txt.png")
# Escalar la imagen del título (opcional)
titulo = pygame.transform.scale(titulo, (450, 100))  # Ajusta el tamaño según lo necesites

# Carga la imagen de la etiqueta
etiqueta = pygame.image.load("nombretxt.png")  # Cargar la imagen de la etiqueta
etiqueta = pygame.transform.scale(etiqueta, (120, 70))  # Ajusta el tamaño según lo necesites

# Carga la imagen de fondo
FONDO = pygame.image.load("inicio.png")
# Escalar la imagen al tamaño de la pantalla
FONDO = pygame.transform.scale(FONDO, (screen_width, screen_height))

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BUTTON_COLOR = (111, 187, 198)
BUTTON_HOVER_COLOR = (0, 200, 0)  # Color del botón al pasar el mouse
FONT_COLOR = (0, 0, 0)
INPUT_BACKGROUND_COLOR = (156, 203, 209)  # Color de fondo para la entrada de texto

font = pygame.font.Font(None, 36)

# Variables para la entrada de texto
nombre_jugador = ""
input_active = False

def mostrar_texto(texto, x, y, color=FONT_COLOR):
    texto_renderizado = font.render(texto, True, color)
    screen.blit(texto_renderizado, (x, y))

def pantalla_inicio():
    global nombre_jugador, input_active
    while True:
        # Dibuja el fondo
        screen.blit(FONDO, (0, 0))  # Coloca la imagen de fondo en la esquina superior izquierda

        # Dibuja la imagen del título
        screen.blit(titulo, (200, 10))  # Centra el título en la parte superior

        # Dibuja la imagen de la etiqueta
        screen.blit(etiqueta, (350, 450))  # Centra la etiqueta

        # Dibuja el fondo del cuadro de entrada de texto
        input_box = pygame.Rect(310, 530, 200, 50)  # Definición del cuadro de entrada
        pygame.draw.rect(screen, INPUT_BACKGROUND_COLOR, input_box)  # Color de fondo

        # Mostrar el texto solo dentro del cuadro de entrada
        mostrar_texto(nombre_jugador, input_box.x + 5, input_box.y + 5, FONT_COLOR)  # Mostrar el texto dentro del cuadro

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if input_active:  # Si el cuadro de texto está activo
                    if event.key == pygame.K_RETURN and nombre_jugador:  # Presiona Enter
                        print(f"Nombre ingresado: {nombre_jugador}")  # Imprime el nombre en la terminal
                        return  # Salir de la pantalla de inicio
                    elif event.key == pygame.K_BACKSPACE:  # Presiona Retroceso
                        nombre_jugador = nombre_jugador[:-1]  # Elimina el último carácter
                    else:
                        # Verificar si el carácter ingresado es una letra y que la longitud no supere 10 caracteres
                        if len(nombre_jugador) < 10 and event.unicode.isalpha():  
                            nombre_jugador += event.unicode  # Agrega el carácter ingresado
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Verificar si el botón izquierdo del mouse fue presionado
                    input_active = input_box.collidepoint(event.pos)  # Activar/desactivar el cuadro de texto

            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                input_active = input_box.collidepoint(mouse_x, mouse_y)

        pygame.display.flip()

pantalla_inicio()

pygame.quit()
