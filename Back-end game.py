import numpy as np
from random import sample


def check_win(player_positions, winning_cond):
    if len(player_positions) < 3:
        return False

    for i in winning_cond:

        for j in i:
            if j not in player_positions:
                break
            if j == i[-1]:
                return True

    return False


board = {1: [2, 0], 2: [6, 0], 3: [10, 0], 4: [30, 0], 5: [34, 0], 6: [38, 0], 7: [58, 0], 8: [62, 0], 9: [66, 0]}

board_representation = '#   |   |   #\n#___________#\n#   |   |   #\n#___________#\n#   |   |   #'

print(len(board_representation))

winning_conditions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

player_pos = {0: [], 1: []}

play = True

#### complete enumeraton of state space

statespace = {}

playeable = [1, 2, 3, 4, 5, 6, 7, 8, 9]


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
            return [1, check_dict, 'Final']

    if len(playable) == 0:
        # if check_win(player_positions_copy[player_turn], winning_conditions):
        #     if player_turn == 0:
        #         return [-1]
        #     elif player_turn == 1:
        #         return [1]
        ### check win condition space.
        ### return a final possition space with value.
        return [0]

    if played is not None:
        player_turn = np.abs(player_turn - 1)

    index = 0
    for i in playable:
        to_play = playable[:index] + playable[(index + 1):len(playable)]
        recursion_dictionairy[i] = searchspace(to_play, player_positions_copy, player_turn, winning_conditions, i)
        value_sum += recursion_dictionairy[i][0]

        index += 1

    return [value_sum, recursion_dictionairy, check_dict]


state_space = searchspace(playeable, player_pos, 0, winning_conditions)

played_simmulation = {0:[],1:[]}
reveal = False
while play:

    prompt = 'Please play a position: \t'

    my_turn = True
    while my_turn:
        playe_me = int(input(prompt))

        index = 0
        for i in playeable:
            if i == playe_me:
                playeable = playeable[:index] + playeable[(index+1):]
                played_simmulation[0].append(playe_me)
                my_turn = False
                break
            if i == playeable[-1]:
                print('Invalid play try again\n')
                break
            index += 1
    ## cpu turn

    state_space = state_space[1][playe_me]

    candidate = [-100000,None]

    if check_win(played_simmulation[0],winning_conditions):
        print('Fuck u won')
        break


    for i in state_space[1]:
        print(i, state_space[1][i][0])

        if state_space[1][i][0] > candidate[0]:
            candidate = [state_space[1][i][0],i]

        elif state_space[1][i][0] == candidate[0]:
            candidate.append(i)


    if len(candidate) > 2:
        pick = sample(candidate[1:],1)
        candidate = [candidate[0],pick[0]]
    index = 0
    for i in playeable:
        if i == candidate[1]:
            playeable = playeable[:index] + playeable[(index + 1):]
            played_simmulation[1].append(candidate[1])
        index += 1
    print(played_simmulation)



    state_space = state_space[1][candidate[1]]

    print(candidate[1])
    if check_win(played_simmulation[1],winning_conditions):
        print('Fuck u I won')
        break

    if len(playeable) < 1:
        print('Fuck this its a draw')
        break




### dictioniary check



#
# while play:
#
#     for player in [1,2]:
#         player_symbol = ['X','O'][player-1]
#         print(board_representation)
#
#
#         print('Pick a spot')
#         prompt = 'Take a spot 1 through 9'
#         turn = int(input(prompt))
#
#         if turn < 0 or turn > 9:
#             print('postion out of bounds try again')
#         elif board[turn][1] == 0:
#             board[turn][1] = player
#             indexadd = board[turn][0] + 1
#             board_representation = board_representation[:board[turn][0]] + player_symbol + board_representation[indexadd:]
#             player_positions[player].append(turn)
#         else:
#             print('position already taken')
#         print('\n\n\n\n\n')
#         print(player_positions[1])
#         print(player_positions[2])
#
#         if check_win(player_positions[player],winning_conditions):
#             print('Congratulations you won')
#             play = False
#             print(board_representation)
#             break
#
#
#
#

#
# def searchspace_step(playable, player_positions, player_turn, winning_conditions, played=None):
#     # return dictionairy to check for called options
#
#     check_dict = {"playeables": playable, "player_pos": player_positions, "turn": player_turn,
#                   "wincod": winning_conditions, "player": played}
#
#     list_positions_zero = player_positions[0].copy()
#     list_positions_one = player_positions[1].copy()
#     player_positions_copy = {0: list_positions_zero, 1: list_positions_one}
#
#     if played is not None:
#
#         if player_turn == 0:
#             list_positions_zero.append(played)
#         else:
#             list_positions_one.append(played)
#
#     value_sum = 0
#
#     recursion_dictionairy = {}
#
#     print(player_positions_copy)
#     print(playable)
#     print(played)
#
#     #### check winning conditions given the previous step return either 1 or -1 when winning statement
#     if check_win(player_positions_copy[player_turn], winning_conditions):
#
#         if player_turn == 0:
#             return [-1]
#         elif player_turn == 1:
#             return [0.99]
#
#     if len(playable) == 0:
#         return [0]
#         ### check win condition space.
#         ### return a final possition space with value.
#
#     player_turn = np.abs(player_turn - 1)
#
#     index = 0
#     for i in playable:
#         to_play = playable[:index] + playable[(index + 1):len(playable)]
#         recursion_dictionairy[i] = searchspace(to_play, player_positions_copy, player_turn, winning_conditions, i)
#         value_sum += recursion_dictionairy[i][0]
#
#         index += 1
#
#     return [value_sum, recursion_dictionairy, check_dict]
#
#
#
#
#
#
# def check_win_step(player_positions,winning_cond):
#
#     if len(player_positions)<3:
#         return False
#
#     for i in winning_cond:
#         print(i)
#         for j in i:
#             print(j)
#             print(player_positions)
#             if j not in player_positions:
#                 break
#             if j == i[-1]:
#                 return True
#
#     return False

