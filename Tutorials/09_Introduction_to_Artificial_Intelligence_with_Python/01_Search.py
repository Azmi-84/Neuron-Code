import marimo

__generated_with = "0.11.30"
app = marimo.App(
    width="medium",
    app_title="CS50's Introduction to Artificial Intelligence with Python",
)


@app.cell
def _(mo):
    mo.vstack(
        [
            mo.vstack([mo.md("# Search")], align="center"),
            mo.md(
                "Finding a solution to a problem, like a navigator app that finds the best route from one's origin to destination, or like playing a game and figuring out the next move."
            ),
            mo.hstack(
                [
                    mo.md(
                        "Search problems involve an agent that is given an initial state and goal state, and it return a solution of how to get from the former to the latter. A navigator app uses a typical search process, where the agent (the thinking part of the program) recives an input from one's current location and one's desired destination, and, based on the search algorithm, returns a suggested path. However there are many others search problem, like puzzle or maze. Finding a solution to a 15 puzzle would require the use of a search algorithm."
                    ),
                    mo.md(
                        "![Puzzle Image](https://cs50.harvard.edu/ai/2024/notes/0/15puzzle.png)"
                    ),
                ],
                justify="space-between",
                gap=2,
            ),
        ],
        gap=2,
    )
    return


@app.cell
def _(mo):
    mo.vstack(
        [
            mo.md("## Depth-First Search"),
            mo.md(
                "This is an uninformed search algorithm that explores as far as possible along each branch before backtracking. It uses a stack data structure to keep track of the nodes to be explored. The algorithm starts at the root node and explores as far down a branch as possible before backtracking to explore other branches. This is a stack (in depth-first search) data structure, which is a data structure that follows the last-in-first-out (LIFO) principle. This means that the last element added to the stack is the first one to be removed. The algorithm continues this process until it finds the goal node or exhausts all possible paths."
            ),
            mo.md("Pros:"),
            mo.md(
                "At best, this algorithm is the fatest. If it 'lucks out' and always choose the right path to the solution (by chance), then depth-first search takes the least possible time to get to a solution."
            ),
            mo.md("Cons:"),
            mo.md(
                "This algorithm is not guaranteed to find the shortest path to the solution. It may get stuck in an infinite loop if there are cycles in the graph. It can also use a lot of memory if the graph is very large."
            ),
        ],
        gap=2,
    )
    return


@app.cell
def _():
    class Node:
        def __init__(self, state, parent=None, action=None):
            self.state = state
            self.parent = parent
            self.action = action


    class StackFrontier:
        def __init__(self):
            self.frontier = []

        def add(self, node):
            self.frontier.append(node)

        def contains_state(self, state):
            return any(node.state == state for node in self.frontier)

        def empty(self):
            return len(self.frontier) == 0

        def remove(self):
            # Terminate the search if the frontier is empty, because this means that there is no solution.
            if self.empty():
                raise Exception("empty frontier")
            else:
                # Save the last item in the list (which is the newest node added)
                node = self.frontier[-1]
                # Save all the items on the list besides the last node (i.e. removing the last node)
                self.frontier = self.frontier[:-1]
                return node


    class DepthFirstSearch:
        def __init__(self, initial_state, goal_test, successors):
            # Function that returns True when we reach the goal
            self.goal_test = goal_test
            # Function that returns a list of (action, state) pairs
            self.successors = successors
            # Starting state
            self.initial_state = initial_state

        def solve(self):
            # Initialize frontier with the initial state
            frontier = StackFrontier()
            start = Node(state=self.initial_state)
            frontier.add(start)

            # Initialize an empty explored set
            explored = set()

            # Keep looping until solution found or no solution possible
            while True:
                # If nothing left in frontier, then no path
                if frontier.empty():
                    return None

                # Choose a node from the frontier using LIFO (for DFS)
                node = frontier.remove()

                # If we've reached the goal, we're done
                if self.goal_test(node.state):
                    actions = []
                    cells = []

                    # Work backwards from goal to get solution path
                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        node = node.parent

                    actions.reverse()
                    cells.reverse()

                    return {"actions": actions, "cells": cells}

                # Add the current state to explored set
                explored.add(node.state)

                # Add neighbors to frontier if they haven't been explored
                for action, state in self.successors(node.state):
                    if state not in explored and not frontier.contains_state(
                        state
                    ):
                        child = Node(state=state, parent=node, action=action)
                        frontier.add(child)
    return DepthFirstSearch, Node, StackFrontier


@app.cell
def _(DepthFirstSearch):
    # Example usage
    if __name__ == "__main__":
        # Simple maze example represented as a 2D grid
        # 'S' is the start, 'G' is the goal, '#' is a wall
        maze = [
            ["S", " ", " ", "#", " "],
            ["#", "#", " ", "#", " "],
            [" ", " ", " ", " ", " "],
            [" ", "#", "#", "#", " "],
            [" ", " ", " ", "G", "#"],
        ]

        # Define helper functions for the maze search
        def find_position(maze, target):
            for i in range(len(maze)):
                for j in range(len(maze[0])):
                    if maze[i][j] == target:
                        return (i, j)
            return None

        # Get start and goal positions
        start = find_position(maze, "S")
        goal = find_position(maze, "G")

        # Define goal test function
        def is_goal(state):
            return state == goal

        # Define successor function
        def get_successors(state):
            row, col = state
            candidates = [
                ("up", (row - 1, col)),
                ("right", (row, col + 1)),
                ("down", (row + 1, col)),
                ("left", (row, col - 1)),
            ]

            # Filter valid moves
            result = []
            for action, (r, c) in candidates:
                if (
                    0 <= r < len(maze)
                    and 0 <= c < len(maze[0])
                    and maze[r][c] != "#"
                ):
                    result.append((action, (r, c)))
            return result

        # Create and solve the problem
        problem = DepthFirstSearch(start, is_goal, get_successors)
        solution = problem.solve()

        if solution:
            print(f"Solution found in {len(solution['actions'])} steps!")
            print(f"Path: {solution['actions']}")
        else:
            print("No solution found.")
    return (
        find_position,
        get_successors,
        goal,
        is_goal,
        maze,
        problem,
        solution,
        start,
    )


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
