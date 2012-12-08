import random, os
import time 
import pygame
from pygame.locals import *
from sys import exit

background_image_filename = 'Image/Nostalgy.gif'
iP_1c = 'Image/01c.gif'
iP_1d = 'Image/01d.gif'
iP_1h = 'Image/01h.gif'
iP_1s = 'Image/01s.gif'
iP_2c = 'Image/02c.gif'
iP_2d = 'Image/02d.gif'
iP_2h = 'Image/02h.gif'
iP_2s = 'Image/02s.gif'
iP_3c = 'Image/03c.gif'
iP_3d = 'Image/03d.gif'
iP_3h = 'Image/03h.gif'
iP_3s = 'Image/03s.gif'
iP_4c = 'Image/04c.gif'
iP_4d = 'Image/04d.gif'
iP_4h = 'Image/04h.gif'
iP_4s = 'Image/04s.gif'
iP_5c = 'Image/05c.gif'
iP_5d = 'Image/05d.gif'
iP_5h = 'Image/05h.gif'
iP_5s = 'Image/05s.gif'
iP_6c = 'Image/06c.gif'
iP_6d = 'Image/06d.gif'
iP_6h = 'Image/06h.gif'
iP_6s = 'Image/06s.gif'
iP_7c = 'Image/07c.gif'
iP_7d = 'Image/07d.gif'
iP_7h = 'Image/07h.gif'
iP_7s = 'Image/07s.gif'
iP_8c = 'Image/08c.gif'
iP_8d = 'Image/08d.gif'
iP_8h = 'Image/08h.gif'
iP_8s = 'Image/08s.gif'
iP_9c = 'Image/09c.gif'
iP_9d = 'Image/09d.gif'
iP_9h = 'Image/09h.gif'
iP_9s = 'Image/09s.gif'
iP_10c = 'Image/10c.gif'
iP_10d = 'Image/10d.gif'
iP_10h = 'Image/10h.gif'
iP_10s = 'Image/10s.gif'
iP_11c = 'Image/11c.gif'
iP_11d = 'Image/11d.gif'
iP_11h = 'Image/11h.gif'
iP_11s = 'Image/11s.gif'
iP_12c = 'Image/12c.gif'
iP_12d = 'Image/12d.gif'
iP_12h = 'Image/12h.gif'
iP_12s = 'Image/12s.gif'
iP_13c = 'Image/13c.gif'
iP_13d = 'Image/13d.gif'
iP_13h = 'Image/13h.gif'
iP_13s = 'Image/13s.gif'
iP_pass = 'Image/pass.jpg'
iBack_Card = 'Image/back101.gif'

SCREEN_SIZE = (1280, 720) 
pygame.init()

pygame.display.set_icon(pygame.image.load("Image/simpybigtwo_default.png"))
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)#SCREEN_SIZE, FULLSCREEN, 32)
pygame.display.set_caption("Big Two")

background = pygame.image.load(background_image_filename).convert()
P_1c = pygame.image.load(iP_1c).convert()
P_1d = pygame.image.load(iP_1d).convert()
P_1h = pygame.image.load(iP_1h).convert()
P_1s = pygame.image.load(iP_1s).convert()
P_2c = pygame.image.load(iP_2c).convert()
P_2d = pygame.image.load(iP_2d).convert()
P_2h = pygame.image.load(iP_2h).convert()
P_2s = pygame.image.load(iP_2s).convert()
P_3c = pygame.image.load(iP_3c).convert()
P_3d = pygame.image.load(iP_3d).convert()
P_3h = pygame.image.load(iP_3h).convert()
P_3s = pygame.image.load(iP_3s).convert()
P_4c = pygame.image.load(iP_4c).convert()
P_4d = pygame.image.load(iP_4d).convert()
P_4h = pygame.image.load(iP_4h).convert()
P_4s = pygame.image.load(iP_4s).convert()
P_5c = pygame.image.load(iP_5c).convert()
P_5d = pygame.image.load(iP_5d).convert()
P_5h = pygame.image.load(iP_5h).convert()
P_5s = pygame.image.load(iP_5s).convert()
P_6c = pygame.image.load(iP_6c).convert()
P_6d = pygame.image.load(iP_6d).convert()
P_6h = pygame.image.load(iP_6h).convert()
P_6s = pygame.image.load(iP_6s).convert()
P_7c = pygame.image.load(iP_7c).convert()
P_7d = pygame.image.load(iP_7d).convert()
P_7h = pygame.image.load(iP_7h).convert()
P_7s = pygame.image.load(iP_7s).convert()
P_8c = pygame.image.load(iP_8c).convert()
P_8d = pygame.image.load(iP_8d).convert()
P_8h = pygame.image.load(iP_8h).convert()
P_8s = pygame.image.load(iP_8s).convert()
P_9c = pygame.image.load(iP_9c).convert()
P_9d = pygame.image.load(iP_9d).convert()
P_9h = pygame.image.load(iP_9h).convert()
P_9s = pygame.image.load(iP_9s).convert()
P_10c = pygame.image.load(iP_10c).convert()
P_10d = pygame.image.load(iP_10d).convert()
P_10h = pygame.image.load(iP_10h).convert()
P_10s = pygame.image.load(iP_10s).convert()
P_11c = pygame.image.load(iP_11c).convert()
P_11d = pygame.image.load(iP_11d).convert()
P_11h = pygame.image.load(iP_11h).convert()
P_11s = pygame.image.load(iP_11s).convert() 
P_12c = pygame.image.load(iP_12c).convert()
P_12d = pygame.image.load(iP_12d).convert()
P_12h = pygame.image.load(iP_12h).convert()
P_12s = pygame.image.load(iP_12s).convert() 
P_13c = pygame.image.load(iP_13c).convert()
P_13d = pygame.image.load(iP_13d).convert()
P_13h = pygame.image.load(iP_13h).convert()
P_13s = pygame.image.load(iP_13s).convert() 
Back_Card = pygame.image.load(iBack_Card).convert()
Back_Card90 = pygame.transform.rotate(Back_Card , 90)
Back_Cardn90 = pygame.transform.rotate(Back_Card , -90)
P_pass = pygame.image.load(iP_pass).convert()

