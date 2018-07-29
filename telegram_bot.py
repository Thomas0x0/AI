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
user_chat_ids = [i for i in cursor.fetchall()]


class Bot():

	def __init__(self, token):
		self.token = token
		self.url = "https://api.telegram.org/" + "bot" + token + '/'
		self.params = {"offset" : 1, "timeout": 60}
		self.methods = {'getUpdates': self.url + 'getUpdates',
					    'sendMessage': self.url + 'sendMessage'}

	def get_updates(self):
		request = requests.get(self.methods['getUpdates'],
								 data=self.params)
		self.updates = request.json()['result']
		if not self.updates: # If no updates, set them to blank list
			self.updates = []

	def updates_handling(self):
		for update in self.updates: # If it is blank, won't be working
			self.params['offset'] = update['update_id'] + 1

			user_chat_id = update['message']['chat']['id']
			if user_chat_id not in user_chat_ids:
				self.add_user_to_db(update['message'])

			if "text" in update["message"]: # If message's type is text
				response = self.ai_response(update['message']['text'])
				if response:
					self.send_message(user_chat_id, response)
				else:
					self.send_message(user_chat_id, 
						'Не понял')
			elif 'photo' in update['message']:
				self.send_message(user_chat_id,
					'Извини, фотографии не распознаю')
			else: # If message's type isn't text
				self.send_message(user_chat_id,
					'Извини, я не понимаю')

	def add_user_to_db(self, update):
		user_information = {
						'user_chat_id': update['from']['id'],
						'first_name': update['from']['first_name'],
						'chat_id': update['chat']['id']
						}
		if 'last_name' in update['from']:
			user_information['last_name'] = update['from']['last_name']
		else:
			user_information['last_name'] = None
		if 'username' in update['from']:
			user_information['username'] = update['from']['username'] 
		else:
			user_information['username'] = None
		cursor.execute("""INSERT INTO telegram_users
			VALUES (Null, {0}, '{1}', '{3}', '{4}', {2})""".format(*user_information.values()))
		conn.commit()
		user_chat_ids.append(user_chat_id)

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
		cursor.execute("SELECT chat_id FROM telegram_users WHERE chat_id != 561706344")
		for chat_id in cursor.fetchall():
			self.send_message(chat_id[0], text)

	def good_morning_creator(self):
		cursor.execute("SELECT id FROM telegram_users DESC LIMIT 1")
		records_amount = cursor.fetchall()[0][0]
		if (record_amount % 10 < 5 and 
			record_amount % 10 > 1):
			word = 'записи'
		elif record_amoun % 10 == 1:
			word = 'запись'
		else:
			word = 'записей'
		self.send_message(561706344,
			'Доброе утро, создатель! На данный момент в вашей базе данных {} {}'.format(records_amount,
				word))


def main():
	while True:
		tns_bot.get_updates()
		tns_bot.updates_handling()

def main1():
	while True:
		schedule.run_pending()
		sleep(60)



if __name__ == '__main__':
	tns_bot = Bot("615432346:AAF5DadZtgo8isAWdNyXaC3oy3QtzAjwphE")

	schedule.every().day.at('03:00').do(tns_bot.good_morning_creator)
	schedule.every().day.at('09:00').do(tns_bot.send_message, 561706344, 'Не забывайте покушать!!!')
	schedule.every().day.at('15:00').do(tns_bot.send_message, 561706344, 'Пора прогуляться???')
	schedule.every().day.at('21:00').do(tns_bot.send_message, 561706344, 'Доброй ночи!')

	schedule.every().day.at('03:00').do(tns_bot.dispatch, 'Доброе утро!')
	schedule.every().day.at('09:00').do(tns_bot.dispatch, 'Время покушать!')
	schedule.every().day.at('21:00').do(tns_bot.dispatch, 'Доброй ночи!')

	proc1 = Process(target=main)
	proc2 = Process(target=main1)
	proc1.start()
	proc2.start()

