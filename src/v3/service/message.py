from loguru import logger
from domain.message import Message
from storage.message import MessageStorage

class MessageService:
    def __init__(self, storage: MessageStorage):
        self.storage = storage

    @classmethod
    def send(self, message: Message) -> int:        
        logger.debug(f'Sending message {message.ToStr()}')
        ret = None
        try:
            ret = self.storage.create(message)
            logger.info(f'Message sent with id {ret}')
        
        except Exception as e:
            logger.error(f'Error sending message: {e}')

        return ret

    @classmethod    
    def get(self, id: int = 0) -> Message:        
        logger.debug(f'Getting message {id}')
        ret = None
        try:
            ret = self.storage.get(id)
            logger.info(f'Message loaded: {ret.ToStr()}')
        
        except Exception as e:
            logger.error(f'Error getting message: {e}')
        
        return ret

    @classmethod
    def get_from_last(self, last : int = 0) -> list[Message]:
        logger.debug(f'Getting messages from {last} id')
        ret = []
        try:
            ret = self.storage.get_from_last(last)
            logger.info(f'Messages loaded: {ret}')
        
        except Exception as e:
            logger.error(f'Error getting messages: {e}')

        return ret
