#   15/09/2022 Review of old versions

import csv
import random

from datetime import datetime


# App start greeting:
def greeting(user_name, _user_bank):
    print('Wellcome to CyberJACK!\n')
    print(f'{user_name}: {_user_bank}$')
    print(f'\nBet: {_user_bet}$')
    print()


def show_menu():
    print('\n____ MENU ____')
    print('0 - Show Menu')
    print('1 - Play Round!')
    print('2 - Change Bet')
    print('3 - Show Account Info')    
    print('4 - Show Statistics')
    print('5 - "Get Five!" (mini-game) ')    
    print('6 - Change Nickname')
    
    print('\n00 - Show Extended Menu')
    print('01 - Show Game Rules')
    
    print('\n9 - Exit') 


def show_extended_menu():
    print('\n____EXTENDED MENU ____')    
    print('11 - Get 1 Random Card')
    print('55 - Get 5 Random Cards')
    print('22 - Get a Few Nums of Random Cards')    
    print('33 - Drop Random Cards Hand\n')

    print('98 - Show deck_list')    
    print('99 - Show Cards Deck')


def show_rules():
    with open("app_data\\game_rules.txt", "r") as file:
        for message in file:
            print(message, end="")
        


#  User's Name Request:
def name_request():
    user_name = input('Enter your Nickname>>>')
    
    if user_name == '': user_name = 'UserName'

    with open("user_data\\user_name.txt", "w") as file:
        file.write(user_name)
       
    return user_name



def init_user_data():
    with open("user_data\\user_name.txt", "r") as file:
        init_user_name = file.readline()
    with open("user_data\\_user_bank.txt", "r") as file:
        init_user_bank = file.readline()
        init_user_bank = int(init_user_bank)
        
    now = datetime.now()
    now_datatime = now.strftime("%d/%m/%Y %H:%M:%S")
    
    _user_bank_reports = f'{now_datatime}_user_bank inited!\n'
    _user_bank_reports += f'_user_bank_balance: {init_user_bank}$\n'
    #print(_user_bank_reports)
    with open("reports\\_user_bank_reports.txt", "a") as file:
        file.write(_user_bank_reports)

    return init_user_name, init_user_bank


def deck_init():
    with open('app_data\\cards_data_df.csv', "r",  encoding='utf-8' ) as file:
        reader = csv.reader(file)

        deck_list = []

        for row in reader:
            row[1] = row[1].replace('\ufeff', '')
            deck_list.append([row[1],row[2]])

    return deck_list


def deck_show(deck_list):
    for i in range(1 , len(deck_list)+1):
        print(f'#{i}: {deck_list[i-1][0]} - {deck_list[i-1][1]}')
        if i % 4 == 0: print()
        
        #print(deck_list)


#  Random Cards mini-game:
def drop_user_hand():
    global user_hand, except_nums_list, ai_hand 
    user_hand = []
    except_nums_list = []

    ai_hand = []
    return  user_hand



def get_random_card(sel_num):
    global random_card_deck, random_card_hand

    if len(random_card_deck) == 0:
        print('The Deck of Random Cards is empty!')
        return

    elif sel_num > len(random_card_deck):
        sel_num = len(random_card_deck)

    for i in range(sel_num):
        random_num_card = random.randint(0,len(random_card_deck)-1)
        random_card_hand.append(random_card_deck[random_num_card])
        r = random_card_deck[random_num_card]
        random_card_deck.remove(r)

    show_random_cards(random_card_hand)

    
def show_random_cards(random_card_hand):
    for i in random_card_hand:
       print(i[0],  end=' ')
    print()
    r_score = 0
    for i in random_card_hand:
       r_score += int(i[1])

    print('Score:', r_score)



