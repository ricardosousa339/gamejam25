"""
Game Jam 2025 - River Cleanup Game
Main entry point
"""
import pygame
import sys
import argparse
from game import Game


def main():
    """Initialize and run the game"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='River Cleanup Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    pygame.init()
    
    # Explicitly initialize mixer for sound support
    # This is important for some systems where pygame.init() doesn't auto-initialize mixer
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    except pygame.error as e:
        # No audio device available (headless system, etc.)
        # Game will run normally without sound
        pass

    # Create game with debug flag
    game = Game(debug=args.debug)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
