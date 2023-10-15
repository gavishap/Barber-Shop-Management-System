import pygame
import random

# Initialize Pygame
pygame.init()


# Set up the display window
WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize a clock
clock = pygame.time.Clock()

# Initialize game variables
score = 0
snake_size = 10
snake_speed = 14
food_eaten = False
game_over = False
direction = 'RIGHT'  # Add this line
font = pygame.font.SysFont(None, 25)

# Create the snake and food objects
snake_body = [(100, 100), (90, 100), (80, 100)]
food = (random.randint(0, WINDOW_SIZE[0]-10), random.randint(0, WINDOW_SIZE[1]-10))

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the snake
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        direction = 'RIGHT'
    elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        direction = 'UP'
    elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
        direction = 'DOWN'

    if direction == 'LEFT':
        new_head = ((snake_body[-1][0]-snake_speed) % WINDOW_SIZE[0], snake_body[-1][1])
    elif direction == 'RIGHT':
        new_head = ((snake_body[-1][0]+snake_speed) % WINDOW_SIZE[0], snake_body[-1][1])
    elif direction == 'UP':
        new_head = (snake_body[-1][0], (snake_body[-1][1]-snake_speed) % WINDOW_SIZE[1])
    elif direction == 'DOWN':
        new_head = (snake_body[-1][0], (snake_body[-1][1]+snake_speed) % WINDOW_SIZE[1])

    snake_body.append(new_head)
    if len(snake_body) > score+snake_size:
        snake_body.pop(0)

    # Create Rect objects for the snake head and the food
    snake_head_rect = pygame.Rect(snake_body[-1][0], snake_body[-1][1], snake_size, snake_size)
    food_rect = pygame.Rect(food[0], food[1], snake_size, snake_size)
    # Check for collision with food
    if snake_head_rect.colliderect(food_rect):
        food = (random.randint(0, WINDOW_SIZE[0]-10), random.randint(0, WINDOW_SIZE[1]-10))
        score += 1
        #snake_size += 10  # Increase the length of the snake
        food_eaten = True  # Set the flag
    else:
        food_eaten = False  # Reset the flag

    # Only remove the first element of snake_body when food is not eaten
    if not food_eaten:
        snake_body.pop(0)
            

    # Check for collision with walls or snake body
    # if new_head[0] < 0 or new_head[0] > WINDOW_SIZE[0] - snake_size or new_head[1] < 0 or new_head[1] > WINDOW_SIZE[1] - snake_size:
    #     print("Collision detected. Game over.")
    #     game_over = True

    # Draw the game objects
    screen.fill(WHITE)
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_size, snake_size])
    pygame.draw.rect(screen, RED, [food[0], food[1], snake_size, snake_size])

    # Display the score
    score_text = font.render("Score: {}".format(score), True, BLUE)
    screen.blit(score_text, [10, 10])

    # Update the display
    pygame.display.flip()
    clock.tick(10)  # Add this line
# Quit Pygame
print("Quitting Pygame.")
pygame.quit()