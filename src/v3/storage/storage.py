import sqlite3
    
class Storage:
    def __init__(self):
        self.db = sqlite3.connect('chat.db', check_same_thread=False)        

    def get_cursor(self):
        return self.db.cursor()
    
    def commit(self):
        self.db.commit()
