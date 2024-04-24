import sqlite3
from werkzeug.security import generate_password_hash

class User:
    def __init__(self, username, password):
        self.id = None  
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)

    def create(self, db_path='users.db'):
        """Save user to the database."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        c.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                  (self.username, self.password_hash))
        conn.commit()
        conn.close()


class Password:
    def __init__(self, user_id, website, username, password):
        self.id = None 
        self.user_id = user_id
        self.website = website
        self.username = username
        self.password = password  

    def create(self, db_path='users.db'):
        """Save password to the database."""
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        c.execute('INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)',
                  (self.user_id, self.website, self.username, self.password))
        conn.commit()
        conn.close()
