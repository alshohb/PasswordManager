import random
import string

def generate_password(length=12):
    """
    Generate a random password.
    
    Parameters:
    - length (int): Desired length of the password. Default is 12 characters.
    
    Returns:
    - str: A randomly generated password.
    
    Ensures the password contains at least one lowercase letter, one uppercase letter,
    one digit, and one special character. The rest of the password is filled with a
    random mix of these character types. The password is then shuffled to ensure randomness.
    """

    # Minimum length check to ensure complexity
    if length < 8:
        length = 8  # Set a sensible minimum to encourage stronger passwords

    # Character sets from which the password will be constructed
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    # Construct the initial password ensuring at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(punctuation)
    ]

    # Fill the remaining part of the password with a random selection of characters
    random_chars = lowercase + uppercase + digits + punctuation
    password += [random.choice(random_chars) for _ in range(length - 4)]

    # Shuffle the list to prevent any predictable patterns
    random.shuffle(password)

    # Join the list into a string to form the final password
    return ''.join(password)

# Example usage to demonstrate the function
if __name__ == "__main__":
    print("Generated Password:", generate_password(12))  # Generates and prints a 12-character password
