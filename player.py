
class Player:
    def __init__(self, piece, type):
        self.type = type
        self.state = 0
        self.picked_pos = (0,0)
        #TODO: Add configuration for when it can win too

