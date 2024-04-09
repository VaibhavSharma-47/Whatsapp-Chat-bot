from pprint import pprint

import requests

from time import sleep


def send_message(chat_id, text):
    """
    Send message to chat_id.
    :param chat_id: Phone number + "@c.us" suffix - 1231231231@c.us
    :param text: Message for the recipient
    """
    # Send a text back via WhatsApp HTTP API
    response = requests.post(
        "http://localhost:3000/api/sendText",
        json={
            "chatId": chat_id,
            "text": text,
            "session": "default",
        },
    )
    response.raise_for_status()


def reply(chat_id, message_id, text):
    response = requests.post(
        "http://localhost:3000/api/reply",
        json={
            "chatId": chat_id,
            "text": text,
            "reply_to": message_id,
            "session": "default",
        },
    )
    response.raise_for_status()


def send_seen(chat_id, message_id, participant):
    response = requests.post(
        "http://localhost:3000/api/sendSeen",
        json={
            "session": "default",
            "chatId": chat_id,
            "messageId": message_id,
            "participant": participant,
        },
    )
    response.raise_for_status()


def start_typing(chat_id):
    response = requests.post(
        "http://localhost:3000/api/startTyping",
        json={
            "session": "default",
            "chatId": chat_id,
        },
    )
    response.raise_for_status()


def stop_typing(chat_id):
    response = requests.post(
        "http://localhost:3000/api/stopTyping",
        json={
            "session": "default",
            "chatId": chat_id,
        },
    )
    response.raise_for_status()


def typing(chat_id, seconds):
    start_typing(chat_id=chat_id)
    sleep(seconds)
    stop_typing(chat_id=chat_id)


def get_messages(chat_id, number_of_messages_to_fetch):
    response = requests.get(
        f'''http://localhost:3000/api/messages?chatId={chat_id}&downloadMedia=true&limit={number_of_messages_to_fetch}&session=default''',
        json={
            "session": "default",
            "chatId": chat_id,
        },
    )
    #pprint("Response for chats \n"+ str(response.json()))
    messages = "";
    for message in response.json()[0:-1]:
        pprint("Messages "+ str(message))
        name = "Other Person";
        if message['fromMe'] :
            name = "Vaibhav"

        messages += f'''{name} - {message['body']} \n'''
    print(messages)
    return messages
