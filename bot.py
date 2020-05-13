# -*- coding: utf-8 -*-

import telebot
import emoji as e
import functions as f

TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)
users = {}


@bot.message_handler(commands=['start'])
def welcome(message):
    global users
    users[message.from_user.id] = {}
    users[message.from_user.id]['game'] = False

    bot.send_message(message.chat.id,
                     "Привет, {}! Я Длиннохвостик - веселый питон {}, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем прямиком из 2014 или оценить вашу фотографию. А также много чего еще, я надеюсь, что вам со мной будет интересно) {}".format(
                         message.from_user.first_name, e.snake, e.celebrate))


@bot.message_handler(content_types=['text'])
def dialog(message):
    global users
    chat = message.chat.id
    us = message.from_user.id
    m = str(message.text).lower()

    if ("шутк" in m) or ("шуте" in m) or ("прикол" in m) and ("прикольно" not in m):
        joke = f.jokes()
        bot.send_message(chat, joke)

    elif 'мем' in m or '2014' in m or 'смеш' in m:
        mem = f.send_mem()
        bot.send_photo(chat, mem)
    elif 'камень-ножницы-бумаг' in m:
        if users[us]['game']:
            bot.send_message(chat, "Мы уже играем! Скорее, выбирай!")
        users[us]['game'] = True
        bot.send_message(chat, 'Выбирай! Если больше не хочешь играть, скажи "нет" ' + e.smile)

    elif users[us]['game'] and f.from_e_to_game(m):
        res = f.game(f.from_e_to_game(m))
        bot.send_message(chat, res + '\n' + "Сыграем еще?)")

    elif users[us]['game'] and m == "да":
        users[us]['game'] = True

    elif users[us]['game'] and m == "нет":
        users[us]['game'] = False

    elif users[us]['game']:
        bot.send_message(chat, "Ты ввел что-то неправильно, повтори пожалуйста!")

    elif f.place(m):
        bot.send_message(us, f.place(m))

    else:

        bot.send_message(chat, "a)")


bot.polling(none_stop=True, interval=0)
