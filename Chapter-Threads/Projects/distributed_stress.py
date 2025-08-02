#!/usr/bin/env python3
"""
Stress distribuido simple - Llena la cola Redis para ver cambios en recomendaciones
"""
import requests
import time
import threading


def create_distributed_task():
    """Crear una tarea distribuida"""
    payload = {
        "images": ["static/images/Clocktower_Panorama_20080622_20mb.jpg"],
        "filters": ["sharpen", "edges", "resize"]
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/process-batch/distributed/",
            json=payload,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ Task created: {task_id[:8]}...")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def rapid_stress(count=10):
    """Generar stress rápido para llenar la cola"""
    print(f"🔥 Generando {count} tareas distribuidas rápidamente...")
    print("=" * 50)
    
    # Crear tareas en paralelo para llenar la cola rápido
    threads = []
    for i in range(count):
        thread = threading.Thread(target=create_distributed_task)
        threads.append(thread)
        thread.start()
        time.sleep(0.1)  # Pequeña pausa entre threads
    
    # Esperar a que terminen
    for thread in threads:
        thread.join()
    
    print(f"\n🎯 {count} tareas enviadas al sistema distribuido!")
    print("📊 Ahora verifica las métricas para ver cambios en recomendaciones:")
    print("   python simple_monitoring/cli.py metrics")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    rapid_stress(count)