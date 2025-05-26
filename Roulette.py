import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎲 Roulette Spin Game")

# Colors
BACKGROUND = (53, 101, 77)  # Dark green
WHEEL_BASE = (100, 100, 100)
WHEEL_RIM = (70, 70, 70)
RED = (214, 40, 40)
DARK_RED = (150, 30, 30)
BLACK = (30, 30, 30)
GREEN = (35, 140, 70)
DARK_GREEN = (20, 90, 50)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GOLD = (255, 200, 0)
BUTTON_BLUE = (0, 120, 215)

# Fonts
font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 32)
font_title = pygame.font.SysFont("Arial", 48, bold=True)

# Game variables
coins = 100
bet_amount = 10
selected_color = None
spinning = False
angle = 0
spin_speed = 0
result_color = None
result_number = None
message = ""
history = []
game_state = "MENU"  # MENU, PLAYING, GAME_OVER

# Roulette layout
roulette_slots = [(0, "green")] + [(i, "red" if (1 <= i <= 10 or 19 <= i <= 28) and i % 2 == 1 or 
                                   (11 <= i <= 18 or 29 <= i <= 36) and i % 2 == 0 else "black") 
                                   for i in range(1, 37)]

# Wheel setup
WHEEL_CENTER = (WIDTH//2, HEIGHT//2 - 30)
WHEEL_RADIUS = 220
BALL_RADIUS = 10
ball_pos = [WHEEL_CENTER[0], WHEEL_CENTER[1]-WHEEL_RADIUS+15]

def draw_wheel():
    """Draw the roulette wheel with numbers and colors"""
    # Wheel base
    pygame.draw.circle(screen, WHEEL_BASE, WHEEL_CENTER, WHEEL_RADIUS)
    pygame.draw.circle(screen, WHEEL_RIM, WHEEL_CENTER, WHEEL_RADIUS-20)
    pygame.draw.circle(screen, (50, 50, 50), WHEEL_CENTER, WHEEL_RADIUS-40)
    
    # Draw colored segments
    slot_angle = 360 / len(roulette_slots)
    for i, (num, color) in enumerate(roulette_slots):
        start_angle = math.radians(i * slot_angle + angle)
        end_angle = math.radians((i+1) * slot_angle + angle)
        
        # Color selection
        segment_color = GREEN if color == "green" else RED if color == "red" else BLACK
        
        # Draw segment
        pygame.draw.arc(
            screen,
            segment_color,
            (WHEEL_CENTER[0]-WHEEL_RADIUS, WHEEL_CENTER[1]-WHEEL_RADIUS, 
             WHEEL_RADIUS*2, WHEEL_RADIUS*2),
            start_angle, end_angle,
            40
        )
        
        # Draw number (fixed orientation)
        text_angle = math.radians(i * slot_angle + slot_angle/2 - angle)
        text = font_medium.render(str(num), True, WHITE)
        text_rotated = pygame.transform.rotate(text, math.degrees(-text_angle))
        text_pos = (
            WHEEL_CENTER[0] + (WHEEL_RADIUS-60) * math.cos(text_angle),
            WHEEL_CENTER[1] + (WHEEL_RADIUS-60) * math.sin(text_angle)
        )
        text_rect = text_rotated.get_rect(center=text_pos)
        screen.blit(text_rotated, text_rect)
    
    # Draw ball
    if spinning:
        ball_angle = math.radians(-angle + 90)  # Adjusted for counter-clockwise
        ball_pos[0] = WHEEL_CENTER[0] + (WHEEL_RADIUS-25) * math.cos(ball_angle)
        ball_pos[1] = WHEEL_CENTER[1] + (WHEEL_RADIUS-25) * math.sin(ball_angle)
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    pygame.draw.circle(screen, (200, 200, 200), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS-3)

def draw_ui():
    """Draw user interface elements"""
    # Coins and bet info
    coins_text = font_large.render(f"Coins: {coins}", True, GOLD)
    screen.blit(coins_text, (20, 20))
    
    bet_text = font_medium.render(f"Bet: {bet_amount}", True, WHITE)
    screen.blit(bet_text, (20, 60))
    
    # Message display
    if message:
        msg_color = GOLD if "won" in message else RED
        msg_text = font_medium.render(message, True, msg_color)
        screen.blit(msg_text, (20, 100))
    
    # Result display
    if result_number is not None:
        res_txt = f"Landed on: {result_number} ({result_color})"
        text_color = RED if result_color == "red" else WHITE if result_color == "black" else GREEN
        result_text = font_large.render(res_txt, True, text_color)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT - 120))
    
    # Color selection buttons
    pygame.draw.rect(screen, RED if selected_color == "red" else DARK_RED, (100, HEIGHT-80, 100, 50), border_radius=5)
    pygame.draw.rect(screen, BLACK if selected_color == "black" else (50, 50, 50), (220, HEIGHT-80, 100, 50), border_radius=5)
    pygame.draw.rect(screen, GREEN if selected_color == "green" else DARK_GREEN, (340, HEIGHT-80, 100, 50), border_radius=5)
    pygame.draw.rect(screen, BUTTON_BLUE, (460, HEIGHT-80, 100, 50), border_radius=5)  # Spin button
    
    # Button labels
    screen.blit(font_medium.render("RED", True, WHITE), (130, HEIGHT-70))
    screen.blit(font_medium.render("BLACK", True, WHITE), (230, HEIGHT-70))
    screen.blit(font_medium.render("GREEN", True, WHITE), (350, HEIGHT-70))
    screen.blit(font_medium.render("SPIN", True, WHITE), (480, HEIGHT-70))
    
    # Bet amount controls
    pygame.draw.rect(screen, (80, 80, 80), (580, HEIGHT-80, 40, 50), border_radius=5)
    pygame.draw.rect(screen, (80, 80, 80), (630, HEIGHT-80, 40, 50), border_radius=5)
    screen.blit(font_large.render("-", True, WHITE), (590, HEIGHT-80))
    screen.blit(font_large.render("+", True, WHITE), (640, HEIGHT-80))
    
    # History display
    history_title = font_medium.render("History:", True, WHITE)
    screen.blit(history_title, (20, 150))
    
    for i, (num, color) in enumerate(history[:5]):
        text_color = RED if color == "red" else WHITE if color == "black" else GREEN
        hist_text = font_small.render(f"{num} ({color})", True, text_color)
        screen.blit(hist_text, (20, 180 + i*25))

