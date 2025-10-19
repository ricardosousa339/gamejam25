"""
Main game class that handles the game loop and state management
"""
import pygame
import random
from config import *
from entities.floating_object import FloatingObject
from entities.crocodile import Crocodile
from entities.crocodile_control import DebugControl
from entities.pegador import Pegador
from utils import resource_path


class Game:
    def __init__(self, debug=False):
        """
        Initialize the game

        Args:
            debug (bool): Enable debug mode with fixed test crocodile
        """
        self.debug = debug
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.score = 0
        
        # Load and scale background images to fill the screen
        rio_original = pygame.image.load(resource_path('assets/rio.png')).convert_alpha()
        margens_original = pygame.image.load(resource_path('assets/margens.png')).convert_alpha()
        
        # Scale images to screen height while maintaining aspect ratio for tiling
        self.scale_factor = SCREEN_HEIGHT / rio_original.get_height()
        new_width = int(rio_original.get_width() * self.scale_factor)
        
        self.rio_img = pygame.transform.scale(rio_original, (new_width, SCREEN_HEIGHT))
        self.margens_img = pygame.transform.scale(margens_original, (new_width, SCREEN_HEIGHT))
        
        # Vertical band where objects should spawn (converted from image space)
        self.river_band_top = int(RIVER_IMAGE_BAND_TOP * self.scale_factor)
        self.river_band_bottom = int(RIVER_IMAGE_BAND_BOTTOM * self.scale_factor)
        self.river_band_top = max(0, min(self.river_band_top, SCREEN_HEIGHT))
        self.river_band_bottom = max(
            self.river_band_top + FloatingObject.HEIGHT,
            min(self.river_band_bottom, SCREEN_HEIGHT)
        )
        
        # River animation
        self.rio_x_offset = 0
        self.rio_width = self.rio_img.get_width()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.floating_objects = pygame.sprite.Group()
        self.crocodiles = pygame.sprite.Group()

        
        # Create pegador
        pegador_x = SCREEN_WIDTH // 2
        pegador_y = PEGADOR_MARGIN_Y
        self.pegador = Pegador(pegador_x, pegador_y, self.river_band_top, self.river_band_bottom)
        self.all_sprites.add(self.pegador)
        
        # Spawn timer
        self.last_spawn = pygame.time.get_ticks()
        
        # Initialize game objects
        self._setup_game()
    
    def _setup_game(self):
        """Set up initial game objects"""
        for _ in range(3):
            y = self._random_river_y()
            x = random.randint(0, SCREEN_WIDTH)
            obj_type = random.choice(list(OBJECT_TYPES.keys()))
            floating_obj = FloatingObject(x, y, self.river_band_top, self.river_band_bottom, obj_type)
            self.floating_objects.add(floating_obj)
            self.all_sprites.add(floating_obj)

        # Spawn initial crocodile
        self.spawn_crocodile()

        # Setup debug mode if enabled
        if self.debug:
            self._setup_debug()
    
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
        
        # Check for pegador collision with crocodiles using pixel-perfect detection
        if self.pegador.state.value in ["descending", "ascending"]:
            for crocodile in self.crocodiles:
                if crocodile.check_collision(self.pegador):
                    # Pegador gets caught by the crocodile
                    self.pegador.get_caught_by_crocodile(crocodile)
                    crocodile.start_carrying_pegador(self.pegador)
                    break  # Only one crocodile can catch at a time

        # Check for pegador collision with trash using the collision_rect
        if self.pegador.captured_trash is None and self.pegador.state.value == "descending":
            for trash in self.floating_objects:
                if self.pegador.collision_rect.colliderect(trash.rect):
                    # Capture the trash
                    self.pegador.capture_trash(trash)
                    self.floating_objects.remove(trash)
                    self.score += 10  # Add points for collecting trash
                    break  # Only capture one at a time
        
        # Remove objects that went off screen (handle both directions)
        for obj in list(self.floating_objects):
            if RIVER_FLOW_SPEED > 0 and obj.rect.right < 0:
                obj.kill()
            elif RIVER_FLOW_SPEED < 0 and obj.rect.left > SCREEN_WIDTH:
                obj.kill()
        
        # Spawn new objects periodically
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn > OBJECT_SPAWN_RATE:
            self.last_spawn = current_time
            y = self._random_river_y()
            obj_type = random.choice(list(OBJECT_TYPES.keys()))
            
            # Spawn on the side opposite to the flow so objects enter the screen
            if RIVER_FLOW_SPEED > 0:
                spawn_x = SCREEN_WIDTH + FloatingObject.WIDTH
                floating_obj = FloatingObject(spawn_x, y, self.river_band_top, self.river_band_bottom, obj_type)
            else:
                spawn_x = -FloatingObject.WIDTH
                floating_obj = FloatingObject(spawn_x, y, self.river_band_top, self.river_band_bottom, obj_type)
            
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
        
        # Draw all sprites (except fully submerged crocodiles)
        for sprite in self.all_sprites:
            # Skip drawing crocodiles that are fully submerged
            if hasattr(sprite, 'control') and sprite.control.current_state == 4:
                continue
            self.screen.blit(sprite.image, sprite.rect)
        
        # Debug: Draw collision rect (uncomment to visualize)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.pegador.collision_rect, 2)
        
        # Draw UI
        self._draw_ui()
        
        pygame.display.flip()
    
    def _draw_ui(self):
        """Draw UI elements like score"""
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw force bar when charging
        if self.pegador.is_charging():
            bar_width = 200
            bar_height = 20
            bar_x = (SCREEN_WIDTH - bar_width) // 2
            bar_y = SCREEN_HEIGHT - 40
            
            # Background bar
            pygame.draw.rect(self.screen, BLACK, (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height))
            
            # Force bar (filled portion)
            force_percentage = self.pegador.get_force_percentage()
            fill_width = int((force_percentage / 100) * bar_width)
            
            # Color gradient based on force
            if force_percentage < 33:
                bar_color = GREEN
            elif force_percentage < 66:
                bar_color = YELLOW
            else:
                bar_color = RED
            
            pygame.draw.rect(self.screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
            
            # Force text
            force_font = pygame.font.Font(None, 24)
            force_text = force_font.render("FORÇA", True, WHITE)
            text_rect = force_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y - 15))
            self.screen.blit(force_text, text_rect)

    def _random_river_y(self):
        """Return a random y within the scaled river band"""
        spawn_min_y = self.river_band_top
        spawn_max_y = max(spawn_min_y, self.river_band_bottom - FloatingObject.HEIGHT)
        return random.randint(spawn_min_y, spawn_max_y)

    def spawn_crocodile(self):
        """Spawn a crocodile in the river"""
        y = self._random_river_y()

        # Spawn on the right side of the screen (will move left with river flow)
        # RIVER_FLOW_SPEED is negative, so crocodile enters from right
        spawn_x = 20

        crocodile = Crocodile(spawn_x, y, self.river_band_top, self.river_band_bottom)
        self.crocodiles.add(crocodile)
        self.all_sprites.add(crocodile)

    def _setup_debug(self):
        """Setup debug mode with fixed test crocodile"""
        # Add a fixed crocodile for testing with DebugControl
        # Position: left side (x=150), middle of river (y = center of river band)
        debug_x = 150
        debug_y = (self.river_band_top + self.river_band_bottom) // 2
        debug_croc = Crocodile(debug_x, debug_y, self.river_band_top, self.river_band_bottom, control=DebugControl)
        self.crocodiles.add(debug_croc)
        self.all_sprites.add(debug_croc)
        self.debug_crocodile = debug_croc

        print("=" * 50)
        print("[DEBUG MODE ENABLED]")
        print(f"Debug crocodile at ({debug_x}, {debug_y}) with DebugControl")
        print(f"River band: {self.river_band_top} to {self.river_band_bottom}")
        print(f"Initial state: {debug_croc.control.current_state}")
        print("States cycle: 0->1->2->3->4->0 (4=invisible)")
        print("=" * 50)
