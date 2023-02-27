import telebot
from telebot import types # клавиатура
from keyboa import Keyboa

import config
import random

bot = telebot.TeleBot(config.TOKEN)

# первое сообзение от пользователя
# Если бот был перезагружен, игра должна начаться сначала
first_message = {}

# в игре
in_game = {}

# словарь названных городов
# user_id: ['список городов']
used_cities = {}

# словарь посльзователей и количества названных ими городов
user_named_cities = {}


# последний названный город
# user_id: 'город'
last_city = {}

# страны
# user_id: ['Домены стран']
user_chosen_countries = {}

def first_letter(a): #Функция поиска первой буквы.
    for m in a:
        return(m[0])

last_letters = ['ь', 'ы', 'ъ']
last_user_letters = {}

def last_letter(p): #Функция поиска последней буквы.
    word = []
    for m in p:
        word.append(m)
    if word[-1] == 'ь' or word[-1] == 'ы' or word[-1] == 'ъ':
        return(word[-2])
    else:
        return(word[-1])

@bot.message_handler(commands=['info'])
def get_info(message):
    bot.reply_to(message, 'Этот бот создан для игры в города.\nСтран в базе: {0}.\nПользователей в игре: {1}.'.format(len(config.all_domains.items()), len(in_game)))

@bot.message_handler(commands=['start'])
def welcome(message):
    global first_message

    if message.chat.id not in first_message:

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('Давай')
        markup.add(button1)

        bot.send_message(message.chat.id, 'Привет, {0}! Давай сыграем в города?'.format(message.chat.first_name), reply_markup=markup)

        first_message[message.chat.id] = True

    else:

        bot.reply_to(message, 'Бот уже запущен.')


