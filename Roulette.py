import pygame
import random
import math
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎲 Roulette Spin Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)

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

# Roulette layout: (number, color)
roulette_slots = [
    (0, "green")
] + [(i, "red" if i % 2 == 1 else "black") for i in range(1, 37)]

def draw_wheel():
    screen.fill((30, 100, 30))
    pygame.draw.circle(screen, (100, 100, 100), (WIDTH//2, HEIGHT//2), 200)

    slot_angle = 360 / len(roulette_slots)
    for i, (num, color) in enumerate(roulette_slots):
        start_angle = math.radians((i * slot_angle + angle) % 360)
        end_angle = math.radians(((i+1) * slot_angle + angle) % 360)
        pygame.draw.arc(
            screen,
            (0, 200, 0) if color == "green" else (200, 0, 0) if color == "red" else (0, 0, 0),
            (100, 100, 400, 400),
            start_angle, end_angle,
            40
        )

def draw_ui():
    pygame.draw.rect(screen, (200, 0, 0) if selected_color == "red" else (100, 0, 0), (100, 500, 80, 40))
    pygame.draw.rect(screen, (0, 0, 0) if selected_color == "black" else (50, 50, 50), (200, 500, 80, 40))
    pygame.draw.rect(screen, (0, 150, 0) if selected_color == "green" else (0, 80, 0), (300, 500, 80, 40))
    pygame.draw.rect(screen, (0, 100, 255), (400, 500, 80, 40))

    screen.blit(font.render("Red", True, (255, 255, 255)), (110, 510))
    screen.blit(font.render("Black", True, (255, 255, 255)), (205, 510))
    screen.blit(font.render("Green", True, (255, 255, 255)), (305, 510))
    screen.blit(font.render("Spin", True, (255, 255, 255)), (410, 510))

    screen.blit(font.render(f"Coins: {coins}", True, (255, 255, 255)), (20, 20))
    screen.blit(font.render(f"Bet: {bet_amount}", True, (255, 255, 255)), (20, 50))
    if message:
        screen.blit(font.render(message, True, (255, 255, 0)), (20, 90))

    if result_number is not None:
        res_txt = f"Landed on {result_number} ({result_color})"
        screen.blit(big_font.render(res_txt, True, (255, 255, 255)), (100, 400))

def start_spin():
    global target_angle, spinning, spin_speed, result_number, result_color, message

    if not selected_color:
        message = "Please select a color!"
        return

    result_number, result_color = random.choice(roulette_slots)
    result_index = roulette_slots.index((result_number, result_color))
    slot_angle = 360 / len(roulette_slots)
    stop_angle = result_index * slot_angle
    spins = random.randint(3, 5)  # full spins before stopping
    target_angle = (spins * 360) + stop_angle
    spinning = True
    spin_speed = 15
    message = ""

def update_spin():
    global angle, spin_speed, spinning, coins, message

    if spinning:
        angle += spin_speed
        spin_speed *= 0.97  # slow down
        if spin_speed < 0.5:
            spinning = False
            angle %= 360

            win = False
            if selected_color == result_color:
                if result_color == "green":
                    win = bet_amount * 14
                else:
                    win = bet_amount * 2
                coins += win
                message = f"You won {win} coins!"
            else:
                coins -= bet_amount
                message = "You lost!"

# Main loop
running = True
while running:
    draw_wheel()
    draw_ui()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
            x, y = event.pos
            if 100 <= x <= 180 and 500 <= y <= 540:
                selected_color = "red"
            elif 200 <= x <= 280 and 500 <= y <= 540:
                selected_color = "black"
            elif 300 <= x <= 380 and 500 <= y <= 540:
                selected_color = "green"
            elif 400 <= x <= 480 and 500 <= y <= 540:
                if coins >= bet_amount:
                    start_spin()
                else:
                    message = "Not enough coins!"

    update_spin()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
