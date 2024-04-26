from werkzeug.security import check_password_hash
import sqlite3
from models.user import User

class LoginController:
    def __init__(self, db_path='users.db'):
        """
        Initialize the LoginController with a database path.
        :param db_path: str - Path to the SQLite database file
        """
        self.db_path = db_path

    def login_user(self, username, password):
        """
        Authenticate a user by their username and password.
        :param username: str - The username of the user trying to log in
        :param password: str - The password provided by the user for login
        :return: int or None - The user's ID if authentication is successful, None otherwise
        """
        # Use the User class's static login method to check credentials
        user_valid = User.login(username, password, self.db_path)
        
        if user_valid:
            # If user is authenticated, fetch the user's details
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cursor.fetchone()
                return user_id[0] if user_id else None
        else:
            return None
