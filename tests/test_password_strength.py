from utils.password_strength_checker import password_strength

def test_passwords():
    """
    Tests various passwords for strength and provides feedback.
    This function will loop through a predefined list of passwords,
    checking each for strength and outputting the results.
    """
    # Define a list of sample passwords to test
    passwords = [
        "short",  # Expected to fail due to length
        "longenoughbutnouppercase1!",  # Expected to fail due to lack of uppercase letters
        "ValidPassword123!",  # Should pass as strong
    ]

    # Iterate through each password and check its strength
    for password in passwords:
        strength, message = password_strength(password)  # Check the strength of each password
        print(f"Password: {password} - Strength: {strength}, Message: {message}")  # Output the strength and feedback message

if __name__ == "__main__":
    test_passwords()  # Run the test function if the script is executed directly
