#myfile = open("matrix.txt", "w")


class Cell():
    """
    Object representing a cell with walls in its compass directons

    """
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.isWall = True

    def __str__(self):
        return f"Wall located at ({self.x}, {self.y})" if self.isWall else f"Open Space located at ({self.x}, {self.y})"
    
    def __repr__(self):
        return f"({self.x}, {self.y})"


class MazeArray():
    """
    Object representing Maze array of Cell() objects
    """
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.world = []
        for i in range(n):
            self.world.append(list())
            for j in range(m):
                self.world[i].append(Cell(i, j))
    
    def __repr__(self):
        return str(self.world)

world = 2
    