from werkzeug.security import check_password_hash
import sqlite3
from models.user import User


class LoginController:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path

    def login_user(self, username, password):
        """Authenticate user by their username and password."""
        return User.check_password(username, password)

        if user and check_password_hash(user[2], password):
            return user[0]  # Return the user ID
        else:
            return None
