#!/usr/bin/env python3
"""
Burst stress - Envía tareas en paralelo para saturar workers
"""
import requests
import threading
import time


def rapid_task():
    """Tarea súper pesada"""
    payload = {
        "images": ["static/images/Clocktower_Panorama_20080622_20mb.jpg"],
        "filters": ["sharpen", "edges", "blur", "resize", "brightness"]  # 5 filtros
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ {task_id[:8]}")
            return True
            
    except Exception as e:
        print(f"⚡ Error: {e}")
        print("⚡ Queued")
        return True


def burst_attack(count=20, threads=10):
    """Ataque burst - múltiples threads simultáneos"""
    print(f"💥 BURST ATTACK: {count} tareas con {threads} threads")
    print("🎯 Objetivo: Saturar workers y llenar cola")
    print("=" * 50)
    
    # Crear todas las threads de una vez
    threads_list = []
    for i in range(count):
        thread = threading.Thread(target=rapid_task)
        threads_list.append(thread)
    
    # Lanzar todas simultáneamente
    for thread in threads_list:
        thread.start()
    
    print(f"🚀 {count} tareas lanzadas simultáneamente!")
    print("\n📊 VERIFICAR MÉTRICAS EN 2-3 SEGUNDOS:")
    print("   python simple_monitoring/cli.py metrics")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    burst_attack(count)