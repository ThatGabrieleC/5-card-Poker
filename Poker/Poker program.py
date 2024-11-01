import random, time, json
from random import shuffle
from collections import Counter
from enum import Enum

class CardSuits(Enum):
    Hearts = "Hearts"
    Diamonds = "Diamonds"
    Clubs = "Clubs"
    Spades = "Spades"

class CardValues(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14


class Card:

    _symbols = {"Hearts": "♥️", "Diamonds": "♦️", "Clubs": "♣️", "Spades": "♠"}
    
    _numbers = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, suit: CardSuits, value: CardValues) -> None:
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        return f"{self._numbers[self.value.value]}{self._symbols[self.suit.name]}"

    def __repr__(self) -> str:
        return f"{self._numbers[self.value.value]}{self._symbols[self.suit.name]}"


#LOAD/SAVE SCORE
def load_scores():
    try:
        with open("PokerScores.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [0, 0, 0]

def save_scores(score):
    filename = "PokerScores.json"
    old_score = load_scores()
    if old_score:
        for i in range(len(score)):
            old_score[i] += score[i]

    #write the scores in the json file
    with open(filename, "w") as file:
        json.dump(score, file)

def generate_player_cards(deck, number_of_cards=5):
    unique_cards = set()
    while len(unique_cards) < number_of_cards:
        unique_cards.add(random.choice(deck))
    return list(unique_cards)

def replace_cards(cards, replacing_cards):
    for i in range(len(replacing_cards)):
        cards[i] = replacing_cards[i]
        return list(cards)

def check_hand(cards, custom_value_order):  
    #Straight
    sorted_card_values = sorted([custom_value_order[card.value] for card in cards])
    is_straight = all(sorted_card_values[i] == sorted_card_values[i - 1] + 1 for i in range(1, len(sorted_card_values)))
    ace_as_one_straight = [CardValues.Two.value, CardValues.Three.value, CardValues.Four.value, CardValues.Five.value, CardValues.Ace.value]
    is_lower_straight = sorted_card_values == ace_as_one_straight
    #Flush
    is_flush = len(set(card.suit for card in cards)) == 1
    #Straight Flush
    is_straight_flush = all([is_straight, is_flush])   # La funzione all() richiede un iterabile come argomento, come una lista, una tupla o un altro tipo di sequenza. Tuttavia, is_straight e is_flush sono valori booleani singoli, non un iterabile di valori, quindi bisogna usare le parentesi quadre per prenderli come singoli    
    #Royal Flush
    max_straight = [CardValues.Ace, CardValues.King, CardValues.Queen, CardValues.Jack, CardValues.Ten]
    is_royal_flush = is_straight_flush and all(card.value in max_straight for card in cards)
    #Other combinations
    cards_values_only = [card.value for card in cards]
    cards_count = Counter(cards_values_only)
    counts = list(cards_count.values())
    counts.sort(reverse=True)
    #Pair
    is_pair = [value for value, count in cards_count.items() if count == 2]
    #Tris
    is_tris = [value for value, count in cards_count.items() if count == 3]
    #Poker
    is_poker = [value for value, count in cards_count.items() if count == 4]

    if is_royal_flush:
        return "Royal Flush"
    elif is_straight_flush:
        return "Straight Flush"
    elif is_poker:
        return "Four of a Kind"
    elif counts == [3, 2]:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight or is_lower_straight:
        return "Straight"
    elif is_tris:
        return "Three of a Kind"
    elif len(is_pair) == 2:
        return "Two Pair"
    elif is_pair:
        return "Pair"
    else:
        return "High Card"
        
game_cycles = 0

#GAME START
def start():
    global game_cycles
    scores = load_scores()
    play = input("You wanna play? ")
    if play.lower() in ("yes", "sure", "yeah"):
        all_cards = [Card(suits, value) for suits in CardSuits for value in CardValues]
        shuffle(all_cards)
        replacing_cards = generate_player_cards(all_cards, number_of_cards=random.choice(range(1, 5)))
        
        # user_cards = generate_player_cards(all_cards)

        #USER SPECIFIC CARDS FOR TRIALS
        user_cards = [
            Card(CardSuits.Clubs, CardValues.Four),
            Card(CardSuits.Spades, CardValues.Three),
            Card(CardSuits.Clubs, CardValues.Five),
            Card(CardSuits.Hearts, CardValues.Ace),
            Card(CardSuits.Clubs, CardValues.Two)
        ]   
        print("Your cards are:", ", ".join(str(card) for card in user_cards))
        time.sleep(2)

        #CHANGE PHASE
        while True:
            change_cards = input("Want to change cards? ")
            if change_cards.lower() == "yes":
                quantity = input("Which cards? ")
                card_input_index = ["first", "second", "third", "fourth", "fifth"]

                if quantity.lower() == "none":
                    break

                elif quantity.lower() in card_input_index:
                    index = card_input_index.index(quantity.lower())
                    user_cards[index] = random.choice(all_cards)
                    print("Your new cards are:", ", ".join(str(card) for card in user_cards))
                    break

                elif " " in quantity:
                    change_indices = quantity.lower().split()
                    if all(index in card_input_index for index in change_indices):
                    #controlla se tutti gli indici dati dall'utente siano presenti in card_input_index
                    #in questo modo non si ha più il problema che salta il passaggio del cambio delle
                    #carte se si scrive una parola a caso con uno spazio
                        for index in change_indices:
                            if index in card_input_index:
                                card_index = card_input_index.index(index)
                                user_cards[card_index] = random.choice(all_cards)
                        print("Your new cards are: ", ", ".join(str(card) for card in user_cards))
                        break
                    else:
                        print("Invalid cards selected")

                elif quantity.lower() == "all":
                    unique_cards = set()
                    while len(unique_cards) < 5:
                        unique_cards.add(random.choice(all_cards))
                    user_cards = list(unique_cards)
                    print("Your new cards are:", ", ".join(str(card) for card in user_cards))
                    break  
                            
                else:
                    print("Invalid cards selected")
            elif change_cards.lower() == "no":    
                break     
        
        #GENERATING SPECIFIC OPPONENTS CARDS FOR TRIALS
        first_opponent_cards = [
            Card(CardSuits.Clubs, CardValues.Queen),
            Card(CardSuits.Spades, CardValues.King),
            Card(CardSuits.Clubs, CardValues.Ten),
            Card(CardSuits.Hearts, CardValues.Ace),
            Card(CardSuits.Clubs, CardValues.Jack)
        ]   
        second_opponent_cards = [
            Card(CardSuits.Clubs, CardValues.Four),
            Card(CardSuits.Spades, CardValues.Two),
            Card(CardSuits.Clubs, CardValues.Ace),
            Card(CardSuits.Hearts, CardValues.Three),
            Card(CardSuits.Clubs, CardValues.Five)
        ]

        time.sleep(2)

        custom_value_order = {v: v.value for v in CardValues}
        user_hand = check_hand(user_cards, custom_value_order)
        first_opponent_hand = check_hand(first_opponent_cards, custom_value_order)
        second_opponent_hand = check_hand(second_opponent_cards, custom_value_order)

        #IF OPPONENTS HAVE HIGH CARD, THERE'S A CHANCE THEY CHANGE ALL CARDS
        # change_chance = ["yes", "no"]   
        # if first_opponent_hand == "High Card":
        #     yes_or_no = random.choice(change_chance)
        #     if yes_or_no == "yes":
        #         first_opponent_cards = replace_cards(first_opponent_cards, replacing_cards)
        #         first_opponent_hand = check_hand(first_opponent_cards, custom_value_order)
        # if second_opponent_hand == "High Card":
        #     yes_or_no = random.choice(change_chance)
        #     if yes_or_no == "yes":
        #         second_opponent_cards = replace_cards(second_opponent_cards, replacing_cards)
        #         second_opponent_hand = check_hand(second_opponent_cards, custom_value_order)

        print(f"""
        Your hand: {user_hand}
        1st Opponent hand: {first_opponent_hand}            ( {", ".join(str(card) for card in first_opponent_cards)} )
        2nd Opponent hand: {second_opponent_hand}           ( {", ".join(str(card) for card in second_opponent_cards)} )   
            """)      
        
        #SCORE DASHBOARD
        players = [user_hand, first_opponent_hand, second_opponent_hand]
        scores = [0, 0, 0] if not scores else scores
        
        #if all players have High Card:
        if user_hand == "High Card" and first_opponent_hand == "High Card" and second_opponent_hand == "High Card": 
            stop_high_cards_cycle = False 
            HCC_cycle = 0
            copy_user_c_values = [card.value.value for card in user_cards]
            copy_first_c_values = [card.value.value for card in first_opponent_cards]
            copy_second_c_values = [card.value.value for card in second_opponent_cards]

            while HCC_cycle < 5: 
                if stop_high_cards_cycle == True:
                    break
                user_high = max(copy_user_c_values)
                first_high = max(copy_first_c_values)
                second_high = max(copy_second_c_values)
                high_list = [user_high, first_high, second_high]
                max_high_list = max(high_list)
                max_HL_index = high_list.index(max_high_list) 
                max_HL_count = high_list.count(max_high_list)

                if max_HL_count == 1:
                    stop_high_cards_cycle = True
                    winner_index = max_HL_index
                    scores[winner_index] += 1
                    break

                else:
                    copy_user_c_values.sort(reverse=True)
                    copy_first_c_values.sort(reverse=True)
                    copy_second_c_values.sort(reverse=True)
                    highest_in_copy = [copy_user_c_values[0], copy_first_c_values[0], copy_second_c_values[0]]
                    print(highest_in_copy)
                    max_high_copy = max(highest_in_copy)
                    max_high_copy_count = highest_in_copy.count(max_high_copy)
                    if max_high_copy_count > 1:
                        if max_high_copy != highest_in_copy[0]:
                            copy_user_c_values = [0, 0]
                        elif max_high_copy != highest_in_copy[1]:
                            copy_first_c_values = [0, 0]
                        elif max_high_copy != highest_in_copy[2]:
                            copy_second_c_values = [0, 0]

                        copy_user_c_values.remove(copy_user_c_values[0])
                        copy_first_c_values.remove(copy_first_c_values[0])
                        copy_second_c_values.remove(copy_second_c_values[0])
                        HCC_cycle += 1
                            
                    else:
                        max_high_copy_index = highest_in_copy.index(max_high_copy)
                        winner_index = max_high_copy_index
                        scores[winner_index] += 1
                        stop_high_cards_cycle = True
                        break
            
            #if 2 or more players have identical cards
            winning_player = ["You", "First opponent", "Second opponent"]
            if winning_player[winner_index] == "You":
                print("You won!")
            else:
                print(f"{winning_player[winner_index]} won. May you'll be luckier next time")

        else:   #if there's at least a pair in one of the hands:                                       
            # Establish the player with highest combination
            combination_order = ["High Card", "Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full", "Four of a Kind", "Straight Flush", "Royal Flush"]
            player_combinations = [combination_order.index(hand) for hand in players]

            max_comb = max(player_combinations)
            max_comb_index = player_combinations.index(max_comb)
            max_comb_count = player_combinations.count(max_comb)
            highest_comb = players[max_comb_index]
            print(f"To try: {player_combinations}, {max_comb_index}, {max_comb_count}, {highest_comb}")

            # Check max comb
            if max_comb_count > 1:
                copy_user_c_values = [card.value.value for card in user_cards]
                copy_first_c_values = [card.value.value for card in first_opponent_cards]
                copy_second_c_values = [card.value.value for card in second_opponent_cards]
                if highest_comb in ("Pair", "Two Pair", "Three of a kind", "Four of a kind"):
                    print("entra in prova coppie")
                    #if valore/max/length.... coppie != 1:
                        #check_high_card (forse creando liste copie e rimuovendo coppie, poi seguire procedura già fatta per controllo HC sopra)
                elif highest_comb in ("Straight", "Flush", "Straigh Flush"): 
                    print("entra in prova scala")
                    straight_order = ["28", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
                    user_straight_sum, first_straight_sum, second_straight_sum = [0, 0, 0]
                    user_sum_index, first_sum_index, second_sum_index = [-1, -1, -1]

                    if user_hand in ("Straight", "Flush", "Straigh Flush"):
                        user_straight_sum = str(sum(copy_user_c_values))
                        user_sum_index = straight_order.index(user_straight_sum)
                    if first_opponent_hand in ("Straight", "Flush", "Straigh Flush"):
                        first_straight_sum = str(sum(copy_first_c_values))
                        first_sum_index = straight_order.index(first_straight_sum)
                    if second_opponent_hand in ("Straight", "Flush", "Straigh Flush"):
                        second_straight_sum = str(sum(copy_second_c_values))
                        second_sum_index = straight_order.index(second_straight_sum)
                    
                    players_straight_index = [user_sum_index, first_sum_index, second_sum_index]
                    players_max_straight = max(players_straight_index)
                    max_straight_count = players_straight_index.count(players_max_straight)
                    print(f"{players_straight_index} + {players_max_straight} + {max_straight_count}")
                    if max_straight_count != 1:
                        #in case max_straight_count is more than one, give score to winning player between both
                        for winner in players_straight_index.count(players_max_straight):
                            #winner_max_combination = CONTINUE FROM THERE
                            #in case of total draw, give to both players score and subtract 1 point to the first winner (if the loop enters the score to prevent assign 1 extra point)
                            pass
                    else:
                        winner_max_combination = players_straight_index.index(players_max_straight)
                        print(winner_max_combination)

                elif highest_comb in ("Full"):
                    print("entra in prova full")
                else:
                    print("in teoria prova royal") #in this case give score to both players

                scores[winner_max_combination] += 1
                winning_player = ["You", "First opponent", "Second opponent"]
                
                if winning_player[winner_max_combination] == "You":
                    print("You won!")
                else:
                    print(f"{winning_player[winner_max_combination]} won. May you'll be luckier next time")
            
            # Increase highest combination player score 
            else:
                scores[max_comb_index] += 1
                winning_player = ["You", "First opponent", "Second opponent"]

                if winning_player[max_comb_index] == "You":
                    print("You won!")
                else:
                    print(f"{winning_player[max_comb_index]} won. May you'll be luckier next time")
                    
        score_phrase = """
        SCORE:          User: {}   |   First opponent: {}   |   Second opponent: {}   """
        print(score_phrase.format(scores[0], scores[1], scores[2]))
        save_scores(scores)
        time.sleep(5)

        game_cycles += 1
        #CONTINUE PLAYING
        while True:        
            continue_playing = input("You want to keep playing? ")
            if continue_playing.lower() == "yes":
                wanna_shuffle = input("Wanna shuffle the deck? ")
                if wanna_shuffle.lower() == "yes":
                    shuffle(all_cards)
                    print("Deck shuffled")
                    break
                elif wanna_shuffle.lower() == "no":
                    break
                else:
                    continue
            elif continue_playing.lower() == "no":
                exit()
        if game_cycles % 3 == 0:
            while True:
                score_reset = input("Want to maintain the score or reset it? ")
                if score_reset.lower() in ("reset", "reset it"):
                    test_file = open("PokerScores.json", "w")
                    test_file.write(json.dumps([0, 0, 0]))
                    test_file.close()
                    break
                elif score_reset.lower() in ("maintain", "maintain it"):
                    break    
        start()   
                
    else:
        exit()
    
start()