from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


def analysis_data(messages):
    res = []
    tokenizer = RegexTokenizer()
    model = FastTextSocialNetworkModel(tokenizer=tokenizer)
    print(messages)
    i = 0
    for message in messages:
        data = model.predict([message], k=2)[0]
        i += 1
        for key, value in data.items():
            if round(value, 1) == 1:
                res.append(key)
        if len(res) != i:
            res.append('neutral')
    return res


def analysis_sentiment_data(
        sentiments):  # 0 - повод задуматься над своим состоянием (много негатива), 1 - все нормально, 2 - состояние эйфории (тоже может быть опасно)
    if sentiments.count('negative') >= (len(sentiments) // 2) + 2:
        return 0
    if sentiments.count('positive') >= len(sentiments) // 2 + len(sentiments) // 4 + 1:
        return 2
    else:
        return 1

def analysis_sentiment(sentiment):
    if sentiment[0] == 'negative':
        return 0
    if sentiment[0] == 'positive':
        return 2
    else:
        return 1


