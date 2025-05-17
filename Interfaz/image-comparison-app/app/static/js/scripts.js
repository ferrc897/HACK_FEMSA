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
});