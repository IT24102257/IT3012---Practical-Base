# agent.py
import heapq
import math
import random
from collections import deque


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # Legacy greedy agent that ignores partial observability and uses random movement.
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """A simple reflex agent that reacts only to the current percept."""

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here'):
            return 'Up'
        if percept.get('wall_ahead'):
            return 'Right'
        return 'Up'


class ModelBasedAgent:
    """A model-based agent that tracks percept-action history to escape loops."""

    def __init__(self):
        self.last_percept = None
        self.last_action = None

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here'):
            action = 'Up'
        elif percept.get('wall_ahead'):
            if self.last_percept == percept and self.last_action == 'Right':
                action = 'Left'
            else:
                action = 'Right'
        else:
            if self.last_percept == percept and self.last_action == 'Up':
                action = 'Right'
            else:
                action = 'Up'

        self.last_percept = dict(percept)
        self.last_action = action
        return action


class SearchAgent:
    """A graph-search agent that can plan paths with BFS, DFS, or UCS."""

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    @staticmethod
    def _moves():
        return [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        width, height = grid_size
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)

        if start == goal:
            return []

        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            pos, path = frontier.popleft()
            for action, delta in self._moves():
                next_pos = (pos[0] + delta[0], pos[1] + delta[1])
                if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                    continue
                if next_pos in walls_set or next_pos in reached:
                    continue

                new_path = path + [action]
                if next_pos == goal:
                    return new_path

                reached.add(next_pos)
                frontier.append((next_pos, new_path))

        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        width, height = grid_size
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)

        if start == goal:
            return []

        stack = [(start, [])]
        reached = {start}

        while stack:
            pos, path = stack.pop()
            for action, delta in reversed(self._moves()):
                next_pos = (pos[0] + delta[0], pos[1] + delta[1])
                if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                    continue
                if next_pos in walls_set or next_pos in reached:
                    continue

                new_path = path + [action]
                if next_pos == goal:
                    return new_path

                reached.add(next_pos)
                stack.append((next_pos, new_path))

        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        width, height = grid_size
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)

        if start == goal:
            return []

        frontier = []
        counter = 0
        heapq.heappush(frontier, (0, counter, start, []))
        reached = {start: 0}

        while frontier:
            cost, _, pos, path = heapq.heappop(frontier)
            if pos == goal:
                return path

            for action, delta in self._moves():
                next_pos = (pos[0] + delta[0], pos[1] + delta[1])
                if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                    continue
                if next_pos in walls_set:
                    continue

                new_cost = cost + 1
                previous_best = reached.get(next_pos)
                if previous_best is not None and new_cost >= previous_best:
                    continue

                reached[next_pos] = new_cost
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, next_pos, path + [action]))

        return None

    def manhattan_distance(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        return math.sqrt((pos[0] - goal[0]) ** 2 + (pos[1] - goal[1]) ** 2)

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        width, height = grid_size
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(tuple(w) for w in walls)
        heuristic = self.euclidean_distance if heuristic_type == 'euclidean' else self.manhattan_distance

        frontier = []
        reached_states = set()
        start_g_cost = 0
        start_f_cost = start_g_cost + heuristic(start, goal)
        heapq.heappush(frontier, (start_f_cost, start_g_cost, start, []))

        while frontier:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(frontier)
            if current_pos == goal:
                return path_taken
            if current_pos in reached_states:
                continue
            reached_states.add(current_pos)

            for action, delta in self._moves():
                next_pos = (current_pos[0] + delta[0], current_pos[1] + delta[1])
                if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                    continue
                if next_pos in walls_set or next_pos in reached_states:
                    continue

                new_g_cost = g_cost + 1
                new_h_cost = heuristic(next_pos, goal)
                new_f_cost = new_g_cost + new_h_cost
                heapq.heappush(frontier, (new_f_cost, new_g_cost, next_pos, path_taken + [action]))

        return None

    def sense_and_act(self, percept: dict) -> str:
        if not self.plan:
            if not percept.get('all_food'):
                return 'Up'

            start_pos = tuple(percept.get('agent_pos', (0, 0)))
            grid_size = percept.get('grid_size', (10, 10))
            walls = percept.get('walls', [])
            all_food = percept.get('all_food', [])
            remaining_food = percept.get('remaining_food', len(all_food))

            if remaining_food == 0 or not all_food:
                return 'Up'

            closest_food = min(
                all_food,
                key=lambda food: abs(food[0] - start_pos[0]) + abs(food[1] - start_pos[1])
            )

            algorithm = {
                'BFS': self.bfs_search,
                'DFS': self.dfs_search,
                'UCS': self.ucs_search,
                'AStar': self.astar_search,
            }.get(self.active_algo, self.bfs_search)

            path = algorithm(start_pos, closest_food, walls, grid_size)
            self.plan = list(path) if path else []

            if not self.plan:
                return 'Up'

        return self.plan.pop(0)
