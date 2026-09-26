"""Unmodified rule functions extracted from the original main.py.

Keep Taiwan mode; the renderer and AI must call these rules.
"""
rule = "Taiwan"
start3c = 1

def straight_taiwan_big(card_list, card_num):
    num_card = [0] * 13
    for i in range(0, card_num):
        num_card[card_list[i]//4] += 1
        if 3 == card_list[i]//4:
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
    if card_list[0]//4 != card_list[1]//4:
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
        card_number[card_list[i]//4] += 1
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
    elif card_number[card_list[0]//4] == 4 or card_number[card_list[1]//4] == 4:
        return 8000
    elif 1 == three_num and 1 == two_num:
        return 6000
    elif 5 == seq:
        return 5000
    else:
        return 0

def thirteen_card(card_list):
    #precondition: sort card
    c = card_list
    if c[0]%4 == c[1]%4 == c[2]%4 == c[3]%4 == c[4]%4 == c[5]%4 == c[6]%4 == c[7]%4 == c[8]%4 == c[9]%4 == c[10]%4 == c[11]%4 == c[12]%4 and 0 == c[0]//4 and 1 == c[1]//4 and 2 == c[2]//4 and 3 == c[3]//4 and 4 == c[4]//4 and 5 == c[5]//4 and 6 == c[6]//4 and 7 == c[7]//4 and 8 == c[8]//4 and 9 == c[9]//4 and 10 == c[10]//4 and 11 == c[11]//4 and 12 == c[12]//4:
        return 11000
    elif 0 == c[0]//4 and 1 == c[1]//4 and 2 == c[2]//4 and 3 == c[3]//4 and 4 == c[4]//4 and 5 == c[5]//4 and 6 == c[6]//4 and 7 == c[7]//4 and 8 == c[8]//4 and 9 == c[9]//4 and 10 == c[10]//4 and 11 == c[11]//4 and 12 == c[12]//4:
        return 10000
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
        if c4[0]//4 == list[i]//4 and i!=0:
            c4[j] = list[i]
            j += 1
        elif cother[0]//4 == list[i]//4 and i!=1:
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
        if c3[0]//4 == list[i]//4:
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
        if list[i]//4 == four_kind_card//4:
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
        elif 13 == org_len:
            if thirteen_card(put_card_list) == 11000:
                if thirteen_card(org_card_list) < 11000:
                    return 1
                elif thirteen_card(org_card_list) == 11000:
                    if one_card(org_card_list, 13) < one_card(put_card_list, 13):
                        return 1
                    else:
                        return -1
                else:
                    return -1
            elif thirteen_card(put_card_list) == 10000:
                if thirteen_card(org_card_list) < 10000:
                    return 1
                if thirteen_card(org_card_list) == 10000:
                    if one_card(org_card_list, 13) < one_card(put_card_list, 13):
                        return 1
                    else:
                        return -1
                else:
                    return -1
            else:
                return -1
        else:#impossible situation
            return -1
    elif 13 == put_len and thirteen_card(put_card_list) > 9000:
        return 1
    elif org_len < 13 and 5 == put_len and five_card(put_card_list) > 7000:
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
    elif 13 == put_len:
        if thirteen_card(put_card_list) > 0:
            if 1 == start3c:
                start3c = 0
            return 1
        else:
            return -1
    else:
        return -1

