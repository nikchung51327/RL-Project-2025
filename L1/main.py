from environment import Environment
from pprint import pprint
from random import random, randint
import matplotlib.pyplot as plt
import numpy as np

STARTING_POS = (0,0)
TREASURE_POS = (4,4)
HOLE_POS = [(1,1), (1,2), (2,1), (2,2)]
BETA = 0.8

env = Environment()
qT_og = env.qT

pprint(qT_og)

def move(current_pos, q_Table):
    
    curr_row  = current_pos[0]
    curr_col = current_pos[1]

    new_row = curr_row
    new_col = curr_col

    action_values = q_Table[(curr_row, curr_col)]

    prob_num = random()
    
    action_idx = 0
    action_val = 0

    if prob_num <= 0.75:
        action_val = max(action_values)
        action_idx = action_values.index(action_val)
    else:
        choosing = True
        while choosing:
            rand_idx = randint(0,3)
            action_idx = rand_idx
            action_val = action_values[rand_idx]
            if action_val != 0:
                choosing = False
    
    action = None        
    
    if action_idx == 0:
        new_col += 1

    elif action_idx == 1:
        new_row += 1
        
    elif action_idx == 2:
        new_col -= 1
        
    elif action_idx == 3:
        new_row -= 1
        
    
    new_pos = (new_row, new_col)
    if not (0 <= new_pos[0] < 5 and 0 <= new_pos[1] < 5):
        return current_pos, 0, action_idx  # Stay in place

    return new_pos, action_val, action_idx

def run(q_Table):

    position_ls = [STARTING_POS]
    action_val_ls = []
    action_idx_ls = []
    running = True
    curr_pos = STARTING_POS
    move_counter = 0
    treasure_reached = False

    while running:
        
        move_counter += 1
        new_pos, action_val, action_idx = move(curr_pos, q_Table)
        curr_pos = new_pos
        position_ls.append(curr_pos)
        action_val_ls.append(action_val)
        action_idx_ls.append(action_idx)

        if curr_pos == TREASURE_POS:
            running = False
            treasure_reached = True
        elif move_counter > 100000:
            running = False

    return position_ls, action_val_ls, action_idx_ls, treasure_reached

def count_scores(position_ls, action_val_ls, action_idx_ls, q_Table):
    current_reward = 100
    in_hole = False

    for i in range(len(action_val_ls) - 1, -1, -1):
        pos = position_ls[i]
        action_idx = action_idx_ls[i]

        if pos in HOLE_POS:
            if not in_hole:
                current_reward -= 30
                in_hole = True
        else:
            in_hole = False

        og_val = q_Table[pos][action_idx]
        new_val = og_val * BETA + (1 - BETA) * current_reward
        q_Table[pos][action_idx] = new_val
        current_reward -= 1

    return q_Table, len(action_val_ls)


alg_on = True
iteration_counter = 0
q_Table = qT_og
num_moves_ls = []
while alg_on:
    iteration_counter += 1
    treasure_reached = False
    position_ls, action_val_ls,action_idx_ls, treasure_reached = run(q_Table=q_Table)
    if treasure_reached:
        q_Table, num_moves = count_scores(position_ls=position_ls, action_val_ls=action_val_ls, action_idx_ls=action_idx_ls,q_Table=q_Table)
        num_moves_ls.append(num_moves)
    if iteration_counter > 10000:
        alg_on = False


x = np.arange(1, len(num_moves_ls) + 1)
y = np.array(num_moves_ls)
plt.plot(x, y)
plt.xlabel('Episode')
plt.ylabel('Steps to treasure')
plt.title('Learning Progress')
plt.grid()
plt.show()

import seaborn as sns

def plot_q_heatmap(q_Table, title='Max Q-values per state'):
    heatmap_data = np.zeros((5, 5))

    for i in range(5):
        for j in range(5):
            if (i, j) in q_Table:
                heatmap_data[i, j] = max(q_Table[(i, j)])
            else:
                heatmap_data[i, j] = np.nan  # Optional: mask unknown

    plt.figure(figsize=(6, 5))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar=True, square=True)
    plt.title(title)
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    #plt.gca().invert_yaxis()  # So (0,0) is top-left
    plt.show()

plot_q_heatmap(q_Table)




        
        




