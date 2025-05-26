"""
Pat: ngrok_monitor/views.py
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .utils import (
    is_ngrok_running, get_ngrok_url, start_ngrok,
    check_env_file, get_telegram_token, mask_token, validate_telegram_token,
    get_bot_detailed_info
)

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
    
    return render(request, 'ngrok_monitor/monitor.html', context)

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
