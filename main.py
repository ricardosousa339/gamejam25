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

    # Create game with debug flag
    game = Game(debug=args.debug)
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