rule = "Taiwan"

num_of_card     = 13
p2_num_of_card  = 13
p3_num_of_card  = 13
p4_num_of_card  = 13
start_turn = 1

card_clicked_list    = [0] * 13
p2_card_clicked_list = [0] * 13
p3_card_clicked_list = [0] * 13
p4_card_clicked_list = [0] * 13
player_card_list  = [0] * 13
player_card_rect  = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
p2_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
p3_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
p4_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
desktop_card_list = [0] * 5
desktop_card_rect = [[0,0], [0,0], [0,0], [0,0], [0,0]]
p2_card_list     = [0] * 13
p3_card_list     = [0] * 13
p4_card_list     = [0] * 13
all_card_list    = [0] * 52

org_player_card_x = SCREEN_SIZE[0]/2-4*P_1c.get_width()
player_card_x     = SCREEN_SIZE[0]/2-4*P_1c.get_width()
player_card_y     = 500
org_p2_card_y = 50 + P_1c.get_height()
p2_card_x     = SCREEN_SIZE[0]-5*Back_Card90.get_width()/2-10
p2_card_y     = 50 + P_1c.get_height()
org_p3_card_x = SCREEN_SIZE[0]/2-4*Back_Card.get_width()
p3_card_x     = SCREEN_SIZE[0]/2-4*Back_Card.get_width()
p3_card_y     = 50
org_p4_card_y = 50 + P_1c.get_height() 
p4_card_x     = Back_Cardn90.get_width()
p4_card_y     = 50 + P_1c.get_height()
org_display_card_x = SCREEN_SIZE[0]/2 - P_1c.get_width()/2
display_card_x     = SCREEN_SIZE[0]/2 - P_1c.get_width()/2
display_card_y     = 280

click_move_y =  30
put_card_alreay = 0
first_put       = 1
turn_id = 1
clicked = 0
start3c = 1

num_of_card     = 13
p2_num_of_card  = 13
p3_num_of_card  = 13
p4_num_of_card  = 13
num_of_desktop_card = 0

count_pass = 0
p_pass  = 0
p2_pass = 0
p3_pass = 0
p4_pass = 0

start_turn_id = turn_id
owner         = start_turn_id
screen_width, screen_height = SCREEN_SIZE

winner = 1

def handle_put(player_card_len):
    global first_put
    global card_clicked_list
    global desktop_card_list
    global num_of_desktop_card
    global player_card_list
    global start3c
    global owner
    put_card_list = [0]*13
    put_len = 0
    

    for ci in range(0, player_card_len):
        if 1 == card_clicked_list[ci]:
            put_card_list[put_len] = player_card_list[ci]
            put_len += 1
    
    if 5 == put_len and 0 == put_card_list[0]/4 and 1 == put_card_list[1]/4 and 2 == put_card_list[2]/4 and 3 == put_card_list[3]/4 and 12 == put_card_list[4]/4:
        t = put_card_list[4]
        for i in range(4, 0, -1):
            put_card_list[i] = put_card_list[i-1]
        put_card_list[0] = t
    
    if 1 == first_put:
        if 1 == valid_first_put_card(put_card_list, put_len):
            owner = 1
            num_of_desktop_card = put_len
            for ci in range(0, put_len):
                desktop_card_list[ci] = put_card_list[ci]
            for ci in range(0, player_card_len):
                if 1 == card_clicked_list[ci]:
                    #print 'ci=%d' % ci
                    card_clicked_list[ci] = 0
                    player_card_list[ci] = 100 #put card set to value 100
            player_card_list.sort()
            first_put = 0
            return put_len
        else:
            for ci in range(0, player_card_len):
                if 1 == card_clicked_list[ci]:
                    move_clicked_card([0,1],ci)
                    card_clicked_list[ci] = 0
            return 0
    else:
        if 1 == compare_card(desktop_card_list, num_of_desktop_card, put_card_list, put_len):
            owner = 1
            num_of_desktop_card = put_len
            for ci in range(0, put_len):
                desktop_card_list[ci] = put_card_list[ci]
            for ci in range(0, player_card_len):
                if 1 == card_clicked_list[ci]:
                    card_clicked_list[ci] = 0
                    player_card_list[ci] = 100 #put card set to value 100
            player_card_list.sort()
            return put_len
        else:
            for ci in range(0, player_card_len):
                if 1 == card_clicked_list[ci]:
                    move_clicked_card([0,1],ci)
                    card_clicked_list[ci] = 0
            return 0

def display_all():
    global put_card_alreay
    global player_card_x
    global player_card_rect
    global p3_card_x
    global p3_card_rect
    global display_card_x
    global desktop_card_rect
    
    fill_background()
    if 1 == put_card_alreay:              
        put_card_alreay = 0
        
        player_card_x = org_player_card_x+(13-num_of_card)*P_1c.get_width()/4 
        for x in range(0, num_of_card):
            player_card_rect[x][0] = player_card_x+x*P_1c.get_width()/2
            
        p3_card_x = org_p3_card_x + (13-p3_num_of_card)*Back_Card.get_width()/4
        for x in range(0, p3_num_of_card):
            p3_card_rect[x][0] = p3_card_x + x*Back_Card.get_width()/2
        
        display_card_x = org_display_card_x - num_of_desktop_card*P_1c.get_width()/2
        for x in range(0, num_of_desktop_card):
            desktop_card_rect[x][0] = display_card_x + x*P_1c.get_width()
    screen.blit(write("Left Button of Mouse"),(screen_width -250,screen_height - 200))
    screen.blit(write("=> Select Cards"), (screen_width -250,screen_height - 175))
    screen.blit(write("Right Button of Mouse"),(screen_width -250,screen_height - 150))
    screen.blit(write("=> Show Cards"),(screen_width -250,screen_height - 125))
    
    display_num_of_cards(player_card_list, num_of_card)
    display_p2_num_of_cards(p2_card_list, p2_num_of_card)
    display_p3_num_of_cards(p3_card_list, p3_num_of_card)
    display_p4_num_of_cards(p4_card_list, p4_num_of_card)
    display_desktop_cards(desktop_card_list, num_of_desktop_card)
    

