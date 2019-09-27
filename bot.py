import pyowm
import telebot
import os

owm = os.environ.get('OWM_TOKEN')
bot = os.environ.get('TELEBOT_TOKEN')

#Переменные
start_mess = "Я здесь, все вижу, все слышу   ^-_-^ "
help_mess = "/now " + "- узнать погоду в Астрахани"
default_city = "Астрахань"
hello_img = 'https://www.meme-arsenal.com/memes/3382ef92cd4fb324948340543935d4af.jpg'

#Блок команд:------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def start_handler(message):
	bot.send_photo(message.chat.id, hello_img)
	bot.send_message(message.chat.id, start_mess)
	bot.send_message(message.chat.id, "/help" + "- для всех команд")

@bot.message_handler(commands=['help'])
def help_handler(message):
	bot.send_message(message.chat.id, help_mess)
	bot.send_message(message.chat.id, "Попросить стикеры - \"Бот дай стикеры\" или \"дай\"")

#Погода в Астрахани.
@bot.message_handler(commands=['now'])
def weather_now(message):
	observation = owm.weather_at_place(default_city)
	w = observation.get_weather()
	status = "В городе " + default_city + " сейчас " + w.get_detailed_status() + "\n"
	temp = w.get_temperature('celsius')["temp"] + float(1.1)

	#Формируем ответ
	answer = status + "Температура воздуха °" + str(temp)
	
	#Отправка сообщения
	bot.send_message(message.chat.id, answer)
#-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text.lower() == "бот привет":
		bot.send_photo(message.chat.id, hello_img)
		bot.send_message(message.chat.id, start_mess)
		bot.send_message(message.chat.id, "/help" + "- для всех команд")
	elif message.text.lower() == "дай" or message.text.lower() == "бот дай стикеры":
	    bot.send_message(message.chat.id, "Здесь будут стикеры когда Надя их сделает :)")
bot.polling(none_stop=True, interval=0)
