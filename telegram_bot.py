#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
import schedule
import apiai, json
from time import sleep

site = "https://api.telegram.org/bot"
token = "615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE"
bot_url = site + token + '/'
dev_chat_id = "561706344"
data = {"offset" : 1, "timeout" : 30}

def get_updates():
	global bot_url, data
	request_json = requests.get(bot_url + "getUpdates",
						 data=data).json()
	if not request_json["result"]:
		sleep(1)
		return

	for update in request_json["result"]:
		data["chat_id"] = update["chat"]["id"]

		if not "message" in update or "text" in update["message"]:
			responce = "Извините, я пока не распознаю НЕ текст."
		else:
			responce = sendapiai(update["text"])
		send_message(data["chat_id"], responce)
		data["offset"] = update["update_id"]

def sendapiai(text):
	request = apiai.ApiAi("de46c0b6430741018a4c3aa85083ddc9").text_request()
	request.lang = "ru"
	request.session_id = "network_speed_bot"
	request.query = text

	responceJson = json.loads(request.getresponce().read().decode("utf-8"))
	responce = responceJson["result"]["fullfillment"]["speech"]

	if responce:
		return responce
	else:
		return "Я вас не понял!"

def greetings(time):
	print("Greetings function started working.")
	if time == "03:00":
		send_message(dev_chat_id, "Good morning!")
	elif time == "09:00":
		send_message(dev_chat_id, "Good afternoon!")
	elif time == "15:00":
		send_message(dev_chat_id, "Good evening!")
	else:
		send_message(dev_chat_id, "Good night!")

def send_message(chat_id, text):
	global bot_url
	bot_url += "sendMessage?chat_id={}&text={}".format(
		chat_id, text)
	responce = requests.post(bot_url)
	if responce.status_code == 200:
		print("Message sent to {}.".format(chat_id))
	else:
		print("Message not sent. Error code: ",
		 responce.status_code)

def main():
	# schedule.every().day.at("03:00").do(greetings, "03:00")
	# schedule.every().day.at("09:00").do(greetings, "09:00")
	# schedule.every().day.at("15:00").do(greetings, "15:00")
	# schedule.every().day.at("21:00").do(greetings, "21:00")

	while True:
		try:
			get_updates()
			# schedule.run_pending()
			# sleep(60)
		except Exception:
			print(repr(Exception))
			send_message(dev_chat_id, repr(Exception))
			exit()


if __name__ == '__main__':
	print("Bot started working.")
	main()