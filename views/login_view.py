from getpass import getpass

def show_login_form():
    """Display the login form to the user and get their input."""
    print("Please log in to continue:")
    username = input("Username: ")
    password = getpass("Password: ") 
    return username, password

def show_login_success(user_id):
    """Display a success message upon login."""
    print(f"Login successful. Welcome, user {user_id}!")

def show_login_failure():
    """Inform the user that the login has failed."""
    print("Login failed. Please check your credentials and try again.")

if __name__ == "__main__":
    username, password = show_login_form()
    print(f"You entered Username: {username} and Password: {password}")
