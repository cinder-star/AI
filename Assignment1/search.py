import numpy as np
import queue
from collections import deque
from hashlib import blake2b

class Node(object):
    state = []
    parent = None
    actions = []
    g_cost = 0.0
    h_cost = 0.0
    n = 0

    def __init__(self, state=[], parent=None, actions=[], g_cost=0.0, h_cost=0.0, n=0):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.n = n

    def take_action(self, action):
        new_state = np.array(self.state, copy=True)
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

    def __contains__(self, item):
        n = item.n
        for i in range(n):
            for j in range(n):
                if item.state[i][j] != self.state[i][j]:
                    return False
        return True
    
    def __eq__(self, item):
        if self.__hash__() == item.__hash__():
            return True
        return False

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        a = self.state.view(np.uint8)
        return int(blake2b(a, digest_size=8).hexdigest(), 16)

final_state = None

def solution(node):
    if not node.parent:
        print(node)
        print()
        return
    solution(node.parent)
    print(node)
    print()

def goal_test(node):
    n = len(node.state)
    for i in range(n):
        for j in range(n):
            if node.state[i][j] != final_state.state[i][j]:
                return False
    return True

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
    return Node(state=np.array(final_state),n=n)

def get_misplaced_tiles(current_state):
    misplaced_tiles = 0
    n = len(current_state)
    for i in range(n):
        for j in range(n):
            if current_state[i][j] != final_state[i][j]:
                misplaced_tiles = misplaced_tiles + 1
    return misplaced_tiles

def get_actions(state):
    n = len(state)
    for i in range(n):
        for j in range(n):
            if state[i][j] == -1:
                break
    actions = []
    if i != n-1:
        actions.append("u")
    if i != 0:
        actions.append("d")
    if j != n-1:
        actions.append("l")
    if j != 0:
        actions.append("r")
    return actions

def child_node(state, action):
    new_state = state.take_action(action)
    new_actions = get_actions(new_state)
    return Node(state=new_state, parent=state, actions=new_actions, n=len(new_state))

def breadth_first_search(initial_state):
    current_state = initial_state
    path_cost = 0
    if goal_test(initial_state):
        return solution(initial_state)
    frontier = deque()
    frontier.append(current_state)
    explored = set()
    while True:
        if not frontier:
            return False
        current_state = frontier.popleft()
        explored.add(current_state)
        for action in current_state.actions:
            child = child_node(current_state, action)
            if child not in explored or child not in frontier:
                if goal_test(child):
                    return solution(child)
                frontier.append(child)

def build_initial_state():
    n = int(input())
    initial_state = []
    for i in range(n):
        z = input()
        x = [int(y) for y in z.split()]
        initial_state.append(x)
    actions = get_actions(initial_state)
    return Node(state=np.array(initial_state), actions=actions, n=n)


if __name__ == ("__main__"):
    final_state = get_final_state(3)
    lst = build_initial_state()
    breadth_first_search(lst)