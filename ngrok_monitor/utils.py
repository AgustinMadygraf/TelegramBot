"""
path: ngrok_monitor/urls.py
"""

import os
import subprocess
import time
from pathlib import Path
import requests
from dotenv import load_dotenv
import json
import datetime

# Ruta al archivo .env en la raíz del proyecto
ENV_PATH = Path(__file__).resolve().parent.parent / '.env'

# Ruta para guardar la caché
CACHE_DIR = Path(__file__).resolve().parent / 'cache'
BOT_INFO_CACHE_FILE = CACHE_DIR / 'bot_info_cache.json'
CACHE_EXPIRY_HOURS = 1  # La caché expira después de 1 hora

def is_ngrok_running():
    """Verifica si ngrok está corriendo comprobando el puerto 4040"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_ngrok_url():
    """Obtiene la URL pública de ngrok desde su API local"""
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=1)
        if response.status_code == 200:
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
            if tunnels:
                return tunnels[0].get('public_url')
        return None
    except requests.exceptions.RequestException:
        return None

def start_ngrok():
    """Inicia ngrok solo si no está ya en ejecución"""
    # Verificar primero si ngrok ya está ejecutándose
    if is_ngrok_running():
        print("ngrok ya está ejecutándose. No se iniciará otra instancia.")
        return True

    try:
        # Inicia ngrok en una nueva ventana de cmd
        subprocess.Popen(
            ['cmd.exe', '/c', 'start', 'cmd', '/k', 'ngrok', 'http', '8000'],
            shell=True,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        # Esperar un momento para permitir que ngrok inicie
        time.sleep(2)
        return True
    except (FileNotFoundError, subprocess.SubprocessError) as e:
        print(f"Error al iniciar ngrok: {e}")
        return False

def check_env_file():
    """Verifica si existe el archivo .env"""
    return ENV_PATH.exists()

def get_telegram_token():
    """Obtiene el token de Telegram desde el archivo .env"""
    if not check_env_file():
        return None

    load_dotenv(ENV_PATH)
    return os.getenv('TELEGRAM_TOKEN')

def mask_token(token):
    """Oculta parcialmente el token para mostrar en la interfaz"""
    if not token:
        return None

    # Si el token tiene formato típico "123456789:ABC..."
    if ':' in token:
        parts = token.split(':')
        #Mostrar primero 6 caracteres del ID, último caracter, luego 4 primeros y 3 últimos del hash
        masked_id = parts[0][:6] + '*' * (len(parts[0]) - 7) + parts[0][-1]
        hash_part = parts[1]
        masked_hash = hash_part[:4] + '*' * (len(hash_part) - 7) + hash_part[-3:]
        return f"{masked_id}:{masked_hash}"
    else:
        # Si el token no tiene el formato esperado, mostrar solo primeros y últimos caracteres
        return token[:6] + '*' * (len(token) - 9) + token[-3:]

def validate_telegram_token(token):
    """Valida el token de Telegram usando la API de Telegram"""
    if not token:
        return False, "No se encontró token"

    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                return True, data['result']['username']
        return False, f"Token inválido: {response.json().get('description', 'Error desconocido')}"
    except requests.exceptions.RequestException as e:
        return False, f"Error de conexión: {str(e)}"

def ensure_cache_dir():
    """Asegura que el directorio de caché exista"""
    CACHE_DIR.mkdir(exist_ok=True)

def get_cached_bot_info():
    """Obtiene la información del bot desde la caché si está disponible y es válida"""
    if not BOT_INFO_CACHE_FILE.exists():
        return None
    
    try:
        cache_data = json.loads(BOT_INFO_CACHE_FILE.read_text('utf-8'))
        # Verificar si la caché ha expirado
        cached_time = datetime.datetime.fromisoformat(cache_data.get('timestamp', ''))
        now = datetime.datetime.now()
        if now - cached_time > datetime.timedelta(hours=CACHE_EXPIRY_HOURS):
            return None  # Caché expirada
        return cache_data.get('data')
    except:
        return None

def save_bot_info_to_cache(bot_info):
    """Guarda la información del bot en la caché"""
    ensure_cache_dir()
    cache_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'data': bot_info
    }
    BOT_INFO_CACHE_FILE.write_text(json.dumps(cache_data), 'utf-8')

def get_bot_detailed_info(token, force_refresh=False):
    """Obtiene información detallada del bot usando getMe, con caché"""
    if not token:
        return None
    
    # Si no se fuerza la actualización, intentar obtener de la caché
    if not force_refresh:
        cached_info = get_cached_bot_info()
        if cached_info:
            return cached_info
    
    # Si llegamos aquí, necesitamos obtener nueva información de la API
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                # Guardar en caché
                save_bot_info_to_cache(bot_info)
                return bot_info
        return None
    except requests.exceptions.RequestException:
        return None
