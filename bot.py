# -*- coding: utf-8 -*-

import telebot

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
                     "Привет, {}! Я Длиннохвостик - веселый питон, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем или оценить вашу фотографию. А также много чегоеще, я надеюсь, что вам со мной будет интересно)".format(
                         message.from_user.first_name))

@bot.message_handler(content_types=['text'])
def dialog(message):
    global users
    if ("шутк" in str(message.text).lower() or "шуте" in str(
            message.text).lower() or "прикол" in str(message.text).lower()) and ("прикольно" not in str(message.text).lower()):
        joke = f.jokes()
        bot.send_message(message.chat.id, joke)
    elif 'камень-ножницы-бумаг' in str(message.text).lower():
        if users[message.from_user.id]['game']:
            bot.send_message(message.chat.id, "Мы уже играем! Скорее, выбирай!")
        users[message.from_user.id]['game'] = True
        bot.send_message(message.chat.id, "Выбирай!")

    elif users[message.from_user.id]['game'] and message.text.lower() in ["камень", "ножницы", "бумага"]:
        res = f.game(message.text)
        bot.send_message(message.chat.id, res + '\n' + "Сыграем еще?)")

    elif users[message.from_user.id]['game'] and message.text.lower() == "да":
        users[message.from_user.id]['game'] = True

    elif users[message.from_user.id]['game'] and message.text.lower() == "нет":
        users[message.from_user.id]['game'] = False

    elif users[message.from_user.id]['game']:
        bot.send_message(message.chat.id, "Ты ввел что-то неправильно, повтори пожалуйста!")
    else:
        bot.send_message(message.chat.id, "a)")


bot.polling(none_stop=True, interval=0)
