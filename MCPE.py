import numpy as np
import random
import time

start = time.time()

V = np.zeros((4, 6)) # top to bottom rows are C, S, M, F
V[0][0] = 50
V[1][0] = 50
V[3][0] = 50
returns = {}
gamma = 0.9
count = 0
r = np.array([[-10], [-5], [-4], [-3]])
crash = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]
              , [0, 0, 0, 0.3, 0, 0], [0, 0, 0, 0.5, 0.3, 0]])
pol = np.array([[50, 1, 1, 1, 1], [50, 1, 1, 1, 1]
              , [0, 0, 0, 0, 0], [50, -1, -1, -1, -1]])  

for i in range(1000):
    # generate an episode
    ep = [[2,0]]
    for j in range(1,6):
        policy = pol[ep[-1][0]][j-1]
        crashprob = crash[ep[-1][0]][j]
        rand = random.random()
        if rand < crashprob:
            ep += [[0,j]]
        else:
            ep += [[ep[-1][0] + policy,j]]
    G = 0
    for k in range(4,-1,-1):
        G = 0.9*G + r[ep[k+1][0]]
        state = (ep[k][0],ep[k][1])
        if returns.get(state):
            returns[state].append(G)
        else:
            returns[state] = [G]
        V[ep[k][0]][ep[k][1]] = sum(returns[state]) / len(returns[state])
    
print(V)


end = time.time()

print(end - start)