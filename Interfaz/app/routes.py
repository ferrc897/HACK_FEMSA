from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import db  # Updated import
from app.models import User, Product  # Import the User and Product models
import os
import csv

app = Blueprint('app', __name__)

UPLOAD_FOLDER = os.path.join('static', 'uploads')  # Ensure uploads folder is inside static
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
CSV_FILE = os.path.join(os.getcwd(), 'CSV.csv')  # Updated to use os.path.join

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

        upload_path = os.path.join('app', 'static', 'uploads', 'products')
        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, filename)
        product_image.save(file_path)

        new_product = Product(name=product_name, quantity=product_quantity, image=upload_path)
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('app.upload_product'))

    products = Product.query.all()
    return render_template('upload_product.html', products=products)


@app.route('/upload_shelf', methods=['GET', 'POST'])
def upload_shelf():
    shelf_image = 'uploads/planograma.png'  # Path relative to static folder
    if request.method == 'POST':
        if 'shelf_image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['shelf_image']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'planograma.png'  # Save the image as "planograma.png"
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
            os.makedirs(os.path.join('app', 'static', 'uploads'), exist_ok=True)
            file.save(file_path)
            print(f"Image saved at: {os.path.abspath(file_path)}")  # Print absolute path for debugging
            flash('Imagen del planograma subida exitosamente.', 'success')
            return redirect(url_for('app.upload_shelf'))
    return render_template('upload_shelf.html', shelf_image=shelf_image)

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

        # Save the image with the CB as its filename
        filename = secure_filename(f"{product_cb}.{product_image.filename.rsplit('.', 1)[1].lower()}")
        upload_path = os.path.join('app', 'static', 'uploads', 'products')
        os.makedirs(upload_path, exist_ok=True)  # Ensure the folder exists
        image_path = os.path.join(upload_path, filename)
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