def display_desktop_cards(list, num):
    for x in range(0, num):
        screen.blit(num_to_cards(list[x]), (desktop_card_rect[x][0], desktop_card_rect[x][1]))

def display_num_of_cards(list, num):
    for x in range(0, num):
        #print 'num=%d' % num
        #print num_to_cards(list[x])
        #print (player_card_rect[x][0], player_card_rect[x][1])
        screen.blit(num_to_cards(list[x]), (player_card_rect[x][0], player_card_rect[x][1]))
    return
    
def display_p2_num_of_cards(list, num):
    for x in range(0, num):
        screen.blit(Back_Card90, (p2_card_rect[x][0], p2_card_rect[x][1]))
    return

def display_p3_num_of_cards(list, num):
    for x in range(0, num):
        screen.blit(Back_Card, (p3_card_rect[x][0], p3_card_rect[x][1]))
    return

def display_p4_num_of_cards(list, num):
    for x in range(0, num):
        screen.blit(Back_Cardn90, (p4_card_rect[x][0], p4_card_rect[x][1]))
    return

def ini_random_cards(p_card_list, p_id):
    global all_card_list
    global turn_id
    for x in range(0, 13):
        start = random.randint(0, 51)
        i = start
        while i != -1 :
            if 0 == all_card_list[start]:
                if i != 0:
                    start += 1
                    start %= 52
                    i -= 1
                else:
                    break
            else:
                start += 1
                start %= 52
        if 4 == start:
            turn_id = p_id
        all_card_list[start] = 1
        p_card_list[x] = start
    return p_card_list
        
def num_to_cards(num):
    if 0==num:
        return P_2c
    if 1==num:
        return P_2d
    if 2==num:
        return P_2h
    if 3==num:
        return P_2s
    if 4==num:
        return P_3c
    if 5==num:
        return P_3d 
    if 6==num:
        return P_3h
    if 7==num:
        return P_3s
    if 8==num:
        return P_4c
    if 9==num:
        return P_4d
    if 10==num:
        return P_4h
    if 11==num:
        return P_4s
    if 12==num:
        return P_5c
    if 13==num:
        return P_5d
    if 14==num:
        return P_5h
    if 15==num:
        return P_5s
    if 16==num:
        return P_6c
    if 17==num:
        return P_6d
    if 18==num:
        return P_6h
    if 19==num:
        return P_6s
    if 20==num:
        return P_7c
    if 21==num:
        return P_7d
    if 22==num:
        return P_7h
    if 23==num:
        return P_7s
    if 24==num:
        return P_8c
    if 25==num:
        return P_8d
    if 26==num:
        return P_8h
    if 27==num:
        return P_8s
    if 28==num:
        return P_9c
    if 29==num:
        return P_9d
    if 30==num:
        return P_9h
    if 31==num:
        return P_9s
    if 32==num:
        return P_10c
    if 33==num:
        return P_10d
    if 34==num:
        return P_10h
    if 35==num:
        return P_10s
    if 36==num:
        return P_11c
    if 37==num:
        return P_11d
    if 38==num:
        return P_11h
    if 39==num:
        return P_11s
    if 40==num:
        return P_12c
    if 41==num:
        return P_12d
    if 42==num:
        return P_12h
    if 43==num:
        return P_12s
    if 44==num:
        return P_13c
    if 45==num:
        return P_13d
    if 46==num:
        return P_13h
    if 47==num:
        return P_13s
    if 48==num:
        return P_1c
    if 49==num:
        return P_1d
    if 50==num:
        return P_1h
    if 51==num:
        return P_1s

def write(msg="pygame is cool", color= (0,0,0)):    
    #myfont = pygame.font.SysFont("None", 32) #To avoid py2exe error
    myfont = pygame.font.Font("FreeSansBold.ttf",14)
    mytext = myfont.render(msg, True, color)
    mytext = mytext.convert_alpha()
    return mytext        

def fill_background():
    for y in range(0, screen_height, background.get_height()):
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, y))
    
def move_clicked_card(speed, card_index):
    global player_card_rect
    global num_of_card
    org_y = player_card_rect[card_index][1]
    while abs(player_card_rect[card_index][1] - org_y) <= click_move_y:
        #print 'click card'
        player_card_rect[card_index][0] += speed[0]
        player_card_rect[card_index][1] += speed[1]
        display_num_of_cards(player_card_list, num_of_card)
    
def handle_click_card( mouse_x, mouse_y):   
    global card_clicked_list
    #global num_of_card
    
    for i in range(0, num_of_card):
        if player_card_x + i * P_1c.get_width()/2 <= mouse_x < player_card_x + (i+1) * P_1c.get_width()/2:
            if 0 == card_clicked_list[i]:
                #unclicked the click card
                if player_card_y <= mouse_y < player_card_y+P_1c.get_height():
                    move_clicked_card([0,-1], i)
                    card_clicked_list[i] = 1
            elif 1 == card_clicked_list[i]:
                #clicked then unclick card
                if player_card_y-click_move_y <= mouse_y < player_card_y+P_1c.get_height()-click_move_y:
                    move_clicked_card([0,1], i)
                    card_clicked_list[i] = 0
    ii = i
    i += 1
    if player_card_x + i * P_1c.get_width()/2 <= mouse_x < player_card_x + (i+1) * P_1c.get_width()/2:
            if 0 == card_clicked_list[ii]:
                #unclicked the click card
                if player_card_y <= mouse_y < player_card_y+P_1c.get_height():
                    move_clicked_card([0,-1], ii)
                    card_clicked_list[ii] = 1
            elif 1 == card_clicked_list[ii]:
                #clicked then unclick card
                if player_card_y-click_move_y <= mouse_y < player_card_y+P_1c.get_height()-click_move_y:
                    move_clicked_card([0,1], ii)
                    card_clicked_list[ii] = 0

def straight_taiwan_big(card_list, card_num):
    num_card = [0] * 13
    for i in range(0, card_num):
        num_card[card_list[i]/4] += 1
        if 3 == card_list[i]/4:
            sc = card_list[i]
    if 1 == num_card[0] and 1 == num_card[1] and 1 == num_card[2] and 1 == num_card[3] and 1 == num_card[12]:
        return sc
    else:
        return one_card(card_list, card_num)
                    
