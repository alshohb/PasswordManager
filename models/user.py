import sqlite3
from utils.encryption import encrypt, decrypt

class User:
    def __init__(self, username, password):
        """
        Initialize the User object with username and password.
        :param username: str - the user's username
        :param password: str - the user's plain text password
        """
        self.username = username
        self.password = password

    def create(self, db_path='users.db', key='my_secret_master_key'):
        """
        Create a user in the database with encrypted credentials.
        :param db_path: str - the database file path
        :param key: str - encryption key for securing the password
        """
        encrypted_password = encrypt(self.password, key)
        with sqlite3.connect(db_path) as conn:
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

    @staticmethod
    def login(username, password_attempt, db_path='users.db', key='my_secret_master_key'):
        """
        Attempt to log in a user by verifying their password.
        :param username: str - the username of the user trying to log in
        :param password_attempt: str - the attempted password to verify
        :param db_path: str - the database file path
        :param key: str - the encryption key used to decrypt the stored password
        :return: bool - True if login is successful, False otherwise
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT password_hash, salt, nonce, tag FROM users WHERE username = ?
            ''', (username,))
            user_data = cursor.fetchone()

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
    def initialize_db(db_path='users.db', key='my_secret_master_key'):
        """
        Initialize the database with necessary tables and a master user if not already present.
        :param db_path: str - the database file path
        :param key: str - the encryption key for creating the master user
        """
        with sqlite3.connect(db_path) as conn:
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
            # Adding the master user if not exists
            cursor.execute("SELECT username FROM users WHERE username = 'masteruser'")
            if not cursor.fetchone():
                encrypted_password = encrypt('masterpass', key)
                cursor.execute('''
                    INSERT INTO users (username, password_hash, salt, nonce, tag)
                    VALUES ('masteruser', ?, ?, ?, ?)
                ''', (
                    encrypted_password['ciphertext'],
                    encrypted_password['salt'],
                    encrypted_password['nonce'],
                    encrypted_password['tag']
                ))
            conn.commit()

    @staticmethod
    def get_user_entries(username, db_path='users.db'):
        """
        Retrieve all entries related to a specific user from the database.
        :param username: str - the username whose entries to retrieve
        :param db_path: str - the database file path
        :return: list - a list of tuples containing website, username, and password
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT website, username, password FROM passwords
                WHERE user_id = (SELECT id FROM users WHERE username = ?)
            ''', (username,))
            return cursor.fetchall()

    @staticmethod
    def get_all_entries(db_path='users.db'):
        """
        Retrieve all entries for the master user, showing encrypted passwords.
        :param db_path: str - the database file path
        :return: list - a list of tuples containing user's username, website, username on website, and encrypted password
        """
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT users.username, passwords.website, passwords.username, passwords.password
                FROM passwords
                JOIN users ON users.id = passwords.user_id
            ''')
            return cursor.fetchall()


class Password:
    def __init__(self, user_id, website, username, password):
        self.user_id = user_id
        self.website = website
        self.username = username
        self.password = password

    def create(self, db_path='users.db'):
        """Save password to the database."""
        with sqlite3.connect(db_path) as conn:
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

if __name__ == "__main__":
    User.initialize_db()
    print("Database initialized.")
    test_user = User('testuser', 'testpassword')
    test_user.create()
    print("Test user created successfully.")
    valid_login = User.login('testuser', 'testpassword')
    print("Login successful:", valid_login)