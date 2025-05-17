import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Earlier version used 'uploads' without 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)  # Create the folder if it doesn't exist

CSV_FILE = os.path.join(os.getcwd(), 'CSV.csv')  # Path to the CSV file

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    UPLOAD_FOLDER = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'local_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False