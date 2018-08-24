import json
import requests
import time
import datetime
from urllib import parse

TOKEN = "661732683:AAGt7XLb6iWKTB3hrVnjNaKQAueaVctaRTs"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


# downloads the content from a URL as string
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


# gets the string response and parses into a json
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))

    return max(update_ids)


def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            if text == 'I love you':
                send_message("I love you too", chat)

            elif text == 'What is your name?':
                send_message("My name is HELLO BOT!", chat)

            elif text == 'How old are you?':
                send_message("I'm 23 years old", chat)

            elif text == 'Nice to meet you':
                send_message("Nice to meet you, too", chat)

            elif text == 'What date is today?':
                send_message(datetime.datetime.now().strftime('%Y-%m-%d'), chat)

            else:
                send_message(text, chat)
        except Exception as e:
            print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id):
    text = parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
