from telegram import ReplyKeyboardMarkup
from maze_generation import new_map
from map_game import change_level
from level_maps import level_num
from player_move import *
from ray_casting import ray_casting

# TOKEN = '5116714628:AAEoIs6Lfm6MwqxSNdB4usb6fMYL_GcOYAQ'
reply_keyboard_walking = [['w'],
                          ['a', 's', 'd'],
                          ['l', 'r'],
                          ['/end_play']]
reply_keyboard_level = [['да', 'нет']]
# print(reply_keyboard_level)
markup_walking = ReplyKeyboardMarkup(reply_keyboard_walking, one_time_keyboard=False)
markup_level = ReplyKeyboardMarkup(reply_keyboard_level, one_time_keyboard=True)

maze_mode = "not_active"


def maze_start(update, context):
    global maze_mode
    maze_mode = "changing_level"
    new_level(update, context)


def new_level(update, context):
    global maze_mode
    maze_mode = "changing_level"
    update.message.reply_text(
        f'выбери уровень с 1 по {level_num}.\n для смена уровня просто пиши цифру.')


# прверка команд и возвращаем позицию и напровлени
def text_to_command_maze(text, player_pos, player_angle, world_map):
    if text == "w":  # вперед
        return move_forward(player_pos, player_angle, world_map)
    elif text == "s":  # назад
        return move_back(player_pos, player_angle, world_map)
    elif text == "d":  # вправо
        return move_right(player_pos, player_angle, world_map)
    elif text == "a":  # влево
        return move_left(player_pos, player_angle, world_map)
    elif text == "l":  # поворот в лево
        player_angle -= 1
        player_angle %= 4
        return player_pos, player_angle
    elif text == "r":  # поворот вправо
        player_angle += 1
        player_angle %= 4
        return player_pos, player_angle
    else:
        return None, None
