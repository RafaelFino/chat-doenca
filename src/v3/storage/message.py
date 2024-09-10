import sqlite3
from domain.message import Message

class MessageStorage:
    def __init__(self, storage):
        self.storage = storage
        c = self.storage.get_cursor()
        c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, sender INT, text TEXT, FOREIGN KEY(sender) REFERENCES users(id))')        
        c.commit()
        c.close()

    def create(self, message: Message) -> int:
        c = self.storage.get_cursor()
        c.execute('INSERT INTO messages (timestamp, sender, text) VALUES (?, ?, ?)', (message.timestamp, message.senderId, message.text))
        c.commit()
        c.close()
        return c.lastrowid
    
    def get(self, id: int) -> Message:
        c = self.db.cursor()
        c.execute('SELECT id, timestamp, sender, text FROM messages WHERE id = ?', (id,))
        m = None

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]

        c.close()
        return m

    def get_from_last(self, last: int) -> list[Message]:
        c = self.storage.get_cursor()
        c.execute('SELECT id, timestamp, sender, text FROM messages WHERE id >= ? order by id', (last,))
        ret = []

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]
            ret.append(m)

        c.close()
        return ret
    
    def get_from_user(self, user: int) -> list[Message]:
        c = self.storage.get_cursor()
        c.execute("""SELECT id, timestamp, sender, text FROM messages WHERE sender = ? order by id""", (user,))
        ret = []

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]
            ret.append(m)

        c.close()
        return ret    