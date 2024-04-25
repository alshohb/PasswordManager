import random
import string

def generate_password(length=12):
    """Generate a random password."""
    if length < 8:
        length = 8  # Ensure password is at least 8 characters long

    # Define the character set for the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    # Make sure to include at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(punctuation)
    ]

    # Fill the rest of the password length with a random choice of all characters
    random_chars = lowercase + uppercase + digits + punctuation
    password += [random.choice(random_chars) for _ in range(length - 4)]

    # Shuffle the resulting password list to avoid predictable patterns
    random.shuffle(password)

    return ''.join(password)
