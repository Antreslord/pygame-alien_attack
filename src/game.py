import pygame
from pygame import mixer
from random import randint
from typing import Optional

# Imports de configuración y entidades
from settings import background_images as imgs, screen_properties, background_music as games_sounds
from src.entities.player import Player
from src.bullets.bullet import BasicBullet
from src.enemies.enemy import BasicEnemy, ShooterEnemy
from src.entities.explosion import Explosion
from src.levelsmanager.level_manager import LevelManager
from src.menu.menu import MenuWithButtons

# Constantes de Pantalla
TITLE = screen_properties["title"]
WINDOW_WIDTH = screen_properties["width"]
WINDOW_HEIGHT = screen_properties["height"]
FPS = 60

# Constantes de Assets
ICON_PATH = imgs["icon"]
BACKGROUND_PATH = imgs["backgrounds"]["background1"]

# Constantes de Juego
DEFAULT_SHOOT_DIRECTION = "up"
ENEMY_Spawn_Y_MIN = 50
ENEMY_Spawn_Y_MAX = 300
SHOOTER_ENEMY_COUNT_DIVISOR = 3


class Game:
    """Clase principal que gestiona el bucle del juego, estados y renderizado."""

    def __init__(self) -> None:
        """Inicializa pygame, ventana, recursos y estados del juego."""
        pygame.init()
        mixer.init()

        # Configuración de ventana
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(pygame.image.load(ICON_PATH))
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.mouse.set_visible(True)

        # Configuración de Audio
        self._load_music()

        # Carga de Assets Gráficos
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        
        # Fuentes (Optimización: cargar una vez)
        self.font_ui = pygame.font.Font(None, 32)

        # Estados del Juego
        self.running = True
        self.clock = pygame.time.Clock()
        self.shoot_direction = DEFAULT_SHOOT_DIRECTION
        
        # estado del juego en el menu
        self.game_state = "menu"

        # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.enemy_bullets_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.explosions_group = pygame.sprite.Group()

        # Entidades
        self.player = Player()
        self.all_sprites.add(self.player)

        # Gestión de Niveles
        self.level_manager = LevelManager()
        self._spawn_enemies_for_level()

    def _load_music(self) -> None:
        """Carga y configura la música de fondo."""
        try:
            music_path = games_sounds["music"][0]
            mixer.music.load(music_path)
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)
        except (KeyError, FileNotFoundError) as e:
            print(f"Error cargando música: {e}")

    def _spawn_enemies_for_level(self) -> None:
        """Crea los enemigos según la configuración del nivel actual."""
        count = self.level_manager.enemies_total
        speed = self.level_manager.enemies_speed

        # Enemigos Básicos
        for _ in range(count):
            enemy = BasicEnemy(
                randint(0, WINDOW_WIDTH - 64),
                randint(ENEMY_Spawn_Y_MIN, ENEMY_Spawn_Y_MAX)
            )
            enemy.speed = speed
            self.enemies_group.add(enemy)
            self.all_sprites.add(enemy)

        # Enemigos Shooter (Cantidad proporcional)
        shooter_count = count // SHOOTER_ENEMY_COUNT_DIVISOR
        for _ in range(shooter_count):
            enemy = ShooterEnemy(
                randint(0, WINDOW_WIDTH - 64),
                randint(ENEMY_Spawn_Y_MIN, 250),
                bullets_group=self.enemy_bullets_group,
                all_sprites=self.all_sprites
            )
            enemy.speed = speed
            self.enemies_group.add(enemy)
            self.all_sprites.add(enemy)
            
            
            
    
    def reset_game(self):
        """ Reinicia el juego para una nueva partida"""
        self.all_sprites.empty()
        self.bullets_group.empty()
        self.enemy_bullets_group.empty()
        self.enemies_group.empty()
        self.explosions_group.empty()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.level_manager = LevelManager()
        self._spawn_enemies_for_level()

    def show_menu(self):
        """ Muestra el menú principal"""
        pygame.mouse.set_visible(True)
        menu = MenuWithButtons(self.screen)
        result = menu.run()
        pygame.mouse.set_visible(False)
        return result

    def show_game_over(self):
        """ Muestra pantalla de Game Over"""
        font_large = pygame.font.Font(None, 74)
        font_medium = pygame.font.Font(None, 36)
        
        running = True
        clock = pygame.time.Clock()
        
        while running:
            clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return "menu"
            
            self.screen.fill((0, 0, 0))
            
            # Texto Game Over
            game_over_text = font_large.render("GAME OVER", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, 250))
            self.screen.blit(game_over_text, game_over_rect)
            
            # Instrucción
            restart_text = font_medium.render("Presiona ENTER para volver al menú", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, 350))
            self.screen.blit(restart_text, restart_rect)
            
            pygame.display.flip()
        
        return "menu"
    
    
    
    

    def _handle_events(self) -> None:
        """Procesa los eventos de entrada (teclado, mouse, ventana)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # cancela todo evento si el jugador ha muerto
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.player.alive():
                    return
                
                if event.button == 1:  # Click izquierdo
                    self._shoot_bullet()

            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key)

            if event.type == pygame.KEYUP:
                self._handle_key_up(event.key)

    def _handle_key_down(self, key: int) -> None:
        """Cambia la dirección del disparo según la tecla presionada."""
        if key == pygame.K_a:
            self.shoot_direction = "left"
        elif key == pygame.K_d:
            self.shoot_direction = "right"
        elif key == pygame.K_s:
            self.shoot_direction = "down"

    def _handle_key_up(self, key: int) -> None:
        """Restaura la dirección por defecto al soltar teclas de dirección."""
        if key in (pygame.K_a, pygame.K_d, pygame.K_s):
            self.shoot_direction = DEFAULT_SHOOT_DIRECTION

    def _shoot_bullet(self) -> None:
        """Crea y dispara una bala desde la posición del jugador."""
        bullet = BasicBullet(
            self.player.rect.centerx,
            self.player.rect.top,
            direction=self.shoot_direction
        )
        self.bullets_group.add(bullet)
        self.all_sprites.add(bullet)
        bullet.play_shooting_sound()

    def _check_collisions(self) -> None:
        """Detecta y resuelve colisiones entre entidades."""
        if not self.player.alive():
            return

        # 1. Balas Jugador vs Enemigos
        impacts = pygame.sprite.groupcollide(
            self.bullets_group,
            self.enemies_group,
            True,   # Elimina bala
            False   # No elimina enemigo inmediatamente (verifica vida)
        )

        for bullet, enemies in impacts.items():
            for enemy in enemies:
                if enemy.receive_damage(bullet.damage):
                    self._create_explosion(enemy)
                    enemy.kill()
            # bullet.stop_shooting_sound() # Opcional: dependiendo de la implementación de BasicBullet

        # 2. Balas Enemigas vs Jugador
        if pygame.sprite.spritecollide(
            self.player, 
            self.enemy_bullets_group, 
            True, 
            pygame.sprite.collide_mask
        ):
            self._handle_player_death()

        # 3. Jugador vs Enemigos (Colisión directa)
        player_hits = pygame.sprite.spritecollide(
            self.player,
            self.enemies_group,
            True,
            pygame.sprite.collide_mask
        )

        if player_hits:
            self._handle_player_death()
            for enemy in player_hits:
                self._create_explosion(enemy)
                enemy.kill()

    def _handle_player_death(self) -> None:
        """Gestiona la lógica cuando el jugador muere."""
        self._create_explosion(self.player)
        self.player.player_destroyed(self.all_sprites)
        
    def verified_game_over(self):
        """Verifica si el jugador no tiene mas vidas"""
        
        if self.player.is_there_lifes():
            self.player.relive_player(self.all_sprites)
        else:
            self.game_state = "game_over"


    def _create_explosion(self, character: pygame.sprite.Sprite) -> None:
        """Crea un efecto de explosión en la posición del personaje."""
        explosion = Explosion(character.rect.centerx, character.rect.centery)
        explosion.play_explosion_sound()
        self.explosions_group.add(explosion)
        self.all_sprites.add(explosion)

    def _update(self) -> None:
        """Actualiza el estado lógico del juego."""
        # Verificar progresión de nivel
        if len(self.enemies_group) == 0:
            self.level_manager.next_level()
            self._spawn_enemies_for_level()

        # Actualizar todos los sprites
        self.all_sprites.update()

        # Verificar colisiones
        self._check_collisions()
        
        # Verifica si el jugador no tiene mas vidas
        self.verified_game_over()

    def _draw_ui(self) -> None:
        """Dibuja la interfaz de usuario (textos)."""
        # Nivel
        text_level = self.font_ui.render(
            f"Nivel: {self.level_manager.current_level}", 
            True, 
            (255, 255, 255)
        )
        self.screen.blit(text_level, (10, 10))

        # Enemigos restantes
        text_enemies = self.font_ui.render(
            f"Enemigos: {len(self.enemies_group)}", 
            True, 
            (255, 255, 255)
        )
        self.screen.blit(text_enemies, (10, 50))

    def _draw(self) -> None:
        """Renderiza todos los elementos en la pantalla."""
        self.screen.blit(self.background, (0, 0))
        
        self._draw_ui()
        
        if self.player.lifes != 0:
            self.all_sprites.draw(self.screen)
        
        pygame.display.flip()

    def run(self) -> None:
        """Bucle principal del juego."""
        while self.running:
            self.clock.tick(FPS)
            
            if self.game_state == "menu":
                result = self.show_menu()
                if result == "start_game":
                    self.reset_game()
                    self.game_state = "playing"
                elif result == "quit":
                    self.running = False
                    
            elif self.game_state == "playing":
                self._handle_events()
                self._update()
                self._draw()
                
                # Verificar si pasó a game_over
                if self.game_state == "game_over":
                    result = self.show_game_over()
                    if result == "menu":
                        self.game_state = "menu"
                    elif result == "quit":
                        self.running = False
            
            elif self.game_state == "game_over":
                result = self.show_game_over()
                if result == "menu":
                    self.game_state = "menu"
                elif result == "quit":
                    self.running = False

        pygame.quit()
