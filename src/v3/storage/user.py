from domain.user import User
from loguru import logger
import hashlib

class UserStorage:
    def __init__(self, storage):
        self.storage = storage
        c = self.storage.get_cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, password TEXT NOT NULL, enable BOOLEAN DEFAULT 0);')
        c.execute("CREATE TABLE IF NOT EXISTS users_audit (timestamp DATE DEFAULT (datetime('now','localtime')), requester INTEGER, target INTEGER, status BOOLEAN);")
        c.close()        

    def get(self, id: int) -> User:
        c = self.storage.get_cursor()
        c.execute('SELECT id, name, enable FROM users WHERE id = ?;', (id,))
        u = None

        for row in c.fetchall():
            u = User(row[1], row[0], row[2])

        c.close()
        return u
    
    def get_all(self) -> list[User]:
        try:
            c = self.storage.get_cursor()
            c.execute('SELECT id, name, enable FROM users;')
            u = []

            for row in c.fetchall():
                u.append(User(row[1], row[0], row[2]))

            c.close()
            return u
        except Exception as e:
            logger.error(f'Error getting all users: {e}')
            return []
    
    def put(self, requester: int, target: int, enable: bool) -> bool:
        try:
            c = self.storage.get_cursor()
            c.execute('UPDATE users SET enable = ? WHERE id = ?;', (enable, target))
            self.storage.commit()
            c.close()

            self.put_audit(requester, target, enable)
        except Exception as e:
            logger.error(f'Error updating user: {e}')
            return False
        
        return True
    
    def create(self, name: str, password: str) -> int:        
        try:
            hidden = hashlib.sha256(password.encode()).hexdigest()
            c = self.storage.get_cursor()
            c.execute('INSERT INTO users (name, password) VALUES (?, ?);', (name, hidden))
            self.storage.commit()
            c.close()
        except Exception as e:
            logger.error(f'Error creating user: {e}')
            return None
       
        return c.lastrowid
    
    def put_audit(self, requester: int, target: int, status: bool) -> bool:
        try:
            c = self.storage.get_cursor()
            c.execute('INSERT INTO users_audit (requester, target, status) VALUES (?, ?, ?);', (requester, target, status))
            self.storage.commit()
            c.close()
        except Exception as e:
            logger.error(f'Error auditing user: {e}')
            return False
        
        return True    

    def auth(self, id: int, password: str) -> bool:
        try:
            hidden = hashlib.sha256(password.encode()).hexdigest()
            c = self.storage.get_cursor()
            c.execute('SELECT id FROM users WHERE id = ? AND password = ? AND enable = 1;', (id, hidden))
            r = c.fetchone()            
            
            return r is not None
        except Exception as e:
            logger.error(f'Error authenticating user: {e}')
            return False
        
