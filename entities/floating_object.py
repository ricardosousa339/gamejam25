"""
Floating objects that move down the river
"""
import pygame
import random
from config import *
from utils import resource_path


class FloatingObject(pygame.sprite.Sprite):
    WIDTH = 40
    HEIGHT = 40

    def __init__(self, x, y, min_y, max_y, object_type="plastic"):
        """
        Initialize a floating object
        
        Args:
            x (int): Initial x position
            y (int): Initial y position
            object_type (str): Type of object (plastic, metal, organic, paper)
        """
        super().__init__()
        
        self.object_type = object_type
        self.object = OBJECT_TYPES.get(object_type)
        
        # Create a simple rectangle sprite (replace with images later)
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.image = pygame.image.load(resource_path(self.object.image))
        # self.color = OBJECT_TYPES.get(object_type, WHITE)
        # self.image.fill(self.color)
        self.rotation = random.randint(0, 359)
        self.image = pygame.transform.rotate(self.image, self.rotation)
        image_width = self.image.get_width() * self.object.scale
        image_height = self.image.get_height() * self.object.scale
        self.image = pygame.transform.smoothscale(self.image, (image_width, image_height))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement properties - synchronized with river flow
        self.vel_y = random.uniform(-0.5, 0.5)  # Slight vertical wobble
        self.min_y = min_y
        self.max_y = max_y
        
        # Capture state
        self.is_captured = False
    
    def update(self):
        """Update the floating object position"""
        # Only move if not captured
        if not self.is_captured:
            # Float with the river - stay in sync with the water texture
            self.rect.x -= RIVER_FLOW_SPEED
            self.rect.y += self.vel_y
            
            # Keep within vertical bounds with bounce
            if self.rect.top < self.min_y:
                self.rect.top = self.min_y
                self.vel_y *= -1
            elif self.rect.bottom > self.max_y:
                self.rect.bottom = self.max_y
                self.vel_y *= -1
