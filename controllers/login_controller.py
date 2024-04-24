from werkzeug.security import check_password_hash
import sqlite3

class LoginController:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path

    def login_user(self, username, password):
        """Authenticate user by their username and password."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            return user[0]  # Return the user ID
        else:
            return None
