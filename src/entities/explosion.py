import pygame
from pygame import mixer
from settings import game_characters, background_music

EXPLOSION_FRAMES = game_characters["explosions"]


class Explosion(pygame.sprite.Sprite):

    def __init__(self, positionX, positionY):
        super().__init__()

        self.frames = [pygame.image.load(img).convert_alpha() for img in EXPLOSION_FRAMES]
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(positionX, positionY))

        self.frame_index = 0
        self.last_update = 0
        self.animation_speed = 90
        self.explosion_sound = mixer.Sound(background_music["sounds"]["explosions"])

    def update(self):
        now = pygame.time.get_ticks()

        if (now - self.last_update) > self.animation_speed:
            self.last_update = now
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.kill()
                return

            self.image = self.frames[self.frame_index]

    def play_explosion_sound(self):
        self.explosion_sound.play()
