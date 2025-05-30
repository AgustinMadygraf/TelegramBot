"""
Pat: telegram_assistant/views.py
"""

# Este archivo se mantiene para compatibilidad con código existente
# Eventualmente, podrías considerar eliminarlo y actualizar todas las referencias

from telegram_assistant.views.monitor import monitor_view, check_status
from telegram_assistant.views.chat import chats_view
from telegram_assistant.views.api import api_messages

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import (
    is_ngrok_running, get_ngrok_url, start_ngrok,
    check_env_file, get_telegram_token, mask_token, validate_telegram_token,
    get_bot_detailed_info
)
from .models import Chat, Message

def monitor_view(request):
    """Vista principal para monitorear ngrok y el token de Telegram"""
    message = None
    
    if request.method == "POST":
        if 'start_ngrok' in request.POST:
            # Verificar si ngrok ya está ejecutándose
            if is_ngrok_running():
                message = "ngrok ya está ejecutándose"
            else:
                # Iniciar ngrok si se presiona el botón y no está ejecutándose
                start_success = start_ngrok()
                if start_success:
                    message = "Se ha iniciado ngrok correctamente"
                else:
                    message = "Error al iniciar ngrok"
        elif 'refresh_bot_info' in request.POST:
            message = "Información del bot actualizada correctamente"
    
    # Verificar estado actual de ngrok
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None
    
    # Verificar archivo .env y token de Telegram
    env_exists = check_env_file()
    token = get_telegram_token() if env_exists else None
    masked_token = mask_token(token) if token else None
    token_valid, token_message = validate_telegram_token(token) if token else (False, "No hay token configurado")
    
    # Obtener información detallada del bot (desde caché si está disponible)
    bot_info = None
    if token and token_valid:
        force_refresh = 'refresh_bot_info' in request.POST
        bot_info = get_bot_detailed_info(token, force_refresh)
    
    context = {
        'ngrok_running': running,
        'ngrok_url': ngrok_url,
        'message': message,
        'env_exists': env_exists,
        'token_exists': token is not None,
        'masked_token': masked_token,
        'token_valid': token_valid,
        'token_message': token_message,
        'bot_info': bot_info,
    }
    
    return render(request, 'telegram_assistant/monitor.html', context)

def check_status(request):
    """Endpoint para verificar el estado de ngrok y token via AJAX"""
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None
    
    # También verificamos el estado del token
    env_exists = check_env_file()
    token = get_telegram_token() if env_exists else None
    masked_token = mask_token(token) if token else None
    token_valid, token_message = validate_telegram_token(token) if token else (False, "No hay token configurado")
    
    return JsonResponse({
        'running': running,
        'url': ngrok_url,
        'env_exists': env_exists,
        'token_exists': token is not None,
        'masked_token': masked_token,
        'token_valid': token_valid,
        'token_message': token_message,
    })

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

@csrf_exempt
def api_messages(request, chat_id):
    """API para cargar mensajes de un chat específico"""
    if request.method == 'GET':
        chat = get_object_or_404(Chat, chat_id=chat_id)
        
        # Opcionalmente, podemos implementar paginación
        last_id = request.GET.get('last_id')
        limit = int(request.GET.get('limit', 20))
        
        messages_query = chat.messages.all()
        if last_id:
            messages_query = messages_query.filter(message_id__lt=last_id)
        
        messages = messages_query.order_by('-date')[:limit]
        
        messages_data = [{
            'id': msg.message_id,
            'text': msg.text,
            'from_name': msg.from_user_name,
            'is_bot': msg.is_bot_message,
            'date': msg.date.strftime('%H:%M'),
            'timestamp': msg.date.timestamp()
        } for msg in messages]
        
        return JsonResponse({'messages': messages_data})
        
    return JsonResponse({'error': 'Method not allowed'}, status=405)
