document.addEventListener('DOMContentLoaded', function() {
    const productUploadForm = document.getElementById('product-upload-form');
    const shelfUploadForm = document.getElementById('shelf-upload-form');

    if (productUploadForm) {
        productUploadForm.addEventListener('submit', function(event) {
            const productImage = document.getElementById('product_image').files[0];
            if (!productImage) {
                alert('Please upload a product image.');
                event.preventDefault();
            }
        });
    }

    if (shelfUploadForm) {
        shelfUploadForm.addEventListener('submit', function(event) {
            const shelfImage = document.getElementById('shelf_image').files[0];
            if (!shelfImage) {
                alert('Please upload a shelf image.');
                event.preventDefault();
            }
        });
    }

    const showLoginLink = document.getElementById('show-login');
    const showRegisterLink = document.getElementById('show-register');
    const registerSection = document.getElementById('register-section');
    const loginSection = document.getElementById('login-section');

    if (showLoginLink && showRegisterLink && registerSection && loginSection) {
        showLoginLink.addEventListener('click', function(event) {
            event.preventDefault();
            registerSection.style.display = 'none';
            loginSection.style.display = 'block';
        });

        showRegisterLink.addEventListener('click', function(event) {
            event.preventDefault();
            loginSection.style.display = 'none';
            registerSection.style.display = 'block';
        });
    }
});