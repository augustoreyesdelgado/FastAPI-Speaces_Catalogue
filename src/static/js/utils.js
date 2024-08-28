const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const dropzoneText = document.getElementById('dropzone-text');
const registerForm = document.getElementById('registerForm');

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

    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const formData = new FormData(registerForm);
        const data = Object.fromEntries(formData.entries());

        const payload = {
            imagen: formData.imagen,
        };

        try {

            const response = await fetch(`/catalogo/clasifica`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                const { resultado, image_url, certeza } = data;  // Agregar certeza aquí

                // Crear un nuevo formulario para enviar los datos mediante POST
                const resultForm = document.createElement('form');
                resultForm.method = 'POST';
                resultForm.action = '/catalogo/results-page';

                // Agregar los datos al formulario
                const resultadoInput = document.createElement('input');
                resultadoInput.type = 'hidden';
                resultadoInput.name = 'resultado';
                resultadoInput.value = resultado;
                resultForm.appendChild(resultadoInput);

                const imageUrlInput = document.createElement('input');
                imageUrlInput.type = 'hidden';
                imageUrlInput.name = 'image_url';
                imageUrlInput.value = image_url;
                resultForm.appendChild(imageUrlInput);

                const certezaInput = document.createElement('input');  // Agregar certeza aquí
                certezaInput.type = 'hidden';
                certezaInput.name = 'certeza';
                certezaInput.value = certeza;
                resultForm.appendChild(certezaInput);

                document.body.appendChild(resultForm);
                resultForm.submit();  // Enviar el formulario

            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
    }
/*
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        var url = window.location.pathname;
        const todoId = url.substring(url.lastIndexOf('/') + 1);

        const payload = {
            title: data.title,
            description: data.description,
            priority: parseInt(data.priority),
            complete: data.complete === "on"
        };

        try {
            const token = getCookie('access_token');
            console.log(token)
            if (!token) {
                throw new Error('Authentication token not found');
            }

            console.log(`${todoId}`)

            const response = await fetch(`/todos/todo/${todoId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                window.location.href = '/todos/todo-page'; // Redirect to the todo page
            } else {
                // Handle error
                const errorData = await response.json();
                alert(`Error: ${errorData.detail}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });
    }*/