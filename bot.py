import pyowm
import telebot
import random
import sys
import datetime
from config import *
from stihi import zalezha_stih
from nadine import nadine_say

owm = pyowm.OWM(owm_token, language = "ru")
bot = telebot.TeleBot(bot_token)

async def handle(request):
    if request.match_info.get('bot') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)


hello_img = 'https://www.meme-arsenal.com/memes/3382ef92cd4fb324948340543935d4af.jpg'
STICKER_ID = 'CAADAgADDgAD_RR4HdA3b1i6s2BgFgQ'


#Блок команд:------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def start_handler(message):
	bot.send_photo(message.chat.id, hello_img)
	bot.send_message(message.chat.id, "Привет, смертный " + message.from_user.first_name + " ^-_-^ ")
	bot.send_message(message.chat.id, "/help " + "- для всех команд")

@bot.message_handler(commands=['help'])
def help_handler(message):
	bot.send_message(message.chat.id, "/stick - Наши стикеры "+ "\n" + "/whoi - Кто я?" + "\n" + "/zalezha - Случайный стих Елизаветы" + "\n" + "/now - Узнать текущую погоду" + "\n" + "/nadine - Рандомая фраза от Нади")

@bot.message_handler(commands=['stick'])
def sticker_pack_handler(message):
	bot.send_sticker(message.chat.id, STICKER_ID)
	bot.send_message(message.chat.id, "Чтобы поделиться используй ссылку - https://t.me/addstickers/what_is")


@bot.message_handler(commands=['zalezha'])
def zalezha(message):
	bot.send_message(message.chat.id, random.choice(zalezha_stih))

#Погода в Астрахани.
@bot.message_handler(commands=['now'])
def weather_now(message):
	observation = owm.weather_at_place(default_city)
	w = observation.get_weather()
	status = "В городе " + default_city + " сейчас " + w.get_detailed_status() + "\n"
	temp = w.get_temperature('celsius')["temp"]

	#Формируем ответ
	answer = status + "Температура воздуха °" + str(temp)

	#Отправка сообщения
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['whoi'])
def who_i(message):
	usr_id = str(message.from_user.id)
	none_switch_lname(message)
	none_switch_username(message)
	bot.reply_to(message, "Ты, " + message.from_user.first_name + " " + message.from_user.last_name + "\n" + "@" + message.from_user.username + "\n" + "Твой сраный id - " + usr_id)

@bot.message_handler(commands=['nadine'])
def nadine(message):
	bot.send_message(message.chat.id, "Как сказала бы Надя - \"" + random.choice(nadine_say) + "\"")

	#-----------------------------------------------------------------------------------------------------------------------
@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def get_text_messages(message):

	data_txt(message)
	contect_text = message.text.lower()
	if contect_text.lower() == "го":
		bot.send_message(message.chat.id, "ох уж эти задроты...")
	elif "слава богу" in contect_text or "бог" in contect_text:
		bot.send_message(message.chat.id, "бога нет.")
	elif "саня" in contect_text  or "сане" in contect_text or "санек" in contect_text or "саша" in contect_text:
		bot.reply_to(message, "@alexander_semenchuk по ходу о тебе речь, хозяин")
	elif "беда" in contect_text or "плохо" in contect_text or "жаль" in contect_text:
		bot.reply_to(message, "ой, хватит ныть..")
	elif "путин" in contect_text:
		bot.send_message(message.chat.id, "бога нет.")
	# if message.text.lower() == "бот привет":
	# 	start_handler(message)

	# elif message.text.lower() == "дай":
	# 	bot.send_sticker(message.chat.id, STICKER_ID)
	# 	bot.send_message(message.chat.id, "Чтобы поделиться используй ссылку - https://t.me/addstickers/what_is")

	# elif message.text.lower() == "кто я?":
	# 	none_switch_lname(message)
	# 	none_switch_username(message)
	# 	bot.reply_to(message, "Ты, " + message.from_user.first_name + " " + message.from_user.last_name + "\n" + "@" + message.from_user.username + "\n" + "Твой сраный id - " + usr_id)

	# elif  message.text.lower() == "а ты кто?" or message.text.lower() == "а ты кто":
	#     bot.send_message(message.chat.id, "Я бот, я бессмертен, а ты нет :)")

	# elif  message.text.lower() == "стих":
	#     bot.send_message(message.chat.id, random.choice(zalezha_stih))



def data_txt(message):

	uid = str(message.from_user.id)
	f = open("/var/TeleBot/data.txt", 'r')
	text = f.read()
	f.close()
	if uid in text:
		return
	else:
		none_switch_lname(message)
		none_switch_username(message)
		f = open("/var/TeleBot/data.txt", 'w')
		f.write(text + "\n" + str(message.from_user.first_name + " " + message.from_user.last_name + " | " + "@" + message.from_user.username) + " | ID - " + uid + " | " + tim_e(message) + "\n")
		f.close()

def none_switch_lname(message):
	if message.from_user.last_name == None:
		message.from_user.last_name = " "

def none_switch_username(message):
	if message.from_user.username == None:
		message.from_user.username = " "

def tim_e(message):
	unixtime = message.date
	timestamp = unixtime
	value = datetime.datetime.fromtimestamp(timestamp)
	return value.strftime('%Y-%m-%d' + " | " + ' %H:%M:%S')

bot.polling(none_stop=True, interval=0)
