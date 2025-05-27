"""
Path: \telegram_assistant\management\commands\import_messages.py
"""

import os
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from telegram_assistant.models import Chat, Message
from telegram_assistant.utils import get_telegram_token

class Command(BaseCommand):
    help = 'Import messages from Telegram API'

    def handle(self, *args, **options):
        token = get_telegram_token()
        if not token:
            self.stdout.write(self.style.ERROR('No Telegram token found'))
            return
            
        # Obtener actualizaciones (solo para ejemplo)
        url = f'https://api.telegram.org/bot{token}/getUpdates'
        response = requests.get(url)
        
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Error: {response.text}'))
            return
            
        data = response.json()
        
        if not data.get('ok'):
            self.stdout.write(self.style.ERROR(f'API Error: {data.get("description")}'))
            return
            
        # Procesar resultados
        for update in data.get('result', []):
            if 'message' in update:
                message = update['message']
                chat_data = message.get('chat', {})
                
                # Crear o actualizar chat
                chat, created = Chat.objects.update_or_create(
                    chat_id=chat_data.get('id'),
                    defaults={
                        'type': chat_data.get('type'),
                        'title': chat_data.get('title'),
                        'username': chat_data.get('username'),
                        'first_name': chat_data.get('first_name'),
                        'last_name': chat_data.get('last_name'),
                    }
                )
                
                # Crear mensaje si no existe
                message_date = datetime.fromtimestamp(message.get('date')).replace(tzinfo=timezone.utc)
                
                Message.objects.get_or_create(
                    chat=chat,
                    message_id=message.get('message_id'),
                    defaults={
                        'from_user_id': message.get('from', {}).get('id'),
                        'from_user_name': message.get('from', {}).get('first_name'),
                        'date': message_date,
                        'text': message.get('text', ''),
                        'is_bot_message': message.get('from', {}).get('is_bot', False)
                    }
                )
                
        self.stdout.write(self.style.SUCCESS('Successfully imported messages'))