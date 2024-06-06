# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Task C solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from typing import Dict, List, Tuple
from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
import heapq
from random import randint, choice, seed



class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation.  You'll need to complete its implementation for task C.
    """


    def __init__(self):
        super().__init__()
        self.m_name = "taskC"


    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        # we call the the solve maze call without the entrance.
        # DO NOT CHANGE THIS METHOD
        self.solveMazeTaskC(maze)



    def solveMazeTaskC(self, maze: Maze3D):
        """       
        Solve the maze, used by Task C.
        This version of solveMaze does not provide a starting entrance, and as part of the solution, the method should
        find the entrance and exit pair (see project specs for requirements of this task).
        TODO: Please complete this implementation for task C. You should call maze.solved(...) to update which entrance
        and exit you used for task C.

        @param maze: Instance of maze to solve.
        """
        # Priority queue for cells to be explored
        open_set = []  
        
        entrances = maze.getEntrances()
        num_exits = len(maze.getExits())
        
        for entrance in entrances:
            # Add the entrance to the open set with a cost of 0
            heapq.heappush(open_set, (0, entrance, entrance))
            
        # Dictionary to track the path (where each node came from)
        came_from = {}
        
        # Cost from start to current cell
        g_score = {entrance: 0 for entrance in entrances}
        
        # Cost from current cell to goal
        f_score = {entrance: 0 for entrance in entrances}
        
        # Set to keep track of explored cells
        explored_cells = set(entrances)

        # List to keep track of any found exits
        found_exits = []

        ### EXPLORATION PHASE ###
        # Loop until all exits are found and there's no more cells to explore
        while open_set and len(found_exits) < num_exits:
            # Get the cell with the lowest f_score
            current_cost, current, start = heapq.heappop(open_set)

            # Check if the current cell is an exit
            if self.is_exit(entrances, maze, current) and current not in found_exits:
                found_exits.append(current)
                if len(found_exits) == num_exits:
                    break
            
            # Explore the neighbours of the current cell
            for neighbour in maze.neighbours(current):
                # Check if the neighbour has no wall (is movable to)
                if not maze.hasWall(current, neighbour):
                    # If movable, calculate a potential g_score
                    provisional_g_score = g_score[current] + 1
                    # If neighbour hasn't been visited yet (not in g_score dict) 
                    # or the potential g_score is less than the previous one (indicating a better path)
                    if neighbour not in g_score or provisional_g_score < g_score[neighbour]:
                        # Track the path
                        came_from[neighbour] = current
                        # Update the g_score to the provisional g_score
                        g_score[neighbour] = provisional_g_score
                        # Update the f_score to the g_score + heuristic
                        f_score[neighbour] = provisional_g_score + min(self.heuristic(neighbour, exit) for exit in found_exits + [start])
                        # Add the neighbour to the open set
                        heapq.heappush(open_set, (f_score[neighbour], neighbour, start))
                        # Add the neighbour to the explored cells set
                        explored_cells.add(neighbour)

        # Find the closest entrance-exit pair and the corresponding path
        ### OPTIMISATION ###
        best_pair, best_path = self.find_closest_entrance_exit_pair(maze, came_from, g_score, explored_cells, found_exits)
        
        self.solved(best_pair[0], best_pair[1])
        print(f"Length of best path: {len(best_path)}")
        
        ## Actual number of cells explored ###
        for cell in explored_cells:
            self.solverPathAppend(cell)
    
    def is_exit(self, entrances: List[Coordinates3D], maze: Maze3D, cell: Coordinates3D) -> bool:
        return maze.isBoundary(cell) and cell not in entrances
    
    def heuristic(self, a: Coordinates3D, b: Coordinates3D) -> int:
        return abs(a.getLevel() - b.getLevel()) + abs(a.getRow() - b.getRow()) + abs(a.getCol() - b.getCol())

    # Reconstructs the shortest path from start to goal using the map
    def find_shortest_path(self, came_from: Dict[Coordinates3D, Coordinates3D], start: Coordinates3D, goal: Coordinates3D) -> List[Coordinates3D]:
        path = []
        current = goal
        while current != start:
            path.append(current)
            #self.solverPathAppend(current)
            current = came_from.get(current, start)
        path.append(start)
        return path[::-1]

    def find_closest_entrance_exit_pair(self, maze: Maze3D, came_from: Dict[Coordinates3D, Coordinates3D], g_score: Dict[Coordinates3D, int], explored_cells: set, exits: List[Coordinates3D]) -> Tuple[Tuple[Coordinates3D, Coordinates3D], List[Coordinates3D], int]:
        entrances = maze.getEntrances()

        # Initialise best cost to infinity - this means any path_cost will be less than infinity, always leading to a solution
        best_cost = float('inf')
        best_pair = None
        best_path = []

        for entrance in entrances:
            for exit in exits:
                if exit in g_score:
                    # Find the path from entrance to exit
                    path = self.find_shortest_path(came_from, entrance, exit)
                    # Calculate the cost of the path
                    path_cost = g_score[exit] + len(explored_cells)
                    # Check if the path cost is less than the best cost
                    if path_cost < best_cost:
                        # If so, update the best cost, pair and path
                        best_cost = path_cost
                        best_pair = (entrance, exit)
                        best_path = path

        return best_pair, best_path