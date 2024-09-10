import datetime
from domain.user import User

class Message:
    def __init__(self, user: User, text: str):
        self.timestamp = datetime.datetime.now().isoformat()
        self.user = user
        self.text = text

    def set_id(self, id: int):
        self.id = id

    def get_id(self):
        return self.id

    def ToStr(self):
        return f'[{self.id:06}] {self.timestamp} {self.user.Name} -> {self.text}'

    def ToJson(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'user': self.sender.ToJson(),
            'text': self.text
        }
    
