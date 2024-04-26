from getpass import getpass

def show_login_form():
    """
    Display the login form to the user and capture their input securely.
    
    Returns:
    - tuple: A tuple containing the entered username and password.
    """
    print("Please log in to continue:")
    username = input("Username: ")  # Get the username input
    password = getpass("Password: ")  # Securely get the password without echoing
    return username, password

def show_login_success(user_id):
    """
    Display a success message upon successful login.
    
    Parameters:
    - user_id (int): The ID of the user who logged in successfully.
    """
    print(f"Login successful. Welcome, user {user_id}!")

def show_login_failure():
    """
    Inform the user that the login attempt has failed.
    """
    print("Login failed. Please check your credentials and try again.")

if __name__ == "__main__":
    # Demonstrate usage
    username, password = show_login_form()
    # This line below is for demonstration and should not be used in production:
    print(f"You entered Username: {username} and Password: [HIDDEN]")
