from telebot.types import *

BOT_TOKEN = "5769907387:AAF0tVVa2RNQjFpOeYmRAIWBhzIBa1jFp4E"
SUB_CHANNEL = "@neuralp"
WARN_MSG = "🤠Be Careful! This is your last chance⚠️"
WELCOME_MSG = "👋Hello, You Have Successfully Passed Captcha🤠"

def chatbtn():
	chatbtn = InlineKeyboardMarkup()
	a = InlineKeyboardButton(text ="✨Join Our Chat✨", url="t.me/neuralg")
	chatbtn.add(a)
	return chatbtn

def sub_btn():
	join =InlineKeyboardMarkup()
	j = InlineKeyboardButton("🤠Join The Channel🤠", url="t.me/neuralp")
	join.add(j)
	return join



 
