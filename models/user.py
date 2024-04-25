import sqlite3
from utils.encryption import encrypt, decrypt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create(self, db_path='users.db', key='my_secret_master_key'):
        """Save user to the database with encrypted password."""
        encrypted_password = encrypt(self.password, key)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password_hash, salt, nonce, tag)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            self.username,
            encrypted_password['ciphertext'],
            encrypted_password['salt'],
            encrypted_password['nonce'],
            encrypted_password['tag']
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def login(username, password_attempt, db_path='users.db', key='my_secret_master_key'):
        """Attempt to login a user."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT password_hash, salt, nonce, tag FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            password_hash, salt, nonce, tag = user_data
            enc_dict = {
                'ciphertext': password_hash,
                'salt': salt,
                'nonce': nonce,
                'tag': tag
            }
            decrypted_password = decrypt(enc_dict, key)
            return decrypted_password == password_attempt
        return False

    @staticmethod
    def initialize_db(db_path='users.db'):
        """Initialize the database and create tables if they don't exist."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT,
                nonce TEXT,
                tag TEXT
            )
        ''')
        conn.commit()
        conn.close()

class Password:
    def __init__(self, user_id, website, username, password):
        self.user_id = user_id
        self.website = website
        self.username = username
        self.password = password

    def create(self, db_path='users.db'):
        """Save password to the database."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        cursor.execute('INSERT INTO passwords (user_id, website, username, password) VALUES (?, ?, ?, ?)',
                       (self.user_id, self.website, self.username, self.password))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    User.initialize_db()
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users')
    conn.commit()
    conn.close()
    test_user = User('testuser', 'testpassword')
    test_user.create()
    print("User created successfully.")
    valid_login = User.login('testuser', 'testpassword')
    print("Login successful:", valid_login)
