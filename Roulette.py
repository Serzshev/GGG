import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎲 Roulette Spin Game")

# Colors
GREEN = (50, 120, 50)
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48)

# Game variables
coins = 100
bet_amount = 10
selected_color = None
spinning = False
angle = 0
target_angle = 0
spin_speed = 0
result_color = None
result_number = None
message = ""
history = []
game_state = "MENU"  # MENU, PLAYING, GAME_OVER

# Roulette layout
roulette_slots = [(0, "green")] + [(i, "red" if i % 2 == 1 else "black") for i in range(1, 37)]

# Wheel setup
WHEEL_CENTER = (WIDTH//2, HEIGHT//2 - 50)
WHEEL_RADIUS = 200
BALL_RADIUS = 8
ball_pos = [WHEEL_CENTER[0], WHEEL_CENTER[1]-WHEEL_RADIUS+10]

# Clock for controlling frame rate
clock = pygame.time.Clock()

def draw_wheel():
    """Draw the roulette wheel with numbers and colors"""
    # Wheel base
    pygame.draw.circle(screen, GRAY, WHEEL_CENTER, WHEEL_RADIUS)
    pygame.draw.circle(screen, (80, 80, 80), WHEEL_CENTER, WHEEL_RADIUS-20)
    
    # Draw colored segments
    slot_angle = 360 / len(roulette_slots)
    for i, (num, color) in enumerate(roulette_slots):
        start_angle = math.radians(i * slot_angle + angle)
        end_angle = math.radians((i+1) * slot_angle + angle)
        
        # Color selection
        segment_color = DARK_GREEN if color == "green" else DARK_RED if color == "red" else BLACK
        
        # Draw segment
        pygame.draw.arc(
            screen,
            segment_color,
            (WHEEL_CENTER[0]-WHEEL_RADIUS, WHEEL_CENTER[1]-WHEEL_RADIUS, 
             WHEEL_RADIUS*2, WHEEL_RADIUS*2),
            start_angle, end_angle,
            40
        )
        
        # Draw number
        text_angle = math.radians(i * slot_angle + angle + slot_angle/2)
        text = font.render(str(num), True, WHITE)
        text_pos = (
            WHEEL_CENTER[0] + (WHEEL_RADIUS-30) * math.cos(text_angle),
            WHEEL_CENTER[1] + (WHEEL_RADIUS-30) * math.sin(text_angle)
        )
        text_rect = text.get_rect(center=text_pos)
        screen.blit(text, text_rect)
    
    # Draw ball
    if spinning:
        ball_angle = math.radians(angle + 90)  # Start at top
        ball_pos[0] = WHEEL_CENTER[0] + (WHEEL_RADIUS-15) * math.cos(ball_angle)
        ball_pos[1] = WHEEL_CENTER[1] + (WHEEL_RADIUS-15) * math.sin(ball_angle)
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

def draw_ui():
    """Draw user interface elements"""
    # Coins and bet info
    screen.blit(font.render(f"Coins: {coins}", True, WHITE), (20, 20))
    screen.blit(font.render(f"Bet: {bet_amount}", True, WHITE), (20, 50))
    
    # Message display
    if message:
        screen.blit(font.render(message, True, YELLOW), (20, 90))
    
    # Result display
    if result_number is not None:
        res_txt = f"Landed on {result_number} ({result_color})"
        text_color = RED if result_color == "red" else WHITE if result_color == "black" else DARK_GREEN
        screen.blit(big_font.render(res_txt, True, text_color), (WIDTH//2 - 200, HEIGHT - 100))
    
    # Color selection buttons
    pygame.draw.rect(screen, RED if selected_color == "red" else DARK_RED, (100, 500, 80, 40))
    pygame.draw.rect(screen, BLACK if selected_color == "black" else (50, 50, 50), (200, 500, 80, 40))
    pygame.draw.rect(screen, DARK_GREEN if selected_color == "green" else (0, 80, 0), (300, 500, 80, 40))
    pygame.draw.rect(screen, (0, 100, 255), (400, 500, 80, 40))  # Spin button
    
    # Button labels
    screen.blit(font.render("Red", True, WHITE), (110, 510))
    screen.blit(font.render("Black", True, WHITE), (205, 510))
    screen.blit(font.render("Green", True, WHITE), (305, 510))
    screen.blit(font.render("Spin", True, WHITE), (410, 510))
    
    # Bet amount controls
    pygame.draw.rect(screen, (100, 100, 100), (500, 500, 30, 40))
    pygame.draw.rect(screen, (100, 100, 100), (540, 500, 30, 40))
    screen.blit(font.render("-", True, WHITE), (510, 510))
    screen.blit(font.render("+", True, WHITE), (550, 510))
    
    # History display
    screen.blit(font.render("History:", True, WHITE), (20, 150))
    for i, (num, color) in enumerate(history[:5]):
        text_color = RED if color == "red" else WHITE if color == "black" else DARK_GREEN
        screen.blit(font.render(f"{num} ({color})", True, text_color), (20, 180 + i*30))

def draw_menu():
    """Draw the main menu screen"""
    screen.fill(GREEN)
    
    # Title
    title = title_font.render("ROULETTE SPIN", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    
    # Start button
    start_btn = pygame.Rect(WIDTH//2-100, HEIGHT//2, 200, 50)
    pygame.draw.rect(screen, DARK_GREEN, start_btn)
    screen.blit(font.render("START GAME", True, WHITE), 
               (WIDTH//2 - 60, HEIGHT//2 + 15))
    
    return start_btn

def draw_game_over():
    """Draw the game over screen"""
    screen.fill(GREEN)
    
    # Game over text
    game_over = title_font.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//3))
    
    # Restart prompt
    restart = big_font.render("Click to play again", True, WHITE)
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2))
    
    # Final coins
    coins_text = font.render(f"Final coins: {coins}", True, YELLOW)
    screen.blit(coins_text, (WIDTH//2 - coins_text.get_width()//2, HEIGHT//2 + 50))

def start_spin():
    """Start the wheel spinning"""
    global target_angle, spinning, spin_speed, result_number, result_color, message
    
    if not selected_color:
        message = "Please select a color!"
        return
    
    if coins < bet_amount:
        message = "Not enough coins!"
        return
    
    # Select random result
    result_number, result_color = random.choice(roulette_slots)
    result_index = roulette_slots.index((result_number, result_color))
    slot_angle = 360 / len(roulette_slots)
    stop_angle = result_index * slot_angle
    
    # Calculate spin parameters
    spins = random.randint(3, 5)  # full spins before stopping
    target_angle = (spins * 360) + stop_angle
    spinning = True
    spin_speed = 15
    message = ""

def update_spin():
    """Update the wheel spinning animation"""
    global angle, spin_speed, spinning, coins, message, history
    
    if spinning:
        angle += spin_speed
        spin_speed *= 0.97  # slow down
        
        # When wheel stops
        if spin_speed < 0.5 and spinning:
            spinning = False
            angle %= 360
            
            # Record result
            history.insert(0, (result_number, result_color))
            if len(history) > 5:
                history.pop()
            
            # Check win
            win = 0
            if selected_color == result_color:
                if result_color == "green":
                    win = bet_amount * 14
                else:
                    win = bet_amount * 2
            
            # Update coins and message
            if win > 0:
                coins += win
                message = f"You won {win} coins!"
            else:
                coins -= bet_amount
                message = "You lost!"
            
            # Check game over
            if coins <= 0:
                global game_state
                game_state = "GAME_OVER"

# Main game loop
running = True
while running:
    # Fill background
    screen.fill(GREEN)
    
    # Handle different game states
    if game_state == "MENU":
        start_btn = draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    game_state = "PLAYING"
                    coins = 100  # Reset coins
                    history = []
    
    elif game_state == "PLAYING":
        # Draw game elements
        draw_wheel()
        draw_ui()
        update_spin()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                x, y = event.pos
                
                # Color selection buttons
                if 100 <= x <= 180 and 500 <= y <= 540:
                    selected_color = "red"
                elif 200 <= x <= 280 and 500 <= y <= 540:
                    selected_color = "black"
                elif 300 <= x <= 380 and 500 <= y <= 540:
                    selected_color = "green"
                elif 400 <= x <= 480 and 500 <= y <= 540:  # Spin button
                    start_spin()
                
                # Bet amount controls
                elif 500 <= x <= 530 and 500 <= y <= 540 and bet_amount > 10:
                    bet_amount -= 10
                elif 540 <= x <= 570 and 500 <= y <= 540 and bet_amount < coins:
                    bet_amount += 10
    
    elif game_state == "GAME_OVER":
        draw_game_over()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "MENU"
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

# Clean up
pygame.quit()
sys.exit()
