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

fondo_image = pygame.image.load("cesped.png")
fondo_image = pygame.transform.scale(fondo_image, (800, 600))

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

try:
    icon = pygame.image.load("conejo.ico")
    pygame.display.set_icon(icon)
except pygame.error as e:
    print(f"Error al cargar el ícono: {e}")

pygame.display.set_caption("Brain Scape")

try:
    image_jugador = pygame.image.load("conejin.png")
    image_jugador = pygame.transform.scale(image_jugador, (40, 40))
    image_jugador_rect = image_jugador.get_rect(center=(screen_width // 2, screen_height - 50))
except pygame.error as e:
    print(f"Error al cargar la imagen del jugador: {e}")

try:
    tronco_image = pygame.image.load('tronco.png')
    tronco_image = pygame.transform.scale(tronco_image, (50, 20))
except pygame.error as e:
    print(f"Error al cargar la imagen del obstáculo: {e}")

troncos = []
tronco_count = 5

class Tronco:
    def __init__(self, position, direction):
        self.image = tronco_image
        self.rect = self.image.get_rect(center=position)
        self.direction = direction

    def move(self):
        self.rect.x += move_speed * self.direction
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.direction *= -1

troncos = [
    Tronco((400, screen_height // 2), random.choice([1, -1])),
    Tronco((100, screen_height // 2), random.choice([1, -1])),
    Tronco((700, screen_height // 2), random.choice([1, -1])),
    Tronco((300, screen_height // 2), random.choice([1, -1])),

    Tronco((700, 60), random.choice([1, -1])),
    Tronco((300, 60), random.choice([1, -1])),
    Tronco((400, 60), random.choice([1, -1])),
    Tronco((100, 60), random.choice([1, -1])),

    Tronco((100, 180), random.choice([1, -1])),
    Tronco((300, 180), random.choice([1, -1])),
    Tronco((700, 180), random.choice([1, -1])),
    Tronco((400, 180), random.choice([1, -1])),

    Tronco((100, 400), random.choice([1, -1])),
    Tronco((300, 400), random.choice([1, -1])),
    Tronco((700, 400), random.choice([1, -1])),
    Tronco((400, 400), random.choice([1, -1])),
    
    Tronco((100, 480), random.choice([1, -1])),
    Tronco((300, 480), random.choice([1, -1])),
    Tronco((700, 480), random.choice([1, -1])),
    Tronco((400, 480), random.choice([1, -1])),
]

WHITE = (255, 255, 255)
RED = (255, 0, 0)

move_speed = 5
pause = False

def move_troncos():
    global pause
    while True:
        if not pause:
            for tronco in troncos:
                tronco.move()
        time.sleep(0.02)

move_thread = threading.Thread(target=move_troncos)
move_thread.daemon = True
move_thread.start()

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_p:
                pause = not pause
                pygame.mixer.music.set_volume(0.1 if pause else 0.3)

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            image_jugador_rect.x -= move_speed
        if keys[pygame.K_RIGHT]:
            image_jugador_rect.x += move_speed
        if keys[pygame.K_UP]:
            image_jugador_rect.y -= move_speed
        if keys[pygame.K_DOWN]:
            image_jugador_rect.y += move_speed

        image_jugador_rect.clamp_ip(screen.get_rect())

        for tronco in troncos:
            if image_jugador_rect.colliderect(tronco.rect):
                game_over = True

    if game_over:
        screen.fill(RED)
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)
    else:
        for x in range(0, screen_width, fondo_image.get_width()):
            for y in range(0, screen_height, fondo_image.get_height()):
                screen.blit(fondo_image, (x, y))
        
        for tronco in troncos:
            screen.blit(tronco.image, tronco.rect)
        screen.blit(image_jugador, image_jugador_rect)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
