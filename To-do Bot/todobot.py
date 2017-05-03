import urllib
import time
import json
import requests
from dbhelper import DBHelper

db = DBHelper()
TOKEN = "<your-bot-token>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
	"""Downloads the content from a URL and gives us a string"""
	response = requests.get(url)
	content = response.content.decode("utf8")
	return content

def get_json_from_url(url):
	"""Gets the string response as above and parses this into a Python dictionary using json.loads()"""
	content = get_url(url)
	js = json.loads(content)
	return js

def get_updates(offset=None):
	"""Call this command https://api.telegram.org/bot<your-bot-token>/getUpdates and retrieves a list of updates"""
	url = URL + "getUpdates?timeout=100"
	if offset:
		#If this is specified, we'll pass it along to the Telegram API to indicate that we don't want to receive any messages with smaller IDs this.
		url += "&offset={}".format(offset)
	js = get_json_from_url(url)
	return js

def get_last_update_id(updates):
	"""Calculates the highest ID of all the updates we receive from getUpdates"""
	update_ids = []
	for update in updates["result"]:
		update_ids.append(int(update["update_id"]))
	return max(update_ids)

def send_message(text,chat_id):
	"""Takes the text of the message we want to send (text) and the chat ID of the chat where we want to send the message (chat_id)"""
	text = urllib.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
	get_url(url)

def handle_updates(updates):
	"""Retreive all the items stored and check if the user want to delete or save it"""
	for update in updates["result"]:
		try:
			text = update["message"]["text"]
			chat = update["message"]["chat"]["id"]
			items = db.get_items()
			if text in items:
				db.delete_item(text)
				items = db.get_items()
			else:
				db.add_item(text)
				items = db.get_items()
			message = "\n".join(items)
			send_message(message, chat)
		except KeyError:
			pass

def main():
	db.setup()
	last_update_id = None
	while True:
		print("getting updates")
		updates = get_updates(last_update_id)
		if len(updates["result"]) > 0:
			last_update_id = get_last_update_id(updates) + 1
			handle_updates(updates)

if __name__ == '__main__':
	main()
