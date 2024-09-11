import uuid
import datetime
import json
from loguru import logger
from storage.user import UserStorage
from domain.token import LoginStatus, Token
from domain.user import User

class AuthService:    
    def __init__(self, storage: UserStorage):
        logger.debug('AuthService created')
        self.storage = storage
        self.tokens = {}

    def login(self, id: int, password: str) -> str:
        try:
            u = self.storage.get(id)
            
            if u is None:
                return None
            
            if not self.storage.auth(id, password):
                return None
            
            token = str(uuid.uuid4()).replace('-', '').upper()
            self.tokens[token] = Token(token, u)

            logger.info(f'User id:{id} logged in')
            
            return token
        except Exception as e:
            logger.error(f'Error logging in: {e}')
            return None
    
    def logout(self, id: int) -> bool:
        try:
            for token in self.tokens:
                if self.tokens[token] == id:        
                    del self.tokens[token]
                    logger.info(f'User {id} logged out')
                    return True
        
        except Exception as e:
            logger.error(f'Error logging out: {e}')
            
        return False
    
    def check(self, token: str) -> Token:
        try:
            if token in self.tokens:
                ret = self.tokens[token]
                logger.debug(f'User token for id:{ret.ToJson()} found!')

                if ret.is_expired():
                    logger.info(f'User token for id:{ret.ToJson()} expired! Discarding...')
                    del self.tokens[token]
                    return ret
                
                ret.set_status(LoginStatus.ACCEPTED)
                ret.add()
                self.tokens[token] = ret
                
                return ret

            logger.info(f'Invalid token: {token}')
            ret = Token(token, User('', -1))
            ret.set_status(LoginStatus.REJECTED)
            return ret

        except Exception as e:
            logger.error(f'Error checking token: {e}')
        
