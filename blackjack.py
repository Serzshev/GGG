import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 900, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Fonts and Colors
FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)
BIG_FONT = pygame.font.SysFont("arial", 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 120, 0)
RED = (200, 0, 0)
GRAY = (200, 200, 200)
CARD_COLOR = (255, 255, 240)
CARD_BORDER = (0, 0, 0)

# Cards and Values
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

def draw_text(text, font, color, x, y):
    label = font.render(text, True, color)
    win.blit(label, (x, y))

def deal_card():
    return random.choice(cards)

def calculate_score(hand):
    score = sum(card_values[card] for card in hand)
    aces = hand.count("A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def draw_card(card, x, y):
    pygame.draw.rect(win, CARD_COLOR, (x, y, 60, 90))
    pygame.draw.rect(win, CARD_BORDER, (x, y, 60, 90), 2)
    
    # Card face (top text)
    card_text = FONT.render(card, True, BLACK)
    win.blit(card_text, (x + 18, y + 10))
    
    # Card value (bottom text)
    value_text = SMALL_FONT.render(f"= {card_values[card]}", True, BLACK)
    win.blit(value_text, (x + 8, y + 60))

def draw_hand(hand, x, y, hide_first=False):
    for i, card in enumerate(hand):
        if hide_first and i == 0:
            pygame.draw.rect(win, RED, (x + i * 70, y, 60, 90))
            pygame.draw.rect(win, BLACK, (x + i * 70, y, 60, 90), 2)
            draw_text("?", FONT, WHITE, x + i * 70 + 22, y + 30)
        else:
            draw_card(card, x + i * 70, y)

def draw_button(text, x, y, w, h, color):
    pygame.draw.rect(win, color, (x, y, w, h), border_radius=8)
    draw_text(text, FONT, BLACK, x + 10, y + 10)
    return pygame.Rect(x, y, w, h)

def main():
    clock = pygame.time.Clock()
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    game_over = False
    result = ""
    player_turn = True

    running = True
    while running:
        win.fill(GREEN)
        draw_text("Blackjack", BIG_FONT, WHITE, 370, 20)
        draw_text("Your Hand", FONT, WHITE, 50, 140)
        draw_hand(player_hand, 50, 170)
        draw_text("Dealer's Hand", FONT, WHITE, 50, 340)
        draw_hand(dealer_hand, 50, 370, hide_first=player_turn)

        if not game_over and player_turn:
            hit_btn = draw_button("Hit", 700, 200, 120, 50, GRAY)
            stand_btn = draw_button("Stand", 700, 270, 120, 50, GRAY)
        else:
            again_btn = draw_button("Play Again", 680, 400, 160, 50, GRAY)

        if game_over:
            draw_text(result, BIG_FONT, RED if "lose" in result.lower() else WHITE, 300, 500)

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if not game_over and player_turn:
                    if hit_btn.collidepoint(mx, my):
                        player_hand.append(deal_card())
                        if calculate_score(player_hand) > 21:
                            result = "You busted! Dealer wins."
                            game_over = True
                            player_turn = False
                    elif stand_btn.collidepoint(mx, my):
                        player_turn = False
                        while calculate_score(dealer_hand) < 17:
                            dealer_hand.append(deal_card())
                        player_score = calculate_score(player_hand)
                        dealer_score = calculate_score(dealer_hand)
                        if dealer_score > 21:
                            result = "Dealer busted! You win!"
                        elif player_score > dealer_score:
                            result = "You win!"
                        elif player_score < dealer_score:
                            result = "Dealer wins!"
                        else:
                            result = "It's a tie!"
                        game_over = True
                elif game_over:
                    if again_btn.collidepoint(mx, my):
                        main()
                        return

    pygame.quit()
    sys.exit()

main()
