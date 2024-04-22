import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import(
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
            center=(
                random.randint(0, SCREEN_WIDTH), 0),
            )
        self.mask = pygame.mask.from_surface(self.surf, threshold=128)
        self.speed = random.randint(5, 6)
        self.show_rect = True
        self.collideRect =  pygame.rect.Rect((0, 0), (120, 95))
        
    
    def update(self):
        self.rect.y += self.speed
        self.collideRect.center = self.rect.center

        

    def handle_collision(self, mouse_pos):
        return self.mask.overlap(bullet_mask, (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y))
            
    def lava_collision(self):
        pass

    #def draw(self, screen):
        #screen.blit(self.surf, self.rect)
        #if self.show_rect:
            #pygame.draw.rect(screen, (255, 0, 0), self.collideRect, 1)
        
    



    

# Initialize pygame
pygame.init()


# Colors
red = (255, 0, 0) # Lava Color
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


score = 0
font = pygame.font.Font(None, 28)  # Font for score display


# Create a invisible surface that can overlap onto money mask for pixel perfect collision
bullet = pygame.Surface((10, 10))
bullet_mask = pygame.mask.from_surface(bullet)





# Create a custom event for adding a money bill
ADDBILL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBILL, 400)



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
        
    for money in bills:
        
        #money.draw(screen)
        if money.collideRect.colliderect(lava_rect):
            # Money touched lava!
            score = 0
    
    

            
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  # White color
    screen.blit(score_text, (10, 10))
    



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
       