from maze_generation import create_maze, dfs, create_position
from a_star_search import a_star
from maze import MazeArray, Cell

def main():
    world = create_maze(100, 100, isRandom=False)
    fog = create_maze(world.m, world.n, hasWalls=False)
    fog.set_boundary_walls()
    dfs(world)

    # setting start
    start = create_position(world)
    world.update_position(start)
    fog.update_position(start)
    fog.update_walls(world, start)
    print(fog.cell_at(start.get_pos()).walls)

    # setting end
    end = create_position(world)
    world.set_end(end)
    fog.set_end(end)

    #print(world)
    #print(fog)

    curr_trajectory = a_star(fog, fog.get_position(), fog.get_end())
    path_taken = [start]

    while curr_trajectory:
        for nextMove in curr_trajectory[1::]:
            if world.valid_move(nextMove):
                fog.update_walls(world, world.cell_at(nextMove.get_pos()))
                fog.update_position(fog.cell_at(nextMove.get_pos()))
                path_taken.append(nextMove)
                world.update_position(world.cell_at(nextMove.get_pos()))
                #print(world)
                #print(fog)
            else:
                break
        curr_trajectory = a_star(fog, fog.get_position(), fog.get_end())
        if len(curr_trajectory)<=1:
            break

    #print(fog)
    #print(path_taken)
    print(len(path_taken))

def debug():
    world = create_maze(400, 400, isRandom=False)
    dfs(world)
    start = create_position(world)
    world.update_position(start)
    end = create_position(world)
    world.set_end(end)
    #print(world)
    curr_trajectory = a_star(world, world.get_position(), world.get_end())
    #print(curr_trajectory)




main()
#debug()
