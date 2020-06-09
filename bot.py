# -*- coding: utf-8 -*-

import telebot
from telebot import types
import emoji as e
import functions as f
import data
from threading import Thread
import diary
import analysis as ans
import time
import check
from flask import Flask, request

secret = "d934d73e-19ae-4553-b0a0-be348ed41f11"
bot = telebot.TeleBot('1114362533:AAHzVc9RIitjqHztpdAGWWM-f-SQILqbY_c')

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://gigantina.pythonanywhere.com/{}".format(secret))

app = Flask(__name__)


@app.route('/{}'.format(secret), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


def menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Мем', 'Шутка']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Камень-ножницы-бумага']])
    return keyboard


def game_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Камень"))
    keyboard.add(types.KeyboardButton("Ножницы"))
    keyboard.add(types.KeyboardButton("Бумага"))
    keyboard.add(types.KeyboardButton("Хватит"))
    return keyboard


global keyboard, game_keyboard
keyboard = menu()
game_keyboard = game_menu()


def planning():  # для отправки сообщений в заданное время
    while True:
        chats = data.get_chats()
        for user in chats:
            time = f.get_time(data.get_utc(user[0]))
            if time == '00-00-00':
                data.new_day(user[0])
            if time == '20-00-00':
                bot.send_message(user[0],
                                 'Привет! Я просто хочу напомнить. Пожалуйста, заполни дневник эмоций на сегодня)',
                                 reply_markup=keyboard)
            if time == '15-00-00' and (check.get_tuesday(user[0]) or check.get_friday(user[0])):
                if diary.analize(user[0]) != None:
                    bot.send_message(user[0], 'Привет! Я недавно проанализировал твой дневник и вот твои результаты:',
                                     reply_markup=keyboard)
                    res = ans.analysis_sentiment(ans.analysis_data(diary.analize(user[0])))
                    if not res:
                        bot.send_message(user[0],
                                         'Знаешь, в последнее время я вижу в тебе много негативных эмоций. Пожалуйста, если ты часто чувствуешь себя плохо, обратись к специалисту. Можешь воспользоваться этим анонимным телефоном доверия: \n 8-800-2000-122, звонок анонимный и бесплатный. Помни, это не стыдно!',
                                         reply_markup=keyboard)
                    if res == 1:
                        bot.send_message(user[0], 'Судя по твоему дневнику, с тобой все в порядке, ура!',
                                         reply_markup=keyboard)
                    else:
                        bot.send_message(user[0],
                                         'Ох, как бы странно это не звучало, но меня настораживает обильное количество позитива в твоем дневнике. Знаешь, не всегда много хороших эмоций - хорошо. Если тебя беспокоит твое состояние, обратись к специалисту',
                                         reply_markup=keyboard)
                check.tuesday_set(user[0], 0)
                check.friday_set(user[0], 0)


t = Thread(target=planning)  # создает поток, который постоянно отслеживает время

t.start()


