import pygame
import random

# Initialize Pygame immediately so we can use its features
pygame.init()

# ==========================================
# PERSON 1: THE ARCHITECT (Configuration)
# Responsibility: Define screen size, colors, and game speed.
# ==========================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Team Start-Up Space Shooter")

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

clock = pygame.time.Clock()
FPS = 60


# ==========================================
# PERSON 2: THE PILOT (Player Class)
# Responsibility: Create the player rect, handle arrow key movement.
# ==========================================
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 100
        self.speed = 5
        # Defining the hitbox (Rect)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed

    def draw(self):
        # Draw a Blue Ship (Triangle shape logic using polygon for style)
        points = [
            (self.rect.x + self.width // 2, self.rect.y),              # Top tip
            (self.rect.x, self.rect.y + self.height),                  # Bottom left
            (self.rect.x + self.width, self.rect.y + self.height)      # Bottom right
        ]
        pygame.draw.polygon(screen, BLUE, points)


# ==========================================
# PERSON 3: THE INVADERS (Enemy Class)
# Responsibility: Spawn enemies, make them fall down.
# ==========================================
class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-100, -40) # Start off-screen
        self.speed = random.randint(3, 7)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.rect.y += self.speed
        # If enemy goes off screen, respawn at top with new speed
        if self.rect.y > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 8)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


# ==========================================
# PERSON 4: THE GUNNER (Bullet Class)
# Responsibility: Create bullets, move them up.
# ==========================================
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = 10
        self.active = True

    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.active = False # Deactivate if off screen

    def draw(self):
        pygame.draw.rect(screen, YELLOW, self.rect)


# ==========================================
# PERSON 5: THE PHYSICIST (Collisions)
# Responsibility: Check if bullets hit enemies or enemies hit player.
# ==========================================
def check_collisions(player, enemies, bullets):
    score_increment = 0
    game_over = False

    # Check Bullet -> Enemy collisions
    for bullet in bullets:
        if not bullet.active:
            continue
        
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                bullet.active = False
                enemy.reset()
                score_increment += 10
    
    # Check Player -> Enemy collisions
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            game_over = True

    return score_increment, game_over


# ==========================================
# PERSON 6: THE ARTIST (Background/Stars)
# Responsibility: Create a moving starfield for effect.
# ==========================================
class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.size)


# ==========================================
# PERSON 7: THE INTERFACE (UI & Text)
# Responsibility: Display score and Game Over messages.
# ==========================================
def draw_ui(score, is_game_over):
    font = pygame.font.SysFont("arial", 30)
    
    # Draw Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if is_game_over:
        over_font = pygame.font.SysFont("arial", 60, bold=True)
        over_text = over_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        
        # Center the text
        text_rect = over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
        
        screen.blit(over_text, text_rect)
        screen.blit(restart_text, restart_rect)


# ==========================================
# PERSON 8: THE DIRECTOR (Main Loop)
# Responsibility: Tie inputs, updates, and drawing together.
# ==========================================
def main():
    running = True
    game_over = False
    score = 0

    # Instantiate objects
    player = Player()
    
    # Create a list of 5 enemies
    enemies = [Enemy() for _ in range(5)]
    
    # List to hold bullets
    bullets = []
    
    # Create 50 stars
    stars = [Star() for _ in range(50)]

    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if not game_over and event.key == pygame.K_SPACE:
                    # Fire bullet from center of ship
                    bullets.append(Bullet(player.rect.x + player.width//2, player.rect.y))
                
                if game_over and event.key == pygame.K_r:
                    # Reset Game
                    main() # Restart the function
                    return

        # 2. Updates
        if not game_over:
            player.move()
            
            for enemy in enemies:
                enemy.move()
            
            # Move bullets and remove inactive ones
            for bullet in bullets:
                bullet.move()
            bullets = [b for b in bullets if b.active]

            # Move stars (Background)
            for star in stars:
                star.move()

            # Check Collisions (Person 5's logic)
            points, is_hit = check_collisions(player, enemies, bullets)
            score += points
            if is_hit:
                game_over = True

        # 3. Drawing
        screen.fill(BLACK) # Clear screen
        
        # Draw background stars first
        for star in stars:
            star.draw()
            
        player.draw()
        
        for enemy in enemies:
            enemy.draw()
            
        for bullet in bullets:
            bullet.draw()
            
        # Draw UI on top of everything
        draw_ui(score, game_over)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()