# agent.py
import random

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
    """A search agent that uses breadth-first search to find the shortest path."""

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        width, height = grid_size
        start = tuple(start_pos)
        goal = tuple(goal_pos)
        walls_set = set(walls)

        if start == goal:
            return []

        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        frontier = [(start, [])]
        visited = {start}

        while frontier:
            pos, path = frontier.pop(0)
            for action, delta in moves:
                next_pos = (pos[0] + delta[0], pos[1] + delta[1])
                if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                    continue
                if next_pos in walls_set or next_pos in visited:
                    continue

                new_path = path + [action]
                if next_pos == goal:
                    return new_path

                visited.add(next_pos)
                frontier.append((next_pos, new_path))

        return None
