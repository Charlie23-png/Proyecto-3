import pygame
import subprocess
import random  # Importa el módulo random para seleccionar mapas aleatorios

pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brain Scape")

# Colores y fuentes
INPUT_BACKGROUND_COLOR = (216, 187, 255)  # Color de fondo del cuadro de texto
FONT_COLOR = (0, 0, 0)  # Color del texto
FONT = pygame.font.Font(None, 32)

# Función para mostrar texto en pantalla
def mostrar_texto(texto, x, y, color):
    text_surface = FONT.render(texto, True, color)
    screen.blit(text_surface, (x, y))

# Carga la imagen de fondo de inicio
FONDO = pygame.image.load(r"bgmain\inicio2.png")
FONDO = pygame.transform.scale(FONDO, (screen_width, screen_height))

# Carga la imagen del botón de inicio
bottonStart = pygame.image.load(r"bgmain\bottonstar.png")
bottonStart = pygame.transform.scale(bottonStart, (170, 120))

def pantalla_inicio():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos  
                    if (320 < mouse_x < 490) and (350 < mouse_y < 470):
                        print("¡Botón de inicio presionado!")  
                        segunda_pantalla()

        screen.blit(FONDO, (0, 0))  
        screen.blit(bottonStart, (320, 350))  
        pygame.display.flip()  

    pygame.quit()

fondop2 = pygame.image.load(r"bgmain\pantalla2.png")
fondop2 = pygame.transform.scale(fondop2, (screen_width, screen_height))

bottonRegistro = pygame.image.load(r"bgmain\bottonregistro.png")
bottonRegistro = pygame.transform.scale(bottonRegistro, (170, 120)) 

fondoRegistro = pygame.image.load(r"bgmain\FONDO_REGISTRO.png")
fondoRegistro = pygame.transform.scale(fondoRegistro, (screen_width, screen_height))

bottonLogin = pygame.image.load(r"bgmain\bottonlogin.png")
bottonLogin = pygame.transform.scale(bottonLogin, (170, 120))  

fondologin = pygame.image.load(r"bgmain\FONDO_LOGIN.png")
fondologin = pygame.transform.scale(fondologin, (screen_width, screen_height))

def pantalla_registro():
    nombre_jugador = ""
    input_active = True
    running = True

    while running:
        screen.blit(fondoRegistro, (0, 0))  # Dibuja el fondo de registro

        # Dibuja el cuadro de entrada con un color de fondo
        input_box = pygame.Rect(310, 200, 200, 50)
        pygame.draw.rect(screen, INPUT_BACKGROUND_COLOR, input_box)  # Dibuja el fondo del cuadro de texto

        # Mostrar el texto ingresado dentro del cuadro
        mostrar_texto(nombre_jugador, input_box.x + 5, input_box.y + 15, FONT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        print(f"Nombre ingresado: {nombre_jugador}")
                        running = False  # Salir de la pantalla de registro y volver a la pantalla de inicio
                    elif event.key == pygame.K_BACKSPACE:
                        nombre_jugador = nombre_jugador[:-1]
                    elif len(nombre_jugador) < 10:
                        nombre_jugador += event.unicode  # Agregar el carácter ingresado
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    input_active = input_box.collidepoint(event.pos)  # Activar el cuadro si se hace clic sobre él

        pygame.display.flip()

    pantalla_inicio() 

def pantalla_login():
    nombre_usuario = ""
    input_active = True
    running = True

    while running:
        screen.blit(fondologin, (0, 0))  
        input_box = pygame.Rect(310, 200, 200, 50)
        pygame.draw.rect(screen, INPUT_BACKGROUND_COLOR, input_box)  

        mostrar_texto(nombre_usuario, input_box.x + 5, input_box.y + 15, FONT_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        print(f"Usuario ingresado: {nombre_usuario}")
                        running = False  
                    elif event.key == pygame.K_BACKSPACE:
                        nombre_usuario = nombre_usuario[:-1]
                    elif len(nombre_usuario) < 10:
                        nombre_usuario += event.unicode 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    input_active = input_box.collidepoint(event.pos) 
        pygame.display.flip()

    deslizar_pantallas()  

def segunda_pantalla():
    current_fondo = fondop2  
    mostrar_botones = True  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    mouse_x, mouse_y = event.pos  
                    if mostrar_botones and (320 < mouse_x < 490) and (350 < mouse_y < 470):
                        print("¡Botón de registro presionado!")  
                        pantalla_registro()  
                        current_fondo = fondoRegistro  
                        mostrar_botones = False  

                    elif mostrar_botones and (320 < mouse_x < 490) and (220 < mouse_y < 340):
                        print("¡Botón de login presionado!")  
                        pantalla_login()  
                        current_fondo = fondologin  
                        mostrar_botones = False  

        screen.blit(current_fondo, (0, 0))  

        if mostrar_botones:
            screen.blit(bottonRegistro, (320, 350))
            screen.blit(bottonLogin, (320, 220))

        pygame.display.flip()

    pygame.quit()

# Lista de mapas y archivos Python asociados
mapas = [
    pygame.image.load(r"bgmain\bosque.png"),
    pygame.image.load(r"bgmain\city.png"),
    pygame.image.load(r"bgmain\desierto.png"),
    pygame.image.load(r"bgmain\marte.png"),
    pygame.image.load(r"bgmain\playa.png")
]
mapas = [pygame.transform.scale(mapa, (screen_width, screen_height)) for mapa in mapas]

archivos_python = [
    "mapa1.py",
    "mapa_city.py",
    "mapa_desierto.py",
    "mapa2.py",
    "mapa_playa.py"
]
def deslizar_pantallas():
    current_map_index = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_map_index is None:
                    current_map_index = 0
                    print(f"Seleccionando mapa inicial: {archivos_python[current_map_index]}")
                    subprocess.Popen(["python", archivos_python[current_map_index]])
                
                elif event.key == pygame.K_a and current_map_index is not None:
                    print("Cambiando a un mapa aleatorio...")
                    current_map_index = random.randint(0, len(mapas) - 1)
                    print(f"Seleccionando mapa aleatorio: {archivos_python[current_map_index]}")
                    subprocess.Popen(["python", archivos_python[current_map_index]])
                    continue  # Reinicia el bucle para cargar el nuevo mapa
        
        if current_map_index is not None:
            screen.blit(mapas[current_map_index], (0, 0))
        
        pygame.display.flip()
    
    pygame.quit()



# Inicia el juego en la pantalla de inicio
pantalla_inicio()
