from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User  # Import the User model
import os

app = Blueprint('app', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(request.url)

        # Check if password is at least 8 characters long
        if len(password) < 8:
            flash('Password must be at least 8 characters long!', 'error')
            return redirect(request.url)

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered!', 'error')
            return redirect(request.url)

        # Save user to the local database
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('app.login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password!', 'error')
            return redirect(request.url)

        # Log the user in
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login successful!', 'success')
        return redirect(url_for('app.home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('app.login'))

@app.route('/upload_product', methods=['GET', 'POST'])
def upload_product():
    if request.method == 'POST':
        if 'product_image' not in request.files:  # Cambiado de 'file' a 'product_image'
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['product_image']  # Cambiado de 'file' a 'product_image'
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('Product image uploaded successfully!', 'success')
            return redirect(url_for('app.home'))
    return render_template('upload_product.html')

@app.route('/upload_shelf', methods=['GET', 'POST'])
def upload_shelf():
    if request.method == 'POST':
        if 'shelf_image' not in request.files:  # Cambiado de 'file' a 'shelf_image'
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['shelf_image']  # Cambiado de 'file' a 'shelf_image'
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('Shelf image uploaded successfully!', 'success')
            return redirect(url_for('app.home'))
    return render_template('upload_shelf.html')

@app.route('/test')
def test():
    return "Flask is working!"