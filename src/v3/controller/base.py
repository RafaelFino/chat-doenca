from flask import make_response
from loguru import logger
from service.auth import AuthService
from service.message import MessageService
from service.user import UserService
from storage.storage import Storage
from storage.message import MessageStorage
from storage.user import UserStorage
from domain.token import Token
import datetime
import json

class Services():
    _storage = Storage()
    _user_storage = UserStorage(_storage)
    _message_storage = MessageStorage(_storage)
    _user_service = UserService(_user_storage)
    _auth_service = AuthService(_user_storage)
    _message_service = MessageService(_message_storage)

    def user_service(self) -> UserService:
        return self._user_service
    
    def auth_service(self) -> AuthService:
        return self._auth_service
    
    def message_service(self) -> MessageService:
        return self._message_service
    
    def auth(self, request: any) -> Token:
        try:
            token = request.headers.get('Authorization')
            if token is None or len(token) == 0:
                return None            

            result = self._auth_service.check(token)

            if result is None:
                logger.error('Token not found')
                return None            
            
            return result
        
        except Exception as e:
            logger.error(f'Error checking token: {e}')
            return None

services = Services()

headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
}

class Response:
    @staticmethod
    def create_response(status: int, message: str, body: dict = None):        
        if body is None:
            body = {}

        body['timestamp'] = datetime.datetime.now().isoformat()
        body['message'] = message
        ret = make_response(json.dumps(body))
        ret.headers = headers
        ret.status_code = status                

        logger.info(f'Response {status}: {json.dumps(body)}')                

        return ret
    
    @staticmethod
    def create_error_response(status: int, error: str, message : str = None):
        body = {}
        body['timestamp'] = datetime.datetime.now().isoformat()
        body['error'] = error
        if message is not None:
            body['message'] = message
        ret = make_response(json.dumps(body))
        ret.headers = headers
        ret.status_code = status 

        logger.error(f'Error response {status}: {json.dumps(body)}')  

        return ret