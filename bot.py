# -*- coding: utf-8 -*-

import telebot

import functions as f

TOKEN = '1114362533:AAEBwGiAgdotOuwqWFLXCbmGTf2yCJIENQU'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Привет, {}! Я Длиннохвостик - веселый питон, а что самое интересное, я написан на Python,как иронично) Я могу стать отличным собеседником, могу рассказать шутку, мы можем поиграть в камень-ножницы-бумагу, отправить мем или оценить вашу фотографию. А также много чегоеще, я надеюсь, что вам со мной будет интересно)".format(
                         message.from_user.first_name))


@bot.message_handler(content_types=['text'])
def dialog(message):
    if ("шутк" in str(message.text).lower() or "шутей" in str(
            message.text).lower() or "прикол" in str(message.text).lower()) and ("прикольно" not in str(message.text).lower()):
        joke = f.jokes()
        bot.send_message(message.chat.id, joke)
    else:
        bot.send_message(message.chat.id, "a)")


bot.polling(none_stop=True, interval=0)
