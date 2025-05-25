from django.shortcuts import render
from django.http import JsonResponse
from .utils import is_ngrok_running, get_ngrok_url, start_ngrok
import time

def monitor_view(request):
    """Vista principal para monitorear ngrok"""
    if request.method == "POST" and 'start_ngrok' in request.POST:
        # Iniciar ngrok si se presiona el botón
        start_ngrok()
        # Esperar un poco para que ngrok inicie
        time.sleep(2)
        
    # Verificar estado actual de ngrok
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None
    
    context = {
        'ngrok_running': running,
        'ngrok_url': ngrok_url,
    }
    
    return render(request, 'ngrok_monitor/monitor.html', context)

def check_status(request):
    """Endpoint para verificar el estado de ngrok via AJAX"""
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None
    
    return JsonResponse({
        'running': running,
        'url': ngrok_url,
    })
