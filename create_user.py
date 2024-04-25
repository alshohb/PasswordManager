from models.user import User

def create_user(username, password):
    new_user = User(username, password)
    new_user.create()

if __name__ == "__main__":
    create_user('shihab', '123')
