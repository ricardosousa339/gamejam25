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

# River bounds in source image coordinates (pixels in margens.png)
RIVER_IMAGE_BAND_TOP = 100
RIVER_IMAGE_BAND_BOTTOM = 225

# Pegador (Pool Net) settings
PEGADOR_SPEED = 5  # Horizontal movement speed
PEGADOR_VERTICAL_SPEED = 8  # Vertical movement speed
PEGADOR_MAX_FORCE = 100  # Maximum force for depth
PEGADOR_FORCE_CHARGE_RATE = 2  # How fast the force bar charges
PEGADOR_MARGIN_Y = SCREEN_HEIGHT - 70  # Y position when at the margin (more visible, less off-screen)
PEGADOR_SCALE = 1.0  # Scale factor for pegador sprite
PEGADOR_STUNNED_DURATION = 1000  # Duration in milliseconds when stunned after maxing out force bar

# Crocodile capture animation settings
CROCODILE_CAPTURE_DURATION = 600  # milliseconds - duration of capture animation (emerge + wobble)
CROCODILE_CAPTURE_WOBBLE_INTENSITY = 3.0  # pixels - intensity of wobble/shake during capture

class ObjectType():
    def __init__(self, type, image, scale):
        self.type = type
        self.image = image
        self.scale = scale

OBJECT_TYPES = {
    "cardboard": ObjectType("paper", "./assets/lixo/caixa.png", 1.2),
    "bag": ObjectType("mixed", "./assets/lixo/garbage-bag.png", 1.2),
    "big-bottle": ObjectType("plastic", "./assets/lixo/garrafa-grande.png", 1),
    "big-bottle-2": ObjectType("plastic", "./assets/lixo/garrafa-grande2.png", 1),
    "bottle": ObjectType("plastic", "./assets/lixo/garrafa.png", 1),
    "can": ObjectType("metal", "./assets/lixo/lata.png", 0.9),
    "small-can": ObjectType("metal", "./assets/lixo/latinha.png", 1),
    "spray-can": ObjectType("metal", "./assets/lixo/spray.png", 1),
    "big-glass-bottle": ObjectType("glass", "./assets/lixo/vidro-grande.png", 1),
    "glass-bottle": ObjectType("glass", "./assets/lixo/vidro.png", 1),
    "glass-bottle2": ObjectType("glass", "./assets/lixo/vidro2.png", 1),
}

# Sound settings
SOUND_ENABLED = True
SPLASH_SOUND_VOLUME = 0.7  # 0.0 to 1.0
CROCODILE_SOUND_VOLUME = 0.8  # 0.0 to 1.0
