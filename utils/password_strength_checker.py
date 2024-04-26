import re

def password_strength(password):
    """
    Evaluate the strength of a given password based on multiple criteria.

    Parameters:
    - password (str): The password string to be evaluated.

    Returns:
    - tuple: A tuple containing two elements:
      1. A string indicating the strength of the password ('Weak' or 'Strong').
      2. A message string explaining why the password was judged as such.

    Criteria for strength evaluation:
    - At least 8 characters long.
    - Contains at least one numeral.
    - Contains at least one uppercase letter.
    - Contains at least one lowercase letter.
    - Contains at least one special character from the set [!@#$%^&*(),.?":{}|<>].
    """

    # Check the length of the password
    if len(password) < 8:
        return 'Weak', 'Password must be at least 8 characters long.'

    # Check for the presence of numerals
    if not re.search(r'[0-9]', password):
        return 'Weak', 'Password must include at least one numeral.'

    # Check for the presence of uppercase letters
    if not re.search(r'[A-Z]', password):
        return 'Weak', 'Password must include at least one uppercase letter.'

    # Check for the presence of lowercase letters
    if not re.search(r'[a-z]', password):
        return 'Weak', 'Password must include at least one lowercase letter.'

    # Check for the presence of special characters
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return 'Weak', 'Password must include at least one special character.'

    # If all checks pass, the password is considered strong
    return 'Strong', 'Your password is strong.'
