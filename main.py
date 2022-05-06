from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from data import db_session
from data.users import User
from data.results import Results
from data.cities import city
from data.main import *
from data.xo import table_xo, TicTacToeAI, is_win
from os import remove
# подключение к базе данных, определение "флагов"
db_session.global_init("db/bot.db")
db_sess = db_session.create_session()
now = {}
now_for_game = {}


# проверка пользователя
def check(update, context):
    global now, now_for_game
    if update.message.from_user.id not in now.keys():
        now[update.message.from_user.id] = ''
    if update.message.from_user.id not in now_for_game.keys():
        now_for_game[update.message.from_user.id] = ''


# функция для переадрессации на нужную
def echo(update, context):
    global now
    check(update, context)
    update.message.reply_text(f'Ответьте пожалуйста на сообщение.')
    if now[update.message.from_user.id] == 'start':
        return start(update, context)
    elif now[update.message.from_user.id] == 'e_p':
        return end_play(update, context)
    elif now[update.message.from_user.id] == '':
        return stop(update, context)
    elif now[update.message.from_user.id] == 'menu':
        return menu(update, context)
    elif 'cities' in now[update.message.from_user.id]:
        return cities(update, context)
    elif 'rating' in now[update.message.from_user.id]:
        return rating(update, context)
    elif 'maze' in now[update.message.from_user.id]:
        return maze(update, context)


# команда /start
def start(update, context):
    global now, db_sess
    check(update, context)
    # проверка, есть ли уже пользователь в базе данных
    a = [i.id_tg for i in db_sess.query(User).all()]
    if update.message.from_user.id not in a:
        # если нет, добавляем
        user = User()
        user.id_tg = update.message.from_user.id
        user.username = update.message.from_user.username
        if user.username is None:
            user.username = str(update.message.from_user.id)
        db_sess.add(user)
        result = Results(user=user)
        db_sess.add(result)
        db_sess.commit()
    # когда бот ещё не активирован
    if now[update.message.from_user.id] == '':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Я бот с играми. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'start'
    # если бот уже включен, но коменд ещё не было
    elif now[update.message.from_user.id] == 'start':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Бот уже активирован 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
    # команда активирована, когда пользователь уже использует бота
    else:
        update.message.reply_text(f'''Бот уже активирован.''')
        echo(update, context)


# команда выключения бота
def stop(update, context):
    global now, now_for_game
    check(update, context)
    # если бота можно выключить
    if now[update.message.from_user.id] != '':
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Бот выключен. Спасибо за игру. 
    Чтобы заново активировать бота нажмите - /start''',
            reply_markup=markup)
        now[update.message.from_user.id] = ''
        now_for_game[update.message.from_user.id] = ''
    # если он уже выключен
    else:
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Бот выключен. 
    Чтобы активировать бота нажмите - /start''',
            reply_markup=markup)


# закончить игру
def end_play(update, context):
    global now, now_for_game
    check(update, context)
    # если игра активирована
    if 'xo' in now[update.message.from_user.id] or 'maze' in now[
        update.message.from_user.id] or 'cities' in now[update.message.from_user.id]:
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Игра досрочно завершена. Результаты не занесены в рейтинг. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'e_p'
        now_for_game[update.message.from_user.id] = ''
    # если игры закончены, но команд больше не было
    elif now[update.message.from_user.id] == 'e_p':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Игра уже завершена. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
    # если игра не включена
    else:
        update.message.reply_text(f'''Вы ещё не начали играть.''')
        echo(update, context)


