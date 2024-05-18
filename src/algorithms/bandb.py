import heapq
import sys
from dataclasses import dataclass

from typing import Any, Self

import numpy as np


@dataclass
class MinMaxBound:
    min: float
    max: float


class PartialSolution:
    order: list[int] = []
    visited: list[bool]
    length: float = 0.0
    upper_bound: float = 0.0
    lower_bound: float = 0.0

    @staticmethod
    def firsts(distance_matrix) -> list[Self]:
        bounds = initial_bounds(distance_matrix)
        firsts = []
        max_upper_bound = sum(map(lambda b: b.max, bounds))
        min_lower_bound = sum(map(lambda b: b.min, bounds))
        for i in range(distance_matrix.shape[0]):
            firsts.append(
                PartialSolution(0, max_upper_bound - bounds[i].max, min_lower_bound - bounds[i].min,
                                [i == j for j in range(distance_matrix.shape[0])], [i]))
        return firsts

    @staticmethod
    def expanded(node: Self, i, added_length, min_max_approaching_bounds):
        new_length = node.length + added_length
        new_upper_bound = node.upper_bound - min_max_approaching_bounds[i].max + added_length
        new_lower_bound = node.lower_bound - min_max_approaching_bounds[i].min + added_length
        new_visited = [v for v in node.visited]
        new_visited[i] = True
        new_order = [o for o in node.order]
        new_order.append(i)
        return PartialSolution(new_length, new_upper_bound, new_lower_bound, new_visited, new_order)

    def __init__(self, length: float, upper_bound: float, lower_bound: float, visited: list[bool], order: list[int]):
        self.length = length
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.visited = visited
        self.order = order

    def can_be_completed(self) -> bool:
        return True

    def is_complete(self) -> bool:
        return len(self.order) == len(self.visited)

    def calculate_bounds(self, distance_matrix):
        self.lower_bound = self.length
        self.upper_bound = self.length

        for i in range(len(self.visited)):
            if self.visited[i]:
                continue

            min_val = float('inf')
            max_val = 0

            for row in range(len(distance_matrix) - 1):
                if i == row:
                    continue
                if row != self.order[-1] and self.visited[row] and len(self.order) < len(
                        distance_matrix) - 1:
                    continue

                min_val = min(min_val, distance_matrix[row][i][1])
                max_val = max(max_val, distance_matrix[row][i][1])

            self.lower_bound += min_val
            self.upper_bound += max_val

    def predict_bounds(self, length, destination_index, distance_matrix):
        min_estimate = length
        max_estimate = length

        self.visited[destination_index] = True

        for i in range(len(self.visited)):
            if self.visited[i]:
                continue

            min_val = float('inf')
            max_val = 0

            for row in range(len(self.visited) - 1):
                if i == row:
                    continue
                if row != self.order[-1] and self.visited[row] and len(self.order) < len(self.visited) - 1:
                    continue

                min_val = min(min_val, distance_matrix[row][i])
                max_val = max(max_val, distance_matrix[row][i])

            min_estimate += min_val
            max_estimate += max_val

        self.visited[destination_index] = False

        return min_estimate, max_estimate

    def __lt__(self, other: Self):
        return len(self.order) > len(other.order)
        return self.lower_bound < other.lower_bound


class Track:
    def __init__(self):
        self.path = []

    def append(self, edge):
        self.path.append(edge)


def expand(queue, node, max_length, distance_matrix, min_max_approaching_bounds):
    for i in range(len(node.visited)):
        if node.visited[i]:
            continue

        added_length = distance_matrix[node.order[-1], i]
        if node.length + added_length < max_length:
            new_node = PartialSolution.expanded(node, i, added_length,
                                                min_max_approaching_bounds=min_max_approaching_bounds)
            if new_node.lower_bound < max_length:
                heapq.heappush(queue, new_node)


def initial_bounds(distance_matrix):
    bounds_list = []

    for col in range(len(distance_matrix)):
        min_val = float('inf')
        max_val = 0
        for row in range(len(distance_matrix)):
            if row == col:
                continue
            min_val = min(min_val, distance_matrix[row][col])
            max_val = max(max_val, distance_matrix[row][col])
        bounds_list.append(MinMaxBound(min=min_val, max=max_val))

    return bounds_list


def salesman_greedy_distance_starting_at(start: int, distance_matrix: np.ndarray):
    visited = [False] * distance_matrix.shape[0]
    visited[start] = True
    current_pos = start
    order = [start]
    dist = 0
    while any(not v for v in visited):
        indexes = distance_matrix[current_pos].argsort()
        for index in indexes:
            if not visited[index]:
                visited[index] = True
                dist += distance_matrix[current_pos, index]
                current_pos = index
                order.append(index)

    return dist, order



def salesman_greedy_distance(distance_matrix: np.ndarray):
    min_dist = float('inf')
    best_order = None

    for i in range(distance_matrix.shape[0]):
        dist, order = salesman_greedy_distance_starting_at(i, distance_matrix)
        if dist < min_dist:
            min_dist = dist
            best_order = order

    return min_dist, best_order


def salesman_track_branch_and_bound(distance_matrix):
    queue = []
    optimum_length, optimum_order = salesman_greedy_distance(distance_matrix)

    yield optimum_length, optimum_order

    best_and_worst_distances = initial_bounds(distance_matrix)

    firsts = PartialSolution.firsts(distance_matrix)
    for first in firsts:
        heapq.heappush(queue, first)

    while queue:
        current_node = heapq.heappop(queue)

        # print(f"progress = {len(current_node.order)}, solutions = {len(queue)}")

        if current_node.is_complete():
            if current_node.length < optimum_length:
                optimum_length = current_node.length
                optimum_order = current_node.order

                yield optimum_length, optimum_order
        else:
            expand(queue, current_node, optimum_length, distance_matrix, best_and_worst_distances)
