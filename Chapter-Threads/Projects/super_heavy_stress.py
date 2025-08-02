#!/usr/bin/env python3
"""
Super Heavy Stress - Tareas MUY pesadas para saturar workers
"""
import requests
import threading
import time
from datetime import datetime


def super_heavy_task():
    """Tarea súper pesada - 20MB + 5 filtros pesados"""
    payload = {
        "images": [
            "static/images/Clocktower_Panorama_20080622_20mb.jpg",
            "static/images/Clocktower_Panorama_20080622_20mb.jpg"  # 2x 20MB
        ],
        "filters": ["sharpen", "edges", "blur", "resize", "brightness"]  # 5 filtros pesados
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ {datetime.now().strftime('%H:%M:%S')} HEAVY: {task_id[:8]}")
            return True
    except:
        print(f"⚡ {datetime.now().strftime('%H:%M:%S')} Heavy task queued")
        return True


def super_heavy_burst(count=10):
    """Burst de tareas súper pesadas"""
    print(f"💀 SUPER HEAVY BURST: {count} tareas de 40MB + 5 filtros cada una")
    print("🎯 Objetivo: Saturar completamente los workers")
    print("=" * 60)
    
    # Lanzar todas las tareas simultáneamente
    threads = []
    for i in range(count):
        thread = threading.Thread(target=super_heavy_task)
        threads.append(thread)
        thread.start()
        time.sleep(0.2)  # Pequeña pausa entre threads
    
    print(f"\n💀 {count} tareas SÚPER PESADAS enviadas!")
    print("\n📊 VERIFICAR MÉTRICAS INMEDIATAMENTE:")
    print("   python simple_monitoring/cli.py metrics")
    print("\n🔄 Y luego monitoreo en vivo:")
    print("   python simple_monitoring/cli.py monitor --duration 60")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    super_heavy_burst(count)