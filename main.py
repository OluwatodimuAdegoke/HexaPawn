import sys
import pygame

reset_button = (200, 200, 200) 
colorbg = (255,255,255)
colorline = (128,128,128)
colorplayer1 = (255,0,0)
colorplayer2 = (0,0,255)
FPS = 60


# board class
class Board:
    def __init__(self,player1,player2):
        self.board = [[player2,player2,player2],[0,0,0],[player1,player1,player1]]
        self.player_pieces = 3
        self.ai_pieces = 3
        self.player1 = player1
        self.player2 = player2
    # Returns the piece at a given row and column
    def get_piece_at(self, row, col):
        return self.board[row][col]
    
    # Moves the piece to the new row and column. Check if it's valid before moving
    def move_piece(self,row, col, new_row, new_col,player):
        if(player ==  self.player1 and self.get_piece_at(new_row, new_col) == self.player2):
            self.ai_pieces -= 1
        elif(player == self.player2 and self.get_piece_at(new_row, new_col) == self.player1):    
            self.player_pieces -= 1
            
        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = 0


    # Checks if the move is valid by checking the current player, the position of the new colums and rows and also valid moves
    def is_valid_move(self, row, col, new_row, new_col,player):
        if(new_col < 0 or new_col > 2 or new_row < 0 or new_row > 2):
            return False
        if self.board[row][col] == self.board[new_row][new_col]:
            return False
        if(self.board[row][col] != player):
            return False

        if(player == self.player1):
            if(new_row == row - 1 and new_col == col and self.board[new_row][new_col] == 0):
                return True
            if(new_row == row - 1 and new_col == col + 1 and self.board[new_row][new_col] == self.player2):
                return True
            if(new_row == row - 1 and new_col == col - 1 and self.board[new_row][new_col] == self.player2):
                return True
            return False
        else:
            if(new_row == row + 1 and new_col == col and self.board[new_row][new_col] == 0):
                return True
            if(new_row == row + 1 and new_col == col + 1 and self.board[new_row][new_col] == self.player1):
                return True
            if(new_row == row + 1 and new_col == col - 1 and self.board[new_row][new_col] == self.player1):
                return True
            return False
        
    # Checks if the current player has won. Returns true if the current player has won, false otherwise
    def check_win_condition(self,player):
        if(player == self.player1):
            if(self.board[0][0] == self.player1 or self.board[0][1] == self.player1 or self.board[0][2] == self.player1):
                print("First row")
                return True
            if(self.ai_pieces == 0):
                print("AI has no pieces")
                return True
            return False
        else:
            if(self.board[2][0] == self.player2 or self.board[2][1] == self.player2 or self.board[2][2] == self.player2 ):
                print("Last row")
                return True
            if(self.player_pieces == 0):
                print("Player has no pieces")
                return True
            return False
        
    def has_valid_moves(self,player):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == player):
                    if(player == self.player1):
                        if(i - 1 >= 0 and self.board[i-1][j] == 0):
                            return True
                        if(i - 1 >= 0 and j + 1 < 3 and self.board[i-1][j+1] == self.player2):
                            return True
                        if(i - 1 >= 0 and j - 1 >= 0 and self.board[i-1][j-1] == self.player2):
                            return True
                    else:
                        if(i + 1 < 3 and self.board[i+1][j] == 0):
                            return True
                        if(i + 1 < 3 and j + 1 < 3 and self.board[i+1][j+1] == self.player1):
                            return True
                        if(i + 1 < 3 and j - 1 >= 0 and self.board[i+1][j-1] == self.player1):
                            return True
        return False

    


class Player:
    def __init__(self, piece, type):
        self.type = type
        self.state = 0
        self.picked_pos = (0,0)
        #TODO: Add configuration for when it can win too


