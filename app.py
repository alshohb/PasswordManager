from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.password_strength_checker import password_strength
from utils.password_generator import generate_password
from models.user import User

app = Flask(__name__)
app.secret_key = 'Shihab2001'  # Use a secure, random secret key

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/generate_password', methods=['POST'])
def generate():
    length = int(request.form.get('length', 12))
    new_password = generate_password(length)
    return render_template('home.html', generated_password=new_password)

@app.route('/check_strength', methods=['POST'])
def check():
    password = request.form['password']
    strength, message = password_strength(password)
    flash(message)
    return render_template('home.html', strength=strength, message=message, checked_password=password)

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    strength, message = password_strength(password)
    if strength == 'Weak':
        flash(message)
        return redirect(url_for('home'))
    try:
        user = User(username, password)
        user.create()
        flash('User registered successfully!')
    except Exception as e:
        flash('Registration failed: ' + str(e))
    return redirect(url_for('home'))

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
        flash('Login failed: ' + str(e))
    return redirect(url_for('home'))

@app.route('/user_dashboard')
def user_dashboard():
    if 'username' not in session:
        flash('Please login to view this page.')
        return redirect(url_for('login'))
    entries = User.get_user_entries(session['username'])
    return render_template('user_dashboard.html', username=session['username'], entries=entries)

@app.route('/master_dashboard')
def master_dashboard():
    if 'username' not in session or session['username'] != 'masteruser':
        flash('Unauthorized access.')
        return redirect(url_for('home'))
    entries = User.get_all_entries()
    return render_template('master_dashboard.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