#   Get ONE Card:
def get_card(user_hand):
    global except_nums_list
    
    num = random.randint(0,51)
  
    while num in except_nums_list:
        num = random.randint(0,51)

    except_nums_list.append(num)
    #print(except_nums_list)
    
    
    user_hand.append(deck_list[num])

    user_hand_signs = ''
    user_hand_score = 0
    
    for i in  user_hand:
        user_hand_signs +=  i[0] + ' '
        user_hand_score += int(i[1])

    print('User hand:',user_hand_signs)    
    print('UserScore:',user_hand_score)


    if len(user_hand) == 2:
        #print('AI must get his Card NOW!')
        #print('ai_hand:',ai_hand)
        num = random.randint(0,51)
        while num in except_nums_list:
            num = random.randint(0,51)

        except_nums_list.append(num)
        ai_hand.append(deck_list[num])

        
    ai_hand_signs = ''
    ai_hand_score = 0
    
    for i in ai_hand:
        ai_hand_signs +=  i[0] + ' '
        ai_hand_score += int(i[1])


    print('ai_hand:', ai_hand_signs)
    print('ai_score:', ai_hand_score)    
    print()
    
    res = score_check(user_hand_score)
    
    #print('res:', res)

    

    if res == 'ok' and len(user_hand) >= 2 :
        
        answer = input('HIT or STAND -> ')

        if answer == '1':
            print('HIT')
            get_card(user_hand)

        elif answer == '5':
            
            print('RESTART GAME:')
            result_game()
            new_game()
            
            
        else:
            print('STAND')
            print('ai_hand get one more card')
            ai_hand_get_card(user_hand_score)


    if res == 'lose' or res == 'jack':
        result_game()
    
    
    pass



def ai_hand_get_card(user_hand_score):
    global ai_hand, except_nums_list
    

    ai_hand_signs = ''
    ai_hand_score = 0    

    for i in ai_hand:
        ai_hand_signs +=  i[0] + ' '
        ai_hand_score += int(i[1])

    
    
    while ai_hand_score < 21 and ai_hand_score < user_hand_score:
    
        num = random.randint(0,51)
        while num in except_nums_list:
            num = random.randint(0,51)

        except_nums_list.append(num)

        ai_hand.append(deck_list[num])

            
        ai_hand_signs = ''
        ai_hand_score = 0
        
        for i in ai_hand:
            ai_hand_signs +=  i[0] + ' '
            ai_hand_score += int(i[1])


        print('ai_hand:', ai_hand_signs)
        print('ai_score:', ai_hand_score)


    result_game()
        


def result_game():
    global user_hand, _user_bank

    user_hand_signs = ''    
    user_hand_score = 0
    
    for i in user_hand:
        user_hand_signs += i[0] + ' '
        user_hand_score += int(i[1])

        
    ai_hand_signs = ''
    ai_hand_score = 0    

    for i in ai_hand:
        ai_hand_signs +=  i[0] + ' '
        ai_hand_score += int(i[1])

    
    print('\nRESULT:')
    print(f'{user_name} vs AI')
    print( f'{user_hand_signs} vs {ai_hand_signs}')
    print(f'{user_hand_score} vs {ai_hand_score}')

    res_game = '...'
    res_protocol = '...'


    if user_hand_score > 21:
        print('You lose!')
        res_protocol = 'User Overhited'
        res_game = 'Lose'
        add_bet_status(res_game) # Your Bet was losed 
        bet_res = f'Lose Bet! -{_user_bet}$'
        
    elif user_hand_score == 21:
        print('\nCYBERJACK!\n')
        res_protocol = 'User Jack'
        res_game = 'WinJack'
        add_bet_status(res_game)
        winjack_bet() # add to balance Bat + 500% of Bet     
        bet_res = f'Jack Bet! +{_user_bet*5}$'
        
    elif ai_hand_score > 21 :
        print('You Win!')
        res_protocol = 'AI Overhited'
        res_game = 'Win'
        add_bet_status(res_game)
        win_bet() # add to balance Bat + 100% of Bet 
        bet_res = f'Win Bet! +{_user_bet*2}$'
        
    elif ai_hand_score == 21 :
        print('You Lose! AI has CyberJack!')
        res_protocol = 'AI Jack'
        res_game = 'LoseJack'
        add_bet_status(res_game)
        losejack_bet() # from balance minus  -200% of Bet  
        bet_res = f'Lose Jack! -{_user_bet*2}$'
        
    elif ai_hand_score > user_hand_score :
        print('You lose!')
        res_protocol = 'AI Raced'
        res_game = 'Lose'
        add_bet_status(res_game) # Your Bet was losed  
        bet_res = f'Lose Bet! -{_user_bet}$'
        
    elif ai_hand_score == user_hand_score :
        print('Equal Points!')
        res_protocol = 'Equal Points'
        res_game = 'Draw'
        add_bet_status(res_game)
        draw_bet() # add to balance 60% of Bet 
        bet_res = f'Draw Bet! +{round(_user_bet*0.6)}$'
        
        

    user_hand = drop_user_hand()
    #print('User Hand is Empty!' if user_hand == [] else 'not')
    
    print(f'{user_hand_score} vs {ai_hand_score} -> {res_protocol}')
    print(bet_res)
    print(f'_user_bank: {_user_bank}$')



    #       PROCESSING DATA FOR reports.txt :        |    
    add_to_report = '\n'
    add_to_report += f'user_name: {user_name}\n'
    add_to_report += f'{user_hand_signs}\n'
    add_to_report += f'{user_hand_score}\n'
    add_to_report += f'{ai_hand_signs}\n'
    add_to_report += f'{ai_hand_score}\n'
    add_to_report += res_protocol + '\n'
    add_to_report += res_game + '\n'

    add_report(add_to_report)
 

