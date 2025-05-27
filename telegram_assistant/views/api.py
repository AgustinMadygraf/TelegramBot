# telegram_assistant/views/api.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from telegram_assistant.models import Chat

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