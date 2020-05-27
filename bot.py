# -*- coding: utf-8 -*-

import telebot
import emoji as e
import functions as f
import data
from datetime import datetime
from threading import Thread
import diary

global feel
TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)
data.create()
diary.create()


def planning():
    random = False
    while True:
        now = datetime.now()
        if str(now.strftime("%H-%M-%S")) == '00-00-00':
            for us in data.get_chats():
                diary.new_day()
                if diary.get_days() % 7 == 0:
                    diary.new_week()
        if str(now.strftime("%H-%M-%S")) == '20-34-00':
            for us in data.get_chats():
                bot.send_message(chat[0],
                                 "Добрый вечер, как у тебя настроение? Я настоятельно рекомендую заполнить таблицу эмоций сегодня. Выбери, что ты сегодня испытывал?")
                data.feel(us, 1)
            random = f.time()
        elif str(now.strftime("%H-%M-%S")) == random:
            for chat in data.get_chats():
                bot.send_message(chat[0], "Привет, прости, если отвлекаю, мне просто интересно, как ты поживаешь))")


t = Thread(target=planning)
t.start()


@bot.message_handler(commands=['start'])
def welcome(message):
    data.new(message.from_user.id)
    bot.send_message(message.chat.id,
                     "Привет, {}! Я Длиннохвостик - веселый питон {}, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем прямиком из 2014 или оценить вашу фотографию. А также много чего еще, я надеюсь, что вам со мной будет интересно) {}".format(
                         message.from_user.first_name, e.snake, e.celebrate))
    bot.send_message(message.chat.id, str(datetime.now(tz=None)))
    print(message.from_user.id)


@bot.message_handler(commands=['note'])
def diary_note(message):
    data.feel(message.from_user.id, 1)


@bot.message_handler(commands=['diary_week'])
def diary_week(message):
    week = diary.get_week_diary(message.from_user.id)
    if week:
        res = ''
        for day in week:
            day_of_week = day[0]
            bot.send_message(message.from_user.id, f"Итак, в {day_of_week} твои записи:")
            print(day[1])
            for i in range(0, len(day[1])):
                emotion, sit = str(day[1][i - 1][0]), str(day[1][i - 1][1])
                print(sit, emotion)
                # advice = diary.get_advice(message.from_user.id)
                string = f'Ты испытал {emotion} в данной ситуации: \n {sit} \n' + '\n'
                res += string
    else:
        res = 'О, ты еще не сделал записей на этой неделе! Тф ысегда можешь это сделать командой "/note"'

    bot.send_message(message.from_user.id, res)


@bot.message_handler(content_types=['text'])
def dialog(message):
    us = message.from_user.id
    m = str(message.text).lower()
    if ("шутк" in m) or ("шуте" in m) or ("прикол" in m) and ("прикольно" not in m):
        joke = f.jokes()
        bot.send_message(us, joke)

    elif 'мем' in m or '2014' in m or 'смеш' in m:
        mem = f.send_mem()
        bot.send_photo(us, mem)
    elif 'камень-ножницы-бумаг' in m:
        data.game(us, 1)
        bot.send_message(us, 'Выбирай! Если больше не хочешь играть, скажи "хватит" ' + e.smile)

    elif data.get_game(us) and f.from_e_to_game(m):
        res = f.game(f.from_e_to_game(m))
        bot.send_message(us, res + '\n' + "Сыграем еще?)")

    elif data.get_game(us) and m == "да":
        data.game(us, 1)

    elif data.get_game(us) and m == "хватит":
        bot.send_message(us, 'Хорошо, больше не будем играть')
        data.game(us, 0)

    elif data.get_game(us):
        bot.send_message(us, "Ты ввел что-то неправильно, повтори пожалуйста. Если надоело, просто напиши 'хватит)'")

    elif data.get_feel(us) and m in ['вина', 'радость', 'грусть', 'гнев', 'страх']:
        bot.send_message(us, 'Отлично! Ты молодец, а теперь опиши ситуацию, когда ты это испытал')
        diary.new_emotion(us, m)
        data.feel(us, 0)
        data.situation(us, 1)

    elif data.get_situation(us) and len(m) > 6:
        data.situation(us, 0)
        diary.situation(us, m)
        bot.send_message(us, 'Отлично, ты сделал запись в нашем дневнике! Ты можешь сделать еще одну, написав "/note"')

    elif f.place(m):
        bot.send_message(us, f.place(m))

    else:
        bot.send_message(us, "a)")


bot.polling(none_stop=True, interval=0)
