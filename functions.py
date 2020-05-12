# -*- coding: utf-8 -*-

import random as r


def jokes():
    lines = '\n'.join([line.strip() for line in open('jokes.txt')])
    joke = lines.split('@')
    r.shuffle(joke)
    return joke[0]
jokes()