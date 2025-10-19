"""
Game configuration and constants
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "River Cleanup"

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# River colors
RIVER_COLOR = (64, 164, 223)  # Light blue
RIVER_FLOW_COLOR = (100, 180, 230)  # Lighter blue for flow lines

# Game settings
GRAVITY = 0.5
RIVER_FLOW_SPEED = -2
OBJECT_SPAWN_RATE = 2000  # milliseconds

# Object types and colors
OBJECT_TYPES = {
    "plastic": RED,
    "metal": (128, 128, 128),  # Gray
    "organic": GREEN,
    "paper": (210, 180, 140)   # Tan
}
