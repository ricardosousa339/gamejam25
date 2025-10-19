"""
Menu system for start screen and credits
"""
import pygame
from config import *
from utils import resource_path


class MenuState:
    """Base class for menu states"""
    def __init__(self, screen):
        self.screen = screen
        self.next_state = None
    
    def handle_events(self, events):
        """Handle input events"""
        pass
    
    def update(self):
        """Update menu state"""
        pass
    
    def draw(self):
        """Draw menu"""
        pass


class StartScreen(MenuState):
    """Start screen with background image and menu options"""
    def __init__(self, screen):
        super().__init__(screen)
        
        # Load start screen background
        self.background = pygame.image.load(resource_path('assets/start_screen.png')).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load font
        try:
            self.title_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 48)
            self.menu_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 32)
            self.hint_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 20)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.title_font = pygame.font.Font(None, 48)
            self.menu_font = pygame.font.Font(None, 32)
            self.hint_font = pygame.font.Font(None, 20)
        
        # Menu options
        self.selected_option = 0
        self.options = ["JOGAR", "CREDITOS"]
        
        # Animation
        self.blink_timer = 0
        self.show_hint = True
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        self.next_state = "story"  # Go to story/instructions first
                    elif self.selected_option == 1:
                        self.next_state = "credits"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Allow clicking to go to story
                self.next_state = "story"
    
    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 30:  # Blink every 30 frames (0.5s at 60fps)
            self.blink_timer = 0
            self.show_hint = not self.show_hint
    
    def draw(self):
        """Draw start screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Position text in lower portion of screen
        menu_y_start = SCREEN_HEIGHT - 250
        
        # Draw menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, menu_y_start + i * 60))
            self.screen.blit(text, text_rect)
        
        # Draw hint at the bottom
        if self.show_hint:
            hint_text = "Pressione ENTER ou Clique para comecar"
            hint = self.hint_font.render(hint_text, True, WHITE)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(hint, hint_rect)


class CreditsScreen(MenuState):
    """Credits screen"""
    def __init__(self, screen):
        super().__init__(screen)
        
        # Load font
        try:
            self.title_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 56)
            self.name_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 36)
            self.hint_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 24)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.title_font = pygame.font.Font(None, 56)
            self.name_font = pygame.font.Font(None, 36)
            self.hint_font = pygame.font.Font(None, 24)
        
        # Credits info
        self.credits = [
            ("CREDITOS", self.title_font, YELLOW),
            ("", None, None),  # Spacing
            ("Desenvolvido por:", self.hint_font, WHITE),
            ("", None, None),  # Spacing
            ("Ricardo Henrique", self.name_font, WHITE),
            ("Mateus Rosario", self.name_font, WHITE),
        ]
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    self.next_state = "start"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.next_state = "start"
    
    def draw(self):
        """Draw credits screen"""
        # Dark background
        self.screen.fill((20, 40, 60))
        
        # Draw credits centered
        y_offset = 150
        line_spacing = 60
        
        for text_str, font, color in self.credits:
            if text_str == "":  # Spacing
                y_offset += line_spacing // 2
                continue
            
            text = font.render(text_str, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += line_spacing
        
        # Draw back hint at bottom
        hint_text = "Pressione ENTER para voltar"
        hint = self.hint_font.render(hint_text, True, WHITE)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)


class StoryScreen(MenuState):
    """Story and instructions screen"""
    def __init__(self, screen):
        super().__init__(screen)
        
        # Load font
        try:
            self.title_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 40)
            self.text_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 16)
            self.hint_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 20)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.title_font = pygame.font.Font(None, 40)
            self.text_font = pygame.font.Font(None, 16)
            self.hint_font = pygame.font.Font(None, 20)
        
        # Story and instructions
        self.story_lines = [
            "O rio está poluido e precisa da sua ajuda!",
            "",
            "Use seu pegador de piscina para limpar o rio,",
            "mas cuidado com os crocodilos famintos!",
        ]
        
        self.instructions = [
            "CONTROLES:",
            "",
            "Setas <- -> : Mover o pegador",
            "ESPACO (segurar): Carregar forca",
            "ESPACO (soltar): Mergulhar e coletar",
            "",
            "Colete o lixo flutuante",
            "Evite os crocodilos!",
            "Voce tem 3 vidas - use com sabedoria",
        ]
        
        # Animation
        self.blink_timer = 0
        self.show_hint = True
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.next_state = "game"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.next_state = "game"
    
    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.blink_timer = 0
            self.show_hint = not self.show_hint
    
    def draw(self):
        """Draw story and instructions"""
        # Gradient background (river themed)
        for y in range(SCREEN_HEIGHT):
            color_factor = y / SCREEN_HEIGHT
            r = int(30 + (60 - 30) * color_factor)
            g = int(120 + (160 - 120) * color_factor)
            b = int(180 + (220 - 180) * color_factor)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Title
        title = self.title_font.render("CROCOLIXO", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title, title_rect)
        
        # Story section
        y_offset = 100
        for line in self.story_lines:
            if line == "":
                y_offset += 15
                continue
            text = self.text_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
        
        # Separator
        y_offset += 20
        pygame.draw.line(self.screen, YELLOW, 
                        (SCREEN_WIDTH // 4, y_offset), 
                        (3 * SCREEN_WIDTH // 4, y_offset), 3)
        y_offset += 30
        
        # Instructions section
        for line in self.instructions:
            if line == "":
                y_offset += 15
                continue
            
            # Highlight the CONTROLES title
            color = YELLOW if "CONTROLES" in line else WHITE
            text = self.text_font.render(line, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
        
        # Hint to continue
        if self.show_hint:
            hint_text = "Pressione ENTER ou ESPACO para comecar!"
            hint = self.hint_font.render(hint_text, True, YELLOW)
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40))
            self.screen.blit(hint, hint_rect)


class GameOverScreen(MenuState):
    """Game Over screen with restart option"""
    def __init__(self, screen):
        super().__init__(screen)
        
        # Load font
        try:
            self.title_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 64)
            self.menu_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 32)
            self.hint_font = pygame.font.Font(resource_path('assets/fonts/upheaval.ttf'), 24)
        except:
            print("Warning: Could not load upheaval.ttf, using default font")
            self.title_font = pygame.font.Font(None, 64)
            self.menu_font = pygame.font.Font(None, 32)
            self.hint_font = pygame.font.Font(None, 24)
        
        # Menu options
        self.selected_option = 0
        self.options = ["JOGAR NOVAMENTE", "MENU PRINCIPAL"]
        
        # Animation
        self.blink_timer = 0
        self.show_title = True
        self.final_score = 0
    
    def set_score(self, score):
        """Set the final score to display"""
        self.final_score = score
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.selected_option == 0:
                        self.next_state = "restart"
                    elif self.selected_option == 1:
                        self.next_state = "start"
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click to restart
                self.next_state = "restart"
    
    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 20:  # Blink every 20 frames
            self.blink_timer = 0
            self.show_title = not self.show_title
    
    def draw(self):
        """Draw game over screen"""
        # Dark red background
        self.screen.fill((80, 20, 20))
        
        # Game Over title (blinking)
        if self.show_title:
            title = self.title_font.render("GAME OVER", True, RED)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(title, title_rect)
        
        # Score
        score_text = self.hint_font.render(f"Pontuacao Final: {self.final_score}", True, YELLOW)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(score_text, score_rect)
        
        # Menu options
        menu_y_start = 300
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, menu_y_start + i * 60))
            self.screen.blit(text, text_rect)
        
        # Hint at the bottom
        hint_text = "Use setas para navegar - ENTER para selecionar"
        hint = self.hint_font.render(hint_text, True, WHITE)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(hint, hint_rect)


class MenuManager:
    """Manages menu states and transitions"""
    def __init__(self, screen):
        self.screen = screen
        self.current_state = None
        self.states = {
            "start": StartScreen(screen),
            "credits": CreditsScreen(screen),
            "story": StoryScreen(screen),
            "gameover": GameOverScreen(screen),
        }
        self.set_state("start")
        self.start_game = False
        self.restart_game = False
    
    def set_state(self, state_name):
        """Change to a different menu state"""
        if state_name in self.states:
            self.current_state = self.states[state_name]
            self.current_state.next_state = None
        elif state_name == "game":
            self.start_game = True
        elif state_name == "restart":
            self.restart_game = True
    
    def set_game_over(self, score):
        """Show game over screen with final score"""
        self.states["gameover"].set_score(score)
        self.set_state("gameover")
    
    def handle_events(self, events):
        """Handle input events"""
        self.current_state.handle_events(events)
    
    def update(self):
        """Update current state"""
        self.current_state.update()
        
        # Check for state transition
        if self.current_state.next_state:
            self.set_state(self.current_state.next_state)
    
    def draw(self):
        """Draw current state"""
        self.current_state.draw()
    
    def should_start_game(self):
        """Check if player wants to start the game"""
        return self.start_game
    
    def should_restart_game(self):
        """Check if player wants to restart the game"""
        return self.restart_game
    
    def reset_flags(self):
        """Reset start and restart flags"""
        self.start_game = False
        self.restart_game = False
