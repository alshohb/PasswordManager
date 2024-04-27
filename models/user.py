import sqlite3
from utils.encryption import encrypt, decrypt

class User:
    def __init__(self, username, password):
        # User initialization with provided username and password
        self.username = username
        self.password = password

    def create(self, db_path='aljahwariDB.db', key='my_secret_master_key'):
        # Encrypt user's password and store user in the database
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
    def login(username, password_attempt, db_path='aljahwariDB.db', key='my_secret_master_key'):
        # Check if the provided password attempt matches the stored password
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT password_hash, salt, nonce, tag FROM users WHERE username = ?
            ''', (username,))
            user_data = cursor.fetchone()

        if user_data:
            # If user is found, verify the password
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
    def initialize_db(db_path='aljahwariDB.db', key='my_secret_master_key'):
        # Initialize the database and create the 'users' and 'passwords' tables if not exist
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    website TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    nonce TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            # Insert master user if it doesn't exist
            cursor.execute("SELECT id FROM users WHERE username = 'masteruser'")
            if cursor.fetchone() is None:
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
            print("Database and tables initialized, master user checked/created.")
        
    def save_password(self, website, username, password, db_path='aljahwariDB.db', key='my_secret_master_key'):
        """Save a password entry for the user."""
        encrypted_password = encrypt(password, key)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            print(f"Saving password for {self.username} for site {website}")
            
            # Ensure the user exists and get their user ID
            cursor.execute('SELECT id FROM users WHERE username = ?', (self.username,))
            user_id_result = cursor.fetchone()
            if user_id_result:
                user_id = user_id_result[0]
                print(f"User ID for {self.username}: {user_id}")

                # Insert the password entry
                cursor.execute('''
                    INSERT INTO passwords (user_id, website, username, password, salt, nonce, tag)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    website,
                    username,  # This should be the username for the site, not the user's login username
                    encrypted_password['ciphertext'],
                    encrypted_password['salt'],
                    encrypted_password['nonce'],
                    encrypted_password['tag']
                ))
                conn.commit()
                print("Password saved successfully.")
            else:
                print("User not found, cannot save password.")



    @staticmethod
    def get_user_entries(username, db_path='aljahwariDB.db', key='my_secret_master_key'):
        """Retrieve and decrypt user's password entries from the database."""
        decrypted_entries = []
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            print(f"Fetching entries for {username}")
            cursor.execute('''
                SELECT p.website, p.username, p.password, p.salt, p.nonce, p.tag
                FROM passwords AS p
                JOIN users AS u ON p.user_id = u.id
                WHERE u.username = ?
            ''', (username,))
            entries = cursor.fetchall()
            print(f"Found {len(entries)} entries for {username}")

            for entry in entries:
                website, username, encrypted_password, salt, nonce, tag = entry
                enc_dict = {
                    'ciphertext': encrypted_password,
                    'salt': salt,
                    'nonce': nonce,
                    'tag': tag
                }
                decrypted_password = decrypt(enc_dict, key)
                decrypted_entries.append({
                    'website': website,
                    'username': username,
                    'decrypted_password': decrypted_password
                })

        return decrypted_entries


    @staticmethod
    def get_all_entries(db_path='aljahwariDB.db'):
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

if __name__ == "__main__":
    User.initialize_db()

    # Before creating a new test user, check if the username already exists
    test_username = 'testuser'
    test_password = 'testpassword'
    test_site_username = 'site_username_for_testuser'  # Site-specific username

    # Create a test user if not exists
    test_user = User(test_username, test_password)
    with sqlite3.connect('aljahwariDB.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (test_username,))
        if cursor.fetchone() is None:
            test_user.create()
            print("Test user created successfully.")
        else:
            print("Test user already exists.")

    # Save a password for the test user
    test_user.save_password('example.com', test_site_username, test_password)
    print("Password for test user saved successfully.")
