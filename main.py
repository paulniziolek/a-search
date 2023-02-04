from maze_generation import create_maze, dfs, create_position
from a_star_search import a_star
from maze import MazeArray, Cell

mymaze = create_maze(25, 25)
dfs(mymaze)
print(mymaze)
start = create_position(mymaze)
end = create_position(mymaze)

start = mymaze.cell_at((0, 0))
end = mymaze.cell_at((24, 24))

print(f"PATH FROM {start} TO {end} IS: ")
mypath = a_star(mymaze, start, end)
print(mymaze)
print(mypath)
print(len(mypath))