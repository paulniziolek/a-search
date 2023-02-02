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
        return f"Cell({self.x}, {self.y})"


mycell = Cell(5, 5)
print(mycell)

    

