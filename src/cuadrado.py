import pygame ,sys

pygame.init()


#definir colores
black=(0,0,0)
white= (255,255,255)
green= (0,255,0)
red=(255,0,0)
blue=(0,0,255)

size=(800,600)

#crear ventana
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

cord_x=350
cord_y=250

#velocidad
speed_x=3
speed_y=3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #poner color de fondo
    #---LOGICA
    cord_x=cord_x+speed_x
    cord_y+=speed_y
    if cord_x > 700 or cord_x < 0 :
        speed_x*=-1
    if cord_y > 500 or cord_y < 0:
        speed_y*=-1
    #--- LOGICA
    screen.fill(white)
    #------------ZONA DE DIBUJO--------"
    """
    pygame.draw.line(screen,green,[0,100],[100,300],50 )
    pygame.draw.polygon(screen, black, [(100, 50), (150, 100), (50, 100)], 5)
    pygame.draw.rect(screen,blue,[700,200,40,20],50)
    pygame.draw.circle(screen,red,[400,300],100,50)
    pygame.draw.ellipse(screen,(50,125,0),(200,200,200,400),1

    for x in range (5,800,50):
        pygame.draw.rect(screen,blue,[x,200,40,20],50)
        pygame.draw.line(screen,black,(x,0),(x,100),15)"""
    pygame.draw.rect(screen,red,(cord_x,cord_y,100,100))
    pygame.draw.rect(screen,blue,(cord_x,cord_y,50,50))


    #ZONA DE DIBUJO#

    #actualizar pantalla
    pygame.display.flip()
    clock.tick(60)