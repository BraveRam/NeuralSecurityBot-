import telebot
from telebot.types import *
import random
import time
from datetime import datetime, timedelta
import time 
from threading import Timer
import utilities

bot = telebot.TeleBot(utilities.BOT_TOKEN)

channel = [utilities.SUB_CHANNEL]

TIMER = None

def gotcha(callback):    
    user = int(callback.data.split(":")[1])
    if not callback.from_user.id == user:
    	return bot.answer_callback_query(callback.id, "❌This message is not for you!", show_alert = True)
    else:          
        if callback.data.startswith("add"):
        	bot.delete_message(callback.message.chat.id, callback.message.message_id)
        	bot.answer_callback_query(callback.id, f" 😉Welcome To Our Group✳️\nHave A Good Time🤝", show_alert = True)
        	bot.restrict_chat_member(callback.message.chat.id, user, can_send_messages = True)
        	msg = bot.send_message(chat_id=callback.message.chat.id, text=utilities.WELCOME_MSG, parse_mode="html")
        	time.sleep(5)
        	bot.delete_message(chat_id=callback.message.chat.id, message_id=msg.message_id)
        else:
        	bot.delete_message(callback.message.chat.id, callback.message.message_id)
        	z = bot.send_message(callback.message.chat.id, "❌Verification Failed🔕\nThey can Join this group after 1 day🤖")
        	bot.ban_chat_member(callback.message.chat.id, user, until_date = datetime.now() + timedelta(days=1))
        	time.sleep(120)
        	bot.delete_message(callback.message.chat.id, z.message_id)
        		
def timeout(message, member, delete):
	bot.delete_message(message.chat.id, delete)
	bot.ban_chat_member(message.chat.id, member.id, until_date = datetime.now() + timedelta(days=1))

def captcha(message, member):
    global TIMER
    num1 = random.randint(10, 30)
    num2 = random.randint(10, 30)
    r1 = random.randint(10, 30)
    r2 = random.randint(10, 30)
    r3 = random.randint(10, 30)
    r4 = random.randint(10, 30)
    r5 = random.randint(10, 30)
    buttons = {f"r1:{member.id}":r1, f"r2:{member.id}":r2, f"add:{member.id}":f"{num1 + num2}", f"r3:{member.id}":r3, f"r4:{member.id}":r4, f"r5:{member.id}":r5}
    btns = []
    keyboard = InlineKeyboardMarkup(row_width=2)    
    for key, value in buttons.items():
        btns.append(InlineKeyboardButton(text=value, callback_data=key))
    random.shuffle(btns)
    keyboard.add(*btns)
    bot.restrict_chat_member(message.chat.id, f"{message.from_user.id}")
    file_info = bot.get_file(bot.get_chat(message.chat.id).photo.big_file_id)
    photo = bot.download_file(file_info.file_path)
    idToDelete = bot.send_photo(message.chat.id,photo=photo, caption = f"✨{member.first_name} Hello and Welcome to {message.chat.title}👋\n\n<i>Please solve this captcha In Three(3) minutes in order to make sure that you are not a robot🤖</i>\n<u>Keep in mind that if do not solve this captcha in a given time, you will be kicked:)</u>\n\n <b>{num1} + {num2} = ____</b>", reply_markup = keyboard, parse_mode = "html", protect_content = True)
    delete = idToDelete.message_id
    TIMER = Timer(180.0, timeout, args=[message, member, delete])
    TIMER.start()    
   	
@bot.message_handler(content_types =["new_chat_members"])
def chat(message):
	global TIMER
	g = bot.get_me().id	
	a = bot.get_chat_member(message.chat.id, g)	
	if a.status not in ["administrator"]:
		pass	
	else:
		pass	
	for member in message.new_chat_members:
		d = bot.get_chat_member(message.chat.id, member.id)		
		if d.can_send_messages != False:
			pass
		else:
			bot.restrict_chat_member(message.chat.id, member.id, until_date = datetime.now() + timedelta(days=1))
			bot.ban_chat_member(message.chat.id, member.id, until_date = datetime.now() + timedelta(days=1))	
			return 		
		bot.delete_message(message.chat.id, message.message_id)		
		if member.id == g:
			bot.send_message(message.chat.id, "🔔Thanks for adding me in {}🔔\n👮‍♂️Make me an admin then i'll work properly⚙️".format(message.chat.title))
		else:
			bot.restrict_chat_member(message.chat.id, f"{message.from_user.id}")			
			captcha(message, member)			
			

@bot.callback_query_handler(func = lambda callback: True)
def ans(callback):
    global TIMER
    try:	    	
    	TIMER.cancel()
    	gotcha(callback)
    except:
    	bot.delete_message(callback.message.chat.id, callback.message.message_id)

def is_bot_admin_fun(chat_id, bot_id):
  if bot.get_chat_member(chat_id, bot_id).status in ["administrator"]:
   return True
  else:
   return False

def is_neural_group_fun(message):
  if message.chat.username == "captcha_group":
   return True
  else:
   return False

