from pprint import pprint

import ollama


def respond(messages, text):
    if messages == None:
        messages = []
    messages.append({
        'role': 'user',
        'content': text,
    })
    response = ollama.chat(model='command-r', messages=messages)
    messages.append(response['message'])
    pprint(messages)
    pprint(messages[-1])
    return messages


def startup(chat):
    messages=[
        {
            'role': 'user',
            'content': f'''Here is a conservation between two people I want you to pretend like you are Vaibhav. Do not break character. You can make assumptions to any personal questions. \n{chat} ''',
        }
    ]

    return messages
