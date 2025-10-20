"""
Pollution Bar - Shows river pollution level based on caught/lost trash
"""
import pygame
from config import *
from utils import resource_path


class PollutionBar:
    """
    Visual bar showing pollution level of the river.
    Displayed horizontally on the top-right corner.
    - Starts at center (50% pollution)
    - INCREASES when trash is lost (passes screen) - more pollution
    - DECREASES when trash is caught - less pollution
    - Color changes based on pollution level: Green (low), Blue (medium), Red (high)
    """

    def __init__(self):
        """
        Initialize the pollution bar
        """
        # Position (top-right corner, horizontal)
        self.x = SCREEN_WIDTH - POLLUTION_BAR_WIDTH - POLLUTION_BAR_MARGIN
        self.y = POLLUTION_BAR_MARGIN
        self.width = POLLUTION_BAR_WIDTH
        self.height = POLLUTION_BAR_HEIGHT

        # Pollution points - starts at center
        self.max_points = POLLUTION_BAR_MAX_POINTS
        self.current_points = self.max_points // 2  # Start at 50%

        # Color thresholds (inverted logic)
        self.green_threshold = self.max_points * 0.33  # Below 33% = green (low pollution)
        self.blue_threshold = self.max_points * 0.66  # 33-66% = blue (medium pollution)
        # Above 66% = red (high pollution)

        # Load custom font
        self.font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 16)

    def lose_trash(self):
        """
        Called when trash passes the right side of screen (lost)
        INCREASES pollution (bar fills to the right)
        """
        self.current_points = min(self.max_points, self.current_points + POLLUTION_BAR_POINTS_LOST_PER_TRASH)
        print(f"[POLLUTION BAR] Lost trash! Pollution increased: {self.current_points}/{self.max_points}")

    def catch_trash(self):
        """
        Called when trash is caught by the pegador
        DECREASES pollution (bar empties to the left)
        """
        self.current_points = max(0, self.current_points - POLLUTION_BAR_POINTS_GAINED_PER_TRASH)
        print(f"[POLLUTION BAR] Caught trash! Pollution decreased: {self.current_points}/{self.max_points}")

    def is_game_over(self):
        """
        Check if pollution bar has reached maximum (game over)

        Returns:
            bool: True if bar is full (max pollution), False otherwise
        """
        return self.current_points >= self.max_points

    def reset(self):
        """Reset the bar to center position"""
        self.current_points = self.max_points // 2
        print(f"[POLLUTION BAR] Reset to {self.current_points}/{self.max_points}")

    def _get_bar_color(self):
        """
        Get the color of the bar based on current pollution level

        Returns:
            tuple: RGB color tuple
        """
        if self.current_points <= self.green_threshold:
            return GREEN  # Low pollution = green
        elif self.current_points <= self.blue_threshold:
            return BLUE  # Medium pollution = blue
        else:
            return RED  # High pollution = red

    def draw(self, screen):
        """
        Draw the pollution bar on the screen (horizontal)

        Args:
            screen (pygame.Surface): The screen to draw on
        """
        # Draw border (black outline)
        border_thickness = 2
        pygame.draw.rect(screen, WHITE,
                        (self.x - border_thickness,
                         self.y - border_thickness,
                         self.width + border_thickness * 2,
                         self.height + border_thickness * 2))

        # Draw background (white/empty bar)
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

        # Draw center marker (vertical white line at center)
        center_x = self.x + (self.width // 2)
        marker_thickness = 2
        pygame.draw.line(screen, WHITE,
                        (center_x, self.y),
                        (center_x, self.y + self.height),
                        marker_thickness)

        # Calculate filled width based on current pollution
        fill_percentage = self.current_points / self.max_points
        fill_width = int(fill_percentage * self.width)

        # Get bar color based on pollution level
        bar_color = self._get_bar_color()

        # Draw filled portion from left to right
        if fill_width > 0:
            pygame.draw.rect(screen, bar_color,
                           (self.x, self.y, fill_width, self.height))

        # Draw label "Poluição" below the bar
        label_text = self.font.render("POLUIÇÃO", True, WHITE)
        label_rect = label_text.get_rect()
        label_rect.centerx = self.x + (self.width // 2)
        label_rect.top = self.y + self.height + 3
        screen.blit(label_text, label_rect)
