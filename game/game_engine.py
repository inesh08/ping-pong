import pygame
from .paddle import Paddle
from .ball import Ball
from .sounds import SoundManager

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over = False
        self.winner = None
        self.winning_score = 5
        self.show_replay_menu = False
        self.replay_options = [3, 5, 7]
        self.selected_option = 1  # Index for best of 5 (default)
        self.sound_manager = SoundManager()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)
        else:
            # Handle game over input
            if self.show_replay_menu:
                if keys[pygame.K_3]:
                    self.winning_score = 3
                    self.reset_game()
                elif keys[pygame.K_5]:
                    self.winning_score = 5
                    self.reset_game()
                elif keys[pygame.K_7]:
                    self.winning_score = 7
                    self.reset_game()
                elif keys[pygame.K_ESCAPE]:
                    return False
            else:
                if keys[pygame.K_SPACE]:
                    self.show_replay_menu = True
                if keys[pygame.K_ESCAPE]:
                    return False
        return True

    def update(self):
        if not self.game_over:
            self.ball.move(self.sound_manager)
            self.ball.check_collision(self.player, self.ai, self.sound_manager)

            if self.ball.x <= 0:
                self.ai_score += 1
                self.sound_manager.play_sound('score')
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.sound_manager.play_sound('score')
                self.ball.reset()

            # Check for game over
            if self.player_score >= self.winning_score:
                self.game_over = True
                self.winner = "Player"
            elif self.ai_score >= self.winning_score:
                self.game_over = True
                self.winner = "AI"

            self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))
        
        # Draw game over screen
        if self.game_over:
            if self.show_replay_menu:
                self.render_replay_menu(screen)
            else:
                self.render_game_over(screen)
    
    def render_game_over(self, screen):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Winner text
        winner_font = pygame.font.SysFont("Arial", 48)
        winner_text = winner_font.render(f"{self.winner} Wins!", True, WHITE)
        winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2 - 50))
        screen.blit(winner_text, winner_rect)
        
        # Instructions
        instruction_font = pygame.font.SysFont("Arial", 24)
        instruction_text = instruction_font.render("Press SPACE to choose game mode or ESC to exit", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(self.width//2, self.height//2 + 20))
        screen.blit(instruction_text, instruction_rect)
    
    def render_replay_menu(self, screen):
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Title
        title_font = pygame.font.SysFont("Arial", 36)
        title_text = title_font.render("Choose Game Mode", True, WHITE)
        title_rect = title_text.get_rect(center=(self.width//2, self.height//2 - 100))
        screen.blit(title_text, title_rect)
        
        # Options
        option_font = pygame.font.SysFont("Arial", 28)
        options = ["Best of 3 (Press 3)", "Best of 5 (Press 5)", "Best of 7 (Press 7)"]
        
        for i, option in enumerate(options):
            option_text = option_font.render(option, True, WHITE)
            option_rect = option_text.get_rect(center=(self.width//2, self.height//2 - 20 + i * 40))
            screen.blit(option_text, option_rect)
        
        # Exit option
        exit_font = pygame.font.SysFont("Arial", 24)
        exit_text = exit_font.render("Press ESC to exit", True, WHITE)
        exit_rect = exit_text.get_rect(center=(self.width//2, self.height//2 + 120))
        screen.blit(exit_text, exit_rect)
    
    def reset_game(self):
        """Reset the game to start a new round"""
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner = None
        self.show_replay_menu = False
        self.ball.reset()
        
        # Reset paddle positions
        self.player.y = self.height // 2 - 50
        self.ai.y = self.height // 2 - 50
