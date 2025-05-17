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

    const inventoryTable = document.getElementById('inventory-table');
    const modal = document.getElementById('product-modal');
    const modalCharola = document.getElementById('modal-charola');
    const modalPosicion = document.getElementById('modal-posicion');
    const modalFrentes = document.getElementById('modal-frentes');
    const modalImage = document.getElementById('modal-image');
    const closeModal = document.querySelector('.modal .close');

    if (inventoryTable) {
        inventoryTable.addEventListener('click', function(event) {
            const row = event.target.closest('tr');
            if (row) {
                modalCharola.textContent = row.dataset.charola || 'N/A';
                modalPosicion.textContent = row.dataset.posicion || 'N/A';
                modalFrentes.textContent = row.dataset.frentes || 'N/A';

                // Read the data-image attribute and assign it to the modal image src
                const imageSrc = row.dataset.image;
                if (imageSrc) {
                    modalImage.src = imageSrc;
                } else {
                    modalImage.src = ''; // Clear the image if no source is found
                }

                modal.style.display = 'flex';
            }
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});