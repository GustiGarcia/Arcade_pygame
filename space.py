import pygame,sys

pygame.init()
screen= pygame.display.set_mode([800,600])
clock= pygame.time.Clock()
pygame.mouse.set_visible(0)

#velocidad y posicion nave 
x_speed=0
coord_x=370

done=False

#cargar sprites
sprite_sheet = pygame.image.load('./recursos/nave_sheet.png').convert_alpha()

#tamaño de cada sprite 
sprite_ancho = 512
sprite_alto=512

#recortar cada sprite
nave_cenital= sprite_sheet.subsurface(pygame.Rect(0,0,sprite_ancho,sprite_alto))
nave_derecha= sprite_sheet.subsurface(pygame.Rect(sprite_ancho,0,sprite_ancho,sprite_alto))
nave_izquierda= sprite_sheet.subsurface(pygame.Rect(sprite_ancho*2,0,sprite_ancho,sprite_alto))

#redimensionar
nave_cenital=pygame.transform.scale(nave_cenital,(80,80))
nave_derecha=pygame.transform.scale(nave_derecha,(90,90))
nave_izquierda=pygame.transform.scale(nave_izquierda,(90,90))


fondo_original=pygame.image.load('./fondos/fondo_space.jpg').convert()
fondo_adaptado=pygame.transform.scale(fondo_original,(800,600))
nave=pygame.image.load('./recursos/ship.png').convert_alpha()
nave_grande=pygame.transform.scale(nave,(60,60))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
    
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                x_speed= -4
            if event.key == pygame.K_d:
                x_speed= +4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                x_speed= 0
            if event.key == pygame.K_d:
                x_speed= 0

    coord_x += x_speed

    if x_speed > 0:
        sprite_actual= nave_derecha
    elif x_speed < 0:
        sprite_actual= nave_izquierda
    else:
        sprite_actual= nave_cenital


    #limitar x

    if coord_x < 0 :
        coord_x = 0
    if coord_x > 740:
        coord_x= 740

    screen.blit(fondo_adaptado,(0,0))
    screen.blit(sprite_actual,[coord_x,520])
   
    
    """ancho,alto=nave.get_size()
    print((ancho), (alto))"""
    

    pygame.display.flip()
    clock.tick(60)
pygame.quit()