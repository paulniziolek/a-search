from maze_generation import create_maze, dfs, create_position
from a_star_search import a_star
from maze import read_maze, write_maze

# TO DO: 
# Implement script for generating mazes
# Implement function for repeated forward/backward/adaptive A*

def main():

    """
    # Creates 50 mazes in ./assets
    for i in range(1, 51):
        create_mazes(i)
    """
    
    #create_mazes(51)
    #forward_a_star(51)
    backward_a_star(51)


def debug():
    pass

def create_mazes(id):
    world = create_maze(101, 101, isRandom=False)
    fog = create_maze(world.m, world.n, hasWalls=False)
    fog.set_boundary_walls()
    dfs(world)

    # setting start
    start = create_position(world)
    world.update_position(start)
    fog.update_position(start)
    fog.update_walls(world, start)

    # setting end
    end = create_position(world)
    world.set_end(end)
    fog.set_end(end)

    # file paths
    file1 = f'./assets/world{id}.pickle'
    file2 = f'./assets/fog{id}.pickle'

    write_maze(world, file1)
    write_maze(fog, file2)

def forward_a_star(id):
    world = read_maze(f'./assets/world{id}.pickle')
    fog = read_maze(f'./assets/fog{id}.pickle')

    #print(world)
    #print(fog)

    curr_trajectory = a_star(fog, fog.get_position(), fog.get_end())
    path_taken = [world.get_position()]

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

def backward_a_star(id):
    world = read_maze(f'./assets/world{id}.pickle')
    fog = read_maze(f'./assets/fog{id}.pickle')

    #print(world)
    #print(fog)

    curr_trajectory = a_star(fog, fog.get_end(), fog.get_position())
    curr_trajectory.reverse()
    path_taken = [world.get_position()]

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
        curr_trajectory = a_star(fog, fog.get_end(), fog.get_position())
        curr_trajectory.reverse()
        if len(curr_trajectory)<=1:
            break

    #print(fog)
    #print(path_taken)
    print(len(path_taken))




main()