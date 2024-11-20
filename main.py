import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up windowed mode
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set the window size
pygame.display.set_caption("Floppy Ball Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = [0, 100, 255]  # Starting color for pipes

# Game Variables
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3
BALL_RADIUS = 15
FONT = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Load high score from file
high_score = 0
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())

# Ball class
class Ball:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.is_alive = True
        self.color = self.random_color()  # Random starting color for the ball

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.color = self.random_color()  # Change color on flap

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(SCREEN, self.color, (self.x, int(self.y)), BALL_RADIUS)

    def random_color(self):
        return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

    def is_off_screen(self):
        return self.x < -PIPE_WIDTH

# Check for collision
def check_collision(ball, pipes):
    for pipe in pipes:
        if ball.x + BALL_RADIUS > pipe.x and ball.x - BALL_RADIUS < pipe.x + PIPE_WIDTH:
            if ball.y - BALL_RADIUS < pipe.height or ball.y + BALL_RADIUS > pipe.height + PIPE_GAP:
                return True
    if ball.y > SCREEN_HEIGHT or ball.y < 0:
        return True
    return False

# Display Score
def display_score(score):
    score_text = FONT.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

# Display Game Over Screen
def game_over_screen(score):
    global high_score
    game_over_text = FONT.render("Game Over! Press 'R' to Restart", True, BLACK)
    score_text = FONT.render(f"Your Score: {score}", True, BLACK)
    high_score_text = FONT.render(f"High Score: {high_score}", True, BLACK)
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60))
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 30))
    SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2))

# Restart game function
def restart_game():
    return Ball(), [Pipe(SCREEN_WIDTH)], 0

# Gradually shift the pipe color
def update_pipe_color():
    PIPE_COLOR[0] = (PIPE_COLOR[0] + 1) % 256
    PIPE_COLOR[1] = (PIPE_COLOR[1] + 2) % 256
    PIPE_COLOR[2] = (PIPE_COLOR[2] + 3) % 256

# Get bright background color based on score
def get_background_color(score):
    base_color = 150  # Minimum brightness level
    red = min(255, base_color + score * 2)
    green = min(255, base_color + score * 3)
    blue = min(255, base_color + score * 4)
    return (red, green, blue)

# Game loop
def game_loop():
    global high_score
    ball, pipes, score = restart_game()  # Initialize variables
    running = True

    while running:
        clock.tick(30)
        SCREEN.fill(get_background_color(score))  # Bright background color

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ball.is_alive:
                    ball.flap()
                elif not ball.is_alive and event.key == pygame.K_r:
                    ball, pipes, score = restart_game()  # Reset game if R is pressed after game over

        # Game logic
        if ball.is_alive:
            ball.move()
            ball.draw()
            
            # Move and draw pipes
            for pipe in pipes:
                pipe.move()
                pipe.draw()

            # Add new pipe and update score
            if pipes[0].is_off_screen():
                pipes.pop(0)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1
                update_pipe_color()  # Change pipe color when score increases
                
            # Check for collision
            if check_collision(ball, pipes):
                ball.is_alive = False
                if score > high_score:
                    high_score = score
                    with open("highscore.txt", "w") as file:
                        file.write(str(high_score))

        else:
            game_over_screen(score)

        # Display score
        display_score(score)

        # Update display
        pygame.display.flip()

    pygame.quit()

# Run the game
game_loop()
