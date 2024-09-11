import datetime
from domain.user import User

class Message:
    def __init__(self, user: User, text: str):
        self.id = 0
        self.timestamp = datetime.datetime.now().isoformat()
        self.user = User(user.name, user.id)
        self.text = text

    def set_id(self, id: int):
        self.id = id

    def get_id(self) -> int:
        return self.id

    def ToStr(self):
        return f'[{self.id:06}] {self.timestamp} {self.user.name} -> {self.text}'

    def ToJson(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'user_id': self.user.id,
            'user_name': self.user.name,
            'text': self.text            
        }
    
