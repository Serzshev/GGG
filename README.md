# 🎲 Roulette Spin Game

A simple roulette-style betting game made with **Pygame**. Spin the wheel, choose your color, and try your luck! This game simulates the experience of placing bets on red, black, or green, just like in a classic casino.

## 📷 Screenshot

*(Add a screenshot here if you'd like by pressing `Print Screen` while the game is running, then paste into an image editor and save.)*

## 🎮 Features

- ✅ Simple UI using Pygame
- ✅ Select a color: **Red**, **Black**, or **Green**
- ✅ Spin the roulette wheel
- ✅ Win coins if your chosen color matches the outcome
- ✅ Multiplied rewards:
  - Red/Black: x2
  - Green: x14
- ✅ Coin balance tracking
- ✅ Bet adjustment (code can be expanded for this)

## 🛠️ Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

Install Pygame with pip:

```bash
pip install pygame
```

Or in **Thonny**, go to:  
`Tools` → `Manage Packages` → Search for `pygame` → Click `Install`.

## ▶️ How to Run

1. Save the script as `roulette_game.py` (or run directly in Thonny).
2. Open a terminal (or Thonny).
3. Run the script:

```bash
python roulette_game.py
```

## 🎯 How to Play

1. Click a color button: **Red**, **Black**, or **Green**.
2. Click **Spin** to spin the wheel.
3. If the ball lands on your chosen color, you win!
4. Your coin balance is shown at the top-left.

### Payouts

| Bet Color | Payout  |
|-----------|---------|
| Red       | 2x Bet  |
| Black     | 2x Bet  |
| Green     | 14x Bet |

## 🧠 How It Works

- The wheel randomly chooses a slot from 0 to 36.
- Each number has an assigned color.
- The wheel spins visually and slows down to a stop.
- The selected slot determines if you win or lose your bet.

## 💡 To-Do / Enhancements (Optional)

- Bet amount adjustment (+/-)
- Add sound effects and animations
- Add luck modifier items (beer, vodka)
- Implement shop system (buy cigars, items, etc.)
- Add a game-over condition or reset option

## 📄 License

This game is for educational and personal use. Feel free to modify and expand it!
