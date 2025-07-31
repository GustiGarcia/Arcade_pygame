import pygame, sys, random
from sprites_space import Disparo, Enemigo, Explosion, Nave

pygame.init()

# Configuración general
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

# Estados del juego
game_over = False
mostrar_game_over = False
puntaje = 0
done = False
x_speed = 0  # inicializar variable que usás para mover la nave

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

fondo_original = pygame.image.load('./fondos/fondo_space.jpg').convert()
fondo_adaptado = pygame.transform.scale(fondo_original, (800, 600))

grupo_disparos = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()

def crear_oleada():
    for fila in range(3):
        for columna in range(5):
            x = columna * 60 + 20
            y = fila * 50 + 20
            enemigo = Enemigo(x, y)
            grupo_enemigos.add(enemigo)

crear_oleada()

direccion = 1
velocidad = 15
bajar = 0

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
                    if len(grupo_disparos) < 8:
                        d1 = Disparo(nave.rect.left + 5, nave.rect.top + 35)
                        d2 = Disparo(nave.rect.right - 20, nave.rect.top + 35)
                        grupo_disparos.add(d1, d2)
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

        # Movimiento enemigos y detección de Game Over
        for enemigo in grupo_enemigos:
            if enemigo.rect.colliderect(nave.rect) or enemigo.rect.bottom >= nave.rect.top:
                game_over = True
                if not explosion_activa:
                    explosion = Explosion(nave.rect.centerx, nave.rect.centery, imagenes_explosion, velocidad_ms=250)
                    grupo_explosiones.add(explosion)
                    explosion_activa = True

        borde = any(e.rect.right >= 800 or e.rect.left <= 0 for e in grupo_enemigos)

        if borde:
            direccion *= -1
            bajar = 15
        else:
            bajar = 0

        for disparo in grupo_disparos:
            enemigos_impactados = pygame.sprite.spritecollide(disparo, grupo_enemigos, True)
            if enemigos_impactados:
                disparo.kill()
                puntaje += len(enemigos_impactados)

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual > tiempo_proxima_oleada and len(grupo_enemigos) == 0:
            velocidad += 1
            crear_oleada()
            tiempo_proxima_oleada = tiempo_actual + intervalo_oleada

        # Actualizar y dibujar sprites
        screen.blit(fondo_adaptado, (0, 0))
        grupo_disparos.update()
        grupo_enemigos.update(direccion * velocidad, bajar)
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