from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.password_strength_checker import password_strength
from utils.password_generator import generate_password
from models.user import User

app = Flask(__name__)
app.secret_key = 'Shihab2001'  # Secure, random secret key for session management

# Home route displays the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Generates a strong password and displays it on the home page
@app.route('/generate_password', methods=['POST'])
def generate():
    length = int(request.form.get('length', 12))
    new_password = generate_password(length)
    return render_template('home.html', generated_password=new_password)

# Checks the strength of the user-inputted password and displays results
@app.route('/check_strength', methods=['POST'])
def check():
    password = request.form['password']
    strength, message = password_strength(password)
    flash(message)
    return render_template('home.html', strength=strength, message=message, checked_password=password)

# Registers a new user if the password is strong enough
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    website = request.form.get('website', 'defaultsite.com')  # Adjust as needed
    site_username = request.form.get('site_username', username)  # Adjust as needed

    strength, message = password_strength(password)
    if strength == 'Weak':
        flash(message)
        return redirect(url_for('home'))
    try:
        user = User(username, password)
        user.create()
        user.save_password(website, site_username, password)  # Save password for the website
        flash('User registered and password saved successfully!')
    except Exception as e:
        flash(f'Registration failed: {str(e)}')
        return redirect(url_for('home'))

    return redirect(url_for('home'))


# Handles user login and redirects based on user type
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        valid_login = User.login(username, password)
        if valid_login:
            session['username'] = username
            if username == 'masteruser':
                flash('Master logged in successfully!')
                return redirect(url_for('master_dashboard'))
            else:
                flash('Logged in successfully!')
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password')
    except Exception as e:
        flash(f'Login failed: {str(e)}')
    return redirect(url_for('home'))

# Displays user-specific entries on the user dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session:
        flash('Please login to view this page.')
        return redirect(url_for('login'))
    entries = User.get_user_entries(session['username'], key='my_secret_master_key')
    print(f"Entries for {session['username']}: {entries}")  # Debugging line
    if not entries:
        flash('No password entries found for your account.')
    return render_template('user_dashboard.html', username=session['username'], entries=entries)

# Master dashboard view showing all entries in the database
@app.route('/master_dashboard')
def master_dashboard():
    if 'username' not in session or session['username'] != 'masteruser':
        flash('Unauthorized access.')
        return redirect(url_for('home'))
    entries = User.get_all_entries()
    return render_template('master_dashboard.html', entries=entries)

# Main function to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
