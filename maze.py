#myfile = open("matrix.txt", "w")

class Cell():
    """
    Object representing a cell with walls in its compass directons

    """
    def __init__(self, x: int, y: int, isWall:bool=True):
        self.x, self.y = x, y
        self.walls={'N': True, 'S': True, 'W': True, 'E': True}
        if not isWall: 
            for key in self.walls.keys(): self.walls[key]=False
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def get_pos(self) -> tuple:
        return (self.x, self.y)
    
    def get_neighbors(self) -> list[tuple]:
        return [(self.x+dx, self.y+dy) for dy, dx in [(0,-1), (0,1), (-1, 0), (1, 0)]]


class MazeArray():
    """
    Object representing Maze array of Cell() objects
    """
    def __init__(self, m: int, n: int, isWall=True):
        self.n = n
        self.m = m
        self.totalnodes = (n+1)*(m+1)
        self.world = []
        ctr = 0
        for i in range(m):
            self.world.append(list())
            for j in range(n):
                self.world[i].append(Cell(j, i, isWall))
                ctr+=1
        print(f"{ctr} nodes created")

    def cell_at(self, n: tuple) -> Cell:
        return self.world[n[1]][n[0]]
    
    def remove_wall(self, currCell: Cell, otherCell: Cell) -> None:
        if abs(currCell.x-otherCell.x)+abs(currCell.y-otherCell.y) != 1:
            raise Exception("{otherCell} not adjacent to self {currCell}")

        if otherCell.x > currCell.x:
            currCell.walls['E'] = False
            otherCell.walls['W'] = False
        elif otherCell.x < currCell.x:
            currCell.walls['W'] = False
            otherCell.walls['E'] = False
        elif otherCell.y > currCell.y:
            currCell.walls['S'] = False
            otherCell.walls['N'] = False
        elif otherCell.y < currCell.y:
            currCell.walls['N'] = False
            otherCell.walls['S'] = False
    
    def __repr__(self):
        return str(self.world)
    
    def __str__(self):
        mystr = ""
        for i in range(self.n):
            mystr += "+--" if self.cell_at((i, 0)).walls['N'] else "+  "
        mystr+='+\n'
        for i in range(self.m):
            horstr = "+"
            verstr = "|"
            for j in range(self.n):
                if self.cell_at((j,i)).walls['E']: verstr += "  |"
                else: verstr += "   "
                if self.cell_at((j,i)).walls['S']: horstr += "--+"
                else: horstr += "  +"
            mystr+=verstr + '\n' + horstr + '\n'
        return mystr

def read_maze(file):
    pass

def write_maze(maze, file):
    pass

