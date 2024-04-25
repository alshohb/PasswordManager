from utils.password_generator import generate_password
from utils.password_strength_checker import password_strength

def test_generate_password():
    print("Generated Passwords and their Strengths:")
    for _ in range(5):  # Generate 5 sample passwords
        password = generate_password(12)  # Generate a password with a length of 12 characters
        strength, message = password_strength(password)
        print(f"Password: {password} - Strength: {strength}, Message: {message}")

if __name__ == "__main__":
    test_generate_password()
