class Node:
    state = None
    parent = None
    actions = None
    g_cost = 0.0
    h_cost = 0.0

    def __init__(self):
        state = self.state
        parent = self.parent
        actions = self.actions
        g_cost = self.g_cost
        h_cost = self.h_cost

    def take_action(self, action):
        new_state = self.state


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
    return final_state

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
    final_state = get_final_state(4)
    print(final_state)