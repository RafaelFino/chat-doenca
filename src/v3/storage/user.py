from domain.user import User
import hashlib

class UserStorage:
    def __init__(self, storage):
        self.storage = storage
        c = self.storage.get_cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
        c.commit()
        c.close()

    def get(self, id: int) -> User:
        c = self.storage.get_cursor()
        c.execute('SELECT id, username FROM users WHERE id = ?', (id,))
        u = None

        for row in c.fetchall():
            u = User(row[1], row[0])

        c.close()
        return u
    
    def create(self, name: str, password: str) -> int:
        c = self.storage.get_cursor()
        hidden = hashlib.sha256(password.encode()).hexdigest()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (name, password))
        c.commit()
        c.close()
        return c.lastrowid

    def auth(self, id: int, password: str) -> bool:
        c = self.storage.get_cursor()
        hidden = hashlib.sha256(password.encode()).hexdigest()
        c.execute('SELECT id FROM users WHERE id = ? AND password = ?', (id, hidden))
        r = c.fetchone()
        c.close()
        return r is not None
        
