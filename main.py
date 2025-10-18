"""
Game Jam 2025 - River Cleanup Game
Main entry point
"""
import pygame
import sys
from game import Game


def main():
    """Initialize and run the game"""
    pygame.init()
    
    game = Game()
    game.run()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
