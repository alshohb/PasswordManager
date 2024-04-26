from models.user import User

def create_user(username, password):
    """
    Create a new user with the given username and password.
    
    Parameters:
    - username (str): The username of the new user.
    - password (str): The password for the new user.
    
    Returns:
    - None
    """
    try:
        new_user = User(username, password)
        new_user.create()
        print("User created successfully.")
    except Exception as e:
        print(f"Failed to create user: {e}")

if __name__ == "__main__":
    # Example usage; adapt or remove for production deployment
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    create_user(username, password)
