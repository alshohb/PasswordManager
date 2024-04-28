from utils.password_generator import generate_password
from utils.password_strength_checker import password_strength

def test_generate_password():
    """
    Test the password generation and strength checking functionality.
    Generates multiple passwords and checks their strength.
    """
    print("Generated Passwords and their Strengths:")
    for _ in range(5):  # Generate 5 sample passwords to test
        password = generate_password(12)
        strength, message = password_strength(password)  # Assess the strength of the generated password
        print(f"Password: {password} - Strength: {strength}, Message: {message}")  # Output the results

if __name__ == "__main__":
    test_generate_password()  # Execute the test function when the script is run directly
