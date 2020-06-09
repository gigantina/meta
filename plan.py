import functions as f
import data
import diary
import analysis as ans
import check
import bot

while True:
    chats = data.get_chats()
    for user in chats:
        time = f.get_time(data.get_utc(user[0]))
        if time == '00-00-00':
            data.new_day(user[0])
        if time == '20-00-00':
            bot.reminder(user[0])
        if time == '15-00-00' and (check.get_tuesday(user[0]) or check.get_friday(user[0])):
            if diary.analize(user[0]) != None:
                bot.message_about(user[0])
                res = ans.analysis_sentiment(ans.analysis_data(diary.analize(user[0])))
                if not res:
                    message = 'Знаешь, в последнее время я вижу в тебе много негативных эмоций. Пожалуйста, если ты часто чувствуешь себя плохо, обратись к специалисту. Можешь воспользоваться этим анонимным телефоном доверия: \n 8-800-2000-122, звонок анонимный и бесплатный. Помни, это не стыдно!'
                elif res == 1:
                    message = 'Судя по твоему дневнику, с тобой все в порядке, ура!'
                else:
                    message = 'Ох, как бы странно это не звучало, но меня настораживает обильное количество позитива в твоем дневнике. Знаешь, не всегда много хороших эмоций - хорошо. Если тебя беспокоит твое состояние, обратись к специалисту'
            bot.results(user[0], message)
            check.tuesday_set(user[0], 0)
            check.friday_set(user[0], 0)
