import pygame, sys, random

pygame.init()
pygame.mixer.init()


screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

fondo=pygame.image.load('./fondos/fondo_pong.jpg').convert()
fondo = pygame.transform.scale(fondo, screen_size)

golpe_p1=pygame.mixer.Sound('./sonidos/pongP1.wav')
golpe_p2=pygame.mixer.Sound("./sonidos/pongP2.wav")
game_over_sound= pygame.mixer.Sound("./sonidos/game_over_pong.mp3")
point=pygame.mixer.Sound('./sonidos/point.mp3')
pausa_sound=pygame.mixer.Sound('./sonidos/pausa.mp3')
pausa_sound.set_volume(0.2)

pygame.mixer.music.load("./sonidos/music_pong.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) #para que se repita en loop

pausa=False

player_width = 15
player_height = 90

# coordenadas player1
player_1_coor_x = 20
player_1_coor_y = 255
player1_speed = 0

# coordenadas player2
player_2_coor_x = 765 
player_2_coor_y = 255
player2_speed = 0

game_over = False

# puntaje
puntos_jugador1 = 0
puntos_jugador2 = 0

# pelota
pelota_x = 400
pelota_y = 300
pelota_speed_x = 3
pelota_speed_y = 3

# Bucle principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       
    
        if event.type == pygame.KEYDOWN:
            # jugador 1
            if event.key == pygame.K_w:
                player1_speed = -3
            if event.key == pygame.K_s:
                player1_speed = 3
            # jugador 2
            if event.key == pygame.K_UP:
                player2_speed = -3
            if event.key == pygame.K_DOWN:
                player2_speed = 3
            if event.key ==pygame.K_p:
                pausa= not pausa
        

        if event.type == pygame.KEYUP:
            # jugador 1
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_speed = 0
            # jugador 2
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2_speed = 0
    if pausa:
            pausa_texto = pygame.font.SysFont(None, 40).render("PAUSA", True,(255,255,255))
            pausa_rect=pausa_texto.get_rect(center=(400,300))
            pausa_sound.play()
            screen.blit(pausa_texto,pausa_rect)
            pygame.display.flip()
            clock.tick(60)
            continue
    # rebote eje Y
    if pelota_y > 590 or pelota_y < 10:
        pelota_speed_y *= -1

    # si sale por derecha
    if pelota_x > 800:
        pelota_x = 400
        pelota_y = 300
        pelota_speed_x *= -1
        pelota_speed_y = random.randrange(-4,4)
        puntos_jugador1 += 1
        point.play()

    # si sale por izquierda
    if pelota_x < 0:
        pelota_x = 400
        pelota_y = 300
        pelota_speed_x *= -1
        pelota_speed_y = random.randrange(-4,4)
        puntos_jugador2 += 1
        point.play()
    
    # fondo
    screen.blit(fondo,[0,0])

    # dibujar jugadores y pelota
    player1 = pygame.draw.rect(screen, [255, 255, 255], (player_1_coor_x, player_1_coor_y, player_width, player_height))
    player2 = pygame.draw.rect(screen, [255, 255, 255], (player_2_coor_x, player_2_coor_y, player_width, player_height))
    pelota = pygame.draw.circle(screen, [255, 255, 255], (pelota_x, pelota_y), 10)

    # movimiento
    player_1_coor_y += player1_speed
    player_2_coor_y += player2_speed
    pelota_x += pelota_speed_x
    pelota_y += pelota_speed_y

    # colisiones con paletas
    if pelota.colliderect(player1) and pelota_speed_x < 0:
        pelota_speed_x *= -1
        golpe_p1.play()
    if pelota.colliderect(player2) and pelota_speed_x > 0:
        pelota_speed_x *= -1
        golpe_p2.play()

    # límites de jugadores
    player_1_coor_y = max(0, min(player_1_coor_y, 510))
    player_2_coor_y = max(0, min(player_2_coor_y, 510))

    # puntaje y nombres
    fuente_puntaje = pygame.font.SysFont(None, 100)
    fuente_jugador = pygame.font.SysFont(None, 40)
    texto1 = fuente_puntaje.render(str(puntos_jugador1), True, (255, 255, 255))
    texto2 = fuente_puntaje.render(str(puntos_jugador2), True, (255, 255, 255))
    nombre1 = fuente_jugador.render("Jugador 1", True, (255, 255, 255))
    nombre2 = fuente_jugador.render("Jugador 2", True, (255, 255, 255))

    screen.blit(texto1, (300, 10))
    screen.blit(texto2, (480, 10))
    screen.blit(nombre1, (250, 80))
    screen.blit(nombre2, (430, 80))

    if puntos_jugador1 >= 7 or puntos_jugador2 >= 7:
        game_over = True

    pygame.display.flip()
    clock.tick(60)

# --- Pantalla final ---
ganador = "¡Ganó el Jugador 1!" if puntos_jugador1 >= 7 else "¡Ganó el Jugador 2!"
fuente_final = pygame.font.SysFont(None, 80)
mensaje = fuente_final.render(ganador, True, (255, 255, 255))
mensaje_rect = mensaje.get_rect(center=(400, 250))
pygame.mixer.music.stop()

game_over_sound.play()

instruccion = pygame.font.SysFont(None, 40).render("Presiona Enter para salir", True, (200, 200, 200))
instruccion_rect = instruccion.get_rect(center=(400, 320))

while True:
    screen.fill((0, 0, 0))
    screen.blit(mensaje, mensaje_rect)
    screen.blit(instruccion, instruccion_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()
