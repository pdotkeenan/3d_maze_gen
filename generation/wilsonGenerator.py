# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
import random
from typing import List, Set
from enum import Enum

import random
from typing import List, Set, Tuple

class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson algorithm maze generator.
    TODO: Complete the implementation (Task A)
    """

    def __init__(self):
        self.visited = []
        self.unvisited = {}
        self.path = {}
        
        self.directions = {
            'NORTH': Coordinates3D(0, 1, 0),
            'NORTHEAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 0, 1),
            'SOUTH': Coordinates3D(0, -1, 0),
            'SOUTHWEST': Coordinates3D(-1, 0, 0),   
            'WEST': Coordinates3D(0, 0, -1),
        }
        
    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)
        self.unvisited = list(maze.allCells())
        
        # Filter out any invalid (boundary cells) - this is important to avoid
        # the assertion error for the isBoundary method
        valid_unvisited = [u for u in self.unvisited if
                            (u.getRow() >= 0 and u.getRow() < maze.rowNum(u.getLevel()) and
                            u.getCol() >= 0 and u.getCol() < maze.colNum(u.getLevel()))]
        
        # Get a random starting cell
        starting_cell = random.choice(valid_unvisited)
        
        # Mark the current cell as visited and remove it from unvisited
        self.visited.append(starting_cell)
        valid_unvisited.remove(starting_cell)
        
        # Loop until all cells have been visited / our unvisited list is empty
        while valid_unvisited:
            # Choose a random unvisited cell
            first_cell = random.choice(valid_unvisited)
            current_cell = first_cell
            
            # Loop until we reach a cell that we've already visited
            while current_cell not in self.visited:
                # Choose a random direction to travel in for the next cell
                direction = random.choice(list(self.directions.values()))
                next_cell = current_cell + direction
                
                # Get all valid neighbours of the current cell
                neighbours = maze.neighbours(current_cell)
                valid_neighbours = [neigh for neigh in neighbours if
                                (neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and
                                 neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel()))]
                
                # Choose a new direction if the next cell is not a neighbour
                while next_cell not in valid_neighbours:                                         
                    direction = random.choice(list(self.directions.values()))                           
                    next_cell = current_cell + direction
                
                # Map the current cell to a list of 'direction' we're about to travel in
                self.path[current_cell] = [direction]
                
                # Change our current cell to the next cell retrieved earlier
                current_cell = next_cell
                
                # We've reached the end of the walk
                if current_cell in self.visited:
                    break
            
            # Go back to the first cell
            current_cell = first_cell
            
            while True:
                # Add and remove the current cell from the visited and unvisited lists
                self.visited.append(current_cell)
                valid_unvisited.remove(current_cell)
                
                # Get the most recent direction we've travelled in for a particular cell - this cuts out any loops that could've formed
                most_recent_direction = self.path[current_cell][-1]       
                
                # Calculate the next cell to move to
                next_cell = current_cell + most_recent_direction
                
                # Remove the wall between the current cell and the next cell
                if maze.isBoundary(next_cell) or maze.isBoundary(current_cell):
                    self.path = {}
                    break
                else:
                    maze.removeWall(current_cell, next_cell)
                
                # Move to the next cell
                current_cell = next_cell
                
                # We've finished carving out this path, now reset the path
                if current_cell in self.visited:
                    self.path = {}
                    break
                
        self.m_mazeGenerated = True