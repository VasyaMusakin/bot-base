from data import db_session
from data.cities import city
from main import *
from data.results import Results
from data.users import User
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater, MessageHandler, Filters

db_session.global_init("db/bot.db")
db_sess = db_session.create_session()
now = ''
now_for_game = ''


def echo(update, context):
    global maze_mode, now
    if now == 'start':
        return start(update, context)
    elif now == 'e_p':
        return end_play(update, context)
    elif now == '':
        return stop(update, context)
    elif now == 'menu':
        return menu(update, context)
    elif 'cities' in now:
        return cities(update, context)
    elif maze_mode == "changing_level" and 'maze' in now:
        if context.isdigit():
            number_level = int(context)
            if number_level > level_num:
                update.message.reply_text('Собака пиши команды')
            else:
                change_level(number_level)
                update.message.reply_text('уровень изменён')
                maze_mode = "active"
                ray_casting(player_pos, ANGELES[player_angle])
                update.message.reply_text(f"pos:{str(player_pos)} angle:{player_angle * 90}")
                context.bot.send_photo(update.message.chat_id, photo=open('6.png', 'rb'),
                                       reply_markup=markup_walking)
    elif 'rating' in now:
        return rating(update, context)
    else:
        update.message.reply_text('Собака пиши команды')


def start(update, context):
    global now, db_sess
    a = [i.id_tg for i in db_sess.query(User).all()]
    if update.message.from_user.id not in a:
        user = User()
        user.id_tg = update.message.from_user.id
        user.username = update.message.from_user.username
        db_sess.add(user)
        db_sess.commit()
        result = Results(user=user)
        db_sess.add(result)
        db_sess.commit()
    if now == '':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Я бот с играми. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
        now = 'start'
    elif now == 'start':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Бот уже активирован 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
    else:
        update.message.reply_text(f'''Бот уже активирован.''')
        echo(update, context)


def stop(update, context):
    global now, now_for_game, maze_mode
    if now != '':
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Бот выключен. Спасибо за игру. 
    Чтобы заново активировать бота нажмите - /start''',
            reply_markup=markup)
        now = ''
        now_for_game = ''
        maze_mode = "not_active"

    else:
        reply_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Бот выключен. 
    Чтобы активировать бота нажмите - /start''',
            reply_markup=markup)


