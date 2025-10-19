"""
Crocodile entity that swims in the river with animated sprites
"""
import pygame
import random
import config
from utils import resource_path
from spritesheet import spritesheet
from entities.crocodile_control import CrocodileControl


class Crocodile(pygame.sprite.Sprite):
    """
    Crocodile that swims in the river with smooth transitions between
    different submersion states (fully surfaced to head-only visible)
    """

    # Sprite dimensions
    BODY_SPRITE_WIDTH = 61
    BODY_SPRITE_HEIGHT = 26
    HEAD_SPRITE_WIDTH = 19
    HEAD_SPRITE_HEIGHT = 11

    # Animation configuration
    ANIMATION_SPEED = 15  # frames to hold each sprite before advancing
    SCALE = 2.0  # scaling factor for sprites

    def __init__(self, x, y, min_y, max_y, control=None):
        """
        Initialize a crocodile

        Args:
            x (int): Initial x position
            y (int): Initial y position
            min_y (int): Minimum y boundary (top of river)
            max_y (int): Maximum y boundary (bottom of river)
            control (CrocodileControl): Control object for behavior (uses default if None)
        """
        super().__init__()

        # Position and movement
        self.min_y = min_y
        self.max_y = max_y
        self.vel_y = random.uniform(-0.3, 0.3)  # Slight vertical wobble

        # Swim direction (0 = left, 1 = right)
        self.swim_direction = random.randint(0, 1)

        # Load all animations
        self._load_animations()

        # State management (delegated to control)
        self.animation_frame = 0  # Current frame counter for animation speed
        self.current_anim_index = 0  # Current index in the active animation

        # Set initial image and rect
        current_animation = self.animations[4]
        self.image = current_animation[0]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Collision mask for pixel-perfect collision detection
        self.mask = None
        self._update_mask()

        # Carrying state
        self.is_carrying_pegador = False
        self.carried_pegador = None

        # Splash events queue - list of (event_type, x, y) tuples
        self.pending_splashes = []

        # Sound reference for crocodile attack sound
        self.attack_sound = None

        # Control system ==> alway last init action (control needs crocodile fully started)
        self.control = control(self) if control is not None else CrocodileControl(self)

        print(f"[CROC] Initialized at ({x}, {y}), state: {self.control.current_state}, image size: {self.image.get_size()}")

    def _load_animations(self):
        """Load all sprite animations from spritesheet"""
        # Load crocodile spritesheet (2 cols x 4 rows)
        # All states are now in the same file with head already positioned
        croc_sheet = spritesheet(resource_path("assets/crocodilo.png"))

        # Extract animations for each row (each row is one animation with 2 frames)
        # Note: pygame.Rect interprets as (x, y, width, height)
        # Row 0: Fully surfaced (frames at y=0)
        self.anim_fully_surfaced = [
            croc_sheet.image_at((0, 0, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1),
            croc_sheet.image_at((self.BODY_SPRITE_WIDTH, 0, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1)
        ]

        # Row 1: Mostly surfaced (frames at y=26)
        self.anim_mostly_surfaced = [
            croc_sheet.image_at((0, self.BODY_SPRITE_HEIGHT, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1),
            croc_sheet.image_at((self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1)
        ]

        # Row 2: Mostly submerged (frames at y=52)
        self.anim_mostly_submerged = [
            croc_sheet.image_at((0, self.BODY_SPRITE_HEIGHT * 2, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1),
            croc_sheet.image_at((self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT * 2, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1)
        ]

        # Row 3: Head only (frames at y=78)
        self.anim_head_only = [
            croc_sheet.image_at((0, self.BODY_SPRITE_HEIGHT * 3, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1),
            croc_sheet.image_at((self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT * 3, self.BODY_SPRITE_WIDTH, self.BODY_SPRITE_HEIGHT), colorkey=-1)
        ]

        # Scale all sprites
        self.anim_fully_surfaced = self._scale_sprites(self.anim_fully_surfaced)
        self.anim_mostly_surfaced = self._scale_sprites(self.anim_mostly_surfaced)
        self.anim_mostly_submerged = self._scale_sprites(self.anim_mostly_submerged)
        self.anim_head_only = self._scale_sprites(self.anim_head_only)

        # Store animations in a list for easy access by state
        self.animations = [
            self.anim_fully_surfaced,
            self.anim_mostly_surfaced,
            self.anim_mostly_submerged,
            self.anim_head_only,
            self.anim_head_only
        ]

    def _scale_sprites(self, sprite_list):
        """
        Scale a list of sprites using nearest-neighbor (no blur, good for pixel art)

        Args:
            sprite_list (list): List of pygame surfaces

        Returns:
            list: List of scaled pygame surfaces
        """
        scaled = []
        for sprite in sprite_list:
            width = int(sprite.get_width() * self.SCALE)
            height = int(sprite.get_height() * self.SCALE)
            # Use scale() instead of smoothscale() to keep pixel art crisp
            scaled.append(pygame.transform.scale(sprite, (width, height)))
        return scaled


    def _update_mask(self):
        """Update the collision mask based on current image"""
        if self.image is not None:
            self.mask = pygame.mask.from_surface(self.image)

    def _update_image(self):
        """Update the current image based on state and animation frame"""
        current_animation = self.animations[self.control.current_state]
        self.image = current_animation[self.current_anim_index]

        # Flip image horizontally if swimming left (swim_direction = 0)
        if self.swim_direction == 0:
            self.image = pygame.transform.flip(self.image, True, False)

        # Update mask whenever image changes
        self._update_mask()

    def update(self):
        """Update crocodile position and animation"""
        # Delegate state transitions to control (always update state)
        self.control.update_state()

        # Skip movement and animation updates when fully submerged
        if self.control.current_state == 4:  # FULLY_SUBMERGED
            return

        # Delegate movement to control (moves the rect)
        self.control.update_movement(self, self.min_y, self.max_y)

        # Update animation frame
        self.animation_frame += 1
        if self.animation_frame >= self.ANIMATION_SPEED:
            self.animation_frame = 0
            # Advance to next frame in animation (loop between 0 and 1)
            self.current_anim_index = (self.current_anim_index + 1) % 2

        # Update the sprite image
        self._update_image()

    def start_carrying_pegador(self, pegador):
        """
        Start carrying the pegador

        Args:
            pegador (Pegador): The pegador to carry
        """
        self.is_carrying_pegador = True
        self.carried_pegador = pegador
        self.control.start_carrying(self)
        print(f"[CROC] Started carrying pegador at ({self.rect.x}, {self.rect.y})")

        # Play crocodile attack sound
        self.play_attack_sound()

    def release_pegador(self):
        """Release the carried pegador and return to normal behavior"""
        if self.carried_pegador:
            print(f"[CROC] Releasing pegador at ({self.rect.x}, {self.rect.y})")
            released_pegador = self.carried_pegador
            self.carried_pegador = None
            self.is_carrying_pegador = False
            self.control.stop_carrying()

            # Stop crocodile attack sound
            self.stop_attack_sound()

            return released_pegador
        return None

    def get_mouth_position(self):
        """
        Get the position of the crocodile's mouth based on swim direction

        Returns:
            tuple: (x, y) coordinates of the mouth center position
        """
        # Mouth offset from the edge of the sprite
        # The mouth is near the edge horizontally and centered vertically
        mouth_offset_from_edge = 10  # pixels from edge

        if self.swim_direction == 1:  # Swimming right (mouth at right end)
            mouth_x = self.rect.right - mouth_offset_from_edge
        else:  # Swimming left (mouth at left end)
            mouth_x = self.rect.left + mouth_offset_from_edge

        # Mouth is at the vertical center of the sprite
        mouth_y = self.rect.centery

        return (mouth_x, mouth_y)

    def check_collision(self, other_sprite):
        """
        Check pixel-perfect collision with another sprite using non-transparent pixels

        Args:
            other_sprite (pygame.sprite.Sprite): The sprite to check collision with.
                                                  Must have a 'mask' attribute.

        Returns:
            bool: True if there is a pixel-perfect collision, False otherwise
        """
        # Skip collision check if crocodile is fully submerged
        if self.control.current_state == 4:  # FULLY_SUBMERGED
            return False

        # Ensure both sprites have masks
        if not hasattr(other_sprite, 'mask') or other_sprite.mask is None:
            return False

        if self.mask is None:
            return False

        # Calculate offset between the two sprites
        offset_x = other_sprite.rect.x - self.rect.x
        offset_y = other_sprite.rect.y - self.rect.y

        # Check if masks overlap (returns None if no collision, otherwise returns contact point)
        overlap = self.mask.overlap(other_sprite.mask, (offset_x, offset_y))

        return overlap is not None

    def play_attack_sound(self):
        """Play crocodile attack sound"""
        if config.SOUND_ENABLED and pygame.mixer.get_init():
            try:
                # Stop previous sound if playing
                self.stop_attack_sound()

                # Load and play new sound
                self.attack_sound = pygame.mixer.Sound(resource_path('assets/sons/crocodilo_agua.ogg'))
                self.attack_sound.set_volume(config.CROCODILE_SOUND_VOLUME)
                self.attack_sound.play()
                print("[CROC] Playing attack sound")
            except (pygame.error, FileNotFoundError) as e:
                print(f"[CROC] Warning: Could not play crocodile sound: {e}")

    def stop_attack_sound(self):
        """Stop crocodile attack sound"""
        if self.attack_sound:
            self.attack_sound.stop()
            self.attack_sound = None
            print("[CROC] Stopped attack sound")
