import random
from PIL import Image, ImageDraw


# проверка выиграна ли партия
def is_win(matrics):
    for i in range(3):
        if matrics[i][0] == matrics[i][1] == matrics[i][2] != 0:
            return True
        if matrics[0][i] == matrics[1][i] == matrics[2][i] != 0:
            return True
    if matrics[0][0] == matrics[1][1] == matrics[2][2] != 0:
        return True
    elif matrics[0][2] == matrics[1][1] == matrics[2][0] != 0:
        return True
    return False


# передается матрица поля ох( где 2-х, а 1-о ) для создания визуального представления поля
def table_xo(matrics):
    im = Image.new("RGB", (408, 408))
    drawer = ImageDraw.Draw(im)
    for i in range(3):
        for j in range(3):
            if matrics[i][j] == 1:
                drawer.arc(((50 + j * 104, 50 + i * 104), (150 + j * 104, 150 + i * 104)), start=0, end=360,
                           fill='blue', width=8)
            elif matrics[i][j] == 2:
                drawer.line((50 + j * 104, 50 + i * 104, 150 + j * 104, 150 + i * 104), fill=(255, 0, 0), width=8)
                drawer.line((150 + j * 104, 50 + i * 104, 50 + j * 104, 150 + i * 104), fill=(255, 0, 0), width=8)
    drawer.rectangle(((150, 50), (154, 358)), fill='white')
    drawer.rectangle(((254, 50), (258, 358)), fill='white')
    drawer.rectangle(((50, 150), (358, 154)), fill='white')
    drawer.rectangle(((50, 254), (358, 258)), fill='white')
    im.save('data/im.png')


def has_a_wining_move(bo, le):
    for i in range(3):
        # проверяем есть ли выйгрышь по горизагтали (тут скорее всего можно было сделать лучше но я тупой)
        # если да то возвращаем True и координаты выйгрышной позиции
        if bo[i][0] == bo[i][1] == le and bo[i][2] == 0:
            return True, (i, 2)
        if bo[i][0] == bo[i][2] == le and bo[i][1] == 0:
            return True, (i, 1)
        if bo[i][1] == bo[i][2] == le and bo[i][0] == 0:
            return True, (i, 0)

    for i in range(3):
        # проверяем есть ли выйгрышь по вертикале если да то возвращаем True и координаты выйгрышной позиции
        if bo[0][i] == bo[1][i] == le and bo[2][i] == 0:
            return True, (2, i)
        if bo[0][i] == bo[2][i] == le and bo[1][i] == 0:
            return True, (1, i)
        if bo[1][i] == bo[2][i] == le and bo[0][i] == 0:
            return True, (0, i)

    # проверяем есть ли выйгрышь по 1 диоганали если да то возвращаем True и координаты выйгрышной позиции
    if bo[0][0] == bo[1][1] == le and bo[2][2] == 0:
        return True, (2, 2)
    if bo[2][2] == bo[1][1] == le and bo[0][0] == 0:
        return True, (0, 0)
    if bo[0][0] == bo[2][2] == le and bo[1][1] == 0:
        return True, (1, 1)
    # проверяем есть ли выйгрышь по 2 диоганали если да то возвращаем True и координаты выйгрышной позиции
    if bo[0][2] == bo[1][1] == le and bo[2][0] == 0:
        return True, (2, 0)
    if bo[2][0] == bo[1][1] == le and bo[0][2] == 0:
        return True, (0, 2)
    if bo[0][0] == bo[0][2] == le and bo[1][1] == 0:
        return True, (1, 1)

    # проверяем есть нет не одной выигрышной позиции мы вохвращаем False и None
    return False, None


def TicTacToeAI(board, letter):  # help me pls Dasha is forcing me to do this i just want to do a ray castong maze
    possible = []
    for y, raw in enumerate(board):
        for x, le in enumerate(raw):
            if le == 0:
                possible.append((y, x))  # находим все возможные ходы и записываем в список

    has_a_win, win_pos = has_a_wining_move(board, letter)

    if has_a_win:  # если мы можем выйграть мы выиграваем                  ༼ つ ◕_◕ ༽つ да ладно
        # (я тут скорее всего совершил 100 грамотических ошибок но мне лень гуглить)
        return win_pos
    other_letter = 3 - letter  # так как у нас вместо X и O 2 и 1 то найти знак противника можно вычев свой знак из 3
    has_a_win, win_pos = has_a_wining_move(board, other_letter)  # проверяем может ли следующим ходом выиграть противник
    if has_a_win:
        return win_pos  # если да то блокируем

    corner = []
    for i in possible:
        if i in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            # если не мы не ппротивник не могут выиграть следующим ходом то мы проверяем можем ли мы воткнутся в угол
            corner.append(i)

    if len(corner) > 0:
        return random.choice(corner)  # если есть свободные углы то берём рандомный чтобы игры неебыли одинаковые

    if (1, 1) in possible:  # если нет углов то смотрим можем ли мы воткнутся в серидину
        return 1, 1  # если можем втыкаемся

    edges = []
    for i in possible:  # если нет углов то мы проверяем можем ли мы воткнутся в края
        if i in [(1, 0), (0, 1), (1, 2), (2, 1)]:
            edges.append(i)

    if len(edges) > 0:
        return random.choice(possible)  # рандомный край го бррррррррррррррррррр
    else:
        return None  # если ничего не получилось возвращаем None но в таких случаях либо я либо Даша затупили
