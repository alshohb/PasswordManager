from flask import Flask, render_template, request, redirect, url_for, flash, session
from utils.password_strength_checker import password_strength
from utils.password_generator import generate_password
from models.user import User

app = Flask(__name__)
app.secret_key = 'Shihab2001'  # Use a secure, random secret key

@app.route('/', methods=['GET'])
def home():
    # Pass any flashed messages to the template
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
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    except Exception as e:
        flash('Login failed: ' + str(e))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
