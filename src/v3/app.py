#! /bin/env python3
import logging
from os import environ
import json

from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS
from loguru import logger

from controller.auth import api as AuthApi
from controller.message import api as MessageApi
from controller.user import api as UserApi

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())

root = ""
app = Flask(__name__)
CORS(app) 
app.logger.addHandler(InterceptHandler())
blueprint = Blueprint('api', __name__)
app.register_blueprint(blueprint)
api = Api(app, title='Chat-Doenca V3', version='3.0', description='Chat-Doenca API', prefix='/v3')

api.add_namespace(UserApi, path='/user')
api.add_namespace(AuthApi, path='/auth')
api.add_namespace(MessageApi, path='/message')

    
@app.route('/')
def index():
    root = ""
    with open('index.html') as f:
        root = f.read()
    
    return root

if __name__ == '__main__':
    logger.info('Starting Chat Doenca API')    
    SERVER_HOST = environ.get('SERVER_HOST_CHAT_V3', 'localhost')

    #app.config["SERVER_NAME"] = "http://learnops.duckdns.org:7111/"
    app.config["SERVER_NAME"] = "localhost:8082"
    app.app_context().__enter__()
    with open('swagger.json', 'w') as f:
        f.write(json.dumps(api.__schema__, indent=2))

    app.run(host=SERVER_HOST, port=8082, threaded=True)
    logger.info('Exiting Chat Doenca API')
