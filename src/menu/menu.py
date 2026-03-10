import pygame

class Button:
    """ Clase para la creacion de botones independientes"""
    def __init__(self, x, y, width, height, text, color, hover_color):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color =color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 36)
        

    def draw(self, screen):
        """Dibujara el boton(es)"""
        mouse_pos = pygame.mouse.get_pos()
        
        # efecto hover
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color =  self.color
            
        # dibujar el rectangulo del boton
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)
        
        
        # dibujar el texto
        text_surface = self.font.render(self.text, True, (125, 125, 125))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, event):
        """Retorna el tipo de boton que se oprimio"""
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
                
        return False


class MenuWithButtons:
    """Menu de opciones en general"""
    
    def __init__(self, screen):
        self.screen = screen
        width, height =  screen.get_size()
        self.running = True
        
        
        # Crear los botones
        self.buttons = {
            'start': Button(width//2 - 100, 250, 200, 50, "Jugar", (0, 100, 0), (0, 200, 0)),
            'options': Button(width//2 - 100, 320, 200, 50, "Opciones", (100, 100, 0), (200, 200, 0)),
            'quit': Button(width//2 - 100, 390, 200, 50, "Salir", (100, 0, 0), (200, 0, 0))
        }
        
    def draw(self):
        """dibuja el menu completo"""
        self.screen.fill((0, 0, 0))
        
        # Título
        font_large = pygame.font.Font(None, 74)
        title = font_large.render("ALIEN ATTACK", True, (125, 125, 125))
        title_rect = title.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title, title_rect)
        
        # dibujar botones
        for button in self.buttons.values():
            button.draw(self.screen)
        
        pygame.display.flip()
        
    def run(self):
        """Ejecuta el menú y retorna la acción seleccionada"""
        clock = pygame.time.Clock()
        
        while self.running:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if self.buttons['start'].is_clicked(event):
                    return "start_game"
                elif self.buttons['options'].is_clicked(event):
                    return "options"
                elif self.buttons['quit'].is_clicked(event):
                    return "quit"
            
            self.draw()
        
        return "quit"
                                    