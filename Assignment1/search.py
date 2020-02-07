import numpy as np

class Node:
    state = []
    parent = None
    actions = []
    g_cost = 0.0
    h_cost = 0.0
    n = 0

    def __init__(self, state, parent, actions, g_cost, h_cost, n):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.n = n

    def take_action(self, action):
        new_state = self.state
        position = -1
        for i in range(self.n):
            for j in range(self.n):
                if new_state[i][j] == -1:
                    position = (i, j)
                    break
        if action == "u":
            new_state[position[0]][position[1]] = new_state[position[0]+1][position[1]]
            new_state[position[0]+1][position[1]] = -1
        elif action == "r":
            new_state[position[0]][position[1]] = new_state[position[0]][position[1]-1]
            new_state[position[0]][position[1]-1] = -1
        elif action == "l":
            new_state[position[0]][position[1]] = new_state[position[0]][position[1]+1]
            new_state[position[0]][position[1]+1] = -1
        else:
            new_state[position[0]][position[1]] = new_state[position[0]-1][position[1]]
            new_state[position[0]-1][position[1]] = -1
        return new_state

final_state = None

def get_final_state(n):
    final_state = []
    row = []
    for i in range(n):
        if i==0:
            row.append(-1)
        else:
            row.append(i)
    final_state.append(row)
    for i in range(1,n):
        row = []
        for j in range(n):
            row.append(i*n+j)
        final_state.append(row)
    return np.array(final_state)

def get_misplaced_tiles(current_state):
    misplaced_tiles = 0
    n = len(current_state)
    for i in range(n):
        for j in range(n):
            if current_state[i][j] != final_state[i][j]:
                misplaced_tiles = misplaced_tiles + 1
    return misplaced_tiles

def build_current_state():
    pass


if __name__ == ("__main__"):
    final_state = get_final_state(3)
    state = np.array([[1, -1, 2],[3, 4, 5],[6, 7, 8]])
    print(state)
    new_state = Node(state=state, parent=final_state, actions=["u", "l", "r"], g_cost=0.0, h_cost=0.0, n=3)
    new_state_matrix = new_state.take_action("u")
    print(new_state_matrix)