import bcrypt
import requests
from flask import Flask, render_template, request, redirect, flash, url_for, session
from models import db, User
from config import Config

RECAPTCHA_SECRET = '6LevdWcrAAAAAOjngz_AEXOuGWNO81an-AGueTk5'  

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def verify_recaptcha(response):
    payload = {
        'secret': RECAPTCHA_SECRET,
        'response': response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    return r.json().get('success', False)

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        role = request.form.get('role')
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not verify_recaptcha(recaptcha_response):
            flash("CAPTCHA verification failed.", "error")
            return redirect(url_for('register'))

        if not username or not email or not password or not role:
            flash("All fields are required!", "error")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "error")
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = User(
            username=username,
            email=email,
            password=hashed_password.decode('utf-8'),
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not verify_recaptcha(recaptcha_response):
            flash("CAPTCHA verification failed.", "error")
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if user:
            if user.is_locked:
                flash("Account is locked.", "error")
                return redirect(url_for('login'))

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                user.failed_attempts = 0
                db.session.commit()
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                user.failed_attempts += 1
                if user.failed_attempts >= 5:
                    user.is_locked = True
                    flash("Account is locked due to too many failed attempts.", "error")
                db.session.commit()
                flash('Invalid credentials!', 'error')
                return redirect(url_for('login'))

        flash('Invalid credentials!', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

    if session.get('role') == 'admin':
        return render_template('dashboard_admin.html')
    return render_template('dashboard_user.html')

@app.route('/admin/users')
def view_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Access denied.", "error")
        return redirect(url_for('dashboard'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
