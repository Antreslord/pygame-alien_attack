import pygame

class LevelManager():
    
    def __init__(self):
        self.current_level = 0
        self.enemies_total= 5
        self.enemies_speed = 1
        self.is_paused = False
    
    
    
    def next_level(self):
        """Aumenta la dificultad del nivel"""
        self.current_level += 1
        self.enemies_total += (self.current_level - 1) * 1
        self.enemies_speed += (self.current_level - 1) * 0.08
    
    def pause_level(self):
        self.is_pause = True
        
    def continue_level(self):
        self.is_pause = False
        
    def game_over(self,):
        """Ejecuta cuando el jugador ha perdido todas sus vidas"""
        self.current_level = 0
        