def draw_menu():
    """Draw the main menu screen"""
    screen.fill(BACKGROUND)
    
    # Title with shadow
    title = font_title.render("ROULETTE SPIN", True, (30, 30, 30))
    screen.blit(title, (WIDTH//2 - title.get_width()//2 + 3, HEIGHT//3 + 3))
    title = font_title.render("ROULETTE SPIN", True, GOLD)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    
    # Start button
    start_btn = pygame.Rect(WIDTH//2-100, HEIGHT//2, 200, 60)
    pygame.draw.rect(screen, GREEN, start_btn, border_radius=10)
    pygame.draw.rect(screen, DARK_GREEN, start_btn, 3, border_radius=10)
    screen.blit(font_large.render("START GAME", True, WHITE), 
               (WIDTH//2 - 70, HEIGHT//2 + 15))
    
    return start_btn

def draw_game_over():
    """Draw the game over screen"""
    screen.fill(BACKGROUND)
    
    # Game over text
    game_over = font_title.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//3))
    
    # Restart prompt
    restart = font_large.render("Click to play again", True, WHITE)
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2))
    
    # Final coins
    coins_text = font_medium.render(f"Final coins: {coins}", True, GOLD)
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
    spins = random.randint(3, 5)
    target_angle = (spins * 360) + (360 - stop_angle)  # Counter-clockwise adjustment
    spinning = True
    spin_speed = 15
    message = ""

def update_spin():
    """Update the wheel spinning animation"""
    global angle, spin_speed, spinning, coins, message, history
    
    if spinning:
        angle -= spin_speed  # Counter-clockwise rotation
        spin_speed *= 0.98
        
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
            
            # Update coins
            coins += win if win else -bet_amount
            message = f"You won {win} coins!" if win else "You lost!"
            
            if coins <= 0:
                global game_state
                game_state = "GAME_OVER"

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BACKGROUND)
    
    if game_state == "MENU":
        start_btn = draw_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    game_state = "PLAYING"
                    coins = 100
                    history = []
                    message = ""
    
    elif game_state == "PLAYING":
        draw_wheel()
        draw_ui()
        update_spin()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                x, y = event.pos
                
                # Color buttons
                if 100 <= x <= 200 and HEIGHT-80 <= y <= HEIGHT-30:
                    selected_color = "red"
                    message = ""
                elif 220 <= x <= 320 and HEIGHT-80 <= y <= HEIGHT-30:
                    selected_color = "black"
                    message = ""
                elif 340 <= x <= 440 and HEIGHT-80 <= y <= HEIGHT-30:
                    selected_color = "green"
                    message = ""
                elif 460 <= x <= 560 and HEIGHT-80 <= y <= HEIGHT-30:
                    start_spin()
                
                # Bet controls
                elif 580 <= x <= 620 and HEIGHT-80 <= y <= HEIGHT-30:
                    if bet_amount > 10:
                        bet_amount -= 10
                elif 630 <= x <= 670 and HEIGHT-80 <= y <= HEIGHT-30:
                    if bet_amount < coins:
                        bet_amount += 10
    
    elif game_state == "GAME_OVER":
        draw_game_over()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "MENU"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
