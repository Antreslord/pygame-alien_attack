"""
Configuraciones del juego
"""

from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent
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
        "background1": str(IMG_DIR / "backgrounds" / "geralt-galaxy-4799471_600x900.jpg"),
    },
    "icon": str(IMG_DIR / "games_icon.png"),
}

# Musica y Sonidos
background_music = {
    "music": [str(SOUNDS_DIR / "bensound-prism.mp3")],
    "sounds": {
        "player": {},
        "enemies": {},
        "environment": {},
        "shooting": {
            "shooting_generic": str(SOUNDS_DIR / "shoot1.mp3"),
            "energy_ball": str(SOUNDS_DIR / "energy_ball.mp3"),
        },
        "explosions": str(SOUNDS_DIR / "explosion.mp3"),
    },
}

# Personajes y Objetos
game_characters = {
    "player": str(IMG_DIR / "player" / "nave_player_64px.png"),
    "enemies": [
        str(IMG_DIR / "enemies" / "ufo1_64px.png"),
        str(IMG_DIR / "enemies" / "ufo_64px_1.png"),
    ],
    "bullets": {
        "player": [str(IMG_DIR / "bullets" / "bullet_normal.png")],
        "enemies": [str(IMG_DIR / "bullets" / "energy_ball_1.png")],
    },
    "explosions": [
        str(IMG_DIR / "explosions" / f"sec_boom_{i}.png")
        for i in range(1, 8)
    ],
}
