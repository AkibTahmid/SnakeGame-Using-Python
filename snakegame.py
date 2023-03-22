import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Set up fonts
font = pygame.font.SysFont(None, 25)

# Set up the clock
clock = pygame.time.Clock()

# Set up the snake and food
snake_block_size = 10
snake_speed = 15
food_block_size = 10
score_booster_block_size = 10
score_booster_color = blue
# Percentage chance of score booster appearing (out of 100)
score_booster_chance = 20
score_booster_duration = 4000  # Duration of score booster in milliseconds


def draw_snake(snake_block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(
            screen, white, [x[0], x[1], snake_block_size, snake_block_size])


def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [screen_width/6, screen_height/3])


def show_score(score):
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, [0, 0])


def gameLoop():
    game_over = False
    game_close = False

    x1 = screen_width/2
    y1 = screen_height/2

    x1_change = 0
    y1_change = 0

    snake_list = []
    Length_of_snake = 1

    foodx = round(random.randrange(
        0, screen_width - food_block_size)/10.0)*10.0
    foody = round(random.randrange(
        0, screen_height - food_block_size)/10.0)*10.0

    score = 0
    score_booster_active = False
    score_booster_start_time = None

    while not game_over:
        while game_close == True:
            screen.fill(black)
            message("You lost! Press Q-Quit or C-Play Again", white)
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block_size
                    x1_change = 0

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(black)

        # Draw the food block
        pygame.draw.rect(
            screen, red, [foodx, foody, food_block_size, food_block_size])

        # Draw the score booster if active
        if score_booster_active:
            pygame.draw.circle(screen, score_booster_color, [int(
                score_booster_x), int(score_booster_y)], score_booster_block_size)

            # Check if the score booster duration has expired
            if pygame.time.get_ticks() - score_booster_start_time > score_booster_duration:
                score_booster_active = False

        # Generate a new score booster if needed
        if (score % 5) == 0 and score > 0 and not score_booster_active and random.randint(1, 100) <= score_booster_chance:
            score_booster_x = round(random.randrange(
                0, screen_width - score_booster_block_size)/10.0)*10.0
            score_booster_y = round(random.randrange(
                0, screen_height - score_booster_block_size)/10.0)*10.0
            score_booster_active = True
            score_booster_start_time = pygame.time.get_ticks()

        # Check for collision with the score booster
        if score_booster_active and x1 == score_booster_x and y1 == score_booster_y:
            score += 25
            score_booster_active = False

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_list.append(snake_Head)

        if len(snake_list) > Length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block_size, snake_list)
        show_score(score)

        pygame.display.update()

        # Generate a new food block if needed and update score
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, screen_width - food_block_size)/10.0)*10.0
            foody = round(random.randrange(
                0, screen_height - food_block_size)/10.0)*10.0
            Length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
