import pygame, sys, random
from sprites_space import Disparo, Enemigo, Explosion, Nave

pygame.init()
pygame.mixer.init()


# carga de sonidos

sonido_disparo = pygame.mixer.Sound('./sonidos/space_shot.mp3')
sonido_disparo.set_volume(0.1)
sonido_enemigo_abatido = pygame.mixer.Sound("./sonidos/enemy_down.ogg")
sonido_nave_exp = pygame.mixer.Sound('./sonidos/explosion_nave.wav')
sonido_game_over = pygame.mixer.Sound('./sonidos/game_over_space.mp3')

pygame.mixer.music.load('./sonidos/fondo_space.ogg')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)


# Configuración general
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)


# marcianitos de colores
imagenes_enemigos = [
    pygame.image.load("./recursos/green.png").convert_alpha(),
    pygame.image.load("./recursos/red.png").convert_alpha(),
    pygame.image.load("./recursos/yellow.png").convert_alpha()
]


# Estados del juego
game_over = False
mostrar_game_over = False
puntaje = 0
done = False
x_speed = 0

# Explosión al perder
imagenes_explosion = []
for i in range(1, 4):
    img = pygame.image.load(f'./recursos/explosion{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    imagenes_explosion.append(img)

explosion_activa = False

# Tiempo de spawn de enemigos
tiempo_proxima_oleada = 0
intervalo_oleada = 3000  # milisegundos

# Cargar sprites
sprite_sheet = pygame.image.load('./recursos/nave_sheet.png').convert_alpha()
sprite_ancho = 512
sprite_alto = 512
nave_cenital = sprite_sheet.subsurface(pygame.Rect(0, 0, sprite_ancho, sprite_alto))
nave_derecha = sprite_sheet.subsurface(pygame.Rect(sprite_ancho, 0, sprite_ancho, sprite_alto))
nave_izquierda = sprite_sheet.subsurface(pygame.Rect(sprite_ancho * 2, 0, sprite_ancho, sprite_alto))
nave_cenital = pygame.transform.scale(nave_cenital, (80, 80))
nave_derecha = pygame.transform.scale(nave_derecha, (90, 90))
nave_izquierda = pygame.transform.scale(nave_izquierda, (90, 90))

nave = Nave(nave_cenital, nave_izquierda, nave_derecha)
grupo_nave = pygame.sprite.GroupSingle(nave)

fondo_original = pygame.image.load('./fondos/fondo_espacial2.png').convert()
fondo_adaptado = pygame.transform.scale(fondo_original, (800, 600))

grupo_disparos = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()

# Bandera para controlar si se acaba de crear una nueva oleada
nueva_oleada_activa = False

def crear_oleada():
    global nueva_oleada_activa
    imagen_elegida = random.choice(imagenes_enemigos)
    for fila in range(3):
        for columna in range(5):
            x = columna * 60 + 20
            y = fila * 50 + 20
            enemigo = Enemigo(x, y, imagen_elegida)
            grupo_enemigos.add(enemigo)
    nueva_oleada_activa = True

crear_oleada()

direccion = 1
velocidad = 8
bajar_pixels = 0

# Definir la velocidad máxima para los enemigos
VELOCIDAD_MAXIMA = 20

fuente_grande = pygame.font.SysFont(None, 72)
fuente_puntaje = pygame.font.SysFont(None, 60)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_speed = -2
                if event.key == pygame.K_d:
                    x_speed = +2
                if event.key == pygame.K_SPACE:
                    if len(grupo_disparos) < 6:
                        d1 = Disparo(nave.rect.left + 5, nave.rect.top + 35)
                        d2 = Disparo(nave.rect.right - 20, nave.rect.top + 35)
                        grupo_disparos.add(d1, d2)
                        sonido_disparo.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_speed = 0
        else:
            if mostrar_game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                done = True

    if not game_over:
        # Actualizar posición nave
        nave.rect.x += x_speed
        if nave.rect.left < 0:
            nave.rect.left = 0
        if nave.rect.right > 800:
            nave.rect.right = 800

        # Detección de Game Over por colisión con la nave o llegada al fondo
        if not nueva_oleada_activa:  # Solo revisamos la condición si la oleada ya está en movimiento
            if pygame.sprite.spritecollide(nave, grupo_enemigos, False) or any(e.rect.bottom >= 600 for e in grupo_enemigos):
                game_over = True
                
                if not explosion_activa:
                    explosion = Explosion(nave.rect.centerx, nave.rect.centery, imagenes_explosion, velocidad_ms=250)
                    grupo_explosiones.add(explosion)
                    explosion_activa = True
                    sonido_nave_exp.play()
        
        # Una vez que los enemigos se han movido en un frame, podemos desactivar la bandera
        if nueva_oleada_activa and len(grupo_enemigos) > 0:
            nueva_oleada_activa = False

        borde = any(e.rect.right >= 800 or e.rect.left <= 0 for e in grupo_enemigos)
        
        if borde:
            direccion *= -1
            bajar_pixels = 30 
        else:
            bajar_pixels = 0
            
        # Colisión de disparos con enemigos
        for disparo in grupo_disparos:
            enemigos_impactados = pygame.sprite.spritecollide(disparo, grupo_enemigos, True)
            if enemigos_impactados:
                disparo.kill()
                sonido_enemigo_abatido.play()
                puntaje += len(enemigos_impactados)

        # Crear nueva oleada si todos los enemigos han sido destruidos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual > tiempo_proxima_oleada and len(grupo_enemigos) == 0:
            if velocidad < VELOCIDAD_MAXIMA:
                velocidad += 1.5
            crear_oleada()
            tiempo_proxima_oleada = tiempo_actual + intervalo_oleada

        # Actualizar y dibujar sprites
        screen.blit(fondo_adaptado, (0, 0))
        grupo_disparos.update()
        grupo_enemigos.update(direccion * velocidad, bajar_pixels)
        grupo_nave.update(pygame.key.get_pressed())
        
        grupo_nave.draw(screen)
        grupo_disparos.draw(screen)
        grupo_enemigos.draw(screen)
        
        screen.blit(fuente_puntaje.render(str(puntaje), True, (255, 255, 255)), (10, 10))

    # Dibujar explosión si está activa
    if explosion_activa:
        grupo_explosiones.update()
        grupo_explosiones.draw(screen)
        
        # Verificar si la explosión terminó
        if len(grupo_explosiones) == 0:
            mostrar_game_over = True
            explosion_activa = False
            pygame.mixer.music.stop()
            sonido_game_over.play()

    # Mostrar pantalla de Game Over después de la explosión
    if mostrar_game_over:
        screen.blit(fondo_adaptado, (0, 0))

        # --- Título de Game Over ---
        msg1 = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        rect1 = msg1.get_rect(center=(800 // 2, 200))
        screen.blit(msg1, rect1)

        # --- Puntaje ---
        msg2 = fuente_puntaje.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        rect2 = msg2.get_rect(center=(800 // 2, 300))
        screen.blit(msg2, rect2)

        # --- Instrucción para salir ---
        msg3 = fuente_puntaje.render("Presiona ENTER para salir", True, (200, 200, 200))
        rect3 = msg3.get_rect(center=(800 // 2, 380))
        screen.blit(msg3, rect3)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()