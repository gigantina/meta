# -*- coding: utf-8 -*-

import telebot
import emoji as e
import functions as f
import data
from threading import Thread
import diary

TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)

def planning():  # для отправки сообщений в заданное время
    while True:
        chats = data.get_chats()
        for user in chats:
            time = f.get_time(data.get_utc(user[0]))
            if time == '00-00-00':
                diary.new_day()
            if time == '20-00-00':
                bot.send_message(user[0],
                                 'Привет! Я просто хочу напомнить. Пожалуйста, заполни дневник эмоций на сегодня)')


t = Thread(target=planning)  # создает поток, который постоянно отслеживает время

t.start()


@bot.message_handler(commands=['start'])
def welcome(message):  # приветствие, а также создание в базе нового пользователя
    data.new(message.from_user.id)
    bot.send_message(message.chat.id,
                     'Привет, {}! Я Длиннохвостик - веселый питон {}, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем прямиком из 2014 или оценить вашу фотографию. Но моя главная функция - ведение дневника эмоций, а также их анализ. Советую сразу написать команду "/help", чтобы больше узнать, что и как писать. Надеюсь, что вам со мной будет интересно) {}'.format(
                         message.from_user.first_name, e.snake, e.celebrate))
    bot.send_message(message.from_user.id,
                     'Точно, я чуть не забыл! Пожалуйста, напиши команду "/utc [свой часовой пояс в формате UTC]", чтобы я мог нормально тебе присылать сообщения. Например, "/utc +3" для Москвы. Еще увидимся! Если возникнут вопросы, просто пиши "/help"')


@bot.message_handler(commands=['help'])
def commands(message):
    bot.send_message(message.from_user.id,
                     'Итак, все возможности бота \n Основные функции: \n 1. /note [эмоция]. Делает новую запись в дневнике эмоций. Вам необходимо выбрать одну из этих эмоций: грусть, гнев, страх, радость, вина \n 2. /utc [время]. Настройка времени в формате UTC. Например, для Москвы необходимо будет написать "/utc +3". По умолчанию стоит время по Лондону \n 3. /diary_week. Вам присылаются записи дневника за последние 7 дней, а так же возможные советы исходя из его анализа \n 4. /diary_all. Вам присылаются записи дневника за все время \n Фишки: \n 1. Просто напишите любой топоним - я найду, что ответить! \n 2. Напишите слово или фразу, включающее слово "мем", я пришлю что-ниюудь смешное из 2014 \n 3. Напишите слово или фразу, включающее слово "шутка" \n 4. Мы можем сыграть в камень-ножницы-бумагу, просто напиши название игры и игрв начнется! \n 5. Ты можешь просто делиться мыслями со мной, я попробую понять тебя (в разработке)')


@bot.message_handler(commands=['note'])
def diary_note(message):  # записывает в базу новую запись в дневник
    m = message.text[6:]
    us = message.from_user.id
    if m in ['вина', 'радость', 'грусть', 'гнев', 'страх']:
        diary.new_emotion(us, m)
        data.situation(us, 1)
        bot.send_message(us, 'Отлично! Ты молодец, а теперь опиши ситуацию, когда ты это испытал')


@bot.message_handler(commands=['del_table_15754'])
def delete(message):
    data.del_table()


@bot.message_handler(commands=['del_table_15755'])
def delete(message):
    diary.del_table()


@bot.message_handler(commands=['utc'])  # настраивает часовой пояс
def change_utc(message):
    m = message.text
    try:
        op = m[5]
        time = int(m[5:])
        if (time > -13) and (time < 15) and (op == '+' or op == '-'):
            print(time, op)
            data.utc(time, message.from_user.id)
        else:
            print(time, op)
            bot.send_message(message.from_user.id, "Введен неправильный формат времени!")
    except:
        bot.send_message(message.from_user.id, "Введен неправильный формат времени!")


@bot.message_handler(commands=['diary_week'])
def diary_week(message):  # присылает дневник за неделю
    week = diary.get_week_diary(message.from_user.id)
    if week:
        res = ''
        for day in week:
            day_of_week = day[0]
            # bot.send_message(message.from_user.id, f"Итак, в {day_of_week} твои записи:")
            bot.send_message(message.from_user.id, f"Итак, твои записи за неделю:")
            for i in range(1, len(day)):
                string = ''
                emotion, sit = str(day[i][0][0]), str(day[i][0][1])
                print(sit, emotion)
                # advice = diary.get_advice(message.from_user.id). Пока нет функции, но она будет анализировать базу с эмоциями
                string = f'Ты испытал {emotion} в данной ситуации: \n {sit} \n' + '\n'
                res += string
    else:
        res = 'О, ты еще не сделал записей на этой неделе! Тф ысегда можешь это сделать командой "/note"'

    bot.send_message(message.from_user.id, res)


@bot.message_handler(commands=['diary_all'])
def diary(message):
    bot.send_message(message.from_user.id, 'В разработке')


@bot.message_handler(content_types=['text'])
def dialog(message):  # проверки сообщения
    us = message.from_user.id
    m = str(message.text).lower()
    if ("шутк" in m) or ("шуте" in m) or ("прикол" in m) and ("прикольно" not in m):
        joke = f.jokes()
        bot.send_message(us, joke)

    elif 'мем' in m or '2014' in m or 'смеш' in m:
        mem = f.send_mem()
        bot.send_photo(us, mem)
    elif 'камень-ножницы-бумаг' in m or 'играть' in m:
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

    elif data.get_situation(us):
        diary.situation(us, m)
        bot.send_message(us, 'Отлично, ты сделал запись в нашем дневнике! Ты можешь сделать еще одну, написав "/note"')

    elif f.place(m):
        bot.send_message(us, f.place(m))

    else:
        bot.send_message(us, "a)")


bot.polling(none_stop=True, interval=0)