def score_check(user_hand_score):
    response = ''
    
    s = user_hand_score
    
    if s > 21:
        response = 'lose'
    elif s == 21:
        response = 'jack'
    else:
        response = 'ok'
        
    return(response)


def new_game():
    global run_flag, user_name, _user_bank, user_hand, ai_hand, except_nums_list, shuffled_deck
        
    user_hand = []
    ai_hand = []
    except_nums_list = []

    #print(user_hand)        
    #print(ai_hand)


    #print('Get 1 card:')
    get_card(user_hand)

    #print('Get 1 card:')
    get_card(user_hand)


#           BET:          |
def make_bet():
    global _user_bet
    
    print('_user_bet:', _user_bet)
    print('_user_bank:', _user_bank)
    
    _user_bet = input('Make your Bet please>>>')

    try:
        _user_bet = int(_user_bet)
        print('_user_bet INPUT:', _user_bet) 
    except:
        print('Denied: INVALID INPUT!')
        return


def debit_bet(_user_bet):
    global _user_bank 
    
    balance_check = _user_bank - _user_bet

    now = datetime.now()
    now_datatime = now.strftime("%d/%m/%Y %H:%M:%S")
        
    if balance_check < 0:
        print('Denied: Insufficient funds!')
        
        _user_bank_reports = f'\n\n{now_datatime}_user_bet Denied!\n'
        _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'
        
        with open("reports\\_user_bank_reports.txt", "a") as file:
            file.write(_user_bank_reports)
        
        return False
    
    else:
      
        _user_bank_reports = f'\n\n{now_datatime}_user_bet Accepted!\n'
        _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'


        _user_bank = _user_bank - _user_bet


        _user_bank_reports += f'_user_bet: {_user_bet}$\n'

        with open("user_data\\_user_bank.txt", "w") as file:
            file.write(str(_user_bank))

        _user_bank_reports += f'_user_bank: -{_user_bet}$\n'
        _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'

        with open("reports\\_user_bank_reports.txt", "a") as file:
            file.write(_user_bank_reports)
            #print(_user_bank_reports)

        print(f'_user_bet: {_user_bet}$')                
        print('Your Bet is accepted!')
        print(f'_user_bank: {_user_bank}$')
        return True   


