#myfile = open("matrix.txt", "w")

class Cell():
    """
    Object representing a cell with walls in its compass directons.
    - get_pos() -> tuple: returns position of cell obj
    - get_neighbors() -> list[tuple]: return all possible unverified neighbors

    """
    def __init__(self, x: int, y: int, hasWalls:bool=True):
        self.x, self.y = x, y
        self.walls={'N': True, 'S': True, 'W': True, 'E': True}
        if not hasWalls: 
            for key in self.walls.keys(): self.walls[key]=False
        
        # including f=0 to have some comparability operation between Cell objects, especially when adding the Cell object to the heap. 
        self.f = 0

    def get_pos(self) -> tuple:
        return (self.x, self.y)
    
    def get_neighbors(self) -> list[tuple]:
        return [(self.x+dx, self.y+dy) for dy, dx in [(0,-1), (0,1), (-1, 0), (1, 0)]]
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    # comparison operator overload for comparing objects
    def __lt__(self, other):
        return self.f < other.f
    def __gt__(self, other):
        return self.f > other.f
    """
    # having the __eq__ comparison removes hasbaility for the cell object when trying to add the object to a set. i do not know why this happens, but it is worth looking into.
    def __eq__(self, other):
        return not (self.f < other.f) and not (other.f < self.f)
    """

class MazeArray():
    """
    Object representing Maze array of Cell() objects
    - cell_at(n: tuple) -> Cell: returns cell object at position n or (x, y)
    - remove_wall(currCell: Cell, otherCell: Cell) -> None: removes the adjacent wall to currCell and otherCell
    - wall_exists(currCell: Cell, otherCell: Cell) -> bool: returns True if a wall exists between currCell and otherCell
    - get_position() -> Cell: returns agent's current position
    - update_position(agent: Cell) -> MazeArray: used to update the string representation with the agent's location
    - set_end(end: Cell) -> None: set the end position
    - get_end() -> Cell: get the end position
    - set_boundary_walls() -> None: To prevent no boundary walls. (implemented to avoid red highlights for printing empty row in vscode)
    - update_walls(otherMaze: MazeArray, cell: Cell) -> None: updates cell's walls from another cell's wall attribute. will also update the neighboring cell's wall that are facing the origin cell. 
    - valid_move(nextpos: tuple) -> bool: returns whether a move is valid
    """
    def __init__(self, m: int, n: int, hasWalls=True):
        self.n = n
        self.m = m
        self.totalnodes = (n+1)*(m+1)
        self.world = []
        ctr = 0
        self.agent = (-1, -1)
        self.end = (-1, -1)
        for i in range(m):
            self.world.append(list())
            for j in range(n):
                self.world[i].append(Cell(j, i, hasWalls))
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
    
    def wall_exists(self, currCell: Cell, otherCell: Cell) -> bool:
        if abs(currCell.x-otherCell.x)+abs(currCell.y-otherCell.y) != 1:
            raise Exception("{otherCell} not adjacent to self {currCell}")

        if otherCell.x > currCell.x:
            return currCell.walls['E'] or otherCell.walls['W']
        elif otherCell.x < currCell.x:
            return currCell.walls['W'] or otherCell.walls['E']
        elif otherCell.y > currCell.y:
            return currCell.walls['S'] or otherCell.walls['N']
        elif otherCell.y < currCell.y:
            return currCell.walls['N'] or otherCell.walls['S']
    
    def get_position(self) -> Cell:
        return self.cell_at(self.agent)

    def update_position(self, agent: Cell):
        self.agent = agent.get_pos()
        return(self)

    def set_end(self, end: Cell) -> None:
        self.end = end.get_pos()
    
    def get_end(self):
        return self.cell_at(self.end)
    
    def set_boundary_walls(self) -> None:
        for i in range(self.m):
            self.cell_at((0, i)).walls['W'] = True
            self.cell_at((self.n-1, i)).walls['E'] = True
        for i in range(self.n):
            self.cell_at((i, 0)).walls['N'] = True
            self.cell_at((i, self.m-1)).walls['S'] = True
    
    def update_walls(self, otherMaze, cell: Cell) -> None:
        cellx, celly = cell.get_pos()
        def isValid(cell: Cell):
            return 0 <= cell[0] < self.n and 0 <= cell[1] < self.m
        
        self.cell_at((cellx, celly)).walls = cell.walls
        if isValid((cellx + 1, celly)): self.cell_at((cellx+1, celly)).walls['W'] = otherMaze.cell_at((cellx+1, celly)).walls['W']
        if isValid((cellx + 1, celly)): self.cell_at((cellx-1, celly)).walls['E'] = otherMaze.cell_at((cellx-1, celly)).walls['E']
        if isValid((cellx, celly + 1)): self.cell_at((cellx, celly + 1)).walls['N'] = otherMaze.cell_at((cellx, celly+1)).walls['N']
        if isValid((cellx, celly + 1)): self.cell_at((cellx, celly - 1)).walls['S'] = otherMaze.cell_at((cellx, celly-1)).walls['S']

    def valid_move(self, nextpos: tuple):
        if abs(self.agent[0]-nextpos[0])+abs(self.agent[1]-nextpos[1]) != 1:
            raise Exception("Cannot Move: {otherCell} not adjacent to self {currCell}")
        if self.agent[0] > nextpos[0]: return not self.cell_at(self.agent).walls['W']
        if self.agent[0] < nextpos[0]: return not self.cell_at(self.agent).walls['E']
        if self.agent[1] > nextpos[1]: return not self.cell_at(self.agent).walls['N']
        if self.agent[1] < nextpos[1]: return not self.cell_at(self.agent).walls['S']

    def __repr__(self):
        return str(self.world)
    
    def __str__(self):
        mystr = ""
        for i in range(self.n):
            mystr += "+--" if self.cell_at((i, 0)).walls['N'] else "+  "
        mystr+='+\n'
        for i in range(self.m):
            horstr = "+"
            verstr = "|" if self.cell_at((0, i)).walls['W'] else " "
            for j in range(self.n):
                if self.cell_at((j,i)).walls['E']: verstr += "  |"
                else: verstr += "   "
                if self.cell_at((j,i)).walls['S']: horstr += "--+"
                else: horstr += "  +"

                # if cell is agent position or end position, then indicate position
                if ((j,i))==self.agent:
                    verstr=verstr[:-3]
                    if self.cell_at((j,i)).walls['E']: verstr += "SS|"
                    else: verstr+="SS "
                elif ((j,i))==self.end:
                    verstr=verstr[:-3]
                    if self.cell_at((j,i)).walls['E']: verstr += "EE|"
                    else: verstr+="EE "

            mystr+=verstr + '\n' + horstr + '\n'
        return mystr

def read_maze(file):
    pass

def write_maze(maze, file):
    pass



