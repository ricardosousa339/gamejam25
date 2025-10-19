"""
Placa entity - displays environmental messages at the top of the screen
"""
import pygame
import random
from utils import resource_path


class Placa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Initialize the placa (sign) with a random environmental message
        
        Args:
            x (int): X position (center)
            y (int): Y position (top)
        """
        super().__init__()
        
        # Load placa image and scale it up
        placa_original = pygame.image.load(resource_path('assets/placa.png')).convert_alpha()
        
        # Scale placa to be 2x larger
        scale_factor = 2.0
        new_width = int(placa_original.get_width() * scale_factor)
        new_height = int(placa_original.get_height() * scale_factor)
        self.base_image = pygame.transform.smoothscale(placa_original, (new_width, new_height))
        
        # Load font with smaller size to fit longer phrases
        try:
            self.font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 18)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.font = pygame.font.Font(None, 16)
        
        # Load phrases from file
        self.phrases = self._load_phrases()
        
        # Select a random phrase
        self.current_phrase = random.choice(self.phrases) if self.phrases else "Preserve a natureza!"
        
        # Create the final image with text
        self._create_image_with_text()
        
        # Position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
    
    def _load_phrases(self):
        """Load phrases from frases.txt file"""
        phrases = []
        try:
            with open(resource_path('assets/frases.txt'), 'r', encoding='utf-8') as f:
                phrases = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Warning: frases.txt not found, using default phrase")
            phrases = ["Preserve a natureza!"]
        return phrases
    
    def _create_image_with_text(self):
        """Create the final image with the placa background and text"""
        # Create a copy of the base image
        self.image = self.base_image.copy()
        
        # Define margins - keep text within these bounds
        margin_x = 30  # Horizontal margins
        margin_y = 40  # Top margin - text starts higher up
        max_width = self.image.get_width() - (margin_x * 2)
        
        # Render the text
        # Use black color for text
        text_color = (0, 0, 0)
        text_surface = self.font.render(self.current_phrase, True, text_color)
        
        # Check if text is too wide and needs wrapping
        if text_surface.get_width() > max_width:
            # Split text into multiple lines
            words = self.current_phrase.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.font.render(test_line, True, text_color)
                
                if test_surface.get_width() <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        # Single word is too long, add it anyway
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Render each line starting from top margin
            line_height = self.font.get_height()
            y_offset = margin_y  # Start from top margin instead of centering
            
            for line in lines:
                line_surface = self.font.render(line, True, text_color)
                line_rect = line_surface.get_rect()
                line_rect.centerx = self.image.get_width() // 2
                line_rect.top = y_offset
                self.image.blit(line_surface, line_rect)
                y_offset += line_height
        else:
            # Text fits in one line, position it near the top
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.image.get_width() // 2
            text_rect.top = margin_y
            self.image.blit(text_surface, text_rect)
    
    def update(self):
        """Update method (placa is static, so nothing to do)"""
        pass
