import urllib
import time
import json
import requests
import os

TOKEN = "<your-bot-token>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
IMAGE_URL = "https://api.telegram.org/file/bot{}/".format(TOKEN)
DOWNLOADED_IMAGE_PATH = "/Telegram/"

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

def send_message(text,chat_id,reply_markup=None):
	"""Takes the text of the message we want to send (text) and the chat ID of the chat where we want to send the message (chat_id)"""
	text = urllib.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
	if reply_markup:
		url += "&reply_markup={}".format(reply_markup)
	get_url(url)

def request_image_path(photo_id):
    """Call this command https://api.telegram.org/bot<your-bot-token>/getFile?file_id=<id>, retrieves the information of the image selected and return the file path"""
    url = URL + "getFile?file_id={}".format(photo_id)
    js = get_json_from_url(url)
    file_path = js["result"]["file_path"]
    return file_path

def get_image(image_path):
    """Receive a path and download the image in a folder named Telegram"""
    filename = image_path[image_path.find("/")+1:]
    url = IMAGE_URL + image_path
    try:
        image_on_web = urllib.urlopen(url)
        buf = image_on_web.read()
        path = os.getcwd() + DOWNLOADED_IMAGE_PATH
        file_path = "%s%s" % (path, filename)
        downloaded_image = file(file_path, "wb")
        downloaded_image.write(buf)
        downloaded_image.close()
        image_on_web.close()
    except:
        return False
    return True

def handle_updates(updates):
    """Manage the incomming updates and check if the user send an image and call get_image method"""
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
        except:
            text = None
        chat = update["message"]["chat"]["id"]
        if text == "/start":
			send_message("Welcome to Image Bot. Send any image and I'll store it forever >:D", chat)
        elif text:
            send_message("That is not an image", chat)
        else:
            photo_list = update["message"]["photo"]
            biggest_index = len(photo_list)-1
            photo_id = photo_list[biggest_index]["file_id"]
            photo_path = request_image_path(photo_id)
            if get_image(photo_path):
                send_message("Image Saved", chat)
            else:
                send_message("Oops :C", chat)

def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"])> 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)

if __name__ == '__main__':
	main()
