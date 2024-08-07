import sys
import pygame
from game import Game
from constants import FPS, SCREEN_HEIGHT,SCREEN_WIDTH ,BACKGROUND_COLOR
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()

    pygame.display.set_caption("HexaPawn")
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

    FramePerSec = pygame.time.Clock()

    game = Game(screen=screen)
    game.current_player = game.player1
    screen.fill(BACKGROUND_COLOR)


    # main loop
    while True:
 
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game.game_over == False:
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
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.game_over = False
                    game.winner = None
                    game.reset_game()


        
                
        screen.fill(BACKGROUND_COLOR)
        game.draw()
        pygame.display.update()
        FramePerSec.tick(FPS)

   
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()