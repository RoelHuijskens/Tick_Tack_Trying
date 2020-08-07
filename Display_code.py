import pygame as pg

SC_width = 500

SC_height = 500




### added stuf
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


answer_right = font_small.render("No",False,black)
answer_right_rect = answer_right.get_rect()
answer_right_rect.center = (loc_button[0]  + right_button_offset + width_text_button//2, loc_button[1] + height_text_button//2)


#loading_Screen

load_text = font_large.render("Loading game ...", False, white)
load_text_rect = load_text.get_rect()
load_text_rect.center = (SC_width//2, SC_height//2)





windo.fill((0,0,0))

play = True

##positison grid

vertical_pos = round((SC_width-6)/3)

horizontal_pos = round((SC_width-6)/3)

figure_positions_vertical = round(vertical_pos/8)

figure_positions_horizontal = round(horizontal_pos/8)

played = {}
player_turn = 0


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

        elif (loc_button[0] + right_button_offset) <  mouse_position[0] < (loc_button[0] + width_text_button + right_button_offset):
            background_button_right = grey

            if picked_start:
                input_screen = False
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

windo.fill((0,0,0))

windo.blit(load_text,load_text_rect)



### start_game

windo.fill((0,0,0))

while play:
    picked_spot = False
    for i in pg.event.get():


        if i.type == pg.QUIT:
            play = False

        if i.type == pg.MOUSEMOTION:
            print(i.dict['pos'])
            mouse_position = i.dict['pos']
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.dict['button'] == 1:
                picked_spot = True

    index = 0
    for f in [0,1,2]:
        ofsett_Horizontal = f * 2

        for j in [0,1,2]:
            ofsett_Vertical = j * 2
            print(played)
            color = True

            if mouse_position[0] > vertical_pos*j + ofsett_Horizontal and mouse_position[0] < vertical_pos*j + ofsett_Horizontal + horizontal_pos:
                if mouse_position[1] > horizontal_pos*f + ofsett_Vertical and mouse_position[1] < horizontal_pos*f + ofsett_Vertical + vertical_pos:
                    color = False
                    if picked_spot:
                        ##ofset left
                        ofl = vertical_pos*j + ofsett_Horizontal + figure_positions_horizontal
                        ofr = vertical_pos*j + ofsett_Horizontal + horizontal_pos - figure_positions_horizontal
                        oft = horizontal_pos*f + ofsett_Vertical + figure_positions_vertical
                        ofb = horizontal_pos*f + ofsett_Vertical + vertical_pos - figure_positions_vertical

                        played[index] = [player_turn,[ofl,ofr,oft,ofb]]
                        player_turn = abs(player_turn-1)


            if color:
                pg.draw.rect(windo, (255, 255, 255), [vertical_pos*j+ofsett_Vertical, horizontal_pos*f+ofsett_Horizontal,horizontal_pos, vertical_pos], 0)
            else:
                pg.draw.rect(windo, (220, 220, 220),
                             [vertical_pos * j + ofsett_Vertical, horizontal_pos * f + ofsett_Horizontal,
                              horizontal_pos, vertical_pos], 0)

            index += 1

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
                print(radius)

                pg.draw.circle(windo,(0,0,0),center,radius)
                pg.draw.circle(windo, (255, 255, 255), center, radius-1)

    pg.display.update()
