import numpy as np

class Maze(object):
    def __init__(self, filename):
        '''
        Maze objects have two main attributes:
        - dim: mazes should be square, with sides of even length. (integer)
        - walls: passages are coded as a 4-bit number, with a bit value taking
            0 if there is a wall and 1 if there is no wall. The 1s register
            corresponds with a square's top edge, 2s register the right edge,
            4s register the bottom edge, and 8s register the left edge. (numpy
            array)

        The initialization function also performs some consistency checks for
        wall positioning.
        '''
        with open(filename, 'rb') as f_in:

            # First line should be an integer with the maze dimensions
            self.dim = int(f_in.next())

            # Subsequent lines describe the permissability of walls
            walls = []
            for line in f_in:
                walls.append(map(int,line.split(',')))
            self.walls = np.array(walls)

        # Perform validation on maze
        # Maze dimensions
        if self.dim % 2:
            raise Exception('Maze dimensions must be even in length!')
        if self.walls.shape != (self.dim, self.dim):
            raise Exception('Maze shape does not match dimension attribute!')

        # Wall permeability
        wall_errors = []
        # vertical walls
        for x in range(self.dim-1):
            for y in range(self.dim):
                if (self.walls[x,y] & 2 != 0) != (self.walls[x+1,y] & 8 != 0):
                    wall_errors.append([(x,y), 'v'])
        # horizontal walls
        for y in range(self.dim-1):
            for x in range(self.dim):
                if (self.walls[x,y] & 1 != 0) != (self.walls[x,y+1] & 4 != 0):
                    wall_errors.append([(x,y), 'h'])

        if wall_errors:
            for cell, wall_type in wall_errors:
                if wall_type == 'v':
                    cell2 = (cell[0]+1, cell[1])
                    print 'Inconsistent vertical wall betweeen {} and {}'.format(cell, cell2)
                else:
                    cell2 = (cell[0], cell[1]+1)
                    print 'Inconsistent horizontal wall betweeen {} and {}'.format(cell, cell2)
            raise Exception('Consistency errors found in wall specifications!')


    def is_permissible(self, cell, direction):
        """
        Returns a boolean designating whether or not a cell is passable in the
        given direction. Cell is input as a list. Directions may be
        input as single letter 'u', 'r', 'd', 'l', or complete words 'up', 
        'right', 'down', 'left'.
        """
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8,
                   'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            return (self.walls[tuple(cell)] & dir_int[direction] != 0)
        except:
            print 'Invalid direction provided!'


    def dist_to_wall(self, cell, direction):
        """
        Returns a number designating the number of open cells to the nearest
        wall in the indicated direction. Cell is input as a list. Directions
        may be input as a single letter 'u', 'r', 'd', 'l', or complete words
        'up', 'right', 'down', 'left'.
        """
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}

        sensing = True
        distance = 0
        curr_cell = list(cell) # make copy to preserve original
        while sensing:
            if self.is_permissible(curr_cell, direction):
                distance += 1
                curr_cell[0] += dir_move[direction][0]
                curr_cell[1] += dir_move[direction][1]
            else:
                sensing = False
        return distance