"""
Pegador Counter - Shows remaining pegador lives (HP system)
"""
import pygame
from config import *
from utils import resource_path


class PegadorCounter:
    """
    Visual counter showing remaining pegador lives.
    Displays 3 small pegador sprites at the top of the screen.
    """

    def __init__(self, x, y, max_lives=3):
        """
        Initialize the pegador counter

        Args:
            x (int): X position of the first pegador icon
            y (int): Y position of the pegador icons
            max_lives (int): Maximum number of lives (default 3)
        """
        self.x = x
        self.y = y
        self.max_lives = max_lives
        self.current_lives = max_lives

        # Load and scale pegador sprite
        pegador_image = pygame.image.load(resource_path('assets/pegador_frente_comprido.png')).convert_alpha()

        # Scale to small icon size
        icon_scale = 0.25  # Increased size for better visibility
        icon_width = int(pegador_image.get_width() * icon_scale)
        icon_height = int(pegador_image.get_height() * icon_scale)

        self.pegador_icon = pygame.transform.smoothscale(pegador_image, (icon_width, icon_height))

        # Spacing between icons
        self.icon_spacing = icon_width + 15

    def lose_life(self):
        """
        Decrease the life counter by 1

        Returns:
            bool: True if lives remaining, False if game over (0 lives)
        """
        if self.current_lives > 0:
            self.current_lives -= 1
            print(f"[COUNTER] Lost a life! Remaining: {self.current_lives}/{self.max_lives}")

        return self.current_lives > 0

    def reset(self):
        """Reset the counter to maximum lives"""
        self.current_lives = self.max_lives
        print(f"[COUNTER] Reset to {self.max_lives} lives")

    def is_game_over(self):
        """
        Check if game is over (no lives remaining)

        Returns:
            bool: True if no lives left, False otherwise
        """
        return self.current_lives <= 0

    def draw(self, screen):
        """
        Draw the pegador life icons on the screen

        Args:
            screen (pygame.Surface): The screen to draw on
        """
        for i in range(self.max_lives):
            icon_x = self.x + (i * self.icon_spacing)
            icon_y = self.y

            if i < self.current_lives:
                # Draw full opacity for remaining lives
                screen.blit(self.pegador_icon, (icon_x, icon_y))
            else:
                # Draw grayed out/transparent for lost lives
                faded_icon = self.pegador_icon.copy()
                faded_icon.set_alpha(50)  # Very transparent
                screen.blit(faded_icon, (icon_x, icon_y))
