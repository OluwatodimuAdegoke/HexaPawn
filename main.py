import sys
import pygame

colorbg = (255,255,255)
colorline = (128,128,128)
colorplayer1 = (255,0,0)
colorplayer2 = (0,0,255)
global ai
global p
ai = 0
p = 0
# type of piece
# 0 = empty
# 1 = player 1
# 2 = ai

# board class
class Board:
    def __init__(self,player1,player2):
        self.board = [[2, 2, 2], [0, 0, 0], [1, 1, 1]]
        self.current_player = player1
        self.player_pieces = 3
        self.ai_pieces = 3
        self.player1 = player1
        self.player2 = player2
    # Returns the piece at a given row and column
    def get_piece_at(self, row, col):
        return self.board[row][col]
    
    # Moves the piece to the new row and column. Check if it's valid before moving
    def move_piece(self,row, col, new_row, new_col):
        if(self.current_player ==  self.player1 and self.get_piece_at(new_row, new_col) == 2):
            self.ai_pieces -= 1
        elif(self.current_player == self.player2 and self.get_piece_at(new_row, new_col) == 1):    
            self.player_pieces -= 1
            
        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = 0


    # Checks if the move is valid by checking the current player, the position of the new colums and rows and also valid moves
    def is_valid_move(self, row, col, new_row, new_col, curr_player):
        if(new_col < 0 or new_col > 2 or new_row < 0 or new_row > 2):
            return False
        if self.board[row][col] == self.board[new_row][new_col]:
            return False
        if(self.board[row][col] != curr_player):
            return False

        if(self.current_player == self.player1):
            if(new_row == row - 1 and new_col == col and self.board[new_row][new_col] == 0):
                return True
            if(new_row == row - 1 and new_col == col + 1 and self.board[new_row][new_col] == 2):
                return True
            if(new_row == row - 1 and new_col == col - 1 and self.board[new_row][new_col] == 2):
                return True
            return False
        else:
            if(new_row == row + 1 and new_col == col and self.board[new_row][new_col] == 0):
                return True
            if(new_row == row + 1 and new_col == col + 1 and self.board[new_row][new_col] == 1):
                return True
            if(new_row == row + 1 and new_col == col - 1 and self.board[new_row][new_col] == 1):
                return True
            return False
        
    # Checks if the current player has won. Returns true if the current player has won, false otherwise
    def check_win_condition(self):
        if(self.current_player == self.player1):
            if(self.board[0][0] == 1 or self.board[0][1] == 1 or self.board[0][2] == 1):
                print("First row")
                return True
            if(self.ai_pieces == 0):
                print("AI has no pieces")
                return True
            return False
        else:
            if(self.board[2][0] == 2 or self.board[2][1] == 2 or self.board[2][2] == 2):
                print("Last row")
                return True
            if(self.player_pieces == 0):
                print("Player has no pieces")
                return True
            return False
        
    def has_valid_moves(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == self.current_player.player):
                    if(self.current_player == self.player1):
                        if(i - 1 >= 0 and self.board[i-1][j] == 0):
                            return True
                        if(i - 1 >= 0 and j + 1 < 3 and self.board[i-1][j+1] == 2):
                            return True
                        if(i - 1 >= 0 and j - 1 >= 0 and self.board[i-1][j-1] == 2):
                            return True
                    else:
                        if(i + 1 < 3 and self.board[i+1][j] == 0):
                            return True
                        if(i + 1 < 3 and j + 1 < 3 and self.board[i+1][j+1] == 1):
                            return True
                        if(i + 1 < 3 and j - 1 >= 0 and self.board[i+1][j-1] == 1):
                            return True
        return False
    


class Player:
    def __init__(self, player, type):
        self.type = type
        self.player = player
        self.state = 0
        self.picked_pos = (0,0)
        self.configurations = {}
        self.last_move = None
        #TODO: Add configuration for when it can win too

    def make_move(self,board, row, col):
        if self.type == "player1":
            if self.state == 0 and board.get_piece_at(row, col) == 1:
                print("Picked up piece")
                self.state = 1
                self.picked_pos = (row, col)
                return False
            elif self.state == 1 and self.picked_pos == (row, col):
                print("Dropped piece")
                self.state = 0
                return False
            elif self.state == 1 and board.is_valid_move(self.picked_pos[0], self.picked_pos[1], row, col, self.player):
                print("Player 1 has moved")
             
                board.move_piece(self.picked_pos[0], self.picked_pos[1], row, col)
                self.state = 0
                return True
        elif self.type == "player2":
            if self.state == 0 and board.get_piece_at(row, col) == 2:
                print("Picked up piece")
                self.state = 1
                self.picked_pos = (row, col)
                return False
            elif self.state == 1 and self.picked_pos == (row, col):
                print("Dropped piece")
                self.state = 0
                return False
            elif self.state == 1 and board.is_valid_move(self.picked_pos[0], self.picked_pos[1], row, col, self.player):
                print("Player 2 has moved")
                board.move_piece(self.picked_pos[0], self.picked_pos[1], row, col)
                self.state = 0
                return True
        return False

    def board_to_tuple(self, board):
        return tuple([tuple(row) for row in board])
    
    def store_configuration(self, newBoard):
        self.configurations[self.board_to_tuple(newBoard)] = True

    def check_configuration(self, newBoard):
        if self.board_to_tuple(newBoard) in self.configurations:
            return True
        return False

    def ai_move(self,board):
        for i in range(3):
            for j in range(3):
                if(board.get_piece_at(i,j) == self.player):
                    moves = [-1, 0, 1]
                    for k in moves:
                        if board.is_valid_move(i, j, i + 1, j + k, self.player):
                            newBoard = [row[:] for row in board.board]
                            newBoard[i][j] = 0
                            newBoard[i+1][j+k] = self.player
                            if not self.check_configuration(newBoard):
                                self.last_move = self.board_to_tuple(newBoard)
                                pygame.time.wait(1000)
                                board.board = newBoard
                                print("AI has moved")
                                return True
        return False
    
    def human_move(self,event,board):
        hasMoved = False
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Get the position of the mouse
            pos = pygame.mouse.get_pos()
            # Get the row and column of the mouse click
            row = pos[1] // 50
            col = pos[0] // 50
            if board.current_player == self.player:
                hasMoved = self.make_move(board, row, col)
            else:
                hasMoved = self.make_move(board, row, col)
        return hasMoved


