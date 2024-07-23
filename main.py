import sys
import pygame

colorbg = (255,255,255)
colorline = (128,128,128)
colorplayer1 = (255,0,0)
colorplayer2 = (0,0,255)

# type of piece
# 0 = empty
# 1 = player 1
# 2 = ai

# board class
class Board:
    def __init__(self):
        self.board = [[2, 2, 2], [0, 0, 0], [1, 1, 1]]
        # self.turn = 0
        self.current_player = 1
        self.player_pieces = 3
        self.ai_pieces = 1

    # Returns the piece at a given row and column
    def get_piece_at(self, row, col):
        return self.board[row][col]
    
    # Moves the piece to the new row and column. Check if it's valid before moving
    def move_piece(self,row, col, new_row, new_col):
        if(self.current_player == 1 and self.get_piece_at(new_row, new_col) == 2):
            self.ai_pieces -= 1
        elif(self.current_player == 2 and self.get_piece_at(new_row, new_col) == 1):    
            self.player_pieces -= 1
            
        self.board[new_row][new_col] = self.board[row][col]
        self.board[row][col] = 0


    # Checks if the move is valid by checking the current player, the position of the new colums and rows and also valid moves
    def is_valid_move(self, row, col, new_row, new_col, curr_player):
        if(self.board[row][col] != curr_player):
            return False
        if(new_col < 0 or new_col > 2 or new_row < 0 or new_row > 2):
            return False
        if(self.current_player == 1):
            if(new_row == row - 1 and new_col == col):
                return True
            if(new_row == row - 1 and new_col == col + 1 ):
                return True
            if(new_row == row - 1 and new_col == col - 1 ):
                return True
            return False
        else:
            if(new_row == row + 1 and new_col == col):
                return True
            if(new_row == row + 1 and new_col == col + 1 ):
                return True
            if(new_row == row + 1 and new_col == col - 1 ):
                return True
            return False
        
    # Checks if the current player has won. Returns true if the current player has won, false otherwise
    def check_win_condition(self):
        if(self.current_player == 2):
            if(self.board[0][0] == 1 or self.board[0][1] == 1 or self.board[0][2] == 1):
                return True
            if(self.ai_pieces == 0):
                return True
            return False
        else:
            if(self.board[2][0] == 2 or self.board[2][1] == 2 or self.board[2][2] == 2):
                return True
            if(self.player_pieces == 0):
                return True
            return False

class Player:
    def __init__(self, player):
        self.player = player
        self.state = 0
        self.picked_pos = (0,0)

    def make_move(self,board):
        print("AI Turn")
        # Make the AI Move
        return 0

class Game:
    def __init__(self,screen):
        self.screen = screen
        self.board = Board()
        self.player = Player(1)
        self.ai = Player(2)

    def switch_turn(self):
        if(self.board.current_player == 1):
            self.board.current_player = 2
        else:
            self.board.current_player = 1
    def handle_events(self,event):
        # Check if the event is a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse
            pos = pygame.mouse.get_pos()
            # Get the row and column of the mouse click
            row = pos[1] // 50
            col = pos[0] // 50
            print(row, col)
            if self.board.current_player == 1 and self.player.state == 0 and self.board.get_piece_at(row, col) == 1:
                print("Picked up piece")
                self.player.state = 1
                self.picked_pos = (row, col)
            elif self.board.current_player == 1 and self.player.state == 1 and self.picked_pos == (row, col):
                print("Dropped piece")
                self.player.state = 0
            elif self.board.current_player == 1 and self.player.state == 1 and self.board.is_valid_move(self.picked_pos[0], self.picked_pos[1], row, col, 1):
                print("Moved piece")
                self.board.move_piece(self.picked_pos[0], self.picked_pos[1], row, col)
                self.switch_turn()
                self.player.state = 0

            print(self.board.board)
        return 0
    def update(self):
        # Update the game
        return 0

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
        # scoreAI = font.render(str(self.board.ai_pieces), True, (0,0,0))
        # scorePlayer = font.render(str(self.board.player_pieces), True, (0,0,0))
        if self.board.current_player == 1:
            pygame.draw.circle(self.screen, colorplayer1, (170, 120), 15)
        else:
            pygame.draw.circle(self.screen, colorplayer2, (170, 120), 15)
        self.screen.blit(textAI, (160, 20))

        self.screen.blit(textPlayer, (160, 70))

        return 0

 
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
    screen.fill(colorbg)

    # main loop
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_events(event)

        screen.fill(colorbg)
        game.draw()
        if game.board.check_win_condition():
            # Handle this better
            print("Player 1" if str(game.board.current_player) == 2 else "Player 0" + " has won")
            pygame.quit()
        
        if game.board.current_player == 2:
            game.ai.make_move(game.board)
            game.switch_turn()

        pygame.display.update()
        FramePerSec.tick(FPS)
        # render()

   
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()