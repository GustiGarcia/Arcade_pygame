import pygame, random  # Importa la librería pygame



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
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass  # Ya no hace movimiento acá

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, imagenes, velocidad_ms=200):
        super().__init__()
        self.imagenes = imagenes
        self.indice = 0
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect(center=(x, y))
        self.tiempo_actual = pygame.time.get_ticks()
        self.velocidad_ms = velocidad_ms  # Tiempo entre cuadros en milisegundos

    def update(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_actual > self.velocidad_ms:
            self.tiempo_actual = ahora
            self.indice += 1
            if self.indice < len(self.imagenes):
                self.image = self.imagenes[self.indice]
            else:
                self.kill()




class Nave(pygame.sprite.Sprite):
    def __init__(self, cenital, izquierda, derecha):
        super().__init__()
        self.imagen_cenital = cenital
        self.imagen_izquierda = izquierda
        self.imagen_derecha = derecha

        self.image = self.imagen_cenital
        self.rect = self.image.get_rect()
        self.rect.center = (400, 560)
        self.velocidad = 4

    def update(self, teclas):
        if teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
            self.image = self.imagen_izquierda
        elif teclas[pygame.K_d]:
            self.rect.x += self.velocidad
            self.image = self.imagen_derecha
        else:
            self.image = self.imagen_cenital
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