@bot.message_handler(commands=['start'])
def welcome(message):  # приветствие, а также создание в базе нового пользователя
    print(message.from_user.id)
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    bot.send_message(message.chat.id,
                     'Привет, {}! Я Длиннохвостик - веселый питон {}, а что самое интересное, я написан на Python, как иронично) \n Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем прямиком из 2014 или оценить вашу фотографию. Но моя главная функция - ведение дневника эмоций, а также их анализ. Советую сразу написать команду "/help", чтобы больше узнать, что и как писать. Надеюсь, что вам со мной будет интересно) {}'.format(
                         message.from_user.first_name, e.snake, e.celebrate), reply_markup=keyboard)
    bot.send_message(message.from_user.id,
                     'Точно, я чуть не забыл! Пожалуйста, напиши команду "/utc [свой часовой пояс в формате UTC]", чтобы я мог нормально тебе присылать сообщения. Например, "/utc +3" для Москвы. Еще увидимся! Если возникнут вопросы, просто пиши "/help"',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def commands(message):
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    bot.send_message(message.from_user.id,
                     'Итак, все возможности бота \n Основные функции: \n 1. /note [эмоция]. Делает новую запись в дневнике эмоций. Вам необходимо выбрать одну из этих эмоций: грусть, гнев, страх, радость, вина \n 2. /utc [время]. Настройка времени в формате UTC. Например, для Москвы необходимо будет написать "/utc +3". По умолчанию стоит время по Москве \n 3. /diary_week. Вам присылаются записи дневника за последние 7 дней, а так же возможные советы исходя из его анализа \n 4. /diary_all. Вам присылаются записи дневника за все время \n Фишки: \n 5. /diary_last. Вам присылаются записи дневника за последний день \n Фишки: \n 1. Просто напишите любой топоним - я найду, что ответить! \n 2. Напишите слово или фразу, включающее слово "мем", я пришлю что-ниюудь смешное из 2014 \n 3. Напишите слово или фразу, включающее слово "шутка" \n 4. Мы можем сыграть в камень-ножницы-бумагу, просто напиши название игры и игрв начнется! \n 5. Ты можешь просто делиться мыслями со мной, я попробую понять тебя \n 6. Два раза в неделю я анализирую твой дневник и, возможно, укажу на неприятности',
                     reply_markup=keyboard)


@bot.message_handler(commands=['note'])
def diary_note(message):  # записывает в базу новую запись в дневник
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    m = str(message.text)[6:].lower()
    us = message.from_user.id
    if m in ['вина', 'радость', 'грусть', 'гнев', 'страх']:
        diary.new_emotion(us, m)
        data.situation(us, 1)
        bot.send_message(us, 'Отлично! Ты молодец, а теперь опиши ситуацию, когда ты это испытал',
                         reply_markup=keyboard)


@bot.message_handler(commands=['del_table_15754'])
def delete(message):
    data.del_table()
    bot.send_message(message.from_user.id, 'Очищено')


@bot.message_handler(commands=['del_table_15755'])
def delete(message):
    diary.del_table()
    bot.send_message(message.from_user.id, 'Очищено')


@bot.message_handler(commands=['utc'])  # настраивает часовой пояс
def change_utc(message):
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    m = message.text
    try:
        op = m[5]
        time = int(m[5:])
        if (time > -13) and (time < 15) and (op == '+' or op == '-'):
            print(time, op)
            data.utc(time, message.from_user.id)
            bot.send_message(message.from_user.id, "Часовой пояс установлен", reply_markup=keyboard)
        else:
            print(time, op)
            bot.send_message(message.from_user.id, "Введен неправильный формат времени!", reply_markup=keyboard)
    except:
        bot.send_message(message.from_user.id, "Введен неправильный формат времени!", reply_markup=keyboard)


@bot.message_handler(commands=['diary_week'])
def diary_week(message):  # присылает дневник за неделю
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    start, end = diary.get_week_diary(message.from_user.id)
    week = diary.get_notes(start, end, message.from_user.id)
    if week:
        res = ''
        for day in week:
            day_of_week = day[0]
            bot.send_message(message.from_user.id, "Итак, твои записи за неделю:", reply_markup=keyboard)
            bot.send_message(message.from_user.id, day_of_week.capitalize() + ":", reply_markup=keyboard)
            for i in range(1, len(day)):
                string = ''
                emotion, sit = str(day[i][0][0]), str(day[i][0][1])
                string = f'Ты испытал {emotion} в данной ситуации: \n {sit} \n' + '\n'
                res += string
    else:
        res = 'О, ты еще не сделал записей на этой неделе! Ты ысегда можешь это сделать командой "/note"'

    bot.send_message(message.from_user.id, res, reply_markup=keyboard)


@bot.message_handler(commands=['diary_all'])
def diary_all(message):
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    start, end = diary.get_week_diary(message.from_user.id)
    week = diary.get_notes(start, end, message.from_user.id)
    if week:
        res = ''
        date = 1
        for day in week:
            day_of_week = day[0]
            bot.send_message(message.from_user.id, "Итак, твои записи за все время:", reply_markup=keyboard)
            bot.send_message(message.from_user.id, f"День {date}, {day_of_week} :", reply_markup=keyboard)
            date += 1
            for i in range(1, len(day)):
                string = ''
                emotion, sit = str(day[i][0][0]), str(day[i][0][1])
                string = f'Ты испытал {emotion} в данной ситуации: \n {sit} \n' + '\n'
                res += string
    else:
        res = 'О, ты еще не сделал записей! Ты всегда можешь это сделать командой "/note"'

    bot.send_message(message.from_user.id, res, reply_markup=keyboard)


@bot.message_handler(commands=['diary_last'])
def diary_all(message):
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    day = diary.get_diary_day(message.from_user.id)
    if day:
        res = ''
        bot.send_message(message.from_user.id, f"Итак, твои записи за день:", reply_markup=keyboard)
        for i in range(0, len(day)):
            string = ''
            emotion, sit = str(day[i][0]), str(day[i][1])
            string = f'Ты испытал {emotion} в данной ситуации: \n {sit} \n' + '\n'
            res += string
    else:
        res = 'О, ты еще не сделал записей за сегодня! Ты всегда можешь это сделать командой "/note"'

    bot.send_message(message.from_user.id, res, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def dialog(message):  # проверки сообщения
    data.new(message.from_user.id)
    check.new(message.from_user.id)
    us = message.from_user.id
    m = str(message.text).lower()
    if ("шутк" in m) or ("шуте" in m) or ("прикол" in m) and ("прикольно" not in m):
        joke = f.jokes()
        bot.send_message(us, joke, reply_markup=keyboard)

    elif 'мем' in m or '2014' in m or 'смеш' in m:
        mem = f.send_mem()
        bot.send_photo(us, mem, reply_markup=keyboard)
    elif 'камень-ножницы-бумаг' in m or 'играть' in m:
        data.game(us, 1)
        bot.send_message(us, 'Выбирай! Если больше не хочешь играть, скажи "хватит" ' + e.smile,
                         reply_markup=game_keyboard)

    elif data.get_game(us) and f.from_e_to_game(m):
        res = f.game(f.from_e_to_game(m))
        bot.send_message(us, res + '\n' + "Сыграем еще?)", reply_markup=game_keyboard)

    elif data.get_game(us) and m == "да":
        data.game(us, 1)

    elif data.get_game(us) and m == "хватит":
        bot.send_message(us, 'Хорошо, больше не будем играть', reply_markup=keyboard)
        data.game(us, 0)

    elif data.get_game(us):
        bot.send_message(us, "Ты ввел что-то неправильно, повтори пожалуйста. Если надоело, просто напиши 'хватит'",
                         reply_markup=game_keyboard)

    elif data.get_situation(us):
        diary.situation(us, m)
        bot.send_message(us, 'Отлично, ты сделал запись в нашем дневнике! Ты можешь сделать еще одну, написав "/note"',
                         reply_markup=keyboard)

    elif f.place(m):
        bot.send_message(us, f.place(m), reply_markup=keyboard)

    elif not ans.analysis_sentiment(ans.analysis_data([m])):
        bot.send_message(us, 'Поменьше негатива, пожалуйста. Можешь записать это в дневник, кстати!',
                         reply_markup=keyboard)

    elif ans.analysis_sentiment(m):
        callback = f.normal()
        bot.send_message(us, callback, reply_markup=keyboard)

    else:
        bot.send_message(us, "хммммм", reply_markup=keyboard)


while True:
    try:
        bot.polling(True, timeout=200)

    except Exception as e:
        print(e)
        time.sleep(15)
