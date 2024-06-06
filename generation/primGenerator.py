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
        maze.initCells(True)
        all_cells = list(maze.allCells())
        
        # Filter out any invalid (boundary cells) - this is important to avoid
        # the assertion error for the isBoundary method
        valid_cells = [u for u in all_cells if
                        (u.getRow() >= 0 and u.getRow() < maze.rowNum(u.getLevel()) and
                        u.getCol() >= 0 and u.getCol() < maze.colNum(u.getLevel()))]
        
        # Randomly select a starting cell
        starting_cell = random.choice(valid_cells)
        
        visited = set()
        visited.add(starting_cell)
        
        # List for neighbour walls of the starting cell
        frontier_set = maze.neighbourWalls(starting_cell)
        
        # Loop until the frontier set is empty
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
                # If so, remove the frontier wall from the frontier set
                frontier_set.remove(frontier_wall)
            else:
                if frontier_cell not in visited and (frontier_cell.getRow() >= 0 and frontier_cell.getRow() < maze.rowNum(frontier_cell.getLevel()) and
                        frontier_cell.getCol() >= 0 and frontier_cell.getCol() < maze.colNum(frontier_cell.getLevel())):
                    # Connect the cells by removing the wall between them
                    maze.removeWall(frontier_cell, visited_cell)
                    
                    # Add the frontier cell to the visited set
                    visited.add(frontier_cell)
                    
                    # Add new unique frontier walls to the frontier set
                    for wall in maze.neighbourWalls(frontier_cell):
                        cell1, cell2 = wall
                        if (cell1 not in visited or cell2 not in visited) and wall not in frontier_set:
                            frontier_set.append(wall)
                
                # Remove the processed frontier wall from the frontier set
                frontier_set.remove(frontier_wall)
        
        self.m_mazeGenerated = True
