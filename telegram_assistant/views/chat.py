# telegram_assistant/views/chat.py
from django.shortcuts import render, get_object_or_404
from telegram_assistant.models import Chat, Message

def chats_view(request):
    """Vista principal que muestra la lista de chats y el chat seleccionado"""
    chats = Chat.objects.all()
    
    # Si hay chats y no se especificó un chat_id, mostrar el primero
    selected_chat_id = request.GET.get('chat_id')
    selected_chat = None
    messages = []
    
    if chats.exists():
        if selected_chat_id:
            selected_chat = get_object_or_404(Chat, chat_id=selected_chat_id)
        else:
            selected_chat = chats.first()
        
        if selected_chat:
            messages = selected_chat.messages.all()[:50]  # Últimos 50 mensajes
    
    return render(request, 'telegram_assistant/chats.html', {
        'chats': chats,
        'selected_chat': selected_chat,
        'messages': messages,
    })