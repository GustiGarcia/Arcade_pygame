import pygame, sys, random

from sprites_space import Disparo, Enemigo

pygame.init()

# Configuración general
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

# Estados del juego
game_over = False
puntaje = 0
x_speed = 0
coord_x = 370
done = False

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

fondo_original = pygame.image.load('./fondos/fondo_space.jpg').convert()
fondo_adaptado = pygame.transform.scale(fondo_original, (800, 600))

# Grupos de sprites
grupo_disparos = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()

# Crear enemigos (3 filas x 5 columnas)
for fila in range(3):
    for columna in range(5):
        x = columna * 60 + 20
        y = fila * 50 + 20
        enemigo = Enemigo(x, y)
        grupo_enemigos.add(enemigo)

# Movimiento de enemigos
direccion = 1
velocidad = 10
bajar = 0

# Fuente para textos
fuente_grande = pygame.font.SysFont(None, 72)
fuente_puntaje = pygame.font.SysFont(None, 60)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_speed = -4
                if event.key == pygame.K_d:
                    x_speed = +4
                if event.key == pygame.K_SPACE:
                    if len(grupo_disparos) < 8:
                        nuevo_disparo = Disparo(coord_x + 3, 550)
                        otro_disparo = Disparo(coord_x + 60, 550)
                        grupo_disparos.add(nuevo_disparo, otro_disparo)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    x_speed = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True

    if not game_over:
        # Actualizar posición de la nave
        coord_x += x_speed
        coord_x = max(0, min(coord_x, 740))

        # Movimiento enemigos y detección de Game Over
        borde = False
        for enemigo in grupo_enemigos:
            if enemigo.rect.right >= 800 or enemigo.rect.left <= 0:
                borde = True
            if enemigo.rect.bottom >= 520:
                game_over = True

        if borde:
            direccion *= -1
            bajar = 15
        else:
            bajar = 0

        # Seleccionar sprite de la nave según dirección
        if x_speed > 0:
            sprite_actual = nave_derecha
        elif x_speed < 0:
            sprite_actual = nave_izquierda
        else:
            sprite_actual = nave_cenital

        # Colisiones disparo - enemigo
        for disparo in grupo_disparos:
            enemigos_impactados = pygame.sprite.spritecollide(disparo, grupo_enemigos, True)
            if enemigos_impactados:
                grupo_disparos.remove(disparo)
                puntaje += len(enemigos_impactados)

        # Actualizar y dibujar pantalla
        screen.blit(fondo_adaptado, (0, 0))
        screen.blit(sprite_actual, (coord_x, 520))
        screen.blit(fuente_puntaje.render(str(puntaje), True, (255, 255, 255)), (10, 10))

        grupo_disparos.update()
        grupo_disparos.draw(screen)

        grupo_enemigos.update(direccion * velocidad, bajar)
        grupo_enemigos.draw(screen)
    else:
        # Pantalla Game Over
        screen.blit(fondo_adaptado, (0, 0))
        mensaje1 = fuente_grande.render("GAME OVER", True, (255, 0, 0))
        mensaje2 = fuente_puntaje.render(f"Este es tu puntaje: {puntaje}", True, (255, 255, 255))
        mensaje3 = fuente_puntaje.render("Presiona ENTER para salir", True, (200, 200, 200))
        screen.blit(mensaje1, (250, 200))
        screen.blit(mensaje2, (220, 300))
        screen.blit(mensaje3, (170, 380))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
