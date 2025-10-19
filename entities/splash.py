"""
Splash animation entity - plays when pegador catches trash
"""
import pygame
from utils import resource_path


class Splash(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the splash animation
        
        Args:
            x (int): Center x position
            y (int): Center y position
        """
        super().__init__()
        
        # Load spritesheet (1x4 vertical)
        spritesheet = pygame.image.load(resource_path('assets/splash.png')).convert_alpha()
        
        # Extract 4 frames (64x64 each from 64x256 sheet)
        frame_width = 64
        frame_height = 64
        self.frames = []
        
        for i in range(4):
            frame = spritesheet.subsurface(pygame.Rect(0, i * frame_height, frame_width, frame_height))
            self.frames.append(frame)
        
        # Animation state
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_duration = 100  # 100ms per frame = 400ms total animation
        
        # Set initial image and position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Flag to track if animation is complete
        self.animation_complete = False
    
    def update(self):
        """Update animation frame"""
        if self.animation_complete:
            return
        
        # Update timer
        self.frame_timer += 16  # ~60 FPS
        
        # Check if it's time to advance frame
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1
            
            # Check if animation is complete
            if self.current_frame >= len(self.frames):
                self.animation_complete = True
                self.kill()  # Remove from sprite groups
            else:
                # Update to next frame
                self.image = self.frames[self.current_frame]
