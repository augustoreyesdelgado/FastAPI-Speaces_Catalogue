const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const dropzoneText = document.getElementById('dropzone-text');

dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropzone.classList.add('border-blue-500');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('border-blue-500');
});

dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropzone.classList.remove('border-blue-500');
    const files = event.dataTransfer.files;
    handleFiles(files);
});

fileInput.addEventListener('change', (event) => {
    const files = event.target.files;
    handleFiles(files);
});

function handleFiles(files) {
    if (files.length > 1) {
        alert("Solo se permite cargar una imagen.");
        return;
    }
    const file = files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = () => {
            preview.src = reader.result;
            preview.classList.remove('hidden');
            dropzoneText.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    } else {
        alert("Solo se permite cargar archivos de imagen.");
    }
}