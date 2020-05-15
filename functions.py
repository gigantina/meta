# -*- coding: utf-8 -*-

import random as r
import emoji as e
from pymorphy2 import MorphAnalyzer

places = {}


def from_e_to_game(choice):
    res = False
    if choice in ["камень", "ножницы", "бумага"]:
        return choice
    elif choice[0] == u'\U00002702':
        res = "ножницы"
    elif choice == u'\U0001F48E':
        res = "камень"
    elif choice == u'\U0001F4F0':
        res = "бумага"
    return res


def jokes():
    lines = '\n'.join([line.strip() for line in open('jokes.txt')])
    joke = lines.split('@')
    r.shuffle(joke)
    return joke[0]


def game(choice):
    computer = r.choice(["камень", "ножницы", "бумага"])

    if computer == choice:
        res = "Ничья! Я тоже выбрал " + e.game[computer]
    elif (computer == "камень" and choice == "бумага") or (computer == "бумага" and choice == "ножницы") or (
            computer == "ножницы" and choice == "камень"):
        res = "Вы выиграли! Я выбрал " + e.game[computer]
    else:
        res = "Вы проиграли! Я выбрал " + e.game[computer]
    return res


def place(message):
    global places
    m = MorphAnalyzer()
    word = m.parse(message)[0]
    if 'гео' in word.tag.cyr_repr:
        if message not in places:
            places[message] = r.choice(["Отличное место! Бывало, что я заползал туда иногда, раз в месяцок",
                                        "О да, знаю, там подают таки-и-ие блюда!",
                                        "Ну, знаешь, насчет этого места. Тут точно дело вкуса, обычному туристу лучше сюда не соваться...",
                                        "Место, откровенно говоря, так себе...",
                                        "Это одно из моих любимых мест на планете! Когда будет возможность, обязательно посети",
                                        "Это место меня отталкивает, даже не планируй туда поездку",
                                        "Да ладно, нашел место для отдыха!", "Погодка там так себе",
                                        "Ну, ничего, норм выбор",
                                        "Как тебе вообще в голову пришло туда захотеть поехать?!",
                                        "Для питона как раз!)"])
        return places[message]
    return False


def send_mem():
    n = r.randint(1, 1011)
    way = 'memes/mem ({}).jpg'.format(n)
    photo = open(way, 'rb')
    return photo