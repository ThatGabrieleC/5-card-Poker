#SUMS
straight_order = ["28", "20", "25", "30", "35", "40", "45", "50", "55", "60"]
card_values_c = [2, 3, 4, 5, 14]
user_straight_sum = str(sum(card_values_c))
user_sum_index = straight_order.index(user_straight_sum)
print(user_sum_index)  # Output: [0]

#ALL INDICES OF AN ELEMENT
my_list = [1, 2, 3, 2, 4, 2, 5]
element = 2
indices = [i for i, x in enumerate(my_list) if x == element]
print(indices)  # Output: [1, 2, 4, 5]

#SCORE
user, first, second = [0, 0, 0]
players = [user, first, second]
winner = 1
players[winner] += 1
winner = 2
players[winner] +=1
print(players)  #Output: [0, 1, 1]
