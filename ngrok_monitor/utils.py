"""
path: ngrok_monitor/urls.py
"""

import requests
import subprocess
import time

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
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error al iniciar ngrok: {e}")
        return False
