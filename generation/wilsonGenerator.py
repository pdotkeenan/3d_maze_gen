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
            'UP': Coordinates3D(1, 0, 0),
            'DOWN': Coordinates3D(-1, 0, 0),
            'LEFT': Coordinates3D(0, -1, 0),
            'RIGHT': Coordinates3D(0, 1, 0),
            'FORWARD': Coordinates3D(0, 0, 1),
            'BACKWARD': Coordinates3D(0, 0, -1)
        }
        
        
    def generateMaze(self, maze: Maze3D):
        
        # Start by initializing all the cells
        maze.initCells(True)
        
        # Fill all unvisited cells
        self.unvisited = list(maze.allCells())
        
        for cell in self.unvisited:
            if maze.isBoundary(cell):
                self.unvisited.remove(cell)
        
        # Get a random starting cell
        starting_cell = random.choice(self.unvisited)
        
        # Mark the current cell as visited and remove it from unvisited
        self.visited.append(starting_cell)
        self.unvisited.remove(starting_cell)
        
        while self.unvisited:
            # Choose a random unvisited cell
            first_cell = random.choice(self.unvisited)
            current_cell = first_cell
            
            while True:
                # Choose a random direction to travel in for the next cell
                direction = random.choice(list(self.directions.values()))
                next_cell = current_cell + direction
                
                # Get all neighbours of the current cell
                neighbours = maze.neighbours(current_cell)
                
                # Choose a new direction if the next cell is not a neighbour (this stops some out of bounds cells, as the code below doesn't work)
                while next_cell not in neighbours:                                         
                    direction = random.choice(list(self.directions.values()))                           
                    next_cell = current_cell + direction
                    
                # doing a boundary check here sometimes creates an infinite loop - code commented out below
                # on the occasions it works, it doesn't do anything
                # unsure what i've done wrong :( feedback would be appreciated
                # non_boundary_neighbours = [n for n in neighbours if not maze.isBoundary(n)]
                          
                # while next_cell not in non_boundary_neighbours:                                         
                #     direction = random.choice(list(self.directions.values()))                           
                #     next_cell = current_cell + direction
                
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
                self.unvisited.remove(current_cell)
                
                # Get the most recent direction we've travelled in for a particular cell
                most_recent_direction = self.path[current_cell][-1]       
                next_cell = current_cell + most_recent_direction
                
                # Remove the wall between the current cell and the next cell
                maze.removeWall(current_cell, next_cell)
                
                # Move to the next cell
                current_cell = next_cell
                
                # We've finished carving out this path, now reset
                if current_cell in self.visited:
                    self.path = {}
                    break
                
        self.m_mazeGenerated = True