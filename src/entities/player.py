import pygame
import math
from settings import game_characters, screen_properties

IMAGE = game_characters["player"]
SCREEN_WIDTH = screen_properties["width"]
SCREEN_HEIGHT = screen_properties["height"]


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(IMAGE).convert_alpha()
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        )
        self.mask = pygame.mask.from_surface(self.image) # utilizado para las colisiones mas exactas
        self.speed = 20

        self.posX = float(self.rect.x)
        self.posY = float(self.rect.y)
        
        # vidas del jugador
        self.lifes = 3
        
        self.time_relive = 0

    def update(self):
        mouseX, mouseY = pygame.mouse.get_pos()

        dirX = mouseX - self.posX
        dirY = mouseY - self.posY
        distance = math.hypot(dirX, dirY)

        if distance != 0:
            dirX /= distance
            dirY /= distance

        if distance > self.speed:
            self.posX += dirX * self.speed
            self.posY += dirY * self.speed
        else:
            self.posX = mouseX
            self.posY = mouseY

        self.rect.centerx = round(self.posX)
        self.rect.centery = round(self.posY)

        # Limitar movimiento a los bordes de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def player_destroyed(self, group):
        """Metodo para cuando el jugador sera destruido por balas o enemigos"""
        self.lifes -= 1
        group.remove(self)
        self.time_relive = pygame.time.get_ticks()
        print(self.lifes)
        
    def is_there_lifes(self):
        """Retorna si tiene mas vidas"""
        if self.lifes > 0:
            return True
        else:
            return False


    def relive_player(self, group):
        """dara un tiempo de esperan antes que aparezca"""
        now = pygame.time.get_ticks()
        
        if (now - self.time_relive)  > 3000:
            group.add(self)
            self.time_relive = 0