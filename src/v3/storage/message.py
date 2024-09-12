import sqlite3
from domain.message import Message
from domain.user import User

class MessageStorage:
    def __init__(self, storage):
        self.storage = storage
        c = self.storage.get_cursor()
        c.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, user_id INT, text TEXT, FOREIGN KEY(user_id) REFERENCES users(id))')        
        c.close()

    def create(self, message: Message) -> int:
        c = self.storage.get_cursor()
        c.execute('INSERT INTO messages (timestamp, user_id, text) VALUES (?, ?, ?)', (message.timestamp, message.user.id, message.text))
        self.storage.commit()
        c.close()
        return c.lastrowid
    
    def get(self, id: int) -> Message:
        c = self.db.cursor()
        c.execute("""
        SELECT 
            m.id, 
            m.timestamp, 
            m.user_id, 
            u.name, 
            m.text 
        FROM 
            messages m inner join users u 
                on m.user_id = u.id
        WHERE 
            m.id = ? 
        """
            , (id,))
        m = None

        for row in c.fetchall():
            m = Message(row[2], row[3])
            m.id = row[0]
            m.timestamp = row[1]

        c.close()
        return m

    def get_from_last(self, last: int):
        c = self.storage.get_cursor()
        c.execute("""
                SELECT 
                    m.id, 
                    m.timestamp, 
                    m.user_id, 
                    u.name, 
                    m.text 
                FROM 
                    messages m inner join users u 
                        on m.user_id = u.id
                WHERE 
                    m.id >= ? 
                order by m.id"""
                  , (last,))
        ret = []

        for row in c.fetchall():
            u = User(row[3], row[2])

            m = Message(u, row[4])
            m.id = row[0]
            m.timestamp = row[1]
            
            ret.append(m)

        c.close()
        return ret