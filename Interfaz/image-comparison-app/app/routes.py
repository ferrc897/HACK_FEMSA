from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User, Product  # Import the User and Product models
import os
import csv

app = Blueprint('app', __name__)

UPLOAD_FOLDER = 'uploads'  # Ensure this matches the folder name
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
CSV_FILE = 'CSV.csv'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_inventory():
    inventory = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:  # Ensure proper encoding
            reader = csv.DictReader(file)
            for row in reader:
                inventory.append({'name': row['Nombre'], 'quantity': 10})  # Add dummy quantity
    return inventory

def write_inventory(product_name, product_quantity, product_image):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'quantity', 'image'])
        if not file_exists:
            writer.writeheader()
        writer.writerow({'name': product_name, 'quantity': product_quantity, 'image': product_image})

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
    return redirect(url_for('app.auth'))

@app.route('/upload_product', methods=['GET', 'POST'])
def upload_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_quantity = request.form['product_quantity']
        product_image = request.files['product_image']

        if not product_image or not allowed_file(product_image.filename):
            flash('Invalid file or no file selected!', 'error')
            return redirect(request.url)

        filename = secure_filename(product_image.filename)
        product_image.save(os.path.join(UPLOAD_FOLDER, filename))

        # Save product to the database
        new_product = Product(name=product_name, quantity=product_quantity, image=filename)
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('app.upload_product'))

    # Fetch all products from the database
    products = Product.query.all()
    return render_template('upload_product.html', products=products)

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

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if 'register' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                flash('Passwords do not match!', 'error')
                return redirect(request.url)

            if len(password) < 8:
                flash('Password must be at least 8 characters long!', 'error')
                return redirect(request.url)

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered!', 'error')
                return redirect(request.url)

            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(request.url)

        elif 'login' in request.form:
            email = request.form['email']
            password = request.form['password']

            user = User.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('Invalid email or password!', 'error')
                return redirect(request.url)

            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('app.home'))

    return render_template('register_login.html')

# Dummy database for inventory
inventory_db = []

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        product_cb = request.form['product_cb']
        product_name = request.form['product_name']
        product_quantity = request.form['product_quantity']
        product_image = request.files['product_image']

        if not product_image or not allowed_file(product_image.filename):
            flash('Invalid file or no file selected!', 'error')
            return redirect(request.url)

        # Rename the image file to the CB value
        filename = secure_filename(f"{product_cb}.{product_image.filename.rsplit('.', 1)[1].lower()}")
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists
        product_image.save(image_path)

        # Add the product to the dummy database
        inventory_db.append({
            'cb': product_cb,
            'name': product_name,
            'quantity': product_quantity,
            'image': filename,
            'charola': 'N/A',  # Dummy data for charola
            'posicion': 'N/A',  # Dummy data for posicion
            'frentes': 'N/A'  # Dummy data for frentes
        })

        flash('Product added successfully!', 'success')
        return redirect(url_for('app.inventory'))

    # Pass the dummy database to the template
    return render_template('inventory.html', products=inventory_db)