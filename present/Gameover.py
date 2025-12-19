import pygame

class GameOver:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.WHITE = (255, 255, 255)

        # 1. Attempt to match the font style from your score.py (size 60)
        try:
            self.large_font = pygame.font.Font(None, 60)
            self.small_font = pygame.font.Font(None, 40)
        except pygame.error:
            self.large_font = pygame.font.SysFont('Arial', 60, bold=True)
            self.small_font = pygame.font.SysFont('Arial', 40)

    def draw(self, screen, final_score):
        """
        Draws the Game Over text and the final score provided by score.py
        """
        # Draw "GAME OVER"
        game_over_text = self.large_font.render("GAME OVER", True, self.WHITE)
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        
        # Draw the Final Score
        score_text = self.large_font.render(f"Score: {int(final_score)}", True, self.WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        # Draw Restart Prompt
        restart_text = self.small_font.render("Press SPACE to Restart", True, self.WHITE)
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

    def check_for_restart(self, event):
        """
        Returns True if the user presses Space to restart
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True
        return False