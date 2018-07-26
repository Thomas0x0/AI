#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
import schedule
import traceback
import apiai, json
from time import sleep

class Bot():

	def __init__(self, token, name, botname):
		self.token = token
		self.name = name
		self.botname = botname
		self.url = "https://api.telegram.org/" + "bot" + token + '/'
		self.params = {"offset" : 1, "timeout": 30}

	def create_session(self):
		self.session = requests.session()
		# self.session.proxies = {"http": "socks5://127.0.0.1:9050",
		# 					"https": "socks5://127.0.0.1:9050"}

	def get_updates(self):
		method = self.url + "getUpdates" 
		request = self.session.get(method, data=self.params)
		self.data = request.json()["result"]
		if not self.data:
			self.data = None

	def updates_handling(self):
		if self.data:
			for update in self.data:
				self.params["offset"] = update["update_id"] + 1
				if "text" in update["message"]:
					message = update["message"]["text"]
					answer = self.ai_send(message)
					chat_id = update["message"]["chat"]["id"]
					self.send_message(chat_id, answer)
				else:
					self.send_message(chat_id, "Sorry, but I can't handle non-text")
		else:
			return

	def ai_send(self, text):
		request = apiai.ApiAI("de46c0b6430741018a4c3aa85083ddc9").text_request()
		request.lang = 'ru'
		request.session_id = 'test_network_bot'
		request.query = text
		response_json = json.loads(request.getresponse().read().decode('utf-8'))
		response = response_json['result']['fulfillment']['speech']
		return response

	def send_message(self, chat_id, text):
		params = {"chat_id": chat_id, "text": text}
		self.session.post(self.url + "sendMessage", data=params)


tns_bot = Bot("615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE",
			"TNS(Test Network Speed)",
			"network_speed_bot")
tns_bot.create_session()

while True:
	tns_bot.get_updates()
	tns_bot.updates_handling()
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