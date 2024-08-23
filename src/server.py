#! /bin/env python3

from flask import Flask, request
from loguru import logger
import logging
import datetime
import json

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

app = Flask(__name__)
app.logger.addHandler(InterceptHandler())

class Message:
    def __init__(self, id: int, sender: str, text: str):
        self.id = id
        self.when = datetime.datetime.now().isoformat()
        self.sender = sender
        self.text = text

    def ToStr(self):
        return f'[{self.id:06}] {self.when} {self.sender} -> {self.text}'
    
    def ToJson(self):
        return {
            'id': self.id,
            'when': self.when,
            'sender': self.sender,
            'text': self.text
        }

messages = []

@app.route('/')
def index():
    return 'Chat Doenca API'

@app.route('/message', methods=['POST'])
def post_message():    
    sender = request.form.get('sender')
    text = request.form.get('text')
    message = Message(len(messages), sender, text)
    messages.append(message)

    logger.info('Received message: {message.ToStr()}')

    return { "message-id": message.id } 

@app.route('/message/<last>', methods=['GET'])
def get_messages(last = 0):
    ret = []
    for m in messages:
        logger.info(m.ToStr())
        ret.append(m.ToJson())
    
    logger.info('Returning messages from {last}: {len(ret)}')
    return { "messages": ret }

if __name__ == '__main__':
    logger.info('Starting Chat Doenca API')
    app.run(port=8080, debug=True)
    logger.info('Exiting Chat Doenca API')