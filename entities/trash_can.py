"""
Trash cans where objects should be placed
"""
import pygame
from config import *


class TrashCan(pygame.sprite.Sprite):
    def __init__(self, x, y, can_type="general"):
        """
        Initialize a trash can
        
        Args:
            x (int): X position
            y (int): Y position
            can_type (str): Type of trash can (general, recycling, organic)
        """
        super().__init__()
        
        self.can_type = can_type
        
        # Create a simple rectangle sprite (replace with images later)
        self.width = 80
        self.height = 100
        self.image = pygame.Surface((self.width, self.height))
        
        # Different colors for different can types
        if can_type == "recycling":
            self.color = BLUE
        elif can_type == "organic":
            self.color = GREEN
        else:
            self.color = (100, 100, 100)  # Gray for general
        
        self.image.fill(self.color)
        
        # Draw a lid on top
        pygame.draw.rect(self.image, BLACK, (0, 0, self.width, 10))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        """Update trash can (static for now, but can add animations)"""
        pass
    
    def accepts_type(self, object_type):
        """
        Check if this trash can accepts a specific object type
        
        Args:
            object_type (str): Type of object
            
        Returns:
            bool: True if the can accepts this type
        """
        if self.can_type == "general":
            return True
        elif self.can_type == "recycling":
            return object_type in ["plastic", "metal", "paper"]
        elif self.can_type == "organic":
            return object_type == "organic"
        return False
