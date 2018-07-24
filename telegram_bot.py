#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
from time import sleep
from datetime import datetime

# while (datetime.now().hour != 0 and
# 		datetime.now().minute != 0):
# 	sleep(60)

token = "615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE/"
url = "https://api.telegram.org/bot" + token
chat_id = "561706344"
messages = ["Good morning", "Good afternoon",
			"Good evening", "Good night"]
data = "sendMessage?chat_id={}&text=".format(chat_id)
# os.system("sudo systemctl start tor")
# time.sleep(10)
# def get_tor_session():
# 	session = requests.session()
# 	session.proxies = {"http" : "socks5://127.0.0.1:9050",
# 						"https": "socks5://127.0.0.1:9050"}
# 	return session

# session = get_tor_session()

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
	

def main():
	while True:
		# for message in messages:
		responce = requests.post(url + data + "Hello!")
		sleep(90)

# greet_bot = BotHandler(token)  


# def main():  
#     new_offset = None

#     while True:
#         greet_bot.get_updates(new_offset)

#         last_update = greet_bot.get_last_update()

#         last_update_id = last_update['update_id']
#         last_chat_text = last_update['message']['text']
#         last_chat_id = last_update['message']['chat']['id']
#         last_chat_name = last_update['message']['chat']['first_name']

#         if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
#             greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
#             today += 1

#         elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
#             greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
#             today += 1

#         elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
#             greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
#             today += 1

#         new_offset = last_update_id + 1

if __name__ == '__main__':  
        main()