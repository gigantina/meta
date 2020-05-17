# -*- coding: utf-8 -*-

import telebot
import emoji as e
import functions as f
import data
from datetime import datetime
from threading import Thread

global feel
TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)
data.create()


def planning():
    random = False
    while True:
        now = datetime.now()
        if str(now.strftime("%H-%M-%S")) == '20-34-00':
            for chat in data.get_chats():
                bot.send_message(chat[0],
                                 "Добрый вечер, как у тебя настроение? Я настоятельно рекомендую заполнить таблицу эмоций сегодня. Выбери, что ты сегодня испытывал?")
                data.feel(chat, 1)
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


@bot.message_handler(commands=['note'])
def diary_note(message):
    data.feel(message.from_user.id, 1)


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
        bot.send_message(chat, 'Выбирай! Если больше не хочешь играть, скажи "хватит" ' + e.smile)

    elif data.get_game(us) and f.from_e_to_game(m):
        res = f.game(f.from_e_to_game(m))
        bot.send_message(chat, res + '\n' + "Сыграем еще?)")

    elif data.get_game(us) and m == "да":
        data.game(us, 1)

    elif data.get_game(us) and m == "хватит":
        data.game(us, 0)

    elif data.get_game(us):
        bot.send_message(chat, "Ты ввел что-то неправильно, повтори пожалуйста. Если надоело, просто напиши 'хватит)'")

    elif data.get_feel(us) and m in ['вина', 'радость', 'грусть', 'гнев', 'страх']:
        bot.send_message(chat, 'Отлично! Ты молодец, а теперь опиши ситуацию, когда ты это испытал')
        data.feel(us, 0)
        data.situation(us, 1)

    elif data.get_situation(us) and len(m) > 6:
        data.situation(us, 0)
        # сюда еще вставим функцию, делает запись о том, что чел испытал и когда (создадим еще одну базу данных)
        bot.send_message(chat, 'Отлично, ты сделал запись в нашем дневнике! Ты можешь сделать еще одну, написав "/note"')

    elif f.place(m):
        bot.send_message(us, f.place(m))

    else:
        bot.send_message(chat, "a)")


bot.polling(none_stop=True, interval=0)
