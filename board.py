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

    