def one_card(card_list, card_num):
    big_card_score = 0
    for i in range(0, card_num):
        if 0 == card_list[i]:
            score = 52
        elif 1 == card_list[i]:
            score = 53
        elif 2 == card_list[i]:
            score = 54
        elif 3 == card_list[i]:
            score = 55
        else:
            score = card_list[i]
        if score > big_card_score:
           big_card_score = score
           #print 'big score=%d' % big_card_score
    return big_card_score

def two_card(card_list):
    if card_list[0]/4 != card_list[1]/4:
        return 0
    else:
        return one_card(card_list, 2)
    
def five_card(card_list):
    card_number = [0]*13
    same_color_num  =  1
    color       =  0
    first       =  0
    seq         =  0
    seq_start   =  0
    three_num    =  0
    two_num  =  0
    #check sequence number and same color
    for i in range(0, 5):
        card_number[card_list[i]/4] += 1
        if 0 == first:
            color = card_list[i]%4
            first = 1
        elif card_list[i]%4 == color:
            same_color_num += 1
    
    first = 0
    for i in range(0,13):
        if 1 == card_number[i]:
            if 0 == first:
                seq_start = i
                seq = 1
                first = 1
            elif i == seq_start+1:
                seq_start += 1
                seq += 1
            #else:pass
    if 1 == card_number[12] and 1 == card_number[0] and 1 == card_number[1] and 1 == card_number[2] and 1 == card_number[3]:
        seq = 5
    for i in range(0,13):
        if 3 == card_number[i]:
            three_num = 1
        elif 2 == card_number[i]:
            two_num = 1
    if 5 == seq and  5 == same_color_num:
        return 9000
    #check 4 color in same number
    elif card_number[card_list[0]/4] == 4 or card_number[card_list[1]/4] == 4:
        return 8000
    elif 1 == three_num and 1 == two_num:
        return 6000
    elif 5 == seq:
        return 5000
    else:
        return 0

def fk_big(list):
    c4 = [0] * 5
    cother = [0] * 5
    c4[0] = list[0]
    cother[0] = list[1]
    j = 1
    jj = 1
    for i in range(0, 5):
        if c4[0]/4 == list[i]/4 and i!=0:
            c4[j] = list[i]
            j += 1
        elif cother[0]/4 == list[i]/4 and i!=1:
            cother[jj] = list[i]
            jj += 1
    if 4 == j:
        return one_card(c4, 4)
    else: # 4 == jj
        return one_card(cother, 4)

def full_house_big(list):
    c2 = [0] * 5
    c3 = [0] * 5
    c3[0] = list[0]
    j = 1
    jj = 0
    for i in range(1, 5):
        if c3[0]/4 == list[i]/4:
            c3[j] = list[i]
            j += 1
        else:
            c2[jj] = list[i]
            jj += 1
    if 3 == j:
        return one_card(c3, 3)
    else: # 3 == jj
        return one_card(c2, 3)

def four_kind_small_card(four_kind_card, list, list_len):
    small_card = 0
    small_index_card = 0
    first            = 1
    for i in range(0, list_len):
        if list[i]/4 == four_kind_card/4:
            continue
        elif 1 == first:
            small_card = list[i]
            small_index_card = i
            first = 0
        # 0 == first
        elif one_card([small_card], 1) > one_card([list[i]], 1):
            small_card = list[i]
            small_index_card = i
    
    return small_index_card
        
def compare_card( org_card_list, org_len, put_card_list, put_len):
    if org_len == put_len:
        #print 'Same number of card'
        if 1 == org_len:
            if one_card(org_card_list, 1) < one_card(put_card_list, 1):
                return 1
            else:
                return -1
        elif 2 == org_len:
            if two_card(org_card_list) < two_card(put_card_list):
                return 1
            else:
                return -1
        elif 5 == org_len:
            if five_card(put_card_list) == 9000:
                #print 'Super Card'
                if five_card(org_card_list) < 9000:
                    return 1
                elif rule == "Taiwan_China":
                    if five_card(org_card_list)+one_card(org_card_list, 5) < five_card(put_card_list)+one_card(put_card_list, 5):
                        return 1
                    else:
                        return -1
                elif rule == "Taiwan":
                    if five_card(org_card_list)+straight_taiwan_big(org_card_list, 5) < five_card(put_card_list)+straight_taiwan_big(put_card_list, 5):
                        return 1
                    else:
                        return -1
            elif five_card(put_card_list) == 8000:
                #print 'Super Card2'
                if 9000 == five_card(org_card_list):
                    return -1
                elif 8000 == five_card(org_card_list):
                    if five_card(org_card_list)+fk_big(org_card_list) < five_card(put_card_list)+fk_big(put_card_list):
                        return 1
                else:
                    return 1
            elif five_card(org_card_list) == 6000: #five_card(put_card_list)<7000
                if 6000 == five_card(put_card_list):
                    if five_card(org_card_list)+full_house_big(org_card_list) < five_card(put_card_list)+full_house_big(put_card_list):
                        return 1
                    else:
                        return -1
                else:
                    return -1
            elif five_card(org_card_list) == 5000:
                if 5000 == five_card(put_card_list):
                    if rule == "Taiwan_China":
                        if five_card(org_card_list)+one_card(org_card_list, 5) < five_card(put_card_list)+one_card(put_card_list, 5):
                            return 1
                        else:
                            return -1
                    elif rule == "Taiwan":
                        if five_card(org_card_list)+straight_taiwan_big(org_card_list, 5) < five_card(put_card_list)+straight_taiwan_big(put_card_list, 5):
                            return 1
                        else:
                            return -1
                else:
                    return -1
            else:
            # It seems org card is super card
                return -1
        else:#impossible situation
            return -1
    elif 5 == put_len and five_card(put_card_list) > 7000:
        return 1
        #print 'Super Card'
    else:
        return -1#put card small than orginal card

