class User:
    def __init__(self, name: str, id: int):
        self.id = id
        self.name = name

    def ToStr(self):
        return f'[{self.id:06}] {self.name}'

    def ToJson(self):
        return {
            'id': self.id,
            'name': self.name
        }