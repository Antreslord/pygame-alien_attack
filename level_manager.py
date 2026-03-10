"""Este modulo gestionara y configurara el comportamiento del juego atraves de los niveles"""


import pygame

class LevelManager:
    
    def __init__(self):
        self.current_level = 1
        self.enemies_for_level = 5 # enemigos iniciales
        self.enemies_speed_for_level = 2
        self.enemies_shoot_delay = 2000 # tiempo de disparo de los enemigos
        self.level_complete = False # Boolean nivel completado
        
        """transiciones entre niveles"""
        self.level_transition_timer = 0
        self.is_transitioning = False


    def get_level_config(self, level):
        """Devuelve la configuracion de cada nivel"""

        return{
            "enemies_count": self.enemies_for_level + (level -1) * 3, # Aumentara 3 enemigos por nivel
            "enemies_speed": self.enemies_speed_for_level + (level -1) * 0.5 # Aumentara 0.5 de velocidada por nivel 
        }
    
    def start_level(self, level):
        """Prepara el inicio del nivel"""
        self.current_level = level
        self.level_complete = False
        self.is_transitioning = False
        print(f"NIVEL {level} INICIADO")
    
    def complete_level(self):
        """Marca el nivel como completado"""
        self.level_complete = True
        self.level_transition_timer = pygame.time.get_ticks()
        self.is_transitioning = True
        print(f"NIVEL {self.current_level} COMPLETADO")
    
    def next_level(self):
        """Prepara el siguiente nivel"""
        self.current_level += 1
        self.level_complete = False
        self.is_transitioning = False
        print(f"PREPARANDO NIVEL {self.current_level}")
        
    def is_transition_complete(self, transition_time=3000):
        """Verifica si termino la transicion entre niveles"""
        if not self.is_transitioning:
            return True
        
        now = pygame.time.get_ticks()
        return (now - self.level_transition_timer > transition_time)