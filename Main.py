import numpy as np
from random import sample


def check_win(player_positions,winning_cond,give_Winning_list = False):
    """
    Takes the current state of the game and returns wether or not a winning position has been played




    """
    if len(player_positions)<3: # impossible to win under 3 moves
        if give_Winning_list:
            return [False]
        else:
            return False

    for i in winning_cond:  # next we will check for each possible winning condition whether its positions are present
                            # in a players play_positions.

        for j in i:
            if j not in player_positions:  # Check wether or not the necessary given winning position is present in the
                                            # player position. If true, break to next winning combination
                break
            if j == i[-1]:  # Once the end of a winning condition is reached without breaking the loop, the game has
                            # been won by the current active player.
                if give_Winning_list:
                    return [True, i]
                else:
                    return True


    if give_Winning_list:  # if call is reached a winnign position has not been found for all winning cnditions.
        return [False]
    return False


# here we will describe what position (if presented in 1 players play history) will result in a win

winning_conditions = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]

# player_pos is the dictioniary of moves played by player 1 and 2.

player_pos = {0:[],1:[]}

play = True



statespace  =  {}

playeable = [1,2,3,4,5,6,7,8,9]  # all playeable options at start of the game.

def searchspace(playable, player_positions, player_turn, winning_conditions, played=None):
    # return dictionairy to check for called options

    check_dict = {"playeables": playable, "turn": player_turn,
                  "wincod": winning_conditions, "player": played}

    list_positions_zero = player_positions[0].copy()
    list_positions_one = player_positions[1].copy()
    player_positions_copy = {0: list_positions_zero, 1: list_positions_one}

    check_dict["player_positions"] = player_positions_copy

    if played is not None:

        if player_turn == 0:
            list_positions_zero.append(played)
        else:
            list_positions_one.append(played)

    value_sum = 0

    recursion_dictionairy = {}
    #### check winning conditions given the previous step return either 1 or -1 when winning statement
    if check_win(player_positions_copy[player_turn], winning_conditions):
        if player_turn == 0:
            return [-1, check_dict, "Final"]
        elif player_turn == 1:
            return [0.98, check_dict, 'Final']

    if len(playable) == 0:
        # if check_win(player_positions_copy[player_turn], winning_conditions):
        #     if player_turn == 0:
        #         return [-1]
        #     elif player_turn == 1:
        #         return [1]
        ### check win condition space.
        ### return a final possition space with value.
        return [-0.001]

    if played is not None:
        player_turn = np.abs(player_turn - 1)

    index = 0
    for i in playable:
        to_play = playable[:index] + playable[(index + 1):len(playable)]
        recursion_dictionairy[i] = searchspace(to_play, player_positions_copy, player_turn, winning_conditions, i)
        value_sum += recursion_dictionairy[i][0]

        index += 1

    return [value_sum, recursion_dictionairy, check_dict]










import pygame as pg

SC_width = 500

SC_height = 500

windo = pg.display.set_mode((SC_width,SC_height))
pg.display.set_caption("Tic Tac Toe")
pg.font.init()
font_large = pg.font.SysFont('arial',16)
font_small = pg.font.SysFont('arial',11)



white = (255, 255, 255)
black = (0, 0, 0)
grey = (220, 220, 220)

width_text_button = 60
height_text_button = 15
loc_button = [150,300]

