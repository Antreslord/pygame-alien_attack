import pygame



class Enemy(pygame.sprite.Sprite):
    
    # constructor
    def __init__(self, positionX, positionY, character_image, health = 100, speed = 1):
        super().__init__()
        
        self.image = pygame.image.load(character_image).convert_alpha() # para que el fondo del enemigo sea transparente
        self.rect = self.image.get_rect(topleft=(positionX, positionY))
        self.mask = pygame.mask.from_surface(self.image) # mascara para la colision pixel a pixel
        
        self.speed = speed # Velocidad de caida o movimientos
        self.life = health
        self.end_screenX = 1 # 1 = derecha, -1 = izquierda
        self.end_screenY = 1 # 1 = abajo, -1 = arriba
    
    def receive_damage(self, damage):
        """Recibir daño y retornar True si el enemigo fue destruido"""
        self.life -= damage
        return self.life <= 0
