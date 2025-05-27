// static/js/monitor.js
// Lógica para actualizar el estado de ngrok y la interfaz en el monitor

setInterval(function() {
    fetch('/check-status/')
        .then(response => response.json())
        .then(data => {
            const statusEl = document.getElementById('status-text');
            if (!statusEl) return;

            if (data.running) {
                statusEl.innerHTML = '<i class="bi bi-check-circle-fill"></i> ngrok está ejecutándose';
                statusEl.className = 'fs-4 my-3 status-running';

                // Actualizar o agregar la URL de ngrok
                const urlContainer = document.getElementById('ngrok-url');
                if (urlContainer) {
                    urlContainer.innerHTML = `<strong>URL pública:</strong> <a href="${data.url}" target="_blank" class="text-decoration-none">${data.url}</a>`;
                } else {
                    const newUrlContainer = document.createElement('div');
                    newUrlContainer.id = 'ngrok-url';
                    newUrlContainer.className = 'alert alert-info ngrok-url';
                    newUrlContainer.innerHTML = `<strong>URL pública:</strong> <a href="${data.url}" target="_blank" class="text-decoration-none">${data.url}</a>`;
                    document.querySelector('.card.mb-4').appendChild(newUrlContainer);
                }

                // Ocultar el botón si ngrok está corriendo
                const form = document.querySelector('form');
                if (form) form.style.display = 'none';
            } else {
                statusEl.innerHTML = '<i class="bi bi-x-circle-fill"></i> ngrok no está ejecutándose';
                statusEl.className = 'fs-4 my-3 status-not-running';

                // Mostrar el botón si ngrok no está corriendo
                const form = document.querySelector('form');
                if (!form) {
                    const newForm = document.createElement('form');
                    newForm.method = 'post';
                    newForm.innerHTML = document.getElementById('csrf-token-template').innerHTML + '<button type="submit" name="start_ngrok" class="btn btn-success btn-lg">Iniciar ngrok</button>';
                    document.querySelector('.card.mb-4').appendChild(newForm);
                } else {
                    form.style.display = 'block';
                }

                // Eliminar la URL de ngrok si existe
                const urlContainer = document.getElementById('ngrok-url');
                if (urlContainer) {
                    urlContainer.remove();
                }
            }
        });
}, 5000);
