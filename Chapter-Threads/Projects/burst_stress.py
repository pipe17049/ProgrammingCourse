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
            timeout=5  # Aumentamos timeout para Windows
        )
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id', 'unknown')
            print(f"✅ {task_id[:8]}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION REFUSED - ¿API corriendo?")
        return False
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT - API sobrecargado")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def burst_attack(count=20, threads=10):
    """Ataque burst - múltiples threads simultáneos"""
    print(f"💥 BURST ATTACK: {count} tareas con {threads} threads")
    print("🎯 Objetivo: Saturar workers y llenar cola")
    print("=" * 50)
    
    # Lista compartida para resultados (thread-safe con GIL)
    results = []
    
    def wrapper_task():
        result = rapid_task()
        results.append(result)
    
    # Crear todas las threads de una vez
    threads_list = []
    for i in range(count):
        thread = threading.Thread(target=wrapper_task)
        threads_list.append(thread)
    
    # Lanzar todas simultáneamente
    start_time = time.time()
    for thread in threads_list:
        thread.start()
    
    print(f"🚀 {count} tareas lanzadas simultáneamente!")
    
    # Esperar a que terminen todas
    for thread in threads_list:
        thread.join()
    
    # Mostrar estadísticas
    success_count = sum(results)
    failed_count = len(results) - success_count
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS DEL BURST ATTACK:")
    print(f"✅ Exitosas: {success_count}/{count} ({success_count/count*100:.1f}%)")
    print(f"❌ Fallidas:  {failed_count}/{count} ({failed_count/count*100:.1f}%)")
    print(f"⏱️  Tiempo total: {elapsed_time:.2f}s")
    
    if failed_count > 0:
        print("\n🔍 POSIBLES CAUSAS DE FALLAS:")
        print("  - API no está corriendo (docker-compose up -d)")
        print("  - API sobrecargado (reducir count o aumentar timeout)")
        print("  - Límites de conexión en Windows")
    
    print("\n📊 VERIFICAR MÉTRICAS AHORA:")
    print("   python simple_monitoring/cli.py metrics")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    burst_attack(count)