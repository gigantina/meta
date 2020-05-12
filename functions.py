# -*- coding: utf-8 -*-

import random as r
from emoji import emojize

emoji = {}
emoji["камень"] = emojize(':package:')
emoji["ножницы"] = emojize(':scissors:')
emoji["бумага"] = emojize(':newspaper:')


def jokes():
    lines = '\n'.join([line.strip() for line in open('jokes.txt')])
    joke = lines.split('@')
    r.shuffle(joke)
    return joke[0]


def game(choice):
    global emoji
    computer = r.choice(["камень", "ножницы", "бумага"])
    choice = choice.lower()

    if computer == choice:
        res = "Ничья! Я тоже выбрал " + emoji[computer]
    elif (computer == "камень" and choice == "бумага") or (computer == "бумага" and choice == "ножницы") or (
            computer == "ножницы" and choice == "камень"):
        res = "Вы выиграли! Я выбрал " + emoji[computer]
    else:
        res = "Вы проиграли! Я выбрал " + emoji[computer]
    return res