# меню
def menu(update, context):
    global now
    check(update, context)
    # если можно открыть меню
    if now[update.message.from_user.id] in ['menu', 'start', 'e_p', 'rating'] or 'rating' in now[
        update.message.from_user.id]:
        reply_keyboard = [['/cities', '/maze', '/xo'], ['/rating'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Выберите игру: 
    города - /cities 
    крестики-нолики - /xo 
    лабиринт - /maze 
    
    Посмотреть рейтинг - /rating 
    Выключить бота - /stop ''',
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'menu'
    # если нельзя
    else:
        update.message.reply_text(f'''В данный момент нельзя открыть меню.''')
        echo(update, context)


# игра крестики-нолики
def xo(update, context):
    global now, now_for_game
    check(update, context)
    # когда возможно запустить игру
    if now[update.message.from_user.id] in ['menu', 'start', 'e_p', 'rating'] or 'rating' in now[
        update.message.from_user.id]:
        reply_keyboard = [['o'], ['x'], ['нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''В этой игре вам нужно обыграть бота в крестики-нолики. 
    Чтобы сделать ход пришлите 2 цифры через пробел: первая - строчка, вторая - столбец. Пример:
    1 1
    2 3
    и тд. 
    Если захотите досрочно окончить игру нажмите - /end_play
        Вы хотите начать игру? Если да, выберите свой знак.''', reply_markup=markup)
        now[update.message.from_user.id] = 'xo'
    # ход игрока
    elif now[update.message.from_user.id] == 'xo 1':
        table_xo(now_for_game[update.message.from_user.id][0])
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open('data/im.png', 'rb'))
        remove('data/im.png')
        reply_keyboard = [['/end_play']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Сделайте ход''', reply_markup=markup)
        now[update.message.from_user.id] = 'xo 1'
    # ход бота
    elif now[update.message.from_user.id] == 'xo 2':
        if now_for_game[update.message.from_user.id][1] == 2:
            f = TicTacToeAI(now_for_game[update.message.from_user.id][0], 1)
            if f is None:
                now[update.message.from_user.id] = 'xo win n'
                return xo(update, context)
            now_for_game[update.message.from_user.id][0][f[0]][f[1]] = 1
        else:
            f = TicTacToeAI(now_for_game[update.message.from_user.id][0], 2)
            if f is None:
                now[update.message.from_user.id] = 'xo win s'
                return xo(update, context)
            now_for_game[update.message.from_user.id][0][f[0]][f[1]] = 2
        if is_win(now_for_game[update.message.from_user.id][0]):
            now[update.message.from_user.id] = 'xo win b'
        else:
            now[update.message.from_user.id] = 'xo 1'
        return xo(update, context)
    # обработка выигрыша и ничьи
    elif 'xo win' in now[update.message.from_user.id]:
        if 'u' in now[update.message.from_user.id]:
            update.message.reply_text(f'''Поздравляю, вы выигарли! Вы перенаправлены в меню.''')
            user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
            db_sess.query(Results).filter(Results.user_id == user.id).update(
                {'xo': Results.xo + 1, 'all': Results.all + 1})
            db_sess.commit()
        elif 'b' in now[update.message.from_user.id]:
            table_xo(now_for_game[update.message.from_user.id][0])
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('data/im.png', 'rb'))
            update.message.reply_text(f'''Бот выиграл. Вы перенаправлены в меню.''')
            remove('data/im.png')
        elif 's' in now[update.message.from_user.id]:
            table_xo(now_for_game[update.message.from_user.id][0])
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open('data/im.png', 'rb'))
            update.message.reply_text(f'''Ничья. Вы перенаправлены в меню.''')
            remove('data/im.png')
        now[update.message.from_user.id] = 'menu'
        now_for_game[update.message.from_user.id] = ''
        return menu(update, context)
    # если игру нельзя сейчас включить
    else:
        update.message.reply_text(f'''В данный момент нельзя начать играть в крестики-нолики.''')
        return echo(update, context)


# игра в города
def cities(update, context):
    global now, now_for_game
    check(update, context)
    # когда возможно запустить игру
    if now[update.message.from_user.id] in ['menu', 'start', 'e_p', 'rating',
                                            'cities'] or 'rating' in now[
        update.message.from_user.id]:
        reply_keyboard = [['да'], ['нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''В этой игре вам нужно угадать город по фотографии со спутника. 
Чтобы ответ засчитался, нужно вбивать название русскими буквами.
Если захотите досрочно окончить игру нажмите - /end_play
    Вы хотите начать игру?''', reply_markup=markup)
        now[update.message.from_user.id] = 'cities'
    # прислать пользователю изображение города со спутника
    elif now[update.message.from_user.id] == 'cities 1':
        spisok = city()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=spisok[0])
        reply_keyboard = [['/end_play']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Какой это город?''', reply_markup=markup)
        now_for_game[update.message.from_user.id] = spisok[1]
        now[update.message.from_user.id] = 'cities 2'
    # проверка верности ответа
    elif now[update.message.from_user.id] == 'cities 2':
        if update.message.text == now_for_game[update.message.from_user.id]:
            reply_keyboard = [['/end_play']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'''Верно. Идём дальше.''', reply_markup=markup)
            user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
            db_sess.query(Results).filter(Results.user_id == user.id).update(
                {'cities': Results.cities + 1, 'all': Results.all + 1})
            db_sess.commit()
            now[update.message.from_user.id] = 'cities 1'
            return cities(update, context)
        else:
            reply_keyboard = [['/end_play']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'''Неверно. Идём дальше.''', reply_markup=markup)
            now[update.message.from_user.id] = 'cities 1'
            return cities(update, context)
    # если игру нельзя сейчас включить
    else:
        update.message.reply_text(f'''В данный момент нельзя начать играть в города.''')
        return echo(update, context)


# лабиринт
def maze(update, context):
    global now, now_for_game
    check(update, context)
    # когда возможно запустить игру
    if now[update.message.from_user.id] in ['menu', 'start', 'e_p', 'rating', 'maze'] or 'rating' in now[
        update.message.from_user.id]:
        markup = ReplyKeyboardMarkup(reply_keyboard_level, one_time_keyboard=False)
        update.message.reply_text(f'''Играть?
    Если захотите окончить игру нажмите - /end_play
        Вы хотите начать игру?''', reply_markup=markup)  # выбор начального уровня
        now[update.message.from_user.id] = 'maze level'  # говорим что мы выьераем уровень

        now_for_game[update.message.from_user.id] = {"pos": [0, 0],
                                                     "angle": 0,
                                                     "map": list(),
                                                     "wall_type_map": dict(),
                                                     "world_map": set(),
                                                     "fin_pos": [0, 0]}
    # прислать пользователю изображение города со спутника
    elif now[update.message.from_user.id] == 'maze level':  # если выбор уровня

        player_pos, fin_pos, world_map, wall_type_map, maze = change_level()
        now_for_game[update.message.from_user.id]["map"] = maze  # обновляем значения карты
        now_for_game[update.message.from_user.id]["pos"] = list(player_pos)  # обновляем значения позиции
        now_for_game[update.message.from_user.id]["fin_pos"] = fin_pos
        now_for_game[update.message.from_user.id]["world_map"] = world_map
        now_for_game[update.message.from_user.id]["wall_type_map"] = wall_type_map
        now_for_game[update.message.from_user.id]["angle"] = 0  # обновляем значения напровлениея
        update.message.reply_text('уровень изменён')
        ray_casting(now_for_game[update.message.from_user.id]["pos"],  # вызываем функцию ray casting
                    ANGELES[now_for_game[update.message.from_user.id]["angle"]],
                    now_for_game[update.message.from_user.id]["world_map"],
                    now_for_game[update.message.from_user.id]["wall_type_map"],
                    now_for_game[update.message.from_user.id]["fin_pos"])
        update.message.reply_text(
            f"pos:{now_for_game[update.message.from_user.id]['pos']}\
angle:{now_for_game[update.message.from_user.id]['angle']}")  # пишем где песонаж
        context.bot.send_photo(update.message.chat_id, photo=open('data/ray_casting_im.png', 'rb'),
                               reply_markup=markup_walking)  # присылаем фото
        remove('data/ray_casting_im.png')  # удоляем фото
        now[update.message.from_user.id] = 'maze play'  # обозначаем что мы играем
    elif now[update.message.from_user.id] == 'maze play':  # если мы играем
        pos, angle = text_to_command_maze(update.message.text, now_for_game[update.message.from_user.id]["pos"],
                                          now_for_game[update.message.from_user.id]["angle"],
                                          now_for_game[update.message.from_user.id][
                                              "world_map"])  # смотрим прислал ли он команду движения
        if pos is not None and angle is not None:  # если да
            now_for_game[update.message.from_user.id]["pos"], now_for_game[update.message.from_user.id][
                "angle"] = pos, angle
            update.message.reply_text(
                f"pos:{now_for_game[update.message.from_user.id]['pos']}\
    angle:{now_for_game[update.message.from_user.id]['angle'] * 90}")
            did_we_win = ray_casting(now_for_game[update.message.from_user.id]["pos"],  # вызываем функцию ray casting
                                     ANGELES[now_for_game[update.message.from_user.id]["angle"]],
                                     now_for_game[update.message.from_user.id]["world_map"],
                                     now_for_game[update.message.from_user.id]["wall_type_map"],
                                     now_for_game[update.message.from_user.id]["fin_pos"])
            # проверяем выиграли мы. функция рай састинг возвращает True если да
            if did_we_win:
                user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
                db_sess.query(Results).filter(Results.user_id == user.id).update(
                    {'maze': Results.maze + 1, 'all': Results.all + 1})  # сохраняем райтинг
                db_sess.commit()
                update.message.reply_text(f"Крутой. Ты закончил уровень.",
                                          reply_markup=markup_level)  # говори что он красава
                now[update.message.from_user.id] = 'maze won'  # выбераем следующий уровнь
                return
            context.bot.send_photo(update.message.chat_id, photo=open('data/ray_casting_im.png', 'rb'),
                                   reply_markup=markup_walking)
            remove('data/ray_casting_im.png')
        else:
            update.message.reply_text(
                f"Испоьзуй команды. Если захотите окончить игру нажмите - /end_play",  # опять же говорим что он не прав
                reply_markup=markup_walking)

    else:
        update.message.reply_text(f'''В данный момент нельзя начать играть в лабиринт.  ༼ つ ◕_◕ ༽つ''')
        return echo(update, context)


# рейтинг
def rating(update, context):
    global now, now_for_game
    check(update, context)
    if now[update.message.from_user.id] in ['start', 'menu', 'e_p', 'rating']:
        reply_keyboard = [['maze', 'xo'], ['cities', 'all'], ['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Какой рейтинг вы хотите посомтреть?
    лабиринт - maze
    города - cities
    крестики-нолики - xo
    общий - all
Вернуться в меню - /menu''',
            reply_markup=markup)
        now[update.message.from_user.id] = 'rating'
    # общий рейтинг
    elif now[update.message.from_user.id] == 'rating all':
        stroka = 'Общий рейтинг:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: -x.all))[:5]:
            stroka += f'    {db_sess.query(User).filter(User.id == result.user_id).first().username}\t{result.all}\n'
        stroka += ' ' * 4 + '.' * 4 + '\n' + '-' * 10 + '\n'
        user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
        stroka += f'Ваш рейтинг:\t{user.username}\t' + \
                  f'{db_sess.query(Results).filter(Results.user_id == user.id).first().all}'
        stroka += '\nВернуться в меню - /menu'
        reply_keyboard = [['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(stroka,
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'rating'
    # Рейтинг по игре крестики-нолики
    elif now[update.message.from_user.id] == 'rating xo':
        stroka = 'Рейтинг по игре крестики-нолики:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: -x.xo))[:5]:
            stroka += f'    {db_sess.query(User).filter(User.id == result.user_id).first().username}\t{result.xo}\n'
        stroka += ' ' * 4 + '.' * 4 + '\n' + '-' * 10 + '\n'
        user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
        stroka += f'Ваш рейтинг:\t{user.username}\t' + \
                  f'{db_sess.query(Results).filter(Results.user_id == user.id).first().xo}'
        stroka += '\nВернуться в меню - /menu'
        reply_keyboard = [['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(stroka,
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'rating'
    # Рейтинг по лабиринту
    elif now[update.message.from_user.id] == 'rating maze':
        stroka = 'Рейтинг по лабиринту:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: -x.maze))[:5]:
            stroka += f'    {db_sess.query(User).filter(User.id == result.user_id).first().username}\t{result.maze}\n'
        stroka += ' ' * 4 + '.' * 4 + '\n' + '-' * 10 + '\n'
        user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
        stroka += f'Ваш рейтинг:\t{user.username}\t' + \
                  f'{db_sess.query(Results).filter(Results.user_id == user.id).first().maze}'
        stroka += '\nВернуться в меню - /menu'
        reply_keyboard = [['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(stroka,
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'rating'
    # Рейтинг по игре города
    elif now[update.message.from_user.id] == 'rating cities':
        stroka = 'Рейтинг по игре города:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: -x.cities))[:5]:
            stroka += f'    {db_sess.query(User).filter(User.id == result.user_id).first().username}\t{result.cities}\n'
        stroka += ' ' * 4 + '.' * 4 + '\n' + '-' * 10 + '\n'
        user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
        stroka += f'Ваш рейтинг:\t{user.username}\t' + \
                  f'{db_sess.query(Results).filter(Results.user_id == user.id).first().cities}'
        stroka += '\nВернуться в меню - /menu'
        reply_keyboard = [['/menu']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(stroka,
                                  reply_markup=markup)
        now[update.message.from_user.id] = 'rating'
    # если нельзя посмотреть сейчас рейтинг
    else:
        reply_keyboard = []
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Сейчас нельзя посмотреть рейтинг.''',
            reply_markup=markup)
        echo(update, context)


# обработка текстовых сообщений
def text(update, context):
    global now, now_for_game
    check(update, context)
    text = update.message.text.lower()
    # обработка в игре города
    if now[update.message.from_user.id] == 'cities':
        # хочет ли пользователь начать игру
        if 'yes' in text \
                or 'ok' in text \
                or 'yes' in text \
                or 'да' in text \
                or 'хорошо' in text:
            now[update.message.from_user.id] = 'cities 1'
            return cities(update, context)
        elif 'не' in text \
                or 'no' in text:
            now[update.message.from_user.id] = 'menu'
            return menu(update, context)
    # обработка в крестики-нолики
    elif now[update.message.from_user.id] == 'xo':
        # хочет ли пользователь начать игру
        if 'x' == text \
                or 'o' == text:
            now[update.message.from_user.id] = 'xo 1'
            b = 2
            if text == 'o':
                b = 1
            now_for_game[update.message.from_user.id] = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], b]
            return xo(update, context)
        elif 'не' in text \
                or 'no' in text:
            now[update.message.from_user.id] = 'menu'
            return menu(update, context)
    # правильно ли пользователь сделал ход
    elif now[update.message.from_user.id] == 'xo 1':
        spisok = text.split()
        if len(spisok) == 2 and all(map(lambda x: x.isdigit(), spisok)):
            spisok = [int(i) for i in spisok]
            if 0 < spisok[0] < 4 and 0 < spisok[1] < 4:
                if now_for_game[update.message.from_user.id][0][spisok[0] - 1][spisok[1] - 1] == 0:
                    now_for_game[update.message.from_user.id][0][spisok[0] - 1][spisok[1] - 1] = \
                        now_for_game[update.message.from_user.id][1]
                    if is_win(now_for_game[update.message.from_user.id][0]):
                        now[update.message.from_user.id] = 'xo win u'
                    else:
                        now[update.message.from_user.id] = 'xo 2'
                else:
                    update.message.reply_text('Неверный ход.')
            else:
                update.message.reply_text('Неверный ход.')
        else:
            update.message.reply_text('Неверный ход.')
        return xo(update, context)
    # обработка в рейтинг, какой конкретно показать
    elif now[update.message.from_user.id] == 'maze':
        if 'yes' in text \
                or 'ok' in text \
                or 'yes' in text \
                or 'да' in text \
                or 'хорошо' in text:
            now[update.message.from_user.id] = 'maze level'
            return maze(update, context)
        elif 'не' in text \
                or 'no' in text:
            now[update.message.from_user.id] = 'menu'
            return menu(update, context)
    elif now[update.message.from_user.id] == 'maze won':
        if 'yes' in text \
                or 'ok' in text \
                or 'yes' in text \
                or 'да' in text \
                or 'хорошо' in text:
            now[update.message.from_user.id] = 'maze level'
            return maze(update, context)
        elif 'не' in text \
                or 'no' in text:
            now[update.message.from_user.id] = 'menu'
            return menu(update, context)
    elif now[update.message.from_user.id] == 'rating':
        if 'maze' in text:
            now[update.message.from_user.id] = 'rating maze'
            return rating(update, context)
        elif 'xo' in text:
            now[update.message.from_user.id] = 'rating xo'
            return rating(update, context)
        elif 'all' in text:
            now[update.message.from_user.id] = 'rating all'
            return rating(update, context)
        elif 'cities' in text:
            now[update.message.from_user.id] = 'rating cities'
            return rating(update, context)
    # обработка в игре города, проверка ответа
    elif now[update.message.from_user.id] in ['cities 1', 'cities 2']:
        return cities(update, context)
    # если пользователь написал что-то не предусмотренное
    elif "maze" in now[update.message.from_user.id]:
        return maze(update, context)
    update.message.reply_text('Извините, я вас не понимаю.')
    echo(update, context)


# запуск бота
def main():
    updater = Updater('5116714628:AAEoIs6Lfm6MwqxSNdB4usb6fMYL_GcOYAQ', use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, text)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("end_play", end_play))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("rating", rating))
    dp.add_handler(CommandHandler("xo", xo))
    dp.add_handler(CommandHandler("cities", cities))
    dp.add_handler(CommandHandler("maze", maze))
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
