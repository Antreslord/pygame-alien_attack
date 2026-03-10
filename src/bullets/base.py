"""Clase base para proyectiles"""

import pygame
from pygame import mixer
from settings import screen_properties

SCREEN_WIDTH = screen_properties["width"]
SCREEN_HEIGHT = screen_properties["height"]


class Bullet(pygame.sprite.Sprite):

    def __init__(self, positionX, positionY, character_image, sound, speed=2, direction="up"):
        super().__init__()

        self.image = pygame.image.load(character_image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(positionX, positionY))
        self.speed = speed
        self.sound = mixer.Sound(sound)
        self.sound.set_volume(0.4)
        self.direction = direction

        # Rotar imagen segun direccion
        if self.direction == "left":
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center=(positionX - 32, positionY + 32))
        elif self.direction == "right":
            self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect(center=(positionX + 32, positionY + 32))
        elif self.direction == "down":
            self.image = pygame.transform.rotate(self.image, 180)
            self.rect = self.image.get_rect(center=(positionX, positionY + 64))

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Eliminar si sale de la pantalla
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
            self.sound.stop()

    def play_shooting_sound(self):
        self.sound.play()

    def stop_shooting_sound(self):
        self.sound.stop()
