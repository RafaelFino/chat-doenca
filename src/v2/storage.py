import sqlite3
from message import Message
    
class Storage:
    def __init__(self):
        self.db = sqlite3.connect('chat.db', check_same_thread=False)
        c = self.db.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, sender TEXT, text TEXT)')
        self.db.commit()

    def add_message(self, message: Message) -> int:
        c = self.db.cursor()
        c.execute('INSERT INTO messages (timestamp, sender, text) VALUES (?, ?, ?)', (message.timestamp, message.sender, message.text))
        self.db.commit()
        c.close()
        return c.lastrowid
    
    def get_message(self, id: int):
        c = self.db.cursor()
        c.execute('SELECT id, timestamp, sender, text FROM messages WHERE id = ?', (id,))
        m = None

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]

        c.close()
        return m

    def get_messages(self, last: int):
        c = self.db.cursor()
        c.execute('SELECT id, timestamp, sender, text FROM messages WHERE id >= ? order by id', (last,))
        ret = []

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]
            ret.append(m)

        c.close()
        return ret