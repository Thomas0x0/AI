#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
import schedule
from time import sleep

site = "https://api.telegram.org/bot"
token = "615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE"
bot_url = site + token + '/'
dev_chat_id = "561706344"

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
	bot_url = "sendMessage?chat_id={}&text={}".format(
		chat_id, text)
	responce = requests.post(bot_url)
	if responce.status_code == 200:
		print("Message send to {}.".format(chat_id))
	else:
		print("Message not send. Error code: ",
		 responce.status_code)

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


if __name__ == '__main__':
	print("Bot started working.")
	main()