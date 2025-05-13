import pygame
import random
import os

# Initialize pygame and sound
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("snake.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Window size
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
bgimg = pygame.image.load("snake.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game title
pygame.display.set_caption("Stranger's ----> Snake Game")

# Clock object to control FPS
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Function to display text on the screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to draw the snake
def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Read High Score from file, or create one if missing
if not os.path.exists("HighScore.txt"):
    with open("HighScore.txt", "w") as f:
        f.write("0")

with open("HighScore.txt", "r") as f:
    high_score = int(f.read().strip())

# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(black)
        gameWindow.blit(bgimg, (0, 0))
        text_screen("WELCOME STRANGER!!!", blue, 200, 300)
        text_screen("Press ENTER to Play", green, 240, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()

        pygame.display.update()
        clock.tick(30)

# Main Game Loop
def gameloop():
    global high_score  # Make sure high_score is recognized

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snake_size = 10
    food_size = 10
    fps = 30
    food_x = random.randint(20, int(screen_width / 2))
    food_y = random.randint(20, int(screen_height / 2))
    init_velocity = 5
    score = 0

    snake_list = []
    snake_length = 1

    while not exit_game:
        if game_over:
            gameWindow.fill(black)
            text_screen(f"GAME OVER! Score: {score}. High Score: {high_score}", red, 100, 250)
            text_screen("Press ENTER to Restart", red, 100, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()  # Restart from welcome screen

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Cheat codes
                    if event.key == pygame.K_x:  # Increase score instantly
                        score += 5
                    if event.key == pygame.K_0:  # Reset score
                        score = 0
                    if event.key == pygame.K_ESCAPE:  # Reset High Score
                        high_score = 0
                        with open("HighScore.txt", "w") as f:
                            f.write(str(high_score))

            # Update snake position
            snake_x += velocity_x
            snake_y += velocity_y

            # Food collision check
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 10
                food_x = random.randint(20, int(screen_width / 2))
                food_y = random.randint(20, int(screen_height / 2))
                snake_length += 4  # Increase snake length

                # Update High Score & Save to File
                if score > high_score:
                    high_score = score
                    with open("HighScore.txt", "w") as f:
                        f.write(str(high_score))

            # Draw everything
            gameWindow.fill(black)
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score}  High Score: {high_score}", green, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            head = [snake_x, snake_y]
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            # If snake touches its own body, game over
            if head in snake_list[:-1]:
                game_over = True

            # If snake touches borders, game over
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, white, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()