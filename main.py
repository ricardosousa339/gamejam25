"""
Game Jam 2025 - Crocolixo
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
    parser = argparse.ArgumentParser(description='Crocolixo - River Cleanup Game')
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

    # Main game loop
    while running:
        # Menu loop
        menu_manager.reset_flags()
        while running and not menu_manager.should_start_game() and not menu_manager.should_restart_game():
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
        if running and (menu_manager.should_start_game() or menu_manager.should_restart_game()):
            game = Game(debug=args.debug)
            game.run()
            
            # Check if game ended due to losing all lives
            if game.game_over:
                # Show game over screen with final score
                menu_manager.set_game_over(game.score)
            else:
                # Player quit the game (ESC), go back to main menu
                menu_manager.set_state("start")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
