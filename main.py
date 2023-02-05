from maze_generation import create_maze, dfs, rand_position
from a_star_search import a_star


def main():
    maze = create_maze(70, 70, isRandom=False)
    print(maze)
    fog = create_maze(maze.m, maze.n, hasWalls=False)
    dfs(maze)
    print(maze)

    # setting start
    start = rand_position(maze)
    maze.update_position(start)
    fog.update_position(start)
    fog.update_walls(maze, start)
    # print(fog.cell_at(start.get_pos()).walls)

    # setting end
    end = rand_position(maze, unallowed=start)
    maze.set_end(end)
    fog.set_end(end)

    # print(world)
    # print(fog)

    curr_trajectory = a_star(fog, fog.get_position(), fog.get_end())
    path_taken = [start]

    from datetime import datetime, timedelta

    tot = timedelta()
    iters = 0

    while curr_trajectory:
        iters += 1
        for next_move in curr_trajectory[1::]:
            if maze.valid_move(next_move):
                fog.update_walls(maze, maze.world[next_move.x][next_move.y])
                fog.update_position(fog.world[next_move.x][next_move.y])
                path_taken.append(next_move)
                maze.update_position(maze.world[next_move.x][next_move.y])
            else:
                break
        start = datetime.now()
        curr_trajectory = a_star(fog, fog.get_position(), fog.get_end())
        tot += datetime.now() - start
        if len(curr_trajectory) <= 1:
            break

    # print(fog)
    # print(path_taken)
    # print(len(path_taken))
    print(tot)
    print(iters)


import cProfile

with cProfile.Profile() as pr:
    main()
    filename = "profile.prof"
    pr.dump_stats(filename)
