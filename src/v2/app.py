#! /bin/env python3

from flask import Flask, request, make_response
from flask_cors import CORS
from loguru import logger
from waitress import serve
from storage import Storage
from message import Message
import sqlite3
import logging
import datetime
import json

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

root = ""
app = Flask(__name__)
CORS(app) 
app.logger.addHandler(InterceptHandler())
    
storage = Storage()

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
}

@app.route('/')
def index():
    root = ""
    with open('index.html') as f:
        root = f.read()
    
    return root

def resp(body: dict, status_code):
    body['timestamp'] = datetime.datetime.now().isoformat()
    ret = make_response(json.dumps(body))
    ret.headers = headers
    ret.status_code = status_code
    return ret

@app.route('/message', methods=['POST'])
def post_message():
    try:
        sender = request.form.get('sender')
        text = request.form.get('text')

        if sender is None or len(sender) == 0:
            logger.error("Sender is empty")
            return resp({
                "error": "Empty sender",
            }, 400)
            

        if text is None or len(text) == 0:
            logger.error("Text is empty")
            return resp({
                "error": "Empty text"                
            }, 400)

        message = Message(sender, text)
        message.id = storage.add_message(message)
        
        logger.info(f'Received message: {message.ToStr()}')

        return resp({
            "id": message.id
            }, 201)
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        return resp({
            "error": str(e)
            }, 500)

@app.route('/message/<id>', methods=['GET'])
def get_message(id: int):
    try:
        if not id.isdigit():
            return resp({
                "error": "Invalid message index"
            }, 400)
        
        id = int(id)
        if id < 0:
            id = 0
        
        m = storage.get_message(id)

        if m is None:
            logger.error(f"Message {id} not found")
            return resp({
                "error": "Message not found"
            }, 404)

        logger.info(f"Returning {m.ToJson()}")
        return resp({
            "messages": m.ToJson()
            }, 200)
    
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        return resp({
            "error": str(e)
            }, 500)    

@app.route('/message', methods=['GET'])
def get_messages():
    try:
        ret = []        
        sender = request.args.get('sender')                
        last = request.args.get('last')        
        logger.info(f"Sender: {sender} // Last: {last}")

        if sender is not None:                      
            for m in storage.get_messages_from(sender):
                ret.append(m.ToJson())

            if len(ret) == 0:
                return resp({
                    "error": "No messages found"
                }, 404)

            logger.info(f"Returning {len(ret)} messages from {sender}: {ret}")
            return resp({
                "messages": ret
                }, 200)
        
        if last is not None:            
            logger.info(f"Last: {last}")
            if not last.isdigit():
                return resp({
                    "error": "Invalid message index"
                }, 400)
            
            last = int(last)
            if last < 0:
                last = 0

            for m in storage.get_messages(last):
                ret.append(m.ToJson())

            logger.info(f"Returning {len(ret)} messages messages from id {last}: {ret}")
            return resp({
                "messages": ret
                }, 200)
        
        logger.error("No parameters found")
        return resp({
            "error": "No parameters found"
            }, 400)
    
    except Exception as e:
        logger.error(f'Error processing message: {e}')
        return resp({
            "error": str(e)
            }, 500)

def start_app():
    logger.info('Starting Chat Doenca API')    
    serve(app, host='0.0.0.0', port=8081)
    logger.info('Exiting Chat Doenca API')