def valid_first_put_card(put_card_list, put_len):
    global start3c
    s3c = 1 
    if 1 == start3c:
        for i in range(0, put_len):
            if 4 == put_card_list[i]:
                s3c = 0
        if 1 == s3c:
            return -1
    if 1 == put_len:
        if one_card(put_card_list, 1) > 0:
            if 1 == start3c:
                start3c = 0
            return 1
        else:
            return -1
    elif 2 == put_len:
        if two_card(put_card_list) > 0:
            if 1 == start3c:
                start3c = 0
            return 1
        else:
            return -1
    elif 5 == put_len:
        if five_card(put_card_list) > 0:
            if 1 == start3c:
                start3c = 0
            return 1
        else:
            return -1
    else:
        return -1

def straight_flush(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    for i in range(0, card_len-4):
        put_card_list[0] = card_list[i]
        card_index_list[0]  = i
        put_len = 1
        for j in range(i+1, card_len):
            if put_card_list[put_len-1]/4 + 1 == card_list[j]/4 and put_card_list[put_len-1]%4 == card_list[j]%4:
                put_card_list[put_len] = card_list[j]
                card_index_list[put_len] = j
                put_len += 1
            elif 4 == put_len and (card_list[j]/4 + 1) % 13 == put_card_list[0] and put_card_list[0]%4 == card_list[j]%4:
                put_card_list[4] = put_card_list[3]
                card_index_list[4] = card_index_list[3]
                put_card_list[3] = put_card_list[2]
                card_index_list[3] = card_index_list[2]
                put_card_list[2] = put_card_list[1]
                card_index_list[2] = card_index_list[1]
                put_card_list[1] = put_card_list[0]
                card_index_list[1] = card_index_list[0]
                put_card_list[0] = card_list[j]
                card_index_list[0] = j
                put_len = 5
            if 5 == put_len:
                if  func == valid_first_put_card:
                    if  1 == func(put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
                elif func == compare_card:
                    if 1 == func(org_card_list, org_card_len, put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
                break
    return put_card_list, card_index_list, put_len, cpass

def four_kind(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    other_small_index = 0    
    put_len           = 0
    four_kind_n       = 0
    
    if card_len > 5:
        for i in range(0, card_len-3):
            if card_list[i]/4 == card_list[i+1]/4 == card_list[i+2]/4 == card_list[i+3]/4:
                put_card_list[0] = card_list[i]
                put_card_list[1] = card_list[i+1]
                put_card_list[2] = card_list[i+2]
                put_card_list[3] = card_list[i+3]
                card_index_list[:4] = [i, i+1, i+2, i+3]
                four_kind_n = card_list[i+3]                    
                other_small_index = four_kind_small_card(four_kind_n, card_list, card_len)
                put_card_list[4] = card_list[other_small_index]
                card_index_list[4] = other_small_index
                put_len = 5
                if func == valid_first_put_card:
                    if  1 == func(put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
                elif func == compare_card:
                    if 1 == func(org_card_list, org_card_len, put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
                    
    return put_card_list, card_index_list, put_len, cpass

def one(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    small_card = card_list[0]
    small_card_index = 0
    for i in range(0, card_len):
        if one_card([small_card], 1) > one_card([card_list[i]], 1):
            small_card = card_list[i]
            small_card_index = i
    for i in range(0, card_len):
        put_card_list[0]   = small_card 
        card_index_list[0] = small_card_index
        put_len            = 1
        if func == valid_first_put_card:
            if 1 == func(put_card_list, put_len):
                cpass = 0
                return put_card_list, card_index_list, put_len, cpass
        elif func == compare_card:
            if 1 == func(org_card_list, org_card_len, put_card_list, put_len):
                cpass = 0
                return put_card_list, card_index_list, put_len, cpass
        small_card_index += 1
        small_card_index %= card_len
        small_card = card_list[small_card_index]
    return put_card_list, card_index_list, put_len, cpass
    
def full_house(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    small_i         = 0
    small_i = small_one(card_list, card_len)
    for i in range(small_i, small_i+card_len-2):
        i = i % card_len
        if card_list[i]/4 == card_list[(i+1)%card_len]/4 == card_list[(i+2)%card_len]/4:
            put_card_list[0] = card_list[i]
            card_index_list[0] = i
            put_card_list[1] = card_list[i+1]
            card_index_list[1] = i+1
            put_card_list[2] = card_list[i+2]
            card_index_list[2] = i+2
            put_len = 3
            for j in range(small_i, small_i+card_len-1):
                j = j % card_len
                if j == card_index_list[0] or j == card_index_list[1] or j == card_index_list[2]:
                    continue
                elif card_list[j]/4 == card_list[(j+1)% card_len]/4:
                    put_card_list[3] = card_list[j]
                    card_index_list[3] = j
                    put_card_list[4] = card_list[j+1]
                    card_index_list[4] = j+1
                    put_len = 5
                    if func == valid_first_put_card:
                        if 1 == func(put_card_list, put_len):
                            cpass = 0
                            return put_card_list, card_index_list, put_len, cpass
                    elif func == compare_card:
                        if 1 == func(org_card_list, org_card_len, put_card_list, put_len):
                            cpass = 0
                            return put_card_list, card_index_list, put_len, cpass
    return put_card_list, card_index_list, put_len, cpass

def straight(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    for i in range(0, card_len-4):
        put_card_list[0] = card_list[i]
        card_index_list[0] = i
        for i2 in range(i+1, card_len-3):
            put_len = 1
            if put_card_list[0]/4 + 1 < card_list[i2]/4:
                break
            elif put_card_list[0]/4 + 1 == card_list[i2]/4:
                put_card_list[1] = card_list[i2]
                card_index_list[1] = i2
                for i3 in range(i2+1, card_len-2):
                    put_len = 2
                    if put_card_list[1]/4 + 1 < card_list[i3]/4:
                        break
                    elif put_card_list[1]/4 + 1 == card_list[i3]/4:
                        put_card_list[2] = card_list[i3]
                        card_index_list[2] = i3                                
                        for i4 in range(i3+1, card_len-1):
                            put_len = 3
                            if put_card_list[2]/4 + 1 < card_list[i4]/4:
                                break
                            elif put_card_list[2]/4 + 1 == card_list[i4]/4:
                                put_card_list[3] = card_list[i4]
                                card_index_list[3] = i4
                                for i5 in range(i4+1, card_len):
                                    put_len = 4
                                    if (card_list[i5]/4 + 1) % 13 == put_card_list[0] or put_card_list[3]/4 + 1 == card_list[i5]/4:
                                        if (card_list[i5]/4 + 1) % 13 == put_card_list[0]:
                                            put_card_list[4] = put_card_list[3]
                                            card_index_list[4] = card_index_list[3]
                                            put_card_list[3] = put_card_list[2]
                                            card_index_list[3] = card_index_list[2]
                                            put_card_list[2] = put_card_list[1]
                                            card_index_list[2] = card_index_list[1]
                                            put_card_list[1] = put_card_list[0]
                                            card_index_list[1] = card_index_list[0]
                                            put_card_list[0] = card_list[i5]
                                            card_index_list[0] = i5
                                            put_len = 5
                                        else:    
                                            put_card_list[4] = card_list[i5]
                                            card_index_list[4] = i5
                                            put_len = 5
                                        if func ==  valid_first_put_card:
                                            if 1 == func(put_card_list, put_len):
                                                cpass = 0
                                                return put_card_list, card_index_list, put_len, cpass
                                        elif func == compare_card:
                                            if  1 == func(org_card_list, org_card_len, put_card_list, put_len):
                                                cpass = 0
                                                return put_card_list, card_index_list, put_len, cpass
    return put_card_list, card_index_list, put_len, cpass

def pair(card_list, card_len, func, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    small_i     = 0
    
    small_i = small_one(card_list, card_len)
    
    put_len = 1
    for i in range(small_i, small_i+card_len-1):
        for j in range(i+1, small_i+card_len):
            i = i%card_len
            j = j%card_len
            if card_list[i]/4 == card_list[j]/4:
                put_card_list[0] = card_list[i]
                card_index_list[0] = i
                put_card_list[1] = card_list[j]
                card_index_list[1] = j
                put_len = 2
                if func == valid_first_put_card:
                    if  1 == func(put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
                elif func == compare_card:
                    if  1 == func(org_card_list, org_card_len, put_card_list, put_len):
                        cpass = 0
                        return put_card_list, card_index_list, put_len, cpass
    return put_card_list, card_index_list, put_len, cpass

def small_one(card_list, card_len):
    small_card = card_list[0]
    small_card_index = 0
    for i in range(0, card_len):
        if one_card([small_card], 1) > one_card([card_list[i]], 1):
            small_card = card_list[i]
            small_card_index = i
    return small_card_index
    
#return put_card_list, card_index_list, put_len, cpass
def strategy(card_list, card_len, fp = 1, org_card_list = [0, 0, 0, 0, 0], org_card_len = 0):
    cpass = 1
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    if 1 == fp:
        if 1 == start3c:
            # four kind
            put_card_list, card_index_list, put_len, cpass = four_kind(card_list, card_len, valid_first_put_card)
            num = [0] * 13
            for a in put_card_list:
                num[a/4] += 1
            if 0 == cpass and 4 == num[1]:
                return put_card_list, card_index_list, put_len, cpass
            #end four kind
        if card_len > 6:
            put_card_list, card_index_list, put_len, cpass = full_house(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass                
            #straight                
            put_card_list, card_index_list, put_len, cpass = straight(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass    
            #end straight
            
            #pair
            put_card_list, card_index_list, put_len, cpass = pair(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass    
            #end pair
            put_card_list, card_index_list, put_len, cpass = one(card_list, card_len, valid_first_put_card)
            
        elif 6 == card_len or 5 == card_len:
            put_card_list, card_index_list, put_len, cpass = straight_flush(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass             
            # four kind
            put_card_list, card_index_list, put_len, cpass = four_kind(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end four kind
            put_card_list, card_index_list, put_len, cpass = full_house(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #straight                
            put_card_list, card_index_list, put_len, cpass = straight(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end straight
            #pair
            put_card_list, card_index_list, put_len, cpass = pair(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end pair
            put_card_list, card_index_list, put_len, cpass = one(card_list, card_len, valid_first_put_card)
            
        elif card_len >= 2:
            #pair
            put_card_list, card_index_list, put_len, cpass = pair(card_list, card_len, valid_first_put_card)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end pair
            put_card_list, card_index_list, put_len, cpass = one(card_list, card_len, valid_first_put_card)
            
        else:
            put_card_list, card_index_list, put_len, cpass = one(card_list, card_len, valid_first_put_card)
    else:
        if org_card_len == 5:
            #cpass == 1
            put_card_list, card_index_list, put_len, cpass = full_house(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #straight 
            put_card_list, card_index_list, put_len, cpass = straight(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end straight
            
            # four kind
            put_card_list, card_index_list, put_len, cpass = four_kind(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end four kind
            
            put_card_list, card_index_list, put_len, cpass = straight_flush(card_list, card_len, compare_card, org_card_list, org_card_len)
            # return put_card_list, card_index_list, put_len, cpass
            
        elif 2 == org_card_len:
            #pair
            put_card_list, card_index_list, put_len, cpass = pair(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end pair
            
            # four kind
            put_card_list, card_index_list, put_len, cpass = four_kind(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end four kind
            
            put_card_list, card_index_list, put_len, cpass = straight_flush(card_list, card_len, compare_card, org_card_list, org_card_len)
            #return put_card_list, card_index_list, put_len, cpass
            
        else: #org_card_len = 1
            put_card_list, card_index_list, put_len, cpass = one(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            
            # four kind
            put_card_list, card_index_list, put_len, cpass = four_kind(card_list, card_len, compare_card, org_card_list, org_card_len)
            if 0 == cpass:
                return put_card_list, card_index_list, put_len, cpass
            #end four kind
            put_card_list, card_index_list, put_len, cpass = straight_flush(card_list, card_len, compare_card, org_card_list, org_card_len)
                    
    return put_card_list, card_index_list, put_len, cpass
        
        
def ai():
    global turn_id
    global count_pass
    global p2_pass
    global p3_pass
    global p4_pass
    global p2_card_list
    global p2_num_of_card
    global p3_card_list
    global p3_num_of_card
    global p4_card_list
    global p4_num_of_card
    global first_put
    global desktop_card_list
    global num_of_desktop_card
    global owner
    
    
    cpass = 0
    put_card_list   = [0] * 5
    card_index_list = [0] * 5
    put_len         = 0
    
    if 2 ==turn_id:
        if 1 == p2_pass:
            turn_id += 1
            return 0
        else:
            if 1 == first_put:
                put_card_list, card_index_list, put_len, cpass = strategy(p2_card_list, p2_num_of_card)
                #cpass can't be 1
                for i in range(0, put_len):
                    p2_card_list[card_index_list[i]] = 100
                    desktop_card_list[i] = put_card_list[i]
                p2_num_of_card -= put_len
                num_of_desktop_card = put_len
                p2_card_list.sort()
                first_put = 0
                time.sleep(1)
                return 1
            elif owner == turn_id:
                turn_id += 1
                return 0
            else:
                put_card_list, card_index_list, put_len, cpass = strategy(p2_card_list, p2_num_of_card, 0, desktop_card_list, num_of_desktop_card)
                if 0 == cpass:
                    for i in range(0, put_len):
                        p2_card_list[card_index_list[i]] = 100
                        desktop_card_list[i] = put_card_list[i]
                    p2_num_of_card -= put_len
                    num_of_desktop_card = put_len
                    p2_card_list.sort()
                    owner = 2
                    time.sleep(1)
                    return 1
                else:
                    p2_pass = 1
                    count_pass += 1
                    return 0
    elif 3 == turn_id:
        if 1 == p3_pass:
            turn_id += 1
            return 0
        else:
            if 1 == first_put:
                put_card_list, card_index_list, put_len, cpass = strategy(p3_card_list, p3_num_of_card)
                #cpass can't be 1
                for i in range(0, put_len):
                    p3_card_list[card_index_list[i]] = 100
                    desktop_card_list[i] = put_card_list[i]
                p3_num_of_card -= put_len
                num_of_desktop_card = put_len
                p3_card_list.sort()
                first_put = 0
                time.sleep(1)
                return 1
            elif owner == turn_id:
                turn_id += 1
                return 0
            else:
                put_card_list, card_index_list, put_len, cpass = strategy(p3_card_list, p3_num_of_card, 0, desktop_card_list, num_of_desktop_card)
                if 0 == cpass:
                    for i in range(0, put_len):
                        p3_card_list[card_index_list[i]] = 100
                        desktop_card_list[i] = put_card_list[i]
                    p3_num_of_card -= put_len
                    num_of_desktop_card = put_len
                    p3_card_list.sort()
                    owner = 3
                    time.sleep(1)
                    return 1
                else:
                    p3_pass = 1
                    count_pass += 1
                    return 0
    elif 4 == turn_id:
        if 1 == p4_pass:
            turn_id = 1
            return 0
        else:
            if 1 == first_put:
                put_card_list, card_index_list, put_len, cpass = strategy(p4_card_list, p4_num_of_card)
                #cpass can't be 1
                for i in range(0, put_len):
                    p4_card_list[card_index_list[i]] = 100
                    desktop_card_list[i] = put_card_list[i]
                p4_num_of_card -= put_len
                num_of_desktop_card = put_len
                p4_card_list.sort()
                first_put = 0
                time.sleep(1)
                return 1
            elif owner == turn_id:
                turn_id = 1
                return 0
            else:
                put_card_list, card_index_list, put_len, cpass = strategy(p4_card_list, p4_num_of_card, 0, desktop_card_list, num_of_desktop_card)
                if 0 == cpass:
                    for i in range(0, put_len):
                        p4_card_list[card_index_list[i]] = 100
                        desktop_card_list[i] = put_card_list[i]
                    p4_num_of_card -= put_len
                    num_of_desktop_card = put_len
                    p4_card_list.sort()
                    owner = 4
                    time.sleep(1)
                    return 1
                else:
                    p4_pass = 1
                    count_pass += 1
                    return 0
    else:
        return 0

def main(loop_num = -1):

    global num_of_card     
    global p2_num_of_card  
    global p3_num_of_card  
    global p4_num_of_card  
    global start_turn 

    global card_clicked_list    
    global p2_card_clicked_list 
    global p3_card_clicked_list 
    global p4_card_clicked_list 
    global player_card_list 
    global player_card_rect 
    global p2_card_rect     
    global p3_card_rect     
    global p4_card_rect     
    global desktop_card_list
    global desktop_card_rect
    global p2_card_list     
    global p3_card_list     
    global p4_card_list     
    global all_card_list    
    
    global org_player_card_x 
    global player_card_x     
    global player_card_y     
    global org_p2_card_y 
    global p2_card_x     
    global p2_card_y     
    global org_p3_card_x 
    global p3_card_x     
    global p3_card_y     
    global org_p4_card_y 
    global p4_card_x     
    global p4_card_y     
    global org_display_card_x 
    global display_card_x     
    global display_card_y     
    
    global click_move_y 
    global put_card_alreay 
    global first_put       
    global turn_id 
    global clicked 
    global start3c 
    
    global num_of_card     
    global p2_num_of_card  
    global p3_num_of_card  
    global p4_num_of_card  
    global num_of_desktop_card 
    
    global count_pass
    global p_pass  
    global p2_pass 
    global p3_pass 
    global p4_pass
    
    global start_turn_id 
    global owner         
    global screen_width, screen_height
    
    global winner
    
    if loop_num > 0:
        loop_number = loop_num
    else:
        loop_number = 1
    
    while loop_number > 0:
        if 1 == start_turn:
            card_clicked_list    = [0] * 13
            p2_card_clicked_list = [0] * 13
            p3_card_clicked_list = [0] * 13
            p4_card_clicked_list = [0] * 13
            player_card_list  = [0] * 13
            player_card_rect  = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
            p2_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
            p3_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
            p4_card_rect      = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
            desktop_card_list = [0] * 5
            desktop_card_rect = [[0,0], [0,0], [0,0], [0,0], [0,0]]
            p2_card_list     = [0] * 13
            p3_card_list     = [0] * 13
            p4_card_list     = [0] * 13
            all_card_list    = [0] * 52

            org_player_card_x = SCREEN_SIZE[0]/2-4*P_1c.get_width()
            player_card_x     = SCREEN_SIZE[0]/2-4*P_1c.get_width()
            player_card_y     = 500
            org_p2_card_y = 50 + P_1c.get_height()
            p2_card_x     = SCREEN_SIZE[0]-5*Back_Card90.get_width()/2-10
            p2_card_y     = 50 + P_1c.get_height()
            org_p3_card_x = SCREEN_SIZE[0]/2-4*Back_Card.get_width()
            p3_card_x     = SCREEN_SIZE[0]/2-4*Back_Card.get_width()
            p3_card_y     = 50
            org_p4_card_y = 50 + P_1c.get_height() 
            p4_card_x     = Back_Cardn90.get_width()
            p4_card_y     = 50 + P_1c.get_height()
            org_display_card_x = SCREEN_SIZE[0]/2 - P_1c.get_width()/2
            display_card_x     = SCREEN_SIZE[0]/2 - P_1c.get_width()/2
            display_card_y     = 280

            click_move_y =  30
            put_card_alreay = 0
            first_put       = 1
            turn_id = 1
            clicked = 0
            start3c = 1

            num_of_card     = 13
            p2_num_of_card  = 13
            p3_num_of_card  = 13
            p4_num_of_card  = 13
            num_of_desktop_card = 0

            count_pass = 0
            p_pass  = 0
            p2_pass = 0
            p3_pass = 0
            p4_pass = 0
            
            random.seed()
            p4_card_list = ini_random_cards(p4_card_list, 4)
            p3_card_list = ini_random_cards(p3_card_list, 3)
            p2_card_list = ini_random_cards(p2_card_list, 2)
            player_card_list = ini_random_cards(player_card_list, 1)
            p2_card_list.sort()
            p3_card_list.sort()
            p4_card_list.sort()
            
            start_turn_id = turn_id
            owner         = start_turn_id

            screen.blit(background, (0,0))
             
            screen_width, screen_height = SCREEN_SIZE
             
            for i in range(0, 13): 
                player_card_rect[i][1] = player_card_y
                player_card_rect[i][0] = player_card_x+i*P_1c.get_width()/2
                p2_card_rect[i][1]     = p2_card_y+i*Back_Card90.get_height()/4
                p2_card_rect[i][0]     = p2_card_x
                p3_card_rect[i][1]     = p3_card_y
                p3_card_rect[i][0]     = p3_card_x+i*Back_Card.get_width()/2
                p4_card_rect[i][1]     = p4_card_y+i*Back_Cardn90.get_height()/4
                p4_card_rect[i][0]     = p4_card_x
                #print (num_to_cards_rect(player_card_list[i])[0], num_to_cards_rect(player_card_list[i])[1])
                #print (player_card_rect[i][0], player_card_rect[i][1])

            for i in range(0,5):
                desktop_card_rect[i][1] = display_card_y

            start_turn = 0
			
            display_all()
            pygame.display.update()
            time.sleep(1)
            player_card_list.sort()
        
        #print 'turn_id=%d, first_put=%d, owner=%d' % (turn_id, first_put, owner)
        #for i in range(0, num_of_desktop_card):
        #    print "[%d]=%d" % (i, desktop_card_list[i])
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and turn_id == 1:
                    handle_click_card(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    #print 'left button'
                if event.button == 3 and turn_id == 1:
                    if 1 == owner and 0 == first_put:
                        turn_id += 1
                        continue
                    for i in range (0, num_of_card):
                        if 1 == card_clicked_list[i]:
                            clicked = 1
                    if 0 == clicked and 0 == first_put:
                        p_pass = 1
                        count_pass += 1
                        turn_id = 2
                        display_all()
                        pygame.display.update()
                        time.sleep(1)
                        continue
                    clicked = 0
                    p_len = handle_put(num_of_card)
                    if  p_len > 0:
                        for i in range(0, 13): 
                            player_card_rect[i][1] = player_card_y
                        num_of_card -= p_len
                        put_card_alreay = 1
                        turn_id = 2
                        display_all()
                        pygame.display.update()
                        #time.sleep(1)
                    #print 'right button'                
                    
        if 1 == turn_id and 1 == p_pass:
            turn_id = 2
        
        if 0 == num_of_card:
            winner = 1
            start_turn = 1
            if loop_num > 0:
                loop_number -= 1
        elif 0 == p2_num_of_card:
            winner = 2
            start_turn = 1
            if loop_num > 0:
                loop_number -= 1
        elif 0 == p3_num_of_card:
            winner = 3
            start_turn = 1
            if loop_num > 0:
                loop_number -= 1
        elif 0 == p4_num_of_card:
            winner = 4
            start_turn = 1
            if loop_num > 0:
                loop_number -= 1
            
        display_all()
        
        if num_of_card != 0 and p2_num_of_card != 0 and p3_num_of_card != 0 and p4_num_of_card != 0:
            if 1 == ai(): 
                put_card_alreay = 1 
        
        if 1 == p_pass:
            #screen.blit(write("Pass", (0, 0, 255)), (screen_width/2-50, 550))
            screen.blit(P_pass, (screen_width/2-50, 550))            
        if 1 == p2_pass:
            #screen.blit(write("Pass", (0, 0, 255)), (p2_card_x+40, screen_height/2-65))
            screen.blit(P_pass, (p2_card_x+40, screen_height/2-65))
        if 1 == p3_pass:
            #screen.blit(write("Pass", (0, 0, 255)), (screen_width/2-50, 100))
            screen.blit(P_pass, (screen_width/2-50, 100))
        if 1 == p4_pass:
            #screen.blit(write("Pass", (0, 0, 255)), (p4_card_x+40, screen_height/2-65))
            screen.blit(P_pass, (p4_card_x+40, screen_height/2-65))
        
        if 3 == count_pass:
            count_pass = 0
            p_pass  = 0
            p2_pass = 0
            p3_pass = 0
            p4_pass = 0
            num_of_desktop_card = 0
            first_put = 1
            turn_id = owner
            pygame.display.update()
            time.sleep(1)
        pygame.display.update()
    
    exit()
		
if __name__ == "__main__":
    main()
    