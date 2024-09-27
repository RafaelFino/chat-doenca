from loguru import logger
from domain.user import User
from storage.user import UserStorage

class UserService:
    def __init__(self, storage: UserStorage):
        logger.debug('UserService created')
        self.storage = storage

    def get(self, id: int) -> User:
        try:
            return self.storage.get(id)
        except Exception as e:
            logger.error(f'Error getting user: {e}')
        
        return None
    
    def get_all(self) -> list[User]:
        try:
            return self.storage.get_all()
        except Exception as e:
            logger.error(f'Error getting all users: {e}')
        
        return []

    def create(self, name: str, password: str) -> int:
        try:
            logger.info(f'Creating user {name}')
            return self.storage.create(name, password)
        except Exception as e:
            logger.error(f'Error creating user: {e}')
        
        return None
    
    def put(self, requester: int, target: int, enable: bool) -> bool:
        try:            
            ret = self.storage.put(requester, target, enable)
            if ret:
                logger.info(f'User {target} updated by {requester} -> enable: {enable}')
                return True
        except Exception as e:
            logger.error(f'Error updating user: {e}')
        
        return False
