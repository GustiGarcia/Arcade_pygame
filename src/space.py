import pygame, sys, random
from sprites_space import Disparo, Enemigo, Explosion, Nave


def main():
    pygame.init()
    pygame.mixer.init()

    # --- Sonidos (RUTAS ACTUALIZADAS) ---
    sonido_disparo = pygame.mixer.Sound('assets//space_shot.mp3')
    sonido_disparo.set_volume(0.1)
    sonido_enemigo_abatido = pygame.mixer.Sound("assets//enemy_down.ogg")
    sonido_nave_exp = pygame.mixer.Sound('assets//explosion_nave.wav')
    sonido_game_over = pygame.mixer.Sound('assets//game_over_space.mp3')

    pygame.mixer.music.load('assets//fondo_space.ogg')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)

    # --- Pantalla ---
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)

    # --- Enemigos (RUTAS ACTUALIZADAS) ---
    imagenes_enemigos = [
        pygame.image.load("assets//green.png").convert_alpha(),
        pygame.image.load("assets//red.png").convert_alpha(),
        pygame.image.load("assets//yellow.png").convert_alpha()
    ]

    # Variables
    game_over = False
    mostrar_game_over = False
    puntaje = 0
    done = False
    x_speed = 0

    # Explosiones (RUTAS ACTUALIZADAS)
    imagenes_explosion = []
    for i in range(1, 4):
        img = pygame.image.load(f'assets//explosion{i}.png').convert_alpha()
        img = pygame.transform.scale(img, (80, 80))
        imagenes_explosion.append(img)

    explosion_activa = False

    # Sprite nave (RUTAS ACTUALIZADAS)
    sprite_sheet = pygame.image.load('assets//nave_sheet.png').convert_alpha()
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

    # Fondo (RUTA ACTUALIZADA)
    fondo_original = pygame.image.load('assets//fondo_espacial2.png').convert()
    fondo_adaptado = pygame.transform.scale(fondo_original, (800, 600))

    # Grupos
    grupo_disparos = pygame.sprite.Group()
    grupo_enemigos = pygame.sprite.Group()
    grupo_explosiones = pygame.sprite.Group()

    # Crear primera oleada
    def crear_oleada():
        imagen_elegida = random.choice(imagenes_enemigos)
        for fila in range(3):
            for columna in range(5):
                x = columna * 60 + 20
                y = fila * 50 + 20
                enemigo = Enemigo(x, y, imagen_elegida)
                grupo_enemigos.add(enemigo)

    crear_oleada()

    direccion = 1
    velocidad = 8
    bajar_pixels = 0
    VELOCIDAD_MAXIMA = 20
    ultimo_descenso = 0
    tiempo_entre_descensos = 500
    tiempo_proxima_oleada = 0
    intervalo_oleada = 3000

    fuente_grande = pygame.font.SysFont(None, 72)
    fuente_puntaje = pygame.font.SysFont(None, 60)

    # --- Bucle principal ---
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
                    if event.key in (pygame.K_a, pygame.K_d):
                        x_speed = 0

        # Movimiento de juego
        if not game_over:
            nave.rect.x += x_speed
            nave.rect.x = max(0, min(nave.rect.x, 720))

            # Colisión
            if pygame.sprite.spritecollide(nave, grupo_enemigos, False):
                game_over = True

            # Movimiento lateral enemigos
            for enemigo in grupo_enemigos:
                enemigo.rect.x += direccion * velocidad

            borde = any(e.rect.right >= 800 or e.rect.left <= 0 for e in grupo_enemigos)
            tiempo_actual = pygame.time.get_ticks()

            if borde and (tiempo_actual - ultimo_descenso > tiempo_entre_descensos):
                direccion *= -1
                for enemigo in grupo_enemigos:
                    enemigo.rect.y += 20
                ultimo_descenso = tiempo_actual

            # Disparos VS enemigos
            for disparo in grupo_disparos:
                enemigos_impactados = pygame.sprite.spritecollide(disparo, grupo_enemigos, True)
                if enemigos_impactados:
                    disparo.kill()
                    sonido_enemigo_abatido.play()
                    puntaje += len(enemigos_impactados)

            # Nueva oleada
            if tiempo_actual > tiempo_proxima_oleada and len(grupo_enemigos) == 0:
                if velocidad < VELOCIDAD_MAXIMA:
                    velocidad += 1.5
                crear_oleada()
                tiempo_proxima_oleada = tiempo_actual + intervalo_oleada

        # Dibujar
        screen.blit(fondo_adaptado, (0, 0))
        grupo_disparos.update()
        grupo_disparos.draw(screen)
        grupo_enemigos.draw(screen)
        grupo_nave.update(pygame.key.get_pressed())
        grupo_nave.draw(screen)

        score_surface = fuente_puntaje.render(str(puntaje), True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
