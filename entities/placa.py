"""
Placa entity - displays environmental messages at the top of the screen
"""
import pygame
import random
from utils import resource_path


class Placa(pygame.sprite.Sprite):
    def __init__(self, x, y, debug=False):
        """
        Initialize the placa (sign) with a random environmental message

        Args:
            x (int): X position (center)
            y (int): Y position (top)
            debug (bool): Show text boundary lines for debugging
        """
        super().__init__()
        self.debug = debug
        
        # Load placa image and scale it up
        placa_original = pygame.image.load(resource_path('assets/placa.png')).convert_alpha()

        # Scale placa to be 1.6x larger (reduced from 2.0x)
        scale_factor = 1.6
        new_width = int(placa_original.get_width() * scale_factor)
        new_height = int(placa_original.get_height() * scale_factor)
        self.base_image = pygame.transform.smoothscale(placa_original, (new_width, new_height))
        
        # Load font with smaller size to fit longer phrases
        try:
            self.font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 15)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.font = pygame.font.Font(None, 12)
        
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
        # Define padding - keep text within these bounds (away from edges)
        padding_x = 30  # Horizontal padding (left and right)
        padding_top = 10  # Top padding
        max_width = self.base_image.get_width() - (padding_x * 2)

        # Render the text
        # Use black color for text
        text_color = (0, 0, 0)
        text_surface = self.font.render(self.current_phrase, True, text_color)

        # Calculate text lines
        lines = []

        # Check if text is too wide and needs wrapping
        if text_surface.get_width() > max_width:
            # Split text into multiple lines
            words = self.current_phrase.split()
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
        else:
            # Text fits in one line
            lines = [self.current_phrase]

        # Calculate total text height needed
        line_height = self.font.get_height()
        total_text_height = len(lines) * line_height

        # Calculate final image height - allows overflow below placa
        required_height = padding_top + total_text_height
        final_height = max(self.base_image.get_height(), required_height)

        # Create a larger surface that can contain overflow
        self.image = pygame.Surface((self.base_image.get_width(), final_height), pygame.SRCALPHA)

        # Draw the placa background at the top
        self.image.blit(self.base_image, (0, 0))

        # DEBUG: Draw red rectangle showing text boundaries (only if debug mode enabled)
        if self.debug:
            red = (255, 0, 0)
            # Top line
            pygame.draw.line(self.image, red, (padding_x, padding_top),
                            (self.image.get_width() - padding_x, padding_top), 2)
            # Bottom line
            pygame.draw.line(self.image, red, (padding_x, padding_top + total_text_height),
                            (self.image.get_width() - padding_x, padding_top + total_text_height), 2)
            # Left line
            pygame.draw.line(self.image, red, (padding_x, padding_top),
                            (padding_x, padding_top + total_text_height), 2)
            # Right line
            pygame.draw.line(self.image, red, (self.image.get_width() - padding_x, padding_top),
                            (self.image.get_width() - padding_x, padding_top + total_text_height), 2)

        # Render each line (will overflow below placa if needed)
        y_offset = padding_top
        for line in lines:
            line_surface = self.font.render(line, True, text_color)
            line_rect = line_surface.get_rect()
            line_rect.centerx = self.image.get_width() // 2
            line_rect.top = y_offset
            self.image.blit(line_surface, line_rect)
            y_offset += line_height
    
    def update(self):
        """Update method (placa is static, so nothing to do)"""
        pass