class Game:
    def __init__(self,screen):
        self.screen = screen
        self.player1 = Player(1, "player1")
        self.player2 = Player(2, "ai")
        self.board = Board(self.player1, self.player2)

    def finish_game(self,type):
        if type == "player1":
            print("Player 1 has won")
            global p
            p = p + 1
            self.player2.store_configuration(self.player2.last_move)
        elif type == "player2":
            global ai
            ai += 1
            print("AI has won")
        else:
            self.player2.store_configuration(self.player2.last_move)
            print("It's a draw")
        print(self.player2.configurations)
        print("AI: "+ str(ai) +" Player: "+ str(p))
        pygame.time.wait(1000)
        return
    
    def switch_turn(self):
        if self.check_win_condition():
            return
        if(self.board.current_player == self.player1):
            self.board.current_player = self.player2
        else:
            self.board.current_player = self.player1

    def handle_events(self,event):
        # Check if the event is a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse
            pos = pygame.mouse.get_pos()
            # Get the row and column of the mouse click
            row = pos[1] // 50
            col = pos[0] // 50
            if self.board.current_player == self.player1:
                move = self.player1.make_move(self.board, row, col)
            else:
                move = self.player2.make_move(self.board, row, col)
            return move
        return False
    
    def update(self):
        # Update the game
        return 0
    
    def reset_game(self):
        self.board = Board(self.player1, self.player2)

    def draw(self):
        self.draw_board()
        self.draw_pawns()
        self.draw_ui()
     
    # Draw the board
    def draw_board(self):
        pygame.draw.line(self.screen, colorline, (0,0), (150,0),2)
        pygame.draw.line(self.screen, colorline, (0,50), (150,50),2)
        pygame.draw.line(self.screen, colorline, (0,100), (150,100),2)
        pygame.draw.line(self.screen, colorline, (0,150), (150,150),2)
        pygame.draw.line(self.screen, colorline, (0,0), (0,150),2)
        pygame.draw.line(self.screen, colorline, (50,0), (50,150),2)
        pygame.draw.line(self.screen, colorline, (100,0), (100,150),2)
        pygame.draw.line(self.screen, colorline, (150,0), (150,150),2)
    
    # Draw the pawns on the board
    def draw_pawns(self):
        for i in range(3):
            for j in range(3):
                if(self.board.get_piece_at(i,j) == 1):
                    pygame.draw.circle(self.screen, colorplayer1, (j*50+25,i*50+25), 20)
                elif(self.board.get_piece_at(i,j) == 2):
                    pygame.draw.circle(self.screen, colorplayer2, (j*50+25,i*50+25), 20)

    # Draw the UI
    def draw_ui(self):
        font = pygame.font.Font("freesansbold.ttf", 15)
        textAI = font.render("AI : " + str(self.board.ai_pieces), True, (0,0,0))
        textPlayer = font.render("P : " + str(self.board.player_pieces), True, (0,0,0))
        if self.board.current_player == 1:
            pygame.draw.circle(self.screen, colorplayer1, (170, 120), 15)
        else:
            pygame.draw.circle(self.screen, colorplayer2, (170, 120), 15)
        self.screen.blit(textAI, (160, 20))

        self.screen.blit(textPlayer, (160, 70))

        return 0

    def check_win_condition(self):
        if self.board.check_win_condition():
            self.finish_game("player1" if self.board.current_player == self.player1 else "player2")
            self.reset_game()
            return True
        elif not self.board.has_valid_moves():
            self.finish_game("draw")
            self.reset_game()
            return True
        return False
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("HexaPawn")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((202,152))


    FramePerSec = pygame.time.Clock()
    FPS = 60

    
    game = Game(screen=screen)
    game.board.current_player = game.player1
    screen.fill(colorbg)


    # main loop
    while True:
 
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.board.current_player.type == "ai":
                if not game.board.current_player.ai_move(game.board):
                    game.finish_game("player1")
                game.switch_turn()
              
            else:
                # res = game.handle_events(event)
                if game.board.current_player.human_move(event,game.board):
                    game.switch_turn()
        
                
                
        screen.fill(colorbg)
        game.draw()
        pygame.display.update()
        FramePerSec.tick(FPS)

   
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()