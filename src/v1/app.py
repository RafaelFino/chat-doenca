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
    try:
        sender = request.form.get('sender')
        text = request.form.get('text')

        if sender is None or len(sender) == 0:
            logger.error("Sender is empty")
            return {
                "error": "Empty sender",
                "timestamp": datetime.datetime.now().isoformat()
            }, 400

        if text is None or len(text) == 0:
            logger.error("Text is empty")
            return {
                "error": "Empty text",
                "timestamp": datetime.datetime.now().isoformat()
            }, 400

        message = Message(len(messages), sender, text)
        messages.append(message)

        logger.info(f'Received message: {message.ToStr()}')

        return {
            "id": message.id,
            "timestamp": datetime.datetime.now().isoformat()
            }, 201
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        return {
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
            }, 500

@app.route('/message/<last>', methods=['GET'])
def get_messages(last: int = 0):
    try:
        ret = []
        if not last.isdigit():
            return {
                "error": "Invalid message index",
                "timestamp": datetime.datetime.now().isoformat()
            }, 400
        last = int(last)
        if last < 0:
            last = 0

        if last >= len(messages):
            return {
                "messages": ret,
                "timestamp": datetime.datetime.now().isoformat()
                }, 200

        for m in messages[last+1:]:
            ret.append(m.ToJson())

        logger.info(f"Returning {len(ret)} messages messages from {last}: {ret}")
        return {
            "messages": ret,
            "timestamp": datetime.datetime.now().isoformat()
            }, 200
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        return {
            "error": str(e),
            "timestamp": datetime.datetime.now().isoformat()
            }, 500

#if __name__ == '__main__':
def start_app():
    logger.info('Starting Chat Doenca API')
    from waitress import serve
    serve(app, host="192.168.1.9", port=8080)
    logger.info('Exiting Chat Doenca API')
