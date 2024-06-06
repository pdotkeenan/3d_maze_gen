# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D



class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.  You'll need to complete its implementation for task B.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"

        self.direction_coordinates = {
            'NORTH': Coordinates3D(0, 1, 0),
            'NORTHEAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 0, 1),
            'SOUTH': Coordinates3D(0, -1, 0),
            'SOUTHWEST': Coordinates3D(-1, 0, 0),   
            'WEST': Coordinates3D(0, 0, -1),
        }
        
        self.direction_opposites = {
            'NORTH': 'SOUTH',
            'NORTHEAST': 'SOUTHWEST',
            'EAST': 'WEST',
            'SOUTH': 'NORTH',
            'SOUTHWEST': 'NORTHEAST',
            'WEST': 'EAST',
        }
        
        self.direction_order = ['NORTH', 'NORTHEAST', 'EAST', 'SOUTH', 'SOUTHWEST', 'WEST']
        self.angles = [0, 45, 90, -180, -135, -90]
        
    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        current_position = entrance
        exits = maze.getExits()
        
        # Assume north as starting orientation - it'll get adjusted later
        current_orientation = 'NORTH'
        original_orientation = 'NORTH'
        total_turn_angle = 0
        
        self.solverPathAppend(current_position)
        self.m_entranceUsed = entrance
        
        # Loop until we reach an exit
        while current_position not in exits:
            # Get a list of all the neighbours for the current position
            neighbours = maze.neighbours(current_position)
            
            # Filter out boundary neighbours
            valid_neighbours = [neigh for neigh in neighbours if
                                (neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and
                                 neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())) or neigh in exits]
            
            # Provisionally choose a new cell in current orientation
            new_position = current_position + self.direction_coordinates[original_orientation]
            
            # If there's no wall, keep moving in the current direction
            if not maze.hasWall(current_position, new_position) and new_position in valid_neighbours and total_turn_angle == 0:
                # Update the current position
                current_position = new_position
                self.solverPathAppend(current_position)
            # Enter wall following mode
            else:
                # Get the index of the current direction/orientation in the direction_order list
                start_index = self.direction_order.index(current_orientation)
                
                # Loop through the direction_order list
                for i in range(len(self.direction_order)):
                    # Index of previous direction/orientation we need to check
                    dir_index = (start_index - (i+1)) % len(self.direction_order)
                    
                    # Direction/orientation we came from - use THIS to determine where we check to move
                    direction = self.direction_order[dir_index]
                    angle = self.angles[dir_index]
                    
                    # I'm unsure if this implementation is correct - I'd appreciate feedback!
                    relative_angle = angle - self.angles[start_index]

                    # Provisionally choose a new position according to the direction/orientation
                    new_position = current_position + self.direction_coordinates[direction]
                    #print(f"relative_angle: {relative_angle} in direction: {direction}")
                    # If new position is in valid_neighbours list AND doesn't have a wall, we can move to that position
                    # Else, we try the next direction
                    if new_position in valid_neighbours and not maze.hasWall(current_position, new_position):
                        # Update the current orientation based on the direction we came from
                        # (e.g., 'direction' was east, which means we travelled east, which means we came from the west)
                        current_orientation = self.direction_opposites[direction]
                        current_position = new_position
                        total_turn_angle += relative_angle
                        print(f"total_turn_angle: {total_turn_angle}")
                        self.solverPathAppend(current_position)
                        break

        self.m_exitUsed = current_position
        self.solved(self.m_entranceUsed, self.m_exitUsed)