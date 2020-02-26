import numpy as np
import queue
import time
from datetime import datetime
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
    f_cost = 0.0
    n = 0
    depth = 0

    def __init__(
        self, state=[], parent=None, actions=[], g_cost=0.0, h_cost=0.0, n=0, depth=0, f_cost=inf
    ):
        self.state = state
        self.parent = parent
        self.actions = actions
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.n = n
        self.depth = depth
        self.f_cost = f_cost

    def take_action(self, action):
        new_state = np.array(self.state, copy=True)
        position = -1
        for i in range(self.n):
            for j in range(self.n):
                if new_state[i][j] == -1:
                    position = (i, j)
                    break
        if action == "u":
            new_state[position[0]][position[1]] = new_state[position[0] - 1][
                position[1]
            ]
            new_state[position[0] - 1][position[1]] = -1
        elif action == "r":
            new_state[position[0]][position[1]] = new_state[position[0]][
                position[1] + 1
            ]
            new_state[position[0]][position[1] + 1] = -1
        elif action == "l":
            new_state[position[0]][position[1]] = new_state[position[0]][
                position[1] - 1
            ]
            new_state[position[0]][position[1] - 1] = -1
        elif action == "d":
            new_state[position[0]][position[1]] = new_state[position[0] + 1][
                position[1]
            ]
            new_state[position[0] + 1][position[1]] = -1
        return new_state

    def __contains__(self, item):
        return self.__eq__(item)

    def __eq__(self, item):
        if self.__hash__() == item.__hash__():
            return True
        return False

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        a = self.state.view(np.uint8)
        return int(blake2b(a, digest_size=10).hexdigest(), 16)

    def __lt__(self, value):
        return self.f_cost < value.f_cost


final_state = None
explored_nodes = 0


def solution(node):
    if not node.parent:
        return [node], 0
    tree, depth = solution(node.parent)
    tree.append(node)
    return tree, depth+1


def goal_test(node):
    if node.__hash__() == final_state.__hash__():
        return True
    return False


def get_final_state(n):
    print("Input final board configuration:")
    final_array = []
    for i in range(n):
        z = input()
        x = [int(y) for y in z.split()]
        final_array.append(x)
    actions = get_actions(final_array)
    global final_state
    final_state = Node(
        state=np.array(final_array),
        h_cost=0,
        actions=actions,
        n=n,
    )


def get_misplaced_tiles(current_state):
    misplaced_tiles = 0
    n = len(current_state)
    for i in range(n):
        for j in range(n):
            if final_state.state[i][j] != -1:
                if current_state[i][j] != final_state.state[i][j]:
                    misplaced_tiles = misplaced_tiles + 1
    return misplaced_tiles


def get_manhatten_distance(current_state):
    total_manhatten_distance = 0
    n = len(current_state.state)
    for i in range(n):
        for j in range(n):
            row = None
            column = None
            value = current_state.state[i][j]
            if value == -1:
                row = 0
                column = 0
            else:
                row = value // n
                column = value % n
            total_manhatten_distance = total_manhatten_distance + abs(row-i) + abs(column-j)
    return total_manhatten_distance


def get_actions(state):
    n = len(state)
    position = None
    for i in range(n):
        for j in range(n):
            if state[i][j] == -1:
                position = (i, j)
                break
    actions = []
    if position[0] != n - 1:
        actions.append("d")
    if position[1] != n - 1:
        actions.append("r")
    if position[0] != 0:
        actions.append("u")
    if position[1] != 0:
        actions.append("l")
    return actions


def child_node(state, action):
    new_state = state.take_action(action)
    new_actions = get_actions(new_state)
    return Node(
        state=new_state,
        parent=state,
        actions=new_actions,
        n=len(new_state),
        h_cost=get_misplaced_tiles(new_state),
        depth=state.depth + 1,
    )


def breadth_first_search(initial_state):
    current_state = initial_state
    path_cost = 0
    frontier = []
    frontier.append(current_state)
    explored = set()
    explored.add(current_state.__hash__())
    while True:
        if not frontier:
            return False
        current_state = frontier.pop(0)
        global explored_nodes
        explored_nodes = explored_nodes + 1;
        if goal_test(current_state):
            return solution(current_state)
        explored.add(current_state.__hash__())
        for action in current_state.actions:
            child = child_node(current_state, action)
            if child.__hash__() not in explored:
                explored.add(child.__hash__())
                frontier.append(child)


def uniform_cost_search(initial_state):
    path_cost = 0
    initial_state.f_cost = 0
    frontier = PriorityQueue()
    frontier.put(initial_state)
    explored = set()
    while True:
        if frontier.empty():
            return False
        node = frontier.get()
        global explored_nodes
        explored_nodes = explored_nodes + 1
        if goal_test(node):
            return solution(node)
        explored.add(node.__hash__())
        for action in node.actions:
            child = child_node(node, action)
            child.f_cost = node.f_cost + 1
            if child.__hash__() not in explored:
                frontier.put(child)
                explored.add(child.__hash__())


def recursive_dls(initial_state, limit, explored):
    explored.add(initial_state.__hash__())
    global explored_nodes
    explored_nodes = explored_nodes + 1
    if goal_test(initial_state):
        return solution(initial_state)
    elif limit == 0:
        return -1
    else:
        cutoff_occured = False
        for action in initial_state.actions:
            child = child_node(initial_state, action)
            if child.__hash__() not in explored:
                explored.add(child.__hash__())
                result = recursive_dls(child, limit - 1, explored)
                explored.remove(child.__hash__())
                if result == -1:
                    cutoff_occured = True
                elif result:
                    return result
        if cutoff_occured:
            return -1
        else:
            return False


