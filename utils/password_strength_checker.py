import math
import string

def password_strength(password):
    """
    Evaluate the strength of a given password based on information entropy and
    provide user-friendly advice for improving password strength.
    
    Parameters:
    - password (str): The password string to be evaluated.
    
    Returns:
    - tuple: A tuple containing two elements:
      1. A string indicating the strength of the password ('Weak', 'Medium', 'Strong', 'Very Strong').
      2. A message string with user-friendly advice on how to improve the password.
    """
    
    if len(password) == 0:
        return 'Weak', 'Password cannot be empty.'

    character_pool = len(set(password))
    entropy = len(password) * math.log2(character_pool)

    strength = ''
    messages = []

    if entropy < 28:
        strength = 'Weak'
        messages.append('Your password is too short and easy to guess.')
    elif entropy < 35:
        strength = 'Medium'
        messages.append('Your password could be improved.')
    elif entropy < 60:
        strength = 'Strong'
        messages.append('Your password is fairly strong.')
    else:
        strength = 'Very Strong'
        messages.append('Your password is very strong.')

    if len(password) < 8:
        messages.append('Use at least 8 characters.')
    if not any(char.isupper() for char in password):
        messages.append('Use at least one uppercase letter.')
    if not any(char.islower() for char in password):
        messages.append('Use at least one lowercase letter.')
    if not any(char.isdigit() for char in password):
        messages.append('Use at least one number.')
    if not any(char in string.punctuation for char in password):
        messages.append('Use at least one special character like !@#$%^&*().')

    return strength, ' '.join(messages)

# Example usage
if __name__ == "__main__":
    test_passwords = ['12345678', 'ComplexPass123!', 'simple', '']
    for pwd in test_passwords:
        strength, message = password_strength(pwd)
        print(f"Password: {pwd} - Strength: {strength}, Message: {message}")
