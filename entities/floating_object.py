"""
Floating objects that move down the river
"""
import pygame
import random
from config import *


class FloatingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, object_type="plastic"):
        """
        Initialize a floating object
        
        Args:
            x (int): Initial x position
            y (int): Initial y position
            object_type (str): Type of object (plastic, metal, organic, paper)
        """
        super().__init__()
        
        self.object_type = object_type
        
        # Create a simple rectangle sprite (replace with images later)
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.color = OBJECT_TYPES.get(object_type, WHITE)
        self.image.fill(self.color)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement properties - synchronized with river flow
        self.vel_y = random.uniform(-0.5, 0.5)  # Slight vertical wobble
    
    def update(self):
        """Update the floating object position"""
        # Float with the river - stay in sync with the water texture
        # The river background moves by: x_pos = position - offset
        # As offset increases, background shifts left (water appears to flow right)
        # Objects floating ON the water should move with the WATER, not the camera
        # So they should move in the OPPOSITE direction of the offset change
        self.rect.x -= RIVER_FLOW_SPEED  # Inverted to match water flow
        self.rect.y += self.vel_y
        
        # Keep within vertical bounds with bounce (between pixels 100-225)
        if self.rect.top < 100:
            self.rect.top = 100
            self.vel_y *= -1
        elif self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.vel_y *= -1
