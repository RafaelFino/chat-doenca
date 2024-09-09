import datetime

class Message:
    def __init__(self, sender: str, text: str):
        self.id = id
        self.timestamp = datetime.datetime.now().isoformat()
        self.sender = sender
        self.text = text

    def ToStr(self):
        return f'[{self.id:06}] {self.timestamp} {self.sender} -> {self.text}'

    def ToJson(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'text': self.text
        }