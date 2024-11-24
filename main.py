import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1350, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SelfDetonation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (255, 87, 51)
RED = (255, 0, 0)

# Button sizes
button_width = 150
button_height = 50
button_x = 10
button_y = 640

# Character properties
character_width = 50
character_height = 50
character_x = WIDTH // 2 - character_width // 2
character_y = HEIGHT // 2 - character_height // 2
char_speed = 1

# TNT properties
tnt_width = 50
tnt_height = 50
explosion_radius = 140
explosion_duration = 500
tnts = []

# Score properties
score = 0

# High score handling
highscore_file = "highscore.txt"

# Load the high score from the file (create the file if it doesn't exist)
if not os.path.exists(highscore_file):
    with open(highscore_file, "w") as f:
        f.write("0")

with open(highscore_file, "r") as f:
    high_score = int(f.read())

# Timer properties
countdown = 20
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 1000)

# Load character image
char_image = pygame.image.load('character_idle.png')
char_image = pygame.transform.scale(char_image, (character_width, character_height))

# Load TNT image
tnt_image = pygame.image.load('tnt.webp')
tnt_image = pygame.transform.scale(tnt_image, (tnt_width, tnt_height))

# Wait function
def wait(milliseconds):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Game Over screen
def game_over():
    global high_score, running, score, countdown, character_x, character_y, tnts, game_over_screen

    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    # Update and save the high score
    if score > high_score:
        high_score = score
        with open(highscore_file, "w") as f:
            f.write(str(high_score))

    # Display the high score and current score
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLUE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, BLUE)
    high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Retry button
    retry_button_width = 200
    retry_button_height = 50
    retry_button_x = WIDTH // 2 - retry_button_width // 2
    retry_button_y = HEIGHT // 2 + 100
    retry_button_rect = pygame.Rect(retry_button_x, retry_button_y, retry_button_width, retry_button_height)

    while True:
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        screen.blit(score_text, score_rect)
        screen.blit(high_score_text, high_score_rect)

        # Draw Retry button
        pygame.draw.rect(screen, GREEN, retry_button_rect)
        retry_text = pygame.font.Font(None, 36).render("Retry", True, WHITE)
        retry_text_rect = retry_text.get_rect(center=retry_button_rect.center)
        screen.blit(retry_text, retry_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button_rect.collidepoint(event.pos):
                    # Reset game state
                    score = 0
                    countdown = 20
                    character_x = WIDTH // 2 - character_width // 2
                    character_y = HEIGHT // 2 - character_height // 2
                    tnts = []
                    game_over_screen = False
                    return  # Exit game over and retry

# Main game loop
running = True
game_over_screen = False

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == TIMER_EVENT:
            countdown -= 1
            if countdown <= 0:
                game_over()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over_screen:
            mouse_x, mouse_y = event.pos
            if (button_x <= mouse_x <= button_x + button_width) and (button_y <= mouse_y <= button_y + button_height):
                for _ in range(2):
                    new_tnt = {
                        "x": random.randint(tnt_width, WIDTH - tnt_width),
                        "y": random.randint(tnt_height, HEIGHT - tnt_height),
                        "time_created": current_time,
                        "detonating": False,
                        "time_detonated": None
                    }
                    tnts.append(new_tnt)
                score += 2

        if event.type == pygame.KEYDOWN and not game_over_screen:
            if event.key == pygame.K_SPACE:
                for _ in range(2):
                    new_tnt = {
                        "x": random.randint(tnt_width, WIDTH - tnt_width),
                        "y": random.randint(tnt_height, HEIGHT - tnt_height),
                        "time_created": current_time,
                        "detonating": False,
                        "time_detonated": None
                    }
                    tnts.append(new_tnt)
                score += 2

    if game_over_screen:
        continue

    for tnt in tnts:
        if not tnt["detonating"] and current_time - tnt["time_created"] >= 3000:
            tnt["detonating"] = True
            tnt["time_detonated"] = current_time

    tnts = [
        tnt for tnt in tnts
        if not tnt["detonating"] or (current_time - tnt["time_detonated"] <= explosion_duration)
    ]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and character_x > 0:
        character_x -= char_speed
    if keys[pygame.K_RIGHT] and character_x < WIDTH - character_width:
        character_x += char_speed
    if keys[pygame.K_UP] and character_y > 0:
        character_y -= char_speed
    if keys[pygame.K_DOWN] and character_y < HEIGHT - character_height:
        character_y += char_speed

    for tnt in tnts:
        if tnt["detonating"]:
            distance = ((character_x - tnt["x"])**2 + (character_y - tnt["y"])**2)**0.5
            if distance <= explosion_radius:
                game_over_screen = True
                game_over()

    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Click Me!", True, WHITE)
    text_x = button_x + (button_width - text.get_width()) // 2
    text_y = button_y + (button_height - text.get_height()) // 2
    screen.blit(text, (text_x, text_y))

    for tnt in tnts:
        if tnt["detonating"]:
            pygame.draw.circle(screen, RED, (tnt["x"], tnt["y"]), explosion_radius)
        else:
            screen.blit(tnt_image, (tnt["x"] - tnt_width // 2, tnt["y"] - tnt_height // 2))

    screen.blit(char_image, (character_x, character_y))

    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLUE)
    score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

    high_score_text = pygame.font.Font(None, 36).render(f"High Score: {high_score}", True, BLUE)
    high_score_rect = high_score_text.get_rect(topright=(WIDTH - 10, 50))
    screen.blit(high_score_text, high_score_rect)

    countdown_text = pygame.font.Font(None, 36).render(f"Time Left: {countdown}", True, BLUE)
    countdown_rect = countdown_text.get_rect(topleft=(10, 10))
    screen.blit(countdown_text, countdown_rect)

    pygame.display.flip()

pygame.quit()
