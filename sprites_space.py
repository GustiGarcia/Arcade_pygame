import pygame  # Importa la librería pygame

# Clase Disparo que hereda de Sprite (permite usar grupos, colisiones, etc.)
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Inicializa correctamente como Sprite

        # Crea una superficie de 5x15 píxeles (el "aspecto" visual del disparo)
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 0, 0))  # Rellena la superficie con color rojo

        # Obtiene el rectángulo que rodea la imagen (se usa para posición y colisiones)
        self.rect = self.image.get_rect()
        self.rect.centerx = x     # Posición horizontal (centro del disparo) igual a x (posición de la nave)
        self.rect.bottom = y      # El disparo comienza desde la parte superior de la nave (y)

        self.speed = -5  # Velocidad vertical negativa: se moverá hacia arriba

    def update(self):
        # Mueve el disparo hacia arriba
        self.rect.y += self.speed

        # Si el disparo sale de la pantalla por arriba, se elimina automáticamente
        if self.rect.bottom < 0:
            self.kill()



class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("./recursos/green.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dx, dy):
        # Moverse en x (izquierda/derecha) y y (bajar)
        self.rect.x += dx
        self.rect.y += dy

        
