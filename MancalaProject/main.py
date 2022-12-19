import random

import pygame
import sys

opponent_type = sys.argv[1]
print(opponent_type)
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([800, 500])
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


player_turn = 1
game_is_running = True

# function that draws the table and the helpful information besides this like which player turns it is and what part
# of the table has every player
def draw_table(screen):
    """
    #function that draws the table and the helpful information besides this like which player turns it is and what part
    #of the table has every player
    :param screen: is getting the screen on which to draw
    """
    pygame.draw.rect(screen, (52, 20, 6), pygame.Rect(0,100,800,300))
    for i in range(6):
        pygame.draw.circle(screen,(196,122,88), ((i+1) * 100 + 50, 175), 35)
        pygame.draw.circle(screen,(196,122,88), ((i+1) * 100 + 50, 325), 35)
    pygame.draw.ellipse(screen, (196,122,88), (25, 125, 75, 250))
    pygame.draw.ellipse(screen, (196, 122, 88), (700, 125, 75, 250))
    text_surface = my_font.render("Player 1", False, (0,255,0))
    screen.blit(text_surface, (350,50))
    text_surface = my_font.render("Player 2", False, (0, 255, 0))
    screen.blit(text_surface, (350, 400))
    text_surface = my_font.render(f"Turn:Player {player_turn + 1}", False, (0, 255, 0))
    screen.blit(text_surface, (0, 50))
    pygame.display.flip()



def draw_stones(table, store, screen):
    """
    # function that draws on screen the number of stones in every position
    :param table: table where the values of every hole is kept
    :param store: list of score of every player
    :param screen: place where to draw the stones
    :return:
    """
    for i in range(6):
        text_surface = my_font.render(str(table[0][i]) + 'x', False, (0,255,0))
        text_surface2 = my_font.render(str(table[1][i]) + 'x', False, (0,255,0))
        screen.blit(text_surface, ((i+1) * 100 + 25, 150))
        screen.blit(text_surface2,((i+1) * 100 + 25, 300))
    for i in range(2):
        text_surface = my_font.render(str(store[i]) + 'x', False, (0, 255, 0))
        screen.blit(text_surface,(i*675 + 50,225))


def verify_move(pos, player_turn):
    """

    # function that verifies that the position on which the player click is a valid position and the move can be made
    :param pos: position of the mouse on the screen
    :param player_turn: index to see which player turn is
    :return: -1 for an invalid position i in range (6) which means the column that was selected
    """
    if player_turn == 0:
        if pos[1] not in range(140, 210):
            return -1
        else:
            for i in range(6):
                if pos[0] in range((i+1) * 100 + 50 - 35, (i+1) * 100 + 50 + 35):
                    return i
            return -1
    else:
        if pos[1] not in range(290, 360):
            return -1
        else:
            for i in range(6):
                if pos[0] in range((i+1) * 100 + 50 - 35, (i+1) * 100 + 50 + 35):
                    return i
            return -1



def init_game():
    """
    # function that is setting the default value in every position and initialize the scores of every player
    :return: the values of store and table
    """
    store= []
    store.append(0)
    store.append(0)
    table = []
    table.append([4,4,4,4,4,4])
    table.append([4,4,4,4,4,4])
    return (store, table)

def make_move(player_turn, selected_column):
    """
    # function that change all the needed values when a move is made
    :param player_turn: to see the player whose turn is right now
    :param selected_column: the column that the player clicked
    :return:
    """
    line = player_turn
    stones = table[line][selected_column]
    table[line][selected_column] = 0
    while stones:
        if line == 0:
            selected_column = selected_column - 1
        else:
            selected_column = selected_column + 1
        if selected_column == 6:
            if line == player_turn:
                store[player_turn] = store[player_turn] + 1
            line = 1 - line
            stones = stones - 1
            continue
        if selected_column == -1:
            if line == player_turn:
                store[player_turn] = store[player_turn] + 1
            line = 1 - line
            stones = stones - 1
            continue
        table[line][selected_column] = table[line][selected_column] + 1
        stones = stones - 1
    if line == player_turn and selected_column in range(0,5) and table[line][selected_column]  == 1:
        store[player_turn] = store[player_turn] + table[1 - line][selected_column]
        table[1-line][selected_column] = 0


def end_game(player_turn):
    """
    # function that see which player has won and is showing this information on the screen
    :param player_turn: to see the player whose turn is right now
    """
    store[player_turn] = store[player_turn] + sum(table[1-player_turn])
    table[1-player_turn] = [0] * 6
    if store[player_turn] > store[1 - player_turn]:
        print(f"Player {player_turn + 1} wins")
        text_surface = my_font.render(f"Player {player_turn + 1} wins", False, (0, 255, 0))
        screen.blit(text_surface, (300, 0))
    else:
        print(f"Player {1 - player_turn + 1} wins")
        text_surface = my_font.render(f"Player {1 - player_turn + 1} wins", False, (0, 255, 0))
        screen.blit(text_surface, (300, 0))
    pygame.display.flip()

# Run until the user asks to quit
running = True
# Fill the background with white

rez = init_game()
store = rez[0]
table = rez[1]



screen.fill((255, 255, 255))

draw_table(screen)
draw_stones(table,store,screen)



while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and game_is_running:
            pos = pygame.mouse.get_pos()
            is_valid_move = verify_move(pos, player_turn)
            print(is_valid_move)
            if is_valid_move != -1:
                make_move(player_turn, is_valid_move)
                screen.fill((255, 255, 255))
                if max(table[player_turn]) == 0:
                    end_game(player_turn)
                    game_is_running = False
                draw_table(screen)
                draw_stones(table,store,screen)
                player_turn = 1 - player_turn
                print(store, int(opponent_type))
                if int(opponent_type) == 1:
                    move = random.randint(0,5)
                    while table[player_turn][move] == 0:
                        move = random.randint(0,5)
                    print(move)
                    make_move(player_turn, move)
                    screen.fill((255, 255, 255))
                    if max(table[player_turn]) == 0:
                        end_game(player_turn)
                        game_is_running = False
                    player_turn = 1 - player_turn
                    draw_table(screen)
                    draw_stones(table, store, screen)




    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()