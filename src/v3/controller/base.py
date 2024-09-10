import datetime
from loguru import logger
from storage import Storage
from storage.user import UserStorage
from storage.message import MessageStorage
from service.auth import AuthService
from service.user import UserService
from service.message import MessageService

class Services(type):
    _storage = Storage()
    _userStorage = UserStorage(_storage)
    _messageStorage = MessageStorage(_storage)
    _userService = UserService(_userStorage)
    _authService = AuthService(_userStorage)
    _messageService = MessageService(_messageStorage)

    def user_service(self) -> UserService:
        return self._userService
    
    def auth_service(self) -> AuthService:
        return self._authService
    
    def message_service(self) -> MessageService:
        return self._messageService
    
    def auth(self, request: any) -> int:
        try:
            token = request.headers.get('Authorization')
            if token is None or len(token) == 0:
                return None          

            id = self._auth_service.check(token)

            if id is None:
                return None
            
            return id
        
        except Exception as e:
            logger.error(f'Error checking token: {e}')
            return None

class Response:
    @staticmethod
    def create_response(status: int, message: str, data: dict = None):        
        ret = {        
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        if data is not None:
            for key in data:
                ret[key] = data[key]

        logger.info(f'Response {status}: {ret}')                

        return ret, status
    
    @staticmethod
    def create_error_response(status: int, error: str):
        logger.error(f'Error {status}: {error}')
        return {
            "error": error,
            "timestamp": datetime.now().isoformat()
        }, status