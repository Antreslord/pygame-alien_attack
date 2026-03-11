# settings.py
"""
Configuraciones del juego
"""
import sys
import os
from pathlib import Path

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta del recurso.
    Funciona tanto en desarrollo como en ejecutable PyInstaller.
    """
    try:
        # Cuando está compilado con PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Cuando se ejecuta como script normal
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Directorio base del proyecto
BASE_DIR = Path(get_resource_path("."))
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
SOUNDS_DIR = ASSETS_DIR / "sounds"

# Pantalla
screen_properties = {
    "title": "Alien: Invasion Attack",
    "width": 1200,
    "height": 650,
}

# Fondos de Pantalla
background_images = {
    "backgrounds": {
        "background1": get_resource_path("assets/img/backgrounds/geralt-galaxy-4799471_600x900.jpg"),
    },
    "icon": get_resource_path("assets/img/games_icon.png"),
}

# Musica y Sonidos
background_music = {
    "music": [get_resource_path("assets/sounds/bensound-prism.mp3")],
    "sounds": {
        "player": {},
        "enemies": {},
        "environment": {},
        "shooting": {
            "shooting_generic": get_resource_path("assets/sounds/shoot1.mp3"),
            "energy_ball": get_resource_path("assets/sounds/energy_ball.mp3"),
        },
        "explosions": get_resource_path("assets/sounds/explosion.mp3"),
    },
}

# Personajes y Objetos
game_characters = {
    "player": get_resource_path("assets/img/player/nave_player_64px.png"),
    "enemies": [
        get_resource_path("assets/img/enemies/ufo1_64px.png"),
        get_resource_path("assets/img/enemies/ufo_64px_1.png"),
    ],
    "bullets": {
        "player": [get_resource_path("assets/img/bullets/bullet_normal.png")],
        "enemies": [get_resource_path("assets/img/bullets/energy_ball_1.png")],
    },
    "explosions": [
        get_resource_path(f"assets/img/explosions/sec_boom_{i}.png")
        for i in range(1, 8)
    ],
}