def win_bet():
    global _user_bank
    _user_bank_reports = f'_user_bank_balance: {_user_bank}$\n'
    
    _win_bet = _user_bet * 2
    
    _user_bank = _user_bank + _win_bet
    
    _user_bank_reports += f'_user_bet: {_user_bet}$\n'
    _user_bank_reports += f'_win_bet: {_user_bet} * 2 = {_win_bet}$\n'
    _user_bank_reports += f'_user_bank: +{_win_bet}$\n'
    _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'

    #print(_user_bank_reports)

    with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
        file.write(_user_bank_reports)
        
    
def winjack_bet():
    global _user_bank
    _user_bank_reports = f'_user_bank_balance: {_user_bank}$\n'
    
    _win_bet = _user_bet * 6
    
    _user_bank = _user_bank + _win_bet
    
    _user_bank_reports += f'_user_bet: {_user_bet}$\n'
    _user_bank_reports += f'_win_bet: {_user_bet} * 6 = {_win_bet}$\n'
    _user_bank_reports += f'_user_bank: +{_win_bet}$\n'
    _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'

    #print(_user_bank_reports)

    with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
        file.write(_user_bank_reports)


def losejack_bet():
    global _user_bank
    _user_bank_reports = f'_user_bank_balance: {_user_bank}$\n'
    
    _lose_bet = _user_bet * 2
    
    _user_bank = _user_bank - _lose_bet
    
    _user_bank_reports += f'_user_bet: {_user_bet}$\n'
    _user_bank_reports += f'_lose_bet: {_user_bet} * 2 = {_lose_bet}$\n'
    _user_bank_reports += f'_user_bank: -{_lose_bet}$\n'
    _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'
    #print(_user_bank_reports)

    with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
        file.write(_user_bank_reports)


def draw_bet():
    global _user_bank
    _user_bank_reports = f'_user_bank_balance: {_user_bank}$\n'
    
    _draw_bet = _user_bet * 0.6
    _draw_bet = int(round(_draw_bet))

    _user_bank = _user_bank + _draw_bet
    
    _user_bank_reports += f'_user_bet: {_user_bet}$\n'
    _user_bank_reports += f'_draw_bet: {_user_bet} * 0.6 = {_draw_bet}$\n'
    _user_bank_reports += f'_user_bank: +{_draw_bet}$\n'
    _user_bank_reports += f'_user_bank_balance: {_user_bank}$\n'

    #print(_user_bank_reports)

    with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
        file.write(_user_bank_reports)


def get_five_game():
        global _user_bank

        now = datetime.now()
        now_datatime = now.strftime("%d/%m/%Y %H:%M:%S")

        get_five_check = _user_bank - 50

        if get_five_check < 0:
            add_to_report = f'\n\n{now_datatime} get_five: Denied!\n'
            return
        else:        
            add_to_report = f'\n\n{now_datatime} get_five: Accepted!\n'
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            add_to_report += f'_user_bank: -50$\n'            
            _user_bank -= 50
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            
            with open("user_data\\_user_bank.txt", "w") as file:
                file.write(str(_user_bank)) 
            
        with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
            file.write(add_to_report)
            
        print(f'_user_bank: -50$')
        print(f'_user_bank: {_user_bank}$')
        
        five_card_deck = deck_list[:]
        five_card_hand = []
        
        for i in range(5):
            random_num_card = random.randint(0,51)
            five_card_hand.append(five_card_deck[random_num_card])
 
        sum_five = 0
        print()
        for i in five_card_hand:
            print(i[0],end=' ')
            sum_five += int(i[1])

        print(f'\n\nScore: -={sum_five}=- -',end=' ')

        if sum_five >= 50:
            print('You gotta FIVE! +500$')
            add_to_report = f'\n\n{now_datatime} get_five: Win!\n'
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            add_to_report += f'_user_bank: +500$\n'
            _user_bank += 500
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            
            with open("user_data\\_user_bank.txt", "w") as file:
                file.write(str(_user_bank))                 
            
            with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
                file.write(add_to_report)
                
            print(f'_user_bank: {_user_bank}$')

        elif sum_five in range(45,49):
            print('Just a little more!')
            add_to_report = f'\n\n{now_datatime} get_five: Just!\n'
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            add_to_report += f'_user_bank: +50$\n'
            _user_bank += 50
            add_to_report += f'_user_bank_balance: {_user_bank}$\n'
            
            with open("user_data\\_user_bank.txt", "w") as file:
                file.write(str(_user_bank))                
            
            with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
                file.write(add_to_report)
            print(f'_user_bank: +50$')                
            print(f'_user_bank: {_user_bank}$')

        else:
            print('Not enough! \nTry more FIVE!')

            add_to_report = f'\n\n{now_datatime} get_five: Lose!\n'            
            with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
                file.write(add_to_report)

                

