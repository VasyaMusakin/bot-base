import random

TILE = 100

wall_char = 'w'
cell = '.'
unvisited = 'u'
height = 9
width = 13
maze = [list(unvisited * width) for i in range(height)]

starting_height = int(random.randint(1, height - 2))
starting_width = int(random.randint(1, width - 2))
maze[starting_height][starting_width] = cell
walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
         [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

# Denote walls in maze
maze[starting_height - 1][starting_width] = wall_char
maze[starting_height][starting_width - 1] = wall_char
maze[starting_height][starting_width + 1] = wall_char
maze[starting_height + 1][starting_width] = wall_char
world_map = set()
for i in walls:
    world_map.add((i[0] * TILE, i[1] * TILE))


def printMaze(maze):
    for i in range(height):
        for j in range(width):
            print(maze[i][j], end=" ")
        print()


# Find number of surrounding cells
def surroundingCells(rand_wall):
    return int(maze[rand_wall[0]][rand_wall[1] + 1] == cell) + int(maze[rand_wall[0]][rand_wall[1] - 1] == cell) + int(
        maze[rand_wall[0] + 1][rand_wall[1]] == cell) + int(maze[rand_wall[0] - 1][rand_wall[1]] == cell)


def upper(rand_wall):
    if rand_wall[0] != 0:
        if maze[rand_wall[0] - 1][rand_wall[1]] != cell:
            maze[rand_wall[0] - 1][rand_wall[1]] = wall_char
            world_map.add(((rand_wall[0] - 1) * TILE, rand_wall[1] * TILE))
        if [rand_wall[0] - 1, rand_wall[1]] not in walls:
            walls.append([rand_wall[0] - 1, rand_wall[1]])
            # print(rand_wall[0] - 1, rand_wall[1])


def bottom(rand_wall):
    if rand_wall[0] != height - 1:
        if maze[rand_wall[0] + 1][rand_wall[1]] != cell:
            maze[rand_wall[0] + 1][rand_wall[1]] = wall_char
            world_map.add(((rand_wall[0] + 1) * TILE, rand_wall[1] * TILE))
        if [rand_wall[0] + 1, rand_wall[1]] not in walls:
            walls.append([rand_wall[0] + 1, rand_wall[1]])


def left(rand_wall):
    if rand_wall[1] != 0:
        if maze[rand_wall[0]][rand_wall[1] - 1] != cell:
            maze[rand_wall[0]][rand_wall[1] - 1] = wall_char
            world_map.add((rand_wall[0] * TILE, (rand_wall[1] - 1) * TILE))
        if [rand_wall[0], rand_wall[1] - 1] not in walls:
            walls.append([rand_wall[0], rand_wall[1] - 1])


def right(rand_wall):
    if rand_wall[1] != width - 1:
        if maze[rand_wall[0]][rand_wall[1] + 1] != cell:
            maze[rand_wall[0]][rand_wall[1] + 1] = wall_char
            world_map.add((rand_wall[0] * TILE, (rand_wall[1] + 1) * TILE))
        if [rand_wall[0], rand_wall[1] + 1] not in walls:
            walls.append([rand_wall[0], rand_wall[1] + 1])


def new_map():
    global maze, starting_height, starting_width, walls, wall, world_map
    maze = [list(unvisited * width) for i in range(height)]
    starting_height = int(random.randint(1, height - 2))
    starting_width = int(random.randint(1, width - 2))
    maze[starting_height][starting_width] = cell
    walls = [[starting_height - 1, starting_width], [starting_height, starting_width - 1],
             [starting_height, starting_width + 1], [starting_height + 1, starting_width]]

    # Denote walls in maze
    maze[starting_height - 1][starting_width] = wall_char
    maze[starting_height][starting_width - 1] = wall_char
    maze[starting_height][starting_width + 1] = wall_char
    maze[starting_height + 1][starting_width] = wall_char
    world_map = set()
    for i in walls:
        world_map.add((i[0] * TILE, i[1] * TILE))

    while walls:
        rand_wall = walls[int(random.random() * len(walls)) - 1]
        if rand_wall[1] != 0:
            if maze[rand_wall[0]][rand_wall[1] - 1] == unvisited and maze[rand_wall[0]][rand_wall[1] + 1] == cell:
                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    if (rand_wall[0], rand_wall[1]) in world_map:
                        world_map.remove((rand_wall[0], rand_wall[1]))
                    upper(rand_wall)
                    bottom(rand_wall)
                    left(rand_wall)
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)
                continue
        if rand_wall[0] != 0:
            if maze[rand_wall[0] - 1][rand_wall[1]] == unvisited and maze[rand_wall[0] + 1][rand_wall[1]] == cell:
                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    if (rand_wall[0], rand_wall[1]) in world_map:
                        world_map.remove((rand_wall[0], rand_wall[1]))
                    upper(rand_wall)
                    left(rand_wall)
                    right(rand_wall)
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)
                continue
        if rand_wall[0] != height - 1:
            if maze[rand_wall[0] + 1][rand_wall[1]] == unvisited and maze[rand_wall[0] - 1][rand_wall[1]] == cell:
                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    if (rand_wall[0], rand_wall[1]) in world_map:
                        world_map.remove((rand_wall[0], rand_wall[1]))
                    bottom(rand_wall)
                    left(rand_wall)
                    right(rand_wall)
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)
                continue
        if rand_wall[1] != width - 1:
            if maze[rand_wall[0]][rand_wall[1] + 1] == unvisited and maze[rand_wall[0]][rand_wall[1] - 1] == cell:
                s_cells = surroundingCells(rand_wall)
                if s_cells < 2:
                    maze[rand_wall[0]][rand_wall[1]] = cell
                    if (rand_wall[0], rand_wall[1]) in world_map:
                        world_map.remove((rand_wall[0], rand_wall[1]))
                    right(rand_wall)
                    bottom(rand_wall)
                    upper(rand_wall)
                for wall in walls:
                    if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                        walls.remove(wall)
                continue
        for wall in walls:
            if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
                walls.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(height):
        for j in range(width):
            if maze[i][j] == unvisited:
                maze[i][j] = wall_char
                world_map.add((i * TILE, j * TILE))
    # Set entrance and exit

    for i in range(width):
        if maze[1][i] == cell:
            maze[1][i] = 'P'
            break

    for i in range(width - 1, 0, -1):
        if maze[height - 2][i] == cell:
            maze[height - 2][i] = 'F'
            break
    text_maze = []
    for i in range(height):
        text_maze.append("")
        for j in range(width):
            text_maze[-1] += maze[i][j]
    # for i in text_maze:
    #     print(i)
    return text_maze