"""
Game Jam 2025 - River Cleanup Game
Main entry point
"""
import pygame
import sys
import argparse
from game import Game
from menu import MenuManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE


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

    # Create screen and clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()

    # Start with menu
    menu_manager = MenuManager(screen)
    running = True

    # Menu loop
    while running and not menu_manager.should_start_game():
        clock.tick(FPS)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        menu_manager.handle_events(events)
        menu_manager.update()
        menu_manager.draw()
        
        pygame.display.flip()

    # Start game if player chose to play
    if running and menu_manager.should_start_game():
        game = Game(debug=args.debug)
        game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
