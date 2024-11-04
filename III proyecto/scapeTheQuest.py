import pygame
import threading
import time

# Inicializar Pygame
pygame.init()

# Inicializar Pygame y el módulo de sonido
pygame.init()
pygame.mixer.init()  # Inicializar el mezclador de sonidos

# Cargar y reproducir la música de fondo
pygame.mixer.music.load("musicaFondo.mp3")  # Cargar la música (puede ser .mp3, .ogg, etc.)
pygame.mixer.music.play(-1)  # Reproducir en bucle (-1 significa que se repetirá indefinidamente)
pygame.mixer.music.set_volume(0.3)

# Configuración de la pantalla
screen_info = pygame.display.Info()
screen_width = screen_info.current_w    #ancho de la pantalla según la resolución del monitor
screen_height = screen_info.current_h   #alto de la pantalla según la resolución del monitor

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Cargar la imagen del ícono
icon = pygame.image.load("conejo.ico")

# Establecer el ícono de la ventana
pygame.display.set_icon(icon)

pygame.display.set_caption("Scape The Quest") #Visible solo en modo ventana tradicional

# Cargar la imagen que se va a mover
image_jugador = pygame.image.load("conejo.png") 
image_jugador_rect = image_jugador.get_rect()  # Obtener el rectángulo de la imagen, se utiliza para procesar mejor las dimensiones de las imágenes y con esto establer posibles choques del jugador con los obstáculos
image_jugador_rect.topleft = (screen_width // 2, screen_height // 2)  # Posición inicial en el centro

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Cargar la imagen del obstáculo
image = pygame.image.load('tronco.png')
image_rect = image.get_rect()
image_rect.y = screen_height // 2 - image_rect.height // 2  # Centrar verticalmente

# Variables de movimiento
move_speed = 5  # Velocidad de movimiento en píxeles
moving_right = True  # Dirección inicial del obstáculo
pause = False #pone pausa al juego

# Función para mover la imagen del obstáculo verifica que la misma no se salga de la ventana y alterna el sentido de iz a derecha
def move_image():
    global moving_right, image_rect, pause
    while True:                     #OJO AQUI: al ser un ciclo while True el proceso se ciclaría en este punto por lo que adelante se lanzará un hilo de ejecución solo con esta función para que de forma paralela corran la tareas de los obstáculo y del movimiento de jugador al mismo tiempo
        if not pause:
            if moving_right:
                image_rect.x += move_speed
                if image_rect.right >= screen_width:
                    moving_right = False
            else:
                image_rect.x -= move_speed
                if image_rect.left <= 0:
                    moving_right = True
        time.sleep(0.02)  # Controlar la velocidad de actualización

# Crear y comenzar el hilo para mover la imagen del obstáculo
move_thread = threading.Thread(target=move_image)
move_thread.daemon = True  # Hilo en modo demonio para que se cierre con el programa
move_thread.start() #Inicializa el hilo que hace mover el obstáculo

# Bucle principal de Pygame 
# Esta siempre verificando los eventos del teclado y las actualizaciones de la ventana

running = True
while running:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:   #Sale del ciclo y cierra la aplicación cuando el usuario cierra la venta en modo ventana tradicional
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    #Sale del ciclo y cierra la aplicación cuando se preciona escape
                running = False
            if event.key == pygame.K_p: #Pone pausa al movimiento de los obstáculos
                pause = not pause
                if pause:
                    pygame.mixer.music.set_volume(0.1)
                else:
                    pygame.mixer.music.set_volume(0.3)

    # Obtener el estado de todas las teclas, el capturar la teclas en este punto y no en el evento anterior permite mantener una acción repetida al momento de mantener las teclas presionadas para mantener un flujo de movimiento constante del jugador
    keys = pygame.key.get_pressed()

    # Mover la imagen en base a las teclas presionadas
    if keys[pygame.K_LEFT]:
        image_jugador_rect.x -= move_speed  # Mover hacia la izquierda
    if keys[pygame.K_RIGHT]:
        image_jugador_rect.x += move_speed  # Mover hacia la derecha
    if keys[pygame.K_UP]:
        image_jugador_rect.y -= move_speed  # Mover hacia arriba
    if keys[pygame.K_DOWN]:
        image_jugador_rect.y += move_speed  # Mover hacia abajo

    # Evitar que la imagen salga de la pantalla
    if image_jugador_rect.left < 0:
        image_jugador_rect.left = 0
    if image_jugador_rect.right > screen_width:
        image_jugador_rect.right = screen_width
    if image_jugador_rect.top < 0:
        image_jugador_rect.top = 0
    if image_jugador_rect.bottom > screen_height:
        image_jugador_rect.bottom = screen_height

    if image_rect.colliderect(image_jugador_rect): #Esta función de los objetos rect perimiten evaluar choque de dos rectángulos que representan las dimensiones y posiciones de las imágenes del jugador y los obstáculos
        screen.fill(RED)
    else:
        screen.fill(WHITE)

    # Dibujar las imagenes en la nueva posición, esta redibuja las imágenes para actualizar su posición pero no se refresca este cambio hasta que se aplique la función flip() 
    screen.blit(image, image_rect)
    screen.blit(image_jugador, image_jugador_rect)

    # Actualizar la pantalla, pygame trabaja con una doble pantalla una por debajo que repinta los objetos cuando son actualizado y al aplicar flip cambia la imagen de abajo por la visible para dar una actualización más adecuada
    pygame.display.flip()

    # Controlar el framerate
    pygame.time.Clock().tick(60)

# Salir de Pygame
pygame.quit()
