import pygame
import random

pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SPEED = 10

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

font = pygame.font.Font(None, 36)

# Function to load or initialize high score
def load_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Function to save new high score
def save_high_score(score):
    with open('high_score.txt', 'w') as f:
        f.write(str(score))

high_score = load_high_score()

# Set up the start button
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

# Start screen loop
game_over = True
while game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                # Start the game
                snake = [(WIDTH // 2, HEIGHT // 2)]
                food = (random.randint(0, WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE, random.randint(0, HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)
                direction = (1, 0)
                score = 0
                game_over = False

    # Draw the start screen
    screen.fill(BLACK)
    text = font.render('Snake Game', True, WHITE)
    screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 - 75))
    
    # Display high score
    text = font.render(f'High Score: {high_score}', True, WHITE)
    screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 - 25))
    
    pygame.draw.rect(screen, WHITE, start_button)
    text = font.render('START', True, BLACK)
    screen.blit(text, (WIDTH // 2 - 40, HEIGHT // 2))
    
    pygame.display.flip()

# Game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Move the snake
    head = (snake[0][0] + direction[0] * GRID_SIZE, snake[0][1] + direction[1] * GRID_SIZE)
    snake.insert(0, head)

    # Check if the snake has eaten the food
    if snake[0] == food:
        food = (random.randint(0, WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE, random.randint(0, HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE)
        score += 1
    else:
        snake.pop()

    # Check if the snake has hit the wall or itself
    if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
        snake[0][1] < 0 or snake[0][1] >= HEIGHT or
        snake[0] in snake[1:]):
        game_over = True
        break

    # Draw everything
    screen.fill(BLACK)
    for pos in snake:
        pygame.draw.rect(screen, GREEN, (pos[0], pos[1], GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.delay(1000 // SPEED)

# Update high score if necessary
if score > high_score:
    high_score = score
    save_high_score(high_score)

# Game over screen
screen.fill(BLACK)
text = font.render('GAME OVER', True, WHITE)
screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 - 18))
text = font.render('You crashed!', True, WHITE)
screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 + 18))
text = font.render(f'Final Score: {score}', True, WHITE)
screen.blit(text, (WIDTH // 2 - 75, HEIGHT // 2 + 54))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()
quit()
