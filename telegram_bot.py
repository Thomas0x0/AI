#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
import schedule
import sqlite3
import json
from apiai import ApiAI
from multiprocessing import Process
from time import sleep

conn = sqlite3.connect('users.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT chat_id FROM telegram_users')
user_chat_ids = list(cursor.fetchall()[0])


class Bot():

	def __init__(self, token, name, botname):
		self.token = token
		self.name = name
		self.botname = botname
		self.url = "https://api.telegram.org/" + "bot" + token + '/'
		self.params = {"offset" : 1, "timeout": 30}
		self.methods = {'getUpdates': self.url + 'getUpdates',
					    'sendMessage': self.url + 'sendMessage'}

	def create_session(self):
		self.session = requests.session()
		self.session.proxies = {"http": "socks5://127.0.0.1:9050",
							"https": "socks5://127.0.0.1:9050"}

	def get_updates(self):
		request = self.session.get(self.methods['getUpdates'],
								 data=self.params)
		self.updates = request.json()['result']
		if not self.updates: # If no updates, set them to None
			self.updates = None

	def updates_handling(self):
		if self.updates:
			for update in self.updates:
				self.params['offset'] = update['update_id'] + 1

				user_chat_id = update['message']['chat']['id']
				if user_chat_id not in user_chat_ids:
					user_information = {
						'user_chat_id': update['message']['from']['id'],
						'first_name': update['message']['from']['first_name'],
						'chat_id': user_chat_id
						}
					if 'last_name' in update['message']['from']:
						user_information['last_name'] = update['message']['from']['last_name']
					else:
						user_information['last_name'] = None
					if 'username' in update['message']['from']:
						user_information['username'] = update['message']['from']['username'] 
					else:
						user_information['username'] = None
					cursor.execute("""INSERT INTO telegram_users
						VALUES (Null, {0}, '{1}', '{3}', '{4}', {2})""".format(*user_information.values()))
					conn.commit()
					user_chat_ids.append(user_chat_id)

				if "text" in update["message"]: # If message's type is text
					response = self.ai_response(update['message']['text'])
					if response:
						self.send_message(user_chat_id, response)
					else:
						self.send_message(user_chat_id, 
							'Извини, такой текст не понимаю')
				elif 'photo' in update['message']:
					self.send_message(user_chat_id,
						'Извини, фотографии не распознаю')
				else: # If message's type isn't text
					self.send_message(user_chat_id,
						'Извини, я не понимаю')

	def ai_response(self, text):
		request = ApiAI("de46c0b6430741018a4c3aa85083ddc9").text_request()
		request.lang = 'ru'
		request.session_id = 'test_network_bot'
		request.query = text
		response_raw = request.getresponse().read().decode('utf-8')
		response_json = json.loads(response_raw)
		response = response_json['result']['fulfillment']['speech']
		self.response = response
		return response

	def send_message(self, chat_id, text):
		params = {"chat_id": chat_id, "text": text}
		self.session.post(self.methods['sendMessage'], data=params)

	def dispatch(self, text):
		cursor.execute("SELECT chat_id FROM telegram_users -- WHERE chat_id != 561706344")
		for chat_id in cursor.fetchall():
			self.send_message(chat_id[0], text)

	def good_morning_creator(self):
		cursor.execute("SELECT id FROM telegram_users DESC LIMIT 1")
		records_amount = cursor.fetchall()[0][0]
		self.send_message(561706344,
			'Доброе утро, создатель! На данный момент в вашей базе данных {} записей'.format(records_amount))

tns_bot = Bot("615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE",
			"TNS(Test Network Speed)",
			"network_speed_bot")
tns_bot.create_session()

schedule.every().day.at('03:00').do(tns_bot.good_morning_creator)
schedule.every().day.at('09:00').do(tns_bot.send_message, 561706344, 'Не забывайте покушать!!!')
schedule.every().day.at('15:00').do(tns_bot.send_message, 561706344, 'Пора прогуляться???')
schedule.every().day.at('21:00').do(tns_bot.send_message, 561706344, 'Доброй ночи!')

schedule.every().day.at('03:00').do(tns_bot.dispatch, 'Доброе утро!')
schedule.every().day.at('09:00').do(tns_bot.dispatch, 'Время покушать!')
schedule.every().day.at('21:00').do(tns_bot.dispatch, 'Доброй ночи!')

def main():
	while True:
		tns_bot.get_updates()
		tns_bot.updates_handling()

def main1():
	while True:
		schedule.run_pending()
		sleep(60)

proc1 = Process(target=main)
proc2 = Process(target=main1)

if __name__ == '__main__':
	# main()
	proc1.start()
	proc2.start()
# dev_chat_id = "561706344"
# site = "https://api.telegram.org/bot"
# token = ""
# bot_url = site + token + '/'
# data = {"offset" : 1, "timeout" : 30}

# def get_updates():
# 	global bot_url, data
# 	request_json = requests.get(bot_url + "getUpdates",
# 						 data=data).json()
# 	if not request_json["result"]:
# 		sleep(1)
# 		return

# 	for update in request_json["result"]:
# 		data["chat_id"] = update["message"]["chat"]["id"]

# 		if not "message" in update or "text" in update["message"]:
# 			responce = "Извините, я пока не распознаю НЕ текст."
# 		else:
# 			responce = sendapiai(update["text"])
# 		send_message(data["chat_id"], responce)
# 		data["offset"] = update["update_id"] + 1

# def sendapiai(text):
# 	request = apiai.ApiAi("de46c0b6430741018a4c3aa85083ddc9").text_request()
# 	request.lang = "ru"
# 	request.session_id = "network_speed_bot"
# 	request.query = text

# 	responceJson = json.loads(request.getresponce().read().decode("utf-8"))
# 	responce = responceJson["result"]["fullfillment"]["speech"]

# 	if responce:
# 		return responce
# 	else:
# 		return "Я вас не понял!"

# def greetings(time):
# 	print("Greetings function started working.")
# 	if time == "03:00":
# 		send_message(dev_chat_id, "Good morning!")
# 	elif time == "09:00":
# 		send_message(dev_chat_id, "Good afternoon!")
# 	elif time == "15:00":
# 		send_message(dev_chat_id, "Good evening!")
# 	else:
# 		send_message(dev_chat_id, "Good night!")

# def send_message(chat_id, text):
# 	global bot_url
# 	bot_url += "sendMessage?chat_id={}&text={}".format(
# 		chat_id, text)
# 	responce = requests.post(bot_url)
# 	if responce.status_code == 200:
# 		print("Message sent to {}.".format(chat_id))
# 	else:
# 		print("Message not sent. Error code: ",
# 		 responce.status_code)

# def main():
# 	# schedule.every().day.at("03:00").do(greetings, "03:00")
# 	# schedule.every().day.at("09:00").do(greetings, "09:00")
# 	# schedule.every().day.at("15:00").do(greetings, "15:00")
# 	# schedule.every().day.at("21:00").do(greetings, "21:00")

# 	while True:
# 		try:
# 			get_updates()
# 			# schedule.run_pending()
# 			# sleep(60)
# 		except:
# 			traceback.print_exc()

# 			send_message(dev_chat_id, repr(error))
# 			exit()


# if __name__ == '__main__':
# 	print("Bot started working.")
# 	main()