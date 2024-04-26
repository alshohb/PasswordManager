from views.login_view import show_login_form, show_login_failure, show_login_success
from controllers.login_controller import LoginController
from models.user import User

def main():
    # Initialize the database tables if they do not exist.
    User.initialize_db()

    # Create an instance of the login controller.
    login_controller = LoginController()

    # Show the login form and capture username and password input from the user.
    username, password = show_login_form()

    # Authenticate the user and retrieve user ID if login is successful.
    user_id = login_controller.login_user(username, password)

    # If user_id is returned, login is successful; otherwise, fail the login.
    if user_id:
        show_login_success(user_id)
    else:
        show_login_failure()

if __name__ == "__main__":
    main()
