import pygame
from settings import game_characters, screen_properties
from src.enemies.base import Enemy
from src.bullets.bullet import EnergyBall


class BasicEnemy(Enemy):

    def __init__(self, positionX, positionY):
        super().__init__(positionX, positionY, game_characters["enemies"][0])

    def update(self):
        self.rect.y += self.speed * self.end_screenY
        self.rect.x += self.speed * self.end_screenX

        # efecto de rebote en los limites de la pantalla
        if self.rect.bottom >= screen_properties["height"] or self.rect.top <= 0:
            self.end_screenY *= -1
        if self.rect.right >= screen_properties["width"] or self.rect.left <= 0:
            self.end_screenX *= -1


class ShooterEnemy(Enemy):

    def __init__(self, positionX, positionY, bullets_group, all_sprites):
        super().__init__(positionX, positionY, game_characters["enemies"][1], health=50)
        self.bullets_group = bullets_group
        self.all_sprites = all_sprites

        # temporizador para los disparos
        self.last_shoot = 0
        self.shoot_delay = 10000

    def try_shoot(self):
        """Dispara si paso suficiente tiempo desde el ultimo disparo"""
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            self.shoot()

    def shoot(self):
        """Crea una bala de energia"""
        bullet = EnergyBall(self.rect.centerx, self.rect.centery)
        bullet.play_shooting_sound()
        self.bullets_group.add(bullet)
        self.all_sprites.add(bullet)

    def update(self):
        self.rect.x += self.speed * self.end_screenX

        if self.rect.right >= screen_properties["width"] or self.rect.left <= 0:
            self.end_screenX *= -1

        self.try_shoot()
