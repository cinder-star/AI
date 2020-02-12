import numpy as np
import queue
from collections import deque
from queue import PriorityQueue
from hashlib import blake2b
from math import inf

class Node(object):
    state = []
    parent = None
    actions = []
    g_cost = 0.0
    h_cost = 0.0
    n = 0
    depth = 0

    def __init__(self, state=[], parent=None, actions=[], g_cost=0.0, h_cost=0.0, n=0, depth=0):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.n = n
        self.depth = depth

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

    def __lt__(self, value):
        return self.g_cost < value.g_cost

final_state = None

def solution(node):
    if not node.parent:
        return [node]
    tree = solution(node.parent)
    tree.append(node)
    return tree

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
            if current_state[i][j] != final_state.state[i][j]:
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
    return Node(state=new_state, parent=state, actions=new_actions, n=len(new_state), h_cost=get_misplaced_tiles(new_state), depth=state.depth+1)

def higher_cost(queue, state):
    for item in queue:
        if item == state:
            return item
    return None

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
            if child not in explored and child not in frontier:
                if goal_test(child):
                    return solution(child)
                frontier.append(child)

def uniform_cost_search(initial_state):
    path_cost = 0
    frontier = PriorityQueue()
    frontier.put(initial_state)
    explored = set()
    while True:
        if frontier.empty():
            return False
        node = frontier.get()
        if goal_test(node):
            return solution(node)
        explored.add(node)
        for action in node.actions:
            child = child_node(node, action)
            child.g_cost = node.g_cost+1
            higher_cost_node = higher_cost(frontier.queue,child)
            if child not in frontier.queue and child not in explored:
                frontier.put(child)
            elif higher_cost_node and higher_cost_node.g_cost > child.g_cost:
                frontier.queue.remove(higher_cost_node)
                frontier.put(child)

def recursive_dls(initial_state, limit):
    if goal_test(initial_state):
        return solution(initial_state)
    elif limit == 0:
        return -1
    else:
        cutoff_occured = False
        for action in initial_state.actions:
            child = child_node(initial_state, action)
            result = recursive_dls(child, limit-1)
            if result == -1:
                cutoff_occured = True
            elif result:
                return result
        if cutoff_occured:
            return -1
        else:
            return False
    

def depth_limited_search(initial_state, limit):
    return recursive_dls(initial_state, limit)

def iterative_depth_limited_search(initial_state):
    depth = 0
    while True:
        result = recursive_dls(initial_state, depth)
        if result != -1:
            return result
        depth = depth + 1

def greedy_best_first_search(initial_state):
    path_cost = initial_state.h_cost
    node = initial_state
    while True:
        if goal_test(node):
            return solution(node)
        current_child = None
        for action in node.actions:
            child = child_node(node, action)
            if child.h_cost < path_cost:
                current_child = child
                path_cost = child.h_cost
        if not current_child:
            return False
        else:
            node = current_child

def a_star(initial_state):
    path_cost = inf
    node = initial_state
    while True:
        if goal_test(node):
            return solution(node)
        current_child = None
        for action in node.actions:
            child = child_node(node, action)
            if child.h_cost + node.g_cost < path_cost:
                current_child = child
                path_cost = child.h_cost + node.g_cost
        if not current_child:
            return False
        else:
            node = current_child


def build_initial_state():
    n = int(input())
    initial_state = []
    for i in range(n):
        z = input()
        x = [int(y) for y in z.split()]
        initial_state.append(x)
    actions = get_actions(initial_state)
    return Node(state=np.array(initial_state), h_cost=get_misplaced_tiles(initial_state), actions=actions, n=n)


if __name__ == ("__main__"):
    final_state = get_final_state(3)
    lst = build_initial_state()
    # answers = breadth_first_search(lst)
    # answer = uniform_cost_search(lst)
    # answers = depth_limited_search(lst, 9)
    # answers = iterative_depth_limited_search(lst)
    # answers = greedy_best_first_search(lst)
    answers = a_star(lst)
    for ans in answers:
        print(ans)
