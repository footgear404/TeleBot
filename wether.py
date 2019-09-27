import pyowm
#import telebot

owm = pyowm.OWM('0a0a399230fb79e20714cd2cea269ff6', language = "ru")
#bot= telebot.TeleBot('640054178:AAEbilhnCSRF5OfqtEK5C_0_3TD4fqpcGiM')

place = input('Введите город ')
observation = owm.weather_at_place(place)
w = observation.get_weather()
temp = w.get_temperature('celsius')["temp"]
print(observation, w, temp)


#bot.polling(none_stop=True, interval=0)
#@bot.message_handler(content_types=['text'])
#def get_text_messages(message):
#	if message.text == "Привет" or message.text == "привет":
#	    bot.send_message(message.from_user.id, "Привет, хочешь узнать погоду?")
#
#	elif message.text == "Дай" or message.text == "дай":
#	    bot.send_message(message.from_user.id, "Хуяй - " + "t.me/addstickers/mfnshit")
#	else:
#	    bot.send_message(message.from_user.id, "Пока этому меня не обучили. Функционал ограничен :( Напиши /help.")






