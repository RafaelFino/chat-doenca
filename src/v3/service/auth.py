import uuid
from loguru import logger
from storage import UserStorage

class AuthService:    
    def __init__(self, storage: UserStorage):
        self.storage = storage
        self.tokens = {}

    @classmethod
    def login(self, id: int, password: str) -> str:
        try:       
            u = self.storage.get(id)
            if u is None:
                return None
            
            if not self.storage.auth(id, password):
                return None
            
            token = str(uuid.uuid4())
            self.tokens[token] = id
            logger.info(f'User {id} logged in')
            return token
        except Exception as e:
            logger.error(f'Error logging in: {e}')
            return None
    
    @classmethod
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
    
    @classmethod
    def check(self, token: str) -> int:
        try:
            if token in self.tokens:
                id = self.tokens[token]
                logger.info(f'User token for {id} checked')
                return id

            logger.info(f'Invalid token: {token}')
            return None       

        except Exception as e:
            logger.error(f'Error checking token: {e}')
        
