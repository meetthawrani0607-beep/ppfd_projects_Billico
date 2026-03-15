/**
 * Bill Upload Functionality
 * Handle file upload and preview
 */

document.addEventListener('DOMContentLoaded', function () {
    initUploadPage();
});

/**
 * Initialize Upload Page
 */
function initUploadPage() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('billFile');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const uploadBtn = document.getElementById('uploadBtn');

    if (!uploadForm || !fileInput) return;

    // File input change event
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];

        if (file) {
            previewFile(file, previewContainer, imagePreview);
        }
    });

    // Form submit event
    uploadForm.addEventListener('submit', function (e) {
        const originalText = uploadBtn.innerHTML;
        Billico.showLoading(uploadBtn);

        // Form will submit normally, but show loading state
        setTimeout(() => {
            if (uploadBtn) {
                uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        }, 100);
    });

    // Drag and drop
    initDragAndDrop(fileInput, previewContainer, imagePreview);
}

/**
 * Preview Image File
 */
function previewFile(file, container, imgElement) {
    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];

    if (!validTypes.includes(file.type)) {
        Billico.showToast('Invalid file type. Please upload JPG, PNG, or PDF', 'danger');
        return;
    }

    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        Billico.showToast('File size must be less than 16MB', 'danger');
        return;
    }

    // Show preview for images
    if (file.type.startsWith('image/')) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imgElement.src = e.target.result;
            container.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else if (file.type === 'application/pdf') {
        // For PDF, show a placeholder
        imgElement.src = '/static/images/pdf-icon.png';
        container.style.display = 'block';
    }

    // Update file name display
    const fileNameDisplay = document.getElementById('fileName');
    if (fileNameDisplay) {
        fileNameDisplay.textContent = file.name;
    }
}

/**
 * Drag and Drop Functionality
 */
function initDragAndDrop(fileInput, previewContainer, imagePreview) {
    const dropZone = document.querySelector('.upload-area');

    if (!dropZone) return;

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop zone when dragging over
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, function () {
            dropZone.classList.add('drag-over');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, function () {
            dropZone.classList.remove('drag-over');
        }, false);
    });

    // Handle dropped files
    dropZone.addEventListener('drop', function (e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            previewFile(files[0], previewContainer, imagePreview);
        }
    }, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
}

/**
 * Review Page - Item Selection
 */
function initReviewPage() {
    const selectAllCheckbox = document.getElementById('selectAll');
    const itemCheckboxes = document.querySelectorAll('.item-checkbox');

    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function () {
            itemCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }

    // Update category/supplier for all items
    const globalCategory = document.getElementById('globalCategory');
    const globalSupplier = document.getElementById('globalSupplier');

    if (globalCategory) {
        globalCategory.addEventListener('change', function () {
            document.querySelectorAll('[name^="category_"]').forEach(select => {
                select.value = this.value;
            });
        });
    }

    if (globalSupplier) {
        globalSupplier.addEventListener('change', function () {
            document.querySelectorAll('[name^="supplier_"]').forEach(select => {
                select.value = this.value;
            });
        });
    }
}

// Initialize review page if exists
if (document.querySelector('.review-page')) {
    document.addEventListener('DOMContentLoaded', initReviewPage);
}
