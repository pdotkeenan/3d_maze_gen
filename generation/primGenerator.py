# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
import random



class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.  
    TODO: Complete the implementation (Task A)
    """
	

    def generateMaze(self, maze: Maze3D):
        # Initialize all cells as walls
        maze.initCells(True)
        
        # Randomly select a starting cell from entrances
        starting_cell = random.choice(list(maze.allCells()))
        
        visited = set()
        visited.add(starting_cell)
        
        # List for frontier walls
        frontier_set = maze.neighbourWalls(starting_cell)
        
        while frontier_set:
            # Randomly select a frontier wall from the frontier set
            frontier_wall = random.choice(frontier_set)
            
            # Unpack the frontier wall tuple into cell1 and cell2
            cell1, cell2 = frontier_wall
            
            # Determine which cell is in the visited set
            if cell1 in visited:
                frontier_cell = cell2
                visited_cell = cell1
            else:
                frontier_cell = cell1
                visited_cell = cell2
            
            # Check if frontier cell is within maze bounds - we don't want to process boundary cells!
            if maze.isBoundary(frontier_cell):
                # Remove the frontier wall from the frontier set
                frontier_set.remove(frontier_wall)
                continue
            
            if frontier_cell not in visited:
                # Connect the cells by removing the wall between them
                maze.removeWall(frontier_cell, visited_cell)
                
                # Add the frontier cell to the visited set
                visited.add(frontier_cell)
                
                # Add new frontier walls to the frontier set, ensuring no duplicates
                for wall in maze.neighbourWalls(frontier_cell):
                    cell1, cell2 = wall
                    if (cell1 not in visited or cell2 not in visited) and wall not in frontier_set:
                        frontier_set.append(wall)
            
            # Remove the processed frontier wall from the frontier set
            frontier_set.remove(frontier_wall)
        
        self.m_mazeGenerated = True
