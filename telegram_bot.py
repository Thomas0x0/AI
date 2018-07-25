#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
import schedule
from time import sleep
# from datetime import datetime

# data = "sendMessage?chat_id=561706344&text="
# messages = ["Good morning", "Good afternoon",
# 			"Good evening", "Good night"]

# class BotHandler():

# 	def __init__(self, token):
# 		self.token = token
# 		self.api_url="https://api.telegram.org/bot{}".format(token)

	# def get_updates(self, offset=None, timeout=30):
	# 	params = {"timeout" : 100,
	# 				"offset": offset}

	# 	responce = session.get(self.api_url + "getUpdates", data=params)
	# 	result_json = responce.json()["result"]
	# 	return result_json

	# def get_last_update(self):
	# 	got_result = self.get_updates()
	# 	if len(got_result) > 0:
	# 		last_update = got_result[-1]
	# 	else:
	# 		last_update = got_result[len(got_result)]
	# 	return last_update

	# def get_chat_id(update):
	# 	chat_id = update["message"]["chat"]["id"]
	# 	return chat_id

# def send_message():
	# global session
	

# def main(text):
# 	# while True:
# 		# for message in messages:
# 	responce = requests.post(url + data + text)
# # greet_bot = BotHandler(token)  

# def get_updates():
# 	responce = requests.get(url + token + "/getUpdates")
# 	return responce.json()["result"]

def greetings(time):
	if time == "03:00":
		send_message(dev_chat_id, "Good morning!")
	elif time == "09:00":
		send_message(dev_chat_id, "Good afternoon!")
	elif time == "15:00":
		send_message(dev_chat_id, "Good evening!")
	else:
		send_message(dev_chat_id, "Good night!")

def send_message(chat_id, text):
	bot_url += "sendMessage?chat_id={}&text={}".format(
		chat_id, text)
	requests.post(bot_url)

def main():
	schedule.every().day.at("03:00").do(greetings, "03:00")
	schedule.every().day.at("09:00").do(greetings, "09:00")
	schedule.every().day.at("15:00").do(greetings, "15:00")
	schedule.every().day.at("21:00").do(greetings, "21:00")

	while True:
		try:
			schedule.run_pending()
			sleep(60)
		except Exception:
			print(Exception)
			send_message(dev_chat_id, Exception)
			exit()


site = "https://api.telegram.org/bot"
token = "615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE"
bot_url = site + token + '/'
dev_chat_id = "561706344"

if __name__ == '__main__':
	main()
