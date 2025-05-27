// JavaScript para la interfaz tipo Telegram

document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos DOM
    const chatsList = document.querySelector('.chats-list');
    const messagesContainer = document.getElementById('messages-container');
    const messageInput = document.getElementById('message-text');
    const sendButton = document.querySelector('.btn-send');
    
    // Scroll al final de los mensajes
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Evento click en los chats
    if (chatsList) {
        const chatItems = chatsList.querySelectorAll('.chat-item');
        
        chatItems.forEach(item => {
            item.addEventListener('click', function() {
                const chatId = this.getAttribute('data-chat-id');
                window.location.href = `/chats/?chat_id=${chatId}`;
            });
        });
    }
    
    // Función para enviar mensaje (simulada)
    if (sendButton) {
        sendButton.addEventListener('click', function() {
            if (messageInput.value.trim() !== '') {
                // Aquí implementarías la lógica real de envío
                alert('En una implementación real, este mensaje se enviaría a través de la API de Telegram');
                messageInput.value = '';
            }
        });
    }
    
    // Permitir enviar con Enter
    if (messageInput) {
        messageInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendButton.click();
            }
        });
        
        // Auto-expandir el textarea
        messageInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
});