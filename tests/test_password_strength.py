from utils.password_strength_checker import password_strength

def test_passwords():
    passwords = [
        "short",
        "longenoughbutnouppercase1!",
        "ValidPassword123!",
    ]
    for password in passwords:
        strength, message = password_strength(password)
        print(f"Password: {password} - Strength: {strength}, Message: {message}")

if __name__ == "__main__":
    test_passwords()
