# -*- coding: utf-8 -*-

import telebot
import emoji as e
import functions as f
import data
from datetime import datetime
from threading import Thread

TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)


def planning():
    random = False
    while True:
        now = datetime.now()
        if str(now.strftime("%H-%M-%S")) == '20-34-00':
            for chat in data.get_chats():
                bot.send_message(chat[0], "Добрый вечер) Как дела?")
            random = f.time()
        elif str(now.strftime("%H-%M-%S")) == random:
            for chat in data.get_chats():
                bot.send_message(chat[0], "Привет, прости, если отвлекаю, мне просто интересно, как ты поживаешь))")


t = Thread(target=planning)
t.start()


@bot.message_handler(commands=['start'])
def welcome(message):
    data.new(message.from_user.id, message.chat.id)
    data.game(message.from_user.id, 0)
    bot.send_message(message.chat.id,
                     "Привет, {}! Я Длиннохвостик - веселый питон {}, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем прямиком из 2014 или оценить вашу фотографию. А также много чего еще, я надеюсь, что вам со мной будет интересно) {}".format(
                         message.from_user.first_name, e.snake, e.celebrate))


@bot.message_handler(content_types=['text'])
def dialog(message):
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
        data.game(us, 1)
        bot.send_message(chat, 'Выбирай! Если больше не хочешь играть, скажи "нет" ' + e.smile)

    elif data.get_game(us) and f.from_e_to_game(m):
        res = f.game(f.from_e_to_game(m))
        bot.send_message(chat, res + '\n' + "Сыграем еще?)")

    elif data.get_game(us) and m == "да":
        data.game(us, 1)

    elif data.get_game(us) and m == "нет":
        data.game(us, 0)

    elif data.get_game(us):
        bot.send_message(chat, "Ты ввел что-то неправильно, повтори пожалуйста!")

    elif f.place(m):
        bot.send_message(us, f.place(m))

    else:
        bot.send_message(chat, "a)")


bot.polling(none_stop=True, interval=0)
