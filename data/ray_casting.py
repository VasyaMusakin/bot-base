from PIL import Image, ImageDraw

from color import Color
from settings import *
from level_maps import *

color_manager = Color()


# Как сделать 3D Игру на Python с Нуля [ Pygame ]
# https://www.youtube.com/watch?v=SmKBsArp2dI&t=768s
# туториал по рай кастинг я его раз 7 смортел там всё очень првельно расказывается
def ray_casting(player_pos, player_angle, world_map, wall_type_map, fin_pos):
    new_image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)) # создаём картинку которую потом можно отсылать
    draw = ImageDraw.Draw(new_image)
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos

    if (xo - TILE // 2, yo - TILE // 2) == fin_pos:
        return True
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            # pygame.draw.line(sc, DARKGRAY, player_pos, (x, y), 2)
            if (x // TILE * TILE, y // TILE * TILE) == fin_pos: # если финишь
                depth *= math.cos(player_angle - cur_angle)
                proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
                color = (255, 255, 255)
                # print(ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
                draw.rectangle(
                    ((int(ray * SCALE), int(HALF_HEIGHT - proj_height // 2)),
                     (int(ray * SCALE + SCALE), int(HALF_HEIGHT - proj_height // 2 + proj_height))),
                    color)
                break
            elif (x // TILE * TILE, y // TILE * TILE) in world_map: # просто стена
                depth *= math.cos(player_angle - cur_angle)
                proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
                c = 255 / (1 + depth * depth * 0.0001)
                num = wall_type_map[str((int(x // TILE * TILE), int(y // TILE * TILE)))] # смотрим какой цвет
                color = color_manager.chek(num, c)
                # print(ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
                draw.rectangle(
                    ((int(ray * SCALE), int(HALF_HEIGHT - proj_height // 2)),
                     (int(ray * SCALE + SCALE), int(HALF_HEIGHT - proj_height // 2 + proj_height))),
                    color)
                break
        cur_angle += DELTA_ANGLE
    new_image.save("data/ray_casting_im.png") # сохраняем
    return False
