#!/usr/bin/python3.7
#! -*- coding: utf-8 -*-

import requests
# import os
from time import sleep

url = "https://api.telegram.org/bot615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE/"

# os.system("sudo systemctl start tor")
# time.sleep(10)
def get_tor_session():
	session = requests.session()
	session.proxies = {"http" : "socks5://127.0.0.1:9050",
					   "https": "socks5://127.0.0.1:9050"}
	return session


def get_updates_json(request):
	# global session
	responce = session.get(request + "getUpdates")
	return responce.json()

def last_update(data):
	results = data["result"]
	# print(results)
	total_updates = len(results) - 1
	return results[total_updates]

def get_chat_id(update):
	chat_id = update["message"]["chat"]["id"]
	return chat_id

def send_mes(chat_id, text):
	# global session
	params = {"chat_id" : chat_id,
			  "text"	: text}
	responce = session.post(url + "sendMessage", data=params)
	return responce

def main():
	update_id = last_update(get_updates_json(url))["update_id"]
	while True:
		if update_id == last_update(get_updates_json(url))["update_id"]:
			send_mes(get_chat_id(last_update(get_updates_json(url))), "TEST")
			update_id += 1
	sleep(1)

if __name__ == "__main__":
	main()