from views.login_view import show_login_form, show_login_failure, show_login_success
from controllers.login_controller import LoginController
from models.user import User  # Import the User class

def main():
    # Initialize the database
    User.initialize_db()  # This line initializes the database tables

    # Initialize the login controller
    login_controller = LoginController()

    # Display login form and get user input
    username, password = show_login_form()

    # Attempt to log the user in
    user_id = login_controller.login_user(username, password)

    # Check if login was successful
    if user_id:
        show_login_success(user_id)
    else:
        show_login_failure()

if __name__ == "__main__":
    main()
