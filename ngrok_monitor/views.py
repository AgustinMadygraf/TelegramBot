"""
Pat: ngrok_monitor/views.py
"""

from django.shortcuts import render
from django.http import JsonResponse
from .utils import is_ngrok_running, get_ngrok_url, start_ngrok

def monitor_view(request):
    """Vista principal para monitorear ngrok"""
    message = None

    if request.method == "POST" and 'start_ngrok' in request.POST:
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

    # Verificar estado actual de ngrok
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None

    context = {
        'ngrok_running': running,
        'ngrok_url': ngrok_url,
        'message': message,
    }

    return render(request, 'ngrok_monitor/monitor.html', context)

from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def check_status(_request):
    """Endpoint para verificar el estado de ngrok via AJAX"""
    running = is_ngrok_running()
    ngrok_url = get_ngrok_url() if running else None

    return JsonResponse({
        'running': running,
        'url': ngrok_url,
    })