@bot.message_handler(content_types=['text'])
def main(message):
    global first_message
    global in_game
    global user_chosen_countries

    def start_game():

        in_game[message.chat.id] = True
        used_cities[message.chat.id] = []
        user_named_cities[message.chat.id] = 0

        return
    
    def over_game():

        del in_game[message.chat.id]
        used_cities.pop(message.chat.id)
        last_city.pop(message.chat.id)
        del user_chosen_countries[message.chat.id]
        return
    
    def result(a=0):
        result = int(user_named_cities[message.chat.id])
        if int(result) == 0:
            res = (str(result) + ' городов. Комментировать не буду.')
        elif int(result) == 1:
            res = (str(result) + ' город. Комментировать не буду.')
        elif int(result) >= 1 and int(result) <= 2:
            res = (str(result) + ' города. Это очень плохой результат, тебе следует подтянуть географию.')
        elif int(result) >= 3 and int(result) < 7:
            res = (str(result) + ' городов. Это неплохо, но в компании друзей похвастаться будет нечем.')
        elif int(result) >= 8 and int(result) < 30:
            res = (str(result) + ' городов. Очень хороший результат, хочешь сыграть ещё?')
        elif int(result) >= 15 and int(result) < 29:
            res = (str(result) + ' городов! Можешь попробовать поиграть в города с учителем географии.')
        elif int(result) >= 30:
            res = (str(result) + ' городов! Я уже думал, что ты меня победишь! Я знаю всего лишь около ' + str(len(config.cities)) + ' городов')
        if a!=0:
            return str(result)
        else:
            return(res)

    if message.chat.id not in first_message:
        bot.send_message(message.chat.id, 'Нужно перезапустить бота командой\n/start'.format(message.chat.first_name))
    else:
        if message.chat.id in in_game:
            if in_game[message.chat.id] == False and message.text in ['Начать игру', 'Играть снова']:

                start_game()

                cities = []
                for country in user_chosen_countries[message.chat.id]:  
                    cities = cities + config.all_domains[country]

                city = random.choice(cities)
                used_cities[message.chat.id].append(city)

                ingame_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button1 = types.KeyboardButton('Закончить')
                ingame_keyboard.add(button1)

                bot.send_message(message.chat.id, city, parse_mode='html', reply_markup=ingame_keyboard)

                last_user_letters[message.chat.id] = last_letter(city)
                last_city[message.chat.id] = city

            elif in_game[message.chat.id] == False and message.text != 'Начать игру':
                bot.send_message(message.chat.id, 'Для начала игры нажми "Начать игру"'.format(message.chat.first_name))
            elif in_game[message.chat.id] == True and message.text == 'Начать игру' or message.text == 'Играть снова':
                bot.send_message(message.chat.id, 'Мы уже играем'.format(message.chat.first_name))
            else:
                if message.text == 'Закончить' and in_game[message.chat.id]==True:

                    bot.send_message(message.chat.id, 'Игра закончена', parse_mode='html')

                    replay_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button1 = types.KeyboardButton('Играть снова')
                    replay_keyboard.add(button1)

                    bot.send_message(message.chat.id, 'Тобой названо ' + result(), reply_markup=replay_keyboard)

                    over_game()
                else:

                    cities = []
                    for country in user_chosen_countries[message.chat.id]:  
                        cities = cities + config.all_domains[country]

                    if message.text in used_cities[message.chat.id]:
                        bot.send_message(message.chat.id, 'Этот город уже назван')
                    else:
                        if message.text in cities:
                            if first_letter(message.text).upper()==last_letter(last_city[message.chat.id]).upper():

                                user_named_cities[message.chat.id] += 1;
                                used_cities[message.chat.id].append(message.text)
                                last_city[message.chat.id] = message.text

                                for city in used_cities[message.chat.id]:
                                    cities.remove(city)

                                available_cities = []
                                for city in cities:
                                    if last_letter(last_city[message.chat.id]).upper() == first_letter(city).upper():
                                        available_cities.append(city)
                                if len(available_cities)!=0:

                                    city = random.choice(available_cities)

                                    last_city[message.chat.id] = city
                                    used_cities[message.chat.id].append(city)

                                    bot.send_message(message.chat.id, city, parse_mode='html')

                                else:
                                    bot.send_message(message.chat.id, 'Мне нечего ответить. Твоя победа.', parse_mode='html')
                                    replay_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                                    button1 = types.KeyboardButton('Играть снова')
                                    replay_keyboard.add(button1)
                                    bot.send_message(message.chat.id, 'Тебе удалось победить меня, количество названных городов: ' + result(1), reply_markup=replay_keyboard)
                                    over_game()
                            else:
                                bot.send_message(message.chat.id, 'Не совпадает - {0} и {1}'.format(message.text[0].upper(),last_city[message.chat.id][-1].upper()), parse_mode='html')
                        else:
                            bot.send_message(message.chat.id, 'Такого города нет в выбранных тобой странах или вообще не существет')
        else:
            if message.chat.id not in user_chosen_countries:
                user_chosen_countries[message.chat.id] = []
                countries_markup = Keyboa(items=config.countries, items_in_row=2)
                bot.send_message(message.chat.id, 'Замечательно, теперь тебе нужно выбрать страны, города в которых будут использоваться в игре.'.format(message.chat.first_name), reply_markup=countries_markup())
            else: 
                if len(user_chosen_countries[message.chat.id]) != 0 and message.text=='Готово':

                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    button1 = types.KeyboardButton('Начать игру')
                    markup.add(button1)

                    bot.send_message(message.chat.id, 'Отлично, страны выбраны, теперь можно начинать!'.format(message.chat.first_name), reply_markup=markup) 
                    in_game[message.chat.id] = False   
                elif len(user_chosen_countries[message.chat.id]) == 0 and message.text=='Готово':
                    bot.send_message(message.chat.id, 'Нужно выбрать хотябы одну страну для игры'.format(message.chat.first_name)) 

@bot.callback_query_handler(func=lambda call: call.data in config.countries)
def callback_inline(call):
    global user_chosen_countries
    global in_game
    try:
        if call.message:

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Готово')
            markup.add(button1)

            country = call.data.split(' ')[0]
            if country not in user_chosen_countries[call.message.chat.id] and call.message.chat.id not in in_game:
                user_chosen_countries[call.message.chat.id] = user_chosen_countries[call.message.chat.id] + [call.data.split(' ')[0]]
                bot.send_message(call.message.chat.id, 'Города из {0} добавлены! (+{1})'.format(call.data.split(' ')[1], len(config.all_domains[call.data.split(' ')[0]])), reply_markup=markup)
                # print(user_chosen_countries[call.message.chat.id])
            
            elif country in user_chosen_countries[call.message.chat.id] and call.message.chat.id not in in_game:
                user_chosen_countries[call.message.chat.id].remove(country)
                bot.send_message(call.message.chat.id, 'Города из {0} убраны (-{1})'.format(call.data.split(' ')[1], len(config.all_domains[call.data.split(' ')[0]])), reply_markup=markup)
                # print(user_chosen_countries[call.message.chat.id])
            
    except Exception as e:
        print(repr(e))

bot.infinity_polling()