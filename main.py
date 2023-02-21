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
    
    create_mazes(101, 2)
    forward_a_star(2)
    #backward_a_star(1)


def debug():
    pass

def create_mazes(size, id):
    world = create_maze(size, size, isRandom=False)
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

    curr_trajectory, total_expanded_cells = a_star(fog, fog.get_position(), fog.get_end())
    path_taken = [world.get_position()]

    while curr_trajectory:
        for nextMove in curr_trajectory[1::]:
            if world.valid_move(nextMove):
                fog.update_walls(world, world.cell_at(nextMove.get_pos()))
                fog.update_position(fog.cell_at(nextMove.get_pos()))
                path_taken.append(nextMove)
                world.update_position(world.cell_at(nextMove.get_pos()))
                #print(fog)
            else:
                break
        curr_trajectory, expanded_cells = a_star(fog, fog.get_position(), fog.get_end())
        total_expanded_cells+=expanded_cells
        if len(curr_trajectory)<=1:
            break

    #print(fog)
    #print(path_taken)
    print(f'Total Expanded Cells: {total_expanded_cells}')
    print(f'Path Length: {len(path_taken)}')

def backward_a_star(id):
    world = read_maze(f'./assets/world{id}.pickle')
    fog = read_maze(f'./assets/fog{id}.pickle')

    #print(world)
    #print(fog)

    curr_trajectory, total_expanded_cells = a_star(fog, fog.get_end(), fog.get_position())
    curr_trajectory.reverse()
    path_taken = [world.get_position()]

    while curr_trajectory:
        for nextMove in curr_trajectory[1::]:
            if world.valid_move(nextMove):
                fog.update_walls(world, world.cell_at(nextMove.get_pos()))
                fog.update_position(fog.cell_at(nextMove.get_pos()))
                path_taken.append(nextMove)
                world.update_position(world.cell_at(nextMove.get_pos()))
                #print(fog)
            else:
                break
        curr_trajectory, expanded_cells = a_star(fog, fog.get_end(), fog.get_position())
        total_expanded_cells+=expanded_cells
        curr_trajectory.reverse()
        if len(curr_trajectory)<=1:
            break

    #print(fog)
    #print(path_taken)
    print(f'Total Expanded Cells: {total_expanded_cells}')
    print(f'Path Length: {len(path_taken)}')

def adaptive_a_star(id):
    world = read_maze(f'./assets/world{id}.pickle')
    fog = read_maze(f'./assets/fog{id}.pickle')

    #print(world)
    #print(fog)

    curr_trajectory, total_expanded_cells = a_star(fog, fog.get_position(), fog.get_end())
    path_taken = [world.get_position()]
    

    while curr_trajectory:
        # ADAPTIVE A* MODIFICATION (truncated)
        #curr_trajectory[0].h = len(curr_trajectory)
        #traversed_length = 1

        # ADAPTIVE A* MODIFICATION
        travlen = 0
        for cell in curr_trajectory:
            cell.h = max(len(curr_trajectory)-travlen, cell.h)
            travlen += 1

        for nextMove in curr_trajectory[1::]:
            if world.valid_move(nextMove):
                fog.update_walls(world, world.cell_at(nextMove.get_pos()))
                fog.update_position(fog.cell_at(nextMove.get_pos()))
                path_taken.append(nextMove)
                world.update_position(world.cell_at(nextMove.get_pos()))
                #print(fog)
                # ADAPTIVE A* MODIFICATION (truncated)
                #nextMove.h = len(curr_trajectory)-traversed_length
            else:
                break
        curr_trajectory, expanded_cells = a_star(fog, fog.get_position(), fog.get_end())
        total_expanded_cells+=expanded_cells
        if len(curr_trajectory)<=1:
            break

    #print(fog)
    #print(path_taken)
    print(f'Total Expanded Cells: {total_expanded_cells}')
    print(f'Path Length: {len(path_taken)}')


main()