# Image Comparison Application

This project is an image comparison application built using Flask. It allows users to register, upload images of various products, and upload images of store shelves for comparison with preloaded images.

## Features

- User registration (stored locally using SQLite)
- Image upload for product images
- Image upload for store shelf images
- Comparison functionality with preloaded images

## Project Structure

```
image-comparison-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── scripts.js
│   ├── templates
│   │   ├── base.html
│   │   ├── register.html
│   │   ├── upload_product.html
│   │   └── upload_shelf.html
│   └── utils.py
├── instance
│   └── config.py
├── migrations
├── requirements.txt
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd image-comparison-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r ./Interfaz/image-comparison-app/requirements.txt
   ```

4. Run the application:
   ```
   python ./Interfaz/image-comparison-app/run.py
   ```

5. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

1. Register a new account or log in if you already have one.

2. Navigate to the upload sections to upload product images and store shelf images for comparison.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.