#              REPORTS:              |

def add_bet_status(bet_status):
    now = datetime.now()
    now_datatime = now.strftime("%d/%m/%Y %H:%M:%S")
        
    bet_status = f'\n{now_datatime}_user_bet: {bet_status}!\n'
    
    #print(bet_status)
    
    with open("reports\\_user_bank_reports.txt", "a", encoding='utf-8') as file:
        file.write(bet_status)    


def add_report(add_to_report):
    with open("reports\\game_reports.txt", "a", encoding='utf-8') as file:
        file.write(add_to_report)
        
    print('Reported to .txt!')


def statistic_report():
        wins_count = 0
        lose_count = 0
        draw_count = 0
        skip_count = 0
        with open("reports\\game_reports.txt", "r", encoding='utf-8') as file:
            
            for i in file:
                if i == 'Win\n':
                    #print(i, end ='')
                    wins_count += 1
                elif i == 'WinJack\n':
                    #print(i, end ='')
                    wins_count += 1
                elif i == 'Lose\n':
                    #print(i, end ='')
                    lose_count += 1                    
                elif i == 'LoseJack\n':
                    #print(i, end ='')
                    lose_count += 1
                elif i == 'Draw\n':
                    #print(i, end ='')
                    draw_count += 1
                elif i == '...\n':
                    #print(i, end ='')
                    skip_count += 1


            total_rounds = wins_count + lose_count + draw_count + skip_count
            
            now = datetime.now()
            now_datatime = now.strftime("%d/%m/%Y %H:%M:%S")
            
            print(now_datatime)
            print('______________________')
            
            print('Total Rounds:', total_rounds)
            print()
            
            wins_percent = round(wins_count/total_rounds * 100, 2)
            lose_percent = round(lose_count/total_rounds * 100, 2)
            draw_percent = round(draw_count/total_rounds * 100, 2)
            skip_percent = round(skip_count/total_rounds * 100, 2)
            
            wins_percent = f"{wins_percent:.{2}f}"
            lose_percent = f"{lose_percent:.{2}f}"
            draw_percent = f"{draw_percent:.{2}f}"
            skip_percent = f"{skip_percent:.{2}f}"
            
            spacer1 = ' ' * (6 - len(str(wins_count)))
            spacer2 = ' ' * (6 - len(str(lose_count)))
            spacer3 = ' ' * (6 - len(str(draw_count)))
            spacer4 = ' ' * (6 - len(str(skip_count)))
            
            spacer11 = ' ' if float(wins_percent) < 10 else ''
            spacer22 = ' ' if float(lose_percent) < 10 else ''
            spacer33 = ' ' if float(draw_percent) < 10 else ''
            spacer44 = ' ' if float(skip_percent) < 10 else ''

            
            print(f'Wins: {wins_count}{spacer1}  - {spacer11}{wins_percent}%')
            print(f'Lose: {lose_count}{spacer2}  - {spacer22}{lose_percent}%')
            print(f'Draw: {draw_count}{spacer3}  - {spacer33}{draw_percent}%')
            print(f'Skip: {skip_count}{spacer4}  - {spacer44}{skip_percent}%')
            print()


            #            add to statistic_report:    |
            statistic_report = '\n'
            statistic_report += now_datatime + '\n'
            statistic_report += '______________________' + '\n'   
            statistic_report += f'Total Rounds: {total_rounds}' + '\n\n'
            statistic_report += f'Wins: {wins_count}{spacer1}  - {spacer11}{wins_percent}%'+ '\n'   
            statistic_report += f'Lose: {lose_count}{spacer2}  - {spacer22}{lose_percent}%'+ '\n'   
            statistic_report += f'Draw: {draw_count}{spacer3}  - {spacer33}{draw_percent}%'+ '\n'   
            statistic_report += f'Skip: {skip_count}{spacer4}  - {spacer44}{skip_percent}%'+ '\n\n'   

            #print(statistic_report)

            with open("reports\\statistic_reports.txt", "a", encoding='utf-8') as file:
                file.write(statistic_report)
                
            print('Reported to: reports/statistic_reports.txt!')         

        

