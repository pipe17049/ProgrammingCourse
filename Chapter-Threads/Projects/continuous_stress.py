#!/usr/bin/env python3
"""
Stress continuo - Mantiene enviando tareas para mantener cola llena
"""
import requests
import threading
import time
from datetime import datetime


def heavy_task():
    """Tarea muy pesada"""
    payload = {
        "images": ["static/images/Clocktower_Panorama_20080622_20mb.jpg"] * 2,  # 2 imágenes de 20MB
        "filters": ["sharpen", "edges", "blur", "resize", "brightness"]  # 5 filtros cada una
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=1
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} {task_id[:8]}")
            return True
    except:
        print(f"⚡ {datetime.now().strftime('%H:%M:%S')} Queued")
        return True


def continuous_load(duration=30, rate=5):
    """Carga continua - envía X tareas por segundo"""
    print(f"🔥 CARGA CONTINUA: {rate} tareas/segundo por {duration} segundos")
    print("🎯 Objetivo: Mantener cola llena constantemente")
    print("=" * 60)
    
    end_time = time.time() + duration
    
    while time.time() < end_time:
        # Enviar múltiples tareas por segundo
        threads = []
        for _ in range(rate):
            thread = threading.Thread(target=heavy_task)
            threads.append(thread)
            thread.start()
        
        # Esperar un segundo antes del siguiente batch
        time.sleep(1)
    
    print(f"\n🎯 Carga continua terminada!")
    print("📊 VERIFICAR MÉTRICAS AHORA:")
    print("   python simple_monitoring/cli.py metrics")


if __name__ == "__main__":
    import sys
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    continuous_load(duration)