def is_group_admin_fun(chat_id, user_id):
    if bot.get_chat_member(chat_id, user_id).status in ["creator", "administrator"]:
        return True
    else:
        return False

def mute_member_fun(chat_id, user_id):
    bot.restrict_chat_member(chat_id, user_id, can_send_messages=False)

def unmute_member_fun(chat_id, user_id):
    bot.restrict_chat_member(chat_id, user_id, can_send_messages=True)

def ban_member_fun(chat_id, user_id):
    bot.ban_chat_member(chat_id, user_id)

def unban_member_fun(chat_id, user_id):
    bot.unban_chat_member(chat_id, user_id, only_if_banned=True)

def kick_member_fun(chat_id, user_id):
    bot.kick_chat_member(chat_id, user_id)

def is_message_replied_fun(message):
    if message.reply_to_message:
        return True
    else:
        return False

def is_links_fun(message):
    is_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
    if "http" in message.text or "https" in message.text:
        if is_admin == False:
            return bot.delete_message(message.chat.id, message.message_id)
        else:
            pass
    else:
        pass

def is_markup_fun(message):
    is_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
    if message.reply_markup:
        if is_admin == False:
            return bot.delete_message(message.chat.id, message.message_id)
        else:
            pass
    else:
        pass


@bot.message_handler(commands =["start"])
def start(message):
	bot.send_message(message.chat.id, "✳️{} This Bot Is A Group Manager Of <b>@NeuralG</b>".format(message.chat.first_name), reply_markup = utilities.chatbtn(), parse_mode="html")

@bot.message_handler(commands =["warn"])
def warn_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id		
			if is_bot_admin == True:
				if is_group_admin == True:
					bot.send_message(message.chat.id, f"{message.from_user.first_name}: {utilities.WARN_MSG}", reply_to_message_id=message.reply_to_message.message_id)					
					bot.delete_message(message.chat.id, message.message_id)
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass


@bot.message_handler(commands =["mute"])
def mute_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					mute_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"😶Shhh, {message.reply_to_message.from_user.first_name}: has been muted:)", reply_to_message_id=message.reply_to_message.message_id)
					bot.delete_message(message.chat.id, message.message_id)					
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass

@bot.message_handler(commands =["unmute"])
def unmute_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					unmute_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"🤠Speak, {message.reply_to_message.from_user.first_name}: has been unmuted:)", reply_to_message_id=message.reply_to_message.message_id)
					bot.delete_message(message.chat.id, message.message_id)					
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass

@bot.message_handler(commands =["kick"])
def kick_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					kick_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name}: has been kicked:)", reply_to_message_id=message.reply_to_message.message_id)
					bot.delete_message(message.chat.id, message.message_id)					
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass
		

@bot.message_handler(commands =["ban"])
def ban_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					ban_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name}: has been banned:)", reply_to_message_id=message.reply_to_message.message_id)
					bot.delete_message(message.chat.id, message.message_id)
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass

@bot.message_handler(commands =["dban"])
def dban_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					ban_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name}: has been banned:)")
					bot.delete_message(message.chat.id, message.message_id)
					bot.delete_message(message.chat.id, message.reply_to_message.message_id)
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass
		

@bot.message_handler(commands =["unban"])
def unban_user(message):
	is_neural_group = is_neural_group_fun(message)	
	is_bot_admin = is_bot_admin_fun(message.chat.id, bot.get_me().id)
	is_group_admin = is_group_admin_fun(message.chat.id, message.from_user.id)
	if is_neural_group == True:
		if message.reply_to_message:
			user_id = message.reply_to_message.from_user.id			
			if is_bot_admin == True:
				if is_group_admin == True:
					unban_member_fun(message.chat.id, user_id)
					bot.send_message(message.chat.id, f"{message.reply_to_message.from_user.first_name}: has been unbanned:)", reply_to_message_id=message.reply_to_message.message_id)
					bot.delete_message(message.chat.id, message.message_id)
				else:
					return bot.reply_to(message, "This command only works for admins:)")
			else:
				return bot.reply_to(message, "🙂I\'m unable to do this action because I\'m not admin:(")
		else:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		pass

@bot.message_handler(func = lambda message: True, chat_types=["supergroup", "group"])
def handle_all(message):
	if bot.get_chat_member("@neuralp", message.from_user.id).status == "left":
		bot.delete_message(message.chat.id, message.message_id)
		bot.send_message(message.chat.id, f"⬛{message.from_user.first_name}, Kindly Join Our Channel before writing a message here:)", reply_markup=utilities.sub_btn())
	else:
		pass
	is_neural_group = is_neural_group_fun(message)
	is_markup = is_markup_fun(message)
	is_links = is_links_fun(message)
	if is_neural_group == True:
		if is_markup == True:
			pass
		elif is_links == True:
			return bot.delete_message(message.chat.id, message.message_id)
		else:
			pass
	else:
		pass

print("Up & Running...")		
bot.infinity_polling()
 