def end_play(update, context):
    global now, now_for_game, maze_mode
    if 'xo' in now or 'maze' in now or 'cities' in now:
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Игра досрочно завершена. Результаты не занесены в рейтинг. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
        now = 'e_p'
        now_for_game = ''
        maze_mode = "not_active"
    elif now == 'e_p':
        reply_keyboard = [['/menu'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Игра уже завершена. 
    Если хотите посмотреть меню нажмите - /menu 
    Если хотите остановить бота нажмите - /stop''',
                                  reply_markup=markup)
    else:
        update.message.reply_text(f'''Вы ещё не начали играть.''')
        echo(update, context)


def menu(update, context):
    global now, maze_mode
    if now in ['menu', 'start', 'e_p', 'rating'] or 'rating' in now:
        reply_keyboard = [['/cities', '/maze', '/xo'], ['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Выберите игру: 
    города - /cities 
    крестики-нолики - /xo 
    лабиринт - /maze 

    Посмотреть рейтинг - /rating 
    Выключить бота - /stop ''',
                                  reply_markup=markup)
        now = 'menu'
        maze_mode = "not_active"
    else:
        update.message.reply_text(f'''В данный момент нельзя открыть меню.''')
        echo(update, context)


def xo(update, context):
    global now
    pass


def cities(update, context):
    global now, now_for_game, maze_mode
    if now in ['menu', 'start', 'e_p', 'rating'] or 'rating' in now or maze_mode != "not_active":
        reply_keyboard = [['да'], ['нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''В этой игре вам нужно угадать город по фотографии со спутника. 
Чтобы ответ засчитался, нужно вбивать название русскими буквами.
Если захотите досрочно окончить игру нажмите - /end_play
    Вы хотите начать игру?''', reply_markup=markup)
        now = 'cities'
        maze_mode = "not_active"
    elif now == 'cities 1':
        spisok = city()
        context.bot.send_photo(chat_id=update.message.chat_id, photo=spisok[0])
        reply_keyboard = [['/end_play']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(f'''Какой это город?''', reply_markup=markup)
        now_for_game = spisok[1]
        now = 'cities 2'
        maze_mode = "not_active"
    elif now == 'cities 2':
        if update.message.text == now_for_game:
            reply_keyboard = [['/end_play']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'''Верно. Идём дальше.''', reply_markup=markup)
            user = db_sess.query(User).filter(User.id_tg == update.message.from_user.id).first()
            db_sess.query(Results).filter(Results.user_id == user.id).update(
                {'cities': Results.cities + 1, 'all': Results.all + 1})
            db_sess.commit()
            now = 'cities 1'
            maze_mode = "not_active"
            return cities(update, context)
        else:
            reply_keyboard = [['/end_play']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
            update.message.reply_text(f'''Неверно. Идём дальше.''', reply_markup=markup)
            now = 'cities 1'
            maze_mode = "not_active"
            return cities(update, context)
    else:
        update.message.reply_text(f'''В данный момент нельзя открыть меню.''')
        return echo(update, context)


def rating(update, context):
    global now, now_for_game
    if now in ['start', 'menu', 'e_p', 'rating']:
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
        now = 'rating'
    elif now == 'rating all':
        stroka = 'Общий рейтинг:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: x.all))[:5]:
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
        now = 'rating'
    elif now == 'rating xo':
        stroka = 'Рейтинг по игре крестики-нолики:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: x.xo))[:5]:
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
        now = 'rating'
    elif now == 'rating maze':
        stroka = 'Рейтинг по игре крестики-нолики:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: x.maze))[:5]:
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
        now = 'rating'
    elif now == 'rating cities':
        stroka = 'Рейтинг по игре города:\n'
        for result in list(sorted(db_sess.query(Results).all(), key=lambda x: x.cities))[:5]:
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
        now = 'rating'
    else:
        reply_keyboard = []
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        update.message.reply_text(
            f'''Сейчас нельзя посмотреть рейтинг.''',
            reply_markup=markup)
        echo(update, context)


def text(update, context):
    global now
    if now == 'cities':
        if 'yes' in update.message.text \
                or 'ok' in update.message.text \
                or 'yes' in update.message.text \
                or 'да' in update.message.text \
                or 'хорошо' in update.message.text:
            now = 'cities 1'
            return cities(update, context)
        elif 'не' in update.message.text \
                or 'no' in update.message.text:
            now = 'menu'
            return menu(update, context)
    if now == 'rating':
        if 'maze' in update.message.text:
            now = 'rating maze'
            return rating(update, context)
        elif 'xo' in update.message.text:
            now = 'rating xo'
            return rating(update, context)
        elif 'all' in update.message.text:
            now = 'rating all'
            return rating(update, context)
        elif 'cities' in update.message.text:
            now = 'rating cities'
            return rating(update, context)
    if now in ['cities 1', 'cities 2']:
        return cities(update, context)
    update.message.reply_text('Извините, я вас не понимаю.')
    echo(update, context)


def main():
    updater = Updater('5104954005:AAFW-n0oIGM7ZqHprL8B-O4szvpjMVhx6yo', use_context=True)
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
    dp.add_handler(CommandHandler("w", forward))
    dp.add_handler(CommandHandler("s", back))
    dp.add_handler(CommandHandler("d", right))
    dp.add_handler(CommandHandler("a", left))
    dp.add_handler(CommandHandler("r", angle_right))
    dp.add_handler(CommandHandler("l", angle_left))
    dp.add_handler(CommandHandler("change_level", new_level))
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