def depth_limited_search(initial_state, limit=22):
    explored = set()
    return recursive_dls(initial_state, limit, explored)


def iterative_depth_limited_search(initial_state):
    depth = 0
    while True:
        explored = set()
        result = recursive_dls(initial_state, depth, explored)
        if result != -1:
            return result
        depth = depth + 1


def greedy_best_first_search(initial_state):
    frontier = PriorityQueue()
    explored = set()
    initial_state.g_cost = 0.0
    initial_state.h_cost = get_misplaced_tiles(initial_state.state)
    initial_state.f_cost = 0.0
    frontier.put(initial_state)

    while True:
        if not frontier:
            break
        node = frontier.get()
        global explored_nodes
        explored_nodes = explored_nodes + 1
        if goal_test(node):
            return solution(node)
        explored.add(node.__hash__())
        for action in node.actions:
            child = child_node(node, action)
            if child.__hash__() not in explored:
                child.g_cost = node.g_cost + 1
                child.f_cost = child.h_cost
                frontier.put(child)
    return False


def a_star(initial_state):
    frontier = PriorityQueue()
    explored = set()
    initial_state.g_cost = 0.0
    initial_state.h_cost = get_misplaced_tiles(initial_state.state)
    initial_state.f_cost = 0.0
    frontier.put(initial_state)

    while True:
        if not frontier:
            break
        node = frontier.get()
        global explored_nodes
        explored_nodes = explored_nodes + 1
        if goal_test(node):
            return solution(node)
        explored.add(node.__hash__())
        for action in node.actions:
            child = child_node(node, action)
            if child.__hash__() not in explored:
                child.g_cost = node.g_cost + 1
                child.f_cost = child.g_cost + child.h_cost
                frontier.put(child)
    return False


def build_initial_state(n):
    print("Input initial board configuration:")
    initial_state = []
    for i in range(n):
        z = input()
        x = [int(y) for y in z.split()]
        initial_state.append(x)
    actions = get_actions(initial_state)
    return Node(
        state=np.array(initial_state),
        actions=actions,
        n=n,
    )

def start_system():
    print("\033[92m"+"\033[1m"+"******************************************************************")
    print("\033[95m"+"********************WELCOME TO N-PUZZLE SOLVER********************")
    print("\033[92m"+"******************************************************************")
    print("\033[91m"+"\033[4m"+"INSTRUCTIONS:"+"\033[0m")
    print("         1) First you need to input the value of N")
    print("         2) Then Input the initial and final state for the puzzle")
    print("         3) -1 is considered to be the empty slot")
    n = int(input("Enter value for n: "))
    print("\033[92m"+"******************************************************************"+"\033[0m")
    initial_state = build_initial_state(n)
    print("\033[92m"+"******************************************************************"+"\033[0m")
    get_final_state(n)
    print("\033[92m"+"******************************************************************"+"\033[0m")
    return initial_state

def all(initial_state):
    global explored_nodes
    explored_nodes = 0
    then = datetime.now()
    path, depth = breadth_first_search(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

    then = datetime.now()
    path, depth = uniform_cost_search(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

    then = datetime.now()
    path, depth = depth_limited_search(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

    then = datetime.now()
    path, depth = iterative_depth_limited_search(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

    then = datetime.now()
    path, depth = greedy_best_first_search(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

    then = datetime.now()
    path, depth = a_star(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)

def choose_search_func():
    func_dict = {
        "1": breadth_first_search,
        "2": uniform_cost_search,
        "3": depth_limited_search,
        "4": iterative_depth_limited_search,
        "5": greedy_best_first_search,
        "6": a_star,
        "7": all
    }
    print("Choose searching algorithm:")
    print("         1) Breadth First Search")
    print("         2) Uniform Cost Search")
    print("         3) Depth Limited Search")
    print("         4) Iterative Depth Limited Search")
    print("         5) Greedy Best First Search")
    print("         6) A* search")
    print("         7) All")
    choice = input("Enter your choice: ")
    return func_dict[choice]


if __name__ == ("__main__"):
    # final_state = get_final_state(3)
    # lst = build_initial_state()
    # answers, depth = breadth_first_search(lst)
    # answer = uniform_cost_search(lst)
    # answers = depth_limited_search(lst, 9)
    # answers = iterative_depth_limited_search(lst)
    # answers = greedy_best_first_search(lst)
    # answers = a_star(lst)
    # for ans in answers:
    #     print(ans, get_actions(ans.state))
    # print(depth)
    # print(get_actions(lst.state))
    explored_nodes = 0
    # initial_state = start_system()
    initial_state = Node(state=np.array([[1, 2, 3], [4, 5, 6], [7, 8, -1]]), n=3, actions=get_actions(np.array([[1, 2, 3], [4, 5, 6], [7, 8, -1]])), f_cost=0)
    final_state = Node(state=np.array([[-1, 1, 2], [3, 4, 5], [6, 7, 8]]), f_cost=0)
    func = choose_search_func()
    then = datetime.now()
    path, depth = func(initial_state=initial_state)
    now = datetime.now()
    print("total time taken:",(now-then).total_seconds(),"second(s)")
    print("explored nodes:", explored_nodes)
    print("solution depth:",depth)
    for node in path:
        print(node)
        print("------------------------")
