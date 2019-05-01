import numpy as np

V = np.zeros((4, 6)) # top to bottom rows are C, S, M, F
V[0][0] = 50
V[1][0] = 50
V[3][0] = 50
theta = 0.05
alpha = 0.1
gamma = 0.9
r = np.array([[-10], [-5], [-4], [-3]])
crash = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]
              , [0, 0, 0, 0.3, 0, 0], [0, 0, 0, 0.5, 0.3, 0]])
count = 0
pol = np.array([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]
              , [0, 0, 0, 0, 0], [-1, -1, -1, -1, -1]])
# 0 stay the same, 1 faster, -1 slower

while alpha > theta:
    alpha = 0
    for j in range(5):
        for i in range(4):
            if V[i][j] != 50:
                u = V[i][j]
                V[i][j] = (crash[i + pol[i][j]][j+1] * (r[0] + gamma * V[0][j+1])) + ((1-crash[i + pol[i][j]][j+1]) * (r[i + pol[i][j]] + gamma * V[i + pol[i][j]][j+1]))
                alpha = max(alpha, abs(u-V[i][j]))
    count += 1

print(V)
print(count)