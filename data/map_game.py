import random
from maze_generation import new_map
from settings import *
from level_maps import *

world_map = set()
wall_type_map = dict()

fin_pos = (0, 0)


def map_layout(text_map):  # создание карты из tile карты
    player_pos = [0, 0]
    world_map = set()
    wall_type_map = dict()
    for j, row in enumerate(text_map):
        for i, char in enumerate(row):
            if char == 'P':
                player_pos[0] = i * TILE + TILE // 2
                player_pos[1] = j * TILE + TILE // 2
            elif char == 'F':
                fin_pos = (i * TILE, j * TILE)
            elif char != '.':
                world_map.add((i * TILE, j * TILE))
                wall_type_map[str((i * TILE, j * TILE))] = random.randint(1, 5)
        text_map[j] = text_map[j].replace(".", "e")
    return player_pos, fin_pos, world_map, wall_type_map, text_map


def change_level():
    return map_layout(new_map())

# map_layout(maps["level_4_map"])
# print('"level 1": {', end="")
# print('"wall_map":', world_map)
# print('"type_map":', wall_type_map)
# print('"fin_pos":', fin_pos, end="},")
