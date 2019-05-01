import numpy as np
import time

start = time.time()

V = np.zeros((4, 6)) # top to bottom rows are C, S, M, F
V[0][0] = 50
V[1][0] = 50
V[3][0] = 50
theta = 0.05
gamma = 0.9
count = 0
r = np.array([[-10], [-5], [-4], [-3]])
crash = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]
              , [0, 0, 0, 0.3, 0, 0], [0, 0, 0, 0.5, 0.3, 0]])
pol = np.array([[50, 1, 1, 1, 1], [50, 1, 1, 1, 1]
              , [0, 0, 0, 0, 0], [50, -1, -1, -1, -1]])  
# 0 stay the same, 1 faster, -1 slower
# 50 means not a state

def peloop(c):
    alpha = 0.1
    while alpha > theta:
        alpha = 0
        for j in range(5):
            for i in range(4):
                if V[i][j] != 50:
                    u = V[i][j]
                    V[i][j] = (crash[i + pol[i][j]][j+1] * (r[0] + gamma * V[0][j+1])) + ((1-crash[i + pol[i][j]][j+1]) * (r[i + pol[i][j]] + gamma * V[i + pol[i][j]][j+1]))
                    alpha = max(alpha, abs(u-V[i][j]))
        c += 1
    return(c)


def piloop():
    stable = True
    for j in range(5):
        for i in range(4):
            if V[i][j] != 50:
                A = pol[i][j]
                if i != 0:
                    if i != 3:
                        a = (crash[i+1][j+1] * (r[0] + gamma * V[0][j+1])) + ((1-crash[i+1][j+1]) * (r[i+1] + gamma * V[i+1][j+1]))
                    else:
                        a = -10000 # very negative so won't be the max
                    b = (crash[i][j+1] * (r[0] + gamma * V[0][j+1])) + ((1-crash[i][j+1]) * (r[i] + gamma * V[i][j+1]))
                    if i != 1:
                        c = (crash[i-1][j+1] * (r[0] + gamma * V[0][j+1])) + ((1-crash[i-1][j+1]) * (r[i-1] + gamma * V[i-1][j+1]))
                    else:
                        c = -1000 
                    newpol = max(a,b,c)
                    if newpol == a:
                        pol[i][j] = 1
                    elif newpol == b:
                        pol[i][j] = 0
                    else:
                        pol[i][j]= -1
                    if A != pol[i][j]:
                        stable = False
    return stable

polstable = False
    
while polstable == False:
    count = peloop(count)
    polstable = piloop()

print(V)
print(pol)

end = time.time()  # time taken

print(end-start)