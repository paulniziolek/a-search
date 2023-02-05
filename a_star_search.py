from typing import Generator, List, Tuple
from maze import MazeArray, Cell
import heapq

def a_star(maze: MazeArray, start: Cell, end: Cell):
    m, n = maze.m, maze.n

    # manhattan distance heuristic from node to end
    def heuristic(node: Cell) -> int:
        return abs(node.x-end.x)+abs(node.y-end.y)
    
    # a position is valid when it is inside the grid and is unblocked
    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < n and 0 <= y < m and not maze.world[x][y].blocked

    # fills neighbors with valid maze Cells
    # a neighbor is valid when it is inside the grid, directly next to its origin cell, and does not have a wall between its origin cell. 
    def get_valid_neighbors(cell: Cell) -> Generator[Cell, None, None]:
        for dx, dy in ((0,-1), (0,1), (-1, 0), (1, 0)):  # for four possible neighbors
            if is_valid(cell.x + dx, cell.y + dy):
                yield maze.world[cell.x + dx][cell.y + dy]
        #print(f"neighbors of {cell} are {unverified_neighbors}") # debugging neighbors

    # A* Algorithm logic follows:
    closed_list = {} # hashmap with key=cell, and val=smallest f(n)
    path = {} # hashmap with key=currNode and val=prevNode, for pathing
    open_list: List[Tuple[int, Cell]] = [(heuristic(start), start)] # will store cells in the open_list heap by tuple (h(n), n)
    heapq.heapify(open_list)

    while open_list:
        fn, node= heapq.heappop(open_list) # fn holds the evaluation result of node. to get g(n), you can subtract fn - heuristic(node).
        if node==end:
            break

        neighbors = get_valid_neighbors(node)
        # g(new n) = fn-heuristic(n)+1, AND h(new n) = heuristic(new n). 
        neighbors = list(map(lambda x: (fn-heuristic(node)+1+heuristic(x), x), neighbors)) # returns list of (f(new n), new n)

        if node in closed_list:
            if closed_list[node] > fn:
                closed_list[node] = fn
        else: closed_list[node] = fn

        # updating neighbors with closed/open lists
        for fN, neighbor in neighbors:
            if neighbor in closed_list:
                if closed_list[neighbor] > fN:
                    closed_list[neighbor] = fN
                    path[neighbor] = node
                else: continue
            heapq.heappush(open_list, (fN, neighbor))
            path[neighbor] = node
        """
        # debugging
        print("open list:")
        print(open_list)
        print(closed_list)
        print(path)
        """

    # creating path as list
    ptr: Cell = end
    realpath: list[Cell] = [ptr]
    while ptr != start:
        realpath.append(path[ptr])
        ptr = path[ptr]
    realpath.reverse()
    return realpath



