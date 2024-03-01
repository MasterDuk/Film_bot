import random
import telebot
#from config import token
from bs4 import BeautifulSoup as bs
import requests

mybot = telebot.TeleBot('Your token')
name = ''
spisok_films = []
spisok_comedy = []
spisok_mult = []
spisok_fant = []
spisok_horr = []

def spisok():
    global spisok_films
    if len(spisok_films) == 0:
        responce_get = requests.get('https://www.film.ru/a-z/movies')
        soup = bs(responce_get.text, features='html.parser')
        quot_f = soup.find_all('a', class_='redesign_afisha_movie_main_title')
        for film in quot_f:
            spisok_films.append(film.text)
        return random.choice(spisok_films)
    else:
        return random.choice(spisok_films)

def spisok_c():
    global spisok_comedy
    if len(spisok_comedy) == 0:
        responce_get_c = requests.get('https://www.film.ru/a-z/movies/comedy')
        soup_c = bs(responce_get_c.text, features='html.parser')
        quot_c = soup_c.find_all('a', class_='redesign_afisha_movie_main_title')
        for film in quot_c:
            spisok_comedy.append(film.text)
        return random.choice(spisok_comedy)
    else:
        return random.choice(spisok_comedy)

def spisok_m():
    global spisok_mult
    if len(spisok_mult) == 0:
        responce_get_m = requests.get('https://www.film.ru/a-z/movies/animation')
        soup_m = bs(responce_get_m.text, features='html.parser')
        quot_m = soup_m.find_all('a', class_='redesign_afisha_movie_main_title')
        for film in quot_m:
            spisok_mult.append(film.text)
        return random.choice(spisok_mult)
    else:
        return random.choice(spisok_mult)

def spisok_f():
    global spisok_fant
    if len(spisok_fant) == 0:
        responce_get_f = requests.get('https://www.film.ru/a-z/movies/science_fiction')
        soup_f = bs(responce_get_f.text, features='html.parser')
        quot_fa = soup_f.find_all('a', class_='redesign_afisha_movie_main_title')
        for film in quot_fa:
            spisok_fant.append(film.text)
        return random.choice(spisok_fant)
    else:
        return random.choice(spisok_fant)

def spisok_h():
    global spisok_horr
    if len(spisok_horr) == 0:
        responce_get_h = requests.get('https://www.film.ru/a-z/movies')
        soup_h = bs(responce_get_h.text, features='html.parser')
        quot_h = soup_h.find_all('a', class_='redesign_afisha_movie_main_title')
        for film in quot_h:
            spisok_horr.append(film.text)
        return random.choice(spisok_horr)
    else:
        return random.choice(spisok_horr)

@mybot.message_handler(commands=['start'])
def start_com(message):
    str = 'Приветствуем в нашем боте.\nКак тебя зовут?'
    mybot.send_message(message.chat.id, str)
    mybot.register_next_step_handler(message, p_name)

@mybot.message_handler(commands=['help'])
def help_com(message):
    help_text ='''
    "Для того чтобы начать введите команду /run" \
    "Для получения помощи введите команду /help" \
    "Для того чтобы заново запустить бота введите команду /start" \
    "При работе с ботом используйте клавитуру, которая появится после отправки команды run" \
    '''
    mybot.send_message(message.chat.id, help_text)

def key_run():
    k_markup = telebot.types.ReplyKeyboardMarkup()
    btn_genre = telebot.types.KeyboardButton('Жанры фильмов')
    btn_rand_popul = telebot.types.KeyboardButton('Случайный фильм из популярного')
    k_markup.row(btn_genre)
    k_markup.row(btn_rand_popul)
    return k_markup

def key_genre(message):
    key_genre = telebot.types.InlineKeyboardMarkup()
    key_comedy = telebot.types.InlineKeyboardButton(text='Комедии', callback_data='comedy')
    key_mult = telebot.types.InlineKeyboardButton(text='Мультфильмы', callback_data='mult')
    key_fantastic = telebot.types.InlineKeyboardButton(text='Фантастика', callback_data='fantastic')
    key_horror = telebot.types.InlineKeyboardButton(text='Ужасы', callback_data='horror')
    key_genre.add(key_comedy, key_mult, key_fantastic, key_horror)
    return key_genre

@mybot.message_handler(commands=['run'])
def run_com(message):
    mybot.send_message(message.chat.id, 'Начинаем', reply_markup=key_run())

def p_name(message):
    global name
    name = message.text
    mybot.send_message(message.chat.id, f'Рад приветствовать тебя {name}\nЧтобы начать отправь /run\n'
                                             f'Если тебе нужна помощь, то отправь /help')

@mybot.message_handler(content_types=['text'])
def genre_r(message):
    if message.text == 'Жанры фильмов':
       mybot.send_message(message.chat.id, 'Выберите один из жанров: ', reply_markup=key_genre(message))
    if message.text == 'Случайный фильм из популярного':
       mybot.send_message(message.chat.id, spisok())

@mybot.callback_query_handler(func=lambda call: True)
def callback_genre(call):
    if call.data == 'comedy':
       mybot.send_message(call.message.chat.id, spisok_c())
    if call.data == 'mult':
       mybot.send_message(call.message.chat.id, spisok_m())
    if call.data == 'fantastic':
       mybot.send_message(call.message.chat.id, spisok_f())
    if call.data == 'horror':
       mybot.send_message(call.message.chat.id, spisok_h())

mybot.polling()
