from loguru import logger
from domain.message import Message
from storage.message import MessageStorage

class MessageService:
    def __init__(self, storage: MessageStorage):
        logger.debug('MessageService created')
        self.storage = storage

    def send(self, message: Message) -> int:        
        logger.debug(f'Sending message {message.ToStr()}')
        ret = None
        try:
            ret = self.storage.create(message)
        
        except Exception as e:
            logger.error(f'Error sending message: {e}')

        return ret

    def get(self, id: int = 0) -> Message:        
        logger.debug(f'Getting message {id}')
        ret = None
        try:
            ret = self.storage.get(id)
            logger.info(f'Message loaded: {ret.ToStr()}')
        
        except Exception as e:
            logger.error(f'Error getting message: {e}')
        
        return ret

    def get_from_last(self, last : int = 0) -> list[Message]:
        logger.debug(f'Getting messages from id:{last}')
        ret = []
        try:
            ret = self.storage.get_from_last(last)        
        except Exception as e:
            logger.error(f'Error getting messages: {e}')

        return ret
