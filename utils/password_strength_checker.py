import re

def password_strength(password):
    """Evaluate password strength."""
    if len(password) < 8:
        return 'Weak', 'Password must be at least 8 characters long.'
    if not re.search(r'[0-9]', password):
        return 'Weak', 'Password must include at least one numeral.'
    if not re.search(r'[A-Z]', password):
        return 'Weak', 'Password must include at least one uppercase letter.'
    if not re.search(r'[a-z]', password):
        return 'Weak', 'Password must include at least one lowercase letter.'
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return 'Weak', 'Password must include at least one special character.'

    return 'Strong', 'Your password is strong.'
