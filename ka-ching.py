# Some sort of background - change color after certain score / changes after x score
# Sound effects
# Change money spawn so its always within screen borders **
# Maybe an animation for burning money
# 

import pygame
import random
from sql import (
    create_connection,
    check_and_create_database,
    create_table,
    insert_initial_score,
    save_high_score,
    load_high_score,
)

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Money(pygame.sprite.Sprite):
    def __init__(self):
        super(Money, self).__init__()
        self.surf = pygame.image.load("dollar.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (200, 200))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, SCREEN_WIDTH), 0),
        )
        self.mask = pygame.mask.from_surface(self.surf, threshold=128)
        self.speed = random.randint(10, 10)
        self.show_rect = True
        self.collideRect = pygame.rect.Rect((0, 0), (120, 60))

    def update(self):
        self.rect.y += update_fall_speed()
        self.collideRect.center = self.rect.center

    def handle_collision(self, mouse_pos):
        return self.mask.overlap(
            bullet_mask, (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
        )

    def lava_collision(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        if self.show_rect:
            pygame.draw.rect(screen, (255, 0, 0), self.collideRect, 1)


def update_fall_speed():
    global score, speed_levels

    # Find the highest threshold below the current score
    current_level = max(level for level, _ in speed_levels.items() if level <= score)

    return speed_levels[current_level]


speed_levels = {
    0: 5,  # Initial speed
    50: 7,  # Speed increase at score 50
    100: 8,  # Speed increase at score 100
    200: 10,  # Speed increase at score 200
}

db_file = "high_scores.db"
check_and_create_database(db_file)

conn = create_connection("high_scores.db")  # Connect to database
high_score = load_high_score()  # Call load_high_score function
conn.close()  # Close the connection after retrieving score


# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Initialize pygame
pygame.init()


# Colors
red = (255, 0, 0)  # Lava Color
green = (0, 255, 0)

# Define Screen Size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create a clock object to control the speed
clock = pygame.time.Clock()

# Create the screen object
# Set window title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ka-Ching!")


# Load high score before starting the game loop
font = pygame.font.Font(None, 28)  # Font for score display


score = 0
font = pygame.font.Font(None, 28)  # Font for score display


# Create a invisible surface that can overlap onto money mask for pixel perfect collision
bullet = pygame.Surface((10, 10))
bullet_mask = pygame.mask.from_surface(bullet)


# Create a custom event for adding a money bill
ADDBILL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBILL, 375)


# Define lava rectangle
money_image = pygame.image.load("dollar.png").convert_alpha()
money_image = pygame.transform.scale(money_image, (200, 200))
money_rect = money_image.get_rect()

lava_width = SCREEN_WIDTH
lava_height = SCREEN_HEIGHT // 4

lava_image = pygame.image.load("lava.png").convert_alpha()
lava_mask = pygame.mask.from_surface(lava_image)
lava_image = pygame.transform.scale(lava_image, (lava_width, lava_height))
lava_rect = lava_image.get_rect(bottom=SCREEN_HEIGHT)

lava_rect.width = lava_image.get_width()
lava_rect.height = lava_image.get_height()
lava_rect.x = 0
lava_rect.y = SCREEN_HEIGHT * 4 // 5

# Create groups to hold sprites
bills = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Variable to keep the main loop running
running = True


# Main loop
while running:
    # Fill screen with white background
    screen.fill((255, 255, 255))

    pos = pygame.mouse.get_pos()

    # Look at every event in the queue (Handle Events)
    for event in pygame.event.get():
        # Check for QUIT event to close the game window
        if event.type == QUIT:
            running = False

        # Add a new bill?
        elif event.type == ADDBILL:
            # Create the new bill and add it to the sprite group
            new_bill = Money()
            bills.add(new_bill)
            all_sprites.add(new_bill)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse position
            mouse_pos = pygame.mouse.get_pos()

            # Check for collision with money objects
            for money in bills:
                if money.handle_collision(pos):
                    # Money clicked!
                    # Remove the money object from the group (or play a sound, etc.)
                    score += 1
                    bills.remove(money)

                    # Assigns high score
                    if score > high_score:
                        high_score = score
        if event.type == QUIT:
            if high_score > load_high_score():  # Check for a new high score
                save_high_score(high_score)

    for money in bills:
        # money.draw(screen)
        if money.collideRect.colliderect(lava_rect):
            # Money touched lava!
            score = 0
            bills.remove(money)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # White color
    high_score_text = font.render(
        f"High Score: {high_score}", True, (0, 0, 0)
    )  # White color
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (640, 10))

    # Draw bills
    for bill in bills:
        screen.blit(bill.surf, bill.rect)

    # Draw lava rectangle
    screen.blit(lava_image, lava_rect)

    # Update bills position
    bills.update()

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
