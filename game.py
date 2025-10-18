"""
Main game class that handles the game loop and state management
"""
import pygame
import random
from config import *
from entities.floating_object import FloatingObject


class Game:
    def __init__(self):
        """Initialize the game"""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.score = 0
        
        # Load and scale background images to fill the screen
        rio_original = pygame.image.load('assets/rio.png').convert_alpha()
        margens_original = pygame.image.load('assets/margens.png').convert_alpha()
        
        # Scale images to screen height while maintaining aspect ratio for tiling
        scale_factor = SCREEN_HEIGHT / rio_original.get_height()
        new_width = int(rio_original.get_width() * scale_factor)
        
        self.rio_img = pygame.transform.scale(rio_original, (new_width, SCREEN_HEIGHT))
        self.margens_img = pygame.transform.scale(margens_original, (new_width, SCREEN_HEIGHT))
        
        # River animation
        self.rio_x_offset = 0
        self.rio_width = self.rio_img.get_width()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.floating_objects = pygame.sprite.Group()
        
        # Spawn timer
        self.last_spawn = pygame.time.get_ticks()
        
        # Initialize game objects
        self._setup_game()
    
    def _setup_game(self):
        """Set up initial game objects"""
        # Create some initial floating objects
        for i in range(3):
            y = random.randint(100, SCREEN_HEIGHT - 100)
            x = random.randint(0, SCREEN_WIDTH)
            obj_type = random.choice(list(OBJECT_TYPES.keys()))
            floating_obj = FloatingObject(x, y, obj_type)
            self.floating_objects.add(floating_obj)
            self.all_sprites.add(floating_obj)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
    
    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        """Update game state"""
        # Update river animation
        self.rio_x_offset += RIVER_FLOW_SPEED
        
        # Handle wrapping for both positive and negative speeds
        if RIVER_FLOW_SPEED > 0:
            # Moving right: reset when offset reaches width
            if self.rio_x_offset >= self.rio_width:
                self.rio_x_offset = 0
        else:
            # Moving left: reset when offset goes negative
            if self.rio_x_offset <= -self.rio_width:
                self.rio_x_offset = 0
        
        # Update all sprites
        self.all_sprites.update()
        
        # Remove objects that went off screen (handle both directions)
        for obj in self.floating_objects:
            if RIVER_FLOW_SPEED > 0 and obj.rect.left > SCREEN_WIDTH:
                obj.kill()
            elif RIVER_FLOW_SPEED < 0 and obj.rect.right < 0:
                obj.kill()
        
        # Spawn new objects periodically
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > OBJECT_SPAWN_RATE:
            self.last_spawn = current_time
            y = random.randint(100, SCREEN_HEIGHT - 100)
            obj_type = random.choice(list(OBJECT_TYPES.keys()))
            
            # Spawn from left if moving right, from right if moving left
            if RIVER_FLOW_SPEED > 0:
                floating_obj = FloatingObject(-50, y, obj_type)
            else:
                floating_obj = FloatingObject(SCREEN_WIDTH + 50, y, obj_type)
            
            self.floating_objects.add(floating_obj)
            self.all_sprites.add(floating_obj)
    
    def draw(self):
        """Draw everything to the screen"""
        # Draw rio.png as repeating pattern
        # Add extra tiles to ensure full coverage during animation in both directions
        num_tiles = (SCREEN_WIDTH // self.rio_width) + 3  # +3 to ensure coverage in both directions
        
        # Calculate starting position to ensure we always cover the screen
        start_tile = -1 if RIVER_FLOW_SPEED >= 0 else -2
        
        for i in range(start_tile, start_tile + num_tiles):
            x_pos = (i * self.rio_width) - self.rio_x_offset
            self.screen.blit(self.rio_img, (x_pos, 0))
        
        # Draw margens.png on top (STATIC - no offset)
        num_tiles_static = (SCREEN_WIDTH // self.rio_width) + 2
        for i in range(-1, num_tiles_static):
            x_pos = i * self.rio_width
            self.screen.blit(self.margens_img, (x_pos, 0))
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw UI elements like score"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
