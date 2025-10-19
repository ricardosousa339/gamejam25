"""
Pegador (Pool Net) entity that collects trash from the river
"""
import pygame
from enum import Enum
from config import *
from utils import resource_path


class PegadorState(Enum):
    """States for the pegador"""
    IDLE = "idle"  # At margin (bottom), can move horizontally
    CHARGING = "charging"  # Holding space, charging force bar
    DESCENDING = "descending"  # Released space, moving up into river
    ASCENDING = "ascending"  # Returning to margin (bottom)
    SHOWING_CATCH = "showing_catch"  # Showing caught trash at margin (1 second delay)
    STUNNED = "stunned"  # Hit by crocodile, cannot move
    CAUGHT_BY_CROCODILE = "caught_by_crocodile"  # Caught by crocodile, following it


class Pegador(pygame.sprite.Sprite):
    def __init__(self, x, y, river_band_top, river_band_bottom):
        """
        Initialize the pegador
        
        Args:
            x (int): Initial x position
            y (int): Initial y position (at margin)
            river_band_top (int): Top boundary of the river where objects spawn
            river_band_bottom (int): Bottom boundary of the river where objects spawn
        """
        super().__init__()
        
        # Load sprites - both are long versions (300px height)
        pegador_front = pygame.image.load(resource_path('assets/pegador_frente_comprido.png')).convert_alpha()
        pegador_side = pygame.image.load(resource_path('assets/pegador_lado.png')).convert_alpha()
        
        # Scale sprites
        front_width = int(pegador_front.get_width() * PEGADOR_SCALE)
        front_height = int(pegador_front.get_height() * PEGADOR_SCALE)
        side_width = int(pegador_side.get_width() * PEGADOR_SCALE)
        side_height = int(pegador_side.get_height() * PEGADOR_SCALE)
        
        self.image_front = pygame.transform.smoothscale(pegador_front, (front_width, front_height))
        self.image_side = pygame.transform.smoothscale(pegador_side, (side_width, side_height))
        
        # Start with front view (when at margin)
        self.image = self.image_front
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y  # Position from top (half will be below screen)

        # Collision rect - smaller area at the net part (top portion of the pegador)
        self.collision_rect = pygame.Rect(0, 0, front_width - 10, 60)
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top

        # Collision mask for pixel-perfect collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # State management
        self.state = PegadorState.IDLE
        self.margin_y = y
        
        # River boundaries - limit dive depth to where trash floats
        self.river_band_top = river_band_top
        self.river_band_bottom = river_band_bottom
        
        # Force system
        self.force = 0
        self.max_depth = 0  # Calculated when space is released
        
        # Captured trash
        self.captured_trash = None
        
        # Show catch delay timer
        self.show_catch_timer = 0
        self.show_catch_duration = 500  # 1 second to show the catch

        # Crocodile reference when caught
        self.catching_crocodile = None
        self.catch_offset_y = 0  # Vertical offset from mouth position where pegador was caught
        
    def update(self):
        """Update pegador state and position"""
        keys = pygame.key.get_pressed()

        if self.state == PegadorState.IDLE:
            self._update_idle(keys)
        elif self.state == PegadorState.CHARGING:
            self._update_charging(keys)
        elif self.state == PegadorState.DESCENDING:
            self._update_descending()
        elif self.state == PegadorState.ASCENDING:
            self._update_ascending()
        elif self.state == PegadorState.SHOWING_CATCH:
            self._update_showing_catch()
        elif self.state == PegadorState.CAUGHT_BY_CROCODILE:
            self._update_caught_by_crocodile()
    
    def _update_idle(self, keys):
        """Handle idle state - horizontal movement at margin"""
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PEGADOR_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PEGADOR_SPEED
        
        # Keep within screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        
        # Update collision rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top
        
        # Start charging when space is pressed
        if keys[pygame.K_SPACE]:
            self.state = PegadorState.CHARGING
            self.force = 0
            self.image = self.image_side  # Switch to side view when diving
            self.mask = pygame.mask.from_surface(self.image)  # Update mask
    
    def _update_charging(self, keys):
        """Handle charging state - building up force"""
        # Continue horizontal movement while charging
        if keys[pygame.K_LEFT]:
            self.rect.x -= PEGADOR_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PEGADOR_SPEED
        
        # Keep within screen bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        
        # Update collision rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top
        
        # Charge force
        if keys[pygame.K_SPACE]:
            self.force = min(self.force + PEGADOR_FORCE_CHARGE_RATE, PEGADOR_MAX_FORCE)
        else:
            # Space released, start descending (going UP into the river)
            # Calculate how far UP the pegador will go based on force
            # Limit dive to the river band where trash floats
            linear_ratio = self.force / PEGADOR_MAX_FORCE
            
            # Apply aggressive ease-in curve:
            # - VERY slow start (need to hold much longer to dive deep)
            # - Only after 50% force it starts going far
            # - Using cubic curve: x³ for aggressive start
            force_ratio = linear_ratio * linear_ratio * linear_ratio
            
            # Minimum depth: just inside the bottom of the river band
            min_dive_y = self.river_band_bottom
            # Maximum depth: top of the river band
            max_dive_y = self.river_band_top
            
            # Calculate target depth based on force (interpolate between min and max)
            self.max_depth = min_dive_y - (force_ratio * (min_dive_y - max_dive_y))
            
            self.state = PegadorState.DESCENDING
    
    def _update_descending(self):
        """Handle descending state - moving UP into river"""
        self.rect.y -= PEGADOR_VERTICAL_SPEED  # Moving UP (y decreases)
        
        # Update collision rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top
        
        # Check if reached target depth
        if self.rect.centery <= self.max_depth:
            self.state = PegadorState.ASCENDING
            self.image = self.image_front  # Switch back to front view when ascending
            self.mask = pygame.mask.from_surface(self.image)  # Update mask
    
    def _update_ascending(self):
        """Handle ascending state - returning to margin (bottom)"""
        self.rect.y += PEGADOR_VERTICAL_SPEED  # Moving DOWN (y increases)
        
        # Update collision rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top
        
        # Update captured trash position if any
        if self.captured_trash:
            self.captured_trash.rect.centerx = self.rect.centerx
            self.captured_trash.rect.centery = self.rect.top + 20  # Trash in the net area
        
        # Check if reached margin (using top position since pegador extends below screen)
        if self.rect.top >= self.margin_y:
            self.rect.top = self.margin_y
            self.collision_rect.top = self.rect.top
            
            # If carrying trash, go to SHOWING_CATCH state for 1 second
            if self.captured_trash:
                self.state = PegadorState.SHOWING_CATCH
                self.show_catch_timer = 0
                self.force = 0
                self.image = self.image_front
                self.mask = pygame.mask.from_surface(self.image)  # Update mask
            else:
                # No trash, go directly to IDLE
                self.state = PegadorState.IDLE
                self.force = 0
                self.image = self.image_front
                self.mask = pygame.mask.from_surface(self.image)  # Update mask
    
    def _update_showing_catch(self):
        """Handle showing catch state - display caught trash for 1 second"""
        # Keep trash at margin position
        if self.captured_trash:
            self.captured_trash.rect.centerx = self.rect.centerx
            self.captured_trash.rect.centery = self.rect.top + 20
        
        # Update timer
        self.show_catch_timer += 16  # Approximate ms per frame (60 FPS)
        
        # After 1 second, release trash and go to IDLE
        if self.show_catch_timer >= self.show_catch_duration:
            if self.captured_trash:
                self.captured_trash.kill()
                self.captured_trash = None
            self.state = PegadorState.IDLE
            self.show_catch_timer = 0
    
    def capture_trash(self, trash):
        """
        Capture a trash object
        
        Args:
            trash (FloatingObject): The trash object to capture
            
        Returns:
            bool: True if trash was captured (triggers splash animation)
        """
        if self.captured_trash is None and self.state == PegadorState.DESCENDING:
            self.captured_trash = trash
            trash.is_captured = True
            # Stop descending, start ascending
            self.state = PegadorState.ASCENDING
            self.image = self.image_front  # Switch back to front view when ascending
            return True  # Indicate that trash was captured
        return False
    
    def get_force_percentage(self):
        """Get current force as percentage (0-100)"""
        return (self.force / PEGADOR_MAX_FORCE) * 100
    
    def is_charging(self):
        """Check if currently charging"""
        return self.state == PegadorState.CHARGING

    def get_caught_by_crocodile(self, crocodile):
        """
        Pegador gets caught by a crocodile and starts following it

        Args:
            crocodile (Crocodile): The crocodile that caught the pegador
        """
        print(f"[PEGADOR] Caught by crocodile at ({crocodile.rect.x}, {crocodile.rect.y})")

        # Change state to caught
        self.state = PegadorState.CAUGHT_BY_CROCODILE
        self.catching_crocodile = crocodile

        # Calculate and store the vertical offset from the mouth where pegador was caught
        _, mouth_y = crocodile.get_mouth_position()
        self.catch_offset_y = self.rect.centery - mouth_y

        print(f"[PEGADOR] Catch vertical offset from mouth: {self.catch_offset_y}")

        # Drop any captured trash
        if self.captured_trash:
            self.captured_trash.kill()
            self.captured_trash = None

        # Switch to side view
        self.image = self.image_side
        self.mask = pygame.mask.from_surface(self.image)

    def _update_caught_by_crocodile(self):
        """Handle caught by crocodile state - follow the crocodile's mouth with stored offset"""
        if self.catching_crocodile is None:
            # Safety check: if crocodile reference is lost, return to idle
            print("[PEGADOR] Lost crocodile reference, returning to idle")
            self.state = PegadorState.IDLE
            self.image = self.image_front
            self.mask = pygame.mask.from_surface(self.image)
            return

        # Get the mouth position from the crocodile
        mouth_x, mouth_y = self.catching_crocodile.get_mouth_position()

        # Position pegador horizontally at mouth, vertically with the original offset
        # This makes it look like the crocodile is holding the pegador at the height it was caught
        self.rect.centerx = mouth_x
        self.rect.centery = mouth_y + self.catch_offset_y

        # Update collision rect
        self.collision_rect.centerx = self.rect.centerx
        self.collision_rect.top = self.rect.top
