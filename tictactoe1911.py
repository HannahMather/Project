
import random
import matplotlib.pyplot as plt


# return all possible moves for player from state
def next_states(player, state):
    return [
        tuple((value if location != next_location else player)
              for location, value in enumerate(state))
        for next_location, value2 in enumerate(state)
        if value2 == 0]

# a random player
def random_move(player, state):
    return random.choice(next_states(player, state))

    
def win(player,state):
    win_loc = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # vertical
        (0, 4, 8), (2, 4, 6)              # diagonal
        ]
    return any(all(state[loc] == player for loc in locs)
               for locs in win_loc)


def is_finished(state):
    return all(value != 0 for value in state)

# a player following a strategy: take winning moves, block winning 
# moves for the other player, otherwise take positions in order of 
# preference ie centre, corners, edges

def update_value_map_perfect(value_map, player, move):
    otherplayer = 3 - player
    next_moves = next_states(otherplayer, move)
    if win(player, move):
        value_map[player, move] = 1
    elif not next_moves:
        value_map[player, move] = 0
    else:
        # assume other player tries to maximize their value
        for next_move in next_moves:
            if (otherplayer, next_move) not in value_map:
                update_value_map_perfect(value_map, otherplayer, next_move)
        max_value = max(value_map[otherplayer, next_move]
                        for next_move in next_moves)
        # if other player wins, we lose, so our value is minus their value
        value_map[player, move] = -max_value

def update_value_map_random(value_map, player, move):
    value_map[player, move] = 0
    if not win(player, move):
        otherplayer = 3 - player
        for next_move in next_states(otherplayer, move):
            if (otherplayer, next_move) not in value_map:
                update_value_map_random(value_map, otherplayer, next_move)
    
def get_value_map(update_func):
    value_map = {}
    initial_state = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    for move in next_states(1, initial_state):
        update_func(value_map, 1, move)
    return value_map


value_map_perfect = get_value_map(update_value_map_perfect)
value_map_random = get_value_map(update_value_map_random)


def player_move(value_map, player, state,explore=-1):
    moves = next_states(player, state)
    if random.random() < explore:
        return random.choice(moves)
    knownmoves = [move for move in moves if (player,move) in value_map]
    if knownmoves:
        max_value = max(value_map[player, move] for move in knownmoves)
        best_moves = [move for move in knownmoves
                      if value_map[player, move] == max_value]
        return random.choice(best_moves)
    else:
        return random.choice(moves)

def next_play(player, state, value_map):
    next_state = player_move(value_map, player, state)
    if win(player, next_state):
        #print("player %i wins" % player)
        return (player, next_state)
    elif is_finished(next_state):
        #print("draw")
        return (0, next_state)
    else:
        return (None, next_state)

# runs one complete test game
def test(value_map_rl,value_map_other,e=0.1):
    state0 = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    alpha = 0.5
    while True:
        state1 = next_play(1, state0,value_map_other)[1]
        #print(state_str(state1) + "\n-----")
        if win(1, state1):
            value_map_rl[2,state0] = 0
            #print("player 1 wins")
            return (value_map_rl,0)
        if is_finished(state1):
            value_map_rl[2,state0] = 0.5
            #print("draw")
            return (value_map_rl,0.5)
        state2 = rl_move(2, state1,value_map_rl,e)
        value_map_rl[2,state0] = (
            value_map_rl.get((2,state0), 0.5)
            + alpha * (value_map_rl.get((2,state2), 0.5) 
            - value_map_rl.get((2,state0), 0.5))
            )
        #print(state_str(state2) + "\n-----")
        if win(2, state2):
            value_map_rl[2,state2] = 1
            #print("player 2 wins")
            return (value_map_rl,1)
        if is_finished(state2):
            value_map_rl[2,state2] = 0.5
            #print("draw")
            return (value_map_rl,0.5)
        state0 = state2

def test2(value_map_one,value_map_two):
    state0 = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    while True:
        state1 = next_play(1, state0,value_map_one)[1]
        #print(state_str(state1) + "\n-----")
        if win(1, state1):
            #print("player 1 wins")
            return (0)
        if is_finished(state1):
            #print("draw")
            return (0.5)
        state2 = next_play(2, state1,value_map_two)[1]
        #print(state_str(state2) + "\n-----")
        if win(2, state2):
            #print("player 2 wins")
            return (1)
        if is_finished(state2):
            #print("draw")
            return (0.5)
        state0 = state2        

# reinforcement learner
def rl_move(player,state,value_map,e):
    a = random.random()
    val = []
    if a < e:
        #print('e')  # indicates when an exploratory move has been made
        return random_move(player, state)
    moves = next_states(player,state)
    for next_state in moves:
        if (2,next_state) in value_map:
            val += [value_map.get((2,next_state))]
    if val:
        opts = (next_state for next_state,vals 
                in zip(moves,val) if vals == max(val))
        return random.choice(list(opts))
    else:
        return random_move(player,state)

        
# produce a graph        
value_map={}
for j in range(5000):
    test(value_map,value_map_random,e=0.15)
     
data1 = 0
data2 = 0
avg1 = []
avg2 = []

for i in range(2,40000):
    test_vals = test(value_map,value_map_random,e=0.15)
    value_map = test_vals[0]
    d1 = test_vals[1]
    d2 = test2(value_map_random,value_map_perfect)
    data1 += d1
    data2 += d2
    avg1 += [data1/i]
    avg2 += [data2/i]
      

data1 = 0
avg3 = []

for i in range(2,20000):
    d1 = test2(value_map_random,value_map)
    data1 += d1
    avg3 += [data1/i]
    
avg1 = avg1 + avg3[9:]    

x = list(range(59987))
plt.plot(x,avg1,lw=0.5,label="RL against random")
plt.plot(x,avg2+avg2[20009:],'r',lw=0.5,label="Perfect against random")
plt.axis([0,59987,0.65,0.97])
plt.xlabel("Number of games",fontsize=12)
plt.ylabel("Average score",fontsize=12)
plt.legend(loc='lower right',fontsize=10)
plt.savefig('vperfecte.pdf')
plt.show()