right_button_offset = (int(round(SC_width // 2, 0)) - loc_button[0])*2 - width_text_button
print(right_button_offset)
print(int(round(SC_width // 2, 0)))


### main message

text = font_large.render("Welcome, would you like to have the first turn?",False,black)
text_Rect = text.get_rect()
text_Rect.center = (SC_width // 2, SC_height // 2 + 20)


answer_left = font_small.render("Yes",False,black)
answer_left_rect = answer_left.get_rect()
answer_left_rect.center = (loc_button[0] + width_text_button//2, loc_button[1] + height_text_button//2)
windo.blit(answer_left,answer_left_rect)

answer_right = font_small.render("No",False,black)
answer_right_rect = answer_right.get_rect()
answer_right_rect.center = (loc_button[0]  + right_button_offset + width_text_button//2, loc_button[1] + height_text_button//2)
windo.blit(answer_right,answer_right_rect)



#loading_Screen

load_text = font_large.render("Loading game ...", False, white)
load_text_rect = load_text.get_rect()
load_text_rect.center = (SC_width//2, SC_height//2)



## startup screen

input_screen = True

picked_start = False

while input_screen:
    pg.draw.rect(windo,white,(50,150, 400,200))


    for i in pg.event.get():

        if i.type == pg.QUIT:
            play = False

        if i.type == pg.MOUSEMOTION:
            mouse_position = i.dict['pos']
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.dict['button'] == 1:
                picked_start = True



    if loc_button[1] <  mouse_position[1] < (loc_button[1] + height_text_button):
        if loc_button[0] <  mouse_position[0] < (loc_button[0] + width_text_button):
            background_button_left = grey

            if picked_start:
                input_screen = False
                start_player = 0

        elif (loc_button[0] + right_button_offset) <  mouse_position[0] < (loc_button[0] + width_text_button + right_button_offset):
            background_button_right = grey

            if picked_start:
                input_screen = False
                start_player = 1

        else:
            background_button_left = background_button_right = white

    else:
        background_button_left = background_button_right = white

    pg.draw.rect(windo, (0, 0, 0),
                 (loc_button[0] - 1, loc_button[1] - 1, width_text_button + 2, height_text_button + 2))
    pg.draw.rect(windo, background_button_left, (loc_button[0], loc_button[1], width_text_button, height_text_button))

    pg.draw.rect(windo, (0, 0, 0), (
    loc_button[0] - 1 + right_button_offset, loc_button[1] - 1, width_text_button + 2, height_text_button + 2))
    pg.draw.rect(windo, background_button_right,
                 (loc_button[0] + right_button_offset, loc_button[1], width_text_button, height_text_button))


    #print messages

    windo.blit(text, text_Rect)
    windo.blit(answer_left, answer_left_rect)
    windo.blit(answer_right, answer_right_rect)

    pg.display.update()






### loading _game

windo.fill((0,0,0))

windo.blit(load_text,load_text_rect)
pg.display.update()
state_space = searchspace(playeable,player_pos, start_player, winning_conditions)

##start_game


windo.fill((0,0,0))

play = True

##positison grid

vertical_pos = round((SC_width-6)/3)

horizontal_pos = round((SC_width-6)/3)

figure_positions_vertical = round(vertical_pos/8)

figure_positions_horizontal = round(horizontal_pos/8)


# positions lists
position_list = []

for i in range(0,3):
    ofsett_Horizontal = i * 2
    for j in range(0,3):
        ofsett_Vertical = j * 2

        ofl = vertical_pos * j + ofsett_Horizontal + figure_positions_horizontal
        ofr = vertical_pos * j + ofsett_Horizontal + horizontal_pos - figure_positions_horizontal
        oft = horizontal_pos * i + ofsett_Vertical + figure_positions_vertical
        ofb = horizontal_pos * i + ofsett_Vertical + vertical_pos - figure_positions_vertical
        position_list.append([ofl,ofr,oft,ofb])


played = {}
player_turn = start_player
playe_me = None

while play:
    picked_spot = False
    for i in pg.event.get():


        if i.type == pg.QUIT:
            play = False

        if i.type == pg.MOUSEMOTION:
            mouse_position = i.dict['pos']
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.dict['button'] == 1:
                picked_spot = True


    index = 0
    for f in [0,1,2]:
        ofsett_Horizontal = f * 2

        for j in [0,1,2]:
            ofsett_Vertical = j * 2

            color = True

            if mouse_position[0] > vertical_pos*j + ofsett_Horizontal and mouse_position[0] < vertical_pos*j + ofsett_Horizontal + horizontal_pos:
                if mouse_position[1] > horizontal_pos*f + ofsett_Vertical and mouse_position[1] < horizontal_pos*f + ofsett_Vertical + vertical_pos:
                    color = False
                    if picked_spot:
                        index_2 = 0
                        playe_me = index + 1
                        for i in playeable:
                            if i == playe_me:
                                playeable = playeable[:index_2] + playeable[(index_2 + 1):]
                                player_pos[0].append(playe_me)
                                ##ofset left


                                played[playe_me] = [player_turn, position_list[playe_me-1]]

                                player_turn = abs(player_turn - 1)
                                print(playeable)
                                break

                            elif len(playeable) == 1:
                                print('check')
                                playeable
                            elif i == playeable[-1]:
                                print('Invalid play try again\n')
                            index_2 += 1
            index += 1


            if color:
                pg.draw.rect(windo, (255, 255, 255), [vertical_pos*j+ofsett_Vertical, horizontal_pos*f+ofsett_Horizontal,horizontal_pos, vertical_pos], 0)
            else:
                pg.draw.rect(windo, (220, 220, 220),
                             [vertical_pos * j + ofsett_Vertical, horizontal_pos * f + ofsett_Horizontal,
                              horizontal_pos, vertical_pos], 0)



    if len(played) > 0:



        for i in played:
            if played[i][0] == 0:
                figure_played = played[i]

                begin_first = [figure_played[1][0],figure_played[1][2]]
                end_first = [figure_played[1][1],figure_played[1][3]]
                pg.draw.line(windo,(0,0,0),begin_first,end_first,1)

                begin_second = [figure_played[1][1],figure_played[1][2]]
                end_second = [figure_played[1][0],figure_played[1][3]]
                pg.draw.line(windo, (0, 0, 0), begin_second, end_second,1)
            elif played[i][0] == 1:
                x = played[i][1][1] - played[i][1][0]
                y = played[i][1][3] - played[i][1][2]
                center = [round(x/2)+played[i][1][0],round(y/2)+played[i][1][2]]
                radius =  vertical_pos- figure_positions_vertical*2
                radius = round(radius/2)


                pg.draw.circle(windo,(0,0,0),center,radius)
                pg.draw.circle(windo, (255, 255, 255), center, radius-1)



    if player_turn == 1:

        if playe_me is not None:
            state_space = state_space[1][playe_me]

        candidate = [-100000, None]

        if check_win(player_pos[0], winning_conditions,True)[0]:
            Winner = check_win(player_pos[0], winning_conditions, True)[0]
            break

        for i in state_space[1]:


            if state_space[1][i][0] > candidate[0]:
                candidate = [state_space[1][i][0], i]

            elif state_space[1][i][0] == candidate[0]:
                candidate.append(i)

        if len(candidate) > 2:
            pick = sample(candidate[1:], 1)
            candidate = [candidate[0], pick[0]]
        index = 0
        for i in playeable:
            print(i)
            print(state_space[1][i][0])
            print("+++++++++")

            if i == candidate[1]:
                playeable = playeable[:index] + playeable[(index + 1):]
                player_pos[1].append(candidate[1])
                played[candidate[1]] = [player_turn, position_list[candidate[1]-1]]
                player_turn = abs(player_turn-1)
            index += 1


        state_space = state_space[1][candidate[1]]

    pg.display.update()

    if check_win(player_pos[1], winning_conditions,True)[0]:
        Winner = check_win(player_pos[1], winning_conditions,True)[1]
        break


    if len(playeable) < 1:
        print('Its ts a draw')
        break






index = 0
for f in [0,1,2]:
    ofsett_Horizontal = f * 2

    for j in [0,1,2]:
        ofsett_Vertical = j * 2

        color = True

        if mouse_position[0] > vertical_pos*j + ofsett_Horizontal and mouse_position[0] < vertical_pos*j + ofsett_Horizontal + horizontal_pos:
            if mouse_position[1] > horizontal_pos*f + ofsett_Vertical and mouse_position[1] < horizontal_pos*f + ofsett_Vertical + vertical_pos:
                color = False
                if picked_spot:
                    index_2 = 0
                    playe_me = index + 1
                    for i in playeable:
                        if i == playe_me:
                            playeable = playeable[:index_2] + playeable[(index_2 + 1):]
                            player_pos[0].append(playe_me)
                            ##ofset left


                            played[playe_me] = [player_turn, position_list[playe_me-1]]

                            player_turn = abs(player_turn - 1)
                            print(playeable)
                            break

                        elif len(playeable) == 1:
                            print('check')
                            playeable
                        elif i == playeable[-1]:
                            print('Invalid play try again\n')
                        index_2 += 1
        index += 1

        if index not in Winner:
            pg.draw.rect(windo, (255, 255, 255), [vertical_pos*j+ofsett_Vertical, horizontal_pos*f+ofsett_Horizontal,horizontal_pos, vertical_pos], 0)
        else:
            pg.draw.rect(windo, (220, 220, 220),
                         [vertical_pos * j + ofsett_Vertical, horizontal_pos * f + ofsett_Horizontal,
                          horizontal_pos, vertical_pos], 0)


        for i in played:
            if played[i][0] == 0:
                figure_played = played[i]

                begin_first = [figure_played[1][0],figure_played[1][2]]
                end_first = [figure_played[1][1],figure_played[1][3]]
                pg.draw.line(windo,(0,0,0),begin_first,end_first,1)

                begin_second = [figure_played[1][1],figure_played[1][2]]
                end_second = [figure_played[1][0],figure_played[1][3]]
                pg.draw.line(windo, (0, 0, 0), begin_second, end_second,1)
            elif played[i][0] == 1:
                x = played[i][1][1] - played[i][1][0]
                y = played[i][1][3] - played[i][1][2]
                center = [round(x/2)+played[i][1][0],round(y/2)+played[i][1][2]]
                radius =  vertical_pos- figure_positions_vertical*2
                radius = round(radius/2)

                pg.draw.circle(windo, (0, 0, 0), center, radius)

                if i not in Winner:
                    pg.draw.circle(windo, (255, 255, 255), center, radius-1)
                else:
                    pg.draw.circle(windo, (220, 220, 220), center, radius - 1)

pg.display.update()
pg.time.delay(5000)



