import pygame
from board import Board
from player import Player
from constants import PLAYER1_COLOR, PLAYER2_COLOR, LINE_COLOR, VALID_MOVE_COLOR

class Game:
    """
    Represents the game of HexaPawn.
    """

    def __init__(self, screen):
        """
        Initializes the Game object.
        """
        self.screen = screen
        self.player1 = Player(1, "player1")
        self.player2 = Player(2, "ai")
        self.current_player = self.player1
        self.board = Board(self.player1, self.player2)
        self.player1Score = 0
        self.player2Score = 0
        self.last_move = None
        self.configurations = {}
        self.game_over = False
        self.winner = None

    def make_move(self, player, row, col):
        """
        Makes a move on the game board.
        Returns:
        - True if the move is valid and made successfully, False otherwise.
        """
        if player.state == 0 and self.board.get_piece_at(row, col) == player:
            player.state = 1
            player.picked_pos = (row, col)
            return False
        elif player.state == 1 and player.picked_pos == (row, col):
            player.state = 0
            return False
        elif player.state == 1 and self.board.is_valid_move(player.picked_pos[0], player.picked_pos[1], row, col, self.current_player):
            self.board.move_piece(player.picked_pos[0], player.picked_pos[1], row, col, player)
            player.state = 0
            return True
        return False

    def board_to_tuple(self, board):
        """
        Converts the game board to a tuple.
        Returns:
        - A tuple representation of the game board.
        """
        return tuple([tuple(row) for row in board])

    def store_configuration(self, newBoard):
        """
        Stores a game configuration in the configurations dictionary.
        """
        self.configurations[self.board_to_tuple(newBoard)] = True

    def check_configuration(self, newBoard):
        """
        Checks if a game configuration exists in the configurations dictionary.
        Returns:
        - True if the configuration exists, False otherwise.
        """
        if self.board_to_tuple(newBoard) in self.configurations:
            return True
        return False

    def ai_move(self):
        """
        Makes a move for the AI player.
        Returns:
        - True if a move is made, False otherwise.
        """
        for i in range(3):
            for j in range(3):
                if self.board.get_piece_at(i, j) == self.current_player:
                    moves = [-1, 0, 1]
                    for k in moves:
                        if self.board.is_valid_move(i, j, i + 1, j + k, self.current_player):
                            newBoard = [row[:] for row in self.board.board]
                            newBoard[i][j] = 0
                            newBoard[i + 1][j + k] = self.current_player
                            if not self.check_configuration(newBoard):
                                self.last_move = self.board_to_tuple(newBoard)
                                pygame.time.wait(500)
                                self.board.move_piece(i, j, i + 1, j + k, self.current_player)
                                pygame.time.wait(500)
                                return True
        return False

    def human_move(self, pos):
        """
        Makes a move for the human player.
        Returns:
        - True if a move is made, False otherwise.
        """
        if pos[0] > 150 or pos[1] > 150:
            return False
        hasMoved = False
        # Get the row and column of the mouse click
        row = pos[1] // 50
        col = pos[0] // 50
        hasMoved = self.make_move(self.current_player, row, col)
        return hasMoved

    def finish_game(self, type):
        """
        Finishes the game and updates the scores.
        """
        if type == "player1":
            self.player1Score += 1
            self.store_configuration(self.last_move)
            self.winner = "player1"
        elif type == "player2":
            self.player2Score += 1
            self.winner = "player2"
        else:
            self.store_configuration(self.last_move)
            self.winner = "draw"
        self.game_over = True
   
        # self.reset_game()
        return

    def switch_turn(self):
        """
        Switches the turn between players.
        """
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def end_turn(self):
        """
        Ends the current turn and checks for game over conditions.
        """
        if self.board.check_win_condition(self.current_player):
            winner = "player1" if self.current_player == self.player1 else "player2"
            self.finish_game(winner)
            return True
        elif not self.board.has_valid_moves(self.current_player):
            self.finish_game("draw")
            return True
        else:
            self.switch_turn()
        return False


    def reset_game(self):
        """
        Resets the game to its initial state.
        """
        self.board = Board(self.player1, self.player2)
        self.current_player = self.player1

    def handle_reset_button(self, pos):
        """
        Handles the reset button click.
        Returns:
        - True if the game is reset, False otherwise.
        """
        if pos[0] > 170 and pos[0] < 200 and pos[1] > 115 and pos[1] < 145:
            self.reset_game()
            return True
        return False

    def draw(self):
        """
        Draws the game on the screen.
        """
        self.draw_valid_move()
        self.draw_board()
        self.draw_pawns()
        self.draw_ui()
        self.draw_reset_button()
        self.draw_final()

    def draw_board(self):
        """
        Draws the game board on the screen.
        """
        pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (150, 0), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 50), (150, 50), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 100), (150, 100), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 150), (150, 150), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (0, 150), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (50, 0), (50, 150), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (100, 0), (100, 150), 2)
        pygame.draw.line(self.screen, LINE_COLOR, (150, 0), (150, 150), 2)

    def draw_pawns(self):
        """
        Draws the pawns on the game board.
        """
        for i in range(3):
            for j in range(3):
                if self.board.get_piece_at(i, j) == self.player1:
                    pygame.draw.circle(self.screen, PLAYER1_COLOR, (j * 50 + 25, i * 50 + 25), 20)
                elif self.board.get_piece_at(i, j) == self.player2:
                    pygame.draw.circle(self.screen, PLAYER2_COLOR, (j * 50 + 25, i * 50 + 25), 20)

    def draw_reset_button(self):
        """
        Draws the reset button on the screen.
        """
        font = pygame.font.Font("freesansbold.ttf", 12)
        button_rect = pygame.Rect(170, 115, 30, 30)

        # Draw the button
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Border

        # Draw the text
        text = font.render("R", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_valid_move(self):
        """
        Draws the valid move overlay on the game board.
        """
        if self.current_player.state == 1:
            row = self.current_player.picked_pos[0]
            col = self.current_player.picked_pos[1]
            overlay = pygame.Surface((48, 48), pygame.SRCALPHA)

            overlay.fill(VALID_MOVE_COLOR)
            can_move = False
            if row - 1 >= 0 and self.board.board[row - 1][col] == 0:
                self.screen.blit(overlay, (col * 50 + 2, (row - 1) * 50 + 2))
                can_move = True
            if row - 1 >= 0 and col + 1 < 3 and self.board.board[row - 1][col + 1] == self.player2:
                self.screen.blit(overlay, ((col + 1) * 50 + 2, (row - 1) * 50 + 2))
                can_move = True
            if row - 1 >= 0 and col - 1 >= 0 and self.board.board[row - 1][col - 1] == self.player2:
                self.screen.blit(overlay, ((col - 1) * 50 + 2, (row - 1) * 50 + 2))
                can_move = True
            if not can_move:
                overlay.fill((255, 0, 0, 100))
                self.screen.blit(overlay, (col * 50 + 2, (row) * 50 + 2))

    def draw_ui(self):
        """
        Draws the user interface on the screen.
        """
        font = pygame.font.Font("freesansbold.ttf", 15)
        textPlayer2 = font.render("p2 -  " + str(self.player2Score), True, (0, 0, 0))
        textPlayer1 = font.render("p1 -  " + str(self.player1Score), True, (0, 0, 0))
        textScore = font.render("SCORE", True, (0, 0, 0))
        self.screen.blit(textScore, (160, 10))
        if self.current_player == self.player1:
            pygame.draw.circle(self.screen, PLAYER1_COLOR, (185, 90), 20)
        else:
            pygame.draw.circle(self.screen, PLAYER2_COLOR, (185, 90), 20)
        self.screen.blit(textPlayer1, (165, 50))
        self.screen.blit(textPlayer2, (165, 30))


    def draw_final(self):
        if self.game_over:
            font = pygame.font.Font("freesansbold.ttf", 20)
            text = ""
            if self.winner == "player1":
                text = font.render("Player 1 wins", True, (0, 0, 0))
            elif self.winner == "player2":
                text = font.render("Player 2 wins", True, (0, 0, 0))
            else:
                text = font.render("Draw", True, (0, 0, 0))   
            self.screen.blit(text, (40, 65))
