# myfile = open("matrix.txt", "w")

from collections import namedtuple
from typing import List, Tuple
import attr


@attr.s(auto_attribs=True)
class Cell:
    x: int
    y: int
    blocked: bool

setattr(Cell, "__hash__", lambda self: id(self))


class MazeArray:
    """
    Object representing Maze array of Cell() objects
    - cell_at(n: tuple) -> Cell: returns cell object at position n or (x, y)
    - remove_wall(currCell: Cell, otherCell: Cell) -> None: removes the adjacent wall to currCell and otherCell
    - wall_exists(currCell: Cell, otherCell: Cell) -> bool: returns True if a wall exists between currCell and otherCell
    - get_position() -> Cell: returns agent's current position
    - update_position(agent: Cell) -> None: used to update the string representation with the agent's location
    - set_end(end: Cell) -> None: set the end position
    - get_end() -> Cell: get the end position
    - set_boundary_walls() -> None: To prevent no boundary walls. (implemented to avoid red highlights for printing empty row in vscode)
    - update_walls(otherMaze: MazeArray, cell: Cell) -> None: updates cell's walls from another cell's wall attribute. will also update the neighboring cell's wall that are facing the origin cell.
    - valid_move(nextpos: Cell) -> bool: returns whether a move is valid
    """

    def __init__(self, m: int, n: int, hasWalls=True):
        self.n = n
        self.m = m
        self.totalnodes = (n + 1) * (m + 1)
        self.world: List[List[Cell]] = [
            [Cell(i, j, hasWalls) for j in range(m)] for i in range(n)
        ]
        ctr = 0
        self.agent_x, self.agent_y = (-1, -1)
        self.end_x, self.end_y = (-1, -1)
        print(f"{ctr} nodes created")

    def get_position(self) -> Cell:
        return self.world[self.agent_x][self.agent_y]

    def update_position(self, agent: Cell):
        self.agent_x, self.agent_y = agent.x, agent.y

    def set_end(self, end: Cell) -> None:
        self.end_x, self.end_y = end.x, end.y

    def get_end(self):
        return self.world[self.end_x][self.end_y]

    def update_walls(self, other_maze: "MazeArray", cell: Cell) -> None:
        def is_valid(x: int, y: int):
            return 0 <= x < self.n and 0 <= y < self.m

        self.world[cell.x][cell.y].blocked = cell.blocked

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            if is_valid(cell.x + dx, cell.y + dy):
                self.world[cell.x + dx][cell.y + dy].blocked = other_maze.world[
                    cell.x + dx
                ][cell.y + dy].blocked

    def valid_move(self, next_pos: Cell) -> bool:
        if abs(self.agent_x - next_pos.x) + abs(self.agent_y - next_pos.y) != 1:
            return False
            # raise Exception("Cannot Move: {otherCell} not adjacent to self {currCell}")
        return not next_pos.blocked

    def __repr__(self):
        return str(self.world)

    def __str__(self):
        return "\n".join(
            "".join("⬛" if self.world[i][j].blocked else "⬜" for j in range(self.m))
            for i in range(self.n)
        )


def read_maze(file):
    pass


def write_maze(maze, file):
    pass
