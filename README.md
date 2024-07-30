# HexaPawn

Implementation of a Hexapawn game using pygame to showcase the use of an artificial intelligence algorithm.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Classes](#classes)
  - [Game](#game)
  - [Player](#player)
  - [Board](#board)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/hexapawn.git
   ```
2. Navigate to the project directory:
   ```sh
   cd hexapawn
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To start the game, run the following command:

```sh
python game.py
```

## Game Rules

1. The game is played on a 3x3 board.
2. Each player has three pawns.
3. Players take turns to move their pawns.
4. Pawns can move forward to an empty square or diagonally forward to capture an opponent's pawn.
5. The game ends when a player reaches the opposite side of the board, or when the opponent has no valid moves left.

## Classes

### Game

The Game class represents the HexaPawn game. It handles the game logic, including making moves, checking configurations, and determining the winner.

### Player

The Player class represents a player in the game. It stores the player's type, state, and the position of the picked piece.

### Board

The Board class represents the game board. It handles the board state, moving pieces, and checking for valid moves and win conditions.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