class Game:
    def __init__(self,screen):
        self.screen = screen
        self.player1 = Player(1, "player1")
        self.player2 = Player(2, "ai")
        self.current_player = self.player1
        self.board = Board(self.player1, self.player2)
        self.player1Score = 0
        self.player2Score = 0
        self.last_move = None
        self.configurations = {}


    def make_move(self,player, row, col):
        if player.state == 0 and self.board.get_piece_at(row, col) == player:
            print("Picked up piece")
            player.state = 1
            player.picked_pos = (row, col)
            return False
        elif player.state == 1 and player.picked_pos == (row, col):
            print("Dropped piece")
            player.state = 0
            return False
        elif player.state == 1 and self.board.is_valid_move(player.picked_pos[0], player.picked_pos[1], row, col,self.current_player):
            print("Player 1 has moved")
            self.board.move_piece(player.picked_pos[0], player.picked_pos[1], row, col,player)
            player.state = 0
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

    def ai_move(self):
        for i in range(3):
            for j in range(3):
                print("Checking piece at: " + str(i) + " " + str(j))
                if self.board.get_piece_at(i,j) == self.current_player:
                    print("AI has picked up piece")
                    moves = [-1, 0, 1]
                    for k in moves:
                        if self.board.is_valid_move(i, j, i + 1, j + k, self.current_player):
                            newBoard = [row[:] for row in self.board.board]
                            newBoard[i][j] = 0
                            newBoard[i+1][j+k] = self.current_player
                            if not self.check_configuration(newBoard):
                                self.last_move = self.board_to_tuple(newBoard)
                                pygame.time.wait(500)
                                self.board.move_piece( i, j, i + 1, j + k,self.current_player)
                                print("AI has moved")
                                pygame.time.wait(500)
                                return True
        return False
    
    def human_move(self,pos):
        if pos[0] > 150 or pos[1] > 150:
            return False
        hasMoved = False
        # Get the row and column of the mouse click
        row = pos[1] // 50
        col = pos[0] // 50
        hasMoved = self.make_move(self.current_player, row, col)
        return hasMoved

    def finish_game(self,type):
        if type == "player1":
            print("Player 1 has won")
            self.player1Score += 1
            self.store_configuration(self.last_move)
        elif type == "player2":
            self.player2Score += 1
            print("AI has won")
        else:
            self.store_configuration(self.last_move)
            print("It's a draw")
        print("AI: "+ str(self.player2Score) +" Player: "+ str(self.player1Score))
        pygame.time.wait(1000)
        self.reset_game()
        return
    
    def switch_turn(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
    
    def end_turn(self):
        if self.board.check_win_condition(self.current_player):
            winner = "player1" if self.current_player == self.player1 else "player2"
            self.finish_game(winner)
            return True
        elif not  self.board.has_valid_moves(self.current_player):
            self.finish_game("draw")
            return True
        else:
            print("Switching turn")
            self.switch_turn()
        return False
    
    def reset_game(self):
        self.board = Board(self.player1, self.player2)
        self.current_player = self.player1

    def handle_reset_button(self, pos):
        if pos[0] > 170 and pos[0] < 200 and pos[1] > 115 and pos[1] < 145:
            self.reset_game()
            return True
        return False

    def draw(self):
        self.draw_valid_move()
        self.draw_board()
        self.draw_pawns()
        self.draw_ui()
        self.draw_reset_button()

     
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
                if(self.board.get_piece_at(i,j) == self.player1):
                    pygame.draw.circle(self.screen, colorplayer1, (j*50+25,i*50+25), 20)
                elif(self.board.get_piece_at(i,j) == self.player2):
                    pygame.draw.circle(self.screen, colorplayer2, (j*50+25,i*50+25), 20)


    def draw_reset_button(self):
        font = pygame.font.Font("freesansbold.ttf", 12)
        button_rect = pygame.Rect(170, 115, 30, 30)
        
        # Draw the button
        pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Border
        
        # Draw the text
        text = font.render("R", True, (0, 0, 0))
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_valid_move(self):
        if self.current_player.state == 1:
            row = self.current_player.picked_pos[0]
            col = self.current_player.picked_pos[1]
            overlay = pygame.Surface((48, 48), pygame.SRCALPHA)
            
            overlay.fill((200,200, 200, 200))  
            can_move = False
            if row - 1 >= 0 and self.board.board[row - 1][col] == 0:
                self.screen.blit(overlay, (col*50+2, (row-1)*50 +2))
                can_move = True
            if row - 1 >= 0 and col + 1 < 3 and self.board.board[row - 1][col + 1] == self.player2:
                self.screen.blit(overlay, ((col+1)*50+2, (row-1)*50+2))
                can_move = True
            if row - 1 >= 0 and col - 1 >= 0 and self.board.board[row - 1][col - 1] == self.player2:
                self.screen.blit(overlay, ((col-1)*50+2, (row-1)*50+2))
                can_move = True
            if not can_move:
                overlay.fill((255,0, 0, 100))
                self.screen.blit(overlay, (col*50+2, (row)*50 +2))
                


    # Draw the UI
    def draw_ui(self):
        font = pygame.font.Font("freesansbold.ttf", 15)
        textPlayer2 = font.render("p2 -  " + str(self.player2Score), True, (0,0,0))
        textPlayer1 = font.render("p1 -  " + str(self.player1Score), True, (0,0,0))
        textScore = font.render("SCORE", True, (0,0,0))
        self.screen.blit(textScore, (160, 10))
        if self.current_player == self.player1:
            pygame.draw.circle(self.screen, colorplayer1, (185, 90), 20)
        else:
            pygame.draw.circle(self.screen, colorplayer2, (185, 90), 20)
        self.screen.blit(textPlayer1, (165, 50))
        self.screen.blit(textPlayer2, (165, 30))
        return 0

    

 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("HexaPawn")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((222,152))


    FramePerSec = pygame.time.Clock()

    game = Game(screen=screen)
    game.current_player = game.player1
    screen.fill(colorbg)


    # main loop
    while True:
 
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.current_player.type == "ai":
                if game.ai_move():
                    game.end_turn()
                else:
                    game.finish_game("player1")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.human_move(pygame.mouse.get_pos()):
                    game.end_turn()
                elif game.handle_reset_button(pygame.mouse.get_pos()):
                    continue


        
                
        screen.fill(colorbg)
        game.draw()
        pygame.display.update()
        FramePerSec.tick(FPS)

   
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()