#                                                     |
#                      MENU                           |
#                                                     |

def menu():
    global run_flag, user_name, _user_bank,_user_bet, user_hand, ai_hand, except_nums_list, random_card_deck, random_card_hand
    

    menu_select = input('\nSelect>>>')


#                                 |
    if menu_select == '0':
        show_menu()
        
#                                 |
    if menu_select == '1':
        print('NEW GAME\n')
        if debit_bet(_user_bet):
            new_game()
            
#                                 |
    if menu_select == '2':
        print('Changing BET')
        make_bet()

#                                 |
    if menu_select == '3':
        print(f'{user_name}: {_user_bank}')

#                                 |
#     Reports's Statistic:        |
    if menu_select == '4':
        print('Show Reports Statictic:\n')
        statistic_report()
        
#         GET FIVE Mini-game       
    if menu_select == '5':
        print('LETS GET FIVE!')
        get_five_game()
        


#                                 |
#      Change Nickname:           |
    if menu_select == '6':
        user_name = name_request()
        init_user_data()   

#                                 |
    if menu_select == '00':
        show_extended_menu()

#                                 |
    if menu_select == '01':
        show_rules()


#                                 |
    if menu_select == '9':
        exit_confirm = input('Sure for Exit?(1/else)>>>')
        if exit_confirm == '1':
            print('Goodbye!')
            run_flag = False
            return
        else:
            print('Let\'s Roll Continue!')            

    

#                                 |
    if menu_select == '001':
        print('001: ADMIN SERVICE: CLEAR REPORTS')
        
        with open("reports\\game_reports.txt", "w", encoding='utf-8') as file:
            file.write('game_reports.txt was cleared by command-001\n')
            

    if menu_select == '11':
        print('Get One Random Card:')
        get_random_card(1)


    if menu_select == '55':
        print('Get Five Random Card:')        
        get_random_card(5)


    if menu_select == '22':
        print('Get a get a certain few of cards:')
        how_many = input('How many Random Cards You want to get? -> ')
        try:
            how_many = int(how_many)
            if how_many not in range(1,53):
                print('OUT OF DECK RANGE! ')
                return
            get_random_card(how_many) 
        except:
            print('INVALID VALUE ENTERED!')


    if menu_select == '33':
        print('Drop Randoms Hand:')
        random_card_hand = []
        random_card_deck = deck_list[:]
        print('Dropped!')
        
       

    if menu_select == '98':
        print('Show deck_list:')        
        #random.shuffle(deck_list)
        print(deck_list)

    if menu_select == '99':
        print('Show Sorted Deck:\n')
        deck_show(deck_list)

    #          for Looping of Menu:        |
    menu()            

#                                                     |
#                    END MENU                         |
#                                                     |


#    Main Function:  |
def main():
    menu()
    

    
#    Initialization of variables: user_name, _user_bank:
user_name, _user_bank = init_user_data()

#    Initialization of the Cards Deck:
deck_list = deck_init()


#    Defoult Bet:
_user_bet = 50

#    Empty User Hand:
user_hand = []
#    Empty AI Hand:
ai_hand = []

#    Empty List of Exceptions Cards:
except_nums_list = []


#   for Random Cards:
random_card_deck = deck_list[:]
random_card_hand = []


#          Start App:        |
greeting(user_name, _user_bank)
show_menu()


#          Run App:        |
run_flag = True

while run_flag == True: main()








        
    
