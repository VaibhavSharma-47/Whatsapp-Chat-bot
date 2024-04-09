import random
import re
from pprint import pprint

import requests
import AIBot
from flask import Flask
from flask import request

from Chat import send_seen, typing, send_message, get_messages

app = Flask(__name__)
messageMap = {}


@app.route("/")
def whatsapp_echo():
    return "WhatsApp Echo Bot is ready!"


@app.route("/bot", methods=["GET", "POST"])
def whatsapp_webhook():
    if request.method == "GET":
        return "WhatsApp Echo Bot is ready!"
    data = request.get_json()
    print("Event " + data["event"])
    if not (data["event"] == "message" or data["event"] == "message.any"):
        # We can't process other event yet
        print("Unknown event ")
        return f"Unknown event {data['event']}"

    # Payload that we've got
    payload = data["payload"]

    # The text
    text = payload.get("body")

    if not text:
        # We can't process non-text messages yet
        print("No text in message")
        print(payload)
        return "OK"
    # Number in format 1231231231@c.us or @g.us for group
    chat_id = payload["from"]
    if text == "stop":
        messageMap[chat_id] = "Stop"
    if not is_person(chat_id):
        print(f'''Message on group {chat_id} no responding''')
        return "OK"
    # Message ID - false_11111111111@c.us_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    message_id = payload['id']
    messages = messageMap.get(chat_id, None)
    if messages == "Stop":
        print(f"Stopping for {chat_id}")
        return "OK"
    if data["event"] != "message":
        return "OK"
    if messages is None:
        # TODO : Introduce a config file
        chat = get_messages(chat_id, 100)
        messages = AIBot.startup(chat)
        messageMap[chat_id] = messages
    # For groups - who sent the message
    participant = payload.get('participant')
    # IMPORTANT - Always send seen before sending new message
    send_seen(chat_id=chat_id, message_id=message_id, participant=participant)

    # Send a text back via WhatsApp HTTP API
    typing(chat_id=chat_id, seconds=random.random() * 3)
    messageMap[message_id] = AIBot.respond(messages, text)
    send_message(chat_id=chat_id, text=messages[-1]['content'])

    # OR reply on the message
    # typing(chat_id=chat_id, seconds=random.random() * 3)
    # reply(chat_id=chat_id, message_id=message_id, text=text)

    # Send OK back
    return "OK"


def is_person(s):
    # TODO Hacky to allow me to talk to a group
    if s == "120363267483752304@g.us":
        return True
    # Define a regular expression pattern to match exactly 12 digits before '@'
    pattern = r'^\d{12}@'

    # Use re.match() to check if the string matches the pattern
    if re.match(pattern, s):
        return True
    else:
        return False


if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
