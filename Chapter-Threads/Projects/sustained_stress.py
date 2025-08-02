#!/usr/bin/env python3
"""
Stress continuo - Mantiene la cola llena para ver cambios en recomendaciones
"""
import requests
import time
import threading
from datetime import datetime


def create_heavy_task():
    """Crear tarea pesada distribuida"""
    payload = {
        "images": ["static/images/Clocktower_Panorama_20080622_20mb.jpg"],
        "filters": ["sharpen", "edges", "resize", "blur", "brightness"]  # 5 filtros pesados
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=2  # Timeout corto para que se acumulen
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} Task: {task_id[:8]}...")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} Task queued (timeout)")
        return True  # Timeout significa que se está procesando


def sustained_load(duration=20, rate=3):
    """Carga sostenida durante X segundos"""
    print(f"🔥 Carga sostenida: {rate} tareas/segundo por {duration} segundos")
    print("🎯 Objetivo: Mantener cola llena para ver cambios en recomendaciones")
    print("=" * 60)
    
    start_time = time.time()
    task_count = 0
    
    # Crear tareas continuas
    while time.time() - start_time < duration:
        # Crear múltiples tareas por segundo
        for _ in range(rate):
            threading.Thread(target=create_heavy_task).start()
            task_count += 1
            time.sleep(1/rate)  # Distribuir en el segundo
    
    print(f"\n🎯 {task_count} tareas pesadas enviadas!")
    print("\n📊 AHORA VERIFICA MÉTRICAS INMEDIATAMENTE:")
    print("   python simple_monitoring/cli.py metrics")
    print("\n💡 Y luego espera 10-15 segundos y verifica de nuevo")


if __name__ == "__main__":
    import sys
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    sustained_load(duration)