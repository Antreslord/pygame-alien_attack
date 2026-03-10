"""Clases concretas de proyectiles del jugador y enemigos"""

from settings import game_characters, background_music
from src.bullets.base import Bullet


class BasicBullet(Bullet):

    def __init__(self, positionX, positionY, direction):
        super().__init__(
            positionX, positionY,
            character_image=game_characters["bullets"]["player"][0],
            sound=background_music["sounds"]["shooting"]["shooting_generic"],
            direction=direction,
        )
        self.damage = 50


class EnergyBall(Bullet):

    def __init__(self, positionX, positionY):
        super().__init__(
            positionX, positionY,
            character_image=game_characters["bullets"]["enemies"][0],
            sound=background_music["sounds"]["shooting"]["energy_ball"],
            speed=1.5,
            direction="down",
        )
        self.damage = 25
