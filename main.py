import pygame
import random

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
# Button position (top-left corner)
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
explosion_radius = 140  # Explosion radius
explosion_duration = 500  # Explosion lasts for 0.5 seconds
tnts = []  # List to store TNTs with their states

# Score properties
score = 0  # Initialize score

# Timer properties
countdown = 20  # Initial countdown time (seconds)
TIMER_EVENT = pygame.USEREVENT + 1  # Define custom timer event
pygame.time.set_timer(TIMER_EVENT, 1000)  # Trigger every 1 second

# Load character image (Ensure the image is in the same folder as the script)
char_image = pygame.image.load('character_idle.png')  # Replace with your sprite
char_image = pygame.transform.scale(char_image, (character_width, character_height))  # Resize to fit the character's dimensions

# Load TNT image (Ensure 'tnt.webp' is in the same folder as the script)
tnt_image = pygame.image.load('tnt.webp')  # Replace with your TNT .webp image
tnt_image = pygame.transform.scale(tnt_image, (tnt_width, tnt_height))  # Resize TNT image

# Wait function to delay before showing Game Over screen
def wait(milliseconds):
    start_time = pygame.time.get_ticks()  # Get current time in milliseconds
    while pygame.time.get_ticks() - start_time < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

# Game Over screen function
def game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Display score on Game Over screen
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLUE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    # Show the screen
    screen.fill(WHITE)
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    # Wait for a few seconds before closing
    wait(3000)
    pygame.quit()
    quit()

# Game loop
running = True
game_over_screen = False

while running:
    current_time = pygame.time.get_ticks()  # Get current time in milliseconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == TIMER_EVENT:  # Handle countdown timer event
            countdown -= 1
            if countdown <= 0:
                game_over()  # Trigger Game Over when time runs out
                
        # Detect mouse click on button
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over_screen:
            mouse_x, mouse_y = event.pos

            # Check if the click is within the button area
            if (button_x <= mouse_x <= button_x + button_width) and (button_y <= mouse_y <= button_y + button_height):
                # Add two new TNTs with their creation time and detonating status
                for _ in range(2):  # Add two TNTs
                    new_tnt = {
                        "x": random.randint(tnt_width, WIDTH - tnt_width),
                        "y": random.randint(tnt_height, HEIGHT - tnt_height),
                        "time_created": current_time,
                        "detonating": False,  # Indicates if the TNT is in the explosion phase
                        "time_detonated": None  # Time when detonation starts
                    }
                    tnts.append(new_tnt)
                score += 2  # Increase score by 2 when button is pressed

        # Detect spacebar key press
        if event.type == pygame.KEYDOWN and not game_over_screen:
            if event.key == pygame.K_SPACE:
                # Simulate button press when spacebar is pressed
                for _ in range(2):  # Add two TNTs
                    new_tnt = {
                        "x": random.randint(tnt_width, WIDTH - tnt_width),
                        "y": random.randint(tnt_height, HEIGHT - tnt_height),
                        "time_created": current_time,
                        "detonating": False,
                        "time_detonated": None
                    }
                    tnts.append(new_tnt)
                score += 2  # Increase score by 2 when spacebar is pressed

    if game_over_screen:
        continue  # Skip the rest of the game loop to display Game Over

    # Update TNTs
    for tnt in tnts:
        # Check if the TNT should start detonating (after 3 seconds)
        if not tnt["detonating"] and current_time - tnt["time_created"] >= 3000:  # 3 seconds after creation
            tnt["detonating"] = True
            tnt["time_detonated"] = current_time

    # Remove TNTs after their explosion ends (explosion duration is 0.5 seconds)
    tnts = [
        tnt for tnt in tnts
        if not tnt["detonating"] or (current_time - tnt["time_detonated"] <= explosion_duration)
    ]

    # Key handling for character movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and character_x > 0:
        character_x -= char_speed
    if keys[pygame.K_RIGHT] and character_x < WIDTH - character_width:
        character_x += char_speed
    if keys[pygame.K_UP] and character_y > 0:
        character_y -= char_speed
    if keys[pygame.K_DOWN] and character_y < HEIGHT - character_height:
        character_y += char_speed

    # Check for explosion collisions (only after detonation)
    for tnt in tnts:
        if tnt["detonating"]:
            # Calculate distance from TNT center to character
            distance = ((character_x - tnt["x"])**2 + (character_y - tnt["y"])**2)**0.5
            if distance <= explosion_radius:
                game_over_screen = True
                game_over()  # Call the game over function

    # background colour
    screen.fill(WHITE)

    # Draw the button (green rectangle)
    pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))

    # Draw the text on the button (centered text)
    font = pygame.font.Font(None, 36)
    text = font.render("Click Me!", True, WHITE)
    text_x = button_x + (button_width - text.get_width()) // 2
    text_y = button_y + (button_height - text.get_height()) // 2
    screen.blit(text, (text_x, text_y))

    # Draw the TNTs
    for tnt in tnts:
        if tnt["detonating"]:
            # Draw the explosion (red circle or animation could be used here)
            pygame.draw.circle(screen, RED, (tnt["x"], tnt["y"]), explosion_radius)
        else:
            # Draw the TNT (using the TNT image)
            screen.blit(tnt_image, (tnt["x"] - tnt_width // 2, tnt["y"] - tnt_height // 2))

    # Draw the character image
    screen.blit(char_image, (character_x, character_y))

    # Draw the score on the screen (continuously)
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}", True, BLUE)
    score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))  # Position at the top-right corner
    screen.blit(score_text, score_rect)

    # Draw the countdown on the screen (continuously)
    countdown_text = pygame.font.Font(None, 36).render(f"Time Left: {countdown}", True, BLUE)
    countdown_rect = countdown_text.get_rect(topleft=(10, 10))  # Position at the top-left corner
    screen.blit(countdown_text, countdown_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
