class User:
    def __init__(self, name: str, id: int, enabled: bool = True):
        self.id = id
        self.name = name
        self.enabled = enabled

    def ToStr(self):
        return f'[{self.id:06}] {self.name}'

    def ToJson(self):
        return {
            'id': self.id,
            'name': self.name,
            'enabled': self.